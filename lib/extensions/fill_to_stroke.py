# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, Group, Path, PathElement, Transform, errormsg
from inkex.units import convert_unit
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point
from shapely.ops import linemerge, nearest_points, split, voronoi_diagram

from ..elements import FillStitch, Stroke
from ..i18n import _
from ..stitches.running_stitch import running_stitch
from ..svg import get_correction_transform
from ..utils import ensure_multi_line_string
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import line_string_to_point_list
from .base import InkstitchExtension


class FillToStroke(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--options", dest="options", type=str, default="")
        self.arg_parser.add_argument("--info", dest="help", type=str, default="")
        self.arg_parser.add_argument("-t", "--threshold_mm", dest="threshold_mm", type=float, default=10)
        self.arg_parser.add_argument("-o", "--keep_original", dest="keep_original", type=Boolean, default=False)
        self.arg_parser.add_argument("-w", "--line_width_mm", dest="line_width_mm", type=float, default=1)
        self.arg_parser.add_argument("-g", "--close_gaps", dest="close_gaps", type=Boolean, default=False)

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

        # convert user input from mm to px
        self.threshold = convert_unit(self.options.threshold_mm, 'px', 'mm')

        # insert centerline group before the first selected element
        first = fill_shapes[0].node
        parent = first.getparent()
        index = parent.index(first) + 1
        centerline_group = Group.new("Centerline Group", id=self.uniqueId("centerline_group_"))
        parent.insert(index, centerline_group)

        for element in fill_shapes:
            transform = Transform(get_correction_transform(parent, child=True))
            stroke_width = convert_unit(self.options.line_width_mm, 'px', 'mm')
            color = element.node.style('fill')
            style = f"fill:none;stroke:{ color };stroke-width:{ stroke_width }"

            multipolygon = element.shape
            for cut_line in cut_lines:
                split_polygon = split(multipolygon, cut_line)
                poly = [polygon for polygon in split_polygon.geoms if polygon.geom_type == 'Polygon']
                multipolygon = MultiPolygon(poly)

            lines = []

            for polygon in multipolygon.geoms:
                if polygon.area < 0.5:
                    continue
                multilinestring = self._get_centerline(polygon)
                if multilinestring is None:
                    continue
                lines.extend(multilinestring.geoms)

            if self.options.close_gaps:
                lines = self._close_gaps(lines, cut_lines)

            # insert new elements
            self._insert_elements(lines, centerline_group, index, transform, style)

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
        parents = []
        for element in self.elements:
            # it is possible, that we get one element twice (if it has both, a fill and a stroke)
            # just ignore the second time
            try:
                parents.append(element.node.getparent())
                element.node.getparent().remove(element.node)
            except AttributeError:
                pass
        # remove empty groups
        for parent in set(parents):
            if parent is not None and not parent.getchildren():
                parent.getparent().remove(parent)

    def _get_high_res_polygon(self, polygon):
        # use running stitch method
        runs = [running_stitch(line_string_to_point_list(polygon.exterior), 1, 0.1)]
        if len(runs[0]) < 3:
            return
        for interior in polygon.interiors:
            shape = running_stitch(line_string_to_point_list(interior), 1, 0.1)
            if len(shape) >= 3:
                runs.append(shape)
        return MultiPolygon([(runs[0], runs[1:])])

    def _get_centerline(self, polygon):
        # increase the resolution of the polygon
        polygon = self._get_high_res_polygon(polygon)
        if polygon is polygon.geom_type == 'MultiPolygon':
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
        multilinestring = ensure_multi_line_string(multilinestring.simplify(0.1))
        if multilinestring is None:
            return
        return multilinestring

    def _get_voronoi_centerline(self, polygon):
        lines = voronoi_diagram(polygon, edges=True).geoms[0]
        if not lines.geom_type == 'MultiLineString':
            return
        multilinestring = []
        for line in lines.geoms:
            if polygon.covers(line):
                multilinestring.append(line)
        lines = linemerge(multilinestring)
        if lines.is_empty:
            return
        return ensure_multi_line_string(lines)

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
            if line in dead_ends and line.length < self.threshold:
                lines.remove(line)
        lines = linemerge(lines)
        if lines.is_empty:
            lines = None
        else:
            lines = ensure_multi_line_string(lines)
        return lines

    def _repair_splitted_ends(self, polygon, multilinestring, dead_ends):
        lines = list(multilinestring.geoms)
        for i, dead_end in enumerate(dead_ends):
            if dead_end.length > self.threshold:
                continue
            self._join_end(polygon, lines, dead_ends, dead_end, i)
        return ensure_multi_line_string(linemerge(lines))

    def _join_end(self, polygon, lines, dead_ends, dead_end, index):
        coords = dead_end.coords
        for j in range(index + 1, len(dead_ends)):
            if dead_ends[j].length > self.threshold:
                continue
            common_point = set([coords[0], coords[-1]]).intersection(dead_ends[j].coords)
            if len(common_point) > 0:
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

    def _close_gaps(self, lines, cut_lines):
        snaped_lines = []
        lines = MultiLineString(lines)
        for i, line in enumerate(lines.geoms):
            # for each cutline check if a line starts or ends close to it
            # if so extend the line at the start/end for the distance of the nearest point and snap it to that other line
            # we do not want to snap it to the rest of the lines directly, this could push the connection point into an unwanted direction
            coords = list(line.coords)
            start = Point(coords[0])
            end = Point(coords[-1])
            l_l = lines.difference(line)
            for cut_line in cut_lines:
                distance = start.distance(l_l)
                if cut_line.distance(start) < 0.6:
                    distance = start.distance(l_l)
                    new_start_point = self._extend_line(line.coords[0], line.coords[1], distance)
                    coords[0] = nearest_points(Point(list(new_start_point)), l_l)[1]
                if cut_line.distance(end) < 0.6:
                    distance = end.distance(l_l)
                    new_end_point = self._extend_line(line.coords[-1], line.coords[-2], distance)
                    coords[-1] = nearest_points(Point(list(new_end_point)), l_l)[1]
            snaped_lines.append(LineString(coords))
        return snaped_lines

    def _extend_line(self, p1, p2, distance):
        start_point = InkstitchPoint.from_tuple(p1)
        end_point = InkstitchPoint.from_tuple(p2)
        direction = (end_point - start_point).unit()
        new_point = start_point - direction * distance
        return new_point

    def _insert_elements(self, lines, parent, index, transform, style):
        for line in lines:
            centerline_element = PathElement(
                d=str(Path(line.coords)),
                style=style,
                transform=str(transform)
            )
            parent.insert(index, centerline_element)
