# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import copy
from typing import List, Tuple, Union

from inkex import Path, errormsg
from shapely.geometry import LinearRing, MultiPolygon, Polygon
from shapely.ops import polygonize, unary_union
from shapely import make_valid

from ..elements import EmbroideryElement
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG
from .base import InkstitchExtension
from ..utils.geometry import ensure_multi_polygon


class BreakApart(InkstitchExtension):
    '''
    This will break apart fill areas into separate elements.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-m", "--method", type=int, default=1, dest="method")
        self.arg_parser.add_argument("-t", "--threshold", type=float, default=1, dest="threshold")

    def effect(self) -> None:  # noqa: C901
        if not self.svg.selection:
            errormsg(_("Please select one or more fill areas to break apart."))
            return

        self.minimum_size = self.options.threshold

        elements = []
        nodes = self.get_nodes()
        for node in nodes:
            if node.tag in SVG_PATH_TAG:
                elements.append(EmbroideryElement(node))

        for element in elements:
            if not element.fill_color:
                continue

            # we don't want to touch valid elements
            paths = element.flatten(element.parse_path())
            try:
                paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
                polygon = MultiPolygon([(paths[0], paths[1:])]).normalize()
                # Check for area size only after the polygon has been made valid.
                # If the directions of the holes are not correct, we could face a problem with negative space,
                # making it difficult to evaluate the actual size
                valid_polygon = ensure_multi_polygon(make_valid(polygon))
                if self.geom_is_valid(polygon) and polygon.area > self.minimum_size:
                    continue
                if valid_polygon.area <= self.minimum_size:
                    element.node.delete()
                    continue
            except ValueError:
                pass

            polygons = self.break_apart_paths(paths)
            if self.options.method == 1:
                polygons = self.combine_overlapping_polygons(polygons)
            recombined_polygons = self.recombine_polygons(polygons)
            if recombined_polygons:
                self.polygons_to_nodes(recombined_polygons, element)

    def break_apart_paths(self, paths: List[List[Union[List[float], Tuple[float, float]]]]) -> List[Polygon]:
        polygons = []
        for path in paths:
            if len(path) < 3:
                continue
            linearring = LinearRing(path)
            if not linearring.is_simple:
                union = unary_union(linearring)
                for polygon in polygonize(union):
                    polygons.append(polygon)
            else:
                polygon = Polygon(path).buffer(0)
                polygons.append(polygon)
        return polygons

    def combine_overlapping_polygons(self, polygons: List[Polygon]) -> List[Polygon]:
        for polygon in polygons:
            for other in polygons:
                if polygon == other:
                    continue
                if polygon.overlaps(other):
                    diff = polygon.symmetric_difference(other)
                    if isinstance(diff, MultiPolygon):
                        polygons.remove(other)
                        polygons.remove(polygon)
                        for p in diff.geoms:
                            polygons.append(p)
                        # it is possible, that a polygons overlap with multiple
                        # polygons, this means, we need to start all over again
                        polygons = self.combine_overlapping_polygons(polygons)
                        return polygons
        return polygons

    def geom_is_valid(self, geom: MultiPolygon) -> bool:
        valid = geom.is_valid
        return valid

    def ensure_minimum_size(self, polygons: List[Polygon]) -> List[Polygon]:
        return [polygon for polygon in polygons if polygon.area > self.minimum_size]

    def recombine_polygons(self, polygons: List[Polygon]) -> List[List[Polygon]]:
        polygons.sort(key=lambda polygon: polygon.area, reverse=True)
        multipolygons = []
        holes = []
        polygons = self.ensure_minimum_size(polygons)
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

    def polygons_to_nodes(self, polygon_list: List[List[Polygon]], element: EmbroideryElement) -> None:
        # reverse the list of polygons, we don't want to cover smaller shapes
        polygon_list = polygon_list[::-1]
        parent = element.node.getparent()
        assert parent is not None, "The element should be part of a group."
        index = parent.index(element.node)
        for polygons in polygon_list:
            if polygons[0].area < 5:
                continue
            el = copy(element.node)

            # Set fill-rule to evenodd
            style = el.get('style', ' ').split(';')
            style = [s for s in style if not s.startswith('fill-rule')]
            style.append('fill-rule:evenodd;')
            style = ';'.join(style)
            el.set('style', style)

            # update element id
            if len(polygon_list) > 1:
                node_id = self.uniqueId(el.get('id') + '_')
                el.set('id', node_id)

            # Set path
            d = Path()
            for polygon in polygons:
                path = Path(polygon.exterior.coords)
                path.close()
                d += path
            el.set('d', str(d))
            el.set('transform', get_correction_transform(element.node))
            parent.insert(index, el)
        element.node.delete()
