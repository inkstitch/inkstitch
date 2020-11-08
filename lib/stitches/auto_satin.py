import math
from itertools import chain

import inkex
import networkx as nx
from lxml import etree
from shapely import geometry as shgeo
from shapely.geometry import Point as ShapelyPoint

from ..commands import add_commands
from ..elements import SatinColumn, Stroke
from ..i18n import _
from ..svg import (PIXELS_PER_MM, generate_unique_id, get_correction_transform,
                   line_strings_to_csp)
from ..svg.tags import (INKSCAPE_LABEL, INKSTITCH_ATTRIBS, SVG_GROUP_TAG,
                        SVG_PATH_TAG)
from ..utils import Point as InkstitchPoint
from ..utils import cache, cut


class SatinSegment(object):
    """A portion of SatinColumn.

    Attributes:
        satin -- the SatinColumn instance
        start -- how far along the satin this graph edge starts (a float from 0.0 to 1.0)
        end -- how far along the satin this graph edge ends (a float from 0.0 to 1.0)
        reverse -- if True, reverse the direction of the satin
    """

    def __init__(self, satin, start=0.0, end=1.0, reverse=False, original_satin=None):
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
        self.original_satin = original_satin or self.satin
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
            satin, after = satin.split(
                (self.end - self.start) / (1.0 - self.start))

        if self.reverse:
            satin = satin.reverse()

        satin = satin.apply_transform()

        return satin

    to_element = to_satin

    def to_running_stitch(self):
        return RunningStitch(self.center_line, self.original_satin)

    def break_up(self, segment_size):
        """Break this SatinSegment up into SatinSegments of the specified size."""

        num_segments = int(math.ceil(self.center_line.length / segment_size))
        segments = []
        for i in range(num_segments):
            segments.append(SatinSegment(self.satin,
                                         float(i) / num_segments,
                                         float(i + 1) / num_segments,
                                         self.reverse,
                                         self.original_satin))

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
            center_line, after = cut(
                center_line, (self.end - self.start) / (1.0 - self.start), normalized=True)

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

    @property
    def original_node(self):
        return self.original_satin.node

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

    def __init__(self, path_or_stroke, original_element=None):
        if isinstance(path_or_stroke, Stroke):
            # Technically a Stroke object's underlying path could have multiple
            # subpaths.  We don't have a particularly good way of dealing with
            # that so we'll just use the first one.
            self.path = shgeo.LineString(path_or_stroke.paths[0])
            original_element = path_or_stroke
        else:
            self.path = path_or_stroke

        self.original_element = original_element
        self.running_stitch_length = \
            original_element.node.get(INKSTITCH_ATTRIBS['running_stitch_length_mm'], '') or \
            original_element.node.get(INKSTITCH_ATTRIBS['center_walk_underlay_stitch_length_mm'], '') or \
            original_element.node.get(INKSTITCH_ATTRIBS['contour_underlay_stitch_length_mm'], '')

    def to_element(self):
        node = etree.Element(SVG_PATH_TAG)
        d = str(inkex.paths.CubicSuperPath(line_strings_to_csp([self.path])))
        node.set("d", d)

        style = self.original_element.parse_style()
        style['stroke-dasharray'] = "0.5,0.5"
        style = str(inkex.Style(style))
        node.set("style", style)
        node.set(INKSTITCH_ATTRIBS['running_stitch_length_mm'], self.running_stitch_length)

        stroke = Stroke(node)

        return stroke

    @property
    @cache
    def start_point(self):
        return self.path.interpolate(0.0, normalized=True)

    @property
    @cache
    def end_point(self):
        return self.path.interpolate(1.0, normalized=True)

    @property
    def original_node(self):
        return self.original_element.node

    @cache
    def reversed(self):
        return RunningStitch(shgeo.LineString(reversed(self.path.coords)), self.original_element)

    def is_sequential(self, other):
        if not isinstance(other, RunningStitch):
            return False

        if self.original_element is not other.original_element:
            return False

        return self.path.distance(other.path) < 0.5

    def __add__(self, other):
        new_path = shgeo.LineString(chain(self.path.coords, other.path.coords))
        return RunningStitch(new_path, self.original_element)


def auto_satin(elements, preserve_order=False, starting_point=None, ending_point=None, trim=False):
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

    If preserve_order is True, then the algorithm is constrained to keep the
    satins in the same order they were in the original list.  It will only split
    them and add running stitch as necessary to achieve an optimal stitch path.

    Elements should be primarily made up of SatinColumn instances.  Some Stroke
    instances (that are running stitch) can be included to indicate how to travel
    between two SatinColumns.  This works best when preserve_order is True.

    If preserve_order is True, then the elements and any newly-created elements
    will be in the same position in the SVG DOM.  If preserve_order is False, then
    the elements will be removed from their current position in SVG DOM and added
    to a newly-created group node.

    If trim is True, then Trim commands will be added to avoid jump stitches.

    Returns: a list of Element instances making up the stitching order chosen.
      Jumps between objects are implied if they are not right next to each
      other.
    """

    # save these for create_new_group() call below
    parent = elements[0].node.getparent()
    index = parent.index(elements[0].node)

    graph = build_graph(elements, preserve_order)
    add_jumps(graph, elements, preserve_order)
    starting_node, ending_node = get_starting_and_ending_nodes(
        graph, elements, preserve_order, starting_point, ending_point)
    path = find_path(graph, starting_node, ending_node)
    operations = path_to_operations(graph, path)
    operations = collapse_sequential_segments(operations)
    new_elements, trims, original_parents = operations_to_elements_and_trims(operations, preserve_order)

    remove_original_elements(elements)

    if preserve_order:
        preserve_original_groups(new_elements, original_parents)
    else:
        group = create_new_group(parent, index)
        add_elements_to_group(new_elements, group)

    name_elements(new_elements, preserve_order)

    if trim:
        new_elements = add_trims(new_elements, trims)

    return new_elements


def build_graph(elements, preserve_order=False):
    if preserve_order:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    # Take each satin and dice it up into pieces 1mm long.  This allows many
    # possible spots for jump-stitches between satins.  NetworkX will find the
    # best spots for us.

    for element in elements:
        segments = []
        if isinstance(element, Stroke):
            segments.append(RunningStitch(element))
        elif isinstance(element, SatinColumn):
            whole_satin = SatinSegment(element)
            segments = whole_satin.break_up(PIXELS_PER_MM)

        for segment in segments:
            # This is necessary because shapely points aren't hashable and thus
            # can't be used as nodes directly.
            graph.add_node(str(segment.start_point), point=segment.start_point)
            graph.add_node(str(segment.end_point), point=segment.end_point)
            graph.add_edge(str(segment.start_point), str(
                segment.end_point), segment=segment, element=element)

            if preserve_order:
                # The graph is a directed graph, but we want to allow travel in
                # any direction in a satin, so we add the edge in the opposite
                # direction too.
                graph.add_edge(str(segment.end_point), str(
                    segment.start_point), segment=segment, element=element)

    return graph


def get_starting_and_ending_nodes(graph, elements, preserve_order, starting_point, ending_point):
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

    nodes.append(find_node(graph, starting_point,
                           min, preserve_order, elements[0]))
    nodes.append(find_node(graph, ending_point,
                           max, preserve_order, elements[-1]))

    return nodes


def find_node(graph, point, extreme_function, constrain_to_satin=False, satin=None):
    if constrain_to_satin:
        nodes = get_nodes_on_element(graph, satin)
    else:
        nodes = graph.nodes()

    if point is None:
        return extreme_function(nodes, key=lambda node: graph.nodes[node]['point'].x)
    else:
        point = shgeo.Point(*point)
        return min(nodes, key=lambda node: graph.nodes[node]['point'].distance(point))


def get_nodes_on_element(graph, element):
    nodes = set()

    for start_node, end_node, element_for_edge in graph.edges(data='element'):
        if element_for_edge is element:
            nodes.add(start_node)
            nodes.add(end_node)

    return nodes


def add_jumps(graph, elements, preserve_order):
    """Add jump stitches between elements as necessary.

    Jump stitches are added to ensure that all elements can be reached.  Only the
    minimal number and length of jumps necessary will be added.
    """

    if preserve_order:
        # For each sequential pair of elements, find the shortest possible jump
        # stitch between them and add it.  The directions of these new edges
        # will enforce stitching the satins in order.

        for element1, element2 in zip(elements[:-1], elements[1:]):
            potential_edges = []

            nodes1 = get_nodes_on_element(graph, element1)
            nodes2 = get_nodes_on_element(graph, element2)

            for node1 in nodes1:
                for node2 in nodes2:
                    point1 = graph.nodes[node1]['point']
                    point2 = graph.nodes[node2]['point']
                    potential_edges.append((point1, point2))

            if potential_edges:
                edge = min(potential_edges, key=lambda p1_p2: p1_p2[0].distance(p1_p2[1]))
                graph.add_edge(str(edge[0]), str(edge[1]), jump=True)
    else:
        # networkx makes this super-easy!  k_edge_agumentation tells us what edges
        # we need to add to ensure that the graph is fully connected.  We give it a
        # set of possible edges that it can consider adding (avail).  Each edge has
        # a weight, which we'll set as the length of the jump stitch.  The
        # algorithm will minimize the total length of jump stitches added.
        for jump in nx.k_edge_augmentation(graph, 1, avail=list(possible_jumps(graph))):
            graph.add_edge(*jump, jump=True)


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
    # Visiting the edges again on the way back allows us to set up
    # "underpathing".  As we stitch down each branch, we'll do running stitch.
    # Then when we come back up, we'll do satin stitch, covering the previous
    # running stitch.
    path = nx.shortest_path(graph, starting_node, ending_node)

    # Copy the graph so that we can remove the edges as we visit them.
    # This also converts the directed graph into an undirected graph in the
    # case that "preserve_order" is set.  This way we avoid going back and
    # forth on each satin twice due to the satin edges being in the graph
    # twice (forward and reverse).
    graph = nx.Graph(graph)
    graph.remove_edges_from(list(zip(path[:-1], path[1:])))

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

    graph = nx.Graph(graph)

    operations = []

    for start, end in path:
        segment = graph[start][end].get('segment')
        if segment:
            start_point = graph.nodes[start]['point']
            if segment.start_point != start_point:
                segment = segment.reversed()
            operations.append(segment)
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


def operations_to_elements_and_trims(operations, preserve_order):
    """Convert a list of operations to Elements and locations of trims.

    Returns:
        (elements, trims, original_parents)

        elements -- a list of Element instances
        trims -- indices of nodes after which the thread should be trimmed
        original_parents -- a parallel list of the original SVG parent nodes that spawned each element
    """

    elements = []
    trims = []
    original_parent_nodes = []

    for operation in operations:
        # Ignore JumpStitch operations.  Jump stitches in Ink/Stitch are
        # implied and added by Embroider if needed.
        if isinstance(operation, (SatinSegment, RunningStitch)):
            elements.append(operation.to_element())
            original_parent_nodes.append(operation.original_node.getparent())
        elif isinstance(operation, (JumpStitch)):
            if elements and operation.length > 0.75 * PIXELS_PER_MM:
                trims.append(len(elements) - 1)

    return elements, list(set(trims)), original_parent_nodes


def remove_original_elements(elements):
    for element in elements:
        for command in element.commands:
            remove_from_parent(command.connector)
            remove_from_parent(command.use)
        remove_from_parent(element.node)


def remove_from_parent(node):
    if node.getparent() is not None:
        node.getparent().remove(node)


def preserve_original_groups(elements, original_parent_nodes):
    """Ensure that all elements are contained in the original SVG group elements.

    When preserve_order is True, no SatinColumn or Stroke elements will be
    reordered in the XML tree.  This makes it possible to preserve original SVG
    group membership.  We'll ensure that each newly-created Element is added
    to the group that contained the original SatinColumn that spawned it.
    """

    for element, parent in zip(elements, original_parent_nodes):
        if parent is not None:
            parent.append(element.node)
            element.node.set('transform', get_correction_transform(parent, child=True))


def create_new_group(parent, insert_index):
    group = etree.Element(SVG_GROUP_TAG, {
        INKSCAPE_LABEL: _("Auto-Satin"),
        "transform": get_correction_transform(parent, child=True)
    })
    parent.insert(insert_index, group)

    return group


def add_elements_to_group(elements, group):
    for element in elements:
        group.append(element.node)


def name_elements(new_elements, preserve_order):
    """Give the newly-created SVG objects useful names.

    Objects will be named like this:

      * AutoSatin 1
      * AutoSatin 2
      * AutoSatin Running Stitch 3
      * AutoSatin 4
      * AutoSatin Running Stitch 5
      ...

    Objects are numbered starting with 1.  Satins are named "AutoSatin #", and
    running stitches are named "AutoSatin Running Stitch #".

    If preserve_order is true and the element already has an INKSCAPE_LABEL,
    we'll leave it alone.  That way users can see which original satin the new
    satin(s) came from.

    SVG element IDs are also set.  Since these need to be unique across the
    document, the numbers will likely not match up with the numbers in the
    name we set.
    """

    index = 1
    for element in new_elements:
        if isinstance(element, SatinColumn):
            element.node.set("id", generate_unique_id(element.node, "autosatin"))
        else:
            element.node.set("id", generate_unique_id(element.node, "autosatinrun"))

        if not (preserve_order and INKSCAPE_LABEL in element.node.attrib):
            if isinstance(element, SatinColumn):
                # L10N Label for a satin column created by Auto-Route Satin Columns and Lettering extensions
                element.node.set(INKSCAPE_LABEL, _("AutoSatin %d") % index)
            else:
                # L10N Label for running stitch (underpathing) created by Auto-Route Satin Columns amd Lettering extensions
                element.node.set(INKSCAPE_LABEL, _("AutoSatin Running Stitch %d") % index)

            index += 1


def add_trims(elements, trim_indices):
    """Add trim commands on the specified elements.

    If any running stitches immediately follow a trim, they are eliminated.
    When we're trimming, there's no need to try to reduce the jump length,
    so the running stitch would be a waste of time (and thread).
    """

    trim_indices = set(trim_indices)
    new_elements = []
    just_trimmed = False
    for i, element in enumerate(elements):
        if just_trimmed and isinstance(element, Stroke):
            element.node.getparent().remove(element.node)
            continue

        if i in trim_indices:
            add_commands(element, ["trim"])
            just_trimmed = True
        else:
            just_trimmed = False

        new_elements.append(element)

    # trim at the end, too
    if i not in trim_indices:
        add_commands(element, ["trim"])

    return new_elements
