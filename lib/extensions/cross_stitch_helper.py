# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

from inkex import Color, Grid, Group, Path, PathElement
from inkex.units import convert_unit
from shapely import make_valid, unary_union

from ..gui.cross_stitch_helper import CrossStitchHelperApp
from ..i18n import _
from ..stitches.utils.cross_stitch import CrossGeometries
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
            'set_params': True,
            'cross_method': 'simple_cross',
            'pixelize': False,
            'pixelize_combined': True,
            'coverage': 50,
            'grid_offset': '0',
            'align_with_canvas': True,
            'nodes': False,
            'set_grid': False,
            'grid_color': (0, 153, 229),
            'remove_grids': False,
            'color_method': 0,
            'convert_bitmap': False,
            'bitmap_num_colors': 5,
            'bitmap_quantize_method': 1,
            'bitmap_rgb_colors': '',
            'bitmap_gimp_palette': '',
            'bitmap_saturation': 1,
            'bitmap_brightness': 1,
            'bitmap_contrast': 1,
            'bitmap_transparency_threshold': 50,
            'bitmap_background_color': (0, 0, 0),
            'bitmap_remove_background': 0
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
        self.settings = settings

        # collect image and fill elements
        images = []
        fills = []
        for element in self.elements:
            if element.name == "Image":
                images.append(element)
            elif element.name == "FillStitch":
                fills.append(element)

        # process elements
        self._process_images(images, palette)
        self._process_fills(fills)

        # add grid
        if settings['set_grid']:
            self.setup_page_grid()

    def _process_images(self, images, palette):
        if not self.settings['convert_bitmap']:
            return
        for image in images:
            self.process_image(image, palette)

    def _process_fills(self, fills):
        if not fills:
            return

        if self.settings['pixelize']:
            if self.settings['pixelize_combined']:
                self.pixelize_combined(fills)
            else:
                for fill in fills:
                    self.pixelize_single(fill)
        elif self.settings['set_params']:
            # Pixelize may split up elements
            # we handle param settings in pixelize when enabled
            # when pixelize is disabled, set params on each fill element
            for fill in fills:
                self.set_element_cross_stitch_params(fill.node)

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

    def process_image(self, element, palette):
        parent = element.node.getparent()
        index = parent.index(element.node)
        bitmap_convert = BitmapToCrossStitch(self.svg, element, self.settings, palette)
        if bitmap_convert.original_image is None:
            return
        elements = bitmap_convert.svg_nodes()
        if elements:
            main_group = Group()
            for color in elements:
                if self.settings['set_params']:
                    for path in color:
                        self.set_element_cross_stitch_params(path)
                if len(elements) == 1:
                    main_group = color
                else:
                    main_group.append(color)
            if elements:
                parent.insert(index + 1, main_group)

    def set_element_cross_stitch_params(self, element):
        box_x = self.settings['box_x']
        box_y = self.settings['box_y']
        grid_param = str(box_x)
        if box_y != box_x:
            grid_param += f' {box_y}'
        element.set('inkstitch:fill_method', 'cross_stitch')
        element.set('inkstitch:cross_stitch_method', self.settings['cross_method'])
        element.set('inkstitch:pattern_size_mm', grid_param)
        element.set('inkstitch:expand_mm', '0.1')
        element.set('inkstitch:fill_coverage', self.settings['coverage'])
        element.set('inkstitch:cross_offset_mm', self.settings['grid_offset'])
        element.set('inkstitch:canvas_grid_origin', self.settings['align_with_canvas'])

    def pixelize_combined(self, fills):
        colored_boxes = self._get_colored_boxes(fills)
        if not colored_boxes:
            return

        cross_stitch_group = Group()
        cross_stitch_group.label = _("Cross stitch group")

        for color, boxes in colored_boxes.items():
            color_group = Group()
            color_group.label = color
            # setup the path
            outline = self._prepare_outline(boxes)
            for polygon in outline.geoms:
                path = Path(list(polygon.exterior.coords))
                for interior in polygon.interiors:
                    interior_path = Path(list(interior.coords))
                    interior_path.close()
                    path += interior_path
                path.close()

                path_element = PathElement()
                path_element.set('d', str(path))
                path_element.set('id', self.svg.get_unique_id('cross_stitch_'))
                path_element.transform = get_correction_transform(fills[-1].node)
                path_element.style['fill'] = color_group.label
                if self.settings['set_params']:
                    self.set_element_cross_stitch_params(path_element)
                color_group.append(path_element)
            if len(color_group) > 1:
                cross_stitch_group.append(color_group)
            else:
                cross_stitch_group.append(color_group[0])

        parent = fills[-1].node.getparent()
        index = parent.index(fills[-1].node)
        parent.insert(index, cross_stitch_group)

        for fill in fills:
            node = fill.node
            parent = node.getparent()
            fill.node.delete()
            self._remove_empty_group(parent)

    def _remove_empty_group(self, group):
        parent = group.getparent()
        if len(group) == 0:
            group.delete()
        if parent and len(parent) == 0:
            self._remove_empty_group(parent)

    def pixelize_single(self, element):
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

        pixelated_outline = self.pixelize_element(element)
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
            if self.settings['set_params']:
                self.set_element_cross_stitch_params(new_element)
        new_path.delete()
        node.delete()

    def pixelize_element(self, element):
        geometries = CrossGeometries(
            element.shrink_or_grow_shape(element.shape, 0.1),
            (self.settings['box_x'] * PIXELS_PER_MM, self.settings['box_y'] * PIXELS_PER_MM),
            self.settings['coverage'],
            'simple_cross',
            self._get_grid_offset(),
            self.settings['align_with_canvas']
        )

        outline = self._prepare_outline(geometries.boxes)
        return outline

    def setup_page_grid(self):
        namedview = self.svg.namedview
        unit = self.svg.document_unit

        # hide old grids
        grids = self.svg.findall('.//inkscape:grid')
        for grid in grids:
            if grid.get_id().startswith("inkstitch_cross_stitch_grid_"):
                if self.settings['remove_grids']:
                    grid.delete()
            else:
                grid.set("enabled", "false")

        grid_id = self.svg.get_unique_id("inkstitch_cross_stitch_grid_")

        # insert new grid
        svg_scale = self.svg.inkscape_scale
        box_x = self.settings['box_x'] / svg_scale
        box_x = convert_unit(f'{box_x}mm', unit)
        box_y = self.settings['box_y'] / svg_scale
        box_y = convert_unit(f'{box_y}mm', unit)
        grid = Grid(attrib={
            "id": grid_id,
            "units": unit,
            "originx": "0",
            "originy": "0",
            "spacingx": str(box_x),
            "spacingy": str(box_y),
            "empcolor": str(Color(self.settings['grid_color']).to('named')),
            "empopacity": "0.30196078",
            "color": str(Color(self.settings['grid_color']).to('named')),
            "opacity": "0.14901961",
            "empspacing": "1",
            "enabled": "true",
            "visible": "true",
        })
        namedview.append(grid)

    def _get_grid_offset(self):
        grid_offset = self.settings['grid_offset'].split(' ')
        try:
            grid_offset = self.settings['grid_offset'].split(' ')
            if len(grid_offset) == 1:
                offset = float(grid_offset[0]) * PIXELS_PER_MM
                return (offset, offset)
            elif len(grid_offset) == 2:
                return (float(grid_offset[0]) * PIXELS_PER_MM, float(grid_offset[1] * PIXELS_PER_MM))
        except ValueError:
            pass
        return (0, 0)  # Fallback

    def _get_colored_boxes(self, fills):
        fill_areas = []
        fill_areas_by_color = defaultdict(list)
        for fill in reversed(fills):
            # subtract areas already filled with a color
            area = unary_union(fill_areas)
            adapted_shape = fill.shape.difference(area)
            if not adapted_shape.is_empty:
                color = Color(fill.fill_color).to('named')
                fill_areas_by_color[color].append(fill.shape.difference(area))
            # add a little expand value to connect otherwise unconnected
            fill_areas.append(fill.shrink_or_grow_shape(fill.shape, 0.1))

        # combine all selected fill shape areas to generate all squares at once
        full_area = ensure_multi_polygon(unary_union(fill_areas))
        # get squares
        grid_offset = self._get_grid_offset()
        geometries = CrossGeometries(
            full_area,
            (self.settings['box_x'] * PIXELS_PER_MM, self.settings['box_y'] * PIXELS_PER_MM),
            self.settings['coverage'],
            'simple_cross',
            grid_offset,
            self.settings['align_with_canvas']
        )

        color_shape_dict = {}
        for color, shapes in fill_areas_by_color.items():
            color_shape_dict[color] = make_valid(unary_union(shapes))

        colored_boxes = defaultdict(list)
        for box in geometries.boxes:
            current_color = None
            highest_overlap = 0
            for color, shape in color_shape_dict.items():
                overlap = box.intersection(shape).area
                if overlap > highest_overlap:
                    current_color = color
                    highest_overlap = overlap
            if current_color is not None:
                colored_boxes[current_color].append(box)
        return colored_boxes

    def _prepare_outline(self, boxes):
        outline = unary_union(boxes)
        # add a small buffer to connect otherwise unconnected elements
        outline = outline.buffer(0.001)
        # the buffer has added some unwanted nodes at corners
        # remove them with simplify
        outline = outline.simplify(0.1)
        outline = make_valid(outline)
        # simplify has removed nodes at grid intersections.
        # the user chose to have some additional nodes (to pull the shape out, let's add some nodes back in
        if self.settings['nodes']:
            outline = outline.segmentize(self.settings['box_x'] * PIXELS_PER_MM + 0.002)
        return ensure_multi_polygon(outline)
