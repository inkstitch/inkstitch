import math
import networkx as nx
from shapely import geometry as shgeo
from shapely.geometry import Point as ShapelyPoint
from itertools import chain
import inkex
import cubicsuperpath
import simplestyle

from ..elements import Stroke
from ..utils import Point as InkstitchPoint, cut, cache
from ..svg import PIXELS_PER_MM, line_strings_to_csp
from ..svg.tags import SVG_PATH_TAG


class SatinSegment(object):
    """A portion of SatinColumn.

    Attributes:
        satin -- the SatinColumn instance
        start -- how far along the satin this graph edge starts (a float from 0.0 to 1.0)
        end -- how far along the satin this graph edge ends (a float from 0.0 to 1.0)
        reverse -- if True, reverse the direction of the satin
    """

    def __init__(self, satin, start=0.0, end=1.0, reverse=False):
        """Initialize a SatinEdge.

        Arguments:
            satin -- the SatinColumn instance
            start, end -- a tuple or Point falling somewhere on the
                          satin column, OR a floating point specifying a
                          normalized projection of a distance along the satin
                          (0.0 to 1.0 inclusive)
            reverse -- boolean
        """

        self.satin = satin
        self.reverse = reverse

        # start and end are stored as normalized projections
        self.start = self._parse_init_param(start)
        self.end = self._parse_init_param(end)

        if self.start > self.end:
            self.end, self.start = self.start, self.end
            self.reverse = True

    def _parse_init_param(self, param):
        if isinstance(param, (float, int)):
            return param
        elif isinstance(param, (tuple, InkstitchPoint, ShapelyPoint)):
            return self.satin.center.project(ShapelyPoint(param), normalized=True)

    def to_satin(self):
        satin = self.satin

        if self.start > 0.0:
            before, satin = satin.split(self.start)

        if self.end < 1.0:
            satin, after = satin.split((self.end - self.start) / (1.0 - self.start))

        if self.reverse:
            satin = satin.reverse()

        satin = satin.apply_transform()

        return satin

    to_element = to_satin

    def to_running_stitch(self):
        return RunningStitch(self.center_line, self.satin.node.get('style'))

    def break_up(self, segment_size):
        """Break this SatinSegment up into SatinSegments of the specified size."""

        num_segments = int(math.ceil(self.center_line.length / segment_size))
        segments = []
        satin = self.to_satin()
        for i in xrange(num_segments):
            segments.append(SatinSegment(satin, float(i) / num_segments, float(i + 1) / num_segments, self.reverse))

        if self.reverse:
            segments.reverse()

        return segments

    def reversed(self):
        """Return a copy of this SatinSegment in the opposite direction."""
        return SatinSegment(self.satin, self.start, self.end, not self.reverse)

    @property
    def center_line(self):
        center_line = self.satin.center_line

        if self.start < 1.0:
            before, center_line = cut(center_line, self.start, normalized=True)

        if self.end > 0.0:
            center_line, after = cut(center_line, (self.end - self.start) / (1.0 - self.start), normalized=True)

        if self.reverse:
            center_line = shgeo.LineString(reversed(center_line.coords))

        return center_line

    @property
    @cache
    def start_point(self):
        return self.satin.center_line.interpolate(self.start, normalized=True)

    @property
    @cache
    def end_point(self):
        return self.satin.center_line.interpolate(self.end, normalized=True)

    def is_sequential(self, other):
        """Check if a satin segment immediately follows this one on the same satin."""

        if not isinstance(other, SatinSegment):
            return False

        if self.satin is not other.satin:
            return False

        if self.reverse != other.reverse:
            return False

        if self.reverse:
            return self.start == other.end
        else:
            return self.end == other.start

    def __add__(self, other):
        """Combine two sequential SatinSegments.

        If self.is_sequential(other) is not True then adding results in
        undefined behavior.
        """
        if self.reverse:
            return SatinSegment(self.satin, other.start, self.end, reverse=True)
        else:
            return SatinSegment(self.satin, self.start, other.end)

    def __eq__(self, other):
        # Two SatinSegments are equal if they refer to the same section of the same
        # satin (even if in opposite directions).
        return self.satin is other.satin and self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((id(self.satin), self.start, self.end))

    def __repr__(self):
        return "SatinSegment(%s, %s, %s, %s)" % (self.satin, self.start, self.end, self.reverse)


class JumpStitch(object):
    """A jump stitch between two points."""

    def __init__(self, start, end):
        """Initialize a JumpStitch.

        Arguments:
            start, end -- instances of shgeo.Point
        """

        self.start = start
        self.end = end

    def is_sequential(self, other):
        # Don't bother joining jump stitches.
        return False

    @property
    @cache
    def length(self):
        return self.start.distance(self.end)


class RunningStitch(object):
    """Running stitch along a path."""

    def __init__(self, path, style):
        self.path = path
        self.style = style

    def to_element(self):
        node = inkex.etree.Element(SVG_PATH_TAG)
        node.set("d", cubicsuperpath.formatPath(line_strings_to_csp([self.path])))

        style = simplestyle.parseStyle(self.style)
        style['stroke-dasharray'] = "0.5,0.5"
        style = simplestyle.formatStyle(style)

        node.set("style", style)

        return Stroke(node)

    def is_sequential(self, other):
        if not isinstance(other, RunningStitch):
            return False

        return self.path.distance(other.path) < 0.5

    def __add__(self, other):
        new_path = shgeo.LineString(chain(self.path.coords, other.path.coords))
        return RunningStitch(new_path, self.style)


def auto_satin(satins, starting_point=None, ending_point=None):
    """Find an optimal order to stitch a list of SatinColumns.

    Add running stitch and jump stitches as necessary to construct a stitch
    order.  Cut satins as necessary to minimize jump stitch length.

    For example, consider three satins making up the letters "PO":

        * one vertical satin for the "P"
        * the loop of the "P"
        * the "O"

    A good stitch path would be:

      1. up the leg
      2. down through half of the loop
      3. running stitch to the bottom of the loop
      4. satin stitch back up to the middle of the loop
      5. jump to the closest point on the O
      6. satin stitch around the O

    If passed, stitching will start from starting_point and end at
    ending_point.  It is expected that the starting and ending points will
    fall on satin columns in the list.  If they don't, the nearest
    point on a satin column in the list will be used.

    Returns: a list of SVG path nodes making up the selected stitch order.
      Jumps between objects are implied if they are not right next to each
      other.
    """

    graph = build_graph(satins)
    add_jumps(graph)
    starting_node, ending_node = get_starting_and_ending_nodes(graph, starting_point, ending_point)
    path = find_path(graph, starting_node, ending_node)
    operations = path_to_operations(graph, path)
    operations = collapse_sequential_segments(operations)
    return operations_to_elements_and_trims(operations)


def build_graph(satins):
    graph = nx.Graph()

    # Take each satin and dice it up into pieces 1mm long.  This allows many
    # possible spots for jump-stitches between satins.  NetworkX will find the
    # best spots for us.

    for satin in satins:
        whole_satin = SatinSegment(satin)
        for segment in whole_satin.break_up(PIXELS_PER_MM):
            # This is necessary because shapely points aren't hashable and thus
            # can't be used as nodes directly.
            graph.add_node(str(segment.start_point), point=segment.start_point)
            graph.add_node(str(segment.end_point), point=segment.end_point)
            graph.add_edge(str(segment.start_point), str(segment.end_point), satin_segment=segment)

    return graph


def get_starting_and_ending_nodes(graph, starting_point, ending_point):
    """Find or choose the starting and ending graph nodes.

    If points were passed, we'll find the nearest graph nodes.  Since we split
    every satin up into 1mm-chunks, we'll be at most 1mm away which is good
    enough.

    If we weren't given starting and ending points, we'll pic kthe far left and
    right nodes.

    returns:
        (starting graph node, ending graph node)
    """

    nodes = []

    if starting_point is not None:
        nodes.append(get_nearest_node(graph, starting_point))
    else:
        nodes.append(get_extreme_node(graph, min))

    if ending_point is not None:
        nodes.append(get_nearest_node(graph, ending_point))
    else:
        nodes.append(get_extreme_node(graph, max))

    return nodes


def get_nearest_node(graph, point):
    point = shgeo.Point(*point)
    return min(graph.nodes, key=lambda node: graph.nodes[node]['point'].distance(point))


def get_extreme_node(graph, extreme_function):
    """Get the node with minimal or maximal X value."""

    return extreme_function(graph.nodes, key=lambda node: graph.nodes[node]['point'].x)


def add_jumps(graph):
    """Add jump stitches between satins as necessary.

    Jump stitches are added to ensure that all satins can be reached.  Only the
    minimal number and length of jumps necessary will be added.
    """

    # networkx makes this super-easy!  k_edge_agumentation tells us what edges
    # we need to add to ensure that the graph is fully connected.  We give it a
    # set of possible edges that it can consider adding (avail).  Each edge has
    # a weight, which we'll set as the length of the jump stitch.  The
    # algorithm will minimize the total length of jump stitches added.
    for jump in nx.k_edge_augmentation(graph, 1, avail=list(possible_jumps(graph))):
        graph.add_edge(*jump)


def possible_jumps(graph):
    """All possible jump stitches in the graph with their lengths.

    Returns: a generator of tuples: (node1, node2, length)
    """

    # We'll take the easy approach and list all edges that aren't already in
    # the graph.  networkx's algorithm is pretty efficient at ignoring
    # pointless options like jumping between two points on the same satin.

    for start, end in nx.complement(graph).edges():
        start_point = graph.nodes[start]['point']
        end_point = graph.nodes[end]['point']
        yield (start, end, start_point.distance(end_point))


def find_path(graph, starting_node, ending_node):
    """Find a path through the graph that sews every satin."""

    # This is done in two steps.  First, we find the shortest path from the
    # start to the end.  We remove it from the graph, and proceed to step 2.
    #
    # Then, we traverse the path node by node.  At each node, we follow any
    # branchings with a depth-first search.  We travel down each branch of
    # the tree, inserting each seen branch into the tree.  When the DFS
    # hits a dead-end, as it back-tracks, we also add the seen edges _again_.
    # Repeat until there are no more edges left in the graph.
    #
    # Duplicating the edges allows us to set up "underpathing".  As we stitch
    # down each branch, we'll do running stitch.  Then when we come back up,
    # we'll do satin stitch, covering the previous running stitch.

    graph = graph.copy()
    path = nx.shortest_path(graph, starting_node, ending_node)
    graph.remove_edges_from(zip(path[:-1], path[1:]))

    final_path = []
    prev = None
    for node in path:
        if prev is not None:
            final_path.append((prev, node))
        prev = node

        for n1, n2, edge_type in list(nx.dfs_labeled_edges(graph, node)):
            if n1 == n2:
                # dfs_labeled_edges gives us (start, start, "forward") for
                # the starting node for some reason
                continue

            if edge_type == "forward":
                final_path.append((n1, n2))
                graph.remove_edge(n1, n2)
            elif edge_type == "reverse":
                final_path.append((n2, n1))
            elif edge_type == "nontree":
                # a "nontree" happens when there exists an edge from n1 to n2
                # but n2 has already been visited.  It's a dead-end that runs
                # into part of the graph that we've already traversed.  We
                # do still need to make sure that satin is sewn, so we travel
                # down and back on this edge.
                #
                # It's possible for a given "nontree" edge to be listed more
                # than once so we'll deduplicate.
                if (n1, n2) in graph.edges:
                    final_path.append((n1, n2))
                    final_path.append((n2, n1))
                    graph.remove_edge(n1, n2)

    return final_path


def reversed_path(path):
    """Generator for a version of the path travelling in the opposite direction.

    Example:

    [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)] =>
    [(1, 5), (5, 4), (4, 3), (3, 2), (2, 1)]
    """

    for node1, node2 in reversed(path):
        yield (node2, node1)


def path_to_operations(graph, path):
    """Convert an edge path to a list of SatinSegment and JumpStitch instances."""

    operations = []

    for start, end in path:
        satin_segment = graph[start][end].get('satin_segment')
        if satin_segment:
            start_point = graph.nodes[start]['point']
            if satin_segment.start_point != start_point:
                satin_segment = satin_segment.reversed()
            operations.append(satin_segment)
        else:
            operations.append(JumpStitch(graph.nodes[start]['point'], graph.nodes[end]['point']))

    # find_path() will have duplicated some of the edges in the graph.  We don't
    # want to sew the same satin twice.  If a satin section appears twice in the
    # path, we'll sew the first occurrence as running stitch.  It will later be
    # covered by the satin stitch.
    seen = set()

    for i, item in reversed(list(enumerate(operations))):
        if isinstance(item, SatinSegment):
            if item in seen:
                operations[i] = item.to_running_stitch()
            else:
                seen.add(item)

    return operations


def collapse_sequential_segments(old_operations):
    old_operations = iter(old_operations)
    new_operations = [next(old_operations)]

    for operation in old_operations:
        if new_operations[-1].is_sequential(operation):
            new_operations[-1] += operation
        else:
            new_operations.append(operation)

    return new_operations


def operations_to_elements_and_trims(operations):
    """Convert a list of operations to Elements and locations of trims.

    Returns:
        (nodes, trims)

        element -- a list of Element instances
        trims -- indices of nodes after which the thread should be trimmed
    """

    elements = []
    trims = []

    for operation in operations:
        # Ignore JumpStitch opertions.  Jump stitches in Ink/Stitch are
        # implied and added by Embroider if needed.
        if isinstance(operation, (SatinSegment, RunningStitch)):
            elements.append(operation.to_element())
        elif isinstance(operation, (JumpStitch)):
            if elements and operation.length > PIXELS_PER_MM:
                trims.append(len(elements) - 1)

    return elements, trims
