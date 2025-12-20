# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

from math import isclose, sqrt

import networkx
from shapely import line_merge, prepare, snap
from shapely.affinity import rotate, scale, translate
from shapely.geometry import (LineString, MultiLineString, MultiPoint, Point,
                              Polygon)
from shapely.ops import nearest_points, unary_union

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_multi_line_string, ensure_multi_point,
                              reverse_line_string)
from ..utils.threading import check_stop_flag
from .auto_fill import (add_edges_between_outline_nodes,
                        build_fill_stitch_graph, fallback, find_stitch_path,
                        graph_make_valid, process_travel_edges,
                        tag_nodes_with_outline_and_projection)
from .circular_fill import _apply_bean_stitch_and_repeats


@debug.time
def cross_stitch(fill, shape, starting_point, ending_point):
    stitch_length = fill.max_stitch_length
    cross_diagonals1, cross_diagonals2, vertical, boxes, scaled_boxes, snap_points, travel_edges = get_cross_geomteries(
        shape, stitch_length, fill.cross_coverage
    )

    if not boxes:
        return []

    # Fix outline
    clamp = False
    outline = unary_union(boxes)
    if outline.geom_type == 'MultiPolygon':
        outline = unary_union(scaled_boxes)
        if outline.geom_type == 'MultiPolygon':
            # we will have to run this on multiple outline shapes
            return cross_stitch_multiple(outline, fill, starting_point, ending_point)
        clamp = True

    # used for snapping
    center_points = MultiPoint(snap_points[0])
    snap_points = MultiPoint(snap_points[0] + snap_points[1])

    diagonals1 = ensure_multi_line_string(line_merge(MultiLineString(cross_diagonals1)))
    diagonals2 = ensure_multi_line_string(line_merge(MultiLineString(cross_diagonals2)))
    verticals = ensure_multi_line_string(line_merge(MultiLineString(vertical)))
    travel_edges = ensure_multi_line_string(line_merge(MultiLineString(travel_edges)))

    # we might have enlarged our outline to connect even crosses which only touch at one corner
    # therefore it is necessary to adjust our geometries to the new outline
    if clamp:
        diagonals1 = ensure_multi_line_string(snap(diagonals1, outline, tolerance=0.000001))
        diagonals2 = ensure_multi_line_string(snap(diagonals2, outline, tolerance=0.000001))
        verticals = ensure_multi_line_string(snap(verticals, outline, tolerance=0.000001))
        travel_edges = ensure_multi_line_string(snap(travel_edges, outline, tolerance=0.000001))
        snap_points = ensure_multi_point(snap(snap_points, outline, tolerance=0.000001))
    travel_edges = list(travel_edges.geoms)

    nodes = get_line_endpoints(diagonals2)
    nodes.extend(get_line_endpoints(diagonals1))
    nodes.extend(get_line_endpoints(verticals))

    starting_point, ending_point = get_start_and_end(starting_point, ending_point, snap_points)

    if fill.flip_layers:
        diagonals2, diagonals1 = diagonals1, diagonals2

    stitches = _lines_to_stitches(
        diagonals1, travel_edges, outline, stitch_length, fill.bean_stitch_repeats,
        starting_point, ending_point, nodes, center_points, clamp
    )
    starting_point = InkstitchPoint(*stitches[-1])
    stitches.extend(
        _lines_to_stitches(
            diagonals2, travel_edges, outline, stitch_length, fill.bean_stitch_repeats,
            starting_point, ending_point, nodes, center_points, clamp
        )
    )

    return [stitches]


def cross_stitch_multiple(outline, fill, starting_point, ending_point):
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
        stitches.extend(cross_stitch(fill, polygon, starting_point, end))
        starting_point = InkstitchPoint(*stitches[-1][-1])
    return stitches


def get_start_and_end(starting_point, ending_point, snap_points):
    if starting_point is not None:
        starting_point = nearest_points(snap_points, Point(starting_point))[0].coords
    if ending_point is not None:
        ending_point = nearest_points(snap_points, Point(ending_point))[0].coords
    return starting_point, ending_point


def get_line_endpoints(multilinestring):
    nodes = []
    for line in multilinestring.geoms:
        coords = list(line.coords)
        nodes.extend((coords[0], coords[-1]))
    return nodes


def get_cross_geomteries(shape, stitch_length, coverage):
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

    cross_diagonals1 = []
    cross_diagonals2 = []
    vertical = []
    boxes = []
    scaled_boxes = []
    snap_points = [[], []]
    travel_edges = []

    y = adapted_miny
    while y <= adapted_maxy:
        x = adapted_minx
        while x <= adapted_maxx:
            box = translate(square, x, y)
            if shape.contains(box):
                travel_edges, boxes, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical = add_cross(
                    box, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical, boxes, travel_edges
                )
            elif shape.intersects(box):
                intersection = box.intersection(shape)
                intersection_area = intersection.area
                if intersection_area / full_square_area * 100 > coverage:
                    travel_edges, boxes, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical = add_cross(
                        box, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical, boxes, travel_edges
                    )
            x += square_size
        y += square_size
        check_stop_flag()
    return cross_diagonals1, cross_diagonals2, vertical, boxes, scaled_boxes, snap_points, travel_edges


def add_cross(box, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical, boxes, travel_edges):
    minx, miny, maxx, maxy = box.bounds
    center = box.centroid
    snap_points[0].append(center)
    snap_points[1].append((minx, miny))
    snap_points[1].append((minx, maxy))
    snap_points[1].append((maxx, miny))
    snap_points[1].append((maxx, maxy))

    cross_diagonals1.append(LineString([(minx, miny), (maxx, maxy)]))
    cross_diagonals2.append(LineString([(maxx, miny), (minx, maxy)]))
    vertical.append(LineString([(maxx, miny), (maxx, maxy)]))

    travel_edges.append(LineString([(minx, miny), center]))
    travel_edges.append(LineString([(maxx, miny), center]))
    travel_edges.append(LineString([(maxx, maxy), center]))
    travel_edges.append(LineString([(minx, maxy), center]))
    travel_edges.append(LineString([(minx, miny), (maxx, miny)]))
    travel_edges.append(LineString([(minx, miny), (minx, maxy)]))
    travel_edges.append(LineString([(maxx, maxy), (maxx, miny)]))
    travel_edges.append(LineString([(maxx, maxy), (minx, maxy)]))

    boxes.append(box)
    # scaling the outline allows us to connect otherwise unconnected boxes
    box = scale(box, xfact=1.0000000000001, yfact=1.0000000000001)
    scaled_boxes.append(box)

    return travel_edges, boxes, scaled_boxes, snap_points, cross_diagonals1, cross_diagonals2, vertical


def _lines_to_stitches(
        line_geoms, travel_edges, shape, stitch_length,
        bean_stitch_repeats, starting_point, ending_point, nodes, snap_points, clamp):
    segments = []
    for line in line_geoms.geoms:
        segments.append(list(line.coords))

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    graph_make_valid(fill_stitch_graph)

    if networkx.is_empty(fill_stitch_graph):
        return fallback(shape, stitch_length, 0.2)
    if not networkx.is_connected(fill_stitch_graph):
        return fallback(shape, stitch_length, 0.2)
    else:
        graph_make_valid(fill_stitch_graph)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, travel_edges, nodes)
    graph_make_valid(travel_graph)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
    result = path_to_stitches(
        shape, path, travel_graph, fill_stitch_graph, stitch_length, snap_points, clamp
    )
    result = collapse_travel_edges(result)
    result = filter_center_points(result, snap_points)
    result = _apply_bean_stitch_and_repeats(result, 1, bean_stitch_repeats)
    return result


def build_travel_graph(fill_stitch_graph, shape, travel_edges, nodes):
    """Build a graph for travel stitches.
    """
    graph = networkx.MultiGraph()

    # Add all the nodes from the main graph.  This will be all of the endpoints
    # of the rows of stitches.  Every node will be on the outline of the shape.
    # They'll all adiagonals1eady have their `outline` and `projection` tags set.
    graph.add_nodes_from(fill_stitch_graph.nodes(data=True))

    # This will ensure that a path traveling inside the shape can reach its
    # target on the outline, which will be one of the points added above.
    tag_nodes_with_outline_and_projection(graph, shape, nodes)
    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    process_travel_edges(graph, fill_stitch_graph, shape, travel_edges)

    debug.log_graph(graph, "travel graph")

    return graph


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, stitch_length, snap_points, clamp):
    stitches = []
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for i, edge in enumerate(path):
        check_stop_flag()
        if edge.is_segment():
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']

            if edge[0] != path_geometry.coords[0]:
                path_geometry = reverse_line_string(path_geometry)

            stitches.extend([Stitch(*point, tags=["auto_fill", "fill_row"]) for point in path_geometry.coords])

            if fill_stitch_graph.has_edge(edge[0], edge[1], key='segment'):
                travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(shape, travel_graph, edge, snap_points, stitch_length, clamp))

    return stitches


def travel(shape, travel_graph, edge, snap_points, stitch_length, clamp=True):
    """Create stitches to get from one point on an outline of the shape to another."""

    start, end = edge
    try:
        path = networkx.shortest_path(travel_graph, start, end, weight='weight')
    except networkx.NetworkXNoPath:
        # This may not look good, but it prevents the fill from failing (which hopefully never happens)
        path = [start, end]

    path = [InkstitchPoint.from_tuple(point) for point in path]
    if not path:
        # This may happen on very small shapes.
        # Simply return nothing as we do not want to error out
        return []

    if len(path) > 1:
        path = clamp_path_to_polygon(path, shape)

    stitches = []
    last_point = None
    for point in path:
        check_stop_flag()
        if last_point is None:
            last_point = point
            continue
        line = LineString([last_point, point])
        if line.length < stitch_length / 2:
            pass
        elif not isclose(last_point[0], point[0], abs_tol=0.011) and not isclose(last_point[1], point[1], abs_tol=0.011):
            pass
        else:
            center = list(rotate(line, 90).coords)
            point1 = Point(center[0])
            if point1.within(shape):
                center_point = point1
            else:
                center_point = Point(center[1])
            # snap to avoid issues with collapsing travel paths due to floating point inaccuracies
            center_point = Point(nearest_points(center_point, snap_points)[1].coords)
            stitches.append(Stitch(center_point, tags=["auto_fill_travel"]))
        stitches.append(Stitch(*point, tags=["auto_fill_travel"]))
        last_point = point

    return stitches


def collapse_travel_edges(result):
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
            last_travel_stitches.append(stitch)
            new_sitches.extend(last_travel_stitches)
            last_travel_stitches = []
    if last_travel_stitches:
        new_sitches.extend(last_travel_stitches)
    return new_sitches


def filter_center_points(stitches, center_points):
    filtered_stitches = []
    last_was_center = False
    for stitch in stitches:
        if 'auto_fill_travel' not in stitch.tags:
            filtered_stitches.append(stitch)
        else:
            point = Point(stitch)
            if point.distance(center_points) == 0:
                last_was_center = True
                filtered_stitches.append(stitch)
            else:
                if last_was_center and len(filtered_stitches) > 2:
                    last_stitch = InkstitchPoint(*filtered_stitches[-2])
                    center = InkstitchPoint(*filtered_stitches[-1])
                    point = InkstitchPoint(*stitch)
                    segment1 = (last_stitch-center).unit()
                    segment2 = (center-point).unit()
                    if isclose(segment1[0], segment2[0], abs_tol=0.011) and isclose(segment1[1], segment2[1], abs_tol=0.011):
                        filtered_stitches = filtered_stitches[:-1]
                filtered_stitches.append(stitch)
                last_was_center = False
    return filtered_stitches
