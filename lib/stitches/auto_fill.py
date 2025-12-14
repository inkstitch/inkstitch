# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

import math
from itertools import chain, groupby
from typing import Iterator

import networkx
from shapely import geometry as shgeo
from shapely import make_valid, segmentize, set_precision
from shapely.ops import snap, unary_union
from shapely.strtree import STRtree

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..svg import PIXELS_PER_MM
from ..utils import cache
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_multi_line_string, ensure_polygon,
                              line_string_to_point_list, offset_points)
from ..utils.list import is_all_zeroes
from ..utils.prng import join_args
from ..utils.smoothing import smooth_path
from ..utils.threading import check_stop_flag
from .fill import intersect_region_with_grating, stitch_row
from .running_stitch import even_running_stitch


class NoGratingsError(Exception):
    pass


class PathEdge(object):
    OUTLINE_KEYS = ("outline", "extra", "initial")
    SEGMENT_KEY = "segment"

    def __init__(self, nodes, key):
        self.nodes = nodes
        self._sorted_nodes = tuple(sorted(self.nodes))
        self.key = key

    def __getitem__(self, item):
        return self.nodes[item]

    def __hash__(self):
        return hash((self._sorted_nodes, self.key))

    def __repr__(self):
        return f"PathEdge({self.key}, {self.nodes})"

    def __eq__(self, other):
        return self._sorted_nodes == other._sorted_nodes and self.key == other.key

    def __iter__(self) -> Iterator:
        for i in range(2):
            yield self[i]

    def is_outline(self):
        return self.key.startswith(self.OUTLINE_KEYS)

    def is_segment(self):
        return self.key.startswith(self.SEGMENT_KEY)


@debug.time
def auto_fill(shape,
              angle,
              row_spacing,
              end_row_spacing,
              max_stitch_length,
              running_stitch_length,
              running_stitch_tolerance,
              staggers,
              skip_last,
              starting_point,
              ending_point=None,
              underpath=True,
              gap_fill_rows=0,
              enable_random_stitch_length=False,
              random_sigma=0.0,
              random_seed="",
              pull_compensation_px=(0, 0),
              pull_compensation_percent=(0, 0)):
    has_pull_compensation = not is_all_zeroes(pull_compensation_px) or not is_all_zeroes(pull_compensation_percent)
    if has_pull_compensation:
        spacing = min(row_spacing, end_row_spacing or row_spacing)
        shape = adjust_shape_for_pull_compensation(shape, angle, spacing, pull_compensation_px, pull_compensation_percent)

    rows = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing)
    if not rows:
        # Small shapes may not intersect with the grating at all.
        return fallback(shape, running_stitch_length, running_stitch_tolerance)
    segments = [segment for row in rows for segment in row]
    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if networkx.is_empty(fill_stitch_graph):
        # The graph may be empty if the shape is so small that it fits between the
        # rows of stitching.
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    # ensure graph is eulerian
    graph_make_valid(fill_stitch_graph)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)

    if not travel_graph:
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, underpath)
    path = fill_gaps(path, round_to_multiple_of_2(gap_fill_rows))
    result = path_to_stitches(shape, path, travel_graph, fill_stitch_graph, angle, row_spacing,
                              max_stitch_length, running_stitch_length, running_stitch_tolerance,
                              staggers, skip_last, underpath, enable_random_stitch_length, random_sigma, random_seed)

    return result


def round_to_multiple_of_2(number):
    if number % 2 == 1:
        return number + 1
    else:
        return number


@debug.time
def adjust_shape_for_pull_compensation(shape, angle, row_spacing, pull_compensation_px, pull_compensation_percent):
    rows = intersect_region_with_grating(shape, angle, row_spacing)
    if not rows:
        return shape
    segments = [segment for row in rows for segment in row]
    segments = apply_pull_compensation(segments, pull_compensation_px, pull_compensation_percent)

    lines = [shgeo.LineString((start, end)) for start, end in segments]
    buffer_amount = row_spacing/2 + 0.01
    buffered_lines = [line.buffer(buffer_amount) for line in lines]

    polygon = ensure_polygon(unary_union(buffered_lines))
    exterior = smooth_path(polygon.exterior.coords, 0.2)
    min_hole_area = row_spacing ** 2
    interiors = [smooth_path(interior.coords) for interior in polygon.interiors if shgeo.Polygon(interior).area > min_hole_area]

    shape = make_valid(shgeo.Polygon(exterior, interiors))
    shape = ensure_polygon(shape)

    return shape


def apply_pull_compensation(segments, pull_compensation_px, pull_compensation_percent):
    new_segments = []
    for segment in segments:
        start = InkstitchPoint.from_tuple(segment[0])
        end = InkstitchPoint.from_tuple(segment[1])
        end = InkstitchPoint.from_tuple(segment[1])
        new_start, new_end = offset_points(start, end, pull_compensation_px, pull_compensation_percent)
        new_segments.append((new_start.as_tuple(), new_end.as_tuple()))

    return new_segments


def which_outline(shape, coords):
    """return the index of the outline on which the point resides

    Index 0 is the outer boundary of the fill region.  1+ are the
    outlines of the holes.
    """

    # I'd use an intersection check, but floating point errors make it
    # fail sometimes.

    point = shgeo.Point(*coords)
    outlines, outline_indices = get_shape_outlines_and_indices(shape)
    closest = min(outline_indices,
                  key=lambda index: outlines[index].distance(point))
    return closest


@cache
def get_shape_outlines_and_indices(shape):
    outlines = ensure_multi_line_string(shape.boundary).geoms
    outline_indices = list(range(len(outlines)))
    return outlines, outline_indices


def project(shape, coords, outline_index):
    """project the point onto the specified outline

    This returns the distance along the outline at which the point resides.
    """

    outline = ensure_multi_line_string(shape.boundary).geoms[outline_index]

    return outline.project(shgeo.Point(*coords))


@debug.time
def build_fill_stitch_graph(shape, segments, starting_point=None, ending_point=None):
    """build a graph representation of the grating segments

    This function builds a specialized graph (as in graph theory) that will
    help us determine a stitching path.  The idea comes from this paper:

    http://www.sciencedirect.com/science/article/pii/S0925772100000158

    The goal is to build a graph that we know must have an Eulerian Path.
    An Eulerian Path is a path from edge to edge in the graph that visits
    every edge exactly once and ends at the node it started at.  Algorithms
    exist to build such a path, and we'll use Hierholzer's algorithm.

    A graph must have an Eulerian Path if every node in the graph has an
    even number of edges touching it.  Our goal here is to build a graph
    that will have this property.

    Based on the paper linked above, we'll build the graph as follows:

        * nodes are the endpoints of the grating segments, where they meet
        with the outer outline of the region the outlines of the interior
        holes in the region.
        * edges are:
        * each section of the outer and inner outlines of the region,
            between nodes
        * double every other edge in the outer and inner hole outlines

    Doubling up on some of the edges seems as if it will just mean we have
    to stitch those spots twice.  This may be true, but it also ensures
    that every node has 4 edges touching it, ensuring that a valid stitch
    path must exist.
    """

    debug.add_layer("auto-fill fill stitch")

    graph = networkx.MultiGraph()

    # First, add the grating segments as edges.  We'll use the coordinates
    # of the endpoints as nodes, which networkx will add automatically.
    for segment in segments:
        # networkx allows us to label nodes with arbitrary data.  We'll
        # mark this one as a grating segment.
        graph.add_edge(segment[0], segment[-1], key="segment", underpath_edges=[], geometry=shgeo.LineString(segment))

        check_stop_flag()

    tag_nodes_with_outline_and_projection(graph, shape, graph.nodes())
    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    if starting_point:
        insert_node(graph, shape, starting_point)

    if ending_point:
        insert_node(graph, shape, ending_point)

    debug.log_graph(graph, "graph")

    return graph


def insert_node(graph, shape, point):
    """Add node to graph, splitting one of the outline edges"""

    point = tuple(point)
    outline = which_outline(shape, point)
    projection = project(shape, point, outline)
    projected_point = ensure_multi_line_string(shape.boundary).geoms[outline].interpolate(projection)
    node = (projected_point.x, projected_point.y)

    edges = []
    for start, end, key, data in graph.edges(keys=True, data=True):
        if key == "outline" and data['outline'] == outline:
            edges.append(((start, end), data))

    if len(edges) > 0:
        edge, data = min(edges, key=lambda edge_data: shgeo.LineString(edge_data[0]).distance(projected_point))
        graph.remove_edge(*edge, key="outline")
        graph.add_edge(edge[0], node, key="outline", **data)
        graph.add_edge(node, edge[1], key="outline", **data)
    else:
        # The node lies on an outline which has no intersection with any segment.
        # We need to add a segment to connect the inserted node with the nearest available edge from
        # an other outline.  It's the best we can do without running into networkx no path errors.
        for start, end, key, data in graph.edges(keys=True, data=True):
            if key == "outline":
                edges.append(((start, end), data))
        edge, data = min(edges, key=lambda edge_data: shgeo.LineString(edge_data[0]).distance(projected_point))
        line_segment = shgeo.LineString([edge[0], node])
        if line_segment.length > 10:
            line_segment = segmentize(line_segment, 10)
        graph.add_edge(edge[0], node, key='segment', underpath_edges=[], geometry=line_segment)
        graph.add_edge(node, edge[1], key='segment', underpath_edges=[], geometry=line_segment.reverse())

    tag_nodes_with_outline_and_projection(graph, shape, nodes=[node])


def tag_nodes_with_outline_and_projection(graph, shape, nodes):
    for node in nodes:
        outline_index = which_outline(shape, node)
        outline_projection = project(shape, node, outline_index)

        graph.add_node(node, outline=outline_index, projection=outline_projection)

        check_stop_flag()


def add_boundary_travel_nodes(graph, shape):
    outlines = ensure_multi_line_string(shape.boundary).geoms
    for outline_index, outline in enumerate(outlines):
        prev = None
        for point in outline.coords:
            point = shgeo.Point(point)
            if prev is not None:
                # Subdivide long straight line segments.  Otherwise we may not
                # have a node near the user's chosen starting or ending point
                length = point.distance(prev)
                segment = shgeo.LineString((prev, point))
                if length > 1:
                    # Just plot a point every pixel, that should be plenty of
                    # resolution.  A pixel is around a quarter of a millimeter.
                    for i in range(1, int(length)):
                        subpoint = segment.interpolate(i)
                        graph.add_node((subpoint.x, subpoint.y), projection=outline.project(subpoint), outline=outline_index)

            check_stop_flag()

            graph.add_node((point.x, point.y), projection=outline.project(point), outline=outline_index)
            prev = point


def add_edges_between_outline_nodes(graph, duplicate_every_other=False):
    """Add edges around the outlines of the graph, connecting sequential nodes.

    This function assumes that all nodes in the graph are on the outline of the
    shape.  It figures out which nodes are next to each other on the shape and
    connects them in the graph with an edge.

    Edges are tagged with their outline number and their position on that
    outline.
    """

    # returns a list of tuples: [(node, {data}), (node, {data}) ...]
    nodes = list(graph.nodes(data=True))
    nodes.sort(key=lambda node: (node[1]['outline'], node[1]['projection']))

    for outline_index, nodes in groupby(nodes, key=lambda node: node[1]['outline']):
        nodes = [node for node, data in nodes]

        # add an edge between each successive node
        for i, (node1, node2) in enumerate(zip(nodes, nodes[1:] + [nodes[0]])):
            data = dict(outline=outline_index, index=i)
            graph.add_edge(node1, node2, key="outline", **data)

            if i % 2 == 0:
                graph.add_edge(node1, node2, key="extra", **data)

        check_stop_flag()


def graph_make_valid(graph):
    if not networkx.is_eulerian(graph):
        newgraph = networkx.eulerize(graph)
        for start, end, key, data in newgraph.edges(keys=True, data=True):
            if isinstance(key, int):
                # make valid duplicated edges, we cannot use the very same key
                # again, but the automatic naming will not apply to the autofill algorithm
                graph_edges = graph[start][end]
                if 'segment' in graph_edges.keys():
                    data = graph_edges['segment']
                    graph.add_edge(start, end, key=f'segment-{key}', **data)
                elif 'outline' in graph_edges.keys():
                    data = graph_edges['outline']
                    graph.add_edge(start, end, key=f'outline-{key}', **data)
                elif 'extra' in graph_edges.keys():
                    data = graph_edges['extra']
                    graph.add_edge(start, end, key=f'extra-{key}', **data)
                elif 'initial' in graph_edges.keys():
                    data = graph_edges['initial']
                    graph.add_edge(start, end, key=f'initial-{key}', **data)


def fallback(shape, running_stitch_length, running_stitch_tolerance):
    """Generate stitches when the auto-fill algorithm fails.

    If we received an empty graph, we're not going to be able to run the
    auto-fill algorithm.  Instead, we'll just do running stitch around the
    outside of the shape.  In all likelihood, the shape is so small it won't
    matter.
    """

    boundary = ensure_multi_line_string(shape.boundary)
    outline = boundary.geoms[0]

    return even_running_stitch(line_string_to_point_list(outline), [running_stitch_length], running_stitch_tolerance)


@debug.time
def build_travel_graph(fill_stitch_graph, shape, fill_stitch_angle, underpath):
    """Build a graph for travel stitches.

    This graph will be used to find a stitch path between two spots on the
    outline of the shape.

    If underpath is False, we'll just be traveling
    around the outline of the shape, so the graph will only contain outline
    edges.

    If underpath is True, we'll also allow travel inside the shape.  We'll
    fill the shape with a cross-hatched grid of lines.  We'll construct a
    graph from them and use a shortest path algorithm to construct travel
    stitch paths in travel().

    When underpathing, we "encourage" the travel() function to travel inside
    the shape rather than on the boundary.  We do this by weighting the
    boundary edges extra so that they're more "expensive" in the shortest path
    calculation.  We also weight the interior edges extra proportional to
    how close they are to the boundary.
    """
    graph = networkx.MultiGraph()

    # Add all the nodes from the main graph.  This will be all of the endpoints
    # of the rows of stitches.  Every node will be on the outline of the shape.
    # They'll all already have their `outline` and `projection` tags set.
    graph.add_nodes_from(fill_stitch_graph.nodes(data=True))

    grating = True
    if underpath:
        try:
            boundary_points, travel_edges = build_travel_edges(shape, fill_stitch_angle)
        except NoGratingsError:
            grating = False

        if grating:
            # This will ensure that a path traveling inside the shape can reach its
            # target on the outline, which will be one of the points added above.
            tag_nodes_with_outline_and_projection(graph, shape, boundary_points)

    if not underpath or not grating:
        add_boundary_travel_nodes(graph, shape)

    add_edges_between_outline_nodes(graph)

    if underpath and grating:
        process_travel_edges(graph, fill_stitch_graph, shape, travel_edges)

    debug.log_graph(graph, "travel graph")

    return graph


def weight_edges_by_length(graph, multiplier=1):
    for start, end, key in graph.edges:
        p1 = InkstitchPoint(*start)
        p2 = InkstitchPoint(*end)

        graph[start][end][key]["weight"] = multiplier * p1.distance(p2)


def get_segments(graph):
    segments = []
    for start, end, key, data in graph.edges(keys=True, data=True):
        if key.startswith('segment'):
            segments.append(data["geometry"])

    return segments


def process_travel_edges(graph, fill_stitch_graph, shape, travel_edges):
    """Weight the interior edges and pre-calculate intersection with fill stitch rows."""

    # Set the weight equal to 3x the edge length, to encourage travel()
    # to avoid them.
    weight_edges_by_length(graph, 3)

    segments = get_segments(fill_stitch_graph)

    # The shapely documentation is pretty unclear on this.  An STRtree
    # allows for building a set of shapes and then efficiently testing
    # the set for intersection.  This allows us to do blazing-fast
    # queries of which line segments overlap each underpath edge.
    strtree = STRtree(segments)

    # This makes the distance calculations below a bit faster.  We're
    # not looking for high precision anyway.
    outline = set_precision(shape.boundary.simplify(0.5 * PIXELS_PER_MM, preserve_topology=False), 0.000001)

    for ls in travel_edges:
        # In most cases, ls will be a simple line segment.  If we're
        # unlucky, in rare cases we can get a tiny little extra squiggle
        # at the end that can be ignored.
        points = [InkstitchPoint(*coord) for coord in ls.coords]
        p1, p2 = points[0], points[-1]

        edge = (p1.as_tuple(), p2.as_tuple(), 'travel')

        for segment in strtree.query(ls, predicate='crosses'):
            segment_geom = strtree.geometries.take(segment)
            start = segment_geom.coords[0]
            end = segment_geom.coords[-1]
            fill_stitch_graph[start][end]['segment']['underpath_edges'].append(edge)

        # The weight of a travel edge is the length of the line segment.
        weight = p1.distance(p2)

        # Give a bonus to edges that are far from the outline of the shape.
        # This includes the outer outline and the outlines of the holes.
        # The result is that travel stitching will tend to hug the center
        # of the shape.
        weight /= ls.distance(outline) + 0.1

        graph.add_edge(*edge, weight=weight)

        check_stop_flag()

    # without this, we sometimes get exceptions like this:
    # Exception AttributeError: "'NoneType' object has no attribute 'GEOSSTRtree_destroy'" in
    #   <bound method STRtree.__del__ of <shapely.strtree.STRtree instance at 0x0D2BFD50>> ignored
    del strtree


def travel_grating(shape, angle, row_spacing):
    rows = intersect_region_with_grating(shape, angle, row_spacing)
    segments = [segment for row in rows for segment in row]

    return shgeo.MultiLineString(list(segments))


def build_travel_edges(shape, fill_angle):
    r"""Given a graph, compute the interior travel edges.

    We want to fill the shape with a grid of line segments that can be used for
    travel stitch routing.  Our goals:

      * not too many edges so that the shortest path algorithm is speedy
      * don't travel in the direction of the fill stitch rows so that the
        travel stitch doesn't visually disrupt the fill stitch pattern

    To do this, we'll fill the shape with three gratings: one at +45 degrees
    from the fill stitch angle, one at -45 degrees, and one at +90 degrees.
    The pattern looks like this:

    /|\|/|\|/|\
    \|/|\|/|\|/
    /|\|/|\|/|\
    \|/|\|/|\|/

    Returns: (endpoints, edges)
        endpoints - the points on travel edges that intersect with the boundary
                    of the shape
        edges     - the line segments we can travel on, as individual LineString
                    instances
    """

    # If the shape is smaller, we'll have less room to maneuver and it's more likely
    # we'll travel around the outside border of the shape.  Counteract that by making
    # the grid denser.
    if shape.area < 10000:
        scale = 0.5
    else:
        scale = 1.0

    grating1 = travel_grating(shape, fill_angle + math.pi / 4, scale * 2 * PIXELS_PER_MM)
    grating2 = travel_grating(shape, fill_angle - math.pi / 4, scale * 2 * PIXELS_PER_MM)
    grating3 = travel_grating(shape, fill_angle - math.pi / 2, scale * math.sqrt(2) * PIXELS_PER_MM)

    debug.add_layer("auto-fill travel")
    debug.log_line_strings(grating1, "grating1")
    debug.log_line_strings(grating2, "grating2")
    debug.log_line_strings(grating3, "grating3")

    endpoints = [coord for mls in (grating1, grating2, grating3)
                 for ls in mls.geoms
                 for coord in ls.coords]

    if grating1.is_empty or grating2.is_empty:
        raise NoGratingsError()

    diagonal_edges = ensure_multi_line_string(grating1.symmetric_difference(grating2))

    check_stop_flag()

    # without this, floating point inaccuracies prevent the intersection points from lining up perfectly.
    vertical_edges = ensure_multi_line_string(snap(grating3.difference(grating1), diagonal_edges, 0.005))

    check_stop_flag()

    return endpoints, chain(diagonal_edges.geoms, vertical_edges.geoms)


def nearest_node(nodes, point, attr=None):
    point = shgeo.Point(*point)
    nearest = min(nodes, key=lambda node: shgeo.Point(*node).distance(point))

    return nearest


@debug.time
def find_stitch_path(graph, travel_graph, starting_point=None, ending_point=None, underpath=True):
    """find a path that visits every grating segment exactly once

    Theoretically, we just need to find an Eulerian Path in the graph.
    However, we don't actually care whether every single edge is visited.
    The edges on the outline of the region are only there to help us get
    from one grating segment to the next.

    We'll build a Eulerian Path using Hierholzer's algorithm.  A true
    Eulerian Path would visit every single edge (including all the extras
    we inserted in build_graph()),but we'll stop short once we've visited
    every grating segment since that's all we really care about.

    Hierholzer's algorithm says to select an arbitrary starting node at
    each step.  In order to produce a reasonable stitch path, we'll select
    the starting node carefully such that we get back-and-forth traversal like
    mowing a lawn.

    To do this, we'll use a simple heuristic: try to start from nodes in
    the order of most-recently-visited first.
    """

    graph = graph.copy()
    composed_graph = networkx.compose(graph, travel_graph)

    if not starting_point:
        starting_point = list(graph.nodes.keys())[0]

    starting_node = nearest_node(graph, starting_point)

    if ending_point:
        ending_node = nearest_node(graph, ending_point)
    else:
        ending_point = starting_point
        ending_node = starting_node

    # The algorithm below is adapted from networkx.eulerian_circuit().
    path = []
    vertex_stack = [(ending_node, None)]
    last_vertex = None
    last_key = None

    # get the outline index for starting and ending node
    outline_start = travel_graph[starting_node][list(travel_graph[starting_node])[0]]['outline']['outline']
    outline_end = travel_graph[ending_node][list(travel_graph[ending_node])[0]]['outline']['outline']

    while vertex_stack:
        current_vertex, current_key = vertex_stack[-1]
        if graph.degree(current_vertex) == 0:
            if last_vertex:
                path.append(PathEdge((last_vertex, current_vertex), last_key))
            last_vertex, last_key = current_vertex, current_key
            vertex_stack.pop()
        else:
            ignore, next_vertex, next_key = pick_edge(graph.edges(current_vertex, keys=True))
            vertex_stack.append((next_vertex, next_key))
            graph.remove_edge(current_vertex, next_vertex, next_key)

    # The above has the excellent property that it tends to do travel stitches
    # before the rows in that area, so we can hide the travel stitches under
    # the rows.
    #
    # The only downside is that the path is a loop starting and ending at the
    # ending node.  We need to start at the starting node, so we'll just
    # start off by traveling to the ending node.
    #
    # Note, it's quite possible that part of this PathEdge will be eliminated by
    # collapse_sequential_outline_edges().

    if underpath or outline_start == outline_end:
        if starting_node is not ending_node:
            path.insert(0, PathEdge((starting_node, ending_node), key="initial"))
    else:
        # If underpath is disabled, we only have the option travel along the outline edges.
        # The user chose to start and end on different oultines, so there is no way to travel
        # along the edge from start to end. Add an additional path from start to end along existing
        # graph and travel edges (they will be duplicated).
        start_path = networkx.shortest_path(composed_graph, starting_node, ending_node, weight='weight')
        for i, edge in enumerate(list(zip(start_path, start_path[1:]))):
            # add as segment so it won't be collapsed
            if 'segment' in composed_graph[edge[0]][edge[1]].keys():
                path.insert(i, PathEdge(edge, key=f'segment-start{i}'))
            else:
                path.insert(i, PathEdge(edge, key=f'outline-start{i}'))

    # If the starting and/or ending point falls far away from the end of a row
    # of stitches (like can happen at the top of a square), then we need to
    # add travel stitch to that point.
    real_start = nearest_node(travel_graph, starting_point)
    path.insert(0, PathEdge((real_start, starting_node), key="outline"))

    # We're willing to start inside the shape, since we'll just cover the
    # stitches.  We have to end on the outline of the shape.  This is mostly
    # relevant in the case that the user specifies an underlay with an inset
    # value, because the starting point (and possibly ending point) can be
    # inside the shape.
    outline_nodes = [node for node, outline in travel_graph.nodes(data="outline") if outline is not None]
    real_end = nearest_node(outline_nodes, ending_point)
    path.append(PathEdge((ending_node, real_end), key="outline"))

    check_stop_flag()

    return path


def pick_edge(edges):
    """Pick the next edge to traverse in the pathfinding algorithm"""

    # Prefer a segment if one is available.  This has the effect of
    # creating long sections of back-and-forth row traversal.
    for source, node, key in edges:
        if key.startswith('segment'):
            return source, node, key

    return list(edges)[0]


def fill_gaps(path, num_rows):
    """Fill gaps between sections caused by fabric distortion.

    If we stitch some rows back and forth, then travel and stitch another
    section, and finally go back to continue on from the first section, there
    can be a gap. This is most noticeable on stretchy fabrics or with poor
    stabilization.

    In this function we'll detect cases where gaps may appear and stitch a few
    extra rows in the gap.

    We'll detect gaps by finding cases where our stitch path does some
    back-and-forth rows of fill stitch and then travels.  It looks like this:

    segment, outline, segment, outline, segment, outline, *outline, outline

    The asterisk indicates where we started to travel.  We'll repeat the last
    row offset by the row spacing 2, 4, 6, or more times, always an even number
    so that we end up near the same spot.
    """

    if num_rows <= 0:
        return path

    # Problem: our algorithm in find_stitch_path() sometimes (often) adds
    # unnecessary loops of travel stitching.  We'll need to eliminate these for
    # the gap detection to work.
    path = remove_loops(path)

    if len(path) < 3:
        return path

    new_path = []
    last_edge = None
    rows_in_section = 0

    for edge in path:
        if last_edge:
            if edge.is_segment() and last_edge.is_outline():
                rows_in_section += 1
            if edge.is_outline() and last_edge.is_outline():
                # we hit the end of a section of alternating segment-outline-segment-outline
                if rows_in_section > 3:
                    # The path has already started traveling on to the new
                    # section, so save it and add it back on after.
                    next_edge = new_path.pop()
                    fill_gap(new_path, num_rows)
                    new_path.append(next_edge)

                rows_in_section = 0
        last_edge = edge
        new_path.append(edge)

    return new_path


def remove_loops(path):
    if len(path) < 2:
        return path

    new_path = []

    # seen_nodes tracks the nodes we've visited and the index _after_ that node.
    # If we see that node again, we'll use the index to delete the intervening
    # section of the path.
    seen_nodes = {}

    for edge in path:
        if edge.is_segment():
            new_path.append(edge)
            seen_nodes.clear()
            continue

        start, end = edge
        if end in seen_nodes:
            del new_path[seen_nodes[end]:]
            seen_nodes.clear()
            continue
        else:
            new_path.append(edge)
            seen_nodes[end] = len(new_path)

    return new_path


def fill_gap(path, num_rows):
    """Fill a gap by repeating the last row."""

    original_end = path[-1][1]
    last_row = (InkstitchPoint.from_tuple(path[-1][0]), InkstitchPoint.from_tuple(path[-1][1]))
    penultimate_row = (InkstitchPoint.from_tuple(path[-3][0]), InkstitchPoint.from_tuple(path[-3][1]))
    last_row_direction = (last_row[1] - last_row[0]).unit()

    offset_direction = last_row_direction.rotate_left()
    if (last_row[1] - penultimate_row[0]) * offset_direction < 0:
        offset_direction *= -1
    spacing = (last_row[1] - penultimate_row[0]) * offset_direction
    offset = offset_direction * spacing

    for i in range(num_rows):
        # calculate the next row, which looks like the last row, but backward and offset
        end, start = last_row
        start += offset
        end += offset

        # Get from the last row to this row.  Note that we're calling this a segment to
        # avoid the underpath algorithm trying to turn this into travel stitch.
        path.append(PathEdge((last_row[1].as_tuple(), start.as_tuple()), 'segment'))

        # Add this extra row.
        path.append(PathEdge((start.as_tuple(), end.as_tuple()), 'segment'))

        last_row = (start, end)

    # go back to where we started
    path.append(PathEdge((last_row[1].as_tuple(), original_end), 'segment'))

    return path


def collapse_sequential_outline_edges(path, graph):
    """collapse sequential edges that fall on the same outline

    When the path follows multiple edges along the outline of the region,
    replace those edges with the starting and ending points.  We'll use
    these to underpath later on.
    """

    start_of_run = None
    new_path = []

    for edge in path:
        if edge.is_segment():
            if start_of_run:
                # Collapse the run of edges along the outline.  If we're
                # traveling from one segment to its neighbor, we can just go
                # there directly.  Otherwise, we're going to have to underpath.
                # The tricky thing is that even if we're going to a neighboring
                # segment, the algorithm may have taken a weird route to get
                # there, doubling back on itself.
                #
                # We can test whether the segments are neighboring by just
                # seeing if there's an edge in the graph directly from one
                # segment to the next.
                #
                # This test is important for the "skip last stitch in each row"
                # feature.
                if graph.has_edge(start_of_run, edge[0]):
                    new_path.append(PathEdge((start_of_run, edge[0]), "outline"))
                else:
                    new_path.append(PathEdge((start_of_run, edge[0]), "collapsed"))

                start_of_run = None

            new_path.append(edge)
        else:
            if not start_of_run:
                start_of_run = edge[0]

    if start_of_run and start_of_run != edge[1]:
        # if we were still in a run, close it off
        new_path.append(PathEdge((start_of_run, edge[1]), "collapsed"))

    return new_path


def travel(shape, travel_graph, edge, running_stitch_length, running_stitch_tolerance, skip_last, underpath, clamp=True):
    """Create stitches to get from one point on an outline of the shape to another."""

    start, end = edge
    try:
        path = networkx.shortest_path(travel_graph, start, end, weight='weight')
    except networkx.NetworkXNoPath:
        # This may not look good, but it prevents the fill from failing (which hopefully never happens)
        path = [start, end]

    if underpath and path != (start, end):
        path = smooth_path(path, 2)
    else:
        path = [InkstitchPoint.from_tuple(point) for point in path]
    if len(path) > 1 and clamp:
        path = clamp_path_to_polygon(path, shape)
    elif not path:
        # This may happen on very small shapes.
        # Simply return nothing as we do not want to error out
        return []

    points = even_running_stitch(path, running_stitch_length, running_stitch_tolerance)
    stitches = [Stitch(point) for point in points]

    for stitch in stitches:
        stitch.add_tag('auto_fill_travel')

    # The path's first stitch will start at the end of a row of stitches.  We
    # don't want to double that last stitch, so we'd like to skip it.
    if skip_last and not edge.is_outline():
        # However, we don't want to skip it if we've had to do any actual
        # travel in the interior of the shape.  The reason is that we can
        # potentially cut a corner and stitch outside the shape.
        #
        # If the path is longer than two nodes, then it is not a simple
        # transition from one row to the next, so we'll keep the stitch.
        return stitches
    else:
        # Just a normal transition from one row to the next, so skip the first
        # stitch.
        return stitches[1:]


@debug.time
def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, angle, row_spacing, max_stitch_length, running_stitch_length,
                     running_stitch_tolerance, staggers, skip_last, underpath, enable_random_stitch_length, random_sigma, random_seed):
    path = collapse_sequential_outline_edges(path, fill_stitch_graph)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for i, edge in enumerate(path):
        if edge.is_segment():
            stitch_row(stitches, edge[0], edge[1], angle, row_spacing, max_stitch_length, staggers, skip_last,
                       enable_random_stitch_length, random_sigma, join_args(random_seed, i))

            # note: gap fill segments won't be in the graph
            if fill_stitch_graph.has_edge(edge[0], edge[1], key='segment'):
                travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(shape, travel_graph, edge, [running_stitch_length], running_stitch_tolerance, skip_last, underpath))

        check_stop_flag()

    return stitches
