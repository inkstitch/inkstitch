# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from .base import InkstitchExtension


class ZigzagLineToSatin(InkstitchExtension):
    """Convert a satin column into a running stitch."""
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--zigzag_to_satin", type=str, default=None)
        self.arg_parser.add_argument("--options", type=str, default=None)
        self.arg_parser.add_argument("--info", type=str, default=None)

        self.arg_parser.add_argument("-s", "--smoothing", type=inkex.Boolean, default=True, dest="smoothing")
        self.arg_parser.add_argument("-p", "--pattern", type=str, default="square", dest="pattern")
        self.arg_parser.add_argument("-r", "--rungs", type=inkex.Boolean, default=True, dest="rungs")
        self.arg_parser.add_argument("-l", "--reduce-rungs", type=inkex.Boolean, default=False, dest="reduce_rungs")

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            inkex.errormsg(_("Please select at least one stroke to convert to a satin column."))
            return

        for node in self.svg.selection:
            d = []
            point_list = list(node.get_path().end_points)
            # find duplicated nodes (= do not smooth)
            point_list, sharp_edges = self._get_sharp_edge_nodes(point_list)
            rails, rungs = self._get_rails_and_rungs(point_list)

            if not self.options.smoothing:
                for rail in rails:
                    d.append('M ' + ' '.join([str(point) for point in rail]))
            else:
                rails, rungs = self._smooth_path(rails, rungs, sharp_edges)
                d.append(rails)

            if self.options.rungs:
                if self.options.pattern != 'zigzag' and self.options.reduce_rungs and len(rungs) > 2:
                    rungs = rungs[0::2]
                d.extend(self._rung_path(rungs))

            node.set('d', " ".join(d))
            node.set('inkstitch:satin_column', True)

    def _get_sharp_edge_nodes(self, point_list):
        points = []
        sharp_edges = []
        skip = False
        for p0, p1 in zip(point_list[:-1], point_list[1:]):
            if skip is True:
                skip = False
                continue
            points.append(p0)
            if inkex.DirectedLineSegment(p0, p1).length < 0.3:
                sharp_edges.append(p0)
                skip = True
        points.append(p1)
        return points, sharp_edges

    def _get_rails_and_rungs(self, point_list):
        if self.options.pattern == "sawtooth":
            # sawtooth pattern: |/|/|/|
            rails = [point_list[0::2], point_list[1::2]]
            rungs = list(zip(point_list[1::2], point_list[:-1:2]))
            return rails, rungs
        elif self.options.pattern == "zigzag":
            # zigzag pattern: VVVVV
            rails = [point_list[0::2], point_list[1::2]]
            rail_points = [[], []]
            rung_points = [[], []]
            for i, rail in enumerate(rails):
                for j, point in enumerate(rail):
                    if j == 0 or point in point_list[2::len(point_list)-3]:
                        rail_points[i].append(point)
                        rung_points[i].append(point)
                        continue
                    p0 = rail[j-1]
                    rail_points[i].append(point)
                    rung_points[i].append(inkex.Vector2d(inkex.DirectedLineSegment(p0, point).point_at_ratio(0.5)))
                    rung_points[i].append(point)
            rungs = list(zip(*rung_points))
            return rail_points, rungs
        else:
            # square pattern: |_|▔|_|▔|
            point_list = [point_list[i:i+4] for i in range(0, len(point_list), 4)]

            rungs = []
            rails = [[], []]
            for i, points in enumerate(point_list):
                if len(points) <= 1:
                    break

                elif len(points) < 4 and len(points) > 1:
                    rails[0].append(points[0])
                    rails[1].append(points[1])
                    rungs.append([points[0], points[1]])
                    break

                rails[0].extend([points[0], points[3]])
                rails[1].extend([points[1], points[2]])
                rungs.extend([[points[0], points[1]], [points[2], points[3]]])
            return rails, rungs

    def _smooth_path(self, rails, rungs, sharp_edges):  # noqa: C901
        path_commands = []
        new_rungs = []
        k = [1, 0]
        smoothing = 0.4
        has_equal_rail_point_count = len(rails[0]) == len(rails[1])
        for j, rail in enumerate(rails):
            r = rungs[j:len(rungs):2]
            for i, point in enumerate(rail):
                if i == 0:
                    path_commands.append(inkex.paths.Move(*point))
                else:
                    # get the two previous points and the next point for handle calculation
                    if i < 2:
                        prev_prev = rail[i - 1]
                    else:
                        prev_prev = rail[i-2]

                    prev = rail[i-1]

                    if i > len(rail) - 2:
                        next = point
                    else:
                        next = rail[i+1]

                    # get length of handles
                    length = inkex.DirectedLineSegment(point, prev).length * smoothing

                    # get start handle positions
                    start = inkex.DirectedLineSegment(prev_prev, point)
                    if prev in sharp_edges:
                        start = prev
                    elif not start.length == 0:
                        start = start.parallel(*prev).point_at_length(start.length - length)
                    else:
                        start = start.start

                    # get end handle positions
                    end = inkex.DirectedLineSegment(next, prev)
                    if point in sharp_edges:
                        end = point
                    elif not end.length == 0:
                        end = end.parallel(*point).point_at_length(end.length - length)
                    else:
                        end = end.start

                    # generate curves
                    path_commands.append(inkex.paths.Curve(*start, *end, *point))

                    # recalculate rungs for zigzag pattern
                    if self.options.pattern == 'zigzag' and (has_equal_rail_point_count or i <= len(r)) and (not self.options.reduce_rungs or j == 0):
                        # in zigzag mode we do have alternating points on rails
                        # when smoothing them out, rungs may not intersect anymore
                        # so we need to find a spot on the smoothed rail to ensure the correct length
                        rung = r[i-1]
                        line = inkex.DirectedLineSegment(rung[0], rung[1])
                        point0 = line.point_at_length(-50)
                        point1 = line.point_at_length(line.length + 50)
                        new_point = inkex.bezier.linebezierintersect((point0, point1), [prev, start, end, point])
                        if new_point:
                            new_rungs.append((rung[k[j]], new_point[0]))
                        else:
                            new_rungs.append(rung)

        rungs = self._update_rungs(new_rungs, rungs, r, has_equal_rail_point_count)
        return str(inkex.Path(path_commands)), rungs

    def _update_rungs(self, new_rungs, rungs, r, has_equal_rail_point_count):
        if self.options.pattern == 'zigzag':
            rungs = new_rungs
            if not has_equal_rail_point_count and not self.options.reduce_rungs:
                # make sure, that the last rail on canvas is also the last rail in the list
                # this important when we delete the very first and very last rung
                count = len(r)
                rungs[count], rungs[-1] = rungs[-1], rungs[count]
        return rungs

    def _rung_path(self, rungs):
        if len(rungs) < 3:
            return []
        d = []
        rungs = rungs[1:-1]
        for point0, point1 in rungs:
            line = inkex.DirectedLineSegment(point0, point1)
            point0 = line.point_at_length(-0.8)
            point1 = line.point_at_length(line.length + 0.8)
            d.append(f'M {point0[0]}, {point0[1]} {point1[0]}, {point1[1]}')
        return d
