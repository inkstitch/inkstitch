from inkex import Path
from shapely import geometry as shgeo

from ..i18n import _
from ..utils import cache
from ..utils.geometry import Point
from .element import EmbroideryElement, Patch, param
from .validation import ValidationWarning


class PolylineWarning(ValidationWarning):
    name = _("Polyline Object")
    description = _("This object is an SVG PolyLine.  Ink/Stitch can work with this shape, "
                    "but you can't edit it in Inkscape.  Convert it to a manual stitch path "
                    "to allow editing.")
    steps_to_solve = [
        _("* Select this object."),
        _("* Do Path > Object to Path."),
        _('* Optional: Run the Params extension and check the "manual stitch" box.')
    ]


class Polyline(EmbroideryElement):
    # Handle a <polyline> element, which is treated as a set of points to
    # stitch exactly.
    #
    # <polyline> elements are pretty rare in SVG, from what I can tell.
    # Anything you can do with a <polyline> can also be done with a <p>, and
    # much more.
    #
    # Notably, EmbroiderModder2 uses <polyline> elements when converting from
    # common machine embroidery file formats to SVG.  Handling those here lets
    # users use File -> Import to pull in existing designs they may have
    # obtained, for example purchased fonts.

    element_name = "Polyline"

    @property
    @param('polyline', _('Manual stitch along path'), type='toggle', inverse=True)
    def polyline(self):
        return self.get_boolean_param("polyline")

    @property
    def points(self):
        # example: "1,2 0,0 1.5,3 4,2"

        points = self.node.get('points')
        points = points.split(" ")
        points = [[float(coord) for coord in point.split(",")] for point in points]

        return points

    @property
    @cache
    def shape(self):
        return shgeo.LineString(self.points)

    @property
    def path(self):
        # A polyline is a series of connected line segments described by their
        # points.  In order to make use of the existing logic for incorporating
        # svg transforms that is in our superclass, we'll convert the polyline
        # to a degenerate cubic superpath in which the bezier handles are on
        # the segment endpoints.
        path = self.node.get_path()
        path = Path(path).to_superpath()

        return path

    @property
    @cache
    def csp(self):
        csp = self.parse_path()

        return csp

    @property
    def color(self):
        # EmbroiderModder2 likes to use the `stroke` property directly instead
        # of CSS.
        return self.get_style("stroke", "#000000")

    @property
    def stitches(self):
        # For a <polyline>, we'll stitch the points exactly as they exist in
        # the SVG, with no stitch spacing interpolation, flattening, etc.

        # See the comments in the parent class's parse_path method for a
        # description of the CSP data structure.

        stitches = [point for handle_before, point, handle_after in self.csp[0]]

        return stitches

    def validation_warnings(self):
        yield PolylineWarning(self.points[0])

    def to_patches(self, last_patch):
        patch = Patch(color=self.color)

        for stitch in self.stitches:
            patch.add_stitch(Point(*stitch))

        return [patch]
