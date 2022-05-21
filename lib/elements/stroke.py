# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import shapely.geometry

from inkex import Transform

from ..i18n import _
from ..stitch_plan import StitchGroup
from ..stitches import bean_stitch, running_stitch
from ..stitches.ripple_stitch import ripple_stitch
from ..svg import get_node_transform, parse_length_with_units
from ..utils import Point, cache
from .element import EmbroideryElement, param
from .satin_column import SatinColumn

warned_about_legacy_running_stitch = False


class Stroke(EmbroideryElement):
    element_name = _("Stroke")

    @property
    @param('satin_column', _('Running stitch along paths'), type='toggle', inverse=True)
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    def dashed(self):
        return self.get_style("stroke-dasharray") is not None

    @property
    @param('stroke_method',
           _('Method'),
           type='dropdown',
           default=0,
           # 0: run/simple satin, 1: manual, 2: ripple
           options=[_("Running Stitch"), _("Manual stitch placement"), _("Ripple")],
           sort_index=0)
    def stroke_method(self):
        return self.get_int_param('stroke_method', 0)

    @property
    @param('repeats',
           _('Repeats'),
           tooltip=_('Defines how many times to run down and back along the path.'),
           type='int',
           default="1",
           select_items=[('stroke_method', 0), ('stroke_method', 2)],
           sort_index=4)
    def repeats(self):
        return max(1, self.get_int_param("repeats", 1))

    @property
    @param(
        'bean_stitch_repeats',
        _('Bean stitch number of repeats'),
        tooltip=_('Backtrack each stitch this many times.  '
                  'A value of 1 would triple each stitch (forward, back, forward).  '
                  'A value of 2 would quintuple each stitch, etc.  Only applies to running stitch.'),
        type='int',
        default=0,
        select_items=[('stroke_method', 0), ('stroke_method', 2)],
        sort_index=5)
    def bean_stitch_repeats(self):
        return self.get_int_param("bean_stitch_repeats", 0)

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches in running stitch mode.'),
           unit='mm',
           type='float',
           default=1.5,
           select_items=[('stroke_method', 0), ('stroke_method', 2)],
           sort_index=2)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('line_count',
           _('Number of lines'),
           tooltip=_('Number of lines from start to finish'),
           type='int',
           default=10,
           select_items=[('stroke_method', 2)],
           sort_index=1)
    @cache
    def line_count(self):
        return max(self.get_int_param("line_count", 10), 1)

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Length of stitches in zig-zag mode.'),
           unit='mm',
           type='float',
           default=0.4,
           select_items=[('stroke_method', 0)],
           sort_index=3)
    @cache
    def zigzag_spacing(self):
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    def paths(self):
        path = self.parse_path()
        flattened = self.flatten(path)

        # manipulate invalid path
        if len(flattened[0]) == 1:
            return [[[flattened[0][0][0], flattened[0][0][1]], [flattened[0][0][0] + 1.0, flattened[0][0][1]]]]

        if self.stroke_method == 1:
            return [self.strip_control_points(subpath) for subpath in path]
        else:
            return flattened

    @property
    @cache
    def shape(self):
        return self.as_multi_line_string().convex_hull

    @cache
    def as_multi_line_string(self):
        line_strings = [shapely.geometry.LineString(path) for path in self.paths]
        return shapely.geometry.MultiLineString(line_strings)

    def get_ripple_target(self):
        command = self.get_command('ripple_target')
        if command:
            pos = [float(command.use.get("x", 0)), float(command.use.get("y", 0))]
            transform = get_node_transform(command.use)
            pos = Transform(transform).apply_to_point(pos)
            return Point(*pos)
        else:
            return self.shape.centroid

    def is_running_stitch(self):
        # using stroke width <= 0.5 pixels to indicate running stitch is deprecated in favor of dashed lines

        stroke_width, units = parse_length_with_units(self.get_style("stroke-width", "1"))

        if self.dashed:
            return True
        elif stroke_width <= 0.5 and self.get_float_param('running_stitch_length_mm', None) is not None:
            # if they use a stroke width less than 0.5 AND they specifically set a running stitch
            # length, then assume they intend to use the deprecated <= 0.5 method to set running
            # stitch.
            #
            # Note that we use self.get_style("stroke_width") _not_ self.stroke_width above.  We
            # explicitly want the stroke width in "user units" ("document units") -- that is, what
            # the user sees in inkscape's stroke settings.
            #
            # Also note that we don't use self.running_stitch_length_mm above.  This is because we
            # want to see if they set a running stitch length at all, and the property will apply
            # a default value.
            #
            # This is so tricky, and and intricate that's a major reason that we deprecated the
            # 0.5 units rule.

            # Warn them the first time.
            global warned_about_legacy_running_stitch
            if not warned_about_legacy_running_stitch:
                warned_about_legacy_running_stitch = True
                print(_("Legacy running stitch setting detected!\n\nIt looks like you're using a stroke " +
                        "smaller than 0.5 units to indicate a running stitch, which is deprecated.  Instead, please set " +
                        "your stroke to be dashed to indicate running stitch.  Any kind of dash will work."), file=sys.stderr)

            # still allow the deprecated setting to work in order to support old files
            return True
        else:
            return False

    def simple_satin(self, path, zigzag_spacing, stroke_width):
        "zig-zag along the path at the specified spacing and wdith"

        # `self.zigzag_spacing` is the length for a zig and a zag
        # together (a V shape).  Start with running stitch at half
        # that length:
        patch = self.running_stitch(path, zigzag_spacing / 2.0)

        # Now move the points left and right.  Consider each pair
        # of points in turn, and move perpendicular to them,
        # alternating left and right.

        offset = stroke_width / 2.0

        for i in range(len(patch) - 1):
            start = patch.stitches[i]
            end = patch.stitches[i + 1]
            # sometimes the stitch results into zero length which cause a division by zero error
            # ignoring this leads to a slightly bad result, but that is better than no output
            if (end - start).length() == 0:
                continue
            segment_direction = (end - start).unit()
            zigzag_direction = segment_direction.rotate_left()

            if i % 2 == 1:
                zigzag_direction *= -1

            patch.stitches[i] += zigzag_direction * offset

        return patch

    def running_stitch(self, path, stitch_length):
        repeated_path = []

        # go back and forth along the path as specified by self.repeats
        for i in range(self.repeats):
            if i % 2 == 1:
                # reverse every other pass
                this_path = path[::-1]
            else:
                this_path = path[:]

            repeated_path.extend(this_path)

        stitches = running_stitch(repeated_path, stitch_length)

        return StitchGroup(self.color, stitches)

    def do_bean_repeats(self, stitches):
        return bean_stitch(stitches, self.bean_stitch_repeats)

    def to_stitch_groups(self, last_patch):
        patches = []

        # ripple stitch
        if self.stroke_method == 2:
            lines = self.as_multi_line_string()
            points = []
            if len(lines.geoms) > 1:
                # use satin column points for satin like build ripple stitches
                points = SatinColumn(self.node).plot_points_on_rails(self.running_stitch_length, 0)
            point_target = self.get_ripple_target()
            patch = StitchGroup(
                color=self.color,
                tags=["ripple_stitch"],
                stitches=ripple_stitch(
                    self.as_multi_line_string(),
                    point_target,
                    self.line_count,
                    points,
                    self.running_stitch_length,
                    self.repeats))
            if patch:
                if self.bean_stitch_repeats > 0:
                    patch.stitches = self.do_bean_repeats(patch.stitches)
                patches.append(patch)
        else:
            for path in self.paths:
                path = [Point(x, y) for x, y in path]
                # manual stitch
                if self.stroke_method == 1:
                    patch = StitchGroup(color=self.color, stitches=path, stitch_as_is=True)
                # running stitch
                elif self.is_running_stitch():
                    patch = self.running_stitch(path, self.running_stitch_length)

                    if self.bean_stitch_repeats > 0:
                        patch.stitches = self.do_bean_repeats(patch.stitches)
                else:
                    patch = self.simple_satin(path, self.zigzag_spacing, self.stroke_width)

            if patch:
                patches.append(patch)

        return patches
