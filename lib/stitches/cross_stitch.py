# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

from .cross_stitch_even import even_cross_stitch
from .cross_stitch_odd import odd_cross_stitch


def cross_stitch(fill, shape, starting_point, ending_point):
    if fill.cross_thread_count % 2 == 0:
        return even_cross_stitch(fill, shape, starting_point)
    return odd_cross_stitch(fill, shape, starting_point, ending_point)
