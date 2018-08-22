import sys
import shapely
import networkx
from itertools import groupby, izip
from collections import deque

from .fill import intersect_region_with_grating, row_num, stitch_row
from .running_stitch import running_stitch
from ..i18n import _
from ..utils.geometry import Point as InkstitchPoint, cut


class MaxQueueLengthExceeded(Exception):
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


def auto_fill(shape, angle, row_spacing, end_row_spacing, max_stitch_length, running_stitch_length, staggers, starting_point, ending_point=None):
    stitches = []

    rows_of_segments = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing)
    segments = [segment for row in rows_of_segments for segment in row]

    graph = build_graph(shape, segments, angle, row_spacing)
    path = find_stitch_path(graph, segments, starting_point, ending_point)

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
    closest = min(outlines, key=lambda index_outline: index_outline[1].distance(point))

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

    nodes = list(graph.nodes(data=True))  # returns a list of tuples: [(node, {data}), (node, {data}) ...]
    nodes.sort(key=lambda node: (node[1]['index'], node[1]['projection']))

    for outline_index, nodes in groupby(nodes, key=lambda node: node[1]['index']):
        nodes = [node for node, data in nodes]

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
    to_search.append((None, set()))

    while to_search:
        if len(to_search) > max_queue_length:
            raise MaxQueueLengthExceeded()

        path, visited_edges = to_search.pop()

        if path is None:
            # This is the very first time through the loop, so initialize.
            path = []
            ending_node = starting_node
        else:
            ending_node = path[-1][-1]

        # get a list of neighbors paired with the key of the edge I can follow to get there
        neighbors = [
            (node, key)
            for node, adj in graph.adj[ending_node].iteritems()
            for key in adj
        ]

        # heuristic: try grating segments first
        neighbors.sort(key=lambda dest_key: dest_key[1] == "segment", reverse=True)

        for next_node, key in neighbors:
            # skip if I've already followed this edge
            edge = PathEdge((ending_node, next_node), key)
            if edge in visited_edges:
                continue

            new_path = path + [edge]

            if next_node == starting_node:
                # ignore trivial loops (down and back a doubled edge)
                if len(new_path) > 3:
                    return new_path

            new_visited_edges = visited_edges.copy()
            new_visited_edges.add(edge)

            to_search.appendleft((new_path, new_visited_edges))


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

    loop = None
    retry = []
    max_queue_length = 2000

    while not loop:
        while not loop and starting_nodes:
            starting_node = starting_nodes.pop()

            try:
                # Note: if bfs_for_loop() returns None, no loop can be
                # constructed from the starting_node (because the
                # necessary edges have already been consumed).  In that
                # case we discard that node and try the next.
                loop = bfs_for_loop(graph, starting_node, max_queue_length)

            except MaxQueueLengthExceeded:
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

    ((p1, p2), (p2, p3), (p3, p4), ...)

    path will be modified in place.
    """

    loop_start = loop[0][0]

    for i, (start, end) in enumerate(path):
        if start == loop_start:
            break
    else:
        # if we didn't find the start of the loop in the list at all, it must
        # be the endpoint of the last segment
        i += 1

    path[i:i] = loop


def nearest_node_on_outline(graph, point, outline_index=0):
    point = shapely.geometry.Point(*point)
    outline_nodes = [node for node, data in graph.nodes(data=True) if data['index'] == outline_index]
    nearest = min(outline_nodes, key=lambda node: shapely.geometry.Point(*node).distance(point))

    return nearest


def get_outline_nodes(graph, outline_index=0):
    outline_nodes = [(node, data['projection'])
                     for node, data
                     in graph.nodes(data=True)
                     if data['index'] == outline_index]
    outline_nodes.sort(key=lambda node_projection: node_projection[1])
    outline_nodes = [node for node, data in outline_nodes]

    return outline_nodes


def find_initial_path(graph, starting_point, ending_point=None):
    starting_node = nearest_node_on_outline(graph, starting_point)

    if ending_point is None:
        # If they didn't give an ending point, pick either neighboring node
        # along the outline -- doesn't matter which.  We do this because
        # the algorithm requires we start with _some_ path.
        neighbors = [n for n, keys in graph.adj[starting_node].iteritems() if 'outline' in keys]
        return [PathEdge((starting_node, neighbors[0]), "initial")]
    else:
        ending_node = nearest_node_on_outline(graph, ending_point)
        outline_nodes = get_outline_nodes(graph)

        # Multiply the outline_nodes list by 2 (duplicate it) because
        # the ending_node may occur first.
        outline_nodes *= 2
        start_index = outline_nodes.index(starting_node)
        end_index = outline_nodes.index(ending_node, start_index)
        nodes = outline_nodes[start_index:end_index + 1]

        # we have a series of sequential points, but we need to
        # turn it into an edge list
        path = []
        for start, end in izip(nodes[:-1], nodes[1:]):
            path.append(PathEdge((start, end), "initial"))

        return path


def find_stitch_path(graph, segments, starting_point=None, ending_point=None):
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
    num_segments = len(segments)
    segments_visited = 0
    nodes_visited = deque()

    if starting_point is None:
        starting_point = segments[0][0]

    path = find_initial_path(graph, starting_point, ending_point)

    # Our graph is Eulerian: every node has an even degree.  An Eulerian graph
    # must have an Eulerian Circuit which visits every edge and ends where it
    # starts.
    #
    # However, we're starting with a path and _not_ removing the edges of that
    # path from the graph.  By doing this, we're implicitly adding those edges
    # to the graph, after which the starting and ending point (and only those
    # two) will now have odd degree.  A graph that's Eulerian except for two
    # nodes must have an Eulerian Path that starts and ends at those two nodes.
    # That's how we force the starting and ending point.

    nodes_visited.append(path[0][0])

    while segments_visited < num_segments:
        loop = find_loop(graph, nodes_visited)

        if not loop:
            print >> sys.stderr, _("Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.")
            break

        segments_visited += sum(1 for edge in loop if edge.is_segment())
        nodes_visited.extend(edge[0] for edge in loop)
        graph.remove_edges_from(loop)

        insert_loop(path, loop)

    if ending_point is None:
        # If they didn't specify an ending point, then the end of the path travels
        # around the outline back to the start (see find_initial_path()). This
        # isn't necessary, so remove it.
        trim_end(path)

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


def connect_points(shape, start, end, running_stitch_length, row_spacing):
    """Create stitches to get from one point on an outline of the shape to another.

    An outline is essentially a loop (a path of points that ends where it starts).
    Given point A and B on that loop, we want to take the shortest path from one
    to the other.  Due to the way our path-finding algorithm above works, it may
    have had to take the long way around the shape to get from A to B, but we'd
    rather ignore that and just get there the short way.
    """

    # We may be on the outer boundary or on on of the hole boundaries.
    outline_index = which_outline(shape, start)
    outline = shape.boundary[outline_index]

    # First, figure out the start and end position along the outline.  The
    # projection gives us the distance travelled down the outline to get to
    # that point.
    start = shapely.geometry.Point(start)
    start_projection = outline.project(start)
    end = shapely.geometry.Point(end)
    end_projection = outline.project(end)

    # If the points are pretty close, just jump there.  There's a slight
    # risk that we're going to sew outside the shape here.  The way to
    # avoid that is to use running_stitch() even for these really short
    # connections, but that would be really slow for all of the
    # connections from one row to the next.
    #
    # This seems to do a good job of avoiding going outside the shape in
    # most cases.  1.4 is chosen as approximately the length of the
    # stitch connecting two rows if the side of the shape is at a 45
    # degree angle to the rows of stitches (sqrt(2)).
    if abs(end_projection - start_projection) < row_spacing * 1.4:
        return [InkstitchPoint(end.x, end.y)]

    # The outline path has a "natural" starting point.  Think of this as
    # 0 or 12 on an analog clock.

    # Cut the outline into two paths at the starting point.  The first
    # section will go from 12 o'clock to the starting point.  The second
    # section will go from the starting point all the way around and end
    # up at 12 again.
    result = cut(outline, start_projection)

    # result will be None if our starting point happens to already be at
    # 12 o'clock.
    if result is not None and result[1] is not None:
        before, after = result

        # Make a new outline, starting from the starting point.  This is
        # like rotating the clock so that now our starting point is
        # at 12 o'clock.
        outline = shapely.geometry.LineString(list(after.coords) + list(before.coords))

    # Now figure out where our ending point is on the newly-rotated clock.
    end_projection = outline.project(end)

    # Cut the new path at the ending point.  before and after now represent
    # two ways to get from the starting point to the ending point.  One
    # will most likely be longer than the other.
    before, after = cut(outline, end_projection)

    if before.length <= after.length:
        points = list(before.coords)
    else:
        # after goes from the ending point to the starting point, so reverse
        # it to get from start to end.
        points = list(reversed(after.coords))

    # Now do running stitch along the path we've found.  running_stitch() will
    # avoid cutting sharp corners.
    path = [InkstitchPoint(*p) for p in points]
    return running_stitch(path, running_stitch_length)


def trim_end(path):
    while path and path[-1].is_outline():
        path.pop()


def path_to_stitches(graph, path, shape, angle, row_spacing, max_stitch_length, running_stitch_length, staggers):
    path = collapse_sequential_outline_edges(graph, path)

    stitches = []

    for edge in path:
        if edge.is_segment():
            stitch_row(stitches, edge[0], edge[1], angle, row_spacing, max_stitch_length, staggers)
        else:
            stitches.extend(connect_points(shape, edge[0], edge[1], running_stitch_length, row_spacing))

    return stitches
