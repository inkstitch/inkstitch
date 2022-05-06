# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import logging
import math
import re
import sys
import traceback

from shapely import geometry as shgeo
from shapely.validation import explain_validity

from ..i18n import _
from ..marker import get_marker_elements
from ..stitch_plan import StitchGroup
from ..stitches import contour_fill, auto_fill, legacy_fill, guided_fill
from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSCAPE_LABEL
from ..utils import cache, version
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


class UnconnectedError(ValidationError):
    name = _("Unconnected")
    description = _("Fill: This object is made up of unconnected shapes.  This is not allowed because "
                    "Ink/Stitch doesn't know what order to stitch them in.  Please break this "
                    "object up into separate shapes.")
    steps_to_solve = [
        _('* Extensions > Ink/Stitch > Fill Tools > Break Apart Fill Objects'),
    ]


class InvalidShapeError(ValidationError):
    name = _("Border crosses itself")
    description = _("Fill: Shape is not valid.  This can happen if the border crosses over itself.")
    steps_to_solve = [
        _('* Extensions > Ink/Stitch > Fill Tools > Break Apart Fill Objects')
    ]


class FillStitch(EmbroideryElement):
    element_name = _("FillStitch")

    @property
    @param('auto_fill', _('Automatically routed fill stitching'), type='toggle', default=True, sort_index=1)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('fill_method', _('Fill method'), type='dropdown', default=0,
           options=[_("Auto Fill"), _("Contour Fill"), _("Guided Fill"), _("Legacy Fill")], sort_index=2)
    def fill_method(self):
        return self.get_int_param('fill_method', 0)

    @property
    @param('contour_strategy', _('Contour Fill Strategy'), type='dropdown', default=1,
           options=[_("Inner to Outer"), _("Single spiral"), _("Double spiral")], select_items=[('fill_method', 1)], sort_index=3)
    def contour_strategy(self):
        return self.get_int_param('contour_strategy', 1)

    @property
    @param('join_style', _('Join Style'), type='dropdown', default=0,
           options=[_("Round"), _("Mitered"), _("Beveled")], select_items=[('fill_method', 1)], sort_index=4)
    def join_style(self):
        return self.get_int_param('join_style', 0)

    @property
    @param('avoid_self_crossing', _('Avoid self-crossing'), type='boolean', default=False, select_items=[('fill_method', 1)], sort_index=5)
    def avoid_self_crossing(self):
        return self.get_boolean_param('avoid_self_crossing', False)

    @property
    @param('clockwise', _('Clockwise'), type='boolean', default=True, select_items=[('fill_method', 1)], sort_index=5)
    def clockwise(self):
        return self.get_boolean_param('clockwise', True)

    @property
    @param('angle',
           _('Angle of lines of stitches'),
           tooltip=_('The angle increases in a counter-clockwise direction.  0 is horizontal.  Negative angles are allowed.'),
           unit='deg',
           type='float',
           sort_index=6,
           select_items=[('fill_method', 0), ('fill_method', 3)],
           default=0)
    @cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    def color(self):
        # SVG spec says the default fill is black
        return self.get_style("fill", "#000000")

    @property
    @param(
        'skip_last',
        _('Skip last stitch in each row'),
        tooltip=_('The last stitch in each row is quite close to the first stitch in the next row.  '
                  'Skipping it decreases stitch count and density.'),
        type='boolean',
        sort_index=6,
        select_items=[('fill_method', 0), ('fill_method', 2),
                      ('fill_method', 3)],
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
        sort_index=7,
        select_items=[('fill_method', 0), ('fill_method', 2),
                      ('fill_method', 3)],
        default=False)
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm',
           _('Spacing between rows'),
           tooltip=_('Distance between rows of stitches.'),
           unit='mm',
           sort_index=6,
           type='float',
           default=0.25)
    def row_spacing(self):
        return max(self.get_float_param("row_spacing_mm", 0.25), 0.1 * PIXELS_PER_MM)

    @property
    def end_row_spacing(self):
        return self.get_float_param("end_row_spacing_mm")

    @property
    @param('max_stitch_length_mm',
           _('Maximum fill stitch length'),
           tooltip=_(
               'The length of each stitch in a row.  Shorter stitch may be used at the start or end of a row.'),
           unit='mm',
           sort_index=6,
           type='float',
           default=3.0)
    def max_stitch_length(self):
        return max(self.get_float_param("max_stitch_length_mm", 3.0), 0.1 * PIXELS_PER_MM)

    @property
    @param('staggers',
           _('Stagger rows this many times before repeating'),
           tooltip=_('Setting this dictates how many rows apart the stitches will be before they fall in the same column position.'),
           type='int',
           sort_index=6,
           select_items=[('fill_method', 0), ('fill_method', 3)],
           default=4)
    def staggers(self):
        return max(self.get_int_param("staggers", 4), 1)

    @property
    @cache
    def paths(self):
        paths = self.flatten(self.parse_path())
        # ensure path length
        for i, path in enumerate(paths):
            if len(path) < 3:
                paths[i] = [(path[0][0], path[0][1]), (path[0][0] +
                                                       1.0, path[0][1]), (path[0][0], path[0][1]+1.0)]
        return paths

    @property
    @cache
    def shape(self):
        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        paths = self.paths
        paths.sort(key=lambda point_list: shgeo.Polygon(
            point_list).area, reverse=True)
        # Very small holes will cause a shape to be rendered as an outline only
        # they are too small to be rendered and only confuse the auto_fill algorithm.
        # So let's ignore them
        if shgeo.Polygon(paths[0]).area > 5 and shgeo.Polygon(paths[-1]).area < 5:
            paths = [path for path in paths if shgeo.Polygon(path).area > 3]

        polygon = shgeo.MultiPolygon([(paths[0], paths[1:])])

        # There is a great number of "crossing border" errors on fill shapes
        # If the polygon fails, we can try to run buffer(0) on the polygon in the
        # hope it will fix at least some of them
        if not self.shape_is_valid(polygon):
            why = explain_validity(polygon)
            message = re.match(r".+?(?=\[)", why)
            if message.group(0) == "Self-intersection":
                buffered = polygon.buffer(0)
                # if we receive a multipolygon, only use the first one of it
                if type(buffered) == shgeo.MultiPolygon:
                    buffered = buffered[0]
                # we do not want to break apart into multiple objects (possibly in the future?!)
                # best way to distinguish the resulting polygon is to compare the area size of the two
                # and make sure users will not experience significantly altered shapes without a warning
                if type(buffered) == shgeo.Polygon and math.isclose(polygon.area, buffered.area, abs_tol=0.5):
                    polygon = shgeo.MultiPolygon([buffered])

        return polygon

    def shape_is_valid(self, shape):
        # Shapely will log to stdout to complain about the shape unless we make
        # it shut up.
        logger = logging.getLogger('shapely.geos')
        level = logger.level
        logger.setLevel(logging.CRITICAL)

        valid = shape.is_valid

        logger.setLevel(level)

        return valid

    def validation_errors(self):
        if not self.shape_is_valid(self.shape):
            why = explain_validity(self.shape)
            message, x, y = re.findall(r".+?(?=\[)|-?\d+(?:\.\d+)?", why)

            # I Wish this weren't so brittle...
            if "Hole lies outside shell" in message:
                yield UnconnectedError((x, y))
            else:
                yield InvalidShapeError((x, y))

    def validation_warnings(self):
        if self.shape.area < 20:
            label = self.node.get(INKSCAPE_LABEL) or self.node.get("id")
            yield SmallShapeWarning(self.shape.centroid, label)

        if self.shrink_or_grow_shape(self.expand, True).is_empty:
            yield ExpandWarning(self.shape.centroid)

        if self.shrink_or_grow_shape(-self.fill_underlay_inset, True).is_empty:
            yield UnderlayInsetWarning(self.shape.centroid)

        # guided fill warnings
        if self.fill_method == 2:
            guide_lines = self._get_guide_lines(True)
            if not guide_lines or guide_lines[0].is_empty:
                yield MissingGuideLineWarning(self.shape.centroid)
            elif len(guide_lines) > 1:
                yield MultipleGuideLineWarning(self.shape.centroid)
            elif guide_lines[0].disjoint(self.shape):
                yield DisjointGuideLineWarning(self.shape.centroid)
            return None

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

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length (traversal between sections)'),
           tooltip=_('Length of stitches around the outline of the fill region used when moving from section to section.'),
           unit='mm',
           type='float',
           default=1.5,
           select_items=[('fill_method', 0), ('fill_method', 2)],
           sort_index=6)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('fill_underlay', _('Underlay'), type='toggle', group=_('AutoFill Underlay'), default=True)
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay", default=True)

    @property
    @param('fill_underlay_angle',
           _('Fill angle'),
           tooltip=_('Default: fill angle + 90 deg. Insert comma-seperated list for multiple layers.'),
           unit='deg',
           group=_('AutoFill Underlay'),
           type='float')
    @cache
    def fill_underlay_angle(self):
        underlay_angles = self.get_param('fill_underlay_angle', None)
        default_value = [self.angle + math.pi / 2.0]
        if underlay_angles is not None:
            underlay_angles = underlay_angles.strip().split(',')
            try:
                underlay_angles = [math.radians(
                    float(angle)) for angle in underlay_angles]
            except (TypeError, ValueError):
                return default_value
        else:
            underlay_angles = default_value

        return underlay_angles

    @property
    @param('fill_underlay_row_spacing_mm',
           _('Row spacing'),
           tooltip=_('default: 3x fill row spacing'),
           unit='mm',
           group=_('AutoFill Underlay'),
           type='float')
    @cache
    def fill_underlay_row_spacing(self):
        return self.get_float_param("fill_underlay_row_spacing_mm") or self.row_spacing * 3

    @property
    @param('fill_underlay_max_stitch_length_mm',
           _('Max stitch length'),
           tooltip=_('default: equal to fill max stitch length'),
           unit='mm',
           group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_max_stitch_length(self):
        return self.get_float_param("fill_underlay_max_stitch_length_mm") or self.max_stitch_length

    @property
    @param('fill_underlay_inset_mm',
           _('Inset'),
           tooltip=_('Shrink the shape before doing underlay, to prevent underlay from showing around the outside of the fill.'),
           unit='mm',
           group=_('AutoFill Underlay'),
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
        group=_('AutoFill Underlay'),
        type='boolean',
        default=False)
    def fill_underlay_skip_last(self):
        return self.get_boolean_param("fill_underlay_skip_last", False)

    @property
    @param('expand_mm',
           _('Expand'),
           tooltip=_('Expand the shape before fill stitching, to compensate for gaps between shapes.'),
           unit='mm',
           type='float',
           default=0,
           sort_index=5,
           select_items=[('fill_method', 0), ('fill_method', 2)])
    def expand(self):
        return self.get_float_param('expand_mm', 0)

    @property
    @param('underpath',
           _('Underpath'),
           tooltip=_('Travel inside the shape when moving from section to section.  Underpath '
                     'stitches avoid traveling in the direction of the row angle so that they '
                     'are not visible.  This gives them a jagged appearance.'),
           type='boolean',
           default=True,
           select_items=[('fill_method', 0), ('fill_method', 2)],
           sort_index=6)
    def underpath(self):
        return self.get_boolean_param('underpath', True)

    @property
    @param(
        'underlay_underpath',
        _('Underpath'),
        tooltip=_('Travel inside the shape when moving from section to section.  Underpath '
                  'stitches avoid traveling in the direction of the row angle so that they '
                  'are not visible.  This gives them a jagged appearance.'),
        group=_('AutoFill Underlay'),
        type='boolean',
        default=True)
    def underlay_underpath(self):
        return self.get_boolean_param('underlay_underpath', True)

    def shrink_or_grow_shape(self, amount, validate=False):
        if amount:
            shape = self.shape.buffer(amount)
            # changing the size can empty the shape
            # in this case we want to use the original shape rather than returning an error
            if shape.is_empty and not validate:
                return self.shape
            if not isinstance(shape, shgeo.MultiPolygon):
                shape = shgeo.MultiPolygon([shape])
            return shape
        else:
            return self.shape

    @property
    def underlay_shape(self):
        return self.shrink_or_grow_shape(-self.fill_underlay_inset)

    @property
    def fill_shape(self):
        return self.shrink_or_grow_shape(self.expand)

    def get_starting_point(self, last_patch):
        # If there is a "fill_start" Command, then use that; otherwise pick
        # the point closest to the end of the last patch.

        if self.get_command('fill_start'):
            return self.get_command('fill_start').target_point
        elif last_patch:
            return last_patch.stitches[-1]
        else:
            return None

    def get_ending_point(self):
        if self.get_command('fill_end'):
            return self.get_command('fill_end').target_point
        else:
            return None

    def to_stitch_groups(self, last_patch):
        # backwards compatibility: legacy_fill used to be inkstitch:auto_fill == False
        if not self.auto_fill or self.fill_method == 3:
            return self.do_legacy_fill()
        else:
            stitch_groups = []
            start = self.get_starting_point(last_patch)
            end = self.get_ending_point()

            try:
                if self.fill_underlay:
                    underlay_stitch_groups, start = self.do_underlay(start)
                    stitch_groups.extend(underlay_stitch_groups)
                if self.fill_method == 0:
                    stitch_groups.extend(self.do_auto_fill(last_patch, start, end))
                if self.fill_method == 1:
                    stitch_groups.extend(self.do_contour_fill(last_patch, start))
                elif self.fill_method == 2:
                    stitch_groups.extend(self.do_guided_fill(last_patch, start, end))
            except Exception:
                self.fatal_fill_error()

            return stitch_groups

    def do_legacy_fill(self):
        stitch_lists = legacy_fill(self.shape,
                                   self.angle,
                                   self.row_spacing,
                                   self.end_row_spacing,
                                   self.max_stitch_length,
                                   self.flip,
                                   self.staggers,
                                   self.skip_last)
        return [StitchGroup(stitches=stitch_list, color=self.color) for stitch_list in stitch_lists]

    def do_underlay(self, starting_point):
        stitch_groups = []
        for i in range(len(self.fill_underlay_angle)):
            underlay = StitchGroup(
                color=self.color,
                tags=("auto_fill", "auto_fill_underlay"),
                stitches=auto_fill(
                    self.underlay_shape,
                    self.fill_underlay_angle[i],
                    self.fill_underlay_row_spacing,
                    self.fill_underlay_row_spacing,
                    self.fill_underlay_max_stitch_length,
                    self.running_stitch_length,
                    self.staggers,
                    self.fill_underlay_skip_last,
                    starting_point,
                    underpath=self.underlay_underpath))
            stitch_groups.append(underlay)

        starting_point = underlay.stitches[-1]
        return [stitch_groups, starting_point]

    def do_auto_fill(self, last_patch, starting_point, ending_point):
        stitch_group = StitchGroup(
            color=self.color,
            tags=("auto_fill", "auto_fill_top"),
            stitches=auto_fill(
                self.fill_shape,
                self.angle,
                self.row_spacing,
                self.end_row_spacing,
                self.max_stitch_length,
                self.running_stitch_length,
                self.staggers,
                self.skip_last,
                starting_point,
                ending_point,
                self.underpath))
        return [stitch_group]

    def do_contour_fill(self, last_patch, starting_point):
        if not starting_point:
            starting_point = (0, 0)
        starting_point = shgeo.Point(starting_point)

        stitch_groups = []
        for polygon in self.fill_shape.geoms:
            tree = contour_fill.offset_polygon(polygon, self.row_spacing, self.join_style + 1, self.clockwise)

            stitches = []
            if self.contour_strategy == 0:
                stitches = contour_fill.inner_to_outer(
                    tree,
                    self.row_spacing,
                    self.max_stitch_length,
                    starting_point,
                    self.avoid_self_crossing
                )
            elif self.contour_strategy == 1:
                stitches = contour_fill.single_spiral(
                    tree,
                    self.max_stitch_length,
                    starting_point
                )
            elif self.contour_strategy == 2:
                stitches = contour_fill.double_spiral(
                    tree,
                    self.max_stitch_length,
                    starting_point
                )

            stitch_group = StitchGroup(
                color=self.color,
                tags=("auto_fill", "auto_fill_top"),
                stitches=stitches)
            stitch_groups.append(stitch_group)

        return stitch_groups

    def do_guided_fill(self, last_patch, starting_point, ending_point):
        guide_line = self._get_guide_lines()

        # No guide line: fallback to normal autofill
        if not guide_line:
            return self.do_auto_fill(last_patch, starting_point, ending_point)

        stitch_group = StitchGroup(
            color=self.color,
            tags=("guided_fill", "auto_fill_top"),
            stitches=guided_fill(
                self.fill_shape,
                guide_line.geoms[0],
                self.angle,
                self.row_spacing,
                self.max_stitch_length,
                self.running_stitch_length,
                self.skip_last,
                starting_point,
                ending_point,
                self.underpath))
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

    def fatal_fill_error(self):
        if hasattr(sys, 'gettrace') and sys.gettrace():
            # if we're debugging, let the exception bubble up
            raise

        # for an uncaught exception, give a little more info so that they can create a bug report
        message = ""
        message += _("Error during autofill!  This means that there is a problem with Ink/Stitch.")
        message += "\n\n"
        # L10N this message is followed by a URL: https://github.com/inkstitch/inkstitch/issues/new
        message += _("If you'd like to help us make Ink/Stitch better, please paste this whole message into a new issue at: ")
        message += "https://github.com/inkstitch/inkstitch/issues/new\n\n"
        message += version.get_inkstitch_version() + "\n\n"
        message += traceback.format_exc()

        self.fatal(message)
