from fill import intersect_region_with_grating, row_num, stitch_row
from .. import _, PIXELS_PER_MM, Point as InkstitchPoint
import sys
import shapely
import networkx
import math
from itertools import groupby
from collections import deque


class MaxQueueLengthExceeded(Exception):
    pass


def auto_fill(shape, angle, row_spacing, end_row_spacing, max_stitch_length, running_stitch_length, staggers, starting_point=None):
    stitches = []

    rows_of_segments = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing)
    segments = [segment for row in rows_of_segments for segment in row]

    graph = build_graph(shape, segments, angle, row_spacing)
    path = find_stitch_path(graph, segments)

    if starting_point:
        stitches.extend(connect_points(shape, starting_point, path[0][0], running_stitch_length))

    stitches.extend(path_to_stitches(graph, path, shape, angle, row_spacing, max_stitch_length, running_stitch_length, staggers))

    return stitches


def which_outline(shape, coords):
    """return the index of the outline on which the point resides

    Index 0 is the outer boundary of the fill region.  1+ are the
    outlines of the holes.
    """

    # I'd use an intersection check, but floating point errors make it
    # fail sometimes.

    point = shapely.geometry.Point(*coords)
    outlines = enumerate(list(shape.boundary))
    closest = min(outlines, key=lambda (index, outline): outline.distance(point))

    return closest[0]


def project(shape, coords, outline_index):
    """project the point onto the specified outline

    This returns the distance along the outline at which the point resides.
    """

    outline = list(shape.boundary)[outline_index]
    return outline.project(shapely.geometry.Point(*coords))


def build_graph(shape, segments, angle, row_spacing):
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

    graph = networkx.MultiGraph()

    # First, add the grating segments as edges.  We'll use the coordinates
    # of the endpoints as nodes, which networkx will add automatically.
    for segment in segments:
        # networkx allows us to label nodes with arbitrary data.  We'll
        # mark this one as a grating segment.
        graph.add_edge(*segment, key="segment")

    for node in graph.nodes():
        outline_index = which_outline(shape, node)
        outline_projection = project(shape, node, outline_index)

        # Tag each node with its index and projection.
        graph.add_node(node, index=outline_index, projection=outline_projection)

    nodes = list(graph.nodes(data=True)) # returns a list of tuples: [(node, {data}), (node, {data}) ...]
    nodes.sort(key=lambda node: (node[1]['index'], node[1]['projection']))

    for outline_index, nodes in groupby(nodes, key=lambda node: node[1]['index']):
        nodes = [ node for node, data in nodes ]

        # heuristic: change the order I visit the nodes in the outline if necessary.
        # If the start and endpoints are in the same row, I can't tell which row
        # I should treat it as being in.
        for i in xrange(len(nodes)):
            row0 = row_num(InkstitchPoint(*nodes[0]), angle, row_spacing)
            row1 = row_num(InkstitchPoint(*nodes[1]), angle, row_spacing)

            if row0 == row1:
                nodes = nodes[1:] + [nodes[0]]
            else:
                break

        # heuristic: it's useful to try to keep the duplicated edges in the same rows.
        # this prevents the BFS from having to search a ton of edges.
        min_row_num = min(row0, row1)
        if min_row_num % 2 == 0:
            edge_set = 0
        else:
            edge_set = 1

        #print >> sys.stderr, outline_index, "es", edge_set, "rn", row_num, inkstitch.Point(*nodes[0]) * self.north(angle), inkstitch.Point(*nodes[1]) * self.north(angle)

        # add an edge between each successive node
        for i, (node1, node2) in enumerate(zip(nodes, nodes[1:] + [nodes[0]])):
            graph.add_edge(node1, node2, key="outline")

            # duplicate every other edge around this outline
            if i % 2 == edge_set:
                graph.add_edge(node1, node2, key="extra")


    if not networkx.is_eulerian(graph):
        raise Exception(_("Unable to autofill.  This most often happens because your shape is made up of multiple sections that aren't connected."))

    return graph


def node_list_to_edge_list(node_list):
    return zip(node_list[:-1], node_list[1:])


def bfs_for_loop(graph, starting_node, max_queue_length=2000):
    to_search = deque()
    to_search.appendleft(([starting_node], set(), 0))

    while to_search:
        if len(to_search) > max_queue_length:
            raise MaxQueueLengthExceeded()

        path, visited_edges, visited_segments = to_search.pop()
        ending_node = path[-1]

        # get a list of neighbors paired with the key of the edge I can follow to get there
        neighbors = [
                    (node, key)
                        for node, adj in graph.adj[ending_node].iteritems()
                        for key in adj
                ]

        # heuristic: try grating segments first
        neighbors.sort(key=lambda (dest, key): key == "segment", reverse=True)

        for next_node, key in neighbors:
            # skip if I've already followed this edge
            edge = (tuple(sorted((ending_node, next_node))), key)
            if edge in visited_edges:
                continue

            new_path = path + [next_node]

            if key == "segment":
                new_visited_segments = visited_segments + 1
            else:
                new_visited_segments = visited_segments

            if next_node == starting_node:
                # ignore trivial loops (down and back a doubled edge)
                if len(new_path) > 3:
                    return node_list_to_edge_list(new_path), new_visited_segments

            new_visited_edges = visited_edges.copy()
            new_visited_edges.add(edge)

            to_search.appendleft((new_path, new_visited_edges, new_visited_segments))


def find_loop(graph, starting_nodes):
    """find a loop in the graph that is connected to the existing path

    Start at a candidate node and search through edges to find a path
    back to that node.  We'll use a breadth-first search (BFS) in order to
    find the shortest available loop.

    In most cases, the BFS should not need to search far to find a loop.
    The queue should stay relatively short.

    An added heuristic will be used: if the BFS queue's length becomes
    too long, we'll abort and try a different starting point.  Due to
    the way we've set up the graph, there's bound to be a better choice
    somewhere else.
    """

    #loop = self.simple_loop(graph, starting_nodes[-2])

    #if loop:
    #    print >> sys.stderr, "simple_loop success"
    #    starting_nodes.pop()
    #    starting_nodes.pop()
    #    return loop

    loop = None
    retry = []
    max_queue_length = 2000

    while not loop:
        while not loop and starting_nodes:
            starting_node = starting_nodes.pop()
            #print >> sys.stderr, "find loop from", starting_node

            try:
                # Note: if bfs_for_loop() returns None, no loop can be
                # constructed from the starting_node (because the
                # necessary edges have already been consumed).  In that
                # case we discard that node and try the next.
                loop = bfs_for_loop(graph, starting_node, max_queue_length)

                #if not loop:
                    #print >> dbg, "failed on", starting_node
                    #dbg.flush()
            except MaxQueueLengthExceeded:
                #print >> dbg, "gave up on", starting_node
                #dbg.flush()
                # We're giving up on this node for now.  We could try
                # this node again later, so add it to the bottm of the
                # stack.
                retry.append(starting_node)

        # Darn, couldn't find a loop.  Try harder.
        starting_nodes.extendleft(retry)
        max_queue_length *= 2

    starting_nodes.extendleft(retry)
    return loop


def insert_loop(path, loop):
    """insert a sub-loop into an existing path

    The path will be a series of edges describing a path through the graph
    that ends where it starts.  The loop will be similar, and its starting
    point will be somewhere along the path.

    Insert the loop into the path, resulting in a longer path.

    Both the path and the loop will be a list of edges specified as a
    start and end point.  The points will be specified in order, such
    that they will look like this:

    ((p1, p2), (p2, p3), (p3, p4) ... (pn, p1))

    path will be modified in place.
    """

    loop_start = loop[0][0]

    for i, (start, end) in enumerate(path):
        if start == loop_start:
            break

    path[i:i] = loop


def find_stitch_path(graph, segments):
    """find a path that visits every grating segment exactly once

    Theoretically, we just need to find an Eulerian Path in the graph.
    However, we don't actually care whether every single edge is visited.
    The edges on the outline of the region are only there to help us get
    from one grating segment to the next.

    We'll build a "cycle" (a path that ends where it starts) using
    Hierholzer's algorithm.  We'll stop once we've visited every grating
    segment.

    Hierholzer's algorithm says to select an arbitrary starting node at
    each step.  In order to produce a reasonable stitch path, we'll select
    the vertex carefully such that we get back-and-forth traversal like
    mowing a lawn.

    To do this, we'll use a simple heuristic: try to start from nodes in
    the order of most-recently-visited first.
    """

    original_graph = graph
    graph = graph.copy()
    num_segments = len(segments)
    segments_visited = 0
    nodes_visited = deque()

    # start with a simple loop: down one segment and then back along the
    # outer border to the starting point.
    path = [segments[0], list(reversed(segments[0]))]

    graph.remove_edges_from(path)

    segments_visited += 1
    nodes_visited.extend(segments[0])

    while segments_visited < num_segments:
        result = find_loop(graph, nodes_visited)

        if not result:
            print >> sys.stderr, _("Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.")
            break

        loop, segments = result

        #print >> dbg, "found loop:", loop
        #dbg.flush()

        segments_visited += segments
        nodes_visited += [edge[0] for edge in loop]
        graph.remove_edges_from(loop)

        insert_loop(path, loop)

        #if segments_visited >= 12:
        #    break

    # Now we have a loop that covers every grating segment.  It returns to
    # where it started, which is unnecessary, so we'll snip the last bit off.
    #while original_graph.has_edge(*path[-1], key="outline"):
    #    path.pop()

    return path


def collapse_sequential_outline_edges(graph, path):
    """collapse sequential edges that fall on the same outline

    When the path follows multiple edges along the outline of the region,
    replace those edges with the starting and ending points.  We'll use
    these to stitch along the outline later on.
    """

    start_of_run = None
    new_path = []

    for edge in path:
        if graph.has_edge(*edge, key="segment"):
            if start_of_run:
                # close off the last run
                new_path.append((start_of_run, edge[0]))
                start_of_run = None

            new_path.append(edge)
        else:
            if not start_of_run:
                start_of_run = edge[0]

    if start_of_run:
        # if we were still in a run, close it off
        new_path.append((start_of_run, edge[1]))

    return new_path


def outline_distance(outline, p1, p2):
    # how far around the outline (and in what direction) do I need to go
    # to get from p1 to p2?

    p1_projection = outline.project(shapely.geometry.Point(p1))
    p2_projection = outline.project(shapely.geometry.Point(p2))

    distance = p2_projection - p1_projection

    if abs(distance) > outline.length / 2.0:
        # if we'd have to go more than halfway around, it's faster to go
        # the other way
        if distance < 0:
            return distance + outline.length
        elif distance > 0:
            return distance - outline.length
        else:
            # this ought not happen, but just for completeness, return 0 if
            # p1 and p0 are the same point
            return 0
    else:
        return distance


def connect_points(shape, start, end, running_stitch_length):
    outline_index = which_outline(shape, start)
    outline = shape.boundary[outline_index]

    pos = outline.project(shapely.geometry.Point(start))
    distance = outline_distance(outline, start, end)
    num_stitches = abs(int(distance / running_stitch_length))

    direction = math.copysign(1.0, distance)
    one_stitch = running_stitch_length * direction

    #print >> dbg, "connect_points:", outline_index, start, end, distance, stitches, direction
    #dbg.flush()

    stitches = [InkstitchPoint(*outline.interpolate(pos).coords[0])]

    for i in xrange(num_stitches):
        pos = (pos + one_stitch) % outline.length

        stitches.append(InkstitchPoint(*outline.interpolate(pos).coords[0]))

    end = InkstitchPoint(*end)
    if (end - stitches[-1]).length() > 0.1 * PIXELS_PER_MM:
        stitches.append(end)

    #print >> dbg, "end connect_points"
    #dbg.flush()

    return stitches


def path_to_stitches(graph, path, shape, angle, row_spacing, max_stitch_length, running_stitch_length, staggers):
    path = collapse_sequential_outline_edges(graph, path)

    stitches = []

    for edge in path:
        if graph.has_edge(*edge, key="segment"):
            stitch_row(stitches, edge[0], edge[1], angle, row_spacing, max_stitch_length, staggers)
        else:
            stitches.extend(connect_points(shape, edge[0], edge[1], running_stitch_length))

    return stitches
