from copy import deepcopy

from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union

import inkex

from ..elements import AutoFill, Fill
from ..i18n import _
from ..svg import get_correction_transform
from .base import InkstitchExtension


class BreakApart(InkstitchExtension):
    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more fill areas to break apart."))
            return

        for element in self.elements:
            if not isinstance(element, AutoFill) and not isinstance(element, Fill):
                continue

            multipolygons = self.break_apart_element(element)
            if multipolygons:
                self.element_to_nodes(multipolygons, element)

    def break_apart_element(self, element):
        '''
        Divides element paths into a list of polygons.
        This will solve the crossing border error for most fill shapes
        '''
        polygons = []

        for path in element.paths:
            linestring = LineString(path)
            if not linestring.is_simple:
                linestring = unary_union(linestring)
            else:
                # if it is simple (not crossing) ignore single paths
                if len(element.paths) <= 1:
                    return
                linestring = [linestring]
            for polygon in polygonize(linestring):
                polygons.append(polygon)

        # sort paths by size and convert to polygons
        polygons.sort(key=lambda polygon: polygon.area, reverse=True)

        return self.recombine_polygons(polygons)

    def recombine_polygons(self, polygons):
        multipolygons = []
        holes = []

        for polygon in polygons:
            if polygon in holes:
                continue
            polygon_list = [polygon]

            for other in polygons:
                if polygon != other and polygon.contains(other) and other not in holes:
                    # check if "other" is inside a hole, before we add it to the list
                    if any(p.contains(other) for p in polygon_list[1:]):
                        continue
                    polygon_list.append(other)
                    holes.append(other)

            multipolygons.append(polygon_list)

        return multipolygons

    def element_to_nodes(self, multipolygons, element):
        valid = True
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
            if not el.is_valid() and valid:
                # in a very few cases we do not receive a valid path (e.g. loop to the inside)
                # let's give it a second chance and run the function once again
                valid = False
                multipolygons = self.break_apart_element(el)
                self.element_to_nodes(multipolygons, el)
        element.node.getparent().remove(element.node)
