# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import sqrt

from inkex import Path, errormsg
from shapely import make_valid, prepare, unary_union
from shapely.affinity import scale, translate
from shapely.geometry import Polygon

from ..i18n import _
from ..svg import get_correction_transform
from ..utils.geometry import ensure_multi_polygon
from .base import InkstitchExtension


class PixelizeFill(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-s", "--stitch_length", type=float, default=3, dest="stitch_length")
        self.arg_parser.add_argument("-c", "--coverage", type=int, default=50, dest="coverage")

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            errormsg(_("Please select one or more fill shapes to pixelize their outline."))
            return

        for element in self.elements:
            if element.name == "FillStitch":
                element_id = element.node.get_id()
                pixelated_outline = self.pixelize_element(element)
                for polygon in pixelated_outline.geoms:
                    path = Path(list(polygon.exterior.coords))
                    path.close()
                    for interior in polygon.interiors:
                        interior_path = Path(list(interior.coords))
                        interior_path.close()
                        path += interior_path

                    new_element = element.node.duplicate()
                    new_element.set('d', str(path))
                    new_element.set('id', self.svg.get_unique_id(f'{element_id}_'))
                    new_element.transform @= get_correction_transform(element.node)
            element.node.delete()

    def pixelize_element(self, element):
        fill_shapes = ensure_multi_polygon(make_valid(element.fill_shape(element.shape)))
        fill_shapes = list(fill_shapes.geoms)
        boxes = []
        for shape in fill_shapes:
            stitch_length = self.options.stitch_length
            square_size = stitch_length / sqrt(2)  # 45° angle
            square = Polygon([(0, 0), (square_size, 0), (square_size, square_size), (0, square_size)])
            full_square_area = square.area

            # start and end have to be a multiple of the stitch length
            minx, miny, maxx, maxy = shape.bounds
            adapted_minx = minx - minx % square_size
            adapted_miny = miny - miny % square_size
            adapted_maxx = maxx + square_size - maxx % square_size
            adapted_maxy = maxy + square_size - maxy % square_size
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
                    x += square_size
                y += square_size

        return ensure_multi_polygon(make_valid(unary_union(boxes))).simplify(0.1)
