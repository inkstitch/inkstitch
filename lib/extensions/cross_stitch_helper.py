# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Color, Grid, Group, Path
from inkex.units import convert_unit

from ..elements import FillStitch
from ..gui.cross_stitch_helper import CrossStitchHelperApp
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG
from ..utils.pixelate import pixelate_element, pixelate_multiple
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
            'remove_overlaps': True,
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
            'bitmap_remove_background': 0,
            'bitmap_display_svg_image': False
        }

        # True will not show the no elements warning
        # they may just simply want to check the the stitch length or setup the grid
        if self.svg.selection:
            self.get_elements(True)
        else:
            # nothing was selected, keep it this way
            self.elements = []

        # Fillter to only handle image and fill elements
        elements = []
        for element in self.elements:
            if element.name in ["Image", "FillStitch"]:
                elements.append(element)

        # Images may have been converted to fills which are not in the document
        # therefore we define a fallback element node, so we can use it to find a got spot to include the new elements
        self.fallback_element = None
        if elements:
            self.fallback_element = elements[-1]

        palette = self._get_stroke_palette()

        app = CrossStitchHelperApp(settings=settings, elements=elements, palette=palette)
        app.MainLoop()

        if not settings['applied']:
            return
        self.settings = settings

        # Pixelate and parametrize elements
        if self.settings['remove_overlaps']:
            # first convert images to fills, then process everything at once
            fills = self._prepare_fills(elements, palette)
            if fills:
                self.pixelize_combined(fills)
        else:
            self._process_elements(elements, palette)

        # add grid
        if settings['set_grid']:
            self.setup_page_grid()

    def _prepare_fills(self, elements, palette):
        fills = []
        for element in elements:
            if element.name == "FillStitch":
                if self.settings['pixelize']:
                    fills.append(element)
                elif self.settings['set_params']:
                    # when pixelize is disabled, set params on each fill element
                    self.set_element_cross_stitch_params(element.node)
            else:
                if not self.settings['convert_bitmap']:
                    continue
                bitmap_convert = BitmapToCrossStitch(self.svg, element, self.settings, palette)
                if bitmap_convert.original_image is None:
                    continue
                nodes = bitmap_convert.svg_nodes(False)
                for color_group in nodes:
                    for el in color_group:
                        fills.append(FillStitch(el))
                # element.node.delete()
        return fills

    def _process_elements(self, elements, palette):
        for element in elements:
            if element.name == "FillStitch":
                if self.settings['pixelize']:
                    self.pixelize_single(element)
                elif self.settings['set_params']:
                    # when pixelize is disabled, set params on each fill element
                    self.set_element_cross_stitch_params(element.node)
            else:
                if not self.settings['convert_bitmap']:
                    continue
                self._process_image(element, palette)

    def _get_stroke_palette(self):
        palette = []
        for element in self.elements:
            if element.name == "Stroke":
                color = element.stroke_color
                if color:
                    palette.extend(color.to_rgb())
        return palette

    def _process_image(self, element, palette):
        parent = element.node.getparent()
        index = parent.index(element.node)
        bitmap_convert = BitmapToCrossStitch(self.svg, element, self.settings, palette)
        if bitmap_convert.original_image is None:
            return
        elements = bitmap_convert.svg_nodes()
        if elements:
            main_group = Group()
            main_group.label = element.node.label or element.node.get_id()
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
        cross_stitch_group = Group()
        cross_stitch_group.label = _("Cross stitch group")

        cross_stitch_group = pixelate_multiple(cross_stitch_group, fills, self.settings)

        for path_element in cross_stitch_group.iterdescendants(SVG_PATH_TAG):
            if self.settings['set_params']:
                self.set_element_cross_stitch_params(path_element)
            path_element.set('id', self.svg.get_unique_id('cross_stitch_'))

        node = fills[-1].node
        parent = fills[-1].node.getparent()
        if fills[-1].node.getroottree().getroot().TAG == "g":
            # use the fallback node when we hit an image
            node = self.fallback_element.node
            parent = node.getparent()
            transform = get_correction_transform(node)
            cross_stitch_group.transform = transform
            index = parent.index(node) + 1
        else:
            index = parent.index(node)
        parent.insert(index, cross_stitch_group)

        for fill in fills:
            node = fill.node
            parent = node.getparent()
            fill.node.delete()
            if parent:
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

        pixelated_outline = pixelate_element(element, self.settings)
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
