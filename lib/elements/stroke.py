# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil

import shapely.geometry as shgeo
from inkex import Transform
from shapely.errors import GEOSException

from ..i18n import _
from ..marker import get_marker_elements
from ..stitch_plan import StitchGroup
from ..stitches.ripple_stitch import ripple_stitch
from ..stitches.running_stitch import bean_stitch, running_stitch
from ..svg import get_node_transform, parse_length_with_units
from ..svg.clip import get_clip_path
from ..threads import ThreadColor
from ..utils import Point, cache
from ..utils.param import ParamOption
from .element import EmbroideryElement, param
from .validation import ValidationWarning


class MultipleGuideLineWarning(ValidationWarning):
    name = _("Multiple Guide Lines")
    description = _("This object has multiple guide lines, but only the first one will be used.")
    steps_to_solve = [
        _("* Remove all guide lines, except for one.")
    ]


class TooFewSubpathsWarning(ValidationWarning):
    name = _("Too few subpaths")
    description = _("This element renders as running stitch while it has a satin column parameter.")
    steps_to_solve = [
        _("* Convert to stroke: select the element and open the parameter dialog. Enable running stitch along path."),
        _("* Use as satin column: add an other rail and optionally rungs.")
    ]


class Stroke(EmbroideryElement):
    element_name = _("Stroke")

    @property
    @param('satin_column', _('Running stitch along paths'), type='toggle', inverse=True)
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        color = self.get_style("stroke")
        if self.cutwork_needle is not None:
            color = ThreadColor(color, description=self.cutwork_needle, chart=self.cutwork_needle)
        return color

    @property
    def cutwork_needle(self):
        needle = self.get_int_param('cutwork_needle') or None
        if needle is not None:
            needle = f'Cut {needle}'
        return needle

    _stroke_methods = [ParamOption('running_stitch', _("Running Stitch / Bean Stitch")),
                       ParamOption('ripple_stitch', _("Ripple Stitch")),
                       ParamOption('zigzag_stitch', _("ZigZag Stitch")),
                       ParamOption('manual_stitch', _("Manual Stitch"))]

    @property
    @param('stroke_method',
           _('Method'),
           type='combo',
           default=0,
           options=_stroke_methods,
           sort_index=0)
    def stroke_method(self):
        return self.get_param('stroke_method', 'running_stitch')

    @property
    @param('repeats',
           _('Repeats'),
           tooltip=_('Defines how many times to run down and back along the path.'),
           type='int',
           select_items=[('stroke_method', 'running_stitch'), ('stroke_method', 'ripple_stitch'), ('stroke_method', 'zigzag_stitch')],
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
                  'A value of 2 would quintuple each stitch, etc.\n\n'
                  'A pattern with various repeats can be created with a list of values separated by a space.'),
        type='str',
        select_items=[('stroke_method', 'running_stitch'), ('stroke_method', 'ripple_stitch')],
        default=0,
        sort_index=3)
    def bean_stitch_repeats(self):
        return self.get_multiple_int_param("bean_stitch_repeats", "0")

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches. Stitches can be shorter according to the stitch tolerance setting.'),
           unit='mm',
           type='float',
           select_items=[('stroke_method', 'running_stitch'), ('stroke_method', 'ripple_stitch')],
           default=2.5,
           sort_index=4)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 2.5), 0.01)

    @property
    @param('running_stitch_tolerance_mm',
           _('Stitch tolerance'),
           tooltip=_('All stitches must be within this distance from the path.  ' +
                     'A lower tolerance means stitches will be closer together.  ' +
                     'A higher tolerance means sharp corners may be rounded.'),
           unit='mm',
           type='float',
           select_items=[('stroke_method', 'running_stitch'), ('stroke_method', 'ripple_stitch')],
           default=0.2,
           sort_index=4)
    def running_stitch_tolerance(self):
        return max(self.get_float_param("running_stitch_tolerance_mm", 0.2), 0.01)

    @property
    @param('max_stitch_length_mm',
           _('Max stitch length'),
           tooltip=_('Split stitches longer than this.'),
           unit='mm',
           type='float',
           select_items=[('stroke_method', 'manual_stitch')],
           sort_index=5)
    def max_stitch_length(self):
        max_length = self.get_float_param("max_stitch_length_mm", None)
        if not max_length or max_length <= 0:
            return
        return max_length

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Length of stitches in zig-zag mode.'),
           unit='mm',
           type='float',
           default=0.4,
           select_items=[('stroke_method', 'zigzag_stitch')],
           sort_index=6)
    @cache
    def zigzag_spacing(self):
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param('pull_compensation_mm',
           _('Pull compensation'),
           tooltip=_('Zigzag stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape. '
                     'This widens the zigzag line width.'),
           unit='mm',
           type='float',
           default=0,
           select_items=[('stroke_method', 'zigzag_stitch')],
           sort_index=6)
    @cache
    def pull_compensation(self):
        return self.get_float_param("pull_compensation_mm", 0)

    @property
    @param('line_count',
           _('Number of lines'),
           tooltip=_('Number of lines from start to finish'),
           type='int',
           default=10,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=7)
    @cache
    def line_count(self):
        return max(self.get_int_param("line_count", 10), 1)

    @property
    @param('min_line_dist_mm',
           _('Minimum line distance'),
           tooltip=_('Overrides the number of lines setting.'),
           unit='mm',
           type='float',
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=8)
    @cache
    def min_line_dist(self):
        min_dist = self.get_float_param("min_line_dist_mm")
        if min_dist is None:
            return
        return max(min_dist, 0.01)

    @property
    @param('staggers',
           _('Stagger lines this many times before repeating'),
           tooltip=_('Length of the cycle by which successive stitch lines are staggered. '
                     'Fractional values are allowed and can have less visible diagonals than integer values. '
                     'For linear ripples only.'),
           type='int',
           select_items=[('stroke_method', 'ripple_stitch')],
           default=1,
           sort_index=9)
    def staggers(self):
        return self.get_float_param("staggers", 1)

    @property
    @param('skip_start',
           _('Skip first lines'),
           tooltip=_('Skip this number of lines at the beginning.'),
           type='int',
           default=0,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=10)
    @cache
    def skip_start(self):
        return abs(self.get_int_param("skip_start", 0))

    @property
    @param('skip_end',
           _('Skip last lines'),
           tooltip=_('Skip this number of lines at the end'),
           type='int',
           default=0,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=11)
    @cache
    def skip_end(self):
        return abs(self.get_int_param("skip_end", 0))

    @property
    @param('exponent',
           _('Line distance exponent'),
           tooltip=_('Increase density towards one side.'),
           type='float',
           default=1,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=12)
    @cache
    def exponent(self):
        return max(self.get_float_param("exponent", 1), 0.1)

    @property
    @param('flip_exponent',
           _('Flip exponent'),
           tooltip=_('Reverse exponent effect.'),
           type='boolean',
           default=False,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=13)
    @cache
    def flip_exponent(self):
        return self.get_boolean_param("flip_exponent", False)

    @property
    @param('reverse',
           _('Reverse'),
           tooltip=_('Flip start and end point'),
           type='boolean',
           default=False,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=14)
    @cache
    def reverse(self):
        return self.get_boolean_param("reverse", False)

    _reverse_rails_options = [ParamOption('automatic', _('Automatic')),
                              ParamOption('none', _("Don't reverse")),
                              ParamOption('first', _('Reverse first rail')),
                              ParamOption('second', _('Reverse second rail')),
                              ParamOption('both', _('Reverse both rails'))
                              ]

    @property
    @param(
        'reverse_rails',
        _('Reverse rails'),
        tooltip=_('Reverse satin ripple rails.  ' +
                  'Default: automatically detect and fix a reversed rail.'),
        type='combo',
        options=_reverse_rails_options,
        default='automatic',
        select_items=[('stroke_method', 'ripple_stitch')],
        sort_index=15)
    def reverse_rails(self):
        return self.get_param('reverse_rails', 'automatic')

    @property
    @param('grid_size_mm',
           _('Grid size'),
           tooltip=_('Render as grid. Use with care and watch your stitch density.'),
           type='float',
           default=0,
           unit='mm',
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=16)
    @cache
    def grid_size(self):
        return abs(self.get_float_param("grid_size_mm", 0))

    @property
    @param('scale_axis',
           _('Scale axis'),
           tooltip=_('Scale axis for satin guided ripple stitches.'),
           type='dropdown',
           default=0,
           # 0: xy, 1: x, 2: y, 3: none
           options=["X Y", "X", "Y", _("None")],
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=17)
    def scale_axis(self):
        return self.get_int_param('scale_axis', 0)

    @property
    @param('scale_start',
           _('Starting scale'),
           tooltip=_('How big the first copy of the line should be, in percent.') + " " + _('Used only for ripple stitch with a guide line.'),
           type='float',
           unit='%',
           default=100,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=18)
    def scale_start(self):
        return self.get_float_param('scale_start', 100.0)

    @property
    @param('scale_end',
           _('Ending scale'),
           tooltip=_('How big the last copy of the line should be, in percent.') + " " + _('Used only for ripple stitch with a guide line.'),
           type='float',
           unit='%',
           default=0.0,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=19)
    def scale_end(self):
        return self.get_float_param('scale_end', 0.0)

    @property
    @param('rotate_ripples',
           _('Rotate'),
           tooltip=_('Rotate satin guided ripple stitches'),
           type='boolean',
           default=True,
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=20)
    @cache
    def rotate_ripples(self):
        return self.get_boolean_param("rotate_ripples", True)

    @property
    @param('join_style',
           _('Join style'),
           tooltip=_('Join style for non circular ripples.'),
           type='dropdown',
           default=0,
           options=(_("flat"), _("point")),
           select_items=[('stroke_method', 'ripple_stitch')],
           sort_index=21)
    @cache
    def join_style(self):
        return self.get_int_param('join_style', 0)

    @property
    @cache
    def is_closed(self):
        # returns true if the outline of a single line stroke is a closed shape
        # (with a small tolerance)
        lines = self.as_multi_line_string().geoms
        if len(lines) == 1:
            coords = lines[0].coords
            return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05
        return False

    @property
    def paths(self):
        path = self.parse_path()
        flattened = self.flatten(path)
        flattened = self._get_clipped_path(flattened)

        # manipulate invalid path
        if len(flattened[0]) == 1:
            return [[[flattened[0][0][0], flattened[0][0][1]], [flattened[0][0][0] + 1.0, flattened[0][0][1]]]]

        if self.stroke_method == 'manual_stitch':
            return [self.strip_control_points(subpath) for subpath in path]
        else:
            return flattened

    @property
    @cache
    def shape(self):
        return self.as_multi_line_string().convex_hull

    @cache
    def as_multi_line_string(self):
        line_strings = [shgeo.LineString(path) for path in self.paths]
        return shgeo.MultiLineString(line_strings)

    def _get_clipped_path(self, paths):
        if self.node.clip is None:
            return paths

        clip_path = get_clip_path(self.node)
        # path to linestrings
        line_strings = [shgeo.LineString(path) for path in paths]
        try:
            intersection = clip_path.intersection(shgeo.MultiLineString(line_strings))
        except GEOSException:
            return paths

        coords = []
        if intersection.is_empty:
            return paths
        elif isinstance(intersection, shgeo.MultiLineString):
            for c in [intersection for intersection in intersection.geoms if isinstance(intersection, shgeo.LineString)]:
                coords.append(c.coords)
        elif isinstance(intersection, shgeo.LineString):
            coords.append(intersection.coords)
        else:
            return paths
        return coords

    def get_ripple_target(self):
        command = self.get_command('ripple_target')
        if command:
            pos = [float(command.use.get("x", 0)), float(command.use.get("y", 0))]
            transform = get_node_transform(command.use)
            pos = Transform(transform).apply_to_point(pos)
            return Point(*pos)
        else:
            return self.shape.centroid

    def simple_satin(self, path, zigzag_spacing, stroke_width, pull_compensation):
        "zig-zag along the path at the specified spacing and wdith"

        # `self.zigzag_spacing` is the length for a zig and a zag
        # together (a V shape).  Start with running stitch at half
        # that length:
        patch = self.running_stitch(path, zigzag_spacing / 2.0, self.running_stitch_tolerance)

        # Now move the points left and right.  Consider each pair
        # of points in turn, and move perpendicular to them,
        # alternating left and right.

        stroke_width = stroke_width + pull_compensation
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

    def running_stitch(self, path, stitch_length, tolerance):
        stitches = running_stitch(path, stitch_length, tolerance)

        repeated_stitches = []
        # go back and forth along the path as specified by self.repeats
        for i in range(self.repeats):
            if i % 2 == 1:
                # reverse every other pass
                this_path = stitches[::-1]
            else:
                this_path = stitches[:]

            repeated_stitches.extend(this_path)

        return StitchGroup(self.color, repeated_stitches, lock_stitches=self.lock_stitches, force_lock_stitches=self.force_lock_stitches)

    def apply_max_stitch_length(self, path):
        # apply max distances
        max_len_path = [path[0]]
        for points in zip(path[:-1], path[1:]):
            line = shgeo.LineString(points)
            dist = line.length
            if dist > self.max_stitch_length:
                num_subsections = ceil(dist / self.max_stitch_length)
                additional_points = [Point(coord.x, coord.y)
                                     for coord in [line.interpolate((i/num_subsections), normalized=True)
                                     for i in range(1, num_subsections + 1)]]
                max_len_path.extend(additional_points)
            max_len_path.append(points[1])
        return max_len_path

    def ripple_stitch(self):
        return StitchGroup(
            color=self.color,
            tags=["ripple_stitch"],
            stitches=ripple_stitch(self),
            lock_stitches=self.lock_stitches,
            force_lock_stitches=self.force_lock_stitches)

    def do_bean_repeats(self, stitches):
        return bean_stitch(stitches, self.bean_stitch_repeats)

    def to_stitch_groups(self, last_patch):  # noqa: C901
        patches = []

        # ripple stitch
        if self.stroke_method == 'ripple_stitch':
            patch = self.ripple_stitch()
            if patch:
                if any(self.bean_stitch_repeats):
                    patch.stitches = self.do_bean_repeats(patch.stitches)
                patches.append(patch)
        else:
            for path in self.paths:
                path = [Point(x, y) for x, y in path]
                # manual stitch
                if self.stroke_method == 'manual_stitch':
                    if self.max_stitch_length:
                        path = self.apply_max_stitch_length(path)

                    if self.force_lock_stitches:
                        lock_stitches = self.lock_stitches
                    else:
                        # manual stitch disables lock stitches unless they force them
                        lock_stitches = (None, None)
                    patch = StitchGroup(color=self.color,
                                        stitches=path,
                                        lock_stitches=lock_stitches,
                                        force_lock_stitches=self.force_lock_stitches)
                # simple satin
                elif self.stroke_method == 'zigzag_stitch':
                    patch = self.simple_satin(path, self.zigzag_spacing, self.stroke_width, self.pull_compensation)
                # running stitch
                else:
                    patch = self.running_stitch(path, self.running_stitch_length, self.running_stitch_tolerance)
                    # bean stitch
                    if any(self.bean_stitch_repeats):
                        patch.stitches = self.do_bean_repeats(patch.stitches)

                if patch:
                    patches.append(patch)

        return patches

    @cache
    def get_guide_line(self):
        guide_lines = get_marker_elements(self.node, "guide-line", False, True, True)
        # No or empty guide line
        # if there is a satin guide line, it will also be in stroke, so no need to check for satin here
        if not guide_lines or not guide_lines['stroke']:
            return None

        # use the satin guide line if there is one, else use stroke
        # ignore multiple guide lines
        if len(guide_lines['satin']) >= 1:
            return guide_lines['satin'][0]
        return guide_lines['stroke'][0]

    def _representative_point(self):
        # if we just take the center of a line string we could end up on some point far away from the actual line
        try:
            coords = list(self.shape.coords)
        except NotImplementedError:
            # linear rings to not have a coordinate sequence
            coords = list(self.shape.exterior.coords)
        return coords[int(len(coords)/2)]

    def validation_warnings(self):
        # satin column warning
        if self.get_boolean_param("satin_column", False):
            yield TooFewSubpathsWarning(self._representative_point())
        # guided fill warnings
        if self.stroke_method == 1:
            guide_lines = get_marker_elements(self.node, "guide-line", False, True, True)
            if sum(len(x) for x in guide_lines.values()) > 1:
                yield MultipleGuideLineWarning(self._representative_point())

        stroke_width, units = parse_length_with_units(self.get_style("stroke-width", "1"))
