# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .utils.cross_stitch import CrossGeometry


def even_cross_stitch(fill, shape, starting_point):
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    if not cross_geoms.cross_diagonals1:
        return []

    return []
