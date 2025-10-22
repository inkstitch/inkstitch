# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import itertools
import typing
from copy import deepcopy
from itertools import chain

import numpy as np
from inkex import Path
from shapely import affinity as shaffinity
from shapely import geometry as shgeo
from shapely import set_precision
from shapely.ops import nearest_points, substring

from ..debug.debug import debug
from ..i18n import _
from ..metadata import InkStitchMetadata
from ..stitch_plan import Stitch, StitchGroup
from ..stitches import running_stitch
from ..svg import line_strings_to_coordinate_lists
from ..svg.styles import get_join_style_args
from ..utils import Point, cache, cut, cut_multiple, offset_points, prng
from ..utils.param import ParamOption
from ..utils.threading import check_stop_flag
from .element import PIXELS_PER_MM, EmbroideryElement, param
from .utils.stroke_to_satin import convert_path_to_satin, set_first_node
from .validation import ValidationError, ValidationWarning


class NotStitchableError(ValidationError):
    name = _("Not stitchable satin column")
    description = _("A satin column consists out of two rails and one or more rungs. This satin column may have a different setup.")
    steps_to_solve = [
        _('Make sure your satin column is not a combination of multiple satin columns.'),
        _('Go to our website and read how a satin column should look like https://inkstitch.org/docs/stitches/satin-column/'),
    ]


rung_message = _("Each rung should intersect both rails once.")


class ClosedPathWarning(ValidationWarning):
    name = _("Rail is a closed path")
    description = _("Rail is a closed path without a definite starting and ending point.")
    steps_to_solve = [
        _('* Select the node where you want the satin to start.'),
        _('* Click on: Break path at selected nodes.')
    ]


class DanglingRungWarning(ValidationWarning):
    name = _("Rung doesn't intersect rails")
    description = _("Satin column: A rung doesn't intersect both rails.") + " " + rung_message


class NoRungWarning(ValidationWarning):
    name = _("Satin has no rungs")
    description = _("Rungs control the stitch direction in satin columns. It is best pratice to use them.")
    steps_to_solve = [
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing a rung.')
    ]


class TooManyIntersectionsWarning(ValidationWarning):
    name = _("Rungs intersects too many times")
    description = _("Satin column: A rung intersects a rail more than once.") + " " + rung_message


class StrokeSatinWarning(ValidationWarning):
    name = _("Simple Satin")
    description = ("If you need more control over the stitch directions within this satin column, convert it to a real satin path")
    steps_to_solve = [
        _('* Select the satin path'),
        _('* Run Extensions > Ink/Stitch > Tools: Satin > Stroke to Satin')
    ]


class TwoRungsWarning(ValidationWarning):
    name = _("Satin has exactly two rungs")
    description = _("There are exactly two rungs. This may lead to false rail/rung detection.")
    steps_to_solve = [
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing a rung.')
    ]


class UnequalPointsWarning(ValidationWarning):
    name = _("Unequal number of points")
    description = _("Satin column: There are no rungs and rails have an unequal number of points.")
    steps_to_solve = [
        _('The easiest way to solve this issue is to add one or more rungs. '),
        _('Rungs control the stitch direction in satin columns.'),
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing the rung.')
    ]


class SatinColumn(EmbroideryElement):
    name = "SatinColumn"
    element_name = _("Satin Column")

    def __init__(self, *args, **kwargs):
        super(SatinColumn, self).__init__(*args, **kwargs)

    @property
    @param('satin_column', _('Custom satin column'), type='toggle')
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    _satin_methods = [ParamOption('satin_column', _('Satin Column')),
                      ParamOption('e_stitch', _('"E" Stitch')),
                      ParamOption('s_stitch', _('"S" Stitch')),
                      ParamOption('zigzag', _('Zig-zag'))]

    @property
    @param('satin_method',
           _('Method'),
           type='combo',
           default=0,
           options=_satin_methods,
           sort_index=0)
    def satin_method(self):
        return self.get_param('satin_method', 'satin_column')

    @property
    @param('random_width_decrease_percent',
           _('Random percentage of satin width decrease'),
           tooltip=_('shorten stitch across rails at most this percent. '
                     'Two values separated by a space may be used for an asymmetric effect.'),
           default=0, type='float', unit=_("% (each side)"), sort_index=91)
    @cache
    def random_width_decrease(self):
        return self.get_split_float_param("random_width_decrease_percent", (0, 0)) / 100

    @property
    @param('random_width_increase_percent',
           _('Random percentage of satin width increase'),
           tooltip=_('lengthen stitch across rails at most this percent. '
                     'Two values separated by a space may be used for an asymmetric effect.'),
           default=0, type='float', unit=_("% (each side)"), sort_index=90)
    @cache
    def random_width_increase(self):
        return self.get_split_float_param("random_width_increase_percent", (0, 0)) / 100

    @property
    @param('random_zigzag_spacing_percent',
           _('Random zig-zag spacing percentage'),
           tooltip=_('Amount of random jitter added to zigzag spacing.'),
           default=0, type='float', unit="± %", sort_index=92)
    def random_zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return max(self.get_float_param("random_zigzag_spacing_percent", 0), 0) / 100

    _split_methods = [ParamOption('default', _('Default')),
                      ParamOption('simple', _('Simple')),
                      ParamOption('staggered', _('Staggered'))]

    @property
    @param('split_method',
           _('Split Method'),
           type='combo',
           tooltip=_('Display needle penetration points in simulator to see the effect of each split method.'),
           default=0,
           options=_split_methods,
           sort_index=93)
    def split_method(self):
        return self.get_param('split_method', 'default')

    @property
    @param('max_stitch_length_mm',
           _('Maximum stitch length'),
           tooltip=_('Maximum stitch length for split stitches.'),
           type='float',
           unit="mm",
           sort_index=94)
    def max_stitch_length_px(self):
        return self.get_float_param("max_stitch_length_mm") or None

    @property
    @param('random_split_jitter_percent',
           _('Random jitter for split stitches'),
           tooltip=_('Randomizes split stitch length if random phase is enabled, stitch position if disabled.'),
           select_items=[('split_method', 'default')],
           default=0, type='float', unit="± %", sort_index=95)
    def random_split_jitter(self):
        return min(max(self.get_float_param("random_split_jitter_percent", 0), 0), 100) / 100

    @property
    @param('random_split_phase',
           _('Random phase for split stitches'),
           tooltip=_('Controls whether split stitches are centered or with a random phase (which may increase stitch count).'),
           select_items=[('split_method', 'default')],
           default=False, type='boolean', sort_index=96)
    def random_split_phase(self):
        return self.get_boolean_param('random_split_phase')

    @property
    @param('min_random_split_length_mm',
           _('Minimum length for random-phase split'),
           tooltip=_('Defaults to maximum stitch length. Smaller values allow for a transition between single-stitch and split-stitch.'),
           select_items=[('split_method', 'default')],
           default='', type='float', unit='mm', sort_index=97)
    def min_random_split_length_px(self):
        if self.max_stitch_length_px is None:
            return None
        return min(self.max_stitch_length_px, self.get_float_param('min_random_split_length_mm', self.max_stitch_length_px))

    @property
    @param('split_staggers',
           _('Stagger split stitches this many times before repeating'),
           # This tooltip is _exactly_ the same as the one for FillStitch.staggers, which
           # means it will be translated the same.
           tooltip=_('Length of the cycle by which successive stitch rows are staggered. '
                     'Fractional values are allowed and can have less visible diagonals than integer values.'),
           select_items=[('split_method', 'staggered')],
           default=4, type='float', sort_index=98)
    def split_staggers(self):
        return self.get_float_param('split_staggers', 4)

    @property
    @param('short_stitch_inset',
           _('Short stitch inset'),
           tooltip=_('Stitches in areas with high density will be inset by this amount.'
                     'Two values separated by a space define inset levels if there are multiple consecutive short stitches.'),
           type='float',
           unit="%",
           default=15,
           sort_index=3)
    def short_stitch_inset(self):
        short_stitch_sequence = self.get_multiple_float_param("short_stitch_inset", "15")
        return [min(short_stitch / 100, 0.5) for short_stitch in short_stitch_sequence]

    @property
    @param('short_stitch_distance_mm',
           _('Short stitch distance'),
           tooltip=_('Inset stitches if the distance between stitches is smaller than this.'),
           type='float',
           unit="mm",
           default=0.25,
           sort_index=4)
    def short_stitch_distance(self):
        return self.get_float_param("short_stitch_distance_mm", 0.25)

    @property
    def color(self):
        return self.stroke_color

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Peak-to-peak distance between zig-zags. This is double the mm/stitch measurement used by most mechanical machines.'),
           unit='mm/cycle',
           type='float',
           default=0.4,
           sort_index=5)
    def zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param(
        'pull_compensation_percent',
        _('Pull compensation percentage'),
        tooltip=_('Additional pull compensation which varies as a percentage of stitch width. '
                  'Two values separated by a space may be used for an asymmetric effect.'),
        unit=_('% (each side)'),
        type='float',
        default=0,
        sort_index=6)
    @cache
    def pull_compensation_percent(self):
        # pull compensation as a percentage of the width
        return self.get_split_float_param("pull_compensation_percent", (0, 0))

    @property
    @param(
        'pull_compensation_mm',
        _('Pull compensation'),
        tooltip=_('Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape. '
                  'This setting expands each pair of needle penetrations outward from the center of the satin column by a fixed length. '
                  'Two values separated by a space may be used for an asymmetric effect.'),
        unit=_('mm (each side)'),
        type='float',
        default=0,
        sort_index=7)
    @cache
    def pull_compensation_px(self):
        # In satin stitch, the stitches have a tendency to pull together and
        # narrow the entire column.  We can compensate for this by stitching
        # wider than we desire the column to end up.
        return self.get_split_mm_param_as_px("pull_compensation_mm", (0, 0))

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
        tooltip=_('This may help if your satin renders very strangely.  ' +
                  'Default: automatically detect and fix a reversed rail.'),
        type='combo',
        options=_reverse_rails_options,
        default='automatic',
        sort_index=10)
    def reverse_rails(self):
        return self.get_param('reverse_rails', 'automatic')

    def _get_rails_to_reverse(self):
        choice = self.reverse_rails

        if choice == 'first':
            return True, False
        elif choice == 'second':
            return False, True
        elif choice == 'both':
            return True, True
        elif choice == 'automatic':
            rails = [shgeo.LineString(rail) for rail in self.rails]
            if len(rails) == 2:
                # Sample ten points along the rails.  Compare the distance
                # between corresponding points on both rails with and without
                # one rail reversed.  If the average distance between points
                # with one rail reversed is less than without one reversed, then
                # the user has probably accidentally reversed a rail.
                lengths = []
                lengths_reverse = []

                for i in range(10):
                    distance = i / 10
                    point0 = rails[0].interpolate(distance, normalized=True)
                    point1 = rails[1].interpolate(distance, normalized=True)
                    point1_reverse = rails[1].interpolate(1 - distance, normalized=True)

                    lengths.append(point0.distance(point1))
                    lengths_reverse.append(point0.distance(point1_reverse))

                debug.log(f"lengths: {lengths}")
                debug.log(f"lengths_reverse: {lengths_reverse}")
                if sum(lengths) > sum(lengths_reverse):
                    # reverse the second rail
                    return False, True

        return False, False

    @property
    @param(
        'swap_satin_rails',
        _('Swap rails'),
        tooltip=_('Swaps the first and second rails of the satin column, '
                  'affecting which side the thread finished on as well as any sided properties'),
        type='boolean',
        default='false',
        sort_index=11)
    def swap_rails(self):
        return self.get_boolean_param('swap_satin_rails', False)

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches for start and end point connections.'),
           unit='mm',
           type='float',
           default=2.5,
           sort_index=20)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 2.5), 0.01)

    @property
    @param('running_stitch_tolerance_mm',
           _('Running stitch tolerance'),
           tooltip=_('Determines how hard Ink/Stitch tries to avoid stitching outside the shape.'
                     'Lower numbers are less likely to stitch outside the shape but require more stitches.'),
           unit='mm',
           type='float',
           default=0.1,
           sort_index=21)
    def running_stitch_tolerance(self):
        return max(self.get_float_param("running_stitch_tolerance_mm", 0.2), 0.01)

    @property
    @param('running_stitch_position',
           _('Running Stitch Position'),
           tooltip=_('Position of running stitches between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.'),
           type='float', unit='%', default=50,
           sort_index=22)
    def running_stitch_position(self):
        return min(100, max(0, self.get_float_param("running_stitch_position", 50)))

    @property
    @param('start_at_nearest_point',
           _('Start at nearest point'),
           tooltip=_('Start at nearest point to previous element. A start position command will overwrite this setting.'),
           default=True, type='boolean', sort_index=23)
    def start_at_nearest_point(self):
        return self.get_boolean_param('start_at_nearest_point', True)

    @property
    @param('end_at_nearest_point',
           _('End at nearest point'),
           tooltip=_('End at nearest point to the next element. An end position command will overwrite this setting.'),
           default=True, type='boolean', sort_index=24)
    def end_at_nearest_point(self):
        return self.get_boolean_param('end_at_nearest_point', True)

    @property
    @param('contour_underlay', _('Contour underlay'), type='toggle', group=_('Contour Underlay'))
    def contour_underlay(self):
        # "Contour underlay" is stitching just inside the rectangular shape
        # of the satin column; that is, up one side and down the other.
        return self.get_boolean_param("contour_underlay")

    @property
    @param('contour_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Contour Underlay'), type='float', default=3)
    def contour_underlay_stitch_length(self):
        return max(self.get_float_param("contour_underlay_stitch_length_mm", 3), 0.01)

    @property
    @param(
        'contour_underlay_stitch_tolerance_mm',
        _('Stitch tolerance'),
        tooltip=_(
            'All stitches must be within this distance from the path. '
            'A lower tolerance means stitches will be closer together. '
            'A higher tolerance means sharp corners may be rounded. '
        ),
        unit='mm',
        group=_('Contour Underlay'),
        type='float',
        default=0.2,
    )
    def contour_underlay_stitch_tolerance(self):
        tolerance = self.get_float_param("contour_underlay_stitch_tolerance_mm", 0.2)
        return max(tolerance, 0.01 * PIXELS_PER_MM)  # sanity check to prevent crash from excessively-small values

    @property
    @param('contour_underlay_inset_mm',
           _('Inset distance (fixed)'),
           tooltip=_('Shrink the outline by a fixed length, to prevent the underlay from showing around the outside of the satin column.'),
           group=_('Contour Underlay'),
           unit=_('mm (each side)'),
           type='float',
           default=0.4,
           sort_index=2)
    @cache
    def contour_underlay_inset_px(self):
        # how far inside the edge of the column to stitch the underlay
        return self.get_split_mm_param_as_px("contour_underlay_inset_mm", (0.4, 0.4))

    @property
    @param('contour_underlay_inset_percent',
           _('Inset distance (proportional)'),
           tooltip=_('Shrink the outline by a proportion of the column width, '
                     'to prevent the underlay from showing around the outside of the satin column.'),
           group=_('Contour Underlay'),
           unit=_('% (each side)'), type='float', default=0,
           sort_index=3)
    @cache
    def contour_underlay_inset_percent(self):
        # how far inside the edge of the column to stitch the underlay
        return self.get_split_float_param("contour_underlay_inset_percent", (0, 0))

    @property
    @param('center_walk_underlay', _('Center-walk underlay'), type='toggle', group=_('Center-Walk Underlay'))
    def center_walk_underlay(self):
        # "Center walk underlay" is stitching down and back in the centerline
        # between the two sides of the satin column.
        return self.get_boolean_param("center_walk_underlay")

    @property
    @param('center_walk_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Center-Walk Underlay'), type='float', default=3)
    def center_walk_underlay_stitch_length(self):
        return max(self.get_float_param("center_walk_underlay_stitch_length_mm", 3), 0.01)

    @property
    @param(
        'center_walk_underlay_stitch_tolerance_mm',
        _('Stitch tolerance'),
        tooltip=_(
            'All stitches must be within this distance from the path. '
            'A lower tolerance means stitches will be closer together. '
            'A higher tolerance means sharp corners may be rounded. '
            'Defaults to stitch length.'
        ),
        unit='mm',
        group=_('Center-Walk Underlay'),
        type='float',
        default=0.2
    )
    def center_walk_underlay_stitch_tolerance(self):
        tolerance = self.get_float_param("center_walk_underlay_stitch_tolerance_mm", 0.2)
        return max(tolerance, 0.01 * PIXELS_PER_MM)

    @property
    @param('center_walk_underlay_repeats',
           _('Repeats'),
           tooltip=_('For an odd number of repeats, this will reverse the direction the satin column is stitched, '
                     'causing stitching to both begin and end at the start point.'),
           group=_('Center-Walk Underlay'),
           type='int', default=2,
           sort_index=2)
    def center_walk_underlay_repeats(self):
        return max(self.get_int_param("center_walk_underlay_repeats", 2), 1)

    @property
    @param('center_walk_underlay_position',
           _('Position'),
           tooltip=_('Position of underlay from between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.'),
           group=_('Center-Walk Underlay'),
           type='float', unit='%', default=50,
           sort_index=3)
    def center_walk_underlay_position(self):
        return min(100, max(0, self.get_float_param("center_walk_underlay_position", 50)))

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
           _('Inset amount (fixed)'),
           tooltip=_('default: half of contour underlay inset'),
           unit=_('mm (each side)'),
           group=_('Zig-zag Underlay'),
           type='float',
           default="")
    def zigzag_underlay_inset_px(self):
        # how far in from the edge of the satin the points in the zigzags
        # should be

        # Default to half of the contour underlay inset.  That is, if we're
        # doing both contour underlay and zigzag underlay, make sure the
        # points of the zigzag fall outside the contour underlay but inside
        # the edges of the satin column.
        default = self.contour_underlay_inset_px * 0.5 / PIXELS_PER_MM
        x = self.get_split_mm_param_as_px("zigzag_underlay_inset_mm", default)
        return x

    @property
    @param('zigzag_underlay_inset_percent',
           _('Inset amount (proportional)'),
           tooltip=_('default: half of contour underlay inset'),
           unit=_('% (each side)'),
           group=_('Zig-zag Underlay'),
           type='float',
           default="")
    @cache
    def zigzag_underlay_inset_percent(self):
        default = self.contour_underlay_inset_percent * 0.5
        return self.get_split_float_param("zigzag_underlay_inset_percent", default)

    @property
    @param('zigzag_underlay_max_stitch_length_mm',
           _('Maximum stitch length'),
           tooltip=_('Split stitch if distance of maximum stitch length is exceeded'),
           unit='mm',
           group=_('Zig-zag Underlay'),
           type='float',
           default="")
    def zigzag_underlay_max_stitch_length(self):
        return self.get_float_param("zigzag_underlay_max_stitch_length_mm") or None

    @property
    @param('random_seed',
           _('Random seed'),
           tooltip=_('Use a specific seed for randomized attributes. Uses the element ID if empty.'),
           type='random_seed',
           default='',
           sort_index=100)
    @cache
    def random_seed(self) -> str:
        seed = self.get_param('random_seed', '')
        if not seed:
            seed = self.node.get_id() or ''
            # TODO(#1696): When inplementing grouped clones, join this with the IDs of any shadow roots,
            # letting each instance without a specified seed get a different default.
        return seed

    @property
    @cache
    def shape(self):
        # This isn't used for satins at all, but other parts of the code
        # may need to know the general shape of a satin column.

        return shgeo.MultiLineString(self.line_string_rails)

    @property
    @cache
    def compensated_shape(self):
        pairs = self.plot_points_on_rails(
            self.zigzag_spacing,
            self.pull_compensation_px,
            self.pull_compensation_percent/100,
            True,
        )
        if len(pairs) == 1:
            # we need at least two points for line string creation
            # if there is only one, we simply duplicate it to prevent an error
            pairs.append(pairs[0])
        rail1 = [point[0] for point in pairs]
        rail2 = [point[1] for point in pairs]
        return shgeo.MultiLineString((rail1, rail2))

    @property
    @cache
    def filtered_subpaths(self):
        paths = [path for path in self.paths if len(path) > 1]
        if len(paths) == 1:
            style_args = get_join_style_args(self)
            if self.is_closed_path:
                set_first_node(paths, self.stroke_width)
            new_satin = convert_path_to_satin(paths[0], self.stroke_width, style_args, rungs_at_nodes=True)
            if new_satin:
                rails, rungs = new_satin
                paths = list(rails) + list(rungs)
        return paths

    @property
    @cache
    def rails(self):
        """The rails in order, as point lists"""
        rails = [subpath for i, subpath in enumerate(self.filtered_subpaths) if i in self.rail_indices]
        if len(rails) == 2 and self.swap_rails:
            return [rails[1], rails[0]]
        else:
            return rails

    @property
    @cache
    def line_string_rails(self):
        """The rails, as LineStrings."""
        paths = [set_precision(shgeo.LineString(rail), 0.00001) for rail in self.rails]

        rails_to_reverse = self._get_rails_to_reverse()
        if paths and rails_to_reverse is not None:
            for i, reverse in enumerate(rails_to_reverse):
                if reverse:
                    paths[i] = shgeo.LineString(paths[i].coords[::-1])

        # if one of the rails has no nodes, return an empty tuple
        if any([path.is_empty for path in paths]):
            return tuple()

        return tuple(paths)

    @property
    @cache
    def line_string_rungs(self):
        """The rungs as LineStrings"""
        return tuple(shgeo.LineString(rung) for rung in self.rungs)

    @property
    @cache
    def rungs(self):
        """The rungs, as point lists.

        If there are no rungs, then this is an old-style satin column.  The
        rails are expected to have the same number of path nodes.  The path
        nodes, taken in sequential pairs, act in the same way as rungs would.
        """
        if len(self.filtered_subpaths) == 2:
            # It's an old-style satin column.  To make things easier we'll
            # actually create the implied rungs.
            return self._synthesize_rungs()
        else:
            return [subpath for i, subpath in enumerate(self.filtered_subpaths) if i not in self.rail_indices]

    @cache
    def _synthesize_rungs(self):
        rung_endpoints = []
        # check for unequal length of rails
        equal_length = len(self.rails[0]) == len(self.rails[1])

        rails_to_reverse = self._get_rails_to_reverse()
        for i, points in enumerate(self.rails):

            if rails_to_reverse[i]:
                points = points[::-1]

            if len(points) > 2 or not equal_length:
                # Don't bother putting rungs at the start and end.
                points = points[1:-1]
            else:
                # But do include one near the start if we wouldn't add one otherwise.
                # This avoids confusing other parts of the code.
                linestring_rail = shgeo.LineString(points)
                points = [linestring_rail.interpolate(0.2)]

            rung_endpoints.append(points)

        rungs = []
        for start, end in zip(*rung_endpoints):
            rung = shgeo.LineString((start, end))
            # make it a bit bigger so that it definitely intersects
            rung = shaffinity.scale(rung, 1.1, 1.1).coords
            rungs.append(rung)

        return rungs

    @property
    @cache
    def rail_indices(self):
        paths = [shgeo.LineString(path) for path in self.filtered_subpaths if len(path) > 1]
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

        # We need to distinguish between two cases. Three subpath are satins with exactly one rung and
        # rails have exactly one intersection. This case has to be distinguished from the case of short
        # coming rungs with only one intersection.
        if len(paths) == 3:
            possible_rails = [i for i in range(num_paths) if intersection_counts[i] == 1 and paths[i].length > 0.001]
        else:
            possible_rails = [i for i in range(num_paths) if intersection_counts[i] > 2 and paths[i].length > 0.001]
        num_possible_rails = len(possible_rails)

        if num_possible_rails == 2:
            # Great, we have two unambiguous rails.
            return possible_rails
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

    @property
    @cache
    def min_stitch_len(self):
        metadata = InkStitchMetadata(self.node.root)
        return metadata['min_stitch_len_mm'] * PIXELS_PER_MM

    @property
    @cache
    def flattened_sections(self):
        """Flatten the rails, cut with the rungs, and return the sections in pairs."""

        rails = list(self.line_string_rails)
        rungs = list(self.line_string_rungs)
        cut_points = [[], []]
        for rung in rungs:
            intersections = rung.intersection(shgeo.MultiLineString(rails))
            # ignore the rungs that are cutting a rail multiple times
            if isinstance(intersections, shgeo.MultiPoint) and len(intersections.geoms) > 2:
                continue
            for i, rail in enumerate(rails):
                point_on_rung, point_on_rail = nearest_points(rung, rail)
                cut_points[i].append(rail.project(point_on_rail))

        for i, rail in enumerate(rails):
            rails[i] = cut_multiple(rail, cut_points[i])

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

    def validation_warnings(self):  # noqa: C901
        paths = self.node.get_path()
        if any([path.letter == 'Z' for path in paths]):
            yield ClosedPathWarning(self.line_string_rails[0].coords[0])

        if len(self.paths) == 1:
            yield StrokeSatinWarning(self.center_line.interpolate(0.5, normalized=True))
        elif len(self.filtered_subpaths) == 4:
            yield TwoRungsWarning(self.line_string_rails[0].interpolate(0.5, normalized=True))
        elif len(self.filtered_subpaths) == 2:
            yield NoRungWarning(self.line_string_rails[1].representative_point())
            if len(self.rails[0]) != len(self.rails[1]):
                yield UnequalPointsWarning(self.line_string_rails[0].interpolate(0.5, normalized=True))
        elif len(self.filtered_subpaths) > 2:
            for rung in self.line_string_rungs:
                for rail in self.line_string_rails:
                    intersection = rung.intersection(rail)
                    if intersection.is_empty:
                        yield DanglingRungWarning(rung.interpolate(0.5, normalized=True))
                    elif not isinstance(intersection, shgeo.Point):
                        yield TooManyIntersectionsWarning(rung.interpolate(0.5, normalized=True))

    def validation_errors(self):
        if len(self.line_string_rails) == 0:
            # Non existing rails can happen due to insane transforms which reduce the size of the
            # satin to zero. The path should still be pointable.
            try:
                point = self.paths[0][0]
            except IndexError:
                point = (0, 0)
            yield NotStitchableError(point)

        elif not self.to_stitch_groups() and self.line_string_rails:
            yield NotStitchableError(self.line_string_rails[0].representative_point())

    def _center_walk_is_odd(self):
        return self.center_walk_underlay and self.center_walk_underlay_repeats % 2 == 1

    def reverse(self):
        """Return a new SatinColumn like this one but in the opposite direction.

        The new satin will contain a new XML node that is not yet in the SVG.
        """
        point_lists = []

        for rail in self.rails:
            point_lists.append(list(reversed(rail)))

        for rung in self.rungs:
            point_lists.append(rung)

        # If originally there were only two subpaths (no rungs) with same number of points, the rails may now
        # have two rails with different number of points, and still no rungs, let's add one.

        if not self.rungs:
            rails = [shgeo.LineString(reversed(rail)) for rail in self.rails]
            rails.reverse()
            path_list = rails

            rung_start = path_list[0].interpolate(0.2)
            rung_end = path_list[1].interpolate(0.2)
            rung = shgeo.LineString((rung_start, rung_end))
            # make it a bit bigger so that it definitely intersects
            rung = shaffinity.scale(rung, 1.1, 1.1)
            path_list.append(rung)
            return (self._path_list_to_satins(path_list))

        return self._coordinates_to_satin(point_lists)

    def flip(self):
        """Return a new SatinColumn like this one but with flipped rails.

        The new satin will contain a new XML
        node that is not yet in the SVG.
        """
        path = self.filtered_subpaths

        if len(path) > 1:
            first, second = self.rail_indices
            path[first], path[second] = path[second], path[first]

        return self._coordinates_to_satin(path)

    def apply_transform(self):
        """Return a new SatinColumn like this one but with transforms applied.

        This node's and all ancestor nodes' transforms will be applied.  The
        new SatinColumn's node will not be in the SVG document.
        """

        return self._coordinates_to_satin(self.filtered_subpaths)

    def split(self, split_point, cut_points=None):
        """Split a satin into two satins at the specified point

        split_point is a point on or near one of the rails, not at one of the
        ends. Finds corresponding point on the other rail (taking into account
        the rungs) and breaks the rails at these points.

        split_point can also be a normalized projection of a distance along the
        satin, in the range 0.0 to 1.0.

        Returns two new SatinColumn instances: the part before and the part
        after the split point.  All parameters are copied over to the new
        SatinColumn instances.

        The returned SatinColumns will not be in the SVG document and will have
        their transforms applied.
        """

        if cut_points is None:
            cut_points = self.find_cut_points(split_point)
        path_lists = self._cut_rails(cut_points)

        # prevent error when split points lies at the start or end of the satin column
        cleaned_path_lists = path_lists
        for i, path_list in enumerate(path_lists):
            if None in path_list:
                cleaned_path_lists[i] = None
                continue
            for path in path_list:
                if shgeo.LineString(path).length < self.zigzag_spacing:
                    cleaned_path_lists[i] = None
        path_lists = cleaned_path_lists

        self._assign_rungs_to_split_rails(path_lists)
        self._add_rungs_if_necessary(path_lists)
        return [self._path_list_to_satins(path_list) for path_list in path_lists]

    def find_cut_points(self, split_point):
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
        points = list(chain.from_iterable(self.plot_points_on_rails(self.zigzag_spacing)))

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

        rails = [shgeo.LineString(rail) for rail in self.rails]

        path_lists = [[], []]

        rails_to_reverse = self._get_rails_to_reverse()

        if rails_to_reverse[0] == rails_to_reverse[1]:
            for i, rail in enumerate(rails):
                before, after = cut(rail, rail.project(shgeo.Point(cut_points[i])))
                path_lists[0].append(before)
                path_lists[1].append(after)
        else:
            # rails have opposite direction
            rail = rails[0]
            before, after = cut(rail, rail.project(shgeo.Point(cut_points[0])))
            path_lists[0].append(before)
            path_lists[1].append(after)
            rail = rails[1]
            before, after = cut(rail, rail.project(shgeo.Point(cut_points[1])))
            path_lists[1].append(before)
            path_lists[0].append(after)

        if rails_to_reverse[0]:
            path_lists = [path_lists[1], path_lists[0]]

        return path_lists

    def _assign_rungs_to_split_rails(self, split_rails):
        """Add this satin's rungs to the new satins.

        Each rung is appended to the correct one of the two new satin columns.
        """

        rungs = [shgeo.LineString(rung) for rung in self.rungs]
        for path_list in split_rails:
            if path_list is not None:
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
            if path_list is None:
                continue
            num_paths = len(path_list)
            if num_paths in (2, 4):
                # Add the rung just after the start of the satin.
                # If the rails have opposite directions it may end up at the end of the satin.
                self._add_rung(path_list, 0.3)
            # When rails are intersecting, add two more rung to prevent bad rail detection
            if num_paths == 2 and path_list[0].intersects(path_list[1]):
                self._add_rung(path_list, 0.5, True)
                self._add_rung(path_list, -0.3)

    def _add_rung(self, path_list, position, normalized=False):
        rung_start = path_list[0].interpolate(position, normalized=normalized)
        rails_to_reverse = self._get_rails_to_reverse()
        if rails_to_reverse[0] == rails_to_reverse[1]:
            rung_end = path_list[1].interpolate(position, normalized=normalized)
        else:
            rung_end = path_list[1].interpolate(-position, normalized=normalized)
        rung = shgeo.LineString((rung_start, rung_end))

        # make it a bit bigger so that it definitely intersects
        rung = shaffinity.scale(rung, 1.1, 1.1)

        if rung.length < 5:
            rung = shaffinity.scale(rung, 3, 3)

        path_list.append(rung)

    def _path_list_to_satins(self, path_list):
        coordinates = line_strings_to_coordinate_lists(path_list)
        if not coordinates:
            return None
        return self._coordinates_to_satin(coordinates)

    def _coordinates_to_satin(self, paths):
        node = deepcopy(self.node)
        d = ""
        for path in paths:
            d += str(Path(path))
        node.set("d", d)

        # we've already applied the transform, so get rid of it
        if node.get("transform"):
            del node.attrib["transform"]

        return SatinColumn(node)

    def _get_filtered_rungs(self, rails, rungs):
        # returns a filtered list of rungs which do intersect the rails exactly twice
        rails = shgeo.MultiLineString(rails)
        filtered_rungs = []
        for rung in shgeo.MultiLineString(rungs).geoms:
            intersection = rung.intersection(rails)
            if intersection.geom_type == "MultiPoint" and len(intersection.geoms) == 2:
                filtered_rungs.append(list(rung.coords))
        return filtered_rungs

    @property
    @cache
    def center_line(self):
        # similar technique to do_center_walk()
        center_walk = [p[0] for p in self.plot_points_on_rails(self.zigzag_spacing, (0, 0), (-0.5, -0.5))]
        if len(center_walk) < 2:
            center_walk = [center_walk[0], center_walk[0]]
        return shgeo.LineString(center_walk)

    @property
    @cache
    def offset_center_line(self):
        stitches = self._get_center_line_stitches(self.running_stitch_position)
        linestring = shgeo.LineString(stitches)
        return linestring

    def _get_center_line_stitches(self, position):
        inset_prop = -np.array([position, 100-position]) / 100

        # Do it like contour underlay, but inset all the way to the center.
        pairs = self.plot_points_on_rails(self.running_stitch_tolerance, (0, 0), inset_prop)

        points = [points[0] for points in pairs]
        stitches = running_stitch.even_running_stitch(points, self.running_stitch_length, self.running_stitch_tolerance)

        if len(stitches) == 1:
            stitches.append(stitches[0])

        return stitches

    def _stitch_distance(self, pos0, pos1, previous_pos0, previous_pos1):
        """Return the distance from one stitch to the next."""

        previous_stitch = previous_pos1 - previous_pos0
        if previous_stitch.length() < 0.01:
            return shgeo.LineString((pos0, pos1)).distance(shgeo.Point(previous_pos0))
        else:
            # Measure the distance at a right angle to the previous stitch, at
            # the start and end of the stitch, and pick the biggest.  If we're
            # going around a curve, the points on the inside of the curve will
            # be much closer together, and we only care about the distance on
            # the outside of the curve.
            #
            # In this example with two horizontal stitches, we want the vertical
            # separation between them.
            #  _________
            #  \_______/
            normal = previous_stitch.unit().rotate_left()
            d0 = pos0 - previous_pos0
            d1 = pos1 - previous_pos1
            return max(abs(d0 * normal), abs(d1 * normal))

    @debug.time
    def plot_points_on_rails(self, spacing, offset_px=(0, 0), offset_proportional=(0, 0), use_random=False,
                             ) -> typing.List[typing.Tuple[Point, Point]]:
        # Take a section from each rail in turn, and plot out an equal number
        # of points on both rails.  Return the points plotted. The points will
        # be contracted or expanded by offset using self.offset_points().

        processor = SatinProcessor(self, offset_px, offset_proportional, use_random)

        pairs = []

        for i, (section0, section1) in enumerate(self.flattened_sections):
            check_stop_flag()

            if i == 0:
                old_pos0 = section0[0]
                old_pos1 = section1[0]
                pairs.append(processor.process_points(old_pos0, old_pos1))

            path0 = shgeo.LineString(section0)
            path1 = shgeo.LineString(section1)

            # Base the number of stitches in each section on the _longer_ of
            # the two sections. Otherwise, things could get too sparse when one
            # side is significantly longer (e.g. when going around a corner).
            num_points = max(path0.length, path1.length, 0.01) / spacing

            # Section stitch spacing and the cursor are expressed as a fraction
            # of the total length of the path, because we use normalized=True
            # below.
            section_stitch_spacing = 1.0 / num_points

            # current_spacing, however, is in pixels.
            spacing_multiple = processor.get_stitch_spacing_multiple()
            current_spacing = spacing * spacing_multiple

            # In all sections after the first, we need to figure out how far to
            # travel before placing the first stitch.
            distance = self._stitch_distance(section0[0], section1[0], old_pos0, old_pos1)
            to_travel = (1 - min(distance / spacing, 1.0)) * section_stitch_spacing * spacing_multiple
            debug.log(f"num_points: {num_points}, section_stitch_spacing: {section_stitch_spacing}, distance: {distance}, to_travel: {to_travel}")

            cursor = 0
            iterations = 0
            while cursor + to_travel <= 1:
                iterations += 1
                pos0 = Point.from_shapely_point(path0.interpolate(cursor + to_travel, normalized=True))
                pos1 = Point.from_shapely_point(path1.interpolate(cursor + to_travel, normalized=True))

                # If the rails are parallel, then our stitch spacing will be
                # perfect.  If the rails are coming together or spreading apart,
                # then we'll have to travel much further along the rails to get
                # the right stitch spacing.  Imagine a satin like the letter V:
                #
                # \______/
                #  \____/
                #   \__/
                #    \/
                #
                # In this case the stitches will be way too close together.
                # We'll compensate for that here.
                #
                # We'll measure how far this stitch is from the previous one.
                # If we went one third as far as we were expecting to, then
                # we'll need to try again, this time travelling 3x as far as we
                # originally tried.
                #
                # This works great for the V, but what if things change
                # mid-stitch?
                #
                # \      /
                #  \    /
                #   \  /
                #    ||
                #
                # In this case, we may way overshoot.  We can also undershoot
                # for similar reasons.  To deal with that, we'll revise our
                # guess a second time.  Two tries seems to be the sweet spot.
                #
                # In any case, we'll only revise if our stitch spacing is off by
                # more than 5%.
                if iterations <= 2:
                    distance = self._stitch_distance(pos0, pos1, old_pos0, old_pos1)
                    if distance > 0.01 and abs((current_spacing - distance) / current_spacing) > 0.05:
                        # We'll revise to_travel then go back to the start of
                        # the loop and try again.
                        to_travel = (current_spacing / distance) * to_travel
                        if iterations == 1:
                            # Don't overshoot the end of this section on the
                            # first try. If we've gone too far, we want to have
                            # a chance to correct.
                            to_travel = min(to_travel, 1 - cursor)
                        continue

                cursor += to_travel
                spacing_multiple = processor.get_stitch_spacing_multiple()
                to_travel = section_stitch_spacing * spacing_multiple
                current_spacing = spacing * spacing_multiple

                old_pos0 = pos0
                old_pos1 = pos1
                pairs.append(processor.process_points(pos0, pos1))
                iterations = 0

        # Add one last stitch at the end unless our previous stitch is already
        # really close to the end.
        if pairs and section0 and section1:
            if self._stitch_distance(section0[-1], section1[-1], old_pos0, old_pos1) > 0.1 * PIXELS_PER_MM:
                pairs.append(processor.process_points(section0[-1], section1[-1]))

        return pairs

    def _connect_stitch_group_with_point(self, first_stitch_group, start_point, end_point=None):
        start_stitch_group = StitchGroup(
            color=self.color,
            stitches=[Stitch(*start_point)]
        )
        connector = self.offset_center_line

        if end_point:
            split_line = shgeo.LineString(self.find_cut_points(end_point))
        else:
            split_line = shgeo.LineString(self.find_cut_points(start_point))
        start = connector.project(nearest_points(split_line, connector)[1])

        if end_point and not self._center_walk_is_odd():
            end = connector.length
        else:
            split_line = shgeo.LineString(self.find_cut_points(first_stitch_group.stitches[0]))
            end = connector.project(nearest_points(split_line, connector)[1])

        start_path = substring(connector, start, end)

        stitches = [Stitch(*coord) for coord in start_path.coords]
        stitch_group = StitchGroup(
            color=self.color,
            stitches=stitches
        )
        stitch_group = self.connect_and_add(start_stitch_group, stitch_group)
        stitch_group.add_tags(("satin_column", "satin_column_underlay"))
        return stitch_group

    def do_end_path(self, end_point):
        return StitchGroup(
            color=self.color,
            tags=("satin_column",),
            stitches=[Point(*end_point)]
        )

    def _do_underlay_stitch_groups(self, end_point):
        stitch_groups = []
        if self.center_walk_underlay:
            stitch_groups.extend(self.do_center_walk(end_point))

        if self.contour_underlay:
            stitch_groups.extend(self.do_contour_underlay(end_point))

        if self.zigzag_underlay:
            stitch_groups.extend(self.do_zigzag_underlay(end_point))

        return stitch_groups

    def _to_stitch_group(self, linestring, tags, reverse=False):
        if reverse:
            linestring = linestring.reverse()
        return StitchGroup(
                color=self.color,
                tags=tags,
                stitches=[Stitch(*coord) for coord in linestring.coords]
            )

    def do_contour_underlay(self, end_point):
        # "contour walk" underlay: do stitches up one side and down the
        # other. if the two sides are far away, adding a running stitch to travel
        # in between avoids a long jump or a trim.

        pairs = self.plot_points_on_rails(
            self.contour_underlay_stitch_tolerance,
            -self.contour_underlay_inset_px, -self.contour_underlay_inset_percent/100)

        if not pairs:
            return []

        first_side = running_stitch.even_running_stitch(
            [points[0] for points in pairs],
            self.contour_underlay_stitch_length,
            self.contour_underlay_stitch_tolerance
        )
        second_side = running_stitch.even_running_stitch(
            [points[1] for points in pairs],
            self.contour_underlay_stitch_length,
            self.contour_underlay_stitch_tolerance
        )

        if self._center_walk_is_odd():
            first_side.reverse()
        else:
            second_side.reverse()

        if end_point:
            stitch_groups = []
            tags = ("satin_column", "satin_column_underlay", "satin_contour_underlay")
            first_linestring = shgeo.LineString(first_side)
            first_start, first_end = self._split_linestring_at_end_point(first_linestring, end_point)
            second_linestring = shgeo.LineString(second_side)
            second_end, second_start = self._split_linestring_at_end_point(second_linestring, end_point)
            stitch_groups.append(self._to_stitch_group(first_start, tags))
            stitch_groups.append(self._to_stitch_group(second_end, tags))
            stitch_groups.append(self._to_stitch_group(second_start, tags))
            stitch_groups.append(self._to_stitch_group(first_end, tags))
            return stitch_groups

        stitch_group = StitchGroup(
            color=self.color,
            tags=("satin_column", "satin_column_underlay", "satin_contour_underlay"),
            stitches=first_side
        )

        self.add_running_stitches(first_side[-1], second_side[0], stitch_group)
        stitch_group.stitches += second_side
        return [stitch_group]

    def do_center_walk(self, end_point):
        # Center walk underlay is just a running stitch down and back on the
        # center line between the bezier curves.
        repeats = self.center_walk_underlay_repeats

        stitch_groups = []
        stitches = self._get_center_line_stitches(self.center_walk_underlay_position)
        if end_point:
            tags = ("satin_column", "satin_column_underlay", "satin_center_walk")
            stitches = shgeo.LineString(stitches)
            start, end = self._split_linestring_at_end_point(stitches, end_point)
            if self._center_walk_is_odd():
                end, start = start, end
            stitch_groups.append(self._to_stitch_group(start, tags))
            stitch_groups.append(self._to_stitch_group(end, tags, True))
        else:
            stitch_group = StitchGroup(
                color=self.color,
                tags=("satin_column", "satin_column_underlay", "satin_center_walk"),
                stitches=stitches
            )
            stitch_groups.append(stitch_group)

        for stitch_group in stitch_groups:
            stitch_count = len(stitch_group.stitches)
            for i in range(repeats - 1):
                if i % 2 == 0:
                    stitch_group.stitches += reversed(stitch_group.stitches[:stitch_count])
                else:
                    stitch_group.stitches += stitch_group.stitches[:stitch_count]
        return stitch_groups

    def do_zigzag_underlay(self, end_point):
        # zigzag underlay, usually done at a much lower density than the
        # satin itself.  It looks like this:
        #
        # \/\/\/\/\/\/\/\/\/\/|
        # /\/\/\/\/\/\/\/\/\/\|
        #
        # In combination with the "contour walk" underlay, this is the
        # "German underlay" described here:
        #   http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/

        stitch_groups = []

        pairs = self.plot_points_on_rails(self.zigzag_underlay_spacing / 2.0,
                                          -self.zigzag_underlay_inset_px,
                                          -self.zigzag_underlay_inset_percent/100)

        if self._center_walk_is_odd():
            pairs = list(reversed(pairs))

        # This organizes the points in each side in the order that they'll be visited.
        # take a point, from each side in turn, then go backed over the other points
        point_groups = [p[i % 2] for i, p in enumerate(pairs)], list(reversed([p[i % 2] for i, p in enumerate(pairs, 1)]))

        start_groups = []
        end_groups = []
        for points in point_groups:
            if not end_point:
                stitch_groups.append(self._generate_zigzag_stitch_group(points))
                continue
            if len(points) == 1:
                points.append(points[0])
            zigzag_line = shgeo.LineString(points)
            start, end = self._split_linestring_at_end_point(zigzag_line, end_point)
            start_groups.append(self._generate_zigzag_stitch_group([Stitch(*point) for point in start.coords]))
            end_groups.append(self._generate_zigzag_stitch_group([Stitch(*point) for point in end.coords]))
        if start_groups:
            stitch_groups.append(self.connect_and_add(start_groups[0], end_groups[-1]))
            stitch_groups.append(self.connect_and_add(start_groups[-1], end_groups[0]))

        return stitch_groups

    def _generate_zigzag_stitch_group(self, points):
        max_len = self.zigzag_underlay_max_stitch_length
        last_point = None
        stitch_group = StitchGroup(color=self.color)
        for point in points:
            if last_point and max_len:
                if last_point.distance(point) > max_len:
                    split_points = running_stitch.split_segment_even_dist(last_point, point, max_len)
                    for p in split_points:
                        stitch_group.add_stitch(p, ("split_stitch",))
            last_point = point
            stitch_group.add_stitch(point, ("edge",))
        stitch_group.add_tags(("satin_column", "satin_column_underlay", "satin_zigzag_underlay"))
        return stitch_group

    def _do_top_layer_stitch_group(self):
        if self.satin_method == 'e_stitch':
            stitch_group = self.do_e_stitch()
        elif self.satin_method == 's_stitch':
            stitch_group = self.do_s_stitch()
        elif self.satin_method == 'zigzag':
            stitch_group = self.do_zigzag()
        else:
            stitch_group = self.do_satin()

        return stitch_group

    def _split_linestring_at_end_point(self, linestring, end_point):
        split_line = set_precision(shgeo.LineString(self.find_cut_points(end_point)), 0.00001)
        if not split_line:
            start = shgeo.Point(linestring.coords[0])
            if start.distance(shgeo.Point(end_point)) < 0.1:
                return start, linestring
            else:
                return linestring, shgeo.Point(linestring.coords[-1])
        split_point = nearest_points(linestring, split_line)[0]
        project = linestring.project(split_point)
        start = substring(linestring, 0, project)
        end = substring(linestring, project, linestring.length)
        return start, end

    def _split_top_layer(self, stitch_group, end_point):
        top_layer = shgeo.LineString(stitch_group.stitches)
        start, end = self._split_linestring_at_end_point(top_layer, end_point)
        stitch_group2 = deepcopy(stitch_group)
        stitch_group2.stitches = [Stitch(*point) for point in end.reverse().coords]
        stitch_group1 = stitch_group
        stitch_group1.stitches = [Stitch(*point) for point in start.coords]
        top_layer_stitch_groups = [stitch_group1, stitch_group2]
        return top_layer_stitch_groups

    def do_satin(self):
        # satin: do a zigzag pattern, alternating between the paths.  The
        # zigzag looks like this to make the satin stitches look perpendicular
        # to the column:
        #
        # |/|/|/|/|/|/|/|/|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        stitch_group = StitchGroup(color=self.color)

        # pull compensation is automatically converted from mm to pixels by get_float_param
        pairs = self.plot_points_on_rails(
            self.zigzag_spacing,
            self.pull_compensation_px,
            self.pull_compensation_percent/100,
            True,
        )

        max_stitch_length = self.max_stitch_length_px
        length_sigma = self.random_split_jitter
        random_phase = self.random_split_phase
        min_split_length = self.min_random_split_length_px
        seed = self.random_seed

        short_pairs = self.inset_short_stitches_sawtooth(pairs)

        last_point = None
        last_short_point = None
        last_count = None
        for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
            if last_point is not None:
                split_points, _ = self.get_split_points(
                    last_point, a, last_short_point, a_short, max_stitch_length, last_count,
                    length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i), row_num=2 * i, from_end=True)
                stitch_group.add_stitches(split_points, ("satin_column", "satin_split_stitch"))

            stitch_group.add_stitch(a_short)
            stitch_group.stitches[-1].add_tags(("satin_column", "satin_column_edge"))

            split_points, last_count = self.get_split_points(
                a, b, a_short, b_short, max_stitch_length, None,
                length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i + 1), row_num=2 * i + 1)
            stitch_group.add_stitches(split_points, ("satin_column", "satin_split_stitch"))

            stitch_group.add_stitch(b_short)
            stitch_group.stitches[-1].add_tags(("satin_column", "satin_column_edge"))
            last_point = b
            last_short_point = b_short

        if self._center_walk_is_odd():
            stitch_group.stitches = list(reversed(stitch_group.stitches))

        return stitch_group

    def do_e_stitch(self):
        # e stitch: do a pattern that looks like the letter "E".  It looks like
        # this:
        #
        # _|_|_|_|_|_|_|_|_|_|_|_|

        stitch_group = StitchGroup(color=self.color)

        pairs = self.plot_points_on_rails(
            self.zigzag_spacing,
            self.pull_compensation_px,
            self.pull_compensation_percent / 100,
            True,
        )

        short_pairs = self.inset_short_stitches_sawtooth(pairs)
        max_stitch_length = self.max_stitch_length_px
        length_sigma = self.random_split_jitter
        random_phase = self.random_split_phase
        min_split_length = self.min_random_split_length_px
        seed = self.random_seed
        last_point = None
        # "left" and "right" here are kind of arbitrary designations meaning
        # a point from the first and second rail respectively
        for i, (left, right), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
            check_stop_flag()
            split_points, _ = self.get_split_points(
                left, right, a_short, b_short, max_stitch_length,
                None, length_sigma, random_phase, min_split_length,
                prng.join_args(seed, 'satin-split', 2 * i + 1), 2 * i + 1)

            # zigzag spacing is wider than stitch length, subdivide
            if last_point is not None and max_stitch_length is not None and self.zigzag_spacing > max_stitch_length:
                points, _ = self.get_split_points(last_point, left, last_point, left, max_stitch_length)
                stitch_group.add_stitches(points)

            stitch_group.add_stitch(a_short, ("edge", "left"))
            stitch_group.add_stitches(split_points, ("split_stitch",))
            stitch_group.add_stitch(b_short, ("edge",))
            stitch_group.add_stitches(split_points[::-1], ("split_stitch",))
            stitch_group.add_stitch(a_short, ("edge",))

            last_point = a_short

        if self._center_walk_is_odd():
            stitch_group.stitches = list(reversed(stitch_group.stitches))

        stitch_group.add_tags(("satin_column", "e_stitch"))
        return stitch_group

    def do_s_stitch(self):
        # S stitch: do a pattern that looks like the letter "S".  It looks like
        # this:
        #   _   _   _   _   _   _
        # _| |_| |_| |_| |_| |_| |

        stitch_group = StitchGroup(color=self.color)

        pairs = self.plot_points_on_rails(
            self.zigzag_spacing,
            self.pull_compensation_px,
            self.pull_compensation_percent / 100,
            True,
        )

        short_pairs = self.inset_short_stitches_sawtooth(pairs)
        max_stitch_length = self.max_stitch_length_px
        length_sigma = self.random_split_jitter
        random_phase = self.random_split_phase
        min_split_length = self.min_random_split_length_px
        seed = self.random_seed
        last_point = None
        for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
            check_stop_flag()
            points = [a_short]
            split_points, _ = self.get_split_points(
                a, b, a_short, b_short, max_stitch_length,
                None, length_sigma, random_phase, min_split_length,
                prng.join_args(seed, 'satin-split', i), i)
            points.extend(split_points)
            points.append(b_short)

            if i % 2 == 0:
                points = list(reversed(points))

            # zigzag spacing is wider than stitch length, subdivide
            if last_point is not None and max_stitch_length is not None and self.zigzag_spacing > max_stitch_length:
                initial_points, _ = self.get_split_points(last_point, points[0], last_point, points[0], max_stitch_length)

            stitch_group.add_stitches(points)
            last_point = points[-1]

        if self._center_walk_is_odd():
            stitch_group.stitches = list(reversed(stitch_group.stitches))

        stitch_group.add_tags(("satin_column", "s_stitch"))
        return stitch_group

    def do_zigzag(self):
        stitch_group = StitchGroup(color=self.color)

        # calculate pairs at double the requested density
        pairs = self.plot_points_on_rails(
            self.zigzag_spacing / 2.0,
            self.pull_compensation_px,
            self.pull_compensation_percent / 100,
            True,
        )

        # alternate picking one point from each pair, first on one rail then the other
        points = [p[i % 2] for i, p in enumerate(pairs)]

        # turn the list of points back into pairs
        pairs = [points[i:i + 2] for i in range(0, len(points), 2)]

        # remove last item if it isn't paired up
        if len(pairs[-1]) == 1:
            del pairs[-1]

        short_pairs = self.inset_short_stitches_sawtooth(pairs)
        max_stitch_length = self.max_stitch_length_px
        length_sigma = self.random_split_jitter
        random_phase = self.random_split_phase
        min_split_length = self.min_random_split_length_px
        seed = self.random_seed

        last_point = None
        last_point_short = None
        for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
            if last_point:
                split_points, _ = self.get_split_points(
                    last_point, a, last_point_short, a_short, max_stitch_length, None,
                    length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i), row_num=2 * i, from_end=True)
                stitch_group.add_stitches(split_points, ("satin_column", "zigzag_split_stitch"))

            stitch_group.add_stitch(a_short)

            split_points, _ = self.get_split_points(
                a, b, a_short, b_short, max_stitch_length, None,
                length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i + 1), row_num=2 * i + 1)
            stitch_group.add_stitches(split_points, ("satin_column", "zigzag_split_stitch"))

            stitch_group.add_stitch(b_short)

            last_point = b
            last_point_short = b_short

        if self._center_walk_is_odd():
            stitch_group.stitches = list(reversed(stitch_group.stitches))

        return stitch_group

    def get_split_points(self, *args, **kwargs):
        if self.split_method == "default":
            return self._get_split_points_default(*args, **kwargs)
        elif self.split_method == "simple":
            return self._get_split_points_simple(*args, **kwargs), None
        elif self.split_method == "staggered":
            return self._get_split_points_staggered(*args, **kwargs), None

    def _get_split_points_default(self, a, b, a_short, b_short, length, count=None, length_sigma=0.0, random_phase=False, min_split_length=None,
                                  seed=None, row_num=0, from_end=None):
        if not length:
            return ([], None)
        if min_split_length is None:
            min_split_length = length
        distance = a.distance(b)
        if distance <= min_split_length:
            return ([], 1)
        if random_phase:
            points = running_stitch.split_segment_random_phase(a_short, b_short, length, length_sigma, seed)
            # avoid hard stitches: do not insert split stitches near the end points
            if len(points) > 1 and points[0].distance(shgeo.Point(a)) <= self.min_stitch_len:
                del points[0]
            if len(points) > 1 and points[-1].distance(shgeo.Point(b)) <= self.min_stitch_len:
                del points[-1]
            return (points, None)
        elif count is not None:
            points = running_stitch.split_segment_even_n(a, b, count, length_sigma, seed)
            return (points, count)
        else:
            points = running_stitch.split_segment_even_dist(a, b, length, length_sigma, seed)
            return (points, len(points) + 1)

    def _get_split_points_simple(self, *args, **kwargs):
        return self._get_split_points_staggered(*args, **kwargs, _staggers=1)

    def _get_split_points_staggered(self, a, b, a_short, b_short, length, count=None, length_sigma=0.0, random_phase=False, min_split_length=None,
                                    seed=None, row_num=0, from_end=False, _staggers=None):
        if not length or a.distance(b) <= length:
            return []

        if _staggers is None:
            # This is only here to allow _get_split_points_simple to override
            _staggers = self.split_staggers

        if from_end:
            a, b = b, a
            a_short, b_short = b_short, a_short

        line = shgeo.LineString((a, b))
        a_short_projection = line.project(shgeo.Point(a_short))
        b_short_projection = line.project(shgeo.Point(b_short))
        split_points = running_stitch.split_segment_stagger_phase(a, b, length, _staggers, row_num, min=a_short_projection, max=b_short_projection)

        if from_end:
            split_points = list(reversed(split_points))

        return split_points

    def inset_short_stitches_sawtooth(self, pairs):
        max_stitch_length = None if self.random_split_phase else self.max_stitch_length_px
        if not self.short_stitch_distance or not len(self.short_stitch_inset):
            return pairs

        shortened = []
        last_a = None
        last_b = None
        inset_a_index = 0
        inset_b_index = 0
        for a, b in pairs:
            a_offset_px, last_a, inset_a_index = self._get_offset_px(a, b, last_a, inset_a_index, max_stitch_length)
            b_offset_px, last_b, inset_b_index = self._get_offset_px(b, a, last_b, inset_b_index, max_stitch_length)
            shortened.append(offset_points(a, b, [a_offset_px, b_offset_px], (0, 0)))

        return shortened

    def _get_offset_px(self, point, other_point, last_point, inset_index, max_stitch_length):
        if inset_index >= len(self.short_stitch_inset):
            inset_index = 0

        dist = point.distance(other_point)
        inset_px = self.short_stitch_inset[inset_index] * dist
        if self.split_method == "default" and max_stitch_length and not self.random_split_phase:
            # make sure inset is less than split stitch length
            inset_px = min(inset_px, max_stitch_length / 3)

        offset_px = 0
        if last_point is None or point.distance(last_point) >= self.short_stitch_distance:
            last_point = point
            inset_index = 0
        else:
            offset_px = -inset_px
            inset_index += 1

        return offset_px, last_point, inset_index

    def _get_inset_point(self, point1, point2, distance_fraction):
        return point1 * (1 - distance_fraction) + point2 * distance_fraction

    def add_running_stitches(self, start_stitch, end_stitch, stitch_group):
        # When max_stitch_length is set, the satin column may be quite wide and the jumps
        # between underlays or from underlay to final satin should be turned into running stitch
        # to avoid long jumps or unexpected trims.

        if self.max_stitch_length_px:
            max_len = self.max_stitch_length_px
            if end_stitch.distance(start_stitch) > max_len:
                split_points = running_stitch.split_segment_even_dist(start_stitch, end_stitch, max_len)
                stitch_group.add_stitches(split_points)
                stitch_group.add_stitch(end_stitch)

    def connect_and_add(self, stitch_group, next_stitch_group):
        if not next_stitch_group.stitches:
            return stitch_group
        if stitch_group.stitches:
            self.add_running_stitches(stitch_group.stitches[-1], next_stitch_group.stitches[0], stitch_group)
        stitch_group += next_stitch_group
        return stitch_group

    @property
    def first_stitch(self):
        if not self.rails or self.start_at_nearest_point:
            return None
        return shgeo.Point(self.line_string_rails[0].coords[0])

    def start_point(self, last_stitch_group):
        start_point = self._get_command_point('starting_point')
        if start_point is None and self.start_at_nearest_point and last_stitch_group is not None:
            start_point = nearest_points(shgeo.Point(*last_stitch_group.stitches[-1]), self.offset_center_line)[1]
            start_point = Point(*list(start_point.coords[0]))
        return start_point

    def end_point(self, next_stitch):
        end_point = self._get_command_point('ending_point')
        if end_point is None and self.end_at_nearest_point and next_stitch is not None:
            end_point = nearest_points(next_stitch, self.compensated_shape)[1]
            end_point = Point(*list(end_point.coords[0]))
        # if we are already near to the end, we won't need to specify an ending point
        if end_point and shgeo.Point(self.offset_center_line.coords[-1]).distance(shgeo.Point(end_point)) < 5:
            end_point = None
        return end_point

    def uses_previous_stitch(self):
        if not self.start_at_nearest_point or self.get_command('starting_point'):
            return False
        else:
            return True

    def uses_next_element(self):
        if not self.end_at_nearest_point or self.get_command('ending_point'):
            return False
        else:
            return True

    def _get_command_point(self, command):
        point = self.get_command(command)
        if point is not None:
            point = point.target_point
        return point

    def _sort_stitch_groups(self, stitch_groups, end_point):
        if end_point:
            ordered_stitch_groups = []
            ordered_stitch_groups.extend(stitch_groups[::2])
            ordered_stitch_groups.append(self._connect_stitch_group_with_point(stitch_groups[1], ordered_stitch_groups[-1].stitches[-1], end_point))
            ordered_stitch_groups.extend(stitch_groups[1::2])
            return ordered_stitch_groups
        return stitch_groups

    def to_stitch_groups(self, last_stitch_group=None, next_element=None):
        # Stitch a variable-width satin column, zig-zagging between two paths.
        # The algorithm will draw zigzags between each consecutive pair of
        # beziers.  The boundary points between beziers serve as "checkpoints",
        # allowing the user to control how the zigzags flow around corners.

        start_point = self.start_point(last_stitch_group)
        end_point = self.end_point(self.next_stitch(next_element))
        stitch_groups = []

        # underlays
        stitch_groups.extend(self._do_underlay_stitch_groups(end_point))

        # top layer
        top_layer_group = self._do_top_layer_stitch_group()
        if end_point:
            stitch_groups.extend(self._split_top_layer(top_layer_group, end_point))
        else:
            stitch_groups.append(top_layer_group)

        # order stitch groups
        stitch_groups = self._sort_stitch_groups(stitch_groups, end_point)

        # start and end
        if start_point is not None:
            stitch_groups = [self._connect_stitch_group_with_point(stitch_groups[0], start_point)] + stitch_groups
        if end_point:
            stitch_groups.append(self.do_end_path(end_point))
            pass

        # assemble stitch groups
        stitch_group = StitchGroup(
            color=self.color,
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches
        )

        for satin_layer in stitch_groups:
            if satin_layer and satin_layer.stitches:
                stitch_group = self.connect_and_add(stitch_group, satin_layer)

        if not stitch_group.stitches:
            return []

        return [stitch_group]


class SatinProcessor:
    def __init__(self, satin, offset_px, offset_proportional, use_random):
        self.satin = satin
        self.use_random = use_random
        self.offset_px = offset_px
        self.offset_proportional = offset_proportional
        self.random_zigzag_spacing = satin.random_zigzag_spacing

        if use_random:
            self.seed = prng.join_args(satin.random_seed, "satin-points")
            self.offset_proportional_min = np.array(offset_proportional) - satin.random_width_decrease
            self.offset_range = (satin.random_width_increase + satin.random_width_decrease)
            self.cycle = 0

    def process_points(self, pos0, pos1):
        if self.use_random:
            roll = prng.uniform_floats(self.seed, self.cycle)
            self.cycle += 1
            offset_prop = self.offset_proportional_min + roll[0:2] * self.offset_range
        else:
            offset_prop = self.offset_proportional

        a, b = offset_points(pos0, pos1, self.offset_px, offset_prop)
        return a, b

    def get_stitch_spacing_multiple(self):
        if self.use_random:
            roll = prng.uniform_floats(self.seed, self.cycle)
            self.cycle += 1
            return max(1.0 + ((roll[0] - 0.5) * 2) * self.random_zigzag_spacing, 0.01)
        else:
            return 1.0
