# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import deepcopy
from math import floor

import inkex
import numpy as np
from inkex import Circle, Path, bezier, errormsg
from shapely import (LineString, MultiLineString, MultiPoint, MultiPolygon,
                     Point, Polygon)

from ..i18n import _
from .base import InkstitchExtension
from shapely.ops import substring


class Rhinestone(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--method", type=str, default="flexible", dest="method")
        self.arg_parser.add_argument("--size", type=float, default="4", dest="size")
        self.arg_parser.add_argument("--x_distance", type=float, default="0.5", dest="x_distance")
        self.arg_parser.add_argument("--y_distance", type=float, default="0.5", dest="y_distance")
        self.arg_parser.add_argument("--offset", type=float, default="50", dest="offset")
        self.arg_parser.add_argument("--color", type=inkex.Color, default=inkex.Color(0x808080FF), dest="color")
        self.arg_parser.add_argument("--stroke_width", type=float, default="0.264", dest="stroke_width")
        self.arg_parser.add_argument("--spacing_method", type=str, default="strict", dest="spacing_method")

    def effect(self):
        if not self.svg.selection:
            errormsg(_("Please select at least one element."))
            return

        self.method = self.options.method
        self.size = self.options.size
        self.x_distance = self.options.x_distance
        self.y_distance = self.options.y_distance
        self.offset = self.options.offset
        self.offset = (self.offset * (self.size + self.x_distance)) / 100
        self.stroke_color = self.options.color
        self.stroke_width = self.options.stroke_width
        self.spacing_method = self.options.spacing_method

        # option flat
        for element in self.svg.selection:
            # TODO: filter groups
            bbox = element.bounding_box()

            shape = Path(element.get_path())
            shape = deepcopy(shape)
            shape = shape.transform(element.composed_transform()).to_superpath()
            bezier.cspsubdiv(shape, 0.1)
            shape = [self.strip_control_points(subpath) for subpath in shape]
            if self.method in ("outline"):
                shape = MultiLineString(shape)
            else:
                shape.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
                if not shape:
                    return
                shape = MultiPolygon([(shape[0], shape[1:])])

            if self.method == "line_offset":
                points = self.line_offset(shape, bbox)
            elif self.method == "outline":
                points = self.outline(shape, bbox)
            elif self.method == "flexible":
                points = self.flexible(shape, bbox)
            else:
                return

            for point in points.geoms:
                circle = Circle(attrib={
                    'style': f"fill: none; stroke: { self.stroke_color }; stroke-width: { str(self.stroke_width) };",
                    'cx': "%s" % point.x,
                    'cy': "%s" % point.y,
                    'r': str(self.size / 2)
                })
                element.getparent().add(circle)

    def outline(self, shape, bbox):
        points = []
        distance = self.size + self.x_distance
        for line in shape.geoms:
            current = 0
            if self.spacing_method == "distribute":
                num_points = floor(line.length / distance)
                distance += (line.length - (num_points * distance - self.x_distance)) / num_points
            while line.length >= current + self.size / 2 + self.x_distance:
                point = line.interpolate(current)
                points.append(point)
                current += distance
        return MultiPoint(points)

    def line_offset(self, shape, bbox):
        min_x, min_y = bbox.minimum
        max_x, max_y = bbox.maximum

        # generate mesh
        xx, yy = np.meshgrid(
            np.arange(min_x - self.size / 2, max_x + self.x_distance, self.size + self.x_distance),
            np.arange(min_y - self.size / 2, max_y + self.y_distance, self.size + self.y_distance)
        )

        # offset every second line
        offset_x = []
        for i, x_coords in enumerate(xx):
            if i % 2 == 0:
                offset_x.extend(x_coords)
            else:
                offset_x.extend(x_coords + self.offset)

        points = MultiPoint(list(zip(offset_x, yy.flatten())))

        # remove points which are outside the shape
        return points.intersection(shape)

    def flexible(self, shape, bbox):
        min_x, min_y = bbox.minimum
        max_x, max_y = bbox.maximum

        x_distance = self.size + self.x_distance
        y_distance = self.y_distance + self.size
        height = bbox.height - 0.2
        num_lines = floor(height / y_distance)
        y_distance = (height / num_lines)

        lines = []
        current_y = min_y + 0.1
        while current_y <= max_y + y_distance:
            lines.append(LineString([(min_x, current_y), (max_x, current_y)]))
            current_y += y_distance

        multiline = MultiLineString(lines)
        lines = multiline.intersection(shape)

        points = []
        for line in lines.geoms:
            import sys
            num_points = max(round(line.length / x_distance - 0.5), 1)
            # prevent overlapping on near by lines
            skip_first = False
            if points and points[-1].y == line.coords[0][1] and abs(points[-1].x - line.coords[0][0]) < x_distance:
                center_point = Point(LineString([points[-1], Point(line.coords[0])]).interpolate(0.5, normalized=True))
                del points[-1]
                points.append(center_point)
                skip_first = True
            if num_points < 2:
                # center out a single line point
                points.append(Point(line.interpolate(0.5, True)))
            else:
                if self.spacing_method == "strict":
                    # cut start and end from line when lines are longer than necessary
                    cut_length = (line.length - (x_distance * (num_points - 1))) / 2
                    line = substring(line, cut_length, line.length - cut_length)
                spaced_lines = np.linspace(line.coords[0], line.coords[-1], num_points)
                line_points = list(MultiPoint(spaced_lines).geoms)
                if skip_first:
                    line_points = line_points[1:]
                points.extend(line_points)

        return MultiPoint(points)

    def strip_control_points(self, subpath):
        return [point for control_before, point, control_after in subpath]
