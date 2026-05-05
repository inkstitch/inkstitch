# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points

from ..commands import Command
from ..elements import SatinColumn, Stroke
from ..i18n import _
from ..svg import get_correction_transform
from ..utils import Point as InkstitchPoint
from .base import InkstitchExtension


class CutSatin(InkstitchExtension):
    """This extension splits a satin column at specified points

    The cut points can be specified by either one or multiple cut commands and/or selected strokes.
    Strokes must intersect with at least one rail. Combined stroke subpaths are handled individually.

    Strokes and command are removed by the extension."""
    def effect(self) -> None:
        if not self.get_elements():
            return

        if not self.svg.selection or not any([isinstance(element, SatinColumn) for element in self.elements]):
            inkex.errormsg(_("Please select one or more satin columns to cut."))
            return

        cut_lines, cut_line_nodes, satin_elements = self._select_elements()
        self._split_satin(satin_elements, cut_lines)

        # delete selected strokes
        for element in cut_line_nodes:
            element.delete()

    def _split_satin(self, satin_elements, split_elements) -> list[SatinColumn]:
        new_satins = []
        for satin in satin_elements:
            old_satin = satin
            self.split = False
            transform = get_correction_transform(satin.node)
            parent = satin.node.getparent()
            self.index = parent.index(satin.node)
            self.label_index = 0

            # collect cut points from split lines and commands (there must be at least one point)
            cut_point_list = self._get_cut_points(satin, split_elements)
            commands = satin.get_commands("satin_cut_point")
            cut_point_list.extend([[Point(point.target_point)] for point in commands])
            # sort cut points according to their distance on the first rail of the satin
            first_rail = satin.line_string_rails[0]
            cut_point_list.sort(key=lambda points: first_rail.project(nearest_points(points[0], first_rail)[0]), reverse=True)

            satins = [None, None]
            for cut_points in cut_point_list:
                if len(cut_points) == 1:
                    point = list(cut_points[0].coords)[0]
                    satins = satin.split(InkstitchPoint(point[0], point[1]))
                else:
                    satins = satin.split(None, cut_points)
                if None in satins:
                    continue
                self.insert_satin(satins[1], parent, transform)
                new_satins.append(satins[1])
                satin = satins[0]
            if satins[0] is not None:
                self.insert_satin(satins[0], parent, transform)
                new_satins.append(satins[0])

            if self.split:
                old_satin.node.delete()
                self._remove_commands(commands)

        if new_satins:
            return new_satins
        return satin_elements

    def _get_cut_points(self, satin: SatinColumn, cut_lines: list[LineString]) -> list[tuple[Point, Point]]:
        """Cut lines must intersect each rail once
        This filters cut lines and returns the cut points"""
        rails = satin.line_string_rails
        filtered_cut_points = []
        for cut_line in cut_lines:
            cut_points = []
            cut_point1 = rails[0].intersection(cut_line)
            if cut_point1.geom_type == "Point":
                cut_points.append(cut_point1)
            cut_point2 = rails[1].intersection(cut_line)
            if cut_point2.geom_type == "Point":
                cut_points.append(cut_point2)
            if len(cut_points) > 0:
                filtered_cut_points.append(tuple(cut_points))
        return filtered_cut_points

    def _select_elements(self) -> tuple[list[LineString], list[inkex.BaseElement], list[SatinColumn]]:
        satins = []
        cut_lines = []
        cut_line_nodes = []
        for element in self.elements:
            if isinstance(element, SatinColumn):
                satins.append(element)
            elif isinstance(element, Stroke):
                cut_line_nodes.append(element.node)
                cut_lines.extend(list(element.as_multi_line_string().geoms))
        return cut_lines, cut_line_nodes, satins

    def insert_satin(self, satin: SatinColumn, parent: inkex.BaseElement, transform: str) -> None:
        if satin is None:
            return
        node = satin.node
        label = node.label or satin.node.get_id()
        node.set('transform', transform)
        parent.insert(self.index, node)
        node.set('inkscape:label', f'{label} {self.label_index}')
        node.apply_transform()
        self.label_index += 1
        self.split = True

    def _remove_commands(self, commands: list[Command]) -> None:
        for command in commands:
            command_group = command.use.getparent()
            if command_group is not None and command_group.get('id').startswith('command_group'):
                command_group.delete()
            else:
                command.use.delete()
                command.connector.delete()
