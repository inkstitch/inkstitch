import math
import sys
import traceback

from shapely import geometry as shgeo

from ..exceptions import InkstitchException
from ..i18n import _
from ..stitches import auto_fill
from ..utils import cache
from .element import Patch, param
from .fill import Fill


class AutoFill(Fill):
    element_name = _("AutoFill")

    @property
    @param('auto_fill', _('Automatically routed fill stitching'), type='toggle', default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @cache
    def outline(self):
        return self.shape.boundary[0]

    @property
    @cache
    def outline_length(self):
        return self.outline.length

    @property
    def flip(self):
        return False

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length (traversal between sections)'),
           tooltip=_('Length of stitches around the outline of the fill region used when moving from section to section.'),
           unit='mm',
           type='float',
           default=1.5)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('fill_underlay', _('Underlay'), type='toggle', group=_('AutoFill Underlay'), default=False)
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay", default=False)

    @property
    @param('fill_underlay_angle',
           _('Fill angle'),
           tooltip=_('default: fill angle + 90 deg'),
           unit='deg',
           group=_('AutoFill Underlay'),
           type='float')
    @cache
    def fill_underlay_angle(self):
        underlay_angle = self.get_float_param("fill_underlay_angle")

        if underlay_angle is not None:
            return math.radians(underlay_angle)
        else:
            return self.angle + math.pi / 2.0

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
           default=0)
    def expand(self):
        return self.get_float_param('expand_mm', 0)

    @property
    @param('underpath',
           _('Underpath'),
           tooltip=_('Travel inside the shape when moving from section to section.  Underpath '
                     'stitches avoid traveling in the direction of the row angle so that they '
                     'are not visible.  This gives them a jagged appearance.'),
           type='boolean',
           default=True)
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

    def shrink_or_grow_shape(self, amount):
        if amount:
            shape = self.shape.buffer(amount)
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

    def validation_errors(self):
        for error in super(AutoFill, self).validation_errors():
            yield error

        # TODO: catch "too small" error

    def to_patches(self, last_patch):
        stitches = []

        starting_point = self.get_starting_point(last_patch)
        ending_point = self.get_ending_point()

        try:
            if self.fill_underlay:
                stitches.extend(auto_fill(self.underlay_shape,
                                          self.fill_underlay_angle,
                                          self.fill_underlay_row_spacing,
                                          self.fill_underlay_row_spacing,
                                          self.fill_underlay_max_stitch_length,
                                          self.running_stitch_length,
                                          self.staggers,
                                          self.fill_underlay_skip_last,
                                          starting_point,
                                          underpath=self.underlay_underpath))
                starting_point = stitches[-1]

            stitches.extend(auto_fill(self.fill_shape,
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
        except InkstitchException, exc:
            # for one of our exceptions, just print the message
            self.fatal(_("Unable to autofill: ") + str(exc))
        except Exception, exc:
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
            message += traceback.format_exc()

            self.fatal(message)

        return [Patch(stitches=stitches, color=self.color)]
