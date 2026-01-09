# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx
from shapely import line_merge, snap
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import nearest_points, unary_union

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import ensure_multi_line_string, reverse_line_string
from ..utils.threading import check_stop_flag
from .auto_fill import (add_edges_between_outline_nodes, fallback,
                        find_stitch_path, graph_make_valid,
                        tag_nodes_with_outline_and_projection)
from .running_stitch import bean_stitch
from .utils.cross_stitch import CrossGeometries


def half_cross_stitch(fill, shape, starting_point, ending_point, bean_stitch_repeats, original_shape=None):
    '''Cross stitch fill type

       Cross stitches are organized in a pixelated pattern. Each "cross pixel" (box) has two diagonals.
       Traditionally cross stitches are strictly organized and each cross follows the same pattern.
       Meaning the layering of the diagonals can't be switched during the stitch out.
       For example all crosses start with '\' as a bottom layer and end with '/' as the top layer.

        fill:           the fill element
        shape:          shape as MultiPolygon
        starting_point: defines where to start
        ending_point:   defines where to end
        original_shape: helps to define a consistent grid offset when the shape had to be split up into multiple shapes
    '''

    max_stitch_length = fill.max_cross_stitch_length
    cross_stitch_method = fill.cross_stitch_method

    cross_geoms = CrossGeometries(fill, shape, cross_stitch_method)

    if not cross_geoms.boxes:
        return []

    # Fix outline. The outline for cross stitches is a bit delicate as it tends to be invalid in a shapely sense.
    # We created scaled boxes to avoid a splitting up of an outline which we would be able to render in one go.
    # But we only want to use the scaled boxes if it is really necessary.
    # It is also possible that the cross stitch pattern is fully unconnected. In this case, we will run the stitch
    # generation on each outline component.
    outline = unary_union(cross_geoms.boxes)
    if outline.geom_type == 'MultiPolygon':
        # we will have to run this on multiple outline shapes
        return cross_stitch_multiple(outline, fill, starting_point, ending_point, original_shape)

    # The cross stitch diagonals
    diagonals = ensure_multi_line_string(line_merge(MultiLineString(cross_geoms.diagonals).segmentize(max_stitch_length)))

    nodes = get_line_endpoints(diagonals)

    stitches = _lines_to_stitches(diagonals, outline, max_stitch_length, bean_stitch_repeats, starting_point, ending_point, nodes)

    return [stitches]


def cross_stitch_multiple(outline, fill, starting_point, ending_point, original_shape):
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
        stitches.extend(half_cross_stitch(fill, polygon, starting_point, end, original_shape))
        starting_point = InkstitchPoint(*stitches[-1][-1])
    return stitches


def get_line_endpoints(multilinestring):
    '''Returns the endpoints of each line from a multilinestring
    '''
    nodes = []
    for line in multilinestring.geoms:
        coords = list(line.coords)
        nodes.extend((coords[0], coords[-1]))
    return nodes


def _lines_to_stitches(line_geoms, shape, max_stitch_length, bean_stitch_repeats, starting_point, ending_point, nodes):
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

    travel_graph = build_travel_graph(fill_stitch_graph, shape, nodes)

    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
    result = path_to_stitches(shape, path, travel_graph, fill_stitch_graph, max_stitch_length)
    result = collapse_travel_edges(result, ending_point)

    if bean_stitch_repeats >= 1:
        # add bean stitches, but ignore travel stitches
        result = bean_stitch(result, [bean_stitch_repeats], ['auto_fill_travel', 'fill_row_start'])
    return result


@debug.time
def build_fill_stitch_graph(shape, segments, starting_point=None, ending_point=None):
    """build a graph representation of the grating segments

       See full explanation of the idea in auto_fill.
       Changes here is the removal of projections nodes on the outline for start and end points
    """

    debug.add_layer("auto-fill fill stitch")

    graph = networkx.MultiGraph()

    # First, add the grating segments as edges.  We'll use the coordinates
    # of the endpoints as nodes, which networkx will add automatically.
    for segment in segments:
        # networkx allows us to label nodes with arbitrary data.  We'll
        # mark this one as a grating segment.
        graph.add_edge(segment[0], segment[-1], key="segment", geometry=LineString(segment))

        check_stop_flag()

    tag_nodes_with_outline_and_projection(graph, shape, graph.nodes())
    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    debug.log_graph(graph, "graph")

    return graph


def build_travel_graph(fill_stitch_graph, shape, nodes):
    """Build a graph for travel stitches.

       See full explanatio in the auto_fill file.
       Here we create different grating lines (using the travel edges)
    """
    graph = networkx.MultiGraph()

    # Add all the nodes from the main graph.  This will be all of the endpoints
    # of the rows of stitches.  Every node will be on the outline of the shape.
    # They'll all adiagonals1eady have their `outline` and `projection` tags set.
    graph.add_nodes_from(fill_stitch_graph.nodes(data=True))

    add_boundary_travel_nodes(graph, shape)

    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    debug.log_graph(graph, "travel graph")

    return graph


def add_boundary_travel_nodes(graph, shape):
    outlines = ensure_multi_line_string(shape.boundary).geoms
    for outline_index, outline in enumerate(outlines):
        for point in outline.coords:
            check_stop_flag()
            point = Point(point)
            graph.add_node((point.x, point.y), projection=outline.project(point), outline=outline_index)


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, max_stitch_length):
    ''' Convert path to stitch data
        while shortening travel paths and adapting the travel edges to the crosses
    '''
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
            stitches.extend(travel(shape, travel_graph, edge, max_stitch_length))

    return stitches


def travel(shape, travel_graph, edge, max_stitch_length):
    """Create stitches to get from one point on an outline of the shape to another."""

    start, end = edge
    try:
        path = networkx.shortest_path(travel_graph, start, end, weight='weight')
    except (networkx.NetworkXNoPath, networkx.exception.NodeNotFound):
        # This may not look good, but it prevents the fill from failing (which hopefully never happens)
        path = [start, end]

    path = [InkstitchPoint.from_tuple(point) for point in path]
    if not path:
        # This may happen on very small shapes.
        # Simply return nothing as we do not want to error out
        return []

    if len(path) > 1:
        path = clamp_path_to_polygon(path, shape)

    # At this point we are almost happy with the path. But we have some segments not following the crosses, but their bounding boxes.
    # This means, we will need to add some extra points.
    stitches = []
    for point in path:
        check_stop_flag()
        stitches.extend([Stitch(*point, tags=["auto_fill_travel"])])

    return stitches


def collapse_travel_edges(result, ending_point):
    '''Removes undwanted loops in travel paths
    '''
    new_sitches = []
    last_travel_stitches = []
    for i, stitch in enumerate(result):
        # cut travel loops off
        if last_travel_stitches:
            point = Point(stitch)
            travel_multi_point = MultiPoint(last_travel_stitches)
            if point.distance(travel_multi_point) < 0.011:
                geoms = list(travel_multi_point.geoms)
                point = snap(point, travel_multi_point, tolerance=0.012)
                index = geoms.index(point)
                last_travel_stitches = last_travel_stitches[0:index]
        last_travel_stitches.append(stitch)
        # add to stitches
        if 'auto_fill_travel' not in stitch.tags:
            if 'fill_row_end' in stitch.tags:
                new_sitches.extend(last_travel_stitches)
                last_travel_stitches = [stitch]
            else:
                last_travel_stitches.append(stitch)
                new_sitches.extend(last_travel_stitches)
                last_travel_stitches = []

    if last_travel_stitches and ending_point:
        new_sitches.extend(last_travel_stitches)
    return new_sitches
