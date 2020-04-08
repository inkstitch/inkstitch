from copy import deepcopy

from shapely import geometry as shgeo

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
            if len(element.paths) <= 1:
                continue

            polygons = []
            multipolygons = []
            holes = []

            # sort paths by size and convert to polygons
            element.paths.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)
            for path in element.paths:
                polygons.append(shgeo.Polygon(path))

            for shape in polygons:
                if shape in holes:
                    continue
                multipolygon = [shape]

                for other in polygons:
                    if shape != other and shape.contains(other) and other not in holes:
                        # check if "other" is inside a hole, before we add it to the list
                        if any(p.contains(other) for p in multipolygon[1:]):
                            continue
                        multipolygon.append(other)
                        holes.append(other)
                multipolygons.append(shgeo.MultiPolygon(multipolygon))
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
