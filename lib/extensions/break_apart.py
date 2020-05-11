from copy import copy

from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize, unary_union

import inkex

from ..elements import EmbroideryElement
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG
from .base import InkstitchExtension


class BreakApart(InkstitchExtension):
    '''
    This will break apart fill areas into separate elements.
    '''
    def effect(self):
        if not self.selected:
            inkex.errormsg(_("Please select one or more fill areas to break apart."))
            return

        elements = []
        nodes = self.get_nodes()
        for node in nodes:
            if node.tag in SVG_PATH_TAG:
                elements.append(EmbroideryElement(node))

        for element in elements:
            if not element.get_style("fill", "black"):
                continue

            multipolygons = self.break_apart_element(element)
            if multipolygons:
                self.element_to_nodes(multipolygons, element)

    def break_apart_element(self, element):
        paths = element.flatten(element.parse_path())
        polygons = []

        for path in paths:
            linestring = LineString(path)
            if not linestring.is_simple:
                linestring = unary_union(linestring)
                for polygon in polygonize(linestring):
                    polygons.append(polygon)
            else:
                polygons.append(Polygon(path))

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
                    # dont't add to holes if "other" is inside a hole or intersects with an outer polygon
                    if any(p.contains(other) or p.intersects(other) for p in polygon_list[1:]):
                        continue
                    polygon_list.append(other)
                    holes.append(other)
            multipolygons.append(polygon_list)

        return multipolygons

    def element_to_nodes(self, multipolygons, element):
        index = element.node.getparent().index(element.node)

        for polygons in multipolygons:
            # ignore very small areas
            if polygons[0].area < 5:
                continue

            el = copy(element.node)
            d = ""

            for polygon in polygons:
                if len(multipolygons) == 1:
                    node_id = el.get('id')
                else:
                    node_id = self.uniqueId(el.get('id') + '_')
                # copy element and replace path
                el.set('id', node_id)
                d += "M"
                for x, y in polygon.exterior.coords:
                    d += "%s,%s " % (x, y)
                    d += " "
                d += "Z"
            el.set('d', d)
            el.set('transform', get_correction_transform(element.node))
            element.node.getparent().insert(index, el)
        element.node.getparent().remove(element.node)
