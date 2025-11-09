# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

import inkex
import networkx as nx
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import nearest_points, substring, unary_union

from ..commands import add_commands
from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, generate_unique_id, get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from ..utils.threading import check_stop_flag
from .utils.autoroute import (add_elements_to_group, add_jumps,
                              create_new_group, find_path,
                              get_starting_and_ending_nodes,
                              preserve_original_groups,
                              remove_original_elements)


class LineSegments:
    '''
    Takes elements and splits them into segments.

    Attributes:
        _lines   -- a list of LineStrings from the subpaths of the Stroke elements
        _elements -- a list of Stroke elements for each corresponding line in _lines
        _intersection_points -- a dictionary with intersection points {line_index: [intersection_points]}
        segments -- (public) a list of segments and corresponding elements [[segment, element], ...]
    '''

    def __init__(self, elements):
        self._lines = []
        self._elements = []
        self._intersection_points = defaultdict(list)
        self.segments = []

        self._process_elements(elements)
        self._get_intersection_points()
        self._get_segments()

    def _process_elements(self, elements):
        for element in elements:
            lines = element.as_multi_line_string().geoms

            for line in lines:
                # split at self-intersections if necessary
                unary_lines = unary_union(line)
                if isinstance(unary_lines, MultiLineString):
                    for unary_line in unary_lines.geoms:
                        self._lines.append(unary_line)
                        self._elements.append(element)
                else:
                    self._lines.append(line)
                    self._elements.append(element)

                check_stop_flag()

    def _get_intersection_points(self):
        for i, line1 in enumerate(self._lines):
            for j in range(i + 1, len(self._lines)):
                check_stop_flag()

                line2 = self._lines[j]
                distance = line1.distance(line2)
                if distance > 50:
                    continue
                if not distance == 0:
                    # add nearest points
                    near = nearest_points(line1, line2)
                    self._add_point(i, near[0])
                    self._add_point(j, near[1])
                # add intersections
                intersections = line1.intersection(line2)
                if isinstance(intersections, Point):
                    self._add_point(i, intersections)
                    self._add_point(j, intersections)
                elif isinstance(intersections, MultiPoint):
                    for point in intersections.geoms:
                        self._add_point(i, point)
                        self._add_point(j, point)
                elif isinstance(intersections, LineString):
                    for point in intersections.coords:
                        self._add_point(i, Point(*point))
                        self._add_point(j, Point(*point))

    def _add_point(self, element, point):
        self._intersection_points[element].append(point)

    def _get_segments(self):
        '''
        Splits elements into segments at intersection and "almost intersecions".
        The split method would make this very easy (it can split a MultiString with
        MultiPoints) but sadly it fails too often, while snap moves the points away
        from where we want them.  So we need to calculate the distance along the line
        and finally split it into segments with shapelys substring method.
        '''
        self.segments = []
        for i, line in enumerate(self._lines):
            length = line.length
            points = self._intersection_points[i]

            distances = [0, length]
            for point in points:
                distances.append(line.project(point))
            distances = sorted(set(distances))

            for j in range(len(distances) - 1):
                start = distances[j]
                end = distances[j + 1]

                if end - start > 0.1:
                    seg = substring(line, start, end)
                    self.segments.append([seg, self._elements[i]])


def autorun(elements, preserve_order=False, break_up=None, starting_point=None, ending_point=None, trim=False):
    graph = build_graph(elements, preserve_order, break_up)

    graph = add_jumps(graph, elements, preserve_order)

    starting_point, ending_point = get_starting_and_ending_nodes(
        graph, elements, preserve_order, starting_point, ending_point)

    path = find_path(graph, starting_point, ending_point)
    path = add_path_attribs(path)

    parent = None
    if not preserve_order:
        parent = elements[0].node.getparent()

    new_elements, trims, original_parents = path_to_elements(graph, path, trim, parent)

    if preserve_order:
        preserve_original_groups(new_elements, original_parents, transform=False)
    else:
        insert_index = parent.index(elements[0].node)
        group = create_new_group(parent, insert_index, _("Auto-Route"), False)
        add_elements_to_group(new_elements, group)

    if trim:
        add_trims(new_elements, trims)

    remove_original_elements(elements)


def build_graph(elements, preserve_order, break_up):
    if preserve_order:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    if not break_up:
        segments = []
        for element in elements:
            line_strings = [[line, element] for line in element.as_multi_line_string().geoms]
            segments.extend(line_strings)
    else:
        segments = LineSegments(elements).segments

    for segment, element in segments:
        for c1, c2 in zip(segment.coords[:-1], segment.coords[1:]):
            start = Point(*c1)
            end = Point(*c2)

            graph.add_node(str(start), point=start)
            graph.add_node(str(end), point=end)
            graph.add_edge(str(start), str(end), element=element)

            if preserve_order:
                # The graph is a directed graph, but we want to allow travel in
                # any direction, so we add the edge in the opposite direction too.
                graph.add_edge(str(end), str(start), element=element)

            check_stop_flag()

    return graph


def add_path_attribs(path):
    # find_path() will have duplicated some of the edges in the graph.  We don't
    # want to sew the same running stitch twice.  If a running stitch section appears
    # twice in the path, we'll sew the first occurrence as a simple running stitch without
    # the original running stitch repetitions and bean stitch settings.
    seen = set()
    for i, point in reversed(list(enumerate(path))):
        if point in seen:
            path[i] = (*point, "underpath")
        else:
            path[i] = (*point, "autorun")
            seen.add(point)
            seen.add((point[1], point[0]))
    return path


def path_to_elements(graph, path, trim, parent=None):  # noqa: C901
    element_list = []
    original_parents = []
    trims = []

    d = ""
    position = 0
    path_direction = "autorun"
    just_trimmed = False
    el = None
    for start, end, direction in path:
        check_stop_flag()

        try:
            element = graph[start][end].get('element')
        except KeyError:
            # runs with the preserve order option may need this
            element = graph[end][start].get('element')
        start_coord = graph.nodes[start]['point']
        end_coord = graph.nodes[end]['point']
        # create a new element if we hit an other original element to keep it's properties
        if el and element and el != element and d and not direction == 'underpath':
            element_list.append(create_element(d, position, path_direction, el, parent))
            original_parents.append(el.node.getparent())
            d = ""
            position += 1
        if element:
            el = element

            if just_trimmed:
                if direction == "underpath":
                    # no sense in doing underpath after we trim
                    continue
                else:
                    just_trimmed = False

            # create a new element if direction (purpose) changes
            if direction != path_direction:
                if d:
                    element_list.append(create_element(d, position, path_direction, el, parent))
                    original_parents.append(el.node.getparent())
                    d = ""
                    position += 1
                path_direction = direction

            if d == "":
                d = f"M {start_coord.x} {start_coord.y}, {end_coord.x} {end_coord.y}"
            else:
                d += f", {end_coord.x} {end_coord.y}"
        elif el and d:
            # this is a jump, so complete the element whose path we've been building
            element_list.append(create_element(d, position, path_direction, el, parent))
            original_parents.append(el.node.getparent())
            d = ""

            if trim and start_coord.distance(end_coord) > 0.75 * PIXELS_PER_MM:
                trims.append(position)
                just_trimmed = True

            position += 1

    if d:
        element_list.append(create_element(d, position, path_direction, el, parent))
    original_parents.append(el.node.getparent())

    return element_list, trims, original_parents


def create_element(path, position, direction, element, parent=None):  # noqa: C901
    if not path:
        return

    el_id = f"{direction}_{position}_"
    if parent is None:
        parent = element.node.getparent()

    index = position + 1
    if direction == "autorun":
        label = _("AutoRun %d") % index
        dasharray = 'none'
        path_type = 'autorun-top'
    else:
        label = _("AutoRun Underpath %d") % index
        dasharray = '2 1.1'
        path_type = 'autorun-underpath'

    node = inkex.PathElement()
    node.set("id", generate_unique_id(element.node, el_id))
    node.set(INKSCAPE_LABEL, label)
    node.set("d", path)
    node.set("inkstitch:path_type", path_type)
    node.set("style", element.node.style)
    node.style["fill"] = 'none'
    node.style["stroke-dasharray"] = dasharray
    node.transform = get_correction_transform(parent, child=True)
    node.apply_transform()

    # Set Ink/Stitch attributes
    stitch_length = element.node.get(INKSTITCH_ATTRIBS['running_stitch_length_mm'], '')
    tolerance = element.node.get(INKSTITCH_ATTRIBS['running_stitch_tolerance_mm'], '')
    repeats = int(element.node.get(INKSTITCH_ATTRIBS['repeats'], 1))
    if repeats % 2 == 0:
        repeats -= 1

    if direction == "autorun":
        for attrib in element.node.attrib:
            if attrib.startswith(inkex.NSS['inkstitch'], 1):
                if attrib == INKSTITCH_ATTRIBS['repeats']:
                    node.set(INKSTITCH_ATTRIBS['repeats'], str(repeats))
                else:
                    node.set(attrib, element.node.get(attrib))
    else:
        if stitch_length:
            node.set(INKSTITCH_ATTRIBS['running_stitch_length_mm'], stitch_length)
        if tolerance:
            node.set(INKSTITCH_ATTRIBS['running_stitch_tolerance_mm'], tolerance)
    return Stroke(node)


def add_trims(elements, trim_indices):
    for i in trim_indices:
        add_commands(elements[i], ["trim"])
