# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import time
from collections import defaultdict
from copy import copy
from itertools import chain
from typing import List, Optional, Tuple, Union, cast

from inkex import BaseElement, Group, Path, PathElement
from networkx import MultiGraph, is_empty
from shapely import (LineString, MultiLineString, MultiPolygon, Point, Polygon,
                     dwithin, minimum_bounding_radius, reverse)
from shapely.ops import linemerge, substring

from ..elements import FillStitch
from ..stitches.auto_fill import (PathEdge, build_fill_stitch_graph,
                                  build_travel_graph, find_stitch_path,
                                  graph_make_valid, which_outline)
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..utils import DotDict, ensure_multi_line_string
from .palette import Palette
from .utils import sort_fills_and_strokes, stripes_to_shapes


class TartanSvgGroup:
    """Generates the tartan pattern for svg element tartans"""

    def __init__(self, settings: DotDict) -> None:
        """
        :param settings: the tartan settings
        """
        self.rotate = settings['rotate']
        self.scale = settings['scale']
        self.offset_x = settings['offset_x'] * PIXELS_PER_MM
        self.offset_y = settings['offset_y'] * PIXELS_PER_MM
        self.output = settings['output']
        self.stitch_type = settings['stitch_type']
        self.row_spacing = settings['row_spacing']
        self.angle_warp = settings['angle_warp']
        self.angle_weft = settings['angle_weft']
        self.min_stripe_width = settings['min_stripe_width']
        self.bean_stitch_repeats = settings['bean_stitch_repeats']

        self.palette = Palette()
        self.palette.update_from_code(settings['palette'])
        self.symmetry = self.palette.symmetry
        self.stripes = self.palette.palette_stripes
        self.warp, self.weft = self.stripes
        if self.palette.get_palette_width(self.scale, self.min_stripe_width) == 0:
            self.warp = []
        if self.palette.get_palette_width(self.scale, self.min_stripe_width, 1) == 0:
            self.weft = []
        if self.palette.equal_warp_weft:
            self.weft = self.warp

    def __repr__(self) -> str:
        return f'TartanPattern({self.rotate}, {self.scale}, ({self.offset_x}, {self.offset_y}), {self.symmetry}, {self.warp}, {self.weft})'

    def generate(self, outline: BaseElement) -> Group:
        """
        Generates a svg group which holds svg elements to represent the tartan pattern

        :param outline: the outline to be filled with the tartan pattern
        """
        parent_group = outline.getparent()

        if parent_group is None:
            raise ValueError("outline must have a parent")

        if parent_group is not None and parent_group.get_id().startswith('inkstitch-tartan'):
            # remove everything but the tartan outline
            for child in parent_group.iterchildren():
                if child != outline:
                    child.delete()
            group = cast(Group, parent_group)
        else:
            group = Group()
            group.set('id', f'inkstitch-tartan-{int(time.time())}')
            index = parent_group.index(outline)
            parent_group.insert(index, group)

        transform = get_correction_transform(outline)
        outline_shapes = FillStitch(outline).shape
        for outline_shape in outline_shapes.geoms:
            self._generate_tartan_group_elements(group, outline_shape, transform)

        # set outline invisible
        outline.style['display'] = 'none'
        group.append(outline)
        return group

    def _generate_tartan_group_elements(self, group, outline_shape, transform):
        dimensions, rotation_center = self._get_dimensions(outline_shape)

        warp = stripes_to_shapes(
            self.warp,
            dimensions,
            outline_shape,
            self.rotate,
            rotation_center,
            self.symmetry,
            self.scale,
            self.min_stripe_width
        )
        warp_routing_lines = self._get_routing_lines(warp)
        warp = self._route_shapes(warp_routing_lines, outline_shape, warp)
        warp = self._shapes_to_elements(warp, warp_routing_lines, transform)

        weft = stripes_to_shapes(
            self.weft,
            dimensions,
            outline_shape,
            self.rotate,
            rotation_center,
            self.symmetry,
            self.scale,
            self.min_stripe_width,
            True
        )
        weft_routing_lines = self._get_routing_lines(weft)
        weft = self._route_shapes(weft_routing_lines, outline_shape, weft, True)
        weft = self._shapes_to_elements(weft, weft_routing_lines, transform, True)

        fills, strokes = self._combine_shapes(warp, weft, outline_shape)
        fills, strokes = sort_fills_and_strokes(fills, strokes)

        for color, fill_elements in fills.items():
            for element in fill_elements:
                group.append(element)
                element.pop('inkstitch:start')
                element.pop('inkstitch:end')

        for color, stroke_elements in strokes.items():
            for element in stroke_elements:
                group.append(element)

    def _route_shapes(self, routing_lines: defaultdict, outline_shape: MultiPolygon, shapes: defaultdict, weft: bool = False) -> defaultdict:
        """
        Route polygons and linestrings

        :param routing_lines: diagonal lines representing the tartan stripes used for routing
        :param outline_shape: the shape to be filled with the tartan pattern
        :param shapes: the tartan shapes (stripes)
        :param weft: wether to render warp or weft oriented stripes
        """
        routed = defaultdict(list)
        for color, lines in routing_lines.items():
            routed_polygons = self._get_routed_shapes('polygon', shapes[color][0], lines[0], outline_shape, weft)
            routed_linestrings = self._get_routed_shapes('linestring', None, lines[1], outline_shape, weft)
            routed[color] = [routed_polygons, routed_linestrings]
        return routed

    def _get_routed_shapes(
        self,
        geometry_type: str,
        polygons: Optional[List[Polygon]],
        lines: Optional[List[LineString]],
        outline_shape: MultiPolygon,
        weft: bool
    ):
        """
        Find path for given elements

        :param geometry_type: wether to route 'polygon' or 'linestring'
        :param polygons: list of polygons to route
        :param lines: list of lines to route (for polygon routing these are the routing lines)
        :param outline_shape: the shape to be filled with the tartan pattern
        :param weft: wether to route warp or weft oriented stripes
        :returns: a list of routed elements
        """
        if not lines:
            return []

        if weft:
            starting_point = lines[-1].coords[-1]
            ending_point = lines[0].coords[0]
        else:
            starting_point = lines[0].coords[0]
            ending_point = lines[-1].coords[-1]

        segments = [list(line.coords) for line in lines if line.length > 5]

        fill_stitch_graph = build_fill_stitch_graph(outline_shape, segments, starting_point, ending_point)
        if is_empty(fill_stitch_graph):
            return []
        graph_make_valid(fill_stitch_graph)
        travel_graph = build_travel_graph(fill_stitch_graph, outline_shape, 0, False)
        path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
        return self._path_to_shapes(path, fill_stitch_graph, polygons, geometry_type, outline_shape)

    def _path_to_shapes(
        self,
        path: List[PathEdge],
        fill_stitch_graph: MultiGraph,
        polygons: Optional[List[Polygon]],
        geometry_type: str,
        outline_shape: MultiPolygon
    ) -> list:
        """
        Return elements in given order (by path) and add strokes for travel between elements

        :param path: routed PathEdges
        :param fill_stitch_graph: the stitch graph
        :param polygons: the polygon shapes (if not LineStrings)
        :param geometry_type: wether to render 'polygon' or 'linestring' segments
        :param outline_shape: the shape to be filled with the tartan pattern
        :returns: a list of routed shape elements
        """
        outline = LineString()
        travel_linestring = LineString()
        routed_shapes = []
        start_distance = 0.0
        for edge in path:
            start, end = edge
            if edge.is_segment():
                if not edge.key == 'segment':
                    # networkx fixed the shape for us, we do not really want to insert the element twice
                    continue
                if not travel_linestring.is_empty:
                    # insert edge run before segment
                    travel_linestring = self._get_shortest_travel(start, outline, travel_linestring)
                    if travel_linestring.geom_type == "LineString":
                        routed_shapes.append(travel_linestring)
                    travel_linestring = LineString()
                routed = self._edge_segment_to_element(edge, geometry_type, fill_stitch_graph, polygons)
                routed_shapes.extend(routed)
            elif routed_shapes:
                # prepare edge run between segments
                if travel_linestring.is_empty:
                    outline_index = which_outline(outline_shape, start)
                    outline = ensure_multi_line_string(outline_shape.boundary).geoms[outline_index]
                    # outline.project's result will be unwrapped into a float.
                    start_distance = outline.project(Point(start))
                    travel_linestring = self._get_travel(start, end, outline)
                else:
                    end_distance = outline.project(Point(end))
                    result = substring(outline, start_distance, end_distance)
                    if isinstance(result, Point):
                        travel_linestring = LineString()
                    else:
                        travel_linestring = result
        return routed_shapes

    def _edge_segment_to_element(
        self,
        edge: PathEdge,
        geometry_type: str,
        fill_stitch_graph: MultiGraph,
        polygons: Optional[List[Polygon]]
    ) -> list:
        """
        Turns an edge back into an element

        :param edge: edge with start and end point information
        :param geometry_type: wether to convert a 'polygon' or 'linestring'
        :param fill_stitch_graph: the stitch graph
        :param polygons: list of polygons if geom_type is 'poylgon'
        :returns: a list of routed elements.
            Polygons are wrapped in dictionaries to preserve information about start and end point.
        """
        start, end = edge
        routed: List[Union[dict, LineString]] = []
        if geometry_type == 'polygon' and polygons is not None:
            polygon = self._find_polygon(polygons, Point(start))
            if polygon:
                routed.append({'shape': polygon, 'start': start, 'end': end})
        elif geometry_type == 'linestring':
            try:
                line = cast(LineString, fill_stitch_graph[start][end]['segment'].get('geometry'))
            except KeyError:
                line = LineString([start, end])
            if not line.is_empty:
                if start != tuple(line.coords[0]):
                    line = line.reverse()
                if line:
                    routed.append(line)
        return routed

    @staticmethod
    def _get_shortest_travel(start: Tuple[float, float], outline: LineString, travel_linestring: LineString) -> LineString:
        """
        Replace travel_linestring with a shorter travel line if possible

        :param start: travel starting point
        :param outline: the part of the outline which is nearest to the starting point
        :param travel_linestring: predefined travel which will be replaced if it is longer
        """
        if outline.length / 2 < travel_linestring.length:
            short_travel = outline.difference(travel_linestring)
            if isinstance(short_travel, MultiLineString):
                short_travel = linemerge(short_travel)
            if isinstance(short_travel, LineString):
                if Point(short_travel.coords[-1]).distance(Point(start)) > Point(short_travel.coords[0]).distance(Point(start)):
                    short_travel = reverse(short_travel)
                return short_travel
        return travel_linestring

    @staticmethod
    def _find_polygon(polygons: List[Polygon], point: Point) -> Optional[Polygon]:
        """
        Find the polygon for a given point

        :param polygons: a list of polygons to chose from
        :param point: the point to match a polygon to
        :returns: a matching polygon or None if no polygon could be found
        """
        for polygon in polygons:
            if dwithin(point, polygon, 0.01):
                return polygon

        return None

    @staticmethod
    def _get_routing_lines(shapes: defaultdict) -> defaultdict:
        """
        Generate routing lines for given polygon shapes

        :param shapes: polygon shapes grouped by color
        :returns: color grouped dictionary with lines which can be used for routing
        """
        routing_lines = defaultdict(list)
        for color, elements in shapes.items():
            routed: list = [[], []]
            for polygon in elements[0]:
                bounding_coords = polygon.minimum_rotated_rectangle.exterior.coords
                routing_line = LineString([bounding_coords[0], bounding_coords[2]])
                routing_line_geoms = ensure_multi_line_string(routing_line.intersection(polygon)).geoms
                routed[0].append(LineString([routing_line_geoms[0].coords[0], routing_line_geoms[-1].coords[-1]]))
            routed[1].extend(elements[1])
            routing_lines[color] = routed
        return routing_lines

    def _shapes_to_elements(self, shapes: defaultdict, routed_lines: defaultdict, transform: str, weft=False) -> defaultdict:
        """
        Generates svg elements from given shapes

        :param shapes: lists of shapes grouped by color
        :param routed_lines: lists of routed lines grouped by color
        :param transform: correction transform to apply to the elements
        :param weft: wether to render warp or weft oriented stripes
        :returns: lists of svg elements grouped by color
        """
        shapes_copy = copy(shapes)
        for color, shape in shapes_copy.items():
            elements: list = [[], []]
            polygons, linestrings = shape
            for polygon in polygons:
                if isinstance(polygon, dict):
                    path_element = self._polygon_to_path(color, polygon['shape'], weft, transform, polygon['start'], polygon['end'])
                    if self.stitch_type == 'legacy_fill':
                        polygon_start = Point(polygon['start'])
                        path_element = self._adapt_legacy_fill_params(path_element, polygon_start)
                    elements[0].append(path_element)
                elif polygon.geom_type == "Polygon":
                    elements[0].append(self._polygon_to_path(color, polygon, weft, transform))
                else:
                    elements[0].append(self._linestring_to_path(color, polygon, transform, True))
            for line in linestrings:
                segment = line.difference(MultiLineString(routed_lines[color][1])).is_empty
                if segment:
                    linestring = self._linestring_to_path(color, line, transform)
                else:
                    linestring = self._linestring_to_path(color, line, transform, True)
                elements[1].append(linestring)
            shapes[color] = elements
        return shapes

    @staticmethod
    def _adapt_legacy_fill_params(path_element: PathElement, start: Point) -> PathElement:
        """
        Find best legacy fill param setting
        Flip and reverse so that the fill starts as near as possible to the starting point

        :param path_element: a legacy fill svg path element
        :param start: the starting point
        :returns: the adapted path element
        """
        if not FillStitch(path_element).to_stitch_groups(None):
            return path_element
        blank = Point(FillStitch(path_element).to_stitch_groups(None)[0].stitches[0])
        path_element.set('inkstitch:reverse', True)
        reverse = Point(FillStitch(path_element).to_stitch_groups(None)[0].stitches[0])
        path_element.set('inkstitch:flip', True)
        reverse_flip = Point(FillStitch(path_element).to_stitch_groups(None)[0].stitches[0])
        path_element.pop('inkstitch:revers')
        flip = Point(FillStitch(path_element).to_stitch_groups(None)[0].stitches[0])
        start_positions = [blank.distance(start), reverse.distance(start), reverse_flip.distance(start), flip.distance(start)]
        best_setting = start_positions.index(min(start_positions))

        if best_setting == 0:
            path_element.set('inkstitch:reverse', False)
            path_element.set('inkstitch:flip', False)
        elif best_setting == 1:
            path_element.set('inkstitch:reverse', True)
            path_element.set('inkstitch:flip', False)
        elif best_setting == 2:
            path_element.set('inkstitch:reverse', True)
            path_element.set('inkstitch:flip', True)
        elif best_setting == 3:
            path_element.set('inkstitch:reverse', False)
            path_element.set('inkstitch:flip', True)
        return path_element

    def _combine_shapes(self, warp: defaultdict, weft: defaultdict, outline: MultiPolygon) -> Tuple[defaultdict, defaultdict]:
        """
        Combine warp and weft elements into color groups, but separated into polygons and linestrings

        :param warp: dictionary with warp polygons and linestrings grouped by color
        :param weft: dictionary with weft polygons and linestrings grouped by color
        :returns: a dictionary with polygons and a dictionary with linestrings each grouped by color
        """
        polygons: defaultdict = defaultdict(list)
        linestrings: defaultdict = defaultdict(list)
        for color, shapes in chain(warp.items(), weft.items()):
            start = None
            end = None
            if shapes[0]:
                if polygons[color]:
                    start = polygons[color][-1].get('inkstitch:end')
                    end = shapes[0][0].get('inkstitch:start')
                    if start and end:
                        start = start[1:-1].split(',')
                        end = end[1:-1].split(',')
                        first_outline = ensure_multi_line_string(outline.boundary).geoms[0]
                        travel = self._get_travel(start, end, first_outline)
                        travel_path_element = self._linestring_to_path(color, travel, shapes[0][0].get('transform', ''), True)
                        polygons[color].append(travel_path_element)
                polygons[color].extend(shapes[0])
            if shapes[1]:
                if linestrings[color]:
                    start = tuple(list(linestrings[color][-1].get_path().end_points)[-1])
                elif polygons[color]:
                    start = polygons[color][-1].get('inkstitch:end')
                    if start:
                        start = start[1:-1].split(',')
                end = tuple(list(shapes[1][0].get_path().end_points)[0])
                if start and end:
                    first_outline = ensure_multi_line_string(outline.boundary).geoms[0]
                    travel = self._get_travel(start, end, first_outline)
                    travel_path_element = self._linestring_to_path(color, travel, shapes[1][0].get('transform', ''), True)
                    linestrings[color].append(travel_path_element)
                linestrings[color].extend(shapes[1])

        return polygons, linestrings

    @staticmethod
    def _get_travel(start: Tuple[float, float], end: Tuple[float, float], outline: LineString) -> LineString:
        """
        Returns a travel line from start point to end point along the outline

        :param start: starting point
        :param end: ending point
        :param outline: the outline
        :returns: a travel LineString from start to end along the outline
        """
        start_distance = outline.project(Point(start))
        end_distance = outline.project(Point(end))

        result = substring(outline, start_distance, end_distance)
        if isinstance(result, Point):
            return LineString((result, result))
        else:
            return result

    def _get_dimensions(self, outline: MultiPolygon) -> Tuple[Tuple[float, float, float, float], Point]:
        """
        Calculates the dimensions for the tartan pattern.
        Make sure it is big enough for pattern rotations.
        We also need additional space to ensure fill stripes go to their full extend, this might be problematic if
        start or end stripes use render mode 2 (stroke spacing).

        :param outline: the shape to be filled with a tartan pattern
        :returns: [0] a list with boundaries and [1] the center point (for rotations)
        """
        bounds = outline.bounds
        minx, miny, maxx, maxy = bounds
        minx -= self.offset_x
        miny -= self.offset_y
        center = LineString([(bounds[0], bounds[1]), (bounds[2], bounds[3])]).centroid

        if self.rotate != 0:
            # add as much space as necessary to perform a rotation without producing gaps
            min_radius = minimum_bounding_radius(outline)
            minx = center.x - min_radius
            miny = center.y - min_radius
            maxx = center.x + min_radius
            maxy = center.y + min_radius

        return (float(minx), float(miny), float(maxx), float(maxy)), center

    def _polygon_to_path(
        self,
        color: str,
        polygon: Polygon,
        weft: bool,
        transform: str,
        start: Optional[Tuple[float, float]] = None,
        end: Optional[Tuple[float, float]] = None
    ) -> PathElement:
        """
        Convert a polygon to an svg path element

        :param color: hex color
        :param polygon: the polygon to convert
        :param weft: wether to render as warp or weft
        :param transform: string of the transform to apply to the element
        :param start: start position for routing
        :param end: end position for routing
        :returns: an svg path element or None if the polygon is empty
        """
        path = Path(list(polygon.exterior.coords))
        path.close()

        for interior in polygon.interiors:
            interior_path = Path(list(interior.coords))
            interior_path.close()
            path += interior_path

        path_element = PathElement(
            attrib={'d': str(path)},
            style=f'fill:{color};fill-opacity:0.6;',
            transform=transform
        )

        if self.stitch_type == 'legacy_fill':
            path_element.set('inkstitch:fill_method', 'legacy_fill')
        elif self.stitch_type == 'auto_fill':
            path_element.set('inkstitch:fill_method', 'auto_fill')
            path_element.set('inkstitch:underpath', False)

        path_element.set('inkstitch:fill_underlay', False)
        path_element.set('inkstitch:row_spacing_mm', self.row_spacing)
        if weft:
            angle = self.angle_weft - self.rotate
            path_element.set('inkstitch:angle', angle)
        else:
            angle = self.angle_warp - self.rotate
            path_element.set('inkstitch:angle', angle)

        if start is not None:
            path_element.set('inkstitch:start', str(start))
        if end is not None:
            path_element.set('inkstitch:end', str(end))

        return path_element

    def _linestring_to_path(self, color: str, line: LineString, transform: str, travel: bool = False):
        """
        Convert a linestring to an svg path element

        :param color: hex color
        :param line: the line to convert
        :param transform: string of the transform to apply to the element
        :param travel: wether to render as travel line or running stitch/bean stitch
        :returns: an svg path element or None if the linestring path is empty
        """
        path = str(Path(list(line.coords)))
        if not path:
            return

        path_element = PathElement(
            attrib={'d': path},
            style=f'fill:none;stroke:{color};stroke-opacity:0.6;',
            transform=transform
        )
        if not travel and self.bean_stitch_repeats > 0:
            path_element.set('inkstitch:bean_stitch_repeats', self.bean_stitch_repeats)
        return path_element
