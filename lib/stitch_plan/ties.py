# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import deepcopy

from .stitch import Stitch
from ..svg import PIXELS_PER_MM


def add_tie(stitches, tie_path):
    if len(tie_path) < 2 or tie_path[0].no_ties:
        # It's from a manual stitch block, so don't add tie stitches.  The user
        # will add them if they want them.
        return

    to_previous = tie_path[1] - tie_path[0]
    length = to_previous.length()
    if length > 0.5 * PIXELS_PER_MM:
        # Travel back one stitch, stopping halfway there.
        # Then go forward one stitch, stopping halfway between
        # again.

        # but travel at most 1.5mm
        length = min(length, 1.5 * PIXELS_PER_MM)

        direction = to_previous.unit()
        for delta in (0.5, 1.0, 0.5, 0):
            stitches.append(Stitch(tie_path[0] + delta * length * direction))
    else:
        # Too short to travel part of the way to the previous stitch; ust go
        # back and forth to it a couple times.
        for i in (1, 0, 1, 0):
            stitches.append(deepcopy(tie_path[i]))


def add_tie_off(stitches):
    # tie_modus: 0 = both | 1 = before | 2 = after | 3 = neither
    if stitches[-1].tie_modus not in [1, 3] or stitches[-1].force_lock_stitches:
        add_tie(stitches, stitches[-1:-3:-1])


def add_tie_in(stitches, upcoming_stitches):
    if stitches[0].tie_modus not in [2, 3]:
        add_tie(stitches, upcoming_stitches)


def add_ties(stitch_plan):
    """Add tie-off before and after trims, jumps, and color changes."""

    need_tie_in = True
    for color_block in stitch_plan:
        new_stitches = []
        for i, stitch in enumerate(color_block.stitches):
            is_special = stitch.trim or stitch.jump or stitch.color_change or stitch.stop

            if is_special and not need_tie_in:
                add_tie_off(new_stitches)
                new_stitches.append(stitch)
                need_tie_in = True
            elif need_tie_in and not is_special:
                new_stitches.append(stitch)
                add_tie_in(new_stitches, upcoming_stitches=color_block.stitches[i:])
                need_tie_in = False
            else:
                new_stitches.append(stitch)

        color_block.replace_stitches(new_stitches)

    if not need_tie_in:
        # tie off at the end if we haven't already
        add_tie_off(color_block.stitches)
