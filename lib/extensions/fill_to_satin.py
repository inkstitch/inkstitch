# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

from inkex import Boolean, Group, Path, PathElement
from shapely.geometry import LineString, MultiLineString, Point
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
        self.arg_parser.add_argument("--skip_end_section", dest="skip_end_section", type=Boolean, default=False)
        self.arg_parser.add_argument("--center", dest="center", type=Boolean, default=False)
        self.arg_parser.add_argument("--contour", dest="contour", type=Boolean, default=False)
        self.arg_parser.add_argument("--zigzag", dest="zigzag", type=Boolean, default=False)
        self.arg_parser.add_argument("--keep_originals", dest="keep_originals", type=Boolean, default=False)

        self.satin_index = 0

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            self.print_error()
            return

        fill_elements, selected_rungs = self._get_shapes()
        if not fill_elements or not selected_rungs:
            self.print_error()
            return

        settings = {
            'skip_end_section': self.options.skip_end_section,
        }

        for fill_element in fill_elements:
            fill_shape = fill_element.shape

            fill_linestrings = self._fill_to_linestrings(fill_shape)
            for linestrings in fill_linestrings:
                fill_to_satin = FillElementToSatin(self.svg, settings, fill_element, fill_shape, linestrings, selected_rungs)
                satins = fill_to_satin.convert_to_satin()
                self._insert_satins(fill_element, satins)

        self._remove_originals()

    def _get_shapes(self):
        '''Filter selected elements. Take rungs and fills.'''
        fill_elements = []
        selected_rungs = []
        nodes = []
        warned = False
        for element in self.elements:
            if element.node in nodes and not warned:
                self.print_error(
                    (f'{element.node.label} ({element.node.get_id()}): ' + _("This element has a fill and a stroke.\n\n"
                     "Rungs only have a stroke color and fill elements a fill color."))
                )
                warned = True
            nodes.append(element.node)
            if isinstance(element, FillStitch):
                fill_elements.append(element)
            elif isinstance(element, Stroke):
                selected_rungs.extend(list(element.as_multi_line_string().geoms))
        return fill_elements, selected_rungs

    def _fill_to_linestrings(self, fill_shape):
        '''Takes a fill shape (Multipolygon) and returns the shape as a list of linestrings'''
        fill_linestrings = []
        for polygon in fill_shape.geoms:
            linestrings = ensure_multi_line_string(polygon.boundary, 1)
            fill_linestrings.append(list(linestrings.geoms))
        return fill_linestrings

    def _insert_satins(self, fill_element, satins):
        '''Insert satin elements into the document'''
        if not satins:
            return
        group = fill_element.node.getparent()
        index = group.index(fill_element.node) + 1
        transform = get_correction_transform(fill_element.node)
        style = f'stroke: {fill_element.color}; fill: none; stroke-width: {self.svg.viewport_to_unit("1px")};'
        if len(satins) > 1:
            new_group = Group()
            group.insert(index, new_group)
            group = new_group
            group.label = _("Satin Group")
            index = 0
        for i, satin in enumerate(satins):
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
            node.label = _("Satin") + f" {self.satin_index}"
            group.insert(index, node)
            self.satin_index += 1

    def _remove_originals(self):
        '''Remove original elements - if requested'''
        if not self.options.keep_originals:
            for element in self.elements:
                element.node.getparent().remove(element.node)

    def print_error(self, message=_("Please select a fill object and rungs.")):
        '''We did not receive the rigth elements, inform user'''
        app = AbortMessageApp(
            message,
            _("https://inkstitch.org/satin-tools#fill-to-satin")
        )
        app.MainLoop()


class FillElementToSatin:
    def __init__(self, svg, settings, fill_element, fill_shape, linestrings, selected_rungs):
        self.svg = svg
        self.settings = settings
        self.fill_element = fill_element
        self.fill_shape = fill_shape
        self.linestrings = linestrings
        self.selected_rungs = selected_rungs

        self.rungs = []
        self.line_sections = []
        self.rung_sections = defaultdict(list)
        self.section_rungs = defaultdict(list)
        self.bridged_rungs = defaultdict(list)
        self.used_bridged_rungs = []
        self.rung_segments = {}

    def convert_to_satin(self):
        intersection_points, bridges = self._validate_rungs()

        self._generate_line_sections()
        self._define_relations(bridges)

        if len(self.line_sections) == 2 and self.line_sections[0].distance(self.line_sections[1]) > 0:
            # there is only one segment, add it directly
            rails = [MultiLineString([self.line_sections[0], self.line_sections[1]])]
            rungs = [ensure_multi_line_string(self.rungs[0])]
            self._insert_satins([rails + rungs])
            return
        else:
            rung_segments, satin_segments = self._get_segments(intersection_points)

        if len(self.rung_sections) == 2 and self.rung_sections[0] == self.rung_sections[1]:
            combined_satins = self._get_two_rung_circle_geoms(rung_segments, satin_segments)
        else:
            combined_satins = self._get_satin_geoms(rung_segments, satin_segments)

        return combined_satins

    def _get_two_rung_circle_geoms(self, rung_segments, satin_segments):
        '''Imagine a donut with two rungs: this is a special case where all segments connect to the very same two rungs'''
        combined = defaultdict(list)
        combined_rungs = defaultdict(list)

        combined[0] = [0, 1]
        combined_rungs[0] = [0, 1]

        return self._combined_segments_to_satin_geoms(combined, combined_rungs, satin_segments)

    def _get_satin_geoms(self, rung_segments, satin_segments):
        '''Combine segments and return satin geometries'''
        self.rung_segments = {rung: segments for rung, segments in rung_segments.items() if len(segments) == 2}
        finished_rungs = []
        finished_segments = []
        combined_rails = defaultdict(list)
        combined_rungs = defaultdict(list)

        for rung, segments in self.rung_segments.items():
            self._find_connected(rung, segments, rung, finished_rungs, finished_segments, combined_rails, combined_rungs)

        unfinished = {i for i, segment in enumerate(satin_segments) if i not in finished_segments}
        segment_count = len(satin_segments)
        for i, segment in enumerate(unfinished):
            index = segment_count + i + 1
            combined_rails[index] = [segment]

        return self._combined_segments_to_satin_geoms(combined_rails, combined_rungs, satin_segments)

    def _combined_segments_to_satin_geoms(self, combined_rails, combined_rungs, satin_segments):
        combined_satins = []
        for i, segments in combined_rails.items():
            segment_geoms = []
            for segment_index in set(segments):
                segment_geoms.extend(list(satin_segments[segment_index].geoms))
            satin_rails = ensure_multi_line_string(linemerge(segment_geoms))
            if len(satin_rails.geoms) != 2:
                continue
            satin_rails = [self._adjust_rail_direction(satin_rails)]
            segment_geoms = []
            for rung_index in set(combined_rungs[i]):
                rung = self.rungs[rung_index]
                # satin behaves bad if a rung is positioned directly at the beginning/end section
                if rung.distance(Point(satin_rails[0].geoms[0].coords[0])) > 1:
                    segment_geoms.append(ensure_multi_line_string(rung))
            combined_satins.append(satin_rails + segment_geoms)
        return combined_satins

    def _get_segments(self, intersection_points):  # noqa: C901
        '''Combine line sections to satin segments (find the rails that belong together)'''
        line_section_multi = MultiLineString(self.line_sections)
        rung_segments = defaultdict(list)
        satin_segments = []
        used_bridges = []

        segment_index = 0
        finished_sections = []
        for i, section in enumerate(self.line_sections):
            if i in finished_sections:
                continue
            s_rungs = self.section_rungs[i]
            if len(s_rungs) == 1:
                if self.settings['skip_end_section'] and len(self.rungs) > 1:
                    continue
                segment = self._get_end_segment(section)
                satin_segments.append(segment)
                finished_sections.append(i)
                for rung in s_rungs:
                    rung_segments[rung].append(segment_index)
                segment_index += 1

            elif len(s_rungs) == 2:
                connected_section = self._get_connected_section(i, s_rungs)
                if connected_section:
                    connect_index, segment = self._get_standard_segment(connected_section, s_rungs, section, finished_sections)
                    if segment is None:
                        continue
                    satin_segments.append(segment)
                    for rung in s_rungs:
                        rung_segments[rung].append(segment_index)
                    segment_index += 1
                    finished_sections.extend([i, connect_index])
                else:
                    for bridge, rung_list in self.bridged_rungs.items():
                        if len(rung_list) != 2:
                            continue
                        for rung in s_rungs:
                            if rung in rung_list:
                                if bridge in used_bridges:
                                    continue
                                points1 = intersection_points[rung_list[0]].geoms
                                points2 = intersection_points[rung_list[1]].geoms
                                segment1 = LineString([points1[0], points2[0]])
                                segment2 = LineString([points1[1], points2[1]])
                                if segment1.intersects(segment2):
                                    segment1 = LineString([points1[0], points2[1]])
                                    segment2 = LineString([points1[1], points2[0]])
                                segment1 = snap(segment1, line_section_multi, 0.0001)
                                segment2 = snap(segment2, line_section_multi, 0.0001)
                                segment = MultiLineString([segment1, segment2])
                                satin_segments.append(segment)
                                rung_segments[rung_list[0]].append(segment_index)
                                rung_segments[rung_list[1]].append(segment_index)
                                segment_index += 1
                                finished_sections.append(i)
                                used_bridges.append(bridge)
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

    def _get_standard_segment(self, connected_section, s_rungs, section, finished_sections):
        section2 = None
        segment = None
        connect_index = None
        if len(connected_section) == 1:
            section2 = self.line_sections[connected_section[0]]
            connect_index = connected_section[0]
        else:
            for connect in connected_section:
                if connect in finished_sections:
                    continue
                offset_rung = self.rungs[s_rungs[0]].offset_curve(0.01)
                section_candidate = self.line_sections[connect]
                if offset_rung.intersects(section) == offset_rung.intersects(section_candidate):
                    section2 = section_candidate
                    connect_index = connect
                    break
        if section2 is not None:
            segment = MultiLineString([section, section2])
        return connect_index, segment

    def _get_connected_section(self, index, s_rungs):
        rung_section_list = []
        for rung in s_rungs:
            connections = self.rung_sections[rung]
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

    def _find_connected(self, rung, segments, first_rung, finished_rungs, finished_segments, combined_rails, combined_rungs):
        '''Group combinable segments'''
        if rung in finished_rungs:
            return
        finished_rungs.append(rung)
        combined_rails[first_rung].extend(segments)
        combined_rungs[first_rung].append(rung)
        finished_segments.extend(segments)
        for segment in segments:
            connected = self._get_combinable_segments(segment, segments)
            if not connected:
                continue
            for connected_rung, connected_segments in connected.items():
                self._find_connected(
                    connected_rung,
                    connected_segments,
                    first_rung, finished_rungs,
                    finished_segments,
                    combined_rails,
                    combined_rungs
                )

    def _get_combinable_segments(self, segment, segments_in):
        '''Finds the segments which are neighboring this segment'''
        return {rung: segments for rung, segments in self.rung_segments.items() if segment in segments and segments_in != segments}

    def _generate_line_sections(self):
        '''Splits the fill outline into sections. Splitter is a MultiLineString with all available rungs'''
        rungs = MultiLineString(self.rungs)

        for line in self.linestrings:
            sections = list(ensure_multi_line_string(split(line, rungs)).geoms)
            if len(sections) > 1:
                # merge end and start section
                sections[0] = linemerge(MultiLineString([sections[0], sections[-1]]))
                del sections[-1]
            self.line_sections.extend(sections)

    def _define_relations(self, bridges):
        ''' Defines information about the relations between line_sections and rungs
            rung_sections: dictionary with rung_index: neighboring sections
            section_rungs: dictionary with section_id: neighboring rungs
            bridged_rungs: lines which define which segments are to be bridged at intersection points
        '''
        for i, section in enumerate(self.line_sections):
            for j, rung in enumerate(self.rungs):
                if section.distance(rung) < 0.01:
                    self.section_rungs[i].append(j)
                    self.rung_sections[j].append(i)
        for i, bridge in enumerate(bridges):
            for j, rung in enumerate(self.rungs):
                if bridge.intersects(rung):
                    self.bridged_rungs[i].append(j)

    def _validate_rungs(self):
        ''' Returns only valid rungs and bridge section markers'''
        multi_line_string = MultiLineString(self.linestrings)
        bridges = []
        intersection_points = []
        rungs = []
        for rung in self.selected_rungs:
            intersection = multi_line_string.intersection(rung)
            if intersection.geom_type == 'MultiPoint' and len(intersection.geoms) == 2:
                rungs.append(rung)
                intersection_points.append(intersection)
            elif intersection.is_empty and rung.within(self.fill_shape):
                # these rungs (possibly) connect two rungs
                bridges.append(rung)
        # filter rungs when they are crossing other rungs. They could possibly produce bad line sections
        for i, rung in enumerate(rungs):
            multi_rung = MultiLineString([r for j, r in enumerate(rungs) if j != i])
            intersection = rung.intersection(multi_rung)
            if not rung.intersects(multi_rung) or not rung.intersection(multi_rung).intersects(self.fill_shape):
                self.rungs.append(rung)
        return intersection_points, bridges
