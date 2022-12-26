# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, Group, PathElement, errormsg
from inkex.units import convert_unit
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon
from shapely.ops import linemerge, split, voronoi_diagram

from ..elements import FillStitch, Stroke
from ..i18n import _
from ..stitches.running_stitch import running_stitch
from ..svg import get_correction_transform
from ..utils.geometry import line_string_to_point_list
from .base import InkstitchExtension


class FillToStroke(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--options", dest="options", type=str, default="")
        self.arg_parser.add_argument("--info", dest="help", type=str, default="")
        self.arg_parser.add_argument("-t", "--threshold", dest="threshold", type=int, default=10)
        self.arg_parser.add_argument("-o", "--keep_original", dest="keep_original", type=Boolean, default=False)
        self.arg_parser.add_argument("-d", "--dashed_line", dest="dashed_line", type=Boolean, default=True)
        self.arg_parser.add_argument("-w", "--line_width", dest="line_width", type=float, default=1)

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            errormsg(_("Please select one or more fill objects to render the centerline."))
            return

        cut_lines = []
        fill_shapes = []

        fill_shapes, cut_lines = self._get_shapes()

        if not fill_shapes:
            errormsg(_("Please select one or more fill objects to render the centerline."))
            return

        # insert centerline group before the first selected element
        first = fill_shapes[0].node
        parent = first.getparent()
        index = parent.index(first) + 1
        centerline_group = Group.new("Centerline Group", id=self.uniqueId("centerline_group_"))
        parent.insert(index, centerline_group)
        transform = get_correction_transform(first)

        for element in fill_shapes:
            transform = element.node.transform @ transform
            dashed = "stroke-dasharray:12,1.5;" if self.options.dashed_line else ""
            stroke_width = convert_unit(self.options.line_width, self.svg.unit)
            color = element.node.style('fill')
            style = "fill:none;stroke:%s;stroke-width:%s;%s" % (color, stroke_width, dashed)

            multipolygon = element.shape
            for cut_line in cut_lines:
                split_polygon = split(multipolygon, cut_line)
                poly = [polygon for polygon in split_polygon.geoms if isinstance(polygon, Polygon)]
                multipolygon = MultiPolygon(poly)

            for polygon in multipolygon.geoms:
                multilinestring = self._get_centerline(polygon)
                if multilinestring is None:
                    continue

                # insert new elements
                self._insert_elements(multilinestring, centerline_group, index, transform, style)

        # clean up
        if not self.options.keep_original:
            self._remove_elements()

    def _get_shapes(self):
        fill_shapes = []
        cut_lines = []
        for element in self.elements:
            if isinstance(element, FillStitch):
                fill_shapes.append(element)
            elif isinstance(element, Stroke):
                cut_lines.extend(list(element.as_multi_line_string().geoms))
        return fill_shapes, cut_lines

    def _remove_elements(self):
        for element in self.elements:
            # it is possible, that we get one element twice (if it has both, a fill and a stroke)
            # just ignore the second time
            try:
                element.node.getparent().remove(element.node)
            except AttributeError:
                pass

    def _get_high_res_polygon(self, polygon):
        # use running stitch method
        runs = [running_stitch(line_string_to_point_list(polygon.exterior), 1, 0.1)]
        if len(runs[0]) < 3:
            return
        for interior in polygon.interiors:
            runs.append(running_stitch(line_string_to_point_list(interior), 1, 0.1))
        return MultiPolygon([(runs[0], runs[1:])])

    def _get_centerline(self, polygon):
        # increase the resolution of the polygon
        polygon = self._get_high_res_polygon(polygon)
        if polygon is isinstance(polygon, MultiPolygon):
            return

        # generate voronoi centerline
        multilinestring = self._get_voronoi_centerline(polygon)
        if multilinestring is None:
            return
        # dead ends
        dead_ends = self._get_dead_end_lines(multilinestring)
        # avoid the splitting of line ends
        multilinestring = self._repair_splitted_ends(polygon, multilinestring, dead_ends)
        # update dead ends
        dead_ends = self._get_dead_end_lines(multilinestring)
        # filter small dead ends
        multilinestring = self._filter_short_dead_ends(multilinestring, dead_ends)
        if multilinestring is None:
            return
        # simplify polygon
        multilinestring = self._ensure_multilinestring(multilinestring.simplify(0.1))
        if multilinestring is None:
            return
        return multilinestring

    def _get_voronoi_centerline(self, polygon):
        lines = voronoi_diagram(polygon, edges=True).geoms[0]
        if not isinstance(lines, MultiLineString):
            return
        multilinestring = []
        for line in lines.geoms:
            if polygon.covers(line):
                multilinestring.append(line)
        lines = linemerge(multilinestring)
        if lines.is_empty:
            return
        return self._ensure_multilinestring(lines)

    def _get_start_and_end_points(self, multilinestring):
        points = []
        for line in multilinestring.geoms:
            points.extend(line.coords[::len(line.coords)-1])
        return points

    def _get_dead_end_lines(self, multilinestring):
        start_and_end_points = self._get_start_and_end_points(multilinestring)
        dead_ends = []
        for line in multilinestring.geoms:
            num_neighbours_start = start_and_end_points.count(line.coords[0]) - 1
            num_neighbours_end = start_and_end_points.count(line.coords[-1]) - 1
            if num_neighbours_start == 0 or num_neighbours_end == 0:
                dead_ends.append(line)
        return dead_ends

    def _filter_short_dead_ends(self, multilinestring, dead_ends):
        lines = list(multilinestring.geoms)
        for i, line in enumerate(multilinestring.geoms):
            if line in dead_ends and line.length < self.options.threshold:
                lines.remove(line)
        lines = linemerge(lines)
        if lines.is_empty:
            lines = None
        else:
            lines = self._ensure_multilinestring(lines)
        return lines

    def _repair_splitted_ends(self, polygon, multilinestring, dead_ends):
        lines = list(multilinestring.geoms)
        for i, dead_end in enumerate(dead_ends):
            coords = dead_end.coords
            for j in range(i + 1, len(dead_ends)):
                common_point = set([coords[0], coords[-1]]).intersection(dead_ends[j].coords)
                if len(common_point) > 0:
                    # prepare all lines to point to the common point
                    dead_point1 = coords[0]
                    if dead_point1 in common_point:
                        dead_point1 = coords[-1]
                    dead_point2 = dead_ends[j].coords[0]
                    if dead_point2 in common_point:
                        dead_point2 = dead_ends[j].coords[-1]
                    end_line = LineString([dead_point1, dead_point2])
                    if polygon.covers(end_line):
                        dead_end_center_point = end_line.centroid
                    else:
                        continue
                    lines.append(LineString([dead_end_center_point, list(common_point)[0]]))
                    if dead_end in lines:
                        lines.remove(dead_end)
                    if dead_ends[j] in lines:
                        lines.remove(dead_ends[j])
                    continue
        return self._ensure_multilinestring(linemerge(lines))

    def _ensure_multilinestring(self, lines):
        if not isinstance(lines, MultiLineString):
            lines = MultiLineString([lines])
        return lines

    def _insert_elements(self, lines, parent, index, transform, style):
        for line in lines.geoms:
            d = "M "
            for coord in line.coords:
                d += "%s,%s " % (coord[0], coord[1])
            centerline_element = PathElement(d=d, style=style, transform=str(transform))
            parent.insert(index, centerline_element)
