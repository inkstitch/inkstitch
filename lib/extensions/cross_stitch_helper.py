# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Grid, Group, Path
from inkex.units import convert_unit
from shapely import make_valid, prepare, unary_union
from shapely.affinity import scale, translate
from shapely.geometry import Polygon

from ..gui.cross_stitch_helper import CrossStitchHelperApp
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..utils.geometry import ensure_multi_polygon
from .base import InkstitchExtension
from .utils.bitmap_to_cross_stitch import BitmapToCrossStitch


class CrossStitchHelper(InkstitchExtension):
    '''Cross stitch helper is a tool to prepare canvas and elements for cross stitching.
       It can:
        * apply grid settings to a page grid (optionally delete previously generated cross stitch grids)
        * apply cross stitch settins to selectd fill elements (and images)
        * pixelate the outlines of fill elements
        * convert bitmap into pixelated fill elements
    '''
    def effect(self):
        settings = {
            'applied': False,
            'square': True,
            'box_x': 3,
            'box_y': 3,
            'update_elements': False,
            'cross_method': 'simple_cross',
            'pixelize': False,
            'coverage': 50,
            'grid_offset': '0',
            'align_with_canvas': True,
            'nodes': False,
            'set_grid': False,
            'grid_color': '0x00d9e5ff',
            'remove_grids': False,
            'color_method': 0,
            'convert_bitmap': False,
            'bitmap_num_colors': 5,
            'bitmap_quantize_method': 1,
            'bitmap_rgb_colors': '',
            'bitmap_gimp_palette': '',
            'bitmap_color_balance': 100,
            'bitmap_brightness': 100,
            'bitmap_contrast': 100,
            'bitmap_background_color': (0, 0, 0),
            'bitmap_background_main_color': False,
            'bitmap_ignore_background': False
        }

        # True will not show the no elements warning
        # they may just simply want to check the the stitch length or setup the grid
        if self.svg.selection:
            self.get_elements(True)
        else:
            # nothing was selected, keep it this way
            self.elements = []

        # When there is an image within the element list, send it to the App (for preview generation)
        # Send only the first one
        image = self._get_image()

        palette = self._get_stroke_palette()

        app = CrossStitchHelperApp(settings=settings, image=image, palette=palette)
        app.MainLoop()

        if not settings['applied']:
            return

        for element in self.elements:
            is_image = False
            if element.name == "Image":
                if not settings['convert_bitmap']:
                    continue
                is_image = True
                self.process_image(element, settings, palette)
            elif element.name != "FillStitch":
                continue

            if settings['pixelize'] and not is_image:
                self.pixelize(element, settings)
            elif settings['update_elements'] and not is_image:
                # Pixelize may split up elements
                # we handle param settings in pixelize when enabled
                # when pixelize is disabled, set params on each fill element
                self.set_element_cross_stitch_params(element.node, settings)
        if settings['set_grid']:
            self.setup_page_grid(settings)

    def _get_stroke_palette(self):
        palette = []
        for element in self.elements:
            if element.name == "Stroke":
                color = element.stroke_color
                if color:
                    palette.extend(color.to_rgb())
        return palette

    def _get_image(self):
        image = None
        for element in self.elements:
            if element.name == "Image":
                image = element
                break
        return image

    def process_image(self, element, settings, palette):
        parent = element.node.getparent()
        index = parent.index(element.node)
        bitmap_convert = BitmapToCrossStitch(self.svg, element, settings, palette)
        if bitmap_convert.prepared_image is None:
            return
        elements = bitmap_convert.svg_nodes()
        if elements:
            main_group = Group()
            for color in elements:
                if settings['update_elements']:
                    for path in color:
                        # Pixelize may split up elements
                        # we handle param settings in pixelize when enabled
                        # when pixelize is disabled, set params on each fill element
                        self.set_element_cross_stitch_params(path, settings)
                if len(elements) == 1:
                    main_group = color
                else:
                    main_group.append(color)
            if elements:
                parent.insert(index + 1, main_group)

    def set_element_cross_stitch_params(self, element, settings):
        box_x = settings['box_x']
        box_y = settings['box_y']
        grid_param = str(box_x)
        if box_y != box_x:
            grid_param += f' {box_y}'
        element.set('inkstitch:fill_method', 'cross_stitch')
        element.set('inkstitch:cross_stitch_method', settings['cross_method'])
        element.set('inkstitch:pattern_size_mm', grid_param)
        element.set('inkstitch:expand_mm', '0.1')
        element.set('inkstitch:fill_coverage', settings['coverage'])
        element.set('inkstitch:cross_offset_mm', settings['grid_offset'])
        element.set('inkstitch:canvas_grid_origin', settings['align_with_canvas'])

    def pixelize(self, element, settings):
        node = element.node
        element_id = node.get_id()

        # Covert non-path elemnts to pah elements
        if node.tag_name != "path" or node.get("sodipodi:type", None) in ['star', 'inkscape:box3dside']:
            new_path = node.to_path_element()
            node_parent = node.getparent()
            node_index = node_parent.index(node)
            node_parent.insert(node_index, new_path)
        else:
            new_path = node.duplicate()

        pixelated_outline = self.pixelize_element(element, settings)
        for polygon in pixelated_outline.geoms:
            path = Path(list(polygon.exterior.coords))
            for interior in polygon.interiors:
                interior_path = Path(list(interior.coords))
                interior_path.close()
                path += interior_path
            path.close()

            new_element = new_path.duplicate()
            new_element.set('d', str(path))
            new_element.set('id', self.svg.get_unique_id(f'{element_id}_'))
            new_element.transform = get_correction_transform(node)
            if settings['update_elements']:
                self.set_element_cross_stitch_params(new_element, settings)
        new_path.delete()
        node.delete()

    def pixelize_element(self, element, settings):
        box_x = settings['box_x'] * PIXELS_PER_MM
        box_y = settings['box_y'] * PIXELS_PER_MM
        # enlarge shape just a little bit, so that barely connected areas combine
        fill_shapes = element.shrink_or_grow_shape(element.shape, 0.1)
        fill_shapes = list(fill_shapes.geoms)
        boxes = []
        for shape in fill_shapes:
            square = Polygon([(0, 0), (box_x, 0), (box_x, box_y), (0, box_y)])
            full_square_area = square.area

            # start and end have to be a multiple of the stitch length
            minx, miny, maxx, maxy = shape.bounds
            adapted_minx = minx - minx % box_x
            adapted_miny = miny - miny % box_y
            adapted_maxx = maxx + box_x - maxx % box_x
            adapted_maxy = maxy + box_y - maxy % box_y
            prepare(shape)

            y = adapted_miny
            while y <= adapted_maxy:
                x = adapted_minx
                while x <= adapted_maxx:
                    box = translate(square, x, y)
                    # scale just enough to avoid disconnected shapes
                    box = scale(box, xfact=1.000000000000001, yfact=1.000000000000001)
                    if shape.contains(box):
                        boxes.append(box)
                    elif shape.intersects(box):
                        intersection = make_valid(box.intersection(shape))
                        intersection_area = intersection.area
                        if intersection_area / full_square_area * 100 >= settings['coverage']:
                            boxes.append(box)
                    x += box_x
                y += box_y

        outline = unary_union(boxes)
        # add a small buffer to connect otherwise unconnected elements
        outline = outline.buffer(0.001)
        # the buffer has added some unwanted nodes at corners
        # remove them with simplify
        outline = outline.simplify(0.1)
        outline = make_valid(outline)
        # simplify has removed nodes at grid intersections.
        # the user chose to have some additional nodes (to pull the shape out, let's add some nodes back in
        if settings['nodes']:
            outline = outline.segmentize(box_x + 0.002)
        return ensure_multi_polygon(outline)

    def setup_page_grid(self, settings):
        namedview = self.svg.namedview
        unit = self.svg.document_unit

        # hide old grids
        grids = self.svg.findall('.//inkscape:grid')
        for grid in grids:
            if grid.get_id().startswith("inkstitch_cross_stitch_grid_"):
                if settings['remove_grids']:
                    grid.delete()
            else:
                grid.set("enabled", "false")

        grid_id = self.svg.get_unique_id("inkstitch_cross_stitch_grid_")

        # insert new grid
        scale = self.svg.inkscape_scale
        box_x = settings['box_x'] / scale
        box_x = convert_unit(f'{box_x}mm', unit)
        box_y = settings['box_y'] / scale
        box_y = convert_unit(f'{box_y}mm', unit)
        grid = Grid(attrib={
            "id": grid_id,
            "units": unit,
            "originx": "0",
            "originy": "0",
            "spacingx": str(box_x),
            "spacingy": str(box_y),
            "empcolor": str(settings['grid_color']),
            "empopacity": "0.30196078",
            "color": str(settings['grid_color']),
            "opacity": "0.14901961",
            "empspacing": "1",
            "enabled": "true",
            "visible": "true",
        })
        namedview.append(grid)
