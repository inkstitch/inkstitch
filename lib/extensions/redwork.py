# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from inkex import Group, Path, PathElement, errormsg
from shapely import unary_union
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, nearest_points, substring

from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..utils.geometry import ensure_multi_line_string
from .base import InkstitchExtension


class Redwork(InkstitchExtension):
    """Takes a bunch of stroke elements and traverses them so,
       that every stroke has exactly two passes
    """
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)

        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-m", "--merge_distance", dest="merge_distance", type=float, default=0.5)

        self.elements = None
        self.graph = None
        self.edge_groups = None
        self.sorted_group = None
        self.merge_distance = None

    def effect(self):
        if not self.get_elements():
            return

        elements = [element for element in self.elements if isinstance(element, Stroke)]
        if not elements:
            errormsg(_("Please select one or more strokes."))
            return

        self.merge_distance = self.options.merge_distance * PIXELS_PER_MM
        starting_point = self._get_starting_point('run_start')

        multi_line_string = self._elements_to_multi_line_string(elements)
        if starting_point:
            multi_line_string = self._ensure_starting_point(multi_line_string, starting_point)
        self._build_graph(multi_line_string)
        self._generate_edge_groups()
        self._sort_edge_groups()
        self._edge_groups_to_elements(elements)

    def _ensure_starting_point(self, multi_line_string, starting_point):
        starting_point = Point(*starting_point)
        new_lines = []
        start_applied = False
        for line in multi_line_string.geoms:
            if line.distance(starting_point) < 2 and not start_applied:
                project = line.project(starting_point, True)
                new_lines.append(substring(line, 0, project, True))
                new_lines = [substring(line, project, 1, True)] + new_lines
                start_applied = True
            else:
                new_lines.append(line)
        return MultiLineString(new_lines)

    def _get_starting_point(self, command_type):
        command = None
        for stroke in self.elements:
            command = stroke.get_command(command_type)
            if command:
                # remove command symbol
                command_group = command.connector.getparent()
                command_group.getparent().remove(command_group)
                # return the first occurence directly
                return command.target_point

    def _edge_groups_to_elements(self, elements):
        # get node style and transform information
        node = elements[0].node
        index = node.getparent().index(node)
        style = node.style
        transform = get_correction_transform(node)

        # create redwork group
        redwork_group = Group()
        redwork_group.label = _("Redwork Group")
        node.getparent().insert(index, redwork_group)

        # insert lines grouped by underpath and top layer
        visited_lines = []
        path = ''
        underpath = True
        insert_path = False
        i = 1
        for edge in self.sorted_edges:
            # Split into underpath and normal path
            linestring = self.graph.get_edge_data(edge[0], edge[1], key=edge[2])['path']
            current_line = linestring
            if current_line in visited_lines:
                if underpath and path:
                    path_id = self.svg.get_unique_id('underpath_')
                    label = _("Redwork Underpath") + f' {i}'
                    insert_path = True
                underpath = False
            else:
                if not underpath and path:
                    path_id = self.svg.get_unique_id('redwork_')
                    label = _("Redwork") + f' {i}'
                    insert_path = True
                underpath = True
                visited_lines.append(current_line)

            if insert_path:
                self._insert_element(path, redwork_group, style, transform, label, path_id)
                path = ''
                i += 1
                insert_path = False

            # add edge to path
            if edge[3] == 'reverse':
                linestring = linestring.reverse()
            path += str(Path(list(linestring.coords)))

        # add last top layer line
        if path:
            path_id = self.svg.get_unique_id('redwork_')
            label = _("Redwork") + f' {i}'
            self._insert_element(path, redwork_group, style, transform, label, path_id)

        # remove input elements
        for element in elements:
            element.node.getparent().remove(element.node)

    def _insert_element(self, path, group, style, transform, label, path_id):
        element = PathElement(
            id=path_id,
            style=str(style),
            transform=transform,
            d=path
        )
        element.label = label
        group.add(element)

    def _build_graph(self, multi_line_string):
        self.graph = nx.MultiDiGraph()

        for geom in multi_line_string.geoms:
            start = geom.coords[0]
            end = geom.coords[-1]

            self.graph.add_edge(str(start), str(end), path=geom)
            self.graph.add_edge(str(start), str(end), path=geom)

    def _generate_edge_groups(self):
        # edge_dfs traverses all edges, however, it doesn't sort them as we need it
        # so let's create groups of connected edges and see if we can combine them later on
        self.edge_groups = []
        edge_group = []
        prev_edge = None
        for edge in nx.edge_dfs(self.graph, orientation="ignore"):
            start = edge[0] if edge[3] == 'forward' else edge[1]
            end = edge[1] if edge[3] == 'forward' else edge[0]
            if prev_edge is None or start == prev_edge:
                edge_group.append(edge)
            else:
                self.edge_groups.append(edge_group)
                edge_group = [edge]
            # set previous edge
            prev_edge = end
        self.edge_groups.append(edge_group)

    def _sort_edge_groups(self):
        # connect groups if possible
        self.sorted_edges = []
        self.used_edge_groups = []
        for i, edge_group in enumerate(self.edge_groups):
            if i in self.used_edge_groups:
                continue
            self.used_edge_groups.append(i)
            for edge in edge_group:
                self.add_recursive_edges(edge)

    def add_recursive_edges(self, edge):
        self.sorted_edges.append(edge)
        end = edge[1] if edge[3] == 'forward' else edge[0]
        if len(self.graph.out_edges(end)) + len(self.graph.in_edges(end)) < 2:
            return
        for j, edge_group in enumerate(self.edge_groups):
            if j in self.used_edge_groups:
                continue
            # Find connected edge
            connected_edge = None
            for edg in edge_group:
                if edg[3] == 'forward' and edg[0] == end:
                    connected_edge = edg
                    break
                elif edg[3] == 'reverse' and edg[1] == end:
                    connected_edge = edg
                    break
            # insert edge group
            if connected_edge:
                self.used_edge_groups.append(j)
                index = edge_group.index(connected_edge)
                sorted_group = edge_group[index:] + edge_group[:index]
                for edge in sorted_group:
                    self.add_recursive_edges(edge)

    def _elements_to_multi_line_string(self, elements):
        lines = []
        for element in elements:
            for geom in element.as_multi_line_string().geoms:
                lines.append(geom)
        multi_line_string = self._add_connectors(lines)
        multi_line_string = ensure_multi_line_string(unary_union(linemerge(multi_line_string), grid_size=0.001))
        return multi_line_string

    def _add_connectors(self, lines):
        connectors = []
        for i, line1 in enumerate(lines):
            for j in range(i + 1, len(lines)):
                line2 = lines[j]
                try:
                    distance = line1.distance(line2)
                except FloatingPointError:
                    continue
                if 0 < distance < self.merge_distance:
                    # add nearest points
                    near = nearest_points(line1, line2)
                    connectors.append(LineString([near[0], near[1]]))
        return MultiLineString(lines + connectors)
