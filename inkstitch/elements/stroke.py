from .. import _, Point
from .element import param, EmbroideryElement, Patch
from ..utils import cache


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
    @cache
    def width(self):
        stroke_width = self.get_style("stroke-width")

        if stroke_width.endswith("px"):
            stroke_width = stroke_width[:-2]

        return float(stroke_width)

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
        return self.flatten(self.parse_path())

    def is_running_stitch(self):
        # stroke width <= 0.5 pixels is deprecated in favor of dashed lines
        return self.dashed or self.width <= 0.5

    def stroke_points(self, emb_point_list, zigzag_spacing, stroke_width):
        # TODO: use inkstitch.stitches.running_stitch

        patch = Patch(color=self.color)
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
            if self.is_running_stitch():
                patch = self.stroke_points(path, self.running_stitch_length, stroke_width=0.0)
            else:
                patch = self.stroke_points(path, self.zigzag_spacing / 2.0, stroke_width=self.width)

            patches.append(patch)

        return patches
