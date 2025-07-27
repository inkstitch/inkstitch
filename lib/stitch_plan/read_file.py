# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import pystitch
from .stitch_plan import StitchPlan

from ..svg import PIXELS_PER_MM


def stitch_plan_from_file(embroidery_file):
    """Read a machine embroidery file in any supported format and return a stitch plan."""
    pattern = pystitch.read(embroidery_file)

    stitch_plan = StitchPlan()
    color_block = None

    for raw_stitches, thread in pattern.get_as_colorblocks():
        color_block = stitch_plan.new_color_block(thread)
        for x, y, command in raw_stitches:
            color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                   jump=(command == pystitch.JUMP),
                                   trim=(command == pystitch.TRIM))

    return stitch_plan
