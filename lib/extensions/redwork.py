# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from inkex import Boolean, Group, Path, PathElement, errormsg
from inkex.paths.lines import Line
from shapely import length, unary_union
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, nearest_points, substring

from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..svg.tags import SVG_GROUP_TAG
from ..utils.geometry import ensure_multi_line_string
from .base import InkstitchExtension


class Redwork(InkstitchExtension):
    """Takes a bunch of stroke elements and traverses them so,
       that every stroke has exactly two passes
    """
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)

        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-c", "--combine", dest="combine", type=Boolean, default=False)
        self.arg_parser.add_argument("-m", "--merge_distance", dest="merge_distance", type=float, default=0.5)
        self.arg_parser.add_argument("-p", "--minimum_path_length", dest="minimum_path_length", type=float, default=0.5)
        self.arg_parser.add_argument("-s", "--redwork_running_stitch_length_mm", dest="redwork_running_stitch_length_mm", type=float, default=2.5)
        self.arg_parser.add_argument("-b", "--redwork_bean_stitch_repeats", dest="redwork_bean_stitch_repeats", type=str, default='0')
        self.arg_parser.add_argument("-k", "--keep_originals", dest="keep_originals", type=Boolean, default=False)

        self.elements = None
        self.graph = None
        self.connected_components = None
        self.merge_distance = None
        self.minimum_path_length = None

    def effect(self):
        no_selection_message = _("Please select one or more strokes.")
        if not self.svg.selection:
            errormsg(no_selection_message)
            return
        if not self.get_elements():
            errormsg(no_selection_message)
            return
        elements = [element for element in self.elements if isinstance(element, Stroke)]
        if not elements:
            errormsg(no_selection_message)
            return

        self.merge_distance = self.options.merge_distance * PIXELS_PER_MM
        self.minimum_path_length = self.options.minimum_path_length * PIXELS_PER_MM

        starting_point = self._get_starting_point('autoroute_start')
        # as the resulting path starts and ends at same place we can also use ending point
        if not starting_point:
            starting_point = self._get_starting_point('autoroute_end')

        multi_line_string = self._elements_to_multi_line_string(elements)
        if starting_point:
            multi_line_string = self._ensure_starting_point(multi_line_string, starting_point)
        self._build_graph(multi_line_string)

        redwork_group = self._create_redwork_group()
        self._generate_strongly_connected_components()
        self._generate_eulerian_circuits()
        self._eulerian_circuits_to_elements(redwork_group, elements)

        if not self.options.keep_originals:
            self._delete_original_elements(elements)

    def _delete_original_elements(self, elements):
        # remove input elements
        for element in elements:
            element.node.delete()
        # remove empty groups
        for element in self.svg.selection:
            selected_groups = self.svg.selection.filter(Group)
            for group in selected_groups:
                groups_within_group = reversed(list(group.iterdescendants(SVG_GROUP_TAG)))
                for g in groups_within_group:
                    if len(g) == 0:
                        g.delete()
                if len(group) == 0:
                    group.delete()

    def _ensure_starting_point(self, multi_line_string, starting_point):
        # returns a MultiLineString whose first  LineString starts close to  starting_point
        starting_point = Point(*starting_point)
        new_lines = []
        start_applied = False
        for line in multi_line_string.geoms:
            if line.distance(starting_point) < 2 and not start_applied:
                project = line.project(starting_point, True)
                if project == 1:
                    new_lines = [line.reverse()] + new_lines
                elif project == 0:
                    new_lines = [line] + new_lines
                else:
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
                if command_group in self.svg.selection:
                    self.svg.selection.pop(command_group.get_id())
                command_group.delete()
                # return the first occurence directly
                return command.target_point

    def _create_redwork_group(self):
        node = self.svg.selection.rendering_order()[-1]
        parent = node.getparent()
        index = parent.index(node) + 1
        # create redwork group
        redwork_group = Group()
        redwork_group.label = _("Redwork Group")
        parent.insert(index, redwork_group)
        return redwork_group

    def _eulerian_circuits_to_elements(self, redwork_group, elements):
        combine_all = self.options.combine and self.options.redwork_bean_stitch_repeats == '0'
        node = elements[0].node

        transform = get_correction_transform(self.svg.selection.rendering_order()[-1], False)
        style = node.style
        # Fix up the stroke width
        stroke_width = elements[0].stroke_width
        style["stroke-width"] = self.svg.viewport_to_unit(stroke_width)

        # insert lines grouped by underpath and top layer
        visited_lines = []
        i = 1

        for circuit in self.eulerian_circuit:
            previous_element_type = False
            connected_group = Group()
            connected_group.label = _("Connected Group")
            if len(self.eulerian_circuit) > 1:
                redwork_group.insert(i, connected_group)
                group = connected_group
            else:
                group = redwork_group

            path = ''
            for edge in circuit:
                linestring = self.graph.get_edge_data(edge[0], edge[1], edge[2])['path']
                if length(linestring) < self.minimum_path_length:
                    continue

                if linestring in visited_lines:
                    redwork = True
                else:
                    redwork = False
                visited_lines.append(linestring.reverse())

                current_path = Path(list(linestring.coords))
                if not self.options.combine or (not combine_all and previous_element_type != redwork):
                    if path:
                        self._insert_element(i, path, group, style, transform, previous_element_type)
                        i += 1
                    path = str(current_path)
                else:
                    if path:
                        current_path[0] = Line(current_path[0].x, current_path[0].y)
                    path += str(current_path)
                previous_element_type = redwork
            if path:
                self._insert_element(i, path, group, style, transform, redwork)

    def _insert_element(self, index, path, group, style, transform, redwork=True):
        if redwork:
            path_id = self.svg.get_unique_id('redwork_')
            path_type = 'redwork-top'
            label = _("Redwork") + f' {index}'
        else:
            path_id = self.svg.get_unique_id('underpath_')
            path_type = 'redwork-underpath'
            label = _("Redwork Underpath") + f' {index}'

        element = PathElement(
            id=path_id,
            style=str(style),
            transform=transform,
            d=path
        )
        element.apply_transform()

        element.label = label
        element.set('inkstitch:running_stitch_length_mm', self.options.redwork_running_stitch_length_mm)
        element.set('inkstitch:path_type', path_type)

        if redwork:
            element.set('inkstitch:bean_stitch_repeats', self.options.redwork_bean_stitch_repeats)
            element.style['stroke-dasharray'] = 'none'
        else:
            element.style['stroke-dasharray'] = '2 1.1'

        group.add(element)

    def _build_graph(self, multi_line_string):
        self.graph = nx.MultiDiGraph()

        for geom in multi_line_string.geoms:
            start = geom.coords[0]
            end = geom.coords[-1]
            self.graph.add_edge(str(start), str(end), path=geom)
            geom = geom.reverse()
            self.graph.add_edge(str(end), str(start), path=geom)

    def _generate_strongly_connected_components(self):

        self.connected_components = list(nx.strongly_connected_components(self.graph))

        for i, cc in enumerate(self.connected_components):
            if list(self.graph.nodes)[0] in cc:
                break
        ordered_connected_components = [self.connected_components[i]] + self.connected_components[:i] + self.connected_components[i+1:]
        self.connected_components = ordered_connected_components

    def _generate_eulerian_circuits(self):
        G = self.graph.subgraph(self.connected_components[0]).copy()
        self.eulerian_circuit = [nx.eulerian_circuit(G, list(self.graph.nodes)[0], keys=True)]
        for c in self.connected_components[1:]:
            G = self.graph.subgraph(c).copy()
            self.eulerian_circuit.append(nx.eulerian_circuit(G, keys=True))

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
