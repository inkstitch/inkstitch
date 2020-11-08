from copy import deepcopy
from itertools import chain

from inkex import paths
from shapely import affinity as shaffinity
from shapely import geometry as shgeo

from ..i18n import _
from ..svg import line_strings_to_csp, point_lists_to_csp
from ..utils import Point, cache, collapse_duplicate_point, cut
from .element import EmbroideryElement, Patch, param
from .validation import ValidationError


class SatinHasFillError(ValidationError):
    name = _("Satin column has fill")
    description = _("Satin column: Object has a fill (but should not)")
    steps_to_solve = [
        _("* Select this object."),
        _("* Open the Fill and Stroke panel"),
        _("* Open the Fill tab"),
        _("* Disable the Fill"),
        _("* Alternative: open Params and switch this path to Stroke to disable Satin Column mode")
    ]


class TooFewPathsError(ValidationError):
    name = _("Too few subpaths")
    description = _("Satin column: Object has too few subpaths.  A satin column should have at least two subpaths (the rails).")
    steps_to_solve = [
        _("* Add another subpath (select two rails and do Path > Combine)"),
        _("* Convert to running stitch or simple satin (Params extension)")
    ]


class UnequalPointsError(ValidationError):
    name = _("Unequal number of points")
    description = _("Satin column: There are no rungs and rails have an an unequal number of points.")
    steps_to_solve = [
        _('The easiest way to solve this issue is to add one or more rungs. '),
        _('Rungs control the stitch direction in satin columns.'),
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing the rung.')
    ]


rung_message = _("Each rung should intersect both rails once.")


class DanglingRungError(ValidationError):
    name = _("Rung doesn't intersect rails")
    description = _("Satin column: A rung doesn't intersect both rails.") + " " + rung_message


class TooManyIntersectionsError(ValidationError):
    name = _("Rung intersects too many times")
    description = _("Satin column: A rung intersects a rail more than once.") + " " + rung_message


class SatinColumn(EmbroideryElement):
    element_name = _("Satin Column")

    def __init__(self, *args, **kwargs):
        super(SatinColumn, self).__init__(*args, **kwargs)

    @property
    @param('satin_column', _('Custom satin column'), type='toggle')
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    # I18N: "E" stitch is so named because it looks like the letter E.
    @property
    @param('e_stitch', _('"E" stitch'), type='boolean', default='false')
    def e_stitch(self):
        return self.get_boolean_param("e_stitch")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Peak-to-peak distance between zig-zags.'),
           unit='mm',
           type='float',
           default=0.4)
    def zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param(
        'pull_compensation_mm',
        _('Pull compensation'),
        tooltip=_('Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape.  '
                  'This setting expands each pair of needle penetrations outward from the center of the satin column.'),
        unit='mm',
        type='float',
        default=0)
    def pull_compensation(self):
        # In satin stitch, the stitches have a tendency to pull together and
        # narrow the entire column.  We can compensate for this by stitching
        # wider than we desire the column to end up.
        return self.get_float_param("pull_compensation_mm", 0)

    @property
    @param('contour_underlay', _('Contour underlay'), type='toggle', group=_('Contour Underlay'))
    def contour_underlay(self):
        # "Contour underlay" is stitching just inside the rectangular shape
        # of the satin column; that is, up one side and down the other.
        return self.get_boolean_param("contour_underlay")

    @property
    @param('contour_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Contour Underlay'), type='float', default=1.5)
    def contour_underlay_stitch_length(self):
        return max(self.get_float_param("contour_underlay_stitch_length_mm", 1.5), 0.01)

    @property
    @param('contour_underlay_inset_mm',
           _('Contour underlay inset amount'),
           tooltip=_('Shrink the outline, to prevent the underlay from showing around the outside of the satin column.'),
           unit='mm',
           group=_('Contour Underlay'),
           type='float',
           default=0.4)
    def contour_underlay_inset(self):
        # how far inside the edge of the column to stitch the underlay
        return self.get_float_param("contour_underlay_inset_mm", 0.4)

    @property
    @param('center_walk_underlay', _('Center-walk underlay'), type='toggle', group=_('Center-Walk Underlay'))
    def center_walk_underlay(self):
        # "Center walk underlay" is stitching down and back in the centerline
        # between the two sides of the satin column.
        return self.get_boolean_param("center_walk_underlay")

    @property
    @param('center_walk_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Center-Walk Underlay'), type='float', default=1.5)
    def center_walk_underlay_stitch_length(self):
        return max(self.get_float_param("center_walk_underlay_stitch_length_mm", 1.5), 0.01)

    @property
    @param('zigzag_underlay', _('Zig-zag underlay'), type='toggle', group=_('Zig-zag Underlay'))
    def zigzag_underlay(self):
        return self.get_boolean_param("zigzag_underlay")

    @property
    @param('zigzag_underlay_spacing_mm',
           _('Zig-Zag spacing (peak-to-peak)'),
           tooltip=_('Distance between peaks of the zig-zags.'),
           unit='mm',
           group=_('Zig-zag Underlay'),
           type='float',
           default=3)
    def zigzag_underlay_spacing(self):
        return max(self.get_float_param("zigzag_underlay_spacing_mm", 3), 0.01)

    @property
    @param('zigzag_underlay_inset_mm',
           _('Inset amount'),
           tooltip=_('default: half of contour underlay inset'),
           unit='mm',
           group=_('Zig-zag Underlay'),
           type='float',
           default="")
    def zigzag_underlay_inset(self):
        # how far in from the edge of the satin the points in the zigzags
        # should be

        # Default to half of the contour underlay inset.  That is, if we're
        # doing both contour underlay and zigzag underlay, make sure the
        # points of the zigzag fall outside the contour underlay but inside
        # the edges of the satin column.
        return self.get_float_param("zigzag_underlay_inset_mm") or self.contour_underlay_inset / 2.0

    @property
    @cache
    def shape(self):
        # This isn't used for satins at all, but other parts of the code
        # may need to know the general shape of a satin column.

        flattened = self.flatten(self.parse_path())
        line_strings = [shgeo.LineString(path) for path in flattened]

        return shgeo.MultiLineString(line_strings)

    @property
    @cache
    def csp(self):
        return self.parse_path()

    @property
    @cache
    def rails(self):
        """The rails in order, as point lists"""
        return [subpath for i, subpath in enumerate(self.csp) if i in self.rail_indices]

    @property
    @cache
    def flattened_rails(self):
        """The rails, as LineStrings."""
        return tuple(shgeo.LineString(self.flatten_subpath(rail)) for rail in self.rails)

    @property
    @cache
    def flattened_rungs(self):
        """The rungs, as LineStrings."""
        return tuple(shgeo.LineString(self.flatten_subpath(rung)) for rung in self.rungs)

    @property
    @cache
    def rungs(self):
        """The rungs, as point lists.

        If there are no rungs, then this is an old-style satin column.  The
        rails are expected to have the same number of path nodes.  The path
        nodes, taken in sequential pairs, act in the same way as rungs would.
        """
        if len(self.csp) == 2:
            # It's an old-style satin column.  To make things easier we'll
            # actually create the implied rungs.
            return self._synthesize_rungs()
        else:
            return [subpath for i, subpath in enumerate(self.csp) if i not in self.rail_indices]

    def _synthesize_rungs(self):
        rung_endpoints = []
        for rail in self.rails:
            points = self.strip_control_points(rail)

            # ignore the start and end
            points = points[1:-1]

            rung_endpoints.append(points)

        rungs = []
        for start, end in zip(*rung_endpoints):
            # Expand the points just a bit to ensure that shapely thinks they
            # intersect with the rails even with floating point inaccuracy.
            start = Point(*start)
            end = Point(*end)
            start, end = self.offset_points(start, end, 0.01)
            start = list(start)
            end = list(end)

            rungs.append([[start, start, start], [end, end, end]])

        return rungs

    @property
    @cache
    def rail_indices(self):
        paths = [self.flatten_subpath(subpath) for subpath in self.csp]
        paths = [shgeo.LineString(path) for path in paths]
        num_paths = len(paths)

        # Imagine a satin column as a curvy ladder.
        # The two long paths are the "rails" of the ladder.  The remainder are
        # the "rungs".
        #
        # The subpaths in this SVG path may be in arbitrary order, so we need
        # to figure out which are the rails and which are the rungs.
        #
        # Rungs are the paths that intersect with exactly 2 other paths.
        # Rails are everything else.

        if num_paths <= 2:
            # old-style satin column with no rungs
            return list(range(num_paths))

        # This takes advantage of the fact that sum() counts True as 1
        intersection_counts = [sum(paths[i].intersects(paths[j]) for j in range(num_paths) if i != j)
                               for i in range(num_paths)]
        paths_not_intersecting_two = [i for i in range(num_paths) if intersection_counts[i] != 2]
        num_not_intersecting_two = len(paths_not_intersecting_two)

        if num_not_intersecting_two == 2:
            # Great, we have two unambiguous rails.
            return paths_not_intersecting_two
        else:
            # This is one of two situations:
            #
            # 1. There are two rails and two rungs, and it looks like a
            # hash symbol (#).  Unfortunately for us, this is an ambiguous situation
            # and we'll have to take a guess as to which are the rails and
            # which are the rungs.  We'll guess that the rails are the longest
            # ones.
            #
            # or,
            #
            # 2. The paths don't look like a ladder at all, but some other
            # kind of weird thing.  Maybe one of the rungs crosses a rail more
            # than once.  Treat it like the previous case and we'll sort out
            # the intersection issues later.
            indices_by_length = sorted(list(range(num_paths)), key=lambda index: paths[index].length, reverse=True)
            return indices_by_length[:2]

    def _cut_rail(self, rail, rung):
        for segment_index, rail_segment in enumerate(rail[:]):
            if rail_segment is None:
                continue

            intersection = rail_segment.intersection(rung)

            # If there are duplicate points in a rung-less satin, then
            # intersection will be a GeometryCollection of multiple copies
            # of the same point.  This reduces it that to a single point.
            intersection = collapse_duplicate_point(intersection)

            if not intersection.is_empty:
                cut_result = cut(rail_segment, rail_segment.project(intersection))
                rail[segment_index:segment_index + 1] = cut_result

                if cut_result[1] is None:
                    # if we were exactly at the end of one of the existing rail segments,
                    # stop here or we'll get a spurious second intersection on the next
                    # segment
                    break

    @property
    @cache
    def flattened_sections(self):
        """Flatten the rails, cut with the rungs, and return the sections in pairs."""

        rails = [[rail] for rail in self.flattened_rails]
        rungs = self.flattened_rungs

        for rung in rungs:
            for rail in rails:
                self._cut_rail(rail, rung)

        for rail in rails:
            for i in range(len(rail)):
                if rail[i] is not None:
                    rail[i] = [Point(*coord) for coord in rail[i].coords]

        # Clean out empty segments.  Consider an old-style satin like this:
        #
        #  |   |
        #  *   *---*
        #  |       |
        #  |       |
        #
        # The stars indicate where the bezier endpoints lay.  On the left, there's a
        # zero-length bezier at the star.  The user's goal here is to ignore the
        # horizontal section of the right rail.

        sections = list(zip(*rails))
        sections = [s for s in sections if s[0] is not None and s[1] is not None]

        return sections

    def validation_errors(self):
        # The node should have exactly two paths with no fill.  Each
        # path should have the same number of points, meaning that they
        # will both be made up of the same number of bezier curves.

        if self.get_style("fill") is not None:
            yield SatinHasFillError(self.shape.centroid)

        if len(self.rails) < 2:
            yield TooFewPathsError(self.shape.centroid)
        elif len(self.csp) == 2:
            if len(self.rails[0]) != len(self.rails[1]):
                yield UnequalPointsError(self.flattened_rails[0].interpolate(0.5, normalized=True))
        else:
            for rung in self.flattened_rungs:
                for rail in self.flattened_rails:
                    intersection = rung.intersection(rail)
                    if intersection.is_empty:
                        yield DanglingRungError(rung.interpolate(0.5, normalized=True))
                    elif not isinstance(intersection, shgeo.Point):
                        yield TooManyIntersectionsError(rung.interpolate(0.5, normalized=True))

    def reverse(self):
        """Return a new SatinColumn like this one but in the opposite direction.

        The path will be flattened and the new satin will contain a new XML
        node that is not yet in the SVG.
        """
        # flatten the path because you can't just reverse a CSP subpath's elements (I think)
        point_lists = []

        for rail in self.rails:
            point_lists.append(list(reversed(self.flatten_subpath(rail))))

        # reverse the order of the rails because we're sewing in the opposite direction
        point_lists.reverse()

        for rung in self.rungs:
            point_lists.append(self.flatten_subpath(rung))

        return self._csp_to_satin(point_lists_to_csp(point_lists))

    def apply_transform(self):
        """Return a new SatinColumn like this one but with transforms applied.

        This node's and all ancestor nodes' transforms will be applied.  The
        new SatinColumn's node will not be in the SVG document.
        """

        return self._csp_to_satin(self.csp)

    def split(self, split_point):
        """Split a satin into two satins at the specified point

        split_point is a point on or near one of the rails, not at one of the
        ends. Finds corresponding point on the other rail (taking into account
        the rungs) and breaks the rails at these points.

        split_point can also be a noramlized projection of a distance along the
        satin, in the range 0.0 to 1.0.

        Returns two new SatinColumn instances: the part before and the part
        after the split point.  All parameters are copied over to the new
        SatinColumn instances.
        """

        cut_points = self._find_cut_points(split_point)
        path_lists = self._cut_rails(cut_points)
        self._assign_rungs_to_split_rails(path_lists)
        self._add_rungs_if_necessary(path_lists)
        return [self._path_list_to_satins(path_list) for path_list in path_lists]

    def _find_cut_points(self, split_point):
        """Find the points on each satin corresponding to the split point.

        split_point is a point that is near but not necessarily touching one
        of the rails.  It is projected onto that rail to obtain the cut point
        for that rail.  A corresponding cut point will be chosen on the other
        rail, taking into account the satin's rungs to choose a matching point.

        split_point can instead be a number in [0.0, 1.0] indicating a
        a fractional distance down the satin to cut at.

        Returns: a list of two Point objects corresponding to the selected
          cut points.
        """

        # like in do_satin()
        points = list(chain.from_iterable(zip(*self.plot_points_on_rails(self.zigzag_spacing, 0))))

        if isinstance(split_point, float):
            index_of_closest_stitch = int(round(len(points) * split_point))
        else:
            split_point = Point(*split_point)
            index_of_closest_stitch = min(list(range(len(points))), key=lambda index: split_point.distance(points[index]))

        if index_of_closest_stitch % 2 == 0:
            # split point is on the first rail
            return (points[index_of_closest_stitch],
                    points[index_of_closest_stitch + 1])
        else:
            # split point is on the second rail
            return (points[index_of_closest_stitch - 1],
                    points[index_of_closest_stitch])

    def _cut_rails(self, cut_points):
        """Cut the rails of this satin at the specified points.

        cut_points is a list of two elements, corresponding to the cut points
        for each rail in order.

        Returns: A list of two elements, corresponding two the two new sets of
          rails.  Each element is a list of two rails of type LineString.
        """

        rails = [shgeo.LineString(self.flatten_subpath(rail)) for rail in self.rails]

        path_lists = [[], []]

        for i, rail in enumerate(rails):
            before, after = cut(rail, rail.project(shgeo.Point(cut_points[i])))
            path_lists[0].append(before)
            path_lists[1].append(after)

        return path_lists

    def _assign_rungs_to_split_rails(self, split_rails):
        """Add this satin's rungs to the new satins.

        Each rung is appended to the correct one of the two new satin columns.
        """

        rungs = [shgeo.LineString(self.flatten_subpath(rung)) for rung in self.rungs]
        for path_list in split_rails:
            path_list.extend(rung for rung in rungs if path_list[0].intersects(rung) and path_list[1].intersects(rung))

    def _add_rungs_if_necessary(self, path_lists):
        """Add an additional rung to each new satin if needed.

        Case #1: If the split point is between the end and the last rung, then
        one of the satins will have no rungs.  It will be treated as an old-style
        satin, but it may not have an equal number of points in each rail.  Adding
        a rung will make it stitch properly.

        Case #2: If one of the satins ends up with exactly two rungs, it's
        ambiguous which of the subpaths are rails and which are rungs.  Adding
        another rung disambiguates this case.  See rail_indices() above for more
        information.
        """

        for path_list in path_lists:
            if len(path_list) in (2, 4):
                # Add the rung just after the start of the satin.
                rung_start = path_list[0].interpolate(0.1)
                rung_end = path_list[1].interpolate(0.1)
                rung = shgeo.LineString((rung_start, rung_end))

                # make it a bit bigger so that it definitely intersects
                rung = shaffinity.scale(rung, 1.1, 1.1)

                path_list.append(rung)

    def _path_list_to_satins(self, path_list):
        return self._csp_to_satin(line_strings_to_csp(path_list))

    def _csp_to_satin(self, csp):
        node = deepcopy(self.node)
        d = paths.CubicSuperPath(csp).to_path()
        node.set("d", d)

        # we've already applied the transform, so get rid of it
        if node.get("transform"):
            del node.attrib["transform"]

        return SatinColumn(node)

    @property
    @cache
    def center_line(self):
        # similar technique to do_center_walk()
        center_walk, _ = self.plot_points_on_rails(self.zigzag_spacing, -100000)
        return shgeo.LineString(center_walk)

    def offset_points(self, pos1, pos2, offset_px):
        # Expand or contract two points about their midpoint.  This is
        # useful for pull compensation and insetting underlay.

        distance = (pos1 - pos2).length()

        if distance < 0.0001:
            # if they're the same point, we don't know which direction
            # to offset in, so we have to just return the points
            return pos1, pos2

        # don't contract beyond the midpoint, or we'll start expanding
        if offset_px < -distance / 2.0:
            offset_px = -distance / 2.0

        pos1 = pos1 + (pos1 - pos2).unit() * offset_px
        pos2 = pos2 + (pos2 - pos1).unit() * offset_px

        return pos1, pos2

    def walk(self, path, start_pos, start_index, distance):
        # Move <distance> pixels along <path>, which is a sequence of line
        # segments defined by points.

        # <start_index> is the index of the line segment in <path> that
        # we're currently on.  <start_pos> is where along that line
        # segment we are.  Return a new position and index.

        # print >> dbg, "walk", start_pos, start_index, distance

        pos = start_pos
        index = start_index
        last_index = len(path) - 1
        distance_remaining = distance

        while True:
            if index >= last_index:
                return pos, index

            segment_end = path[index + 1]
            segment = segment_end - pos
            segment_length = segment.length()

            if segment_length > distance_remaining:
                # our walk ends partway along this segment
                return pos + segment.unit() * distance_remaining, index
            else:
                # our walk goes past the end of this segment, so advance
                # one point
                index += 1
                distance_remaining -= segment_length
                pos = segment_end

    def plot_points_on_rails(self, spacing, offset):
        # Take a section from each rail in turn, and plot out an equal number
        # of points on both rails.  Return the points plotted. The points will
        # be contracted or expanded by offset using self.offset_points().

        def add_pair(pos0, pos1):
            pos0, pos1 = self.offset_points(pos0, pos1, offset)
            points[0].append(pos0)
            points[1].append(pos1)

        points = [[], []]

        to_travel = 0

        for section0, section1 in self.flattened_sections:
            # Take one section at a time, delineated by the rungs.  For each
            # one, we want to try to travel proportionately on each rail as
            # we go between stitches.  For example, for the letter O, the
            # outside rail is longer than the inside rail.  We need to travel
            # further on the outside rail between each stitch than we do
            # on the inside rail.

            pos0 = section0[0]
            pos1 = section1[0]

            len0 = shgeo.LineString(section0).length
            len1 = shgeo.LineString(section1).length

            last_index0 = len(section0) - 1
            last_index1 = len(section1) - 1

            ratio = len1 / len0

            index0 = 0
            index1 = 0

            while index0 < last_index0 and index1 < last_index1:
                # Each iteration of this outer loop is one stitch.  Keep going
                # until we fall off the end of the section.

                # TODO: is there an other way?
                # old_center = (pos0 + pos1) / 2.0
                old_center = shgeo.Point(x/2 for x in (pos0 + pos1))

                while to_travel > 0 and index0 < last_index0 and index1 < last_index1:
                    # In this loop, we inch along each rail a tiny bit per
                    # iteration.  The goal is to travel the requested spacing
                    # amount along the _centerline_ between the two rails.
                    #
                    # Why not just travel the requested amount along the rails
                    # themselves?  Imagine a letter V.  The distance we travel
                    # along the rails themselves is much longer than the distance
                    # between the horizontal stitches themselves:
                    #
                    # \______/
                    #  \____/
                    #   \__/
                    #    \/
                    #
                    # For more complicated rail shapes, the distance between each
                    # stitch will vary as the angles of the rails vary.  The
                    # easiest way to compensate for this is to just go a tiny bit
                    # at a time and see how far we went.

                    # Note that this is 0.05 pixels, which is around 0.01mm, way
                    # smaller than the resolution of an embroidery machine.
                    pos0, index0 = self.walk(section0, pos0, index0, 0.05)
                    pos1, index1 = self.walk(section1, pos1, index1, 0.05 * ratio)

                    # TODO: is there a better way?
                    # new_center = (pos0 + pos1) / 2.0
                    new_center = shgeo.Point(x/2 for x in (pos0 + pos1))
                    to_travel -= new_center.distance(old_center)
                    old_center = new_center

                if to_travel <= 0:
                    add_pair(pos0, pos1)
                    to_travel = spacing

        if to_travel > 0:
            add_pair(pos0, pos1)

        return points

    def do_contour_underlay(self):
        # "contour walk" underlay: do stitches up one side and down the
        # other.
        forward, back = self.plot_points_on_rails(self.contour_underlay_stitch_length,
                                                  -self.contour_underlay_inset)
        return Patch(color=self.color, stitches=(forward + list(reversed(back))))

    def do_center_walk(self):
        # Center walk underlay is just a running stitch down and back on the
        # center line between the bezier curves.

        # Do it like contour underlay, but inset all the way to the center.
        forward, back = self.plot_points_on_rails(self.center_walk_underlay_stitch_length,
                                                  -100000)
        return Patch(color=self.color, stitches=(forward + list(reversed(back))))

    def do_zigzag_underlay(self):
        # zigzag underlay, usually done at a much lower density than the
        # satin itself.  It looks like this:
        #
        # \/\/\/\/\/\/\/\/\/\/|
        # /\/\/\/\/\/\/\/\/\/\|
        #
        # In combination with the "contour walk" underlay, this is the
        # "German underlay" described here:
        #   http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/

        patch = Patch(color=self.color)

        sides = self.plot_points_on_rails(self.zigzag_underlay_spacing / 2.0,
                                          -self.zigzag_underlay_inset)

        # This organizes the points in each side in the order that they'll be
        # visited.
        sides = [sides[0][::2] + list(reversed(sides[0][1::2])),
                 sides[1][1::2] + list(reversed(sides[1][::2]))]

        # This fancy bit of iterable magic just repeatedly takes a point
        # from each side in turn.
        for point in chain.from_iterable(zip(*sides)):
            patch.add_stitch(point)

        return patch

    def do_satin(self):
        # satin: do a zigzag pattern, alternating between the paths.  The
        # zigzag looks like this to make the satin stitches look perpendicular
        # to the column:
        #
        # |/|/|/|/|/|/|/|/|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        patch = Patch(color=self.color)

        sides = self.plot_points_on_rails(self.zigzag_spacing, self.pull_compensation)

        # Like in zigzag_underlay(): take a point from each side in turn.
        for point in chain.from_iterable(zip(*sides)):
            patch.add_stitch(point)

        return patch

    def do_e_stitch(self):
        # e stitch: do a pattern that looks like the letter "E".  It looks like
        # this:
        #
        # _|_|_|_|_|_|_|_|_|_|_|_|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        patch = Patch(color=self.color)

        sides = self.plot_points_on_rails(self.zigzag_spacing, self.pull_compensation)

        # "left" and "right" here are kind of arbitrary designations meaning
        # a point from the first and second rail repectively
        for left, right in zip(*sides):
            patch.add_stitch(left)
            patch.add_stitch(right)
            patch.add_stitch(left)

        return patch

    def to_patches(self, last_patch):
        # Stitch a variable-width satin column, zig-zagging between two paths.

        # The algorithm will draw zigzags between each consecutive pair of
        # beziers.  The boundary points between beziers serve as "checkpoints",
        # allowing the user to control how the zigzags flow around corners.

        patch = Patch(color=self.color)

        if self.center_walk_underlay:
            patch += self.do_center_walk()

        if self.contour_underlay:
            patch += self.do_contour_underlay()

        if self.zigzag_underlay:
            # zigzag underlay comes after contour walk underlay, so that the
            # zigzags sit on the contour walk underlay like rail ties on rails.
            patch += self.do_zigzag_underlay()

        if self.e_stitch:
            patch += self.do_e_stitch()
        else:
            patch += self.do_satin()

        return [patch]
