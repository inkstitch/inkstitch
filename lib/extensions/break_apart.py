import logging
from copy import copy

from shapely.geometry import LineString, MultiPolygon, Polygon
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
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.OptionParser.add_option("-m", "--method", type="int", default=1, dest="method")

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

            # we don't want to touch valid elements
            paths = element.flatten(element.parse_path())
            paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
            polygon = MultiPolygon([(paths[0], paths[1:])])
            if self.geom_is_valid(polygon):
                continue

            polygons = self.break_apart_paths(paths)
            polygons = self.ensure_minimum_size(polygons, 5)
            if self.options.method == 1:
                polygons = self.combine_overlapping_polygons(polygons)
            polygons = self.recombine_polygons(polygons)
            if polygons:
                self.polygons_to_nodes(polygons, element)

    def break_apart_paths(self, paths):
        polygons = []
        for path in paths:
            linestring = LineString(path)
            polygon = Polygon(path).buffer(0)
            if not linestring.is_simple:
                linestring = unary_union(linestring)
                for polygon in polygonize(linestring):
                    polygons.append(polygon)
            else:
                polygons.append(polygon)
        return polygons

    def combine_overlapping_polygons(self, polygons):
        for polygon in polygons:
            for other in polygons:
                if polygon == other:
                    continue
                if polygon.overlaps(other):
                    diff = polygon.symmetric_difference(other)
                    if diff.geom_type == 'MultiPolygon':
                        polygons.remove(other)
                        polygons.remove(polygon)
                        for p in diff:
                            polygons.append(p)
                        # it is possible, that a polygons overlap with multiple
                        # polygons, this means, we need to start all over again
                        polygons = self.combine_overlapping_polygons(polygons)
                        return polygons
        return polygons

    def geom_is_valid(self, geom):
        # Don't complain about invalid shapes, we just want to know
        logger = logging.getLogger('shapely.geos')
        level = logger.level
        logger.setLevel(logging.CRITICAL)
        valid = geom.is_valid
        logger.setLevel(level)
        return valid

    def ensure_minimum_size(self, polygons, size):
        for polygon in polygons:
            if polygon.area < size:
                polygons.remove(polygon)
        return polygons

    def recombine_polygons(self, polygons):
        polygons.sort(key=lambda polygon: polygon.area, reverse=True)
        multipolygons = []
        holes = []
        for polygon in polygons:
            if polygon in holes:
                continue
            polygon_list = [polygon]
            for other in polygons:
                if polygon == other:
                    continue
                if polygon.contains(other) and other not in holes:
                    if any(p.contains(other) or p.intersects(other) for p in polygon_list[1:]):
                        continue
                    holes.append(other)
                    # if possible let's make the hole a tiny little bit smaller, just in case, it hits the edge
                    # and would lead therefore to an invalid shape
                    o = other.buffer(-0.01)
                    if not o.is_empty and o.geom_type == 'Polygon':
                        other = o
                    polygon_list.append(other)
            multipolygons.append(polygon_list)
        return multipolygons

    def polygons_to_nodes(self, polygon_list, element):
        # reverse the list of polygons, we don't want to cover smaller shapes
        polygon_list = polygon_list[::-1]
        index = element.node.getparent().index(element.node)
        for polygons in polygon_list:
            if polygons[0].area < 5:
                continue
            el = copy(element.node)
            d = ""
            for polygon in polygons:
                # update element id
                if len(polygon_list) > 1:
                    node_id = self.uniqueId(el.get('id') + '_')
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
