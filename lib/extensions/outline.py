# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from .base import InkstitchExtension
from shapely.geometry import LineString, MultiPolygon
from shapely import concave_hull
from ..svg.tags import SVG_PATH_TAG


class Outline(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-r", "--ratio", type=float, default=0.0, dest="ratio")
        self.arg_parser.add_argument("-a", "--allow-holes", type=inkex.Boolean, default=False, dest="allow_holes")

    def effect(self):
        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more shapes to convert to their outline."))
            return

        for element in self.svg.selection:
            self.element_to_outline(element)

    def element_to_outline(self, element):
        if element.tag_name == 'g':
            for element in element.iterdescendants(SVG_PATH_TAG):
                self.element_to_outline(element)
            return

        path = element.get_path()
        path = path.end_points
        hull = concave_hull(LineString(path), ratio=self.options.ratio, allow_holes=self.options.allow_holes)
        if isinstance(hull, LineString):
            return

        if not isinstance(hull, MultiPolygon):
            hull = MultiPolygon([hull])
        d = ''
        for geom in hull.geoms:
            d += 'M '
            for x, y in geom.exterior.coords:
                d += f'{x}, {y} '
            d += "Z"

        element.set('d', d)
