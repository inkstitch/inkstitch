# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import atan2, degrees

import inkex
from lxml import etree
from shapely.geometry import LineString, MultiPoint, Point
from shapely.ops import split

from ..elements import Stroke
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG, INKSCAPE_LABEL
from .base import InkstitchExtension


class CutworkTiling(InkstitchExtension):
    '''
    This will split up stroke elements according to their direction. This is useful for cutwork.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-as", "--a_start", type=int, default=0, dest="a_start")
        self.arg_parser.add_argument("-ae", "--a_end", type=int, default=0, dest="a_end")
        self.arg_parser.add_argument("-ac", "--a_color", type=inkex.Color, default=inkex.Color(0x808080FF), dest="a_color")
        self.arg_parser.add_argument("-bs", "--b_start", type=int, default=0, dest="b_start")
        self.arg_parser.add_argument("-be", "--b_end", type=int, default=0, dest="b_end")
        self.arg_parser.add_argument("-bc", "--b_color", type=inkex.Color, default=inkex.Color(0x808080FF), dest="b_color")
        self.arg_parser.add_argument("-cs", "--c_start", type=int, default=0, dest="c_start")
        self.arg_parser.add_argument("-ce", "--c_end", type=int, default=0, dest="c_end")
        self.arg_parser.add_argument("-cc", "--c_color", type=inkex.Color, default=inkex.Color(0x808080FF), dest="c_color")
        self.arg_parser.add_argument("-ds", "--d_start", type=int, default=0, dest="d_start")
        self.arg_parser.add_argument("-de", "--d_end", type=int, default=0, dest="d_end")
        self.arg_parser.add_argument("-dc", "--d_color", type=inkex.Color, default=inkex.Color(0x808080FF), dest="d_color")
        self.arg_parser.add_argument("-s", "--sort_by_color", type=inkex.Boolean, default=True, dest="sort_by_color")
        self.arg_parser.add_argument("-k", "--keep_original", type=inkex.Boolean, default=False, dest="keep_original")

    def effect(self):
        self.sectors = []
        self.sectors.append([self.options.a_start, self.options.a_end, self.options.a_color, 1])
        self.sectors.append([self.options.b_start, self.options.b_end, self.options.b_color, 2])
        self.sectors.append([self.options.c_start, self.options.c_end, self.options.c_color, 3])
        self.sectors.append([self.options.d_start, self.options.d_end, self.options.d_color, 4])

        if not self.svg.selected:
            inkex.errormsg(_("Please select one or more stroke elements."))
            return

        if not self.get_elements():
            return

        self.new_elements = []
        for element in self.elements:
            if isinstance(element, Stroke):

                # save parent and index to be able to position and insert new elements later on
                parent = element.node.getparent()
                index = parent.index(element.node)

                for path in element.paths:
                    points = []
                    linestring = LineString(path)
                    prev_point = None
                    current_sector = None

                    # collect the split points by angle sections and apply them to each path (split)
                    for point in linestring.coords:
                        point = Point(*point)
                        if prev_point is None:
                            prev_point = point
                            continue

                        angle = self._get_angle(point, prev_point)
                        if current_sector:
                            if not self._in_sector(angle, current_sector):
                                points.append(prev_point)
                                current_sector = self._get_sector(angle)
                        else:
                            current_sector = self._get_sector(angle)

                        prev_point = point

                    lines = self.split_line(linestring, points)
                    self._prepare_line_elements(element, lines)

                self._remove_originals(parent, element.node)

        self._insert_elements(parent, index)

    def split_line(self, line, points):
        return split(line, MultiPoint(points))

    def _get_sector(self, angle):
        for sector in self.sectors:
            if self._in_sector(angle, sector):
                return sector

    def _in_sector(self, angle, sector):
        stop = sector[1] + 1
        if sector[0] > sector[1]:
            return angle in range(sector[0], 360) or angle in range(0, stop)
        else:
            return angle in range(sector[0], stop)

    def _get_angle(self, p1, p2):
        angle = round(degrees(atan2(p2.y - p1.y, p2.x - p1.x)) % 360)
        if angle > 180:
            angle -= 180
        return angle

    def _insert_elements(self, parent, index):
        if self.options.sort_by_color is True:
            self.new_elements = sorted(self.new_elements, key=lambda x: x[1])

        group = etree.Element("g", {
            INKSCAPE_LABEL: _("Cutwork Group"),
            "id": self.uniqueId("__inkstitch_cutwork_group__")
        })
        parent.insert(index, group)

        for element, section_id in self.new_elements:
            group.insert(0, element)

    def _remove_originals(self, parent, element):
        if not self.options.keep_original:
            parent.remove(element)

    def _prepare_line_elements(self, element, lines):
        for line in lines:
            if len(line.coords) < 2:
                continue

            try:
                sector = self._get_sector(self._get_angle(Point(line.coords[0]), Point(line.coords[1])))
                color = sector[2]
                section_id = sector[3]
            except TypeError:
                color = "black"
                section_id = 0

            d = "M"
            for x, y in line.coords:
                d += "%s,%s " % (x, y)
                d += " "

            stroke_element = etree.Element(SVG_PATH_TAG,
                                           {
                                            "style": str(self.path_style(element, str(color))),
                                            "transform": get_correction_transform(element.node),
                                            "d": d
                                           })
            self.new_elements.append([stroke_element, section_id])

    def path_style(self, element, color):
        return inkex.Style(element.node.get('style', '')) + inkex.Style('stroke:%s' % color)
