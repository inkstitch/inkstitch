# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
from itertools import chain

import networkx as nx
from shapely import geometry as shgeo
from shapely.geometry import Point as ShapelyPoint

import inkex

from ..commands import add_commands
from ..elements import SatinColumn, Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, generate_unique_id, line_strings_to_csp
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from ..utils import Point as InkstitchPoint
from ..utils import cache, cut
from .utils.autoroute import (add_elements_to_group, add_jumps,
                              create_new_group, find_path,
                              get_starting_and_ending_nodes,
                              preserve_original_groups,
                              remove_original_elements)


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

        _ensure_even_repeats(satin)
        _ensure_rungs(satin)

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

    def __init__(self, start, end, source_element, destination_element):
        """Initialize a JumpStitch.

        Arguments:
            start, end -- instances of shgeo.Point
        """

        self.start = start
        self.end = end
        self.source_element = source_element
        self.destination_element = destination_element

    def is_sequential(self, other):
        # Don't bother joining jump stitches.
        return False

    @property
    @cache
    def length(self):
        return self.start.distance(self.end)

    def as_line_string(self):
        return shgeo.LineString((self.start, self.end))

    def should_trim(self):
        actual_jump = self.as_line_string().difference(self.source_element.shape)
        actual_jump = actual_jump.difference(self.destination_element.shape)

        return actual_jump.length > PIXELS_PER_MM


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
        node = inkex.PathElement()
        d = str(inkex.paths.CubicSuperPath(line_strings_to_csp([self.path])))
        node.set("d", d)

        dasharray = inkex.Style("stroke-dasharray:0.5,0.5;")
        style = inkex.Style(self.original_element.node.get('style', '')) + dasharray
        node.set("style", str(style))
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
        group = create_new_group(parent, index, _("Auto-Route"))
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
            graph.add_node(str(segment.start_point), point=segment.start_point, element=element)
            graph.add_node(str(segment.end_point), point=segment.end_point, element=element)
            graph.add_edge(str(segment.start_point), str(
                segment.end_point), segment=segment, element=element)

            if preserve_order:
                # The graph is a directed graph, but we want to allow travel in
                # any direction in a satin, so we add the edge in the opposite
                # direction too.
                graph.add_edge(str(segment.end_point), str(
                    segment.start_point), segment=segment, element=element)

    return graph


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
            operations.append(JumpStitch(graph.nodes[start]['point'],
                                         graph.nodes[end]['point'],
                                         graph.nodes[start]['element'],
                                         graph.nodes[end]['element']))

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
            if elements and operation.should_trim():
                trims.append(len(elements) - 1)

    return elements, list(set(trims)), original_parent_nodes


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


def _ensure_rungs(element):
    if len(element.paths) == 2 and len(element.paths[0]) != len(element.paths[1]):
        rails = [shgeo.LineString(element.flatten_subpath(rail)) for rail in element.rails]
        # Add the rung just after the start of the satin.
        rung_start = rails[0].interpolate(0.1)
        rung_end = rails[1].interpolate(0.1)
        rung = shgeo.LineString((rung_start, rung_end))

        # insert rung into the satin path
        d = element.node.get('d')
        d += ' M '
        d += ', '.join(' '.join(str(c) for c in coord) for coord in rung.coords)
        element.node.set('d', d)


def _ensure_even_repeats(element):
    # center underlay can have an odd number of repeats, this would cause jumps in auto route satin
    # so let's set it to an even number of repeats, but not lower than 2
    if int(element.node.get(INKSTITCH_ATTRIBS['center_walk_underlay_repeats'], 2)) % 2 == 1:
        repeats = max(int(element.node.get(INKSTITCH_ATTRIBS['center_walk_underlay_repeats'])) - 1, 2)
        element.node.set(INKSTITCH_ATTRIBS['center_walk_underlay_repeats'], repeats)


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
