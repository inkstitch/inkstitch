# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx
from shapely import line_merge
from shapely.geometry import MultiLineString, Point
from shapely.ops import nearest_points, unary_union

from ..stitch_plan import Stitch
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import ensure_multi_line_string, reverse_line_string, ensure_multi_polygon
from ..utils.threading import check_stop_flag
from .auto_fill import (fallback,
                        find_stitch_path, graph_make_valid, build_travel_graph,
                        build_fill_stitch_graph, travel, collapse_sequential_outline_edges)
from .running_stitch import bean_stitch
from .utils.cross_stitch import CrossGeometries


def half_cross_stitch(fill, shape, starting_point, ending_point, bean_stitch_repeats, original_shape=None):
    ''' Half crosses in machine embroidery have unavoidably strongly visible travel stitches along the outline.
        They behave much like an auto_fill in 45 degree angle. They only differ from auto-fill in:
        - their pixelated outline
        - thread count (bean stitch repeats)
          bean stitch repeats will always return an odd thread count, opposed to the other cross stitch methods

        fill:                   the fill element
        shape:                  shape as MultiPolygon
        starting_point:         defines where to start
        ending_point:           defines where to end
        bean_stitch_repeats:    defines the thread count (odd number)
        original_shape:         helps to define a consistent grid offset when the shape had to be split up into multiple shapes
    '''

    max_stitch_length = fill.max_cross_stitch_length
    cross_stitch_method = fill.cross_stitch_method

    cross_geoms = CrossGeometries(fill, shape, cross_stitch_method, original_shape)

    if not cross_geoms.boxes:
        return []

    # Fix outline.
    # The outline for cross stitches is a bit delicate as it tends to be invalid in a shapely sense.
    # We add a small buffer to connect unconnected geometry parts at touching corners.
    # It is possible though, that the cross stitch areas are fully unconnected. In this case, we will run the stitch
    # generation on each outline component separately.
    outline = ensure_multi_polygon(unary_union(cross_geoms.boxes).buffer(0.00001))
    if len(outline.geoms) > 1:
        # we will have to run this on multiple outline shapes
        return cross_stitch_multiple(outline, fill, starting_point, ending_point, bean_stitch_repeats, shape)
    else:
        outline = list(outline.geoms)[0]

    # The cross stitch diagonals
    diagonals = ensure_multi_line_string(line_merge(MultiLineString(cross_geoms.diagonals).segmentize(max_stitch_length)))

    stitches = _lines_to_stitches(diagonals, outline, max_stitch_length, bean_stitch_repeats, starting_point, ending_point)

    return [stitches]


def cross_stitch_multiple(outline, fill, starting_point, ending_point, bean_stitch_repeats, original_shape):
    '''Run the cross stitch generator on separated outline components
    '''
    shapes = list(outline.geoms)
    if starting_point:
        shapes.sort(key=lambda shape: shape.distance(Point(starting_point)))
    else:
        shapes.sort(key=lambda shape: shape.bounds[0])

    stitches = []
    for i, polygon in enumerate(shapes):
        if i < len(shapes) - 1:
            end = nearest_points(polygon, shapes[i+1])[0].coords
        else:
            end = ending_point
        stitches.extend(half_cross_stitch(fill, polygon, starting_point, end, bean_stitch_repeats, original_shape))
        if stitches:
            starting_point = InkstitchPoint(*stitches[-1][-1])
    return stitches


def _lines_to_stitches(line_geoms, shape, max_stitch_length, bean_stitch_repeats, starting_point, ending_point):
    segments = []
    for line in line_geoms.geoms:
        segments.append(list(line.coords))

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if networkx.is_empty(fill_stitch_graph):
        return fallback(shape, max_stitch_length, 0.2)
    if not networkx.is_connected(fill_stitch_graph):
        # try to rescue the operation in selecting only the largest connected component
        largest_cc = max(networkx.connected_components(fill_stitch_graph), key=len)
        fill_stitch_graph = fill_stitch_graph.subgraph(largest_cc).copy()
    graph_make_valid(fill_stitch_graph)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, 0, False)

    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
    result = path_to_stitches(shape, path, travel_graph, fill_stitch_graph, max_stitch_length)

    if bean_stitch_repeats >= 1:
        # add bean stitches, but ignore travel stitches
        result = bean_stitch(result, [bean_stitch_repeats], ['auto_fill_travel', 'fill_row_start'])
    return result


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, max_stitch_length):
    ''' Convert path to stitch data
    '''
    path = collapse_sequential_outline_edges(path, fill_stitch_graph)
    stitches = []
    if not path[0].is_original_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for i, edge in enumerate(path):
        check_stop_flag()
        if edge.is_segment():
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']

            if edge[0] != path_geometry.coords[0]:
                path_geometry = reverse_line_string(path_geometry)

            if edge.is_original_segment():
                row_stitches = [Stitch(*point, tags=['auto_fill', 'fill_row']) for point in path_geometry.coords]
                row_stitches[0].add_tag('fill_row_start')
                row_stitches[-1].add_tag('fill_row_end')
            else:
                row_stitches = [Stitch(*point, tags=['auto_fill_travel']) for point in path_geometry.coords]
            stitches.extend(row_stitches)

        else:
            stitches.extend(travel(shape, travel_graph, edge, [max_stitch_length], 0.2, False, False))

    return stitches
