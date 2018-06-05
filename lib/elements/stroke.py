import sys

from .element import param, EmbroideryElement, Patch
from ..i18n import _
from ..utils import cache, Point


warned_about_legacy_running_stitch = False


class Stroke(EmbroideryElement):
    element_name = "Stroke"

    @property
    @param('satin_column', _('Satin stitch along paths'), type='toggle', inverse=True)
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    def dashed(self):
        return self.get_style("stroke-dasharray") is not None

    @property
    @param('running_stitch_length_mm', _('Running stitch length'), unit='mm', type='float', default=1.5)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('zigzag_spacing_mm', _('Zig-zag spacing (peak-to-peak)'), unit='mm', type='float', default=0.4)
    @cache
    def zigzag_spacing(self):
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param('repeats', _('Repeats'), type='int', default="1")
    def repeats(self):
        return self.get_int_param("repeats", 1)

    @property
    def paths(self):
        path = self.parse_path()

        if self.manual_stitch_mode:
            return [self.strip_control_points(subpath) for subpath in path]
        else:
            return self.flatten(path)

    @property
    @param('manual_stitch', _('Manual stitch placement'), tooltip=_("Stitch every node in the path.  Stitch length and zig-zag spacing are ignored."), type='boolean', default=False)
    def manual_stitch_mode(self):
        return self.get_boolean_param('manual_stitch')

    def is_running_stitch(self):
        # using stroke width <= 0.5 pixels to indicate running stitch is deprecated in favor of dashed lines

        try:
            stroke_width = float(self.get_style("stroke-width"))
        except ValueError:
            stroke_width = 1

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
            # Thsi is so tricky, and and intricate that's a major reason that we deprecated the
            # 0.5 units rule.

            # Warn them the first time.
            global warned_about_legacy_running_stitch
            if not warned_about_legacy_running_stitch:
                warned_about_legacy_running_stitch = True
                print >> sys.stderr, _("Legacy running stitch setting detected!\n\nIt looks like you're using a stroke " + \
                    "smaller than 0.5 units to indicate a running stitch, which is deprecated.  Instead, please set " + \
                    "your stroke to be dashed to indicate running stitch.  Any kind of dash will work.")

            # still allow the deprecated setting to work in order to support old files
            return True
        else:
            return False

    def stroke_points(self, emb_point_list, zigzag_spacing, stroke_width):
        # TODO: use inkstitch.stitches.running_stitch

        patch = Patch(color=self.color)

        # can't stitch a single point
        if len(emb_point_list) < 2:
            return patch

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
                        rho = zigzag_spacing
                        patch.add_stitch(p0)

                # iteration variable: how far we are along segment
                while (rho <= seg_len):
                    left_pt = p0 + along * rho + perp * side
                    patch.add_stitch(left_pt)
                    rho += zigzag_spacing
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
            path = [Point(x, y) for x, y in path]
            if self.manual_stitch_mode:
                patch = Patch(color=self.color, stitches=path, stitch_as_is=True)
            elif self.is_running_stitch():
                patch = self.stroke_points(path, self.running_stitch_length, stroke_width=0.0)
            else:
                patch = self.stroke_points(path, self.zigzag_spacing / 2.0, stroke_width=self.stroke_width)

            if patch:
                patches.append(patch)

        return patches
