# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points

import inkex

from ..i18n import _
from ..svg import generate_unique_id, get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from .utils.autoroute import (add_jumps, create_new_group, find_path,
                              get_starting_and_ending_nodes,
                              remove_original_elements)
from shapely.ops import substring


class LineSegments:
    '''
    Takes elements and splits them into segments.

    Attributes:
        elements -- a list of selected stroke elements
        intersection_points -- a dictionary with intersection points {element_index: [intersection_points]}
        segments -- a list of segments and corresponding elements [[segment, element]]
    '''
    def __init__(self, elements):
        self.elements = elements
        self._get_intersection_points()
        self._get_segments()

    def _get_intersection_points(self):
        self.intersection_points = {}
        num_elements = len(self.elements)
        for i, element in enumerate(self.elements):
            element_shape = element.as_multi_line_string()
            for j in range(i + 1, num_elements):
                e = self.elements[j]
                shape = e.as_multi_line_string()
                distance = element_shape.distance(shape)
                if distance > 50:
                    continue
                if not distance == 0:
                    # add nearest points
                    near = nearest_points(element_shape, shape)
                    self._add_point(i, near[0])
                    self._add_point(j, near[1])
                # add intersections
                intersections = element_shape.intersection(shape)
                if isinstance(intersections, Point):
                    self._add_point(i, intersections)
                    self._add_point(j, intersections)
                elif isinstance(intersections, LineString):
                    for point in intersections.coords:
                        self._add_point(i, Point(*point))
                        self._add_point(j, Point(*point))

    def _add_point(self, element, point):
        if element in self.intersection_points:
            self.intersection_points[element] += [point]
        else:
            self.intersection_points[element] = [point]

    def _get_segments(self):
        '''
        Splits elements into segments at intersection and "almost intersecions".
        The split method would make this very easy (it can split a MultiString with
        MultiPoints) but sadly it fails too often, while snap moves the points away
        from where we want them.  So we need to calculate the distance along the line
        and finally split it into segments with shapelys substring method.
        '''
        self.segments = []
        for i, element in enumerate(self.elements):
            line_strings = element.as_multi_line_string()
            points = self.intersection_points[i]
            for line in line_strings.geoms:
                length = line.length
                points = self.intersection_points[i]
                distances = [0, length]
                for point in points:
                    distance = line.project(point, normalized=True)
                    if distance < length:
                        distances.append(distance)
                distances = sorted(set(distances))
                for i in range(len(distances) - 1):
                    start = distances[i]
                    end = distances[i + 1]
                    seg = substring(line, start, end, normalized=True)
                    if seg.length > 0.1:
                        self.segments.append([seg, element])


def autorun(elements, preserve_order=False, break_up=None, starting_point=None, ending_point=None):
    graph = build_graph(elements, preserve_order, break_up)
    graph = add_jumps(graph, elements, preserve_order)

    starting_point, ending_point = get_starting_and_ending_nodes(
        graph, elements, preserve_order, starting_point, ending_point)

    path = find_path(graph, starting_point, ending_point)
    path = add_path_attribs(path)

    new_elements, original_parents = path_to_elements(graph, path)

    if preserve_order:
        for element, parent in zip(new_elements, original_parents):
            if parent is not None:
                parent.append(element)
                element.set('transform', get_correction_transform(parent, child=True))
    else:
        parent = elements[0].node.getparent()
        insert_index = parent.index(elements[0].node)
        group = create_new_group(parent, insert_index, _("Auto-Run"))
        insert_elements(group, new_elements)

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


def path_to_elements(graph, path):
    element_list = []
    original_parents = []

    d = ""
    position = 0
    path_direction = "autorun"
    el = None
    for start, end, direction in path:
        element = graph[start][end].get('element')
        end_coord = graph.nodes[end]['point']
        if element:
            el = element
            # create a new element if direction (purpose) changes
            if direction != path_direction:
                if d:
                    element_list.append(create_element(d, position, path_direction, el))
                    original_parents.append(el.node.getparent())
                    d = ""
                    position += 1
                path_direction = direction

            if d == "":
                start_coord = graph.nodes[start]['point']
                d = "M %s %s, %s %s" % (start_coord.x, start_coord.y, end_coord.x, end_coord.y)
            else:
                d += ", %s %s" % (end_coord.x, end_coord.y)
        # exclude jump stitches bigger than 1 mm from the path
        elif el and d:
            element_list.append(create_element(d, position, path_direction, el))
            original_parents.append(el.node.getparent())
            d = ""
            position += 1

    element_list.append(create_element(d, position, path_direction, el))
    original_parents.append(el.node.getparent())

    return [element_list, original_parents]


def create_element(path, position, direction, element):
    if not path:
        return

    style = inkex.Style(element.node.get("style"))
    style = style + inkex.Style("stroke-dasharray:0.5,0.5;fill:none;marker-start:none;marker-end:none;")
    el_id = "%s_%s_" % (direction, position)

    index = position + 1
    if direction == "autorun":
        label = _("AutoRun %d") % index
    else:
        label = _("AutoRun Underpath %d") % index

    stitch_length = element.node.get(INKSTITCH_ATTRIBS['running_stitch_length_mm'], '')
    bean = element.node.get(INKSTITCH_ATTRIBS['bean_stitch_repeats'], 0)
    repeats = int(element.node.get(INKSTITCH_ATTRIBS['repeats'], 1))
    if repeats % 2 == 0:
        repeats -= 1

    node = inkex.PathElement()
    node.set("id", generate_unique_id(element.node, el_id))
    node.set(INKSCAPE_LABEL, label)
    node.set("d", path)
    node.set("style", str(style))
    if stitch_length:
        node.set(INKSTITCH_ATTRIBS['running_stitch_length_mm'], stitch_length)
    if direction == "autorun":
        node.set(INKSTITCH_ATTRIBS['repeats'], str(repeats))
        if bean:
            node.set(INKSTITCH_ATTRIBS['bean_stitch_repeats'], bean)

    return node


def insert_elements(group, elements):
    elements.reverse()
    for element in elements:
        group.insert(0, element)
