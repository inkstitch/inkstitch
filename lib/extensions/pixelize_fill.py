# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Path, errormsg
from shapely import make_valid, prepare, unary_union
from shapely.affinity import scale, translate
from shapely.geometry import Polygon

from ..i18n import _
from ..svg import get_correction_transform, PIXELS_PER_MM
from ..utils.geometry import ensure_multi_polygon
from .base import InkstitchExtension


class PixelizeFill(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-x", "--box_size_x", dest="box_size_x", type=float, default=3)
        self.arg_parser.add_argument("-y", "--box_size_y", dest="box_size_y", type=float, default=3)
        self.arg_parser.add_argument("-c", "--coverage", type=int, default=50, dest="coverage")

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            errormsg(_("Please select one or more fill shapes to pixelize their outline."))
            return

        for element in self.elements:
            if element.name == "FillStitch":
                node = element.node
                element_id = node.get_id()

                # Covert non-path elemnts to pah elements
                if node.tag_name != "pah":
                    new_path = node.to_path_element()
                    node_parent = node.getparent()
                    node_index = node_parent.index(node)
                    node_parent.insert(node_index, new_path)
                else:
                    new_path = node.duplicate()

                pixelated_outline = self.pixelize_element(element)
                for polygon in pixelated_outline.geoms:
                    path = Path(list(polygon.exterior.coords))
                    path.close()
                    for interior in polygon.interiors:
                        interior_path = Path(list(interior.coords))
                        interior_path.close()
                        path += interior_path

                    new_element = new_path.duplicate()
                    new_element.set('d', str(path))
                    new_element.set('id', self.svg.get_unique_id(f'{element_id}_'))
                    new_element.transform = get_correction_transform(node)
                new_path.delete()
            node.delete()

    def pixelize_element(self, element):
        box_x = self.options.box_size_x * PIXELS_PER_MM
        box_y = self.options.box_size_y * PIXELS_PER_MM
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
                        if intersection_area / full_square_area * 100 > self.options.coverage:
                            boxes.append(box)
                    x += box_x
                y += box_y

        outline = make_valid(unary_union(boxes)).simplify(0.1)
        return ensure_multi_polygon(outline)
