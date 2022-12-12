# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import atan2, degrees

from lxml import etree
from shapely.geometry import LineString, Point

import inkex

from ..elements import Stroke
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS, SVG_PATH_TAG
from .base import InkstitchExtension


class CutworkSegmentation(InkstitchExtension):
    '''
    This will split up stroke elements according to their direction.
    Overlapping angle definitions (user input) will result in overlapping paths.
    This is wanted behaviour if the needles have a hard time to cut edges at the border of their specific angle capability.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-o", "--options", type=str, default=None, dest="page_1")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_2")
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
        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more stroke elements."))
            return

        if not self.get_elements():
            return

        self.sectors = {
                        1: {'id': 1, 'start': self.options.a_start, 'end': self.options.a_end, 'color': self.options.a_color, 'point_list': []},
                        2: {'id': 2, 'start': self.options.b_start, 'end': self.options.b_end, 'color': self.options.b_color, 'point_list': []},
                        3: {'id': 3, 'start': self.options.c_start, 'end': self.options.c_end, 'color': self.options.c_color, 'point_list': []},
                        4: {'id': 4, 'start': self.options.d_start, 'end': self.options.d_end, 'color': self.options.d_color, 'point_list': []}
                       }

        # remove sectors where the start angle equals the end angle (some setups only work with two needles instead of four)
        self.sectors = {index: sector for index, sector in self.sectors.items() if sector['start'] != sector['end']}

        self.new_elements = []
        parent = None
        for element in self.elements:
            if isinstance(element, Stroke):
                # save parent and index to be able to position and insert new elements later on
                parent = element.node.getparent()
                index = parent.index(element.node)

                for path in element.paths:
                    linestring = LineString(path)
                    # fill self.new_elements list with line segments
                    self._prepare_line_sections(element, linestring.coords)

        if parent is None:
            inkex.errormsg(_("Please select at least one element with a stroke color."))
            return

        self._insert_elements(parent, index)
        self._remove_originals()

    def _get_sectors(self, angle):
        sectors = []
        for sector in self.sectors.values():
            if self._in_sector(angle, sector):
                sectors.append(sector)
        return sectors

    def _in_sector(self, angle, sector):
        stop = sector['end'] + 1
        if sector['start'] > stop:
            return angle in range(sector['start'], 181) or angle in range(0, stop)
        else:
            return angle in range(sector['start'], stop)

    def _get_angle(self, p1, p2):
        angle = round(degrees(atan2(p2.y - p1.y, p2.x - p1.x)) % 360)
        if angle > 180:
            angle -= 180
        return angle

    def _prepare_line_sections(self, element, coords):
        prev_point = None
        current_sectors = []

        for index, point in enumerate(coords):
            point = Point(*point)
            if prev_point is None:
                prev_point = point
                continue

            angle = self._get_angle(point, prev_point)
            sectors = self._get_sectors(angle)

            for sector in sectors:
                self.sectors[sector['id']]['point_list'].append(prev_point)
                # don't miss the last point
                if index == len(coords) - 1:
                    self.sectors[sector['id']]['point_list'].append(point)
                    self._prepare_element(self.sectors[sector['id']], element)

            # if a segment ends, prepare the element and clear point_lists
            for current in current_sectors:
                if current not in sectors:
                    # add last point
                    self.sectors[current['id']]['point_list'].append(prev_point)
                    self._prepare_element(self.sectors[current['id']], element)

            prev_point = point
            current_sectors = sectors

    def _prepare_element(self, sector, element):
        point_list = sector['point_list']
        if len(point_list) < 2:
            return

        color = str(self.path_style(element, str(sector['color'])))

        d = "M "
        for point in point_list:
            d += "%s,%s " % (point.x, point.y)

        stroke_element = etree.Element(SVG_PATH_TAG,
                                       {
                                        "style": color,
                                        "transform": get_correction_transform(element.node),
                                        INKSTITCH_ATTRIBS["ties"]: "3",
                                        INKSTITCH_ATTRIBS["running_stitch_length_mm"]: "1",
                                        "d": d
                                       })
        self.new_elements.append([stroke_element, sector['id']])
        # clear point_list in self.sectors
        self.sectors[sector['id']].update({'point_list': []})

    def _insert_elements(self, parent, index):
        self.new_elements.reverse()
        if self.options.sort_by_color is True:
            self.new_elements = sorted(self.new_elements, key=lambda x: x[1], reverse=True)

        group = self._insert_group(parent, _("Cutwork Group"), "__inkstitch_cutwork_group__", index)

        section = 0
        for element, section_id in self.new_elements:
            # if sorted by color, add a subgroup for each knife
            if self.options.sort_by_color:
                if section_id != section:
                    section = section_id
                    section_group = self._insert_group(group, _("Needle #%s") % section, "__inkstitch_cutwork_needle_group__")
            else:
                section_group = group

            section_group.insert(0, element)

    def _insert_group(self, parent, label, group_id, index=0):
        group = etree.Element("g", {
            INKSCAPE_LABEL: "%s" % label,
            "id": self.uniqueId("%s" % group_id)
        })
        parent.insert(index, group)
        return group

    def _remove_originals(self):
        if self.options.keep_original:
            return

        for element in self.elements:
            if isinstance(element, Stroke):
                parent = element.node.getparent()
                parent.remove(element.node)

    def path_style(self, element, color):
        # set stroke color and make it a running stitch - they don't want to cut zigzags
        return inkex.Style(element.node.get('style', '')) + inkex.Style('stroke:%s;stroke-dasharray:6,1;' % color)
