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
        self.connected_components = None
        self.eulerian_circuits = None
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
        ## as the resulting path starts and ends at same place we can also use ending point
        if not starting_point:
            starting_point = self._get_starting_point('run_end')

        multi_line_string = self._elements_to_multi_line_string(elements)
        if starting_point:
            multi_line_string = self._ensure_starting_point(multi_line_string, starting_point)
        self._build_graph(multi_line_string)

        self._generate_strongly_connected_components()
        self._generate_eulerian_circuits()
        self._eulerian_circuits_to_elements(elements)

    def _ensure_starting_point(self, multi_line_string, starting_point):
        # returns a MultiLineString whose first  LineString starts close to  starting_point
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

    def _eulerian_circuits_to_elements(self, elements):

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
        i = 1
     
        for circuit in self.eulerian_circuit:
            connected_group = Group()
            connected_group.label = _("Connected Group")
           
            for edge in circuit:
                linestring = self.graph.get_edge_data(edge[0], edge[1], edge[2])['path']
                current_line = linestring
                if current_line in visited_lines:
                    path_id = self.svg.get_unique_id('redwork_')
                    label = _("Redwork") + f' {i}'

                else:
                    path_id = self.svg.get_unique_id('underpath_')
                    label = _("Redwork Underpath") + f' {i}'
                    visited_lines.append(current_line.reverse())

                path = str(Path(list(current_line.coords)))
                if len(self.eulerian_circuit) > 1:
                    redwork_group.insert(i, connected_group)
                    self._insert_element(path, connected_group, style, transform, label, path_id)
                else:
                   self._insert_element(path, redwork_group, style, transform, label, path_id) 

                i += 1

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
