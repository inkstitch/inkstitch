# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

import math
from itertools import chain, groupby
import warnings

import networkx
from shapely import geometry as shgeo
from shapely.ops import snap
from shapely.strtree import STRtree

from ..debug import debug
from ..stitch_plan import Stitch
from ..svg import PIXELS_PER_MM
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import Point as InkstitchPoint, line_string_to_point_list, ensure_multi_line_string
from .fill import intersect_region_with_grating, stitch_row
from .running_stitch import running_stitch
from ..utils.smoothing import smooth_path
from ..utils.threading import check_stop_flag


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

    def is_outline(self):
        return self.key in self.OUTLINE_KEYS

    def is_segment(self):
        return self.key == self.SEGMENT_KEY


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
              underpath=True):
    rows = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing)
    if not rows:
        # Small shapes may not intersect with the grating at all.
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    segments = [segment for row in rows for segment in row]
    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if not graph_is_valid(fill_stitch_graph, shape, max_stitch_length):
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)

    if not travel_graph:
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(shape, path, travel_graph, fill_stitch_graph, angle, row_spacing,
                              max_stitch_length, running_stitch_length, running_stitch_tolerance,
                              staggers, skip_last, underpath)

    return result


def which_outline(shape, coords):
    """return the index of the outline on which the point resides

    Index 0 is the outer boundary of the fill region.  1+ are the
    outlines of the holes.
    """

    # I'd use an intersection check, but floating point errors make it
    # fail sometimes.

    point = shgeo.Point(*coords)
    outlines = ensure_multi_line_string(shape.boundary).geoms
    outline_indices = list(range(len(outlines)))
    closest = min(outline_indices,
                  key=lambda index: outlines[index].distance(point))

    return closest


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
        if key == "outline":
            edges.append(((start, end), data))

    edge, data = min(edges, key=lambda edge_data: shgeo.LineString(edge_data[0]).distance(projected_point))

    graph.remove_edge(*edge, key="outline")
    graph.add_edge(edge[0], node, key="outline", **data)
    graph.add_edge(node, edge[1], key="outline", **data)
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


def graph_is_valid(graph, shape, max_stitch_length):
    # The graph may be empty if the shape is so small that it fits between the
    # rows of stitching.  Certain small weird shapes can also cause a non-
    # eulerian graph.
    return not networkx.is_empty(graph) and networkx.is_eulerian(graph)


def fallback(shape, running_stitch_length, running_stitch_tolerance):
    """Generate stitches when the auto-fill algorithm fails.

    If graph_is_valid() returns False, we're not going to be able to run the
    auto-fill algorithm.  Instead, we'll just do running stitch around the
    outside of the shape.  In all likelihood, the shape is so small it won't
    matter.
    """

    boundary = ensure_multi_line_string(shape.boundary)
    outline = boundary.geoms[0]

    return running_stitch(line_string_to_point_list(outline), running_stitch_length, running_stitch_tolerance)


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

    if underpath:
        try:
            boundary_points, travel_edges = build_travel_edges(shape, fill_stitch_angle)
        except NoGratingsError:
            return

        # This will ensure that a path traveling inside the shape can reach its
        # target on the outline, which will be one of the points added above.
        tag_nodes_with_outline_and_projection(graph, shape, boundary_points)
    else:
        add_boundary_travel_nodes(graph, shape)

    add_edges_between_outline_nodes(graph)

    if underpath:
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
        if key == 'segment':
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
    with warnings.catch_warnings():
        # We know about this upcoming change and we don't want to bother users.
        warnings.filterwarnings('ignore', 'STRtree will be changed in 2.0.0 and will not be compatible with versions < 2.')
        strtree = STRtree(segments)

    # This makes the distance calculations below a bit faster.  We're
    # not looking for high precision anyway.
    outline = shape.boundary.simplify(0.5 * PIXELS_PER_MM, preserve_topology=False)

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
def find_stitch_path(graph, travel_graph, starting_point=None, ending_point=None):
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

    if starting_node is not ending_node:
        path.insert(0, PathEdge((starting_node, ending_node), key="initial"))

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
        if key == 'segment':
            return source, node, key

    return list(edges)[0]


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


def travel(shape, travel_graph, edge, running_stitch_length, running_stitch_tolerance, skip_last, underpath):
    """Create stitches to get from one point on an outline of the shape to another."""

    start, end = edge
    path = networkx.shortest_path(travel_graph, start, end, weight='weight')
    if underpath and path != (start, end):
        path = smooth_path(path, 2)
    else:
        path = [InkstitchPoint.from_tuple(point) for point in path]
    path = clamp_path_to_polygon(path, shape)

    points = running_stitch(path, running_stitch_length, running_stitch_tolerance)
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
                     running_stitch_tolerance, staggers, skip_last, underpath):
    path = collapse_sequential_outline_edges(path, fill_stitch_graph)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for edge in path:
        if edge.is_segment():
            stitch_row(stitches, edge[0], edge[1], angle, row_spacing, max_stitch_length, staggers, skip_last)
            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(shape, travel_graph, edge, running_stitch_length, running_stitch_tolerance, skip_last, underpath))

        check_stop_flag()

    return stitches
