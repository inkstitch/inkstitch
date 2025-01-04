# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

from inkex import Boolean, Group, Path, PathElement
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge, snap, split, substring

from ..elements import FillStitch, Stroke
from ..gui.abort_message import AbortMessageApp
from ..i18n import _
from ..svg import get_correction_transform
from ..utils import ensure_multi_line_string
from .base import InkstitchExtension


class FillToSatin(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--center", dest="center", type=Boolean, default=False)
        self.arg_parser.add_argument("--contour", dest="contour", type=Boolean, default=False)
        self.arg_parser.add_argument("--zigzag", dest="zigzag", type=Boolean, default=False)
        self.arg_parser.add_argument("--keep_originals", dest="keep_originals", type=Boolean, default=False)

        self.fill_element = None
        self.rungs = []
        self.rung_segments = {}

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            self.print_error()
            return

        self._get_shapes()
        if self.fill_element is None or len(self.rungs) < 1:
            self.print_error()
            return

        fill_shape = self.fill_element.shape
        fill_linestrings = self._fill_to_linestrings(fill_shape)
        intersection_points, bridges = self._validate_rungs(fill_linestrings)

        line_sections = self._get_line_sections(fill_linestrings)
        rung_sections, section_rungs, bridged_sections = self._get_connections(line_sections, bridges)

        rung_segments, satin_segments = self._get_segments(line_sections, rung_sections, section_rungs, bridged_sections, intersection_points)

        combined_satins = self._get_satin_geoms(rung_segments, satin_segments)

        self._insert_satins(combined_satins)
        self._remove_originals()

    def _insert_satins(self, combined_satins):
        if not combined_satins:
            return
        group = self.fill_element.node.getparent()
        transform = get_correction_transform(self.elements[0].node)
        style = f'stroke: {self.fill_element.color}; fill: none; stroke-width: {self.svg.viewport_to_unit("1px")};'
        if len(combined_satins) > 1:
            new_group = Group()
            group.append(new_group)
            group = new_group
            group.label = _("Satin Group")
        for i, satin in enumerate(combined_satins):
            node = PathElement()
            d = ""
            for segment in satin:
                for geom in segment.geoms:
                    d += str(Path(list(geom.coords)))
            node.set('d', d)
            node.set('style', style)
            node.set('inkstitch:satin_column', True)
            if self.options.center:
                node.set('inkstitch:center_walk_underlay', True)
            if self.options.contour:
                node.set('inkstitch:contour_underlay', True)
            if self.options.zigzag:
                node.set('inkstitch:zigzag_underlay', True)
            node.transform = transform
            node.apply_transform()
            node.label = _("Satin") + f" {i+1}"
            group.append(node)

    def _remove_originals(self):
        if not self.options.keep_originals:
            for element in self.elements:
                element.node.getparent().remove(element.node)

    def _get_satin_geoms(self, rung_segments, satin_segments):
        self.rung_segments = {rung: segments for rung, segments in rung_segments.items() if len(segments) == 2}
        finished_rungs = []
        finished_segments = []
        combined = defaultdict(list)
        combined_rungs = defaultdict(list)

        for rung, segments in self.rung_segments.items():
            self._find_connected(rung, segments, rung, finished_rungs, finished_segments, combined, combined_rungs)

        unfinished = {i for i, segment in enumerate(satin_segments) if i not in finished_segments}
        segment_count = len(satin_segments)
        for i, segment in enumerate(unfinished):
            index = segment_count + i + 1
            combined[index] = [segment]

        combined_satins = []
        for i, segments in combined.items():
            segment_geoms = []
            for segment_index in set(segments):
                segment_geoms.extend(list(satin_segments[segment_index].geoms))
            satin_rails = ensure_multi_line_string(linemerge(segment_geoms))
            satin_rails = [self._adjust_rail_direction(satin_rails)]

            segment_geoms = []
            for rung_index in set(combined_rungs[i]):
                segment_geoms.append(ensure_multi_line_string(self.rungs[rung_index]))
            combined_satins.append(satin_rails + segment_geoms)
        return combined_satins

    def _get_segments(self, line_sections, rung_sections, section_rungs, bridged_sections, intersection_points):  # noqa: C901
        line_section_multi = MultiLineString(line_sections)
        rung_segments = defaultdict(list)
        satin_segments = []

        segment_index = 0
        finished_sections = []
        for i, section in enumerate(line_sections):
            if i in finished_sections:
                continue
            s_rungs = section_rungs[i]
            if len(s_rungs) == 1:
                segment = self._get_end_segment(section)
                satin_segments.append(segment)
                for rung in s_rungs:
                    rung_segments[rung].append(segment_index)
                segment_index += 1

            elif len(s_rungs) == 2:
                connected_section = self._get_connected_section(i, s_rungs, rung_sections)
                if connected_section:
                    segment = self._get_standard_segment(line_sections, connected_section, s_rungs, section)
                    if segment is None:
                        continue
                    satin_segments.append(segment)
                    for rung in s_rungs:
                        rung_segments[rung].append(segment_index)
                    segment_index += 1

                    # mark sections as finished
                    finished_sections.append(connected_section[0])

                elif i in bridged_sections:
                    segment = self._get_bridged_segment(section, s_rungs, intersection_points, line_section_multi)
                    if segment:
                        satin_segments.append(segment)
                        for rung in s_rungs:
                            rung_segments[rung].append(segment_index)
                        segment_index += 1
                else:
                    # sections with multiple rungs, open ends, not bridged
                    # IF users define their rungs well, they won't have a problem if we just ignore these sections
                    # otherwise they will see some sort of gap, they can close it manually if they want
                    pass
        return rung_segments, satin_segments

    def _get_end_segment(self, section):
        section = section.simplify(0.5)
        rail1 = substring(section, 0, 0.40009, True).coords
        rail2 = substring(section, 0.50001, 1, True).coords
        if len(rail1) > 2:
            rail1 = rail1[:-1]
        if len(rail2) > 2:
            rail2 = rail2[1:]

        segment = MultiLineString([LineString(rail1), LineString(rail2)])
        return segment

    def _get_standard_segment(self, line_sections, connected_section, s_rungs, section):
        section2 = None
        segment = None
        if len(connected_section) == 1:
            section2 = line_sections[connected_section[0]]
        else:
            for connect in connected_section:
                test_rung = self.rungs[s_rungs[0]].offset_curve(0.01)
                test_section = line_sections[connect]
                if test_rung.intersects(section) == test_rung.intersects(test_section):
                    section2 = test_section
                    break
        if section2 is not None:
            segment = MultiLineString([section, section2])
        return segment

    def _get_bridged_segment(self, section, s_rungs, intersection_points, line_section_multi):
        segment = None
        bridge_points = []
        # create bridge
        for rung in s_rungs:
            rung_points = intersection_points[rung].geoms
            for point in rung_points:
                if point.distance(section) > 0.01:
                    bridge_points.append(point)
        if len(bridge_points) == 2:
            rung = self.rungs[s_rungs[0]]
            bridge = LineString(bridge_points)
            bridge = snap(bridge, line_section_multi, 0.0001)
            segment = MultiLineString([section, bridge])
        return segment

    def _get_connected_section(self, index, s_rungs, rung_sections):
        rung_section_list = []
        for rung in s_rungs:
            connections = rung_sections[rung]
            rung_section_list.append(connections)
        connected_section = list(set(rung_section_list[0]) & set(rung_section_list[1]))
        connected_section.remove(index)
        return connected_section

    def _adjust_rail_direction(self, satin_rails):
        # See also elements/satin_column.py (_get_rails_to_reverse)
        rails = list(satin_rails.geoms)
        lengths = []
        lengths_reverse = []

        for i in range(10):
            distance = i / 10
            point0 = rails[0].interpolate(distance, normalized=True)
            point1 = rails[1].interpolate(distance, normalized=True)
            point1_reverse = rails[1].interpolate(1 - distance, normalized=True)

            lengths.append(point0.distance(point1))
            lengths_reverse.append(point0.distance(point1_reverse))

        if sum(lengths) > sum(lengths_reverse):
            rails[0] = rails[0].reverse()

        return MultiLineString(rails)

    def _find_connected(self, rung, segments, first_rung, finished_rungs, finished_segments, combined, combined_rungs):
        if rung in finished_rungs:
            return
        finished_rungs.append(rung)
        combined[first_rung].extend(segments)
        combined_rungs[first_rung].append(rung)
        finished_segments.extend(segments)
        for segment in segments:
            connected = self._get_combinable_segments(segment, segments)
            if not connected:
                continue
            for connected_rung, connected_segments in connected.items():
                self._find_connected(connected_rung, connected_segments, first_rung, finished_rungs, finished_segments, combined, combined_rungs)

    def _get_combinable_segments(self, segment, segments_in):
        return {rung: segments for rung, segments in self.rung_segments.items() if segment in segments and segments_in != segments}

    def _get_line_sections(self, linestrings):
        '''Splits the fill outline into sections. Splitter is a MultiLineString with all available rungs'''
        rungs = MultiLineString(self.rungs)
        line_sections = []
        for line in linestrings:
            sections = list(ensure_multi_line_string(split(line, rungs)).geoms)
            if len(sections) > 1:
                # merge end and start section
                sections[0] = linemerge(MultiLineString([sections[0], sections[-1]]))
                del sections[-1]
            line_sections.extend(sections)
        return line_sections

    def _get_connections(self, line_sections, bridges):
        ''' Defines information about the relations between line_sections and rungs
            Returns:
                rung_sections: dictionary with rung_index: neighboring sections
                section_rungs: dictionary with section_id: neighboring rungs
                bridged_sections: list of sections which the user marked for bridging
        '''
        rung_sections = defaultdict(list)
        section_rungs = defaultdict(list)
        bridged_sections = []
        for i, section in enumerate(line_sections):
            if not section.intersection(bridges).is_empty:
                bridged_sections.append(i)
            for j, rung in enumerate(self.rungs):
                if section.distance(rung) < 0.01:
                    section_rungs[i].append(j)
                    rung_sections[j].append(i)
        return rung_sections, section_rungs, bridged_sections

    def _validate_rungs(self, fill_linestrings):
        multi_line_string = MultiLineString(fill_linestrings)
        valid_rungs = []
        bridge_indicators = []
        intersection_points = []
        for rung in self.rungs:
            intersection = multi_line_string.intersection(rung)
            if intersection.geom_type == 'MultiPoint' and len(intersection.geoms) == 2:
                valid_rungs.append(rung)
                intersection_points.append(intersection)
            elif intersection.geom_type == 'Point':
                # these rungs help to indicate how the satin section should be connected
                bridge_indicators.append(rung)
        self.rungs = valid_rungs
        return intersection_points, MultiLineString(bridge_indicators)

    def _fill_to_linestrings(self, fill_shape):
        fill_linestrings = []
        for polygon in fill_shape.geoms:
            linestrings = ensure_multi_line_string(polygon.boundary)
            fill_linestrings.extend(list(linestrings.geoms))
        return fill_linestrings

    def _get_shapes(self):
        for element in self.elements:
            if isinstance(element, FillStitch):
                # we take only one fill element at a time (the last one in the list)
                self.fill_element = element
            elif isinstance(element, Stroke):
                self.rungs.extend(list(element.as_multi_line_string().geoms))

    def print_error(self):
        app = AbortMessageApp(
            _("Please select a fill object and rungs."),
            _("https://inkstitch.org/satin-tools#fill-to-satin")
        )
        app.MainLoop()
