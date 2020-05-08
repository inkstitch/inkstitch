from copy import deepcopy

from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize, unary_union

import inkex

from ..elements import AutoFill, Fill
from ..i18n import _
from ..svg import get_correction_transform
from .base import InkstitchExtension


class BreakApart(InkstitchExtension):
    def effect(self):  # noqa: C901
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more fill areas to break apart."))
            return

        for element in self.elements:
            if not isinstance(element, AutoFill) and not isinstance(element, Fill):
                continue

            polygons = []
            multipolygons = []
            holes = []

            for path in element.paths:
                linestring = LineString(path)
                if linestring.is_simple:
                    polygons.append(Polygon(path))
                else:
                    # split non-simple linestrings (with loops)
                    union = unary_union(linestring)
                    for polygon in polygonize(union):
                        polygons.append(polygon)

            # sort paths by size and convert to polygons
            polygons.sort(key=lambda polygon: polygon.area, reverse=True)

            for shape in polygons:
                if shape in holes:
                    continue
                polygon_list = [shape]

                for other in polygons:
                    if shape != other and shape.contains(other) and other not in holes:
                        # check if "other" is inside a hole, before we add it to the list
                        if any(p.contains(other) for p in polygon_list[1:]):
                            continue
                        polygon_list.append(other)
                        holes.append(other)
                multipolygons.append(polygon_list)
            self.element_to_nodes(multipolygons, element)

    def element_to_nodes(self, multipolygons, element):
        for polygons in multipolygons:
            el = deepcopy(element)
            d = ""
            for polygon in polygons:
                # copy element and replace path
                el.node.set('id', self.uniqueId(element.node.get('id') + "_"))
                d += "M"
                for x, y in polygon.exterior.coords:
                    d += "%s,%s " % (x, y)
                    d += " "
                d += "Z"
            el.node.set('d', d)
            el.node.set('transform', get_correction_transform(element.node))
            element.node.getparent().insert(0, el.node)
        element.node.getparent().remove(element.node)
