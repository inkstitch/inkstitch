# -*- coding: UTF-8 -*-

from itertools import groupby, chain
import math

import networkx
from shapely import geometry as shgeo
from shapely.strtree import STRtree

from ..exceptions import InkstitchException
from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..utils.geometry import Point as InkstitchPoint
from .fill import intersect_region_with_grating, stitch_row
from .running_stitch import running_stitch


class InvalidPath(InkstitchException):
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

    def __eq__(self, other):
        return self._sorted_nodes == other._sorted_nodes and self.key == other.key

    def is_outline(self):
        return self.key in self.OUTLINE_KEYS

    def is_segment(self):
        return self.key == self.SEGMENT_KEY


def auto_fill(shape,
              angle,
              row_spacing,
              end_row_spacing,
              max_stitch_length,
              running_stitch_length,
              staggers,
              skip_last,
              starting_point,
              ending_point=None,
              underpath=True):

    fill_stitch_graph = build_fill_stitch_graph(shape, angle, row_spacing, end_row_spacing)
    check_graph(fill_stitch_graph, shape, max_stitch_length)
    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(path, travel_graph, fill_stitch_graph, angle, row_spacing,
                              max_stitch_length, running_stitch_length, staggers, skip_last)

    return result


def which_outline(shape, coords):
    """return the index of the outline on which the point resides

    Index 0 is the outer boundary of the fill region.  1+ are the
    outlines of the holes.
    """

    # I'd use an intersection check, but floating point errors make it
    # fail sometimes.

    point = shgeo.Point(*coords)
    outlines = list(shape.boundary)
    outline_indices = range(len(outlines))
    closest = min(outline_indices, key=lambda index: outlines[index].distance(point))

    return closest


def project(shape, coords, outline_index):
    """project the point onto the specified outline

    This returns the distance along the outline at which the point resides.
    """

    outline = list(shape.boundary)[outline_index]
    return outline.project(shgeo.Point(*coords))


def build_fill_stitch_graph(shape, angle, row_spacing, end_row_spacing):
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

    # Convert the shape into a set of parallel line segments.
    rows_of_segments = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing)
    segments = [segment for row in rows_of_segments for segment in row]

    graph = networkx.MultiGraph()

    # First, add the grating segments as edges.  We'll use the coordinates
    # of the endpoints as nodes, which networkx will add automatically.
    for segment in segments:
        # networkx allows us to label nodes with arbitrary data.  We'll
        # mark this one as a grating segment.
        graph.add_edge(*segment, key="segment", underpath_edges=[])

    tag_nodes_with_outline_and_projection(graph, shape, graph.nodes())

    for node in graph.nodes():
        outline_index = which_outline(shape, node)
        outline_projection = project(shape, node, outline_index)

        # Tag each node with its index and projection.
        graph.add_node(node, index=outline_index, projection=outline_projection)

    add_edges_between_outline_nodes(graph, key="outline")

    for node1, node2, key, data in graph.edges(keys=True, data=True):
        if key == "outline":
            # duplicate every other edge
            if data['index'] % 2 == 0:
                graph.add_edge(node1, node2, key="extra")

    return graph


def tag_nodes_with_outline_and_projection(graph, shape, nodes):
    for node in nodes:
        outline_index = which_outline(shape, node)
        outline_projection = project(shape, node, outline_index)

        graph.add_node(node, outline=outline_index, projection=outline_projection)


def add_edges_between_outline_nodes(graph, key=None):
    """Add edges around the outlines of the graph, connecting sequential nodes.

    This function assumes that all nodes in the graph are on the outline of the
    shape.  It figures out which nodes are next to each other on the shape and
    connects them in the graph with an edge.

    Edges are tagged with their outline number and their position on that
    outline.
    """

    nodes = list(graph.nodes(data=True))  # returns a list of tuples: [(node, {data}), (node, {data}) ...]
    nodes.sort(key=lambda node: (node[1]['outline'], node[1]['projection']))

    for outline_index, nodes in groupby(nodes, key=lambda node: node[1]['outline']):
        nodes = [node for node, data in nodes]

        # add an edge between each successive node
        for i, (node1, node2) in enumerate(zip(nodes, nodes[1:] + [nodes[0]])):
            data = dict(outline=outline_index, index=i)
            if key:
                graph.add_edge(node1, node2, key=key, **data)
            else:
                graph.add_edge(node1, node2, **data)


def build_travel_graph(fill_stitch_graph, shape, fill_stitch_angle, underpath):
    """Build a graph for travel stitches.

    This graph will be used to find a stitch path between two spots on the
    outline of the shape.

    If underpath is False, we'll just be traveling
    around the outline of the shape, so the graph will only contain outline
    edges.

    If underpath is True, we'll also allow travel inside the shape.  We'll
    fill the shape with a cross-hatched grid of lines 2mm apart, at ±45
    degrees from the fill stitch angle.  This will ensure that travel stitches
    won't be visible and won't disrupt the fill stitch.

    When underpathing, we "encourage" the travel() function to travel inside
    the shape rather than on the boundary.  We do this by weighting the
    boundary edges extra so that they're more "expensive" in the shortest path
    calculation.
    """

    graph = networkx.Graph()

    # Add all the nodes from the main graph.  This will be all of the endpoints
    # of the rows of stitches.  Every node will be on the outline of the shape.
    # They'll all already have their `outline` and `projection` tags set.
    graph.add_nodes_from(fill_stitch_graph.nodes(data=True))

    if underpath:
        # These two MultiLineStrings will make up the cross-hatched grid.
        grating1 = shgeo.MultiLineString(list(chain(*intersect_region_with_grating(shape, fill_stitch_angle + math.pi / 4, 2 * PIXELS_PER_MM))))
        grating2 = shgeo.MultiLineString(list(chain(*intersect_region_with_grating(shape, fill_stitch_angle - math.pi / 4, 2 * PIXELS_PER_MM))))

        # We'll add the endpoints of the crosshatch grating lines too  These
        # will all be on the outline of the shape.  This will ensure that a
        # path traveling inside the shape can reach its target on the outline,
        # which will be one of the points added above.
        endpoints = [coord for mls in (grating1, grating2)
                     for ls in mls
                     for coord in ls.coords]
        tag_nodes_with_outline_and_projection(graph, shape, endpoints)

    add_edges_between_outline_nodes(graph)
    for start, end in graph.edges:
        p1 = InkstitchPoint(*start)
        p2 = InkstitchPoint(*end)

        # Set the weight equal to triple the edge length, to encourage travel()
        # to avoid them when underpathing is enabled.
        graph.add_edge(start, end, weight=3 * p1.distance(p2))

    if underpath:
        segments = []
        for start, end, key, data in fill_stitch_graph.edges(keys=True, data=True):
            if key == 'segment':
                segments.append(shgeo.LineString((start, end)))

        # The shapely documentation is pretty unclear on this.  An STRtree
        # allows for building a set of shapes and then efficiently testing
        # the set for intersection.  This allows us to do blazing-fast
        # queries of which line segments overlap each underpath edge.
        rtree = STRtree(segments)

        interior_edges = grating1.symmetric_difference(grating2)
        for ls in interior_edges.geoms:
            p1, p2 = [InkstitchPoint(*coord) for coord in ls.coords]
            edge = (p1.as_tuple(), p2.as_tuple())

            for segment in rtree.query(ls):
                start, end = segment.coords
                fill_stitch_graph[start][end]['segment']['underpath_edges'].append(edge)

            graph.add_edge(*edge, weight=p1.distance(p2))

        # otherwise we sometimes get exceptions like this:
        # Exception AttributeError: "'NoneType' object has no attribute 'GEOSSTRtree_destroy'" in
        #   <bound method STRtree.__del__ of <shapely.strtree.STRtree instance at 0x0D2BFD50>> ignored
        del rtree

    return graph


def check_graph(graph, shape, max_stitch_length):
    if networkx.is_empty(graph) or not networkx.is_eulerian(graph):
        if shape.area < max_stitch_length ** 2:
            raise InvalidPath(_("This shape is so small that it cannot be filled with rows of stitches.  "
                                "It would probably look best as a satin column or running stitch."))
        else:
            raise InvalidPath(_("Cannot parse shape.  "
                                "This most often happens because your shape is made up of multiple sections that aren't connected."))


def nearest_node(graph, point):
    point = shgeo.Point(*point)
    nearest = min(graph.nodes, key=lambda node: shgeo.Point(*node).distance(point))

    return nearest


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

    if starting_point is None:
        starting_point = graph.nodes.keys()[0]

    starting_node = nearest_node(graph, starting_point)

    if ending_point is None:
        ending_point = starting_point
        ending_node = starting_node
    else:
        ending_node = nearest_node(graph, ending_point)

    # The algorithm below is adapted from networkx.eulerian_circuit().
    path = []
    vertex_stack = [(ending_node, None)]
    last_vertex = None
    last_key = None

    while vertex_stack:
        current_vertex, current_key = vertex_stack[-1]
        if graph.degree(current_vertex) == 0:
            if last_vertex is not None:
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

    real_end = nearest_node(travel_graph, ending_point)
    path.append(PathEdge((ending_node, real_end), key="outline"))

    return path


def pick_edge(edges):
    """Pick the next edge to traverse in the pathfinding algorithm"""

    # Prefer a segment if one is available.  This has the effect of
    # creating long sections of back-and-forth row traversal.
    for source, node, key in edges:
        if key == 'segment':
            return source, node, key

    return list(edges)[0]


def collapse_sequential_outline_edges(path):
    """collapse sequential edges that fall on the same outline

    When the path follows multiple edges along the outline of the region,
    replace those edges with the starting and ending points.  We'll use
    these to stitch along the outline later on.
    """

    start_of_run = None
    new_path = []

    for edge in path:
        if edge.is_segment():
            if start_of_run:
                # close off the last run
                new_path.append(PathEdge((start_of_run, edge[0]), "collapsed"))
                start_of_run = None

            new_path.append(edge)
        else:
            if not start_of_run:
                start_of_run = edge[0]

    if start_of_run:
        # if we were still in a run, close it off
        new_path.append(PathEdge((start_of_run, edge[1]), "collapsed"))

    return new_path


def travel(travel_graph, start, end, running_stitch_length, skip_last):
    """Create stitches to get from one point on an outline of the shape to another."""

    path = networkx.shortest_path(travel_graph, start, end, weight='weight')
    path = [InkstitchPoint(*p) for p in path]
    stitches = running_stitch(path, running_stitch_length)

    # The path's first stitch will start at the end of a row of stitches.  We
    # don't want to double that last stitch, so we'd like to skip it.
    if skip_last and len(path) > 2:
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


def path_to_stitches(path, travel_graph, fill_stitch_graph, angle, row_spacing, max_stitch_length, running_stitch_length, staggers, skip_last):
    path = collapse_sequential_outline_edges(path)

    stitches = []

    for edge in path:
        if edge.is_segment():
            stitch_row(stitches, edge[0], edge[1], angle, row_spacing, max_stitch_length, staggers, skip_last)
            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(travel_graph, edge[0], edge[1], running_stitch_length, skip_last))

    return stitches
