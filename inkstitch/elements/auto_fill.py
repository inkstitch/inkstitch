import math
from .. import _
from .element import param, Patch
from ..utils import cache
from .fill import Fill
from shapely import geometry as shgeo
from ..stitches import auto_fill


class AutoFill(Fill):
    element_name = _("Auto-Fill")

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
    @param('running_stitch_length_mm', _('Running stitch length (traversal between sections)'), unit='mm', type='float', default=1.5)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('fill_underlay', _('Underlay'), type='toggle', group=_('AutoFill Underlay'), default=False)
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay", default=False)

    @property
    @param('fill_underlay_angle', _('Fill angle (default: fill angle + 90 deg)'), unit='deg', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_angle(self):
        underlay_angle = self.get_float_param("fill_underlay_angle")

        if underlay_angle:
            return math.radians(underlay_angle)
        else:
            return self.angle + math.pi / 2.0

    @property
    @param('fill_underlay_row_spacing_mm', _('Row spacing (default: 3x fill row spacing)'), unit='mm', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_row_spacing(self):
        return self.get_float_param("fill_underlay_row_spacing_mm") or self.row_spacing * 3

    @property
    @param('fill_underlay_max_stitch_length_mm', _('Max stitch length'), unit='mm', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_max_stitch_length(self):
        return self.get_float_param("fill_underlay_max_stitch_length_mm") or self.max_stitch_length

    @property
    @param('fill_underlay_inset_mm', _('Inset'), unit='mm', group=_('AutoFill Underlay'), type='float', default=0)
    def fill_underlay_inset(self):
        return self.get_float_param('fill_underlay_inset_mm', 0)

    @property
    def underlay_shape(self):
        if self.fill_underlay_inset:
            shape = self.shape.buffer(-self.fill_underlay_inset)
            if not isinstance(shape, shgeo.MultiPolygon):
                shape = shgeo.MultiPolygon([shape])
            return shape
        else:
            return self.shape

    def to_patches(self, last_patch):
        stitches = []

        if last_patch is None:
            starting_point = None
        else:
            starting_point = last_patch.stitches[-1]

        if self.fill_underlay:
            stitches.extend(auto_fill(self.underlay_shape,
                                      self.fill_underlay_angle,
                                      self.fill_underlay_row_spacing,
                                      self.fill_underlay_row_spacing,
                                      self.fill_underlay_max_stitch_length,
                                      self.running_stitch_length,
                                      self.staggers,
                                      starting_point))
            starting_point = stitches[-1]

        stitches.extend(auto_fill(self.shape,
                                  self.angle,
                                  self.row_spacing,
                                  self.end_row_spacing,
                                  self.max_stitch_length,
                                  self.running_stitch_length,
                                  self.staggers,
                                  starting_point))

        return [Patch(stitches=stitches, color=self.color)]
