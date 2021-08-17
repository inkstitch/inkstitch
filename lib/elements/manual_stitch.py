# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import shapely.geometry

from .element import EmbroideryElement, StitchGroup
from ..utils import Point, cache


class ManualStitch(EmbroideryElement):
    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @cache
    def paths(self):
        paths = self.parse_path()
        return [self.strip_control_points(path) for path in paths]

    @property
    @cache
    def shape(self):
        line_strings = [shapely.geometry.LineString(path) for path in self.paths]

        # Using convex_hull here is an important optimization.  Otherwise
        # complex paths cause operations on the shape to take a long time.
        # This especially happens when importing machine embroidery files.
        return shapely.geometry.MultiLineString(line_strings).convex_hull

    def to_patches(self, last_patch):
        patches = []
        for path in self.paths:
            points = [Point(x, y) for x, y in path]
            patches.append(StitchGroup(color=self.color, stitches=points, stitch_as_is=True))

        return patches
