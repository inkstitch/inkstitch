from itertools import chain, izip
from shapely import geometry as shgeo, ops as shops

from .element import param, EmbroideryElement, Patch
from ..i18n import _
from ..utils import cache, Point


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
    @param('zigzag_spacing_mm', _('Zig-zag spacing (peak-to-peak)'), tooltip=_('Peak-to-peak distance between zig-zags.'), unit='mm', type='float', default=0.4)
    def zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param('pull_compensation_mm', _('Pull compensation'), tooltip=_('Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape.  This setting expands each pair of needle penetrations outward from the center of the satin column.'), unit='mm', type='float', default=0)
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
    @param('contour_underlay_inset_mm', _('Contour underlay inset amount'), tooltip=_('Shrink the outline, to prevent the underlay from showing around the outside of the satin column.'), unit='mm', group=_('Contour Underlay'), type='float', default=0.4)
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
    @param('center_walk_underlay_stitch_length_mm', _('Stitch length'), tooltip=_('Length of each stitch.'), unit='mm', group=_('Center-Walk Underlay'), type='float', default=1.5)
    def center_walk_underlay_stitch_length(self):
        return max(self.get_float_param("center_walk_underlay_stitch_length_mm", 1.5), 0.01)

    @property
    @param('zigzag_underlay', _('Zig-zag underlay'), type='toggle', group=_('Zig-zag Underlay'))
    def zigzag_underlay(self):
        return self.get_boolean_param("zigzag_underlay")

    @property
    @param('zigzag_underlay_spacing_mm', _('Zig-Zag spacing (peak-to-peak)'), tooltip=_('Distance between peaks of the zig-zags.'), unit='mm', group=_('Zig-zag Underlay'), type='float', default=3)
    def zigzag_underlay_spacing(self):
        return max(self.get_float_param("zigzag_underlay_spacing_mm", 3), 0.01)

    @property
    @param('zigzag_underlay_inset_mm', _('Inset amount'), tooltip=_('default: half of contour underlay inset'), unit='mm', group=_('Zig-zag Underlay'), type='float', default="")
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
    def flattened_beziers(self):
        if len(self.csp) == 2:
            return self.simple_flatten_beziers()
        elif len(self.csp) < 2:
            self.fatal(_("satin column: %(id)s: at least two subpaths required (%(num)d found)") % dict(num=len(self.csp), id=self.node.get('id')))
        else:
            return self.flatten_beziers_with_rungs()


    def flatten_beziers_with_rungs(self):
        input_paths = [self.flatten([path]) for path in self.csp]
        input_paths = [shgeo.LineString(path[0]) for path in input_paths]

        paths = input_paths[:]
        paths.sort(key=lambda path: path.length, reverse=True)

        # Imagine a satin column as a curvy ladder.
        # The two long paths are the "rails" of the ladder.  The remainder are
        # the "rungs".
        rails = paths[:2]
        rungs = shgeo.MultiLineString(paths[2:])

        # The rails should stay in the order they were in the original CSP.
        # (this lets the user control where the satin starts and ends)
        rails.sort(key=lambda rail: input_paths.index(rail))

        result = []

        for rail in rails:
            if not rail.is_simple:
                self.fatal(_("One or more rails crosses itself, and this is not allowed.  Please split into multiple satin columns."))

            # handle null intersections here?
            linestrings = shops.split(rail, rungs)

            #print >> dbg, "rails and rungs", [str(rail) for rail in rails], [str(rung) for rung in rungs]
            if len(linestrings.geoms) < len(rungs.geoms) + 1:
                self.fatal(_("satin column: One or more of the rungs doesn't intersect both rails.") + "  " + _("Each rail should intersect both rungs once."))
            elif len(linestrings.geoms) > len(rungs.geoms) + 1:
                self.fatal(_("satin column: One or more of the rungs intersects the rails more than once.") + "  " + _("Each rail should intersect both rungs once."))

            paths = [[Point(*coord) for coord in ls.coords] for ls in linestrings.geoms]
            result.append(paths)

        return zip(*result)


    def simple_flatten_beziers(self):
        # Given a pair of paths made up of bezier segments, flatten
        # each individual bezier segment into line segments that approximate
        # the curves.  Retain the divisions between beziers -- we'll use those
        # later.

        paths = []

        for path in self.csp:
            # See the documentation in the parent class for parse_path() for a
            # description of the format of the CSP.  Each bezier is constructed
            # using two neighboring 3-tuples in the list.

            flattened_path = []

            # iterate over pairs of 3-tuples
            for prev, current in zip(path[:-1], path[1:]):
                flattened_segment = self.flatten([[prev, current]])
                flattened_segment = [Point(x, y) for x, y in flattened_segment[0]]
                flattened_path.append(flattened_segment)

            paths.append(flattened_path)

        return zip(*paths)

    def validate_satin_column(self):
        # The node should have exactly two paths with no fill.  Each
        # path should have the same number of points, meaning that they
        # will both be made up of the same number of bezier curves.

        node_id = self.node.get("id")

        if self.get_style("fill") is not None:
            self.fatal(_("satin column: object %s has a fill (but should not)") % node_id)

        if len(self.csp) == 2:
            if len(self.csp[0]) != len(self.csp[1]):
                self.fatal(_("satin column: object %(id)s has two paths with an unequal number of points (%(length1)d and %(length2)d)") % \
                             dict(id=node_id, length1=len(self.csp[0]), length2=len(self.csp[1])))

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

    def walk_paths(self, spacing, offset):
        # Take a bezier segment from each path in turn, and plot out an
        # equal number of points on each bezier.  Return the points plotted.
        # The points will be contracted or expanded by offset using
        # offset_points().

        points = [[], []]

        def add_pair(pos1, pos2):
            pos1, pos2 = self.offset_points(pos1, pos2, offset)
            points[0].append(pos1)
            points[1].append(pos2)

        # We may not be able to fit an even number of zigzags in each pair of
        # beziers.  We'll store the remaining bit of the beziers after handling
        # each section.
        remainder_path1 = []
        remainder_path2 = []

        for segment1, segment2 in self.flattened_beziers:
            subpath1 = remainder_path1 + segment1
            subpath2 = remainder_path2 + segment2

            len1 = shgeo.LineString(subpath1).length
            len2 = shgeo.LineString(subpath2).length

            # Base the number of stitches in each section on the _longest_ of
            # the two beziers. Otherwise, things could get too sparse when one
            # side is significantly longer (e.g. when going around a corner).
            # The risk here is that we poke a hole in the fabric if we try to
            # cram too many stitches on the short bezier.  The user will need
            # to avoid this through careful construction of paths.
            #
            # TODO: some commercial machine embroidery software compensates by
            # pulling in some of the "inner" stitches toward the center a bit.

            # note, this rounds down using integer-division
            num_points = max(len1, len2) / spacing

            spacing1 = len1 / num_points
            spacing2 = len2 / num_points

            pos1 = subpath1[0]
            index1 = 0

            pos2 = subpath2[0]
            index2 = 0

            for i in xrange(int(num_points)):
                add_pair(pos1, pos2)

                pos1, index1 = self.walk(subpath1, pos1, index1, spacing1)
                pos2, index2 = self.walk(subpath2, pos2, index2, spacing2)

            if index1 < len(subpath1) - 1:
                remainder_path1 = [pos1] + subpath1[index1 + 1:]
            else:
                remainder_path1 = []

            if index2 < len(subpath2) - 1:
                remainder_path2 = [pos2] + subpath2[index2 + 1:]
            else:
                remainder_path2 = []

        # We're off by one in the algorithm above, so we need one more
        # pair of points.  We also want to add points at the very end to
        # make sure we match the vectors on screen as best as possible.
        # Try to avoid doing both if they're going to stack up too
        # closely.

        end1 = remainder_path1[-1]
        end2 = remainder_path2[-1]

        if (end1 - pos1).length() > 0.3 * spacing:
            add_pair(pos1, pos2)

        add_pair(end1, end2)

        return points

    def do_contour_underlay(self):
        # "contour walk" underlay: do stitches up one side and down the
        # other.
        forward, back = self.walk_paths(self.contour_underlay_stitch_length,
                                        -self.contour_underlay_inset)
        return Patch(color=self.color, stitches=(forward + list(reversed(back))))

    def do_center_walk(self):
        # Center walk underlay is just a running stitch down and back on the
        # center line between the bezier curves.

        # Do it like contour underlay, but inset all the way to the center.
        forward, back = self.walk_paths(self.center_walk_underlay_stitch_length,
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

        sides = self.walk_paths(self.zigzag_underlay_spacing / 2.0,
                                -self.zigzag_underlay_inset)

        # This organizes the points in each side in the order that they'll be
        # visited.
        sides = [sides[0][::2] + list(reversed(sides[0][1::2])),
                 sides[1][1::2] + list(reversed(sides[1][::2]))]

        # This fancy bit of iterable magic just repeatedly takes a point
        # from each side in turn.
        for point in chain.from_iterable(izip(*sides)):
            patch.add_stitch(point)

        return patch

    def do_satin(self):
        # satin: do a zigzag pattern, alternating between the paths.  The
        # zigzag looks like this to make the satin stitches look perpendicular
        # to the column:
        #
        # /|/|/|/|/|/|/|/|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        patch = Patch(color=self.color)

        sides = self.walk_paths(self.zigzag_spacing, self.pull_compensation)

        # Like in zigzag_underlay(): take a point from each side in turn.
        for point in chain.from_iterable(izip(*sides)):
            patch.add_stitch(point)

        return patch

    def do_e_stitch(self):
        # e stitch: do a pattern that looks like the letter "E".  It looks like
        # this:
        #
        # _|_|_|_|_|_|_|_|_|_|_|_|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        patch = Patch(color=self.color)

        sides = self.walk_paths(self.zigzag_spacing, self.pull_compensation)

        # "left" and "right" here are kind of arbitrary designations meaning
        # a point from the first and second rail repectively
        for left, right in izip(*sides):
            patch.add_stitch(left)
            patch.add_stitch(right)
            patch.add_stitch(left)

        return patch


    def to_patches(self, last_patch):
        # Stitch a variable-width satin column, zig-zagging between two paths.

        # The algorithm will draw zigzags between each consecutive pair of
        # beziers.  The boundary points between beziers serve as "checkpoints",
        # allowing the user to control how the zigzags flow around corners.

        # First, verify that we have valid paths.
        self.validate_satin_column()

        patches = []

        if self.center_walk_underlay:
            patches.append(self.do_center_walk())

        if self.contour_underlay:
            patches.append(self.do_contour_underlay())

        if self.zigzag_underlay:
            # zigzag underlay comes after contour walk underlay, so that the
            # zigzags sit on the contour walk underlay like rail ties on rails.
            patches.append(self.do_zigzag_underlay())

        if self.e_stitch:
            patches.append(self.do_e_stitch())
        else:
            patches.append(self.do_satin())

        return patches
