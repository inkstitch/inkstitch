from .. import _, PIXELS_PER_MM
from .element import param, EmbroideryElement, Patch
from ..utils import cache
from shapely import geometry as shgeo
import math
from ..stitches import running_stitch, auto_fill, legacy_fill

class Fill(EmbroideryElement):
    element_name = _("Fill")

    def __init__(self, *args, **kwargs):
        super(Fill, self).__init__(*args, **kwargs)

    @property
    @param('auto_fill', _('Manually routed fill stitching'), type='toggle', inverse=True, default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('angle', _('Angle of lines of stitches'), unit='deg', type='float', default=0)
    @cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    def color(self):
        return self.get_style("fill")

    @property
    @param('flip', _('Flip fill (start right-to-left)'), type='boolean', default=False)
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm', _('Spacing between rows'), unit='mm', type='float', default=0.25)
    def row_spacing(self):
        return max(self.get_float_param("row_spacing_mm", 0.25), 0.1 * PIXELS_PER_MM)

    @property
    def end_row_spacing(self):
        return self.get_float_param("end_row_spacing_mm")

    @property
    @param('max_stitch_length_mm', _('Maximum fill stitch length'), unit='mm', type='float', default=3.0)
    def max_stitch_length(self):
        return max(self.get_float_param("max_stitch_length_mm", 3.0), 0.1 * PIXELS_PER_MM)

    @property
    @param('staggers', _('Stagger rows this many times before repeating'), type='int', default=4)
    def staggers(self):
        return self.get_int_param("staggers", 4)

    @property
    @cache
    def paths(self):
        return self.flatten(self.parse_path())

    @property
    @cache
    def shape(self):
        poly_ary = []
        for sub_path in self.paths:
            point_ary = []
            last_pt = None
            for pt in sub_path:
                if (last_pt is not None):
                    vp = (pt[0] - last_pt[0], pt[1] - last_pt[1])
                    dp = math.sqrt(math.pow(vp[0], 2.0) + math.pow(vp[1], 2.0))
                    # dbg.write("dp %s\n" % dp)
                    if (dp > 0.01):
                        # I think too-close points confuse shapely.
                        point_ary.append(pt)
                        last_pt = pt
                else:
                    last_pt = pt
            if point_ary:
                poly_ary.append(point_ary)

        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        # TODO: actually figure out which things are holes and which are shells
        poly_ary.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)

        polygon = shgeo.MultiPolygon([(poly_ary[0], poly_ary[1:])])
        # print >> sys.stderr, "polygon valid:", polygon.is_valid
        return polygon

    def to_patches(self, last_patch):
        stitch_lists = legacy_fill(self.shape,
                                   self.angle,
                                   self.row_spacing,
                                   self.end_row_spacing,
                                   self.max_stitch_length,
                                   self.flip,
                                   self.staggers)
        return [Patch(stitches=stitch_list, color=self.color) for stitch_list in stitch_lists]
