# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import base64
import os
from collections import defaultdict
from io import BytesIO
from operator import itemgetter
from re import findall
from urllib.parse import unquote

import numpy as np
from inkex import Color, Group
from inkex import Image as InkexImage
from inkex import Path, PathElement
from PIL import Image, ImageChops, ImageDraw, ImageEnhance
from shapely import make_valid, unary_union
from shapely.affinity import translate

from ...stitches.utils.cross_stitch import CrossGeometries
from ...svg import PIXELS_PER_MM, get_correction_transform
from ...threads import ThreadPalette
from ...utils.geometry import ensure_multi_polygon


class BitmapToCrossStitch(object):
    ''' Bitmap to pixel fill, used within the cross stitch helper extension.
        It basically takes a selected image and generates the cross stitch pixels by also trying to combine as many as possible.
    '''
    def __init__(self, svg, bitmap, settings, palette=None):
        '''Prepare the bitmap image:
            * self.reduced_image:       scaled pillow image with reduced colors
                                        known limitations:
                                        rotations or skewing is not applied
            * self.rgb_image            same as reduced_image, but in rgb mode
            * self.initial_alpha:       a mask for the intial alpha channel

           Parameters:
           * svg:       the svg document
           * bitmap:    Ink/Stitch Image insance
           * settings:  dictionary with cross stitch settings
           * palette:   flat list with rgb values (optional)
        '''
        if not isinstance(bitmap.node, InkexImage):
            return

        self.svg = svg
        self.bitmap = bitmap
        self.settings = settings
        self.palette = palette
        self.prepared_image = None
        self.reduced_image = None
        self.rgb_image = None
        self.initial_alpha = None
        self.alpha_mask = None

        image = self._get_image_byte_string(bitmap.node)
        if image is None:
            # Could not find image data, abort
            return

        minx, miny, width, height = self._get_unclipped_dimensions()

        if not all((width, height)):
            # Image has zero width or height, abort
            return

        with Image.open(image) as img:
            self.image = img
            self.prepared_image = self.image.resize((width, height))

        # ensure rgba mode
        self.prepared_image = self.prepared_image.convert("RGBA")
        self.reduced_image = self.prepared_image

        # Get initial alpha mask
        self.initial_alpha = self.reduced_image.getchannel("A")
        self.initial_alpha = self.initial_alpha.point(lambda a: 255 if a > 0 else 0)

        self.apply_color_corrections()

        # Transform after color adaptions to avoid additional background color sections
        self.reduced_image = self.apply_transform(self.reduced_image)

    def _get_unclipped_dimensions(self):
        # Image bounds of the unclipped image
        minx, miny, maxx, maxy = self.bitmap.original_shape.bounds
        width = int(maxx - minx)
        height = int(maxy - miny)
        return minx, miny, width, height

    def apply_transform(self, image):
        # Map original image corners on transformed image corners
        # Move original shape to the top corner
        if image is None:
            return

        minx, miny, width, height = self._get_unclipped_dimensions()
        bitmap_shape_at_origin = translate(self.bitmap.original_shape, -minx, -miny)
        # get transform data
        transform_data = self.get_transform_data(
            [(0, 0), (width, 0), (width, height), (0, height)],
            list(bitmap_shape_at_origin.geoms[0].exterior.coords)[:4]
        )

        # Apply the perspective transformation
        return image.transform((width, height), Image.PERSPECTIVE, transform_data, Image.BICUBIC)

    def apply_color_corrections(self):
        """ Applies color settings
            - color balance
            - brightness
            - contrast
            - transparent images: fill background with given color
            - reduce number of colors by either a given number or palette
        """
        if self.prepared_image is None:
            return

        background_color = None
        self.reduced_image = self.prepared_image

        saturation_enhancer = ImageEnhance.Color(self.reduced_image)
        self.reduced_image = saturation_enhancer.enhance(self.settings['bitmap_saturation'])

        brightness_enhancer = ImageEnhance.Brightness(self.reduced_image)
        self.reduced_image = brightness_enhancer.enhance(self.settings['bitmap_brightness'])

        contrast_enhancer = ImageEnhance.Brightness(self.reduced_image)
        self.reduced_image = contrast_enhancer.enhance(self.settings['bitmap_contrast'])

        # Some quantize methods will only work with rgb mode images. Means, we need to fill transparent image parts with a color.
        # To do this, we use the most prominent color from the image itself.
        # Using this color ensures, that the background will not have an impact on color selection methods.
        most_common_color = self._get_main_color(self.reduced_image, False)
        background = Image.new("RGBA", self.reduced_image.size, most_common_color)
        self.reduced_image = self.reduced_image.convert("RGBA")
        self.reduced_image = Image.alpha_composite(background, self.reduced_image)
        self.reduced_image = self.reduced_image.convert("RGB")

        color_palette = self._get_color_palette()
        if not color_palette:
            # used for color_method 1 if selected or if we failed to get palette data
            num_colors = self.settings['bitmap_num_colors']
            if num_colors == 0:
                num_colors = 1
            self.reduced_image = self.reduced_image.quantize(num_colors, method=self.settings['bitmap_quantize_method'], kmeans=5)
        else:
            palette_image = Image.new("P", (1, 1))
            palette_image.putpalette(color_palette)
            self.reduced_image = self.reduced_image.quantize(palette=palette_image, dither=Image.NONE)

        self.rgb_image = self.reduced_image

        # return to rgba mode and apply initial alpha mask
        self.reduced_image = self.reduced_image.convert('RGBA')
        self.reduced_image.putalpha(self.initial_alpha)

        # set background to alpha (optional)
        if self.settings['bitmap_remove_background'] == 1:
            background_color = self._nearest_color(self.settings['bitmap_background_color'])
        elif self.settings['bitmap_remove_background'] == 2:
            background_color = self._get_main_color(self.reduced_image, False)

        if background_color is not None:
            background = Image.new("RGBA", self.reduced_image.size, background_color)
            diff = ImageChops.difference(self.reduced_image, background).convert("L")
            background_mask = diff.point(lambda x: 255 if x else 0)
            self.alpha_mask = ImageChops.multiply(self.initial_alpha, background_mask)
            self.reduced_image.putalpha(self.alpha_mask)

    def _nearest_color(self, target_color):
        def distance(p):
            r, g, b, a = p
            return (r - target_color[0])**2 + (g - target_color[1])**2 + (b - target_color[2])**2 + (255)

        # Find the nearest RGBA color
        img = self.reduced_image.convert("RGBA")
        colors = img.getcolors()
        # Filter transparent areas
        colors = [color for count, color in colors if color[3] > 0]
        nearest = min(colors, key=distance)
        return nearest

    def apply_clip(self, image):
        # clips the image (used in cross stitch helper gui)
        # ensure rgba mode
        image = image.convert("RGBA")

        # get the clip shape and move it to canvas origin
        clip = self.bitmap.clip_shape
        if not clip:
            return image
        minx, miny, maxx, maxy = self.bitmap.original_shape.bounds
        clip = translate(clip, -minx, -miny)

        # setup mask
        mask = Image.new("L", (int(maxx-minx), int(maxy-miny)), 0)
        draw = ImageDraw.Draw(mask)
        for polygon in clip.geoms:
            draw.polygon(list(polygon.exterior.coords), fill=255)
            for interior in polygon.interiors:
                draw.polygon(list(interior.coords), fill=0)

        # combine mask with existing alpha channel
        mask = ImageChops.multiply(image.getchannel("A"), mask)

        # apply mask
        image.putalpha(mask)
        image = self._crop_transparent_borders(image)

        return image

    def _crop_transparent_borders(self, image):
        # crop transparent borders (only for use in cross stitch helper)
        bbox = image.getchannel("A").getbbox()
        if bbox:
            return image.crop(bbox)
        return image

    def svg_nodes(self):
        '''Converts the bitmap into path elements by respecting the given cross stitch settings
           Returns:
            * elements: a list of path elements grouped by color (svg groups)
        '''
        if self.reduced_image is None:
            return

        elements = []
        color_boxes = defaultdict(list)
        width = self.settings['box_x'] * PIXELS_PER_MM
        height = self.settings['box_y'] * PIXELS_PER_MM
        offset = self._get_offset_value()
        geometries = CrossGeometries(
            self.bitmap.shape, (width, height), max(75, self.settings['coverage']), 'simple_cross', offset, self.settings['align_with_canvas']
        )

        offset_x, offset_y, maxx, maxy = self.bitmap.original_shape.bounds
        offset_x -= offset[0]
        offset_y -= offset[1]

        for box in geometries.boxes:
            minx, miny, maxx, maxy = box.bounds

            # Find and apply the dominant color for each grid cell
            # Images with an alpha mask seem to end up with way too many colors, therefore, we check for alpha and the actual color separately
            crop_box = (minx - offset_x, miny - offset_y, maxx - offset_x, maxy - offset_y)
            cropped = self.alpha_mask.crop(crop_box)
            main_color = self._get_main_color(cropped)
            if main_color == [0, 0, 0, 255]:
                continue
            # This grid cell is not masked, find the most common color within the rgb mode image
            main_color = self._get_main_color(self.rgb_image.crop(crop_box))
            color_boxes[main_color[:3]].append(box)

        for color, boxes in color_boxes.items():
            color_group = Group()
            color_group.label = Color(color).to('named')
            outline = unary_union(boxes)
            # add a small buffer to connect otherwise unconnected elements
            outline = outline.buffer(0.001)
            # the buffer has added some unwanted nodes at corners
            # remove them with simplify
            outline = outline.simplify(0.1)
            outline = make_valid(outline)
            if self.settings['nodes']:
                outline = outline.segmentize(width + 0.002)
            multipolygon = ensure_multi_polygon(outline)

            for polygon in multipolygon.geoms:
                path = Path(list(polygon.exterior.coords))
                for interior in polygon.interiors:
                    interior_path = Path(list(interior.coords))
                    interior_path.close()
                    path += interior_path
                path.close()

                new_element = PathElement()
                new_element.set('d', str(path))
                new_element.set('style', f'fill:rgb{color}')
                new_element.transform = get_correction_transform(self.bitmap.node)
                color_group.append(new_element)
            elements.append(color_group)
        elements.sort(key=lambda group: len(group), reverse=True)
        return elements

    def _get_offset_value(self):
        '''converts the grid_offset string into a tuple with two integer values
        '''
        offset = self.settings['grid_offset'].split(' ')
        offset_value = (0, 0)
        if len(offset) == 1:
            try:
                offset_value = (int(offset[0]) * PIXELS_PER_MM, int(offset[0]) * PIXELS_PER_MM)
            except (TypeError, ValueError):
                pass
        if len(offset) == 2:
            try:
                offset_value = (int(offset[0]) * PIXELS_PER_MM, int(offset[1]) * PIXELS_PER_MM)
            except (TypeError, ValueError):
                pass
        return offset_value

    def _get_main_color(self, image, include_alpha=True):
        '''Returns the rgb value of the most prominent color within the given image
        '''
        image = image.convert('RGBA')
        if include_alpha:
            colors = image.getcolors()
        else:
            colors = [
                (count, (r, g, b, a))
                for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1])
                if a > 0
            ]
        return max(colors, key=itemgetter(0))[1]

    def _get_color_palette(self):
        '''Catches the colors for color method 1, 2 and 3
        '''
        color_method = self.settings['color_method']
        color_palette = None
        if color_method == 1:
            # Color method 1 reads colors from selected strokes and uses them as a palette
            color_palette = self.palette
        elif color_method == 2:
            # Color method 2 is a manual input of rgb values.
            # We don't care about the form, just read all numbers from a string into a list and make sure it is a multiple of 3 (rgb)
            colors = self.settings['bitmap_rgb_colors']
            color_palette = findall(r'\d+', colors)
            color_palette = [min(255, int(color_palette[i])) for i in range(len(color_palette) - len(color_palette) % 3)]
        elif color_method == 3:
            # Color method 3 reads a gimp color palette and converts it into a flat list with rgb values
            palette_path = self.settings['bitmap_gimp_palette']
            try:
                palette = ThreadPalette(palette_path)
            except FileNotFoundError:
                return None
            color_palette = []
            for i, color in enumerate(palette.threads):
                if i >= 256:
                    break
                color_palette.extend(color.rgb)
        return color_palette

    def _get_image_byte_string(self, image):
        '''Gets the image byte strig, base64
        '''
        image_string = None
        xlink = image.get('xlink:href', None)
        if not xlink:
            return None
        # linked image
        if xlink.startswith('file'):
            image_string = unquote(xlink[7:])
            if not os.path.isfile(image_string):
                return None
        # embedded imagae
        elif xlink.startswith('data'):
            image = xlink.split(',', 1)
            image_string = BytesIO(base64.b64decode(image[1]))
        return image_string

    def get_transform_data(self, source, target):
        '''Get the transform data to apply original image transforms
           For reference see https://stackoverflow.com/questions/14177744
        '''
        matrix = []
        for s, t in zip(source, target):
            matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
            matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])

        a = np.matrix(matrix, dtype=float)
        b = np.array(source).reshape(8)

        res = np.dot(np.linalg.inv(a.T * a) * a.T, b)
        return np.array(res).reshape(8)

    def flatten_palette(self, palette):
        pass
