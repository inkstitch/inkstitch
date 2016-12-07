#!/usr/bin/python
#
# documentation: see included index.html
# LICENSE:
# Copyright 2010 by Jon Howell,
# Originally licensed under <a href="http://www.gnu.org/licenses/quick-guide-gplv3.html">GPLv3</a>.
# Copyright 2015 by Bas Wijnen <wijnen@debian.org>.
# New parts are licensed under AGPL3 or later.
# (Note that this means this work is licensed under the common part of those two: AGPL version 3.)
#
# Important resources:
# lxml interface for walking SVG tree:
# http://codespeak.net/lxml/tutorial.html#elementpath
# Inkscape library for extracting paths from SVG:
# http://wiki.inkscape.org/wiki/index.php/Python_modules_for_extensions#simplepath.py
# Shapely computational geometry library:
# http://gispython.org/shapely/manual.html#multipolygons
# Embroidery file format documentation:
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
import subprocess
from copy import deepcopy
import time
from itertools import chain, izip
import inkex
import simplepath
import simplestyle
import simpletransform
from bezmisc import bezierlength, beziertatlength, bezierpointatt
from cspsubdiv import cspsubdiv
import cubicsuperpath
import math
import lxml.etree as etree
import shapely.geometry as shgeo
import shapely.affinity as affinity
import shapely.ops
from pprint import pformat

import PyEmb
#from PyEmb import cache

dbg = open("./embroider-debug.txt", "w")
PyEmb.dbg = dbg

SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')


class Param(object):
    def __init__(self, name, description, unit=None, values=[], type=None, group=None, inverse=False, default=None):
        self.name = name
        self.description = description
        self.unit = unit
        self.values = values or [""]
        self.type = type
        self.group = group
        self.inverse = inverse
        self.default = default

    def __repr__(self):
        return "Param(%s)" % vars(self)

# Decorate a member function or property with information about
# the embroidery parameter it corresponds to
def param(*args, **kwargs):
    p = Param(*args, **kwargs)

    def decorator(func):
        func.param = p
        return func

    return decorator

class EmbroideryElement(object):
    def __init__(self, node, options=None):
        self.node = node
        self.options = options

    @property
    def id(self):
        return self.node.get('id')

    @classmethod
    def get_params(cls):
        params = []
        for attr in dir(cls):
            prop = getattr(cls, attr)
            if isinstance(prop, property):
                # The 'param' attribute is set by the 'param' decorator defined above.
                if hasattr(prop.fget, 'param'):
                    params.append(prop.fget.param)

        return params

    #@cache
    def get_param(self, param, default):
        value = self.node.get("embroider_" + param, "").strip()

        if not value:
            value = getattr(self.options, param, default)

        return value

    #@cache
    def get_boolean_param(self, param, default=None):
        value = self.get_param(param, default)

        if isinstance(value, bool):
            return value
        else:
            return value and (value.lower() in ('yes', 'y', 'true', 't', '1'))

    #@cache
    def get_float_param(self, param, default=None):
        try:
            value = float(self.get_param(param, default))
        except (TypeError, ValueError):
            return default

        if param.endswith('_mm'):
            # print >> dbg, "get_float_param", param, value, "*", self.options.pixels_per_mm
            value = value * self.options.pixels_per_mm

        return value

    #@cache
    def get_int_param(self, param, default=None):
        try:
            value = int(self.get_param(param, default))
        except (TypeError, ValueError):
            return default

        if param.endswith('_mm'):
            value = int(value * self.options.pixels_per_mm)

        return value

    def set_param(self, name, value):
        self.node.set("embroider_%s" % name, str(value))

    #@cache
    def get_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        if (style_name not in style):
            return None
        value = style[style_name]
        if value == 'none':
            return None
        return value

    #@cache
    def has_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        return style_name in style

    #@cache
    def parse_path(self):
        # A CSP is a  "cubic superpath".
        #
        # A "path" is a sequence of strung-together bezier curves.
        #
        # A "superpath" is a collection of paths that are all in one object.
        #
        # The "cubic" bit in "cubic superpath" is because the bezier curves
        # inkscape uses involve cubic polynomials.
        #
        # Each path is a collection of tuples, each of the form:
        #
        # (control_before, point, control_after)
        #
        # A bezier curve segment is defined by an endpoint, a control point,
        # a second control point, and a final endpoint.  A path is a bunch of
        # bezier curves strung together.  One could represent a path as a set
        # of four-tuples, but there would be redundancy because the ending
        # point of one bezier is the starting point of the next.  Instead, a
        # path is a set of 3-tuples as shown above, and one must construct
        # each bezier curve by taking the appropriate endpoints and control
        # points.  Bleh. It should be noted that a straight segment is
        # represented by having the control point on each end equal to that
        # end's point.
        #
        # In a path, each element in the 3-tuple is itself a tuple of (x, y).
        # Tuples all the way down.  Hasn't anyone heard of using classes?

        path = cubicsuperpath.parsePath(self.node.get("d"))

        # print >> sys.stderr, pformat(path)

        # start with the identity transform
        transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

        # combine this node's transform with all parent groups' transforms
        transform = simpletransform.composeParents(self.node, transform)

        # apply the combined transform to this node's path
        simpletransform.applyTransformToPath(transform, path)

        return path

    def flatten(self, path):
        """approximate a path containing beziers with a series of points"""

        path = deepcopy(path)

        cspsubdiv(path, self.options.flat)

        flattened = []

        for comp in path:
            vertices = []
            for ctl in comp:
                vertices.append((ctl[1][0], ctl[1][1]))
            flattened.append(vertices)

        return flattened

    def to_patches(self, last_patch):
        raise NotImplementedError("%s must implement to_path()" % self.__class__.__name__)

    def fatal(self, message):
        print >> sys.stderr, "error:", message
        sys.exit(1)


class Fill(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super(Fill, self).__init__(*args, **kwargs)

    @property
    @param('auto_fill', 'Manually routed fill stitching', type='toggle', inverse=True, default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('angle', 'Angle of lines of stitches', unit='deg', type='float')
    #@cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    def color(self):
        return self.get_style("fill")

    @property
    @param('flip', 'Flip fill (start right-to-left)', type='boolean')
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm', 'Spacing between rows', unit='mm', type='float')
    def row_spacing(self):
        return self.get_float_param("row_spacing_mm")

    @property
    @param('max_stitch_length_mm', 'Maximum fill stitch length', unit='mm', type='float')
    def max_stitch_length(self):
        return self.get_float_param("max_stitch_length_mm")

    @property
    @param('staggers', 'Stagger rows this many times before repeating', type='int')
    def staggers(self):
        return self.get_int_param("staggers", 4)

    @property
    #@cache
    def paths(self):
        return self.flatten(self.parse_path())

    @property
    #@cache
    def shape(self):
        poly_ary = []
        for sub_path in self.paths:
            point_ary = []
            last_pt = None
            for pt in sub_path:
                if (last_pt is not None):
                    vp = (pt[0] - last_pt[0], pt[1] - last_pt[1])
                    dp = math.sqrt(math.pow(vp[0], 2.0) + math.pow(vp[1], 2.0))
                    # dbg.write("dp %s\n" % dp)
                    if (dp > 0.01):
                        # I think too-close points confuse shapely.
                        point_ary.append(pt)
                        last_pt = pt
                else:
                    last_pt = pt
            poly_ary.append(point_ary)

        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        # TODO: actually figure out which things are holes and which are shells
        poly_ary.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)

        polygon = shgeo.MultiPolygon([(poly_ary[0], poly_ary[1:])])
        # print >> sys.stderr, "polygon valid:", polygon.is_valid
        return polygon

    #@cache
    def east(self, angle):
        # "east" is the name of the direction that is to the right along a row
        return PyEmb.Point(1, 0).rotate(-angle)

    #@cache
    def north(self, angle):
        return self.east(angle).rotate(math.pi / 2)

    def adjust_stagger(self, stitch, angle, row_spacing, max_stitch_length):
        row_num = round((stitch * self.north(angle)) / row_spacing)
        row_stagger = row_num % self.staggers
        stagger_offset = (float(row_stagger) / self.staggers) * max_stitch_length
        offset = ((stitch * self.east(angle)) - stagger_offset) % max_stitch_length

        return stitch - offset * self.east(angle)

    def intersect_region_with_grating(self, angle=None, row_spacing=None):
        if angle is None:
            angle = self.angle

        if row_spacing is None:
            row_spacing = self.row_spacing

        # the max line length I'll need to intersect the whole shape is the diagonal
        (minx, miny, maxx, maxy) = self.shape.bounds
        upper_left = PyEmb.Point(minx, miny)
        lower_right = PyEmb.Point(maxx, maxy)
        length = (upper_left - lower_right).length()
        half_length = length / 2.0

        # Now get a unit vector rotated to the requested angle.  I use -angle
        # because shapely rotates clockwise, but my geometry textbooks taught
        # me to consider angles as counter-clockwise from the X axis.
        direction = PyEmb.Point(1, 0).rotate(-angle)

        # and get a normal vector
        normal = direction.rotate(math.pi / 2)

        # I'll start from the center, move in the normal direction some amount,
        # and then walk left and right half_length in each direction to create
        # a line segment in the grating.
        center = PyEmb.Point((minx + maxx) / 2.0, (miny + maxy) / 2.0)

        # I need to figure out how far I need to go along the normal to get to
        # the edge of the shape.  To do that, I'll rotate the bounding box
        # angle degrees clockwise and ask for the new bounding box.  The max
        # and min y tell me how far to go.

        _, start, _, end = affinity.rotate(self.shape, angle, origin='center', use_radians=True).bounds

        # convert start and end to be relative to center (simplifies things later)
        start -= center.y
        end -= center.y

        # offset start slightly so that rows are always an even multiple of
        # row_spacing_px from the origin.  This makes it so that abutting
        # fill regions at the same angle and spacing always line up nicely.
        start -= (start + normal * center) % row_spacing

        rows = []

        while start < end:
            p0 = center + normal * start + direction * half_length
            p1 = center + normal * start - direction * half_length
            endpoints = [p0.as_tuple(), p1.as_tuple()]
            grating_line = shgeo.LineString(endpoints)

            res = grating_line.intersection(self.shape)

            if (isinstance(res, shgeo.MultiLineString)):
                runs = map(lambda line_string: line_string.coords, res.geoms)
            else:
                if res.is_empty or len(res.coords) == 1:
                    # ignore if we intersected at a single point or no points
                    start += row_spacing
                    continue
                runs = [res.coords]

            runs.sort(key=lambda seg: (PyEmb.Point(*seg[0]) - upper_left).length())

            if self.flip:
                runs.reverse()
                runs = map(lambda run: tuple(reversed(run)), runs)

            rows.append(runs)

            start += row_spacing

        return rows

    def is_same_run(self, segment1, segment2):
        if shgeo.LineString(segment1).distance(shgeo.LineString(segment2)) > self.row_spacing * 1.001:
            return False
        return True

    def pull_runs(self, rows):
        # Given a list of rows, each containing a set of line segments,
        # break the area up into contiguous patches of line segments.
        #
        # This is done by repeatedly pulling off the first line segment in
        # each row and calling that a shape.  We have to be careful to make
        # sure that the line segments are part of the same shape.  Consider
        # the letter "H", with an embroidery angle of 45 degrees.  When
        # we get to the bottom of the lower left leg, the next row will jump
        # over to midway up the lower right leg.  We want to stop there and
        # start a new patch.

        # for row in rows:
        #    print >> sys.stderr, len(row)

        # print >>sys.stderr, "\n".join(str(len(row)) for row in rows)

        runs = []
        count = 0
        while (len(rows) > 0):
            run = []
            prev = None

            for row_num in xrange(len(rows)):
                row = rows[row_num]
                first, rest = row[0], row[1:]

                # TODO: only accept actually adjacent rows here
                if prev is not None and not self.is_same_run(prev, first):
                    break

                run.append(first)
                prev = first

                rows[row_num] = rest

            # print >> sys.stderr, len(run)
            runs.append(run)
            rows = [row for row in rows if len(row) > 0]

            count += 1

        return runs

    def section_to_patch(self, group_of_segments, angle=None, row_spacing=None, max_stitch_length=None):
        if max_stitch_length is None:
            max_stitch_length = self.max_stitch_length

        if row_spacing is None:
            row_spacing = self.row_spacing

        if angle is None:
            angle = self.angle

        # print >> sys.stderr, len(groups_of_segments)

        patch = Patch(color=self.color)
        first_segment = True
        swap = False
        last_end = None

        for segment in group_of_segments:
            # We want our stitches to look like this:
            #
            # ---*-----------*-----------
            # ------*-----------*--------
            # ---------*-----------*-----
            # ------------*-----------*--
            # ---*-----------*-----------
            #
            # Each successive row of stitches will be staggered, with
            # num_staggers rows before the pattern repeats.  A value of
            # 4 gives a nice fill while hiding the needle holes.  The
            # first row is offset 0%, the second 25%, the third 50%, and
            # the fourth 75%.
            #
            # Actually, instead of just starting at an offset of 0, we
            # can calculate a row's offset relative to the origin.  This
            # way if we have two abutting fill regions, they'll perfectly
            # tile with each other.  That's important because we often get
            # abutting fill regions from pull_runs().

            (beg, end) = segment

            if (swap):
                (beg, end) = (end, beg)

            beg = PyEmb.Point(*beg)
            end = PyEmb.Point(*end)

            row_direction = (end - beg).unit()
            segment_length = (end - beg).length()

            # only stitch the first point if it's a reasonable distance away from the
            # last stitch
            if last_end is None or (beg - last_end).length() > 0.1 * self.options.pixels_per_mm:
                patch.add_stitch(beg)

            first_stitch = self.adjust_stagger(beg, angle, row_spacing, max_stitch_length)

            # we might have chosen our first stitch just outside this row, so move back in
            if (first_stitch - beg) * row_direction < 0:
                first_stitch += row_direction * max_stitch_length

            offset = (first_stitch - beg).length()

            while offset < segment_length:
                patch.add_stitch(beg + offset * row_direction)
                offset += max_stitch_length

            if (end - patch.stitches[-1]).length() > 0.1 * self.options.pixels_per_mm:
                patch.add_stitch(end)

            last_end = end
            swap = not swap

        return patch

    def to_patches(self, last_patch):
        rows_of_segments = self.intersect_region_with_grating()
        groups_of_segments = self.pull_runs(rows_of_segments)

        return [self.section_to_patch(group) for group in groups_of_segments]


class AutoFill(Fill):
    @property
    @param('auto_fill', 'Automatically routed fill stitching', type='toggle', default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    #@cache
    def outline(self):
        return self.shape.boundary[0]

    @property
    #@cache
    def outline_length(self):
        return self.outline.length

    @property
    def flip(self):
        return False

    @property
    @param('running_stitch_length_mm', 'Running stitch length (traversal between sections)', unit='mm', type='float')
    def running_stitch_length(self):
        return self.get_float_param("running_stitch_length_mm")

    @property
    @param('fill_underlay', 'Underlay', type='toggle', group='AutoFill Underlay')
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay")

    @property
    @param('fill_underlay_angle', 'Fill angle (default: fill angle + 90 deg)', unit='deg', group='AutoFill Underlay', type='float')
    #@cache
    def fill_underlay_angle(self):
        underlay_angle = self.get_float_param("fill_underlay_angle")

        if underlay_angle:
            return math.radians(underlay_angle)
        else:
            return self.angle + math.pi / 2.0

    @property
    @param('fill_underlay_row_spacing_mm', 'Row spacing (default: 3x fill row spacing)', unit='mm', group='AutoFill Underlay', type='float')
    #@cache
    def fill_underlay_row_spacing(self):
        return self.get_float_param("fill_underlay_row_spacing_mm") or self.row_spacing * 3

    @property
    @param('fill_underlay_max_stitch_length_mm', 'Max stitch length', unit='mm', group='AutoFill Underlay', type='float')
    #@cache
    def fill_underlay_max_stitch_length(self):
        return self.get_float_param("fill_underlay_max_stitch_length_mm" or self.max_stitch_length)

    def validate(self):
        if len(self.shape.boundary) > 1:
            self.fatal("auto-fill: object %s cannot be auto-filled because it has one or more holes.  Please disable auto-fill for this object or break it into separate objects without holes." % self.node.get('id'))

    def is_same_run(self, segment1, segment2):
        if shgeo.Point(segment1[0]).distance(shgeo.Point(segment2[0])) > self.max_stitch_length:
            return False

        if shgeo.Point(segment1[1]).distance(shgeo.Point(segment2[1])) > self.max_stitch_length:
            return False

        return True

    def perimeter_distance(self, p1, p2):
        # how far around the perimeter (and in what direction) do I need to go
        # to get from p1 to p2?

        p1_projection = self.outline.project(shgeo.Point(p1))
        p2_projection = self.outline.project(shgeo.Point(p2))

        distance = p2_projection - p1_projection

        if abs(distance) > self.outline_length / 2.0:
            # if we'd have to go more than halfway around, it's faster to go
            # the other way
            if distance < 0:
                return distance + self.outline_length
            elif distance > 0:
                return distance - self.outline_length
            else:
                # this ought not happen, but just for completeness, return 0 if
                # p1 and p0 are the same point
                return 0
        else:
            return distance

    def connect_points(self, p1, p2):
        patch = Patch(color=self.color)

        pos = self.outline.project(shgeo.Point(p1))
        distance = self.perimeter_distance(p1, p2)
        stitches = abs(int(distance / self.running_stitch_length))

        direction = math.copysign(1.0, distance)
        one_stitch = self.running_stitch_length * direction

        for i in xrange(stitches):
            pos = (pos + one_stitch) % self.outline_length

            stitch = PyEmb.Point(*self.outline.interpolate(pos).coords[0])

            # if we're moving along the fill direction, adjust the stitch to
            # match the fill so it blends in
            if patch.stitches:
                if abs((stitch - patch.stitches[-1]) * self.north(self.angle)) < 0.01:
                    new_stitch = self.adjust_stagger(stitch, self.angle, self.row_spacing, self.max_stitch_length)

                    # don't push the point past the end of this section of the outline
                    if self.outline.distance(shgeo.Point(new_stitch)) <= 0.01:
                        stitch = new_stitch

            patch.add_stitch(stitch)

        return patch

    def get_corner_points(self, section):
        return section[0][0], section[0][-1], section[-1][0], section[-1][-1]

    def nearest_corner(self, section, point):
        return min(self.get_corner_points(section),
                   key=lambda corner: abs(self.perimeter_distance(point, corner)))

    def find_nearest_section(self, sections, point):
        sections_with_nearest_corner = [(i, self.nearest_corner(section, point))
                                        for i, section in enumerate(sections)]
        return min(sections_with_nearest_corner,
                   key=lambda(section, corner): abs(self.perimeter_distance(point, corner)))

    def section_from_corner(self, section, start_corner, angle, row_spacing, max_stitch_length):
        if start_corner not in section[0]:
            section = list(reversed(section))

        if section[0][0] != start_corner:
            section = [list(reversed(row)) for row in section]

        return self.section_to_patch(section, angle, row_spacing, max_stitch_length)

    def do_auto_fill(self, angle, row_spacing, max_stitch_length, starting_point=None):
        rows_of_segments = self.intersect_region_with_grating(angle, row_spacing)
        sections = self.pull_runs(rows_of_segments)

        patches = []
        last_stitch = starting_point
        while sections:
            if last_stitch:
                section_index, start_corner = self.find_nearest_section(sections, last_stitch)
                patches.append(self.connect_points(last_stitch, start_corner))
                patches.append(self.section_from_corner(sections.pop(section_index), start_corner, angle, row_spacing, max_stitch_length))
            else:
                patches.append(self.section_to_patch(sections.pop(0), angle, row_spacing, max_stitch_length))

            last_stitch = patches[-1].stitches[-1]

        return patches

    def to_patches(self, last_patch):
        print >> dbg, "autofill"
        self.validate()

        patches = []

        if last_patch is None:
            last_stitch = None
        else:
            last_stitch = last_patch.stitches[-1]

        if self.fill_underlay:
            patches.extend(self.do_auto_fill(self.fill_underlay_angle, self.fill_underlay_row_spacing, self.fill_underlay_max_stitch_length, last_stitch))
            last_stitch = patches[-1].stitches[-1]

        patches.extend(self.do_auto_fill(self.angle, self.row_spacing, self.max_stitch_length, last_stitch))

        return patches


class SergFill(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super(SergFill, self).__init__(*args, **kwargs)

    @property
    @param('auto_fill', 'Manually routed fill stitching', type='toggle', inverse=True, default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('angle', 'Angle of lines of stitches', unit='deg', type='float')
    #@cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    def color(self):
        return self.get_style("fill")

    @property
    @param('flip', 'Flip fill (start right-to-left)', type='boolean')
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm', 'Spacing between rows', unit='mm', type='float')
    def row_spacing(self):
        return self.get_float_param("row_spacing_mm")

    @property
    @param('max_stitch_length_mm', 'Maximum fill stitch length', unit='mm', type='float')
    def max_stitch_length(self):
        return self.get_float_param("max_stitch_length_mm")

    @property
    @param('staggers', 'Stagger rows this many times before repeating', type='int')
    def staggers(self):
        return self.get_int_param("staggers", 4)

    @property
    #@cache
    def paths(self):
        return self.flatten(self.parse_path())

    @property
    #@cache
    def shape(self):
        poly_ary = []
        for sub_path in self.paths:
            point_ary = []
            last_pt = None
            for pt in sub_path:
                if (last_pt is not None):
                    vp = (pt[0] - last_pt[0], pt[1] - last_pt[1])
                    dp = math.sqrt(math.pow(vp[0], 2.0) + math.pow(vp[1], 2.0))
                    # dbg.write("dp %s\n" % dp)
                    if (dp > 0.01):
                        # I think too-close points confuse shapely.
                        point_ary.append(pt)
                        last_pt = pt
                else:
                    last_pt = pt
            poly_ary.append(point_ary)

        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        # TODO: actually figure out which things are holes and which are shells
        poly_ary.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)

        polygon = shgeo.MultiPolygon([(poly_ary[0], poly_ary[1:])])
        # print >> sys.stderr, "polygon valid:", polygon.is_valid
        return polygon

    #@cache
    def east(self, angle):
        # "east" is the name of the direction that is to the right along a row
        return PyEmb.Point(1, 0).rotate(-angle)

    #@cache
    def north(self, angle):
        return self.east(angle).rotate(math.pi / 2)

    def adjust_stagger(self, stitch, angle, row_spacing, max_stitch_length):
        row_num = round((stitch * self.north(angle)) / row_spacing)
        row_stagger = row_num % self.staggers
        stagger_offset = (float(row_stagger) / self.staggers) * max_stitch_length
        offset = ((stitch * self.east(angle)) - stagger_offset) % max_stitch_length

        return stitch - offset * self.east(angle)

    def intersect_region_with_grating(self, angle=None, row_spacing=None):
        if angle is None:
            angle = self.angle

        if row_spacing is None:
            row_spacing = self.row_spacing

        # the max line length I'll need to intersect the whole shape is the diagonal
        (minx, miny, maxx, maxy) = self.shape.bounds
        upper_left = PyEmb.Point(minx, miny)
        lower_right = PyEmb.Point(maxx, maxy)
        length = (upper_left - lower_right).length()
        half_length = length / 2.0

        # Now get a unit vector rotated to the requested angle.  I use -angle
        # because shapely rotates clockwise, but my geometry textbooks taught
        # me to consider angles as counter-clockwise from the X axis.
        direction = PyEmb.Point(1, 0).rotate(-angle)

        # and get a normal vector
        normal = direction.rotate(math.pi / 2)

        # I'll start from the center, move in the normal direction some amount,
        # and then walk left and right half_length in each direction to create
        # a line segment in the grating.
        center = PyEmb.Point((minx + maxx) / 2.0, (miny + maxy) / 2.0)

        # I need to figure out how far I need to go along the normal to get to
        # the edge of the shape.  To do that, I'll rotate the bounding box
        # angle degrees clockwise and ask for the new bounding box.  The max
        # and min y tell me how far to go.

        _, start, _, end = affinity.rotate(self.shape, angle, origin='center', use_radians=True).bounds

        # convert start and end to be relative to center (simplifies things later)
        start -= center.y
        end -= center.y

        # offset start slightly so that rows are always an even multiple of
        # row_spacing_px from the origin.  This makes it so that abutting
        # fill regions at the same angle and spacing always line up nicely.
        start -= (start + normal * center) % row_spacing

        rows = []

        while start < end:
            p0 = center + normal * start + direction * half_length
            p1 = center + normal * start - direction * half_length
            endpoints = [p0.as_tuple(), p1.as_tuple()]
            grating_line = shgeo.LineString(endpoints)

            res = grating_line.intersection(self.shape)

            if (isinstance(res, shgeo.MultiLineString)):
                runs = map(lambda line_string: line_string.coords, res.geoms)
            else:
                if res.is_empty or len(res.coords) == 1:
                    # ignore if we intersected at a single point or no points
                    start += row_spacing
                    continue
                runs = [res.coords]

            runs.sort(key=lambda seg: (PyEmb.Point(*seg[0]) - upper_left).length())

            if self.flip:
                runs.reverse()
                runs = map(lambda run: tuple(reversed(run)), runs)

            rows.append(runs)

            start += row_spacing

        return rows

    def inter_distance(self, segment1, segment2):
        return shgeo.LineString(segment1).distance(shgeo.LineString(segment2))

    def is_same_run(self, segment1, segment2):
        #if we have intersection due to hole with sharp corner and an angle fill
        dist=shgeo.Point(segment1[0]).distance(shgeo.Point(segment1[1]))
        dist1=shgeo.Point(segment1[0]).distance(shgeo.LineString(segment2))
        dist2=shgeo.Point(segment1[1]).distance(shgeo.LineString(segment2))
        if (dist1 > dist-self.row_spacing or dist2 > dist-self.row_spacing) and dist > self.row_spacing * 3:
            return False

        if self.inter_distance(segment1, segment2) <= self.row_spacing * 1.001:
            return True
        return False

    def adjacent_count(self, row, segment):
        count = 0
        if len(row):
            for onesegment in row:
                if self.is_same_run(onesegment,segment):
                    count = count + 1
        return count

    def find_adjacent_run(self, runs, prevrow, segment):
        for onesegment in prevrow:
            if self.is_same_run(onesegment,segment):
                for run in runs:
                    if run[-1] == onesegment:
                        return runs.index(run)
        return -1 #something went wrong, we must crash here or smth else

    def neighbours_count(self, runs, run):
        top = 0
        bottom = 0
        for onerun in runs:
            if (onerun == run):
                continue
            if self.is_same_run(run[0],onerun[-1]):
                top = top + 1
            if self.is_same_run(run[-1],onerun[0]):
                bottom = bottom + 1
        return top,bottom

    def pull_runs(self, rows):
        #remake: splitting into runs
        #each run should not be enclosed by any other one
        #all runs can figure out their neighbours up and down 
        #thus we can determine right sequence for jump stitches
        #which connect runs to avoid going through already filled area
        #Sequence detection algorithm:
        #run can be filled starting from side where it has no neighbours (top or bottom)
        #after being filled the run is eliminated from list
        #Shape detection algorithm
        #scan each segment of current row agains all previous row segments and 
        #each segment of previous row against all segments of current row 
        #if adjacent_count == 1: append this segment to shape
        #if adjacent_count == 0: start new run
        #if adjacent_count >1: start new run (obstacle detected)
        #       (aka close corresponding shape from bottom)
        #--------------------
        #-------------------- segment from prevrow intersect couple of segments from
        #------/^^^^^\------- next row. Obstacle begin detected. We split block here
        #------|     |-------
        #------|     |-------
        #-------\   /--------
        #--------\_/--------- segment from next row intersect couple of segments from
        #-------------------- prev row. obstacle end detected. We split block here too.
        #Jump stitch will go though the middle of common segments betwenn adjacent blocks
        fill_logic = "serg_reordered"
        runs = []
        prevrow = []
        for row in rows:
            for segment in row:
                #print >>sys.stderr, "P", str(prevrow)
                #print >>sys.stderr, "R", str(row)
                obstacleedge = True
                if self.adjacent_count(prevrow,segment) == 1:
                    rindex = self.find_adjacent_run(runs,prevrow,segment)
                    if self.adjacent_count(row,runs[rindex][-1]) == 1:
                        runs[rindex].append(segment)
                        obstacleedge = False
                if(obstacleedge):
                    run = []
                    run.append(segment)
                    runs.append(run)

            prevrow = row

        #let's try to reorder runs for no visible jumpstitches on the surface
        if (fill_logic == "serg_reordered"):
            orderedruns = []
            direction = 'down'
            isadjacent = False
            while (len(runs)>1):
                mincnt = len(runs)
                minrun = runs[0]
                mindist = 1000;
                mintop = 100
                for run in runs:
                    top,bottom = self.neighbours_count(runs,run)
                    isadjacent = False
                    if  top == 0 or bottom == 0:
                        dist = 0
                        if len(orderedruns) >0:
                            dist = self.inter_distance(orderedruns[-1][-1],run[0])
                            dist1 = self.inter_distance(orderedruns[-1][-1],run[-1])
                            if dist1 < dist:
                                dist = dist1
                        #print >> sys.stderr, "dist:", dist, "dist1:", dist1
                            if direction == 'down':
                                isadjacent = isadjacent or self.is_same_run(orderedruns[-1][-1],run[0])
                            else:
                                isadjacent = isadjacent or self.is_same_run(orderedruns[-1][-1],run[-1])

                        if ((top+bottom) < mincnt or
                            (top+bottom) == mincnt and (mindist > dist)):
                            minrun = run
                            mincnt = top+bottom
                            mintop = top
                            mindist = dist
                            if isadjacent:
                                mindist = -1
                runs.remove(minrun)
                #if (mintop != 0 or (isadjacent and direction == 'up')):   #if needs to fill from bottom
                #print >> sys.stderr, "mintop:", mintop
                if (mintop != 0):   #if needs to fill from bottom
                    minrun.reverse()
                    direction = 'up'
                else:
                    direction = 'down'
                orderedruns.append(minrun)
            if (direction == 'up'):   #if prelast was filled from bottom last will bee the same
                runs[0].reverse()
            orderedruns.append(runs[0])
            
            return orderedruns
            
        else:
            return runs

    def section_to_patch(self, group_of_segments, angle=None, row_spacing=None, max_stitch_length=None):
        if max_stitch_length is None:
            max_stitch_length = self.max_stitch_length

        if row_spacing is None:
            row_spacing = self.row_spacing

        if angle is None:
            angle = self.angle

        # print >> sys.stderr, len(groups_of_segments)

        patch = Patch(color=self.color)
        first_segment = True
        swap = False
        last_end = None

        for segment in group_of_segments:
            # We want our stitches to look like this:
            #
            # ---*-----------*-----------
            # ------*-----------*--------
            # ---------*-----------*-----
            # ------------*-----------*--
            # ---*-----------*-----------
            #
            # Each successive row of stitches will be staggered, with
            # num_staggers rows before the pattern repeats.  A value of
            # 4 gives a nice fill while hiding the needle holes.  The
            # first row is offset 0%, the second 25%, the third 50%, and
            # the fourth 75%.
            #
            # Actually, instead of just starting at an offset of 0, we
            # can calculate a row's offset relative to the origin.  This
            # way if we have two abutting fill regions, they'll perfectly
            # tile with each other.  That's important because we often get
            # abutting fill regions from pull_runs().

            (beg, end) = segment

            if (swap):
                (beg, end) = (end, beg)

            beg = PyEmb.Point(*beg)
            end = PyEmb.Point(*end)

            row_direction = (end - beg).unit()
            segment_length = (end - beg).length()

            # only stitch the first point if it's a reasonable distance away from the
            # last stitch
            if last_end is None or (beg - last_end).length() > 0.1 * self.options.pixels_per_mm:
                patch.add_stitch(beg)

            first_stitch = self.adjust_stagger(beg, angle, row_spacing, max_stitch_length)

            # we might have chosen our first stitch just outside this row, so move back in
            if (first_stitch - beg) * row_direction < 0:
                first_stitch += row_direction * max_stitch_length

            offset = (first_stitch - beg).length()

            while offset < segment_length:
                patch.add_stitch(beg + offset * row_direction)
                offset += max_stitch_length

            if (end - patch.stitches[-1]).length() > 0.1 * self.options.pixels_per_mm:
                patch.add_stitch(end)

            last_end = end
            swap = not swap

        return patch

    def to_patches(self, last_patch):
        dbg.write("sergfill to_patches: %s\n" % time.time())
        dbg.flush()

        rows_of_segments = self.intersect_region_with_grating()
        dbg.write("sergfill rows_of: %s\n" % time.time())
        dbg.flush()
        groups_of_segments = self.pull_runs(rows_of_segments)
        dbg.write("sergfill groups_of: %s\n" % time.time())
        dbg.flush()

        return [self.section_to_patch(group) for group in groups_of_segments]


class Stroke(EmbroideryElement):
    @property
    @param('satin_column', 'Satin along paths', type='toggle', inverse=True)
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    #@cache
    def width(self):
        stroke_width = self.get_style("stroke-width")

        if stroke_width.endswith("px"):
            stroke_width = stroke_width[:-2]

        return float(stroke_width)

    @property
    def dashed(self):
        return self.get_style("stroke-dasharray") is not None

    @property
    @param('running_stitch_length_mm', 'Running stitch length', unit='mm', type='float')
    def running_stitch_length(self):
        return self.get_float_param("running_stitch_length_mm")

    @property
    @param('zigzag_spacing_mm', 'Zig-zag spacing (peak-to-peak)', unit='mm', type='float')
    #@cache
    def zigzag_spacing(self):
        return self.get_float_param("zigzag_spacing_mm")

    @property
    @param('repeats', 'Repeats', type='int')
    def repeats(self):
        return self.get_int_param("repeats", 1)

    @property
    def paths(self):
        return self.flatten(self.parse_path())

    def is_running_stitch(self):
        # stroke width <= 0.5 pixels is deprecated in favor of dashed lines
        return self.dashed or self.width <= 0.5

    def stroke_points_exact(self, emb_point_list, zigzag_spacing, stroke_width):
        patch = Patch(color=self.color)
        for p0 in emb_point_list:
            patch.add_stitch(p0)
        return patch

    def stroke_points(self, emb_point_list, zigzag_spacing, stroke_width):
        patch = Patch(color=self.color)
        p0 = emb_point_list[0]
        rho = 0.0
        side = 1
        last_segment_direction = None

        for repeat in xrange(self.repeats):
            if repeat % 2 == 0:
                order = range(1, len(emb_point_list))
            else:
                order = range(-2, -len(emb_point_list) - 1, -1)

            for segi in order:
                p1 = emb_point_list[segi]

                # how far we have to go along segment
                seg_len = (p1 - p0).length()
                if (seg_len == 0):
                    continue

                # vector pointing along segment
                along = (p1 - p0).unit()

                # vector pointing to edge of stroke width
                perp = along.rotate_left() * (stroke_width * 0.5)

                if stroke_width == 0.0 and last_segment_direction is not None:
                    if abs(1.0 - along * last_segment_direction) > 0.5:
                        # if greater than 45 degree angle, stitch the corner
                        rho = self.zigzag_spacing
                        patch.add_stitch(p0)

                # iteration variable: how far we are along segment
                while (rho <= seg_len):
                    left_pt = p0 + along * rho + perp * side
                    patch.add_stitch(left_pt)
                    rho += self.zigzag_spacing
                    side = -side

                p0 = p1
                last_segment_direction = along
                rho -= seg_len

            if (p0 - patch.stitches[-1]).length() > 0.1:
                patch.add_stitch(p0)

        return patch

    def to_patches(self, last_patch):
        patches = []

        for path in self.paths:
            path = [PyEmb.Point(x, y) for x, y in path]
            if self.options.svg2emb == "true":
                patch = self.stroke_points_exact(path, self.running_stitch_length, stroke_width=0.0)
            elif self.is_running_stitch():
                patch = self.stroke_points(path, self.running_stitch_length, stroke_width=0.0)
            else:
                patch = self.stroke_points(path, self.zigzag_spacing / 2.0, stroke_width=self.width)

            patches.append(patch)

        return patches


class SatinColumn(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super(SatinColumn, self).__init__(*args, **kwargs)

    @property
    @param('satin_column', 'Custom satin column', type='toggle')
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @param('zigzag_spacing_mm', 'Zig-zag spacing (peak-to-peak)', unit='mm', type='float')
    def zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return self.get_float_param("zigzag_spacing_mm")

    @property
    @param('pull_compensation_mm', 'Pull compensation', unit='mm', type='float')
    def pull_compensation(self):
        # In satin stitch, the stitches have a tendency to pull together and
        # narrow the entire column.  We can compensate for this by stitching
        # wider than we desire the column to end up.
        return self.get_float_param("pull_compensation_mm", 0)

    @property
    @param('contour_underlay', 'Contour underlay', type='toggle', group='Contour Underlay')
    def contour_underlay(self):
        # "Contour underlay" is stitching just inside the rectangular shape
        # of the satin column; that is, up one side and down the other.
        return self.get_boolean_param("contour_underlay")

    @property
    @param('contour_underlay_stitch_length_mm', 'Stitch length', unit='mm', group='Contour Underlay', type='float')
    def contour_underlay_stitch_length(self):
        # use "contour_underlay_stitch_length", or, if not set, default to "stitch_length"
        return self.get_float_param("contour_underlay_stitch_length_mm") or self.get_float_param("running_stitch_length_mm")

    @property
    @param('contour_underlay_inset_mm', 'Contour underlay inset amount', unit='mm', group='Contour Underlay', type='float')
    def contour_underlay_inset(self):
        # how far inside the edge of the column to stitch the underlay
        return self.get_float_param("contour_underlay_inset_mm", 0.4)

    @property
    @param('center_walk_underlay', 'Center-walk underlay', type='toggle', group='Center-Walk Underlay')
    def center_walk_underlay(self):
        # "Center walk underlay" is stitching down and back in the centerline
        # between the two sides of the satin column.
        return self.get_boolean_param("center_walk_underlay")

    @property
    @param('center_walk_underlay_stitch_length_mm', 'Stitch length', unit='mm', group='Center-Walk Underlay', type='float')
    def center_walk_underlay_stitch_length(self):
        # use "center_walk_underlay_stitch_length", or, if not set, default to "stitch_length"
        return self.get_float_param("center_walk_underlay_stitch_length_mm") or self.get_float_param("running_stitch_length_mm")

    @property
    @param('zigzag_underlay', 'Zig-zag underlay', type='toggle', group='Zig-zag Underlay')
    def zigzag_underlay(self):
        return self.get_boolean_param("zigzag_underlay")

    @property
    @param('zigzag_underlay_spacing_mm', 'Zig-Zag spacing (peak-to-peak)', unit='mm', group='Zig-zag Underlay', type='float')
    def zigzag_underlay_spacing(self):
        # peak-to-peak distance between zigzags in zigzag underlay
        return self.get_float_param("zigzag_underlay_spacing_mm", 1)

    @property
    @param('zigzag_underlay_inset', 'Inset amount (default: half of contour underlay inset)', unit='mm', group='Zig-zag Underlay', type='float')
    def zigzag_underlay_inset(self):
        # how far in from the edge of the satin the points in the zigzags
        # should be

        # Default to half of the contour underlay inset.  That is, if we're
        # doing both contour underlay and zigzag underlay, make sure the
        # points of the zigzag fall outside the contour underlay but inside
        # the edges of the satin column.
        return self.get_float_param("zigzag_underlay_inset_mm") or self.contour_underlay_inset / 2.0

    @property
    #@cache
    def csp(self):
        return self.parse_path()

    @property
    #@cache
    def flattened_beziers(self):
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
                flattened_segment = [PyEmb.Point(x, y) for x, y in flattened_segment[0]]
                flattened_path.append(flattened_segment)

            paths.append(flattened_path)

        return zip(*paths)

    def validate_satin_column(self):
        # The node should have exactly two paths with no fill.  Each
        # path should have the same number of points, meaning that they
        # will both be made up of the same number of bezier curves.

        node_id = self.node.get("id")

        if len(self.csp) != 2:
            self.fatal("satin column: object %s invalid: expected exactly two sub-paths, but there are %s" % (node_id, len(csp)))

        if self.get_style("fill") is not None:
            self.fatal("satin column: object %s has a fill (but should not)" % node_id)

        if len(self.csp[0]) != len(self.csp[1]):
            self.fatal("satin column: object %s has two paths with an unequal number of points (%s and %s)" % (node_id, len(self.csp[0]), len(self.csp[1])))

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

        patches.append(self.do_satin())

        return patches


def detect_classes(node):
    element = EmbroideryElement(node)

    if element.get_boolean_param("satin_column"):
        return [SatinColumn]
    else:
        classes = []

        if element.get_style("fill"):
            if element.get_boolean_param("auto_fill", True):
                classes.append(AutoFill)
            else:
                classes.append(SergFill)

        if element.get_style("stroke"):
            classes.append(Stroke)

        if element.get_boolean_param("stroke_first", False):
            classes.reverse()

        return classes


def descendants(node):
    nodes = []
    element = EmbroideryElement(node)

    if element.has_style('display') and element.get_style('display') is None:
        return []

    if node.tag == SVG_DEFS_TAG:
        return []

    for child in node:
        nodes.extend(descendants(child))

    if node.tag == SVG_PATH_TAG:
        nodes.append(node)

    return nodes

class Patch:
    def __init__(self, color=None, stitches=None):
        self.color = color
        self.stitches = stitches or []

    def __add__(self, other):
        if isinstance(other, Patch):
            return Patch(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("Patch can only be added to another Patch")

    def add_stitch(self, stitch):
        self.stitches.append(stitch)

    def reverse(self):
        return Patch(self.color, self.stitches[::-1])


class Embroider(inkex.Effect):

    def __init__(self, *args, **kwargs):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--row_spacing_mm",
                                     action="store", type="float",
                                     dest="row_spacing_mm", default=0.4,
                                     help="row spacing (mm)")
        self.OptionParser.add_option("-z", "--zigzag_spacing_mm",
                                     action="store", type="float",
                                     dest="zigzag_spacing_mm", default=1.0,
                                     help="zigzag spacing (mm)")
        self.OptionParser.add_option("-l", "--max_stitch_len_mm",
                                     action="store", type="float",
                                     dest="max_stitch_length_mm", default=3.0,
                                     help="max stitch length (mm)")
        self.OptionParser.add_option("--running_stitch_len_mm",
                                     action="store", type="float",
                                     dest="running_stitch_length_mm", default=3.0,
                                     help="running stitch length (mm)")
        self.OptionParser.add_option("-c", "--collapse_len_mm",
                                     action="store", type="float",
                                     dest="collapse_length_mm", default=0.0,
                                     help="max collapse length (mm)")
        self.OptionParser.add_option("-t", "--trim_len_mm",
                                     action="store", type="float",
                                     dest="trim_len_mm", default=20.0,
                                     help="min trim length (mm)")
        self.OptionParser.add_option("--split_path_on_jumps",
                                     action="store", type="choice",
                                     choices=["true","false"],
                                     dest="split_path_on_jumps", default="false",
                                     help="Split SVG path on every jump stitch")
        self.OptionParser.add_option("-f", "--flatness",
                                     action="store", type="float",
                                     dest="flat", default=0.1,
                                     help="Minimum flatness of the subdivided curves")
        self.OptionParser.add_option("--hide_layers",
                                     action="store", type="choice",
                                     choices=["true", "false"],
                                     dest="hide_layers", default="true",
                                     help="Hide all other layers when the embroidery layer is generated")
        self.OptionParser.add_option("-O", "--output_format",
                                     action="store", type="choice",
                                     choices=["melco", "csv", "gcode"],
                                     dest="output_format", default="melco",
                                     help="File output format")
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")
        self.OptionParser.add_option("-b", "--max-backups",
                                     action="store", type="int",
                                     dest="max_backups", default=5,
                                     help="Max number of backups of output files to keep.")
        self.OptionParser.add_option("-p", "--pixels_per_mm",
                                     action="store", type="float",
                                     dest="pixels_per_mm", default=10,
                                     help="Number of on-screen pixels per millimeter.")
        self.OptionParser.add_option("--svg2emb",
                                     action="store", type="choice",
                                     choices=["true","false"],
                                     dest="svg2emb", default="false",
                                     help="Just generate embroidmodder2 CSV from existing paths.")
        self.patches = []

    def handle_node(self, node):
        print >> dbg, "handling node", node.get('id'), node.get('tag')
        nodes = descendants(node)
        for node in nodes:
            classes = detect_classes(node)
            print >> dbg, "classes:", classes
            self.elements.extend(cls(node, self.options) for cls in classes)

    def get_output_path(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'))
        csv_filename = svg_filename.replace('.svg', '.csv')
        output_path = os.path.join(self.options.path, csv_filename)

        def add_suffix(path, suffix):
            if suffix > 0:
                path = "%s.%s" % (path, suffix)

            return path

        def move_if_exists(path, suffix=0):
            source = add_suffix(path, suffix)

            if suffix >= self.options.max_backups:
                return

            dest = add_suffix(path, suffix + 1)

            if os.path.exists(source):
                move_if_exists(path, suffix + 1)
                os.rename(source, dest)

        move_if_exists(output_path)

        return output_path

    def hide_layers(self):
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            if g.get(inkex.addNS("groupmode", "inkscape")) == "layer":
                g.set("style", "display:none")

    def effect(self):
        # Printing anything other than a valid SVG on stdout blows inkscape up.
        old_stdout = sys.stdout
        sys.stdout = sys.stderr

        self.patch_list = []

        print >> dbg, "starting nodes: %s\n" % time.time()
        dbg.flush()

        self.elements = []

        if self.selected:
            # be sure to visit selected nodes in the order they're stacked in
            # the document
            for node in self.document.getroot().iter():
                if node.get("id") in self.selected:
                    self.handle_node(node)
        else:
            self.handle_node(self.document.getroot())

        print >> dbg, "finished nodes: %s" % time.time()
        dbg.flush()

        if not self.elements:
            if self.selected:
                inkex.errormsg("No embroiderable paths selected.")
            else:
                inkex.errormsg("No embroiderable paths found in document.")
            inkex.errormsg("Tip: use Path -> Object to Path to convert non-paths before embroidering.")
            return

        if self.options.hide_layers:
            self.hide_layers()
        dbg.write("finished hide layers: %s\n" % time.time())
        dbg.flush()

        patches = []
        for element in self.elements:
            if patches:
                last_patch = patches[-1]
            else:
                last_patch = None

            patches.extend(element.to_patches(last_patch))
        dbg.write("finished patches: %s\n" % time.time())
        dbg.flush()

        stitches = self.patches_to_stitches(patches, self.options.collapse_length_mm * self.options.pixels_per_mm
                , self.options.trim_len_mm * self.options.pixels_per_mm)
        dbg.write("finished stitches: %s\n" % time.time())
        dbg.flush()
        emb = PyEmb.Embroidery(stitches, self.options.pixels_per_mm)
        dbg.write("finished emb: %s\n" % time.time())
        dbg.flush()

        emb.export(self.get_output_path(), self.options.output_format)
        dbg.write("finished export: %s\n" % time.time())
        dbg.flush()

        if self.options.svg2emb != "true":
            new_layer = inkex.etree.SubElement(self.document.getroot(), SVG_GROUP_TAG, {})
            new_layer.set('id', self.uniqueId("embroidery"))
            new_layer.set(inkex.addNS('label', 'inkscape'), 'Embroidery')
            new_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
            self.emit_inkscape(new_layer, stitches)

        sys.stdout = old_stdout
        dbg.write("finished output: %s\n" % time.time())
        dbg.flush()

    def patches_to_stitches(self, patch_list, collapse_len_px=0, trim_len_px=0):
        stitches = []

        last_stitch = None
        last_color = None
        for patch in patch_list:
            jump_stitch = 'j'
            for stitch in patch.stitches:
                if last_stitch and last_color == patch.color:
                    l = (stitch - last_stitch).length()
                    if l <= 0.1:
                        # filter out duplicate successive stitches
                        jump_stitch = 's'
                        continue

                    if jump_stitch == 'j':
                        # consider collapsing jump stitch, if it is pretty short
                        if l < collapse_len_px or collapse_len_px == 0:
                            #dbg.write("... collapsed\n")
                            jump_stitch = 's'
                        if l >= trim_len_px and trim_len_px > 0:
                            jump_stitch = 't'

                # dbg.write("stitch color %s\n" % patch.color)

                new_stitch = PyEmb.Stitch(stitch.x, stitch.y, patch.color, jump_stitch)
                stitches.append(new_stitch)

                jump_stitch = 's'
                last_stitch = stitch
                last_color = patch.color

        return stitches


    def stitches_to_paths(self, stitches):
        paths = []
        last_color = None
        last_stitch = None
        for stitch in stitches:
            if stitch.jump_stitch=='t' or (stitch.jump_stitch=='j' and self.options.split_path_on_jumps=='true'):
                if last_color == stitch.color:
                    paths.append([None, []])
                    if last_stitch is not None:
                        paths[-1][1].append(['M', last_stitch.as_tuple()])
                        paths[-1][1].append(['L', stitch.as_tuple()])
                last_color = None
            if stitch.color != last_color:
                paths.append([stitch.color, []])
            paths[-1][1].append(['L' if len(paths[-1][1]) > 0 else 'M', stitch.as_tuple()])
            last_color = stitch.color
            last_stitch = stitch
        return paths


    def emit_inkscape(self, parent, stitches):
        for color, path in self.stitches_to_paths(stitches):
            # dbg.write('path: %s %s\n' % (color, repr(path)))
            inkex.etree.SubElement(parent,
                                   inkex.addNS('path', 'svg'),
                                   {'style': simplestyle.formatStyle(
                                       {'stroke': color if color is not None else '#000000',
                                        'stroke-width': "0.4",
                                        'fill': 'none'}),
                                       'd': simplepath.formatPath(path),
                                    })


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    e = Embroider()
    e.affect()
    dbg.flush()

dbg.close()
