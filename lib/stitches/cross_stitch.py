# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

from math import isclose

import networkx
from shapely import line_merge, prepare, snap
from shapely.affinity import scale, translate
from shapely.geometry import (LineString, MultiLineString, MultiPoint,
                              MultiPolygon, Point, Polygon)
from shapely.ops import nearest_points, unary_union

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_multi_line_string, ensure_multi_point,
                              reverse_line_string)
from ..utils.threading import check_stop_flag
from .auto_fill import (add_edges_between_outline_nodes, fallback,
                        find_stitch_path, graph_make_valid,
                        process_travel_edges,
                        tag_nodes_with_outline_and_projection)
from .circular_fill import _apply_bean_stitch_and_repeats


@debug.time
def cross_stitch(fill, shape, starting_point, ending_point):
    '''Cross stitch fill type

       Cross stitches are organized in a pixelated pattern. Each "cross pixel" (box) has two diagonals.
       Traditionally cross stitches are strictly organized and each cross follows the same pattern.
       Meaning the layering of the diagonals can't be switched during the stitch out.
       For example all crosses start with '\' as a bottom layer and end with '/' as the top layer.
    '''
    max_stitch_length = fill.max_cross_stitch_length
    cross_diagonals1, cross_diagonals2, boxes, scaled_boxes, snap_points, travel_edges, = get_cross_geomteries(
        shape, fill.pattern_size, fill.fill_coverage, fill.cross_offset
    )
    if not boxes:
        return []

    # Fix outline. The outline for cross stitches is a bit delicate as it tends to be invalid in a shapely sense.
    # We created scaled boxes to avoid a splitting up of an outline which we would be able to render in one go.
    # But we only want to use the scaled boxes if it is really necessary.
    # It is also possible that the cross stitch pattern is fully unconnected. In this case, we will run the stitch
    # generation on each outline component.
    outline_scaled = False
    outline = unary_union(boxes)
    if outline.geom_type == 'MultiPolygon':
        outline = unary_union(scaled_boxes)
        if outline.geom_type == 'MultiPolygon':
            # we will have to run this on multiple outline shapes
            return cross_stitch_multiple(outline, fill, starting_point, ending_point)
        outline_scaled = True

    # used for snapping
    center_points = MultiPoint(snap_points[0])
    snap_points = MultiPoint(snap_points[0] + snap_points[1])

    # The cross stitch diagnonals
    diagonals1 = ensure_multi_line_string(line_merge(MultiLineString(cross_diagonals1)).segmentize(max_stitch_length))
    diagonals2 = ensure_multi_line_string(line_merge(MultiLineString(cross_diagonals2)).segmentize(max_stitch_length))
    # Travel edges includ all possible edges, the box outlines, as well as edges from the bounding boxes corners to the box center (☒)
    travel_edges = ensure_multi_line_string(line_merge(MultiLineString(travel_edges)))

    # we might have enlarged our outline to connect even crosses which only touch at one corner
    # therefore it is necessary to adjust our geometries to the new outline
    if outline_scaled:
        diagonals1 = ensure_multi_line_string(snap(diagonals1, outline, tolerance=0.000001))
        diagonals2 = ensure_multi_line_string(snap(diagonals2, outline, tolerance=0.000001))
        travel_edges = ensure_multi_line_string(snap(travel_edges, outline, tolerance=0.000001))
        snap_points = ensure_multi_point(snap(snap_points, outline, tolerance=0.000001))
    travel_edges = list(travel_edges.geoms)

    # Nodes include all end points of our grating lines
    nodes = get_line_endpoints(diagonals2)
    nodes.extend(get_line_endpoints(diagonals1))

    # Snap start and end points to spots which are actually part of the cross stitch pattern
    starting_point, ending_point = get_start_and_end(starting_point, ending_point, snap_points)

    if fill.cross_stitch_method in ['simple_cross_flipped', 'half_cross_flipped']:
        diagonals2, diagonals1 = diagonals1, diagonals2

    half_stitch = False
    last_pass = False
    underpath = True
    if fill.cross_stitch_method in ['half_cross', 'half_cross_flipped']:
        last_pass = True
        half_stitch = True
        underpath = False

    # We finally finished with all the preparations. Let's convert our crosses to routed stitches
    stitches = _lines_to_stitches(
        diagonals1, travel_edges, outline, max_stitch_length, fill.bean_stitch_repeats,
        starting_point, ending_point, nodes, center_points, last_pass, underpath
    )

    if not half_stitch:
        if not fill.cross_stitch_method == ['double_cross']:
            last_pass = True
        starting_point = InkstitchPoint(*stitches[-1])
        stitches.extend(
            _lines_to_stitches(
                diagonals2, travel_edges, outline, max_stitch_length, fill.bean_stitch_repeats,
                starting_point, ending_point, nodes, center_points, last_pass, underpath
            )
        )

    return [stitches]


def cross_stitch_multiple(outline, fill, starting_point, ending_point):
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
        stitches.extend(cross_stitch(fill, polygon, starting_point, end))
        starting_point = InkstitchPoint(*stitches[-1][-1])
    return stitches


def get_start_and_end(starting_point, ending_point, snap_points):
    '''Snap starting and ending point on existng spots on our cross stitch pattern
    '''
    if starting_point is not None:
        starting_point = nearest_points(snap_points, Point(starting_point))[0].coords
    if ending_point is not None:
        ending_point = nearest_points(snap_points, Point(ending_point))[0].coords
    return starting_point, ending_point


def get_line_endpoints(multilinestring):
    '''Returns the endpoints of each line from a multilinestring
    '''
    nodes = []
    for line in multilinestring.geoms:
        coords = list(line.coords)
        nodes.extend((coords[0], coords[-1]))
    return nodes


def get_cross_geomteries(shape, box_size, coverage, offset):
    '''Generates data for cross stitch geometry, including:

       boxes:                   a list of box shaped polygons. The outlines for each cross.
                                To get the final outline for our cross stitch pattern,
                                we will combine all available boxes to a (hopefully) single shape.

       scaled_boxes:            same as boxes, except that the boxes are scaled p slightly.
                                Used to reconnect shapes which would be disconnected otherwise.
                                A good example for this are crosses which are touching each other at only one corner.

        diagonals1, diagonals2: A list of Linestrings with the actual cross stitch geometry

        travel_edges:           a list of Linestings with every possible edge in a cross stitch box:
                                the box outlines as well as lines from the box cornes to the center

        snap_points:            a list containing two lists with points.
                                1. the center points for each box
                                2. the four corners of each box
    '''
    box_x, box_y = box_size
    offset_x, offset_y = offset
    square = Polygon([(0, 0), (box_x, 0), (box_x, box_y), (0, box_y)])
    full_square_area = square.area

    # start and end have to be a multiple of the stitch length
    # we also add the initial offset
    minx, miny, maxx, maxy = shape.bounds
    adapted_minx = minx - minx % box_x - offset_x
    adapted_miny = miny - miny % box_y + offset_y
    adapted_maxx = maxx + box_x - maxx % box_x
    adapted_maxy = maxy + box_y - maxy % box_y
    prepare(shape)

    boxes = []
    scaled_boxes = []

    cross_diagonals1 = []
    cross_diagonals2 = []

    travel_edges = []
    snap_points = [[], []]

    y = adapted_miny
    while y <= adapted_maxy:
        x = adapted_minx
        while x <= adapted_maxx:
            # translate box to cross position
            box = translate(square, x, y)
            if shape.contains(box):
                boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points = add_cross(
                    box, boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points
                )
            elif shape.intersects(box):
                intersection = box.intersection(shape)
                intersection_area = intersection.area
                if intersection_area / full_square_area * 100 + 0.0001 >= coverage:
                    boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points = add_cross(
                        box, boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points
                    )
            x += box_x
        y += box_y
        check_stop_flag()
    return cross_diagonals1, cross_diagonals2, boxes, scaled_boxes, snap_points, travel_edges


def add_cross(box, boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points):
    # snap onto existing boxes to avoid floating point inacurracies
    box = snap(box, MultiPolygon(boxes), tolerance=0.0001)

    minx, miny, maxx, maxy = box.bounds
    center = box.centroid

    boxes.append(box)
    scaled_boxes.append(scale(box, xfact=1.0000000000001, yfact=1.0000000000001))

    cross_diagonals1.append(LineString([(minx, miny), (maxx, maxy)]))
    cross_diagonals2.append(LineString([(maxx, miny), (minx, maxy)]))

    travel_edges.append(LineString([(minx, miny), center]))
    travel_edges.append(LineString([(maxx, miny), center]))
    travel_edges.append(LineString([(maxx, maxy), center]))
    travel_edges.append(LineString([(minx, maxy), center]))
    travel_edges.append(LineString([(minx, miny), (maxx, miny)]))
    travel_edges.append(LineString([(minx, miny), (minx, maxy)]))
    travel_edges.append(LineString([(maxx, maxy), (maxx, miny)]))
    travel_edges.append(LineString([(maxx, maxy), (minx, maxy)]))

    snap_points[0].append(center)
    snap_points[1].append((minx, miny))
    snap_points[1].append((minx, maxy))
    snap_points[1].append((maxx, miny))
    snap_points[1].append((maxx, maxy))

    return boxes, scaled_boxes, cross_diagonals1, cross_diagonals2, travel_edges, snap_points


def _lines_to_stitches(
        line_geoms, travel_edges, shape, max_stitch_length,
        bean_stitch_repeats, starting_point, ending_point,
        nodes, snap_points, last_pass, underpath):
    segments = []
    for line in line_geoms.geoms:
        segments.append(list(line.coords))

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if networkx.is_empty(fill_stitch_graph):
        return fallback(shape, max_stitch_length, 0.2)
    if not networkx.is_connected(fill_stitch_graph):
        return fallback(shape, max_stitch_length, 0.2)
    else:
        graph_make_valid(fill_stitch_graph)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, travel_edges, nodes, underpath)
    graph_make_valid(travel_graph)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
    result = path_to_stitches(
        shape, path, travel_graph, fill_stitch_graph, max_stitch_length, snap_points, underpath
    )
    result = collapse_travel_edges(result, last_pass)
    result = filter_center_points(result, snap_points)
    result = _apply_bean_stitch_and_repeats(result, 1, bean_stitch_repeats)
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
        graph.add_edge(segment[0], segment[-1], key="segment", underpath_edges=[], geometry=LineString(segment))

        check_stop_flag()

    tag_nodes_with_outline_and_projection(graph, shape, graph.nodes())
    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    debug.log_graph(graph, "graph")

    return graph


def build_travel_graph(fill_stitch_graph, shape, travel_edges, nodes, underpath):
    """Build a graph for travel stitches.

       See full explanatio in the auto_fill file.
       Here we create different grating lines (using the travel edges)
    """
    graph = networkx.MultiGraph()

    # Add all the nodes from the main graph.  This will be all of the endpoints
    # of the rows of stitches.  Every node will be on the outline of the shape.
    # They'll all adiagonals1eady have their `outline` and `projection` tags set.
    graph.add_nodes_from(fill_stitch_graph.nodes(data=True))

    if underpath:
        # This will ensure that a path traveling inside the shape can reach its
        # target on the outline, which will be one of the points added above.
        tag_nodes_with_outline_and_projection(graph, shape, nodes)
    else:
        add_boundary_travel_nodes(graph, shape)

    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    if underpath:
        process_travel_edges(graph, fill_stitch_graph, shape, travel_edges)

    debug.log_graph(graph, "travel graph")

    return graph


def add_boundary_travel_nodes(graph, shape):
    outlines = ensure_multi_line_string(shape.boundary).geoms
    for outline_index, outline in enumerate(outlines):
        for point in outline.coords:
            check_stop_flag()
            point = Point(point)
            graph.add_node((point.x, point.y), projection=outline.project(point), outline=outline_index)


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, max_stitch_length, snap_points, underpath):
    ''' Convert path to stitch data
        while shortening travel paths and adapting the travel edges to the crosses
    '''
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
            stitches.extend(travel(shape, travel_graph, edge, snap_points, max_stitch_length, underpath))

    return stitches


def travel(shape, travel_graph, edge, snap_points, max_stitch_length, underpath):
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

    # At this point we are almost happy with the path. But we have some segments not following the crosses, but their bounding boxes.
    # This means, we will need to add some extra points.
    stitches = []
    last_point = None
    for point in path:
        check_stop_flag()
        if last_point is None:
            last_point = point
            continue
        line = LineString([last_point, point])
        if underpath and (last_point[0] == point[0] or last_point[1] == point[1]):
            # We are traveling along the outside of a cross stitch box (x1 == x2 or y1 == y2)
            # This means, we will need to add a stitch at the center of the box to we create a V shaped line.
            # To do this, we grab the center of the path and snap it to the nearest box center point we can find
            center_point = line.interpolate(0.5, normalized=True)
            center_point = Point(nearest_points(center_point, snap_points)[1].coords)
            line = LineString([last_point, center_point, point])
        stitches.extend([Stitch(*coord, tags=["auto_fill_travel"]) for coord in list(line.segmentize(max_stitch_length).coords)[1:]])
        last_point = point

    return stitches


def collapse_travel_edges(result, last_pass):
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
            last_travel_stitches.append(stitch)
            new_sitches.extend(last_travel_stitches)
            last_travel_stitches = []
    if last_travel_stitches and last_pass:
        new_sitches.extend(last_travel_stitches)
    return new_sitches


def filter_center_points(stitches, center_points):
    '''Filter unnecessary stitches at the center of the cross stitch boxes

       For routing we did add nodes to the centers of each cross stitch box.
       Travel pathes are incorporating these additional nodes.
       When we travel completely diagnolly through a box, we can ommit these extra stitches.
    '''
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
