# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
import re

import numpy as np
from inkex import Color, ColorError, LinearGradient
from shapely import geometry as shgeo
from shapely import set_precision
from shapely.errors import GEOSException
from shapely.ops import nearest_points
from shapely.validation import explain_validity, make_valid

from .. import tiles
from ..i18n import _
from ..marker import get_marker_elements
from ..stitch_plan import StitchGroup
from ..stitches import (auto_fill, circular_fill, contour_fill, guided_fill,
                        legacy_fill, linear_gradient_fill, meander_fill,
                        tartan_fill)
from ..stitches.linear_gradient_fill import gradient_angle
from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSCAPE_LABEL
from ..tartan.utils import get_tartan_settings, get_tartan_stripes
from ..utils import cache
from ..utils.geometry import ensure_multi_polygon
from ..utils.param import ParamOption
from .element import EmbroideryElement, param
from .validation import ValidationError, ValidationWarning


class SmallShapeWarning(ValidationWarning):
    name = _("Small Fill")
    description = _("This fill object is so small that it would probably look better as running stitch or satin column. "
                    "For very small shapes, fill stitch is not possible, and Ink/Stitch will use running stitch around "
                    "the outline instead.")


class ExpandWarning(ValidationWarning):
    name = _("Expand")
    description = _("The expand parameter for this fill object cannot be applied. "
                    "Ink/Stitch will ignore it and will use original size instead.")


class UnderlayInsetWarning(ValidationWarning):
    name = _("Inset")
    description = _("The underlay inset parameter for this fill object cannot be applied. "
                    "Ink/Stitch will ignore it and will use the original size instead.")


class MissingGuideLineWarning(ValidationWarning):
    name = _("Missing Guideline")
    description = _('This object is set to "Guided Fill", but has no guide line.')
    steps_to_solve = [
        _('* Create a stroke object'),
        _('* Select this object and run Extensions > Ink/Stitch > Edit > Selection to guide line')
    ]


class DisjointGuideLineWarning(ValidationWarning):
    name = _("Disjointed Guide Line")
    description = _("The guide line of this object isn't within the object borders. "
                    "The guide line works best, if it is within the target element.")
    steps_to_solve = [
        _('* Move the guide line into the element')
    ]


class MultipleGuideLineWarning(ValidationWarning):
    name = _("Multiple Guide Lines")
    description = _("This object has multiple guide lines, but only the first one will be used.")
    steps_to_solve = [
        _("* Remove all guide lines, except for one.")
    ]


class UnconnectedWarning(ValidationWarning):
    name = _("Unconnected")
    description = _("Fill: This object is made up of unconnected shapes. "
                    "Ink/Stitch doesn't know what order to stitch them in.  Please break this "
                    "object up into separate shapes.")
    steps_to_solve = [
        _('* Extensions > Ink/Stitch > Fill Tools > Break Apart Fill Objects'),
    ]


class BorderCrossWarning(ValidationWarning):
    name = _("Border crosses itself")
    description = _("Fill: The border crosses over itself. This may lead into unconnected shapes. "
                    "Please break this object into separate shapes to indicate in which order it should be stitched in.")
    steps_to_solve = [
        _('* Extensions > Ink/Stitch > Fill Tools > Break Apart Fill Objects')
    ]


class StrokeAndFillWarning(ValidationWarning):
    name = _("Fill and Stroke color")
    description = _("Element has both a fill and a stroke color. It is recommended to use two separate elements instead.")
    steps_to_solve = [
        _('* Duplicate the element. Remove stroke color from the first and fill color from the second.'),
        _('* Adapt the shape of the second element to compensate for push and pull fabric distortion.')
    ]


class NoGradientWarning(ValidationWarning):
    name = _("No linear gradient color")
    description = _("Linear Gradient has no linear gradient color.")
    steps_to_solve = [
        _('* Open the Fill and Stroke dialog.'),
        _('* Set a linear gradient as a fill and adapt colors to your liking.')
    ]


class NoTartanStripeWarning(ValidationWarning):
    name = _("No stripes to render")
    description = _("Tartan fill: There is no active fill stripe to render")
    steps_to_solve = [
        _('Go to Extensions > Ink/Stitch > Fill Tools > Tartan and adjust stripe settings:'),
        _('* Check if stripes are active'),
        _('* Check the minimum stripe width setting and the scale factor')
    ]


class DefaultTartanStripeWarning(ValidationWarning):
    name = _("No customized pattern")
    description = _("Tartan fill: Using default pattern")
    steps_to_solve = [
        _('Go to Extensions > Ink/Stitch > Fill Tools > Tartan and adjust stripe settings:'),
        _('* Customize your pattern')
    ]


class InvalidShapeError(ValidationError):
    name = _("This shape is invalid")
    description = _('Fill: This shape cannot be stitched out. Please try to repair it with the "Break Apart Fill Objects" extension.')
    steps_to_solve = [
        _('* Extensions > Ink/Stitch > Fill Tools > Break Apart Fill Objects')
    ]


class FillStitch(EmbroideryElement):
    name = "FillStitch"
    element_name = _("FillStitch")

    @property
    @param('auto_fill', _('Automatically routed fill stitching'), type='toggle', default=True, sort_index=1)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    _fill_methods = [ParamOption('auto_fill', _("Auto Fill")),
                     ParamOption('circular_fill', _("Circular Fill")),
                     ParamOption('contour_fill', _("Contour Fill")),
                     ParamOption('guided_fill', _("Guided Fill")),
                     ParamOption('linear_gradient_fill', _("Linear Gradient Fill")),
                     ParamOption('meander_fill', _("Meander Fill")),
                     ParamOption('tartan_fill', _("Tartan Fill")),
                     ParamOption('legacy_fill', _("Legacy Fill"))]

    @property
    @param('fill_method',
           _('Fill method'),
           type='combo',
           default=0,
           options=_fill_methods,
           sort_index=2)
    def fill_method(self):
        return self.get_param('fill_method', 'auto_fill')

    @property
    @param('guided_fill_strategy', _('Guided Fill Strategy'), type='dropdown', default=0,
           options=[_("Copy"), _("Parallel Offset")], select_items=[('fill_method', 'guided_fill')], sort_index=10,
           tooltip=_('Copy (the default) will fill the shape with shifted copies of the line. '
                     'Parallel offset will ensure that each line is always a consistent distance from its neighbor. '
                     'Sharp corners may be introduced.'))
    def guided_fill_strategy(self):
        return self.get_int_param('guided_fill_strategy', 0)

    @property
    @param('contour_strategy', _('Contour Fill Strategy'), type='dropdown', default=0,
           options=[_("Inner to Outer"), _("Single spiral"), _("Double spiral")], select_items=[('fill_method', 'contour_fill')], sort_index=10)
    def contour_strategy(self):
        return self.get_int_param('contour_strategy', 0)

    @property
    @param('join_style', _('Join Style'), type='dropdown', default=0,
           options=[_("Round"), _("Mitered"), _("Beveled")], select_items=[('fill_method', 'contour_fill')], sort_index=11)
    def join_style(self):
        return self.get_int_param('join_style', 0)

    @property
    @param('avoid_self_crossing',
           _('Avoid self-crossing'),
           type='boolean',
           default=False,
           select_items=[('fill_method', 'contour_fill')],
           sort_index=12)
    def avoid_self_crossing(self):
        return self.get_boolean_param('avoid_self_crossing', False)

    @property
    @param('clockwise', _('Clockwise'), type='boolean', default=True, select_items=[('fill_method', 'contour_fill')], sort_index=13)
    def clockwise(self):
        return self.get_boolean_param('clockwise', True)

    @property
    @param('meander_pattern', _('Meander Pattern'), type='combo', default=0,
           options=sorted(tiles.all_tiles()), select_items=[('fill_method', 'meander_fill')], sort_index=10)
    def meander_pattern(self):
        return self.get_param('meander_pattern', min(tiles.all_tiles()).id)

    @property
    @param('meander_angle',
           _('Meander pattern angle'),
           type='float', unit="degrees",
           default=0,
           select_items=[('fill_method', 'meander_fill')],
           sort_index=11)
    def meander_angle(self):
        return math.radians(self.get_float_param('meander_angle', 0))

    @property
    @param('meander_scale_percent',
           _('Meander pattern scale'),
           tooltip=_("Percentage to stretch or compress the meander pattern.  You can scale horizontally " +
                     "and vertically individually by giving two percentages separated by a space. "),
           type='float', unit="%",
           default=100,
           select_items=[('fill_method', 'meander_fill')],
           sort_index=12)
    def meander_scale(self):
        return np.maximum(self.get_split_float_param('meander_scale_percent', (100, 100)), (1, 1)) / 100

    @property
    @param('clip', _('Clip path'),
           tooltip=_('Constrain stitching to the shape.  Useful when smoothing and expand are used.'),
           type='boolean',
           default=False,
           select_items=[('fill_method', 'meander_fill')],
           sort_index=13)
    def clip(self):
        return self.get_boolean_param('clip', False)

    @property
    @param('smoothness_mm', _('Smoothness'),
           tooltip=_(
               'Smooth the stitch path.  Smoothness limits how far the smoothed stitch path ' +
               'is allowed to deviate from the original path.  Try low numbers like 0.2.  ' +
               'Hint: a lower running stitch tolerance may be needed too.'
           ),
           type='integer',
           unit='mm',
           default=0,
           select_items=[('fill_method', 'contour_fill'), ('fill_method', 'meander_fill')],
           sort_index=14)
    def smoothness(self):
        return self.get_float_param('smoothness_mm', 0)

    @property
    @param('expand_mm',
           _('Expand'),
           tooltip=_('Expand the shape before fill stitching, to compensate for gaps between shapes.  Negative values contract instead.'),
           unit='mm',
           type='float',
           default=0,
           sort_index=20,
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'meander_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'tartan_fill'),
                         ('fill_method', 'linear_gradient_fill')])
    def expand(self):
        return self.get_float_param('expand_mm', 0)

    @property
    @param('gap_fill_rows',
           _('Gap Filling'),
           tooltip=_('Add extra rows to compensate for gaps between sections caused by distortion.'
                     'Rows are always added in pairs, so this number will be rounded up to the nearest multiple of 2.'),
           unit='rows',
           type='int',
           default=0,
           sort_index=21,
           select_items=[('fill_method', 'auto_fill')])
    def gap_fill_rows(self):
        return self.get_int_param('gap_fill_rows', 0)

    @property
    @param('angle',
           _('Angle of lines of stitches'),
           tooltip=_('The angle increases in a counter-clockwise direction.  0 is horizontal.  Negative angles are allowed.'),
           unit='deg',
           type='float',
           sort_index=21,
           select_items=[('fill_method', 'auto_fill'), ('fill_method', 'legacy_fill')],
           default=0)
    @cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    @param('tartan_angle',
           _('Angle of lines of stitches'),
           tooltip=_('Relative to the tartan stripe direction.'),
           unit='deg',
           type='float',
           sort_index=21,
           select_items=[('fill_method', 'tartan_fill')],
           default=-45)
    @cache
    def tartan_angle(self):
        return self.get_float_param('tartan_angle', -45)

    @property
    @param('max_stitch_length_mm',
           _('Maximum fill stitch length'),
           tooltip=_(
               'The length of each stitch in a row.  Shorter stitch may be used at the start or end of a row.'),
           unit='mm',
           sort_index=22,
           type='float',
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'linear_gradient_fill'),
                         ('fill_method', 'tartan_fill'),
                         ('fill_method', 'legacy_fill')],
           default=3.0)
    def max_stitch_length(self):
        return max(self.get_float_param("max_stitch_length_mm", 3.0), 0.1 * PIXELS_PER_MM)

    @property
    @param('row_spacing_mm',
           _('Spacing between rows'),
           tooltip=_('Distance between rows of stitches.'),
           unit='mm',
           sort_index=23,
           type='float',
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'linear_gradient_fill'),
                         ('fill_method', 'tartan_fill'),
                         ('fill_method', 'legacy_fill')],
           default=0.25)
    def row_spacing(self):
        return max(self.get_float_param("row_spacing_mm", 0.25), 0.1 * PIXELS_PER_MM)

    @property
    @param('end_row_spacing_mm',
           _('End row spacing'),
           tooltip=_('Increases or decreases the row spacing towards the end.'),
           unit='mm',
           sort_index=24,
           type='float',
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'legacy_fill')],
           default=None)
    def end_row_spacing(self):
        end_row_spacing = self.get_float_param("end_row_spacing_mm")
        return max(end_row_spacing, 0) if end_row_spacing else None

    @property
    @param('staggers',
           _('Stagger rows this many times before repeating'),
           tooltip=_('Length of the cycle by which successive stitch rows are staggered. '
                     'Fractional values are allowed and can have less visible diagonals than integer values.'),
           type='int',
           sort_index=25,
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'linear_gradient_fill'),
                         ('fill_method', 'tartan_fill'),
                         ('fill_method', 'legacy_fill')],
           default=4)
    def staggers(self):
        return self.get_float_param("staggers", 4)

    @property
    @param(
        'skip_last',
        _('Skip last stitch in each row'),
        tooltip=_('The last stitch in each row is quite close to the first stitch in the next row.  '
                  'Skipping it decreases stitch count and density.'),
        type='boolean',
        sort_index=30,
        select_items=[('fill_method', 'auto_fill'),
                      ('fill_method', 'guided_fill'),
                      ('fill_method', 'linear_gradient_fill'),
                      ('fill_method', 'legacy_fill')],
        default=False)
    def skip_last(self):
        return self.get_boolean_param("skip_last", False)

    @property
    @param(
        'flip',
        _('Flip fill (start right-to-left)'),
        tooltip=_('The flip option can help you with routing your stitch path.  '
                  'When you enable flip, stitching goes from right-to-left instead of left-to-right.'),
        type='boolean',
        sort_index=31,
        select_items=[('fill_method', 'legacy_fill')],
        default=False)
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param(
        'reverse',
        _('Reverse fill'),
        tooltip=_('Reverses fill path.'),
        type='boolean',
        sort_index=32,
        select_items=[('fill_method', 'legacy_fill')],
        default=False)
    def reverse(self):
        return self.get_boolean_param("reverse", False)

    @property
    @param(
        'stop_at_ending_point',
        _('Stop at ending point'),
        tooltip=_('If this option is disabled, the ending point will only be used to define a general direction for '
                  'stitch routing. When enabled the last section will end at the defined spot.'),
        type='boolean',
        sort_index=33,
        select_items=[('fill_method', 'linear_gradient_fill'), ('fill_method', 'tartan_fill')],
        default=False
     )
    def stop_at_ending_point(self):
        return self.get_boolean_param("stop_at_ending_point", False)

    @property
    @param('underpath',
           _('Underpath'),
           tooltip=_('Travel inside the shape when moving from section to section.  Underpath '
                     'stitches avoid traveling in the direction of the row angle so that they '
                     'are not visible.  This gives them a jagged appearance.'),
           type='boolean',
           default=True,
           select_items=[('fill_method', 'auto_fill'), ('fill_method', 'guided_fill'), ('fill_method', 'circular_fill')],
           sort_index=40)
    def underpath(self):
        return self.get_boolean_param('underpath', True)

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches around the outline of the fill region used when moving from section to section. '
                     'Also used for meander and circular fill.'),
           unit='mm',
           type='float',
           default=2.5,
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'meander_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'linear_gradient_fill'),
                         ('fill_method', 'tartan_fill')],
           sort_index=41)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 2.5), 0.01)

    @property
    @param('running_stitch_tolerance_mm',
           _('Running stitch tolerance'),
           tooltip=_('Determines how hard Ink/Stitch tries to avoid stitching outside the shape.' +
                     'Lower numbers are less likely to stitch outside the shape but require more stitches.'),
           unit='mm',
           type='float',
           default=0.1,
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'meander_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'linear_gradient_fill'),
                         ('fill_method', 'tartan_fill')],
           sort_index=43)
    def running_stitch_tolerance(self):
        return max(self.get_float_param("running_stitch_tolerance_mm", 0.2), 0.01)

    @property
    @param('enable_random_stitch_length',
           _('Randomize stitch length'),
           tooltip=_('Randomize stitch length and phase instead of dividing evenly or staggering. '
                     'This is recommended for closely-spaced curved fills to avoid Moiré artefacts.'),
           type='boolean',
           enables=['random_stitch_length_jitter_percent'],
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'linear_gradient_fill'),],
           default=False,
           sort_index=44)
    def enable_random_stitch_length(self):
        return self.get_boolean_param('enable_random_stitch_length', False)

    @property
    @param('random_stitch_length_jitter_percent',
           _('Random stitch length jitter'),
           tooltip=_('Amount to vary the length of each stitch by when randomizing.'),
           unit='± %',
           type='float',
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'linear_gradient_fill'),],
           default=10,
           sort_index=46)
    def random_stitch_length_jitter(self):
        return max(self.get_float_param("random_stitch_length_jitter_percent", 10), 0.0) / 100.0

    @property
    @param('repeats',
           _('Repeats'),
           tooltip=_('Defines how many times to run down and back along the path.'),
           type='int',
           default="1",
           select_items=[('fill_method', 'meander_fill'),
                         ('fill_method', 'circular_fill')],
           sort_index=50)
    def repeats(self):
        return max(1, self.get_int_param("repeats", 1))

    @property
    @param('bean_stitch_repeats',
           _('Bean stitch number of repeats'),
           tooltip=_('Backtrack each stitch this many times.  '
                     'A value of 1 would triple each stitch (forward, back, forward).  '
                     'A value of 2 would quintuple each stitch, etc.\n\n'
                     'A pattern with various repeats can be created with a list of values separated by a space.'),
           type='str',
           select_items=[('fill_method', 'meander_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'tartan_fill')],
           default=0,
           sort_index=51)
    def bean_stitch_repeats(self):
        return self.get_multiple_int_param("bean_stitch_repeats", "0")

    @property
    @param('zigzag_spacing_mm',
           _('Zig-zag spacing (peak-to-peak)'),
           tooltip=_('Length of stitches in zig-zag mode.'),
           unit='mm',
           type='float',
           select_items=[('fill_method', 'meander_fill')],
           default=0,
           sort_index=60)
    @cache
    def zigzag_spacing(self):
        return self.get_float_param("zigzag_spacing_mm", 0)

    @property
    @param('zigzag_width_mm',
           _('Zig-zag width'),
           tooltip=_('Width of the zig-zag line.'),
           unit='mm',
           type='float',
           select_items=[('fill_method', 'meander_fill')],
           default=3,
           sort_index=61)
    @cache
    def zigzag_width(self):
        return self.get_float_param("zigzag_width_mm", 3)

    @property
    @param(
        'rows_per_thread',
        _("Rows per tartan thread"),
        tooltip=_("Consecutive rows of the same color"),
        type='int',
        default="2",
        select_items=[('fill_method', 'tartan_fill')],
        sort_index=62
    )
    def rows_per_thread(self):
        return max(1, self.get_int_param("rows_per_thread", 2))

    @property
    @param('herringbone_width_mm',
           _('Herringbone width'),
           tooltip=_('Defines width of a herringbone pattern. Use 0 for regular rows.'),
           unit='mm',
           type='int',
           default=0,
           select_items=[('fill_method', 'tartan_fill')],
           sort_index=63)
    def herringbone_width(self):
        return self.get_float_param('herringbone_width_mm', 0)

    @property
    @param(
        'pull_compensation_mm',
        _('Pull compensation'),
        tooltip=_('Fill stitch can pull the fabric together, resulting in a shape narrower than you draw in Inkscape. '
                  'This setting expands each row of stitches outward from the center of the row by a fixed length. '
                  'Two values separated by a space may be used for an asymmetric effect.'),
        select_items=[('fill_method', 'auto_fill')],
        unit=_('mm (each side)'),
        type='float',
        default=0,
        sort_index=26)
    @cache
    def pull_compensation_px(self):
        return np.maximum(self.get_split_mm_param_as_px("pull_compensation_mm", (0, 0)), 0)

    @property
    @param(
        'pull_compensation_percent',
        _('Pull compensation percentage'),
        tooltip=_('Additional pull compensation which varies as a percentage of row width. '
                  'Two values separated by a space may be used for an asymmetric effect.'),
        select_items=[('fill_method', 'auto_fill')],
        unit=_('% (each side)'),
        type='float',
        default=0,
        sort_index=27)
    @cache
    def pull_compensation_percent(self):
        return np.maximum(self.get_split_float_param("pull_compensation_percent", (0, 0)), 0)

    @property
    def color(self):
        return self.fill_color

    @property
    def gradient(self):
        if isinstance(self.fill_color, LinearGradient):
            return self.fill_color
        return None

    @property
    @param('fill_underlay', _('Underlay'), type='toggle', group=_('Fill Underlay'), default=True)
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay", default=True)

    @property
    @param('fill_underlay_angle',
           _('Fill angle'),
           tooltip=_('Default: fill angle + 90 deg. Insert a list for multiple layers separated by a space.'),
           unit='deg',
           group=_('Fill Underlay'),
           type='float')
    @cache
    def fill_underlay_angle(self):
        underlay_angles = self.get_param('fill_underlay_angle', None)
        default_value = [self.angle + math.pi / 2.0]
        if underlay_angles is not None:
            underlay_angles = underlay_angles.strip().split(' ')
            # remove comma separator for backward compatibility
            underlay_angles = [angle[:-1] if angle.endswith(',') else angle for angle in underlay_angles]
            try:
                underlay_angles = [math.radians(
                    float(angle)) for angle in underlay_angles]
            except (TypeError, ValueError):
                return default_value
        elif self.fill_method == 'linear_gradient_fill' and self.gradient is not None:
            return [-gradient_angle(self.node, self.gradient)]
        else:
            underlay_angles = default_value

        return underlay_angles

    @property
    @param('fill_underlay_row_spacing_mm',
           _('Row spacing'),
           tooltip=_('default: 3x fill row spacing'),
           unit='mm',
           group=_('Fill Underlay'),
           type='float')
    @cache
    def fill_underlay_row_spacing(self):
        return self.get_float_param("fill_underlay_row_spacing_mm") or self.row_spacing * 3

    @property
    @param('fill_underlay_max_stitch_length_mm',
           _('Max stitch length'),
           tooltip=_('default: equal to fill max stitch length'),
           unit='mm',
           group=_('Fill Underlay'), type='float')
    @cache
    def fill_underlay_max_stitch_length(self):
        return self.get_float_param("fill_underlay_max_stitch_length_mm") or self.max_stitch_length

    @property
    @param('fill_underlay_inset_mm',
           _('Inset'),
           tooltip=_('Shrink the shape before doing underlay, to prevent underlay from showing around the outside of the fill.'),
           unit='mm',
           group=_('Fill Underlay'),
           type='float',
           default=0)
    def fill_underlay_inset(self):
        return self.get_float_param('fill_underlay_inset_mm', 0)

    @property
    @param(
        'fill_underlay_skip_last',
        _('Skip last stitch in each row'),
        tooltip=_('The last stitch in each row is quite close to the first stitch in the next row.  '
                  'Skipping it decreases stitch count and density.'),
        group=_('Fill Underlay'),
        type='boolean',
        default=False)
    def fill_underlay_skip_last(self):
        return self.get_boolean_param("fill_underlay_skip_last", False)

    @property
    @param(
        'underlay_underpath',
        _('Underpath'),
        tooltip=_('Travel inside the shape when moving from section to section.  Underpath '
                  'stitches avoid traveling in the direction of the row angle so that they '
                  'are not visible.  This gives them a jagged appearance.'),
        group=_('Fill Underlay'),
        type='boolean',
        default=True)
    def underlay_underpath(self):
        return self.get_boolean_param('underlay_underpath', True)

    @property
    @param('random_seed',
           _('Random seed'),
           tooltip=_('Use a specific seed for randomized attributes. Uses the element ID if empty.'),
           select_items=[('fill_method', 'auto_fill'),
                         ('fill_method', 'contour_fill'),
                         ('fill_method', 'guided_fill'),
                         ('fill_method', 'circular_fill'),
                         ('fill_method', 'meander_fill'),
                         ('fill_method', 'linear_gradient_fill')],
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
    def paths(self):
        paths = self.flatten(self.parse_path())
        # ensure path length
        for i, path in enumerate(paths):
            if len(path) < 3:
                paths[i] = [(path[0][0], path[0][1]), (path[0][0] + 1.0, path[0][1]), (path[0][0], path[0][1] + 1.0)]
        return paths

    @property
    @cache
    def original_shape(self):
        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        paths = self.paths
        paths.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)
        shape = shgeo.MultiPolygon([(paths[0], paths[1:])])
        return shape

    @property
    @cache
    def shape(self):
        shape = self._get_clipped_path()

        if shape.is_valid:
            # set_precision to avoid FloatingPointErrors
            return ensure_multi_polygon(set_precision(shape, 0.0000000001), 3)

        shape = make_valid(shape)

        return ensure_multi_polygon(set_precision(shape, 0.00000000001), 3)

    def _get_clipped_path(self):
        if self.clip_shape is None:
            return self.original_shape

        # make sure clip path and shape are valid
        clip_path = make_valid(self.clip_shape)
        shape = make_valid(self.original_shape)

        try:
            intersection = clip_path.intersection(shape)
        except GEOSException:
            return self.original_shape

        return intersection

    def validation_errors(self):
        if not self.shape.is_valid:
            why = explain_validity(self.shape)
            match = re.match(r"(?P<message>.+)\[(?P<x>.+)\s(?P<y>.+)\]", why)
            assert match is not None, f"Could not parse validity message '{why}'"
            message, x, y = match.groups()
            yield InvalidShapeError((x, y))

    def validation_warnings(self):  # noqa: C901
        if not self.original_shape.is_valid:
            why = explain_validity(self.original_shape)
            match = re.match(r"(?P<message>.+)\[(?P<x>.+)\s(?P<y>.+)\]", why)
            assert match is not None, f"Could not parse validity message '{why}'"
            message, x, y = match.groups()
            if "Hole lies outside shell" in message:
                yield UnconnectedWarning((x, y))
            else:
                yield BorderCrossWarning((x, y))

        for shape in self.shape.geoms:
            if self.shape.area < 20:
                label = self.node.get(INKSCAPE_LABEL) or self.node.get("id")
                yield SmallShapeWarning(shape.centroid, label)

            if self.shrink_or_grow_shape(shape, self.expand, True).is_empty:
                yield ExpandWarning(shape.centroid)

            if self.shrink_or_grow_shape(shape, -self.fill_underlay_inset, True).is_empty:
                yield UnderlayInsetWarning(shape.centroid)

        # guided fill warnings
        if self.fill_method == 'guided_fill':
            guide_lines = self._get_guide_lines(True)
            if not guide_lines or guide_lines[0].is_empty:
                yield MissingGuideLineWarning(self.shape.centroid)
            elif len(guide_lines) > 1:
                yield MultipleGuideLineWarning(self.shape.centroid)
            elif guide_lines[0].disjoint(self.shape):
                yield DisjointGuideLineWarning(self.shape.centroid)
            return None

        # linear gradient fill
        if self.fill_method == 'linear_gradient_fill' and self.gradient is None:
            yield NoGradientWarning(self.shape.representative_point())

        if self.node.style('stroke', None) is not None:
            if not self.shape.is_empty:
                yield StrokeAndFillWarning(self.shape.representative_point())
            else:
                # they may used a fill on a straight line
                yield StrokeAndFillWarning(self.paths[0][0])

        # tartan fill
        if self.fill_method == 'tartan_fill':
            settings = get_tartan_settings(self.node)
            warp, weft = get_tartan_stripes(settings)
            if not (warp or weft):
                yield NoTartanStripeWarning(self.shape.representative_point())
            if not self.node.get('inkstitch:tartan', ''):
                yield DefaultTartanStripeWarning(self.shape.representative_point())

        for warning in super(FillStitch, self).validation_warnings():
            yield warning

    @property
    @cache
    def outline(self):
        return self.shape.boundary[0]

    @property
    @cache
    def outline_length(self):
        return self.outline.length

    def shrink_or_grow_shape(self, shape, amount, validate=False):
        new_shape = shape
        if amount:
            new_shape = shape.buffer(amount)
            # changing the size can empty the shape
            # in this case we want to use the original shape rather than returning an error
            if (new_shape.is_empty and not validate):
                new_shape = shape

        if not isinstance(new_shape, shgeo.MultiPolygon):
            new_shape = shgeo.MultiPolygon([new_shape])

        return new_shape

    def underlay_shape(self, shape):
        return self.shrink_or_grow_shape(shape, -self.fill_underlay_inset)

    def fill_shape(self, shape):
        return self.shrink_or_grow_shape(shape, self.expand)

    @property
    def first_stitch(self):
        # Serves as a reverence point for the end point of the previous element
        if self.get_command('starting_point'):
            return shgeo.Point(*self.get_command('starting_point').target_point)
        return None

    def get_starting_point(self, previous_stitch_group):
        # If there is a "starting_point" Command, then use that; otherwise pick
        # the point closest to the end of the last stitch_group.

        if self.get_command('starting_point'):
            return self.get_command('starting_point').target_point
        elif previous_stitch_group:
            return previous_stitch_group.stitches[-1]
        else:
            return None

    def get_ending_point(self, next_stitch):
        if self.get_command('ending_point'):
            return self.get_command('ending_point').target_point
        elif next_stitch:
            return next_stitch.coords
        else:
            return None

    def uses_previous_stitch(self):
        if self.get_command('starting_point'):
            return False
        else:
            return True

    def uses_next_element(self):
        if self.get_command('ending_point'):
            return False
        else:
            return True

    def to_stitch_groups(self, previous_stitch_group, next_element=None):  # noqa: C901
        # backwards compatibility: legacy_fill used to be inkstitch:auto_fill == False
        if not self.auto_fill or self.fill_method == 'legacy_fill':
            return self.do_legacy_fill()
        else:
            stitch_groups = []

            # start and end points
            start = self.get_starting_point(previous_stitch_group)
            final_end = self.get_ending_point(self.next_stitch(next_element))

            # sort shapes to get a nicer routing
            shapes = list(self.shape.geoms)
            if start:
                shapes.sort(key=lambda shape: shape.distance(shgeo.Point(start)))
            else:
                shapes.sort(key=lambda shape: shape.bounds[0])

            for i, shape in enumerate(shapes):
                start = self.get_starting_point(previous_stitch_group)
                if i < len(shapes) - 1:
                    end = nearest_points(shape, shapes[i+1])[0].coords
                else:
                    end = final_end

                if self.fill_underlay:
                    underlay_shapes = self.underlay_shape(shape)
                    for underlay_shape in underlay_shapes.geoms:
                        underlay_stitch_groups, start = self.do_underlay(underlay_shape, start)
                        stitch_groups.extend(underlay_stitch_groups)

                fill_shapes = self.fill_shape(shape)
                for i, fill_shape in enumerate(fill_shapes.geoms):
                    if self.fill_method == 'contour_fill':
                        stitch_groups.extend(self.do_contour_fill(fill_shape, start))
                    elif self.fill_method == 'guided_fill':
                        stitch_groups.extend(self.do_guided_fill(fill_shape, start, end))
                    elif self.fill_method == 'meander_fill':
                        stitch_groups.extend(self.do_meander_fill(fill_shape, shape, i, start, end))
                    elif self.fill_method == 'circular_fill':
                        stitch_groups.extend(self.do_circular_fill(fill_shape, start, end))
                    elif self.fill_method == 'linear_gradient_fill':
                        stitch_groups.extend(self.do_linear_gradient_fill(fill_shape, start, end))
                    elif self.fill_method == 'tartan_fill':
                        stitch_groups.extend(self.do_tartan_fill(fill_shape, start, end))
                    else:
                        # auto_fill
                        stitch_groups.extend(self.do_auto_fill(fill_shape, start, end))
                    if stitch_groups:
                        previous_stitch_group = stitch_groups[-1]

            # sort colors of linear gradient
            if len(shapes) > 1 and self.fill_method == 'linear_gradient_fill':
                self.color_sort(stitch_groups)

            # sort colors of tartan fill
            if len(shapes) > 1 and self.fill_method == 'tartan_fill':
                # while color sorting make sure stroke lines go still on top of the fills
                fill_groups = []
                stroke_groups = []
                for stitch_group in stitch_groups:
                    if "tartan_run" in stitch_group.stitches[0].tags:
                        stroke_groups.append(stitch_group)
                    else:
                        fill_groups.append(stitch_group)
                self.color_sort(fill_groups)
                self.color_sort(stroke_groups)
                stitch_groups = fill_groups + stroke_groups

            return stitch_groups

    def color_sort(self, stitch_groups):
        colors = [stitch_group.color for stitch_group in stitch_groups]
        stitch_groups.sort(key=lambda group: colors.index(group.color))

    def do_legacy_fill(self):
        stitch_lists = legacy_fill(
            self.shape,
            self.angle,
            self.row_spacing,
            self.end_row_spacing,
            self.max_stitch_length,
            self.flip,
            self.reverse,
            self.staggers,
            self.skip_last
        )

        return [StitchGroup(
            stitches=stitch_list,
            color=self.color,
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches
        ) for stitch_list in stitch_lists]

    def do_underlay(self, shape, starting_point):
        color = self.color
        if self.gradient is not None and self.fill_method == 'linear_gradient_fill':
            try:
                color = self.gradient.stops[0].get_computed_style('stop-color')
            except ColorError:
                color = Color('black')

        stitch_groups = []
        for i in range(len(self.fill_underlay_angle)):
            underlay = StitchGroup(
                color=color,
                tags=("auto_fill", "auto_fill_underlay"),
                lock_stitches=self.lock_stitches,
                stitches=auto_fill(
                    shape,
                    self.fill_underlay_angle[i],
                    self.fill_underlay_row_spacing,
                    self.fill_underlay_row_spacing,
                    self.fill_underlay_max_stitch_length,
                    self.running_stitch_length,
                    self.running_stitch_tolerance,
                    self.staggers,
                    self.fill_underlay_skip_last,
                    starting_point,
                    underpath=self.underlay_underpath
                )
            )
            stitch_groups.append(underlay)
            starting_point = underlay.stitches[-1]
        return [stitch_groups, starting_point]

    def do_auto_fill(self, shape, starting_point, ending_point):
        stitch_group = StitchGroup(
            color=self.color,
            tags=("auto_fill", "auto_fill_top"),
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches,
            stitches=auto_fill(
                shape,
                self.angle,
                self.row_spacing,
                self.end_row_spacing,
                self.max_stitch_length,
                self.running_stitch_length,
                self.running_stitch_tolerance,
                self.staggers,
                self.skip_last,
                starting_point,
                ending_point,
                self.underpath,
                self.gap_fill_rows,
                self.enable_random_stitch_length,
                self.random_stitch_length_jitter,
                self.random_seed,
                self.pull_compensation_px,
                self.pull_compensation_percent / 100,
            )
        )
        return [stitch_group]

    def do_contour_fill(self, polygon, starting_point):
        if not starting_point:
            starting_point = (0, 0)
        starting_point = shgeo.Point(starting_point)

        stitch_groups = []
        tree = contour_fill.offset_polygon(polygon, self.row_spacing, self.join_style + 1, self.clockwise)

        stitches = []
        if self.contour_strategy == 0:
            stitches = contour_fill.inner_to_outer(
                tree,
                polygon,
                self.row_spacing,
                self.max_stitch_length,
                self.running_stitch_tolerance,
                self.smoothness,
                starting_point,
                self.avoid_self_crossing,
                self.enable_random_stitch_length,
                self.random_stitch_length_jitter,
                self.random_seed
            )
        elif self.contour_strategy == 1:
            stitches = contour_fill.single_spiral(
                tree,
                self.max_stitch_length,
                self.running_stitch_tolerance,
                starting_point,
                self.enable_random_stitch_length,
                self.random_stitch_length_jitter,
                self.random_seed
            )
        elif self.contour_strategy == 2:
            stitches = contour_fill.double_spiral(
                tree,
                self.max_stitch_length,
                self.running_stitch_tolerance,
                starting_point,
                self.enable_random_stitch_length,
                self.random_stitch_length_jitter,
                self.random_seed
            )

        stitch_group = StitchGroup(
            color=self.color,
            tags=("auto_fill", "auto_fill_top"),
            stitches=stitches,
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches)
        stitch_groups.append(stitch_group)

        return stitch_groups

    def do_guided_fill(self, shape, starting_point, ending_point):
        guide_line = self._get_guide_lines()

        # No guide line: fallback to normal autofill
        if not guide_line:
            return self.do_auto_fill(shape, starting_point, ending_point)

        stitch_group = StitchGroup(
            color=self.color,
            tags=("guided_fill", "auto_fill_top"),
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches,
            stitches=guided_fill(
                shape,
                guide_line.geoms[0],
                self.angle,
                self.row_spacing,
                self.staggers,
                self.max_stitch_length,
                self.running_stitch_length,
                self.running_stitch_tolerance,
                self.skip_last,
                starting_point,
                ending_point,
                self.underpath,
                self.guided_fill_strategy,
                self.enable_random_stitch_length,
                self.random_stitch_length_jitter,
                self.random_seed,
            )
        )
        return [stitch_group]

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

    def do_meander_fill(self, shape, original_shape, i, starting_point, ending_point):
        stitch_group = StitchGroup(
            color=self.color,
            tags=("meander_fill", "meander_fill_top"),
            stitches=meander_fill(self, shape, original_shape, i, starting_point, ending_point),
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches
        )
        return [stitch_group]

    def do_circular_fill(self, shape, starting_point, ending_point):
        # get target position
        command = self.get_command('target_point')
        if command:
            target = shgeo.Point(*command.target_point)
        else:
            target = shape.centroid
        stitches = circular_fill(
            shape,
            self.angle,
            self.row_spacing,
            self.end_row_spacing,
            self.staggers,
            self.running_stitch_length,
            self.running_stitch_tolerance,
            self.bean_stitch_repeats,
            self.repeats,
            self.skip_last,
            starting_point,
            ending_point,
            self.underpath,
            target,
            self.enable_random_stitch_length,
            self.random_stitch_length_jitter,
            self.random_seed,
        )

        stitch_group = StitchGroup(
            color=self.color,
            tags=("circular_fill", "auto_fill_top"),
            stitches=stitches,
            force_lock_stitches=self.force_lock_stitches,
            lock_stitches=self.lock_stitches
        )
        return [stitch_group]

    def do_linear_gradient_fill(self, shape, start, end):
        return linear_gradient_fill(self, shape, start, end)

    def do_tartan_fill(self, shape, start, end):
        return tartan_fill(self, shape, start, end)
