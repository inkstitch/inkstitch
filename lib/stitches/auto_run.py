# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from shapely.geometry import LineString, Point, MultiPoint, MultiLineString

import inkex

from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, generate_unique_id, get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from .utils.autoroute import (add_jumps, create_new_group, find_path,
                              get_starting_and_ending_nodes,
                              remove_original_elements)


def autorun(elements, preserve_order=False, starting_point=None, ending_point=None):
    graph = build_graph(elements, preserve_order)
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


def build_graph(elements, preserve_order):
    if preserve_order:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    for element in elements:
        if not isinstance(element, Stroke):
            continue

        segments = break_up_segments(element, elements)

        for segment in segments:
            for c1, c2 in zip(segment.coords[1:], segment.coords[:-1]):
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


def break_up_segments(element, elements):
    segment_list = []
    line_strings = [LineString(path) for path in element.paths]
    for line in line_strings:
        points = []
        # add points at intersections with other elements (not at self intersections, sorry)
        intersection_points = get_intersections(line, element, elements)
        if intersection_points:
            points.extend(intersection_points)
        # maybe that are already enough points
        # split at points
        points = MultiPoint(points)
        # split line at points, trouble: split() doesn't seem to work on small lines at all
        # but differene with buffer seems to do the trick
        # source: https://gis.stackexchange.com/questions/297134/shapely-floating-problems-with-split/327287#327287
        seg = line.difference(points.buffer(1e-13))
        if isinstance(seg, LineString):
            segment_list.append(seg)
        else:
            segment_list.extend(seg.geoms)

    return segment_list


def get_intersections(line, element, elements):
    points = []
    for e in elements:
        if element == e:
            continue
        intersections = line.intersection(e.shape)
        if intersections.is_empty:
            continue
        if isinstance(intersections, Point):
            points.append(intersections)
        elif isinstance(intersections, LineString):
            points.extend([Point(*c) for c in intersections.coords])
        elif isinstance(intersections, MultiLineString):
            for line in intersections.geoms:
                points.extend([Point(*c) for c in line.coords])
    return points


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
        if element:
            el = element
            end = graph.nodes[end]['point']
            # create a new element if direction (prupose) changes
            if direction != path_direction:
                if d:
                    element_list.append(create_element(d, position, path_direction, el))
                    original_parents.append(el.node.getparent())
                    d = ""
                    position += 1
                path_direction = direction

            if d == "":
                start = graph.nodes[start]['point']
                d = "M %s %s, %s %s" % (start.x, start.y, end.x, end.y)
            else:
                d += ", %s %s" % (end.x, end.y)
        # exclude jump stitches bigger than 1 mm
        elif el and d and graph.nodes[start]['point'].distance(graph.nodes[end]['point']) > PIXELS_PER_MM:
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
    style = style + inkex.Style("stroke-dasharray:0.5,0.5;fill:none;")
    el_id = "%s_" % direction

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
        node.set(INKSTITCH_ATTRIBS['bean_stitch_repeats'], bean)
        node.set(INKSTITCH_ATTRIBS['repeats'], str(repeats))

    return node


def insert_elements(group, elements):
    elements.reverse()
    for element in elements:
        group.insert(0, element)
