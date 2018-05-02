from ..utils import cut_path
from ..stitches import running_stitch
from .. import Stitch
from copy import deepcopy

def add_tie(stitches, tie_path):
    if stitches[-1].no_ties:
        # It's from a manual stitch block, so don't add tie stitches.  The user
        # will add them if they want them.
        return

    tie_path = cut_path(tie_path, 0.6)
    tie_stitches = running_stitch(tie_path, 0.3)
    tie_stitches = [Stitch(stitch.x, stitch.y) for stitch in tie_stitches]

    stitches.extend(deepcopy(tie_stitches[1:]))
    stitches.extend(deepcopy(list(reversed(tie_stitches))[1:]))


def add_tie_off(stitches):
    add_tie(stitches, list(reversed(stitches)))


def add_tie_in(stitches, upcoming_stitches):
    add_tie(stitches, upcoming_stitches)


def add_ties(stitch_plan):
    """Add tie-off before and after trims, jumps, and color changes."""

    for color_block in stitch_plan:
        need_tie_in = True
        new_stitches = []
        for i, stitch in enumerate(color_block.stitches):
            is_special = stitch.trim or stitch.jump or stitch.stop

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

        if not need_tie_in:
            add_tie_off(new_stitches)

        color_block.replace_stitches(new_stitches)
