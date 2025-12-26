# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Grid, Path
from inkex.units import convert_unit
from shapely import make_valid, prepare, unary_union
from shapely.affinity import scale, translate
from shapely.geometry import Polygon

from ..gui.cross_stitch_helper import CrossStitchHelperApp
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..utils.geometry import ensure_multi_polygon
from .base import InkstitchExtension


class CrossStitchHelper(InkstitchExtension):
    def effect(self):
        settings = {
            'applied': False,
            'box_x': 3,
            'box_y': 3,
            'update_elements': False,
            'pixelize': False,
            'coverage': 50,
            'nodes': False,
            'set_grid': False,
            'grid_color': '0x00d9e5ff',
            'remove_grids': False
        }
        app = CrossStitchHelperApp(settings=settings)
        app.MainLoop()

        # True will not show the no elements warning
        # they may just simply want to check the the stitch length or setup the grid
        self.get_elements(True)

        for element in self.elements:
            if element.name != "FillStitch":
                continue
            if settings['pixelize']:
                self.pixelize(element, settings)
            elif settings['update_elements']:
                # Pixelize may split up elements
                # we handle param settings in pixelize when enabled
                # when pixelize is disabled, set params on each fill element
                self.set_element_cross_stitch_params(element, settings)
        if settings['set_grid']:
            self.setup_page_grid(settings)

    def set_element_cross_stitch_params(self, element, settings):
        box_x = settings['box_x']
        box_y = settings['box_y']
        grid_param = str(box_x)
        if box_y != box_x:
            grid_param += f' {box_y}'
        element.set('inkstitch:fill_method', 'cross_stitch')
        element.set('inkstitch:pattern_size_mm', grid_param)

    def pixelize(self, element, settings):
        node = element.node
        element_id = node.get_id()

        # Covert non-path elemnts to pah elements
        if node.tag_name != "path":
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
        fill_shapes = ensure_multi_polygon(make_valid(element.fill_shape(element.shape)))
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
                        intersection = box.intersection(shape)
                        intersection_area = intersection.area
                        if intersection_area / full_square_area * 100 > settings['coverage']:
                            boxes.append(box)
                    x += box_x
                y += box_y

        outline = make_valid(unary_union(boxes))
        if not settings['nodes']:
            outline = outline.simplify(0.1)
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
