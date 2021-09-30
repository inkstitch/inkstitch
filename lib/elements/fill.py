# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import logging
import math
import re

from shapely import geometry as shgeo
from shapely.validation import explain_validity

from .element import EmbroideryElement, param
from .validation import ValidationError
from ..i18n import _
from ..stitch_plan import StitchGroup
from ..stitches import legacy_fill
from ..svg import PIXELS_PER_MM
from ..utils import cache


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


class Fill(EmbroideryElement):
    element_name = _("Fill")

    def __init__(self, *args, **kwargs):
        super(Fill, self).__init__(*args, **kwargs)

    @property
    @param('auto_fill',
           _('Manually routed fill stitching'),
           tooltip=_('AutoFill is the default method for generating fill stitching.'),
           type='toggle',
           inverse=True,
           default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('angle',
           _('Angle of lines of stitches'),
           tooltip=_('The angle increases in a counter-clockwise direction.  0 is horizontal.  Negative angles are allowed.'),
           unit='deg',
           type='float',
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
        default=False)
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm',
           _('Spacing between rows'),
           tooltip=_('Distance between rows of stitches.'),
           unit='mm',
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
           tooltip=_('The length of each stitch in a row.  Shorter stitch may be used at the start or end of a row.'),
           unit='mm',
           type='float',
           default=3.0)
    def max_stitch_length(self):
        return max(self.get_float_param("max_stitch_length_mm", 3.0), 0.1 * PIXELS_PER_MM)

    @property
    @param('staggers',
           _('Stagger rows this many times before repeating'),
           tooltip=_('Setting this dictates how many rows apart the stitches will be before they fall in the same column position.'),
           type='int',
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
                paths[i] = [(path[0][0], path[0][1]), (path[0][0]+1.0, path[0][1]), (path[0][0], path[0][1]+1.0)]
        return paths

    @property
    @cache
    def shape(self):
        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        paths = self.paths
        paths.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)
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

    def to_stitch_groups(self, last_patch):
        stitch_lists = legacy_fill(self.shape,
                                   self.angle,
                                   self.row_spacing,
                                   self.end_row_spacing,
                                   self.max_stitch_length,
                                   self.flip,
                                   self.staggers,
                                   self.skip_last)
        return [StitchGroup(stitches=stitch_list, color=self.color) for stitch_list in stitch_lists]
