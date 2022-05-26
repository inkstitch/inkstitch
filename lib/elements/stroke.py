# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import shapely.geometry

from inkex import Transform

from ..i18n import _
from ..marker import get_marker_elements
from ..stitch_plan import StitchGroup
from ..stitches import bean_stitch, running_stitch
from ..stitches.ripple_stitch import ripple_stitch
from ..svg import get_node_transform, parse_length_with_units
from ..utils import Point, cache
from .element import EmbroideryElement, param
from .satin_column import SatinColumn
from .validation import ValidationWarning

warned_about_legacy_running_stitch = False


class IgnoreSkipValues(ValidationWarning):
    name = _("Ignore skip")
    description = _("Skip values are ignored, because there was no line left to embroider.")
    steps_to_solve = [
        _('* Reduce values of Skip first and last lines or'),
        _('* Increase number of lines accordinly in the params dialog.'),
    ]


class MultipleGuideLineWarning(ValidationWarning):
    name = _("Multiple Guide Lines")
    description = _("This object has multiple guide lines, but only the first one will be used.")
    steps_to_solve = [
        _("* Remove all guide lines, except for one.")
    ]


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
           options=[_("Running Stitch"), _("Ripple")],
           sort_index=0)
    def stroke_method(self):
        return self.get_int_param('stroke_method', 0)

    @property
    @param('manual_stitch',
           _('Manual stitch placement'),
           tooltip=_("Stitch every node in the path.  All other options are ignored."),
           type='boolean',
           default=False,
           select_items=[('stroke_method', 0)],
           sort_index=1)
    def manual_stitch_mode(self):
        return self.get_boolean_param('manual_stitch')

    @property
    @param('repeats',
           _('Repeats'),
           tooltip=_('Defines how many times to run down and back along the path.'),
           type='int',
           default="1",
           sort_index=2)
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
        sort_index=3)
    def bean_stitch_repeats(self):
        return self.get_int_param("bean_stitch_repeats", 0)

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches in running stitch mode.'),
           unit='mm',
           type='float',
           default=1.5,
           sort_index=4)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('line_count',
           _('Number of lines'),
           tooltip=_('Number of lines from start to finish'),
           type='int',
           default=10,
           select_items=[('stroke_method', 1)],
           sort_index=5)
    @cache
    def line_count(self):
        return max(self.get_int_param("line_count", 10), 1)

    @property
    @param('skip_start',
           _('Skip first lines'),
           tooltip=_('Skip this number of lines at the beginning.'),
           type='int',
           default=0,
           select_items=[('stroke_method', 1)],
           sort_index=6)
    @cache
    def skip_start(self):
        return abs(self.get_int_param("skip_start", 0))

    @property
    @param('skip_end',
           _('Skip last lines'),
           tooltip=_('Skip this number of lines at the end'),
           type='int',
           default=0,
           select_items=[('stroke_method', 1)],
           sort_index=7)
    @cache
    def skip_end(self):
        return abs(self.get_int_param("skip_end", 0))

    @property
    @param('flip',
           _('Flip'),
           tooltip=_('Flip outer to inner'),
           type='boolean',
           default=False,
           select_items=[('stroke_method', 1)],
           sort_index=8)
    @cache
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('render_grid',
           _('Grid distance'),
           tooltip=_('Render as grid. Works only with satin type ripple stitches.'),
           type='float',
           default=0,
           unit='mm',
           select_items=[('stroke_method', 1)],
           sort_index=8)
    @cache
    def render_grid(self):
        return abs(self.get_float_param("render_grid", 0))

    @property
    @param('exponent',
           _('Line distance exponent'),
           tooltip=_('Increse density towards one side.'),
           type='float',
           default=1,
           select_items=[('stroke_method', 1)],
           sort_index=9)
    @cache
    def exponent(self):
        return max(self.get_float_param("exponent", 1), 0.1)

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Length of stitches in zig-zag mode.'),
           unit='mm',
           type='float',
           default=0.4,
           select_items=[('stroke_method', 0)],
           sort_index=5)
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

        if self.manual_stitch_mode:
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
        if self.stroke_method == 1:
            lines = self.as_multi_line_string()
            guide_line = self._get_guide_lines()
            points = []
            if len(lines.geoms) > 1:
                # if render_grid has a number use this, otherwise use running_stitch_length
                length = self.render_grid or self.running_stitch_length
                # use satin column points for satin like build ripple stitches
                points = SatinColumn(self.node).plot_points_on_rails(length, 0)
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
                    self.repeats,
                    self.flip,
                    self.skip_start,
                    self.skip_end,
                    self.render_grid,
                    self.exponent,
                    guide_line))
            if patch:
                if self.bean_stitch_repeats > 0:
                    patch.stitches = self.do_bean_repeats(patch.stitches)
                patches.append(patch)
        else:
            for path in self.paths:
                path = [Point(x, y) for x, y in path]
                # manual stitch
                if self.manual_stitch_mode:
                    patch = StitchGroup(color=self.color, stitches=path, stitch_as_is=True)
                # running stitch
                elif self.is_running_stitch():
                    patch = self.running_stitch(path, self.running_stitch_length)
                    if self.bean_stitch_repeats > 0:
                        patch.stitches = self.do_bean_repeats(patch.stitches)
                # simple satin
                else:
                    patch = self.simple_satin(path, self.zigzag_spacing, self.stroke_width)

                if patch:
                    patches.append(patch)

        return patches

    @cache
    def _get_guide_lines(self, multiple=False):
        guide_lines = get_marker_elements(self.node, "guide-line", False, True)
        # No or empty guide line
        if not guide_lines or not guide_lines['stroke']:
            return None

        if multiple:
            return guide_lines['stroke']
        else:
            return guide_lines['stroke'][0]

    def validation_warnings(self):
        if self.stroke_method == 1 and self.skip_start + self.skip_end >= self.line_count:
            yield IgnoreSkipValues(self.shape.centroid)

        # guided fill warnings
        if self.stroke == 1:
            guide_lines = self._get_guide_lines(True)
            if len(guide_lines) > 1:
                yield MultipleGuideLineWarning(self.shape.centroid)
            return None
