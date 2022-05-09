# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import nearest_points

import inkex

from ..debug import debug
from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, generate_unique_id, get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from .utils.autoroute import (add_jumps, create_new_group, find_path,
                              get_starting_and_ending_nodes,
                              remove_original_elements)


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

    for element in elements:
        if not isinstance(element, Stroke):
            continue

        if not break_up:
            segments = [LineString(path) for path in element.paths]
        else:
            segments = break_up_segments(element, elements)

        for segment in segments:
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


def break_up_segments(element, elements):
    '''
    Add extra nodes at intersections and nearest points.  Users will still have control
    over the precision by adding nodes where they think good breaking points are.
    '''
    segment_list = []
    line_strings = [LineString(path) for path in element.paths]
    for line in line_strings:
        points = []
        # add points at intersections with other elements (not at self intersections, sorry)
        intersection_points = get_intersections(line, element, elements)
        if intersection_points:
            points.extend(intersection_points)
        # split at points
        points = MultiPoint(points)
        # split line at points, trouble: split() doesn't seem to work on small lines at all
        # but differene with buffer seems to do the trick
        # source: https://gis.stackexchange.com/questions/297134/shapely-floating-problems-with-split/327287#327287
        seg = line.difference(points.buffer(1e-13))
        if isinstance(seg, LineString):
            segment_list.append(seg)
        else:
            for geom in seg.geoms:
                if isinstance(geom, LineString) and geom.length > 1:
                    segment_list.append(geom)

    return segment_list


def get_intersections(line, element, elements):
    points = []
    for e in elements:
        if element == e:
            continue
        if line.distance(e.shape) > 50:
            continue
        # add nearest points
        near = nearest_points(line, e.as_multi_line_string())
        points.extend(near)
        # add intersections
        intersections = line.intersection(e.as_multi_line_string())
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
        elif el and d and graph.nodes[start]['point'].distance(graph.nodes[end]['point']) > PIXELS_PER_MM:
            element_list.append(create_element(d, position, path_direction, el))
            original_parents.append(el.node.getparent())
            d = ""
            position += 1
        elif el and d:
            # small jumps: use as normal stitches
            d += ", %s %s" % (end_coord.x, end_coord.y)

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
