# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import re
from copy import deepcopy
from math import degrees

from inkex import DirectedLineSegment, Path
from shapely.geometry import LineString
from shapely.ops import substring

from ..svg import PIXELS_PER_MM
from ..utils import string_to_floats
from .stitch import Stitch
from .lock_stitch import TIES, LOCK_TYPES


def add_ties(stitch_plan):
    """Add tie-off before and after trims, jumps, and color changes."""

    need_tie_in = True
    for color_block in stitch_plan:
        new_stitches = []
        for i, stitch in enumerate(color_block.stitches):
            is_special = stitch.trim or stitch.jump or stitch.color_change or stitch.stop

            if is_special and not need_tie_in:
                add_tie(new_stitches)
                new_stitches.append(stitch)
                need_tie_in = True
            elif need_tie_in and not is_special:
                new_stitches.append(stitch)
                add_tie(new_stitches, color_block.stitches[i:], 'start')
                need_tie_in = False
            else:
                new_stitches.append(stitch)

        color_block.replace_stitches(new_stitches)

    if not need_tie_in:
        # tie off at the end if we haven't already
        add_tie(color_block.stitches)


def add_tie(stitches, upcoming_stitches=None, pos='end'):
    if upcoming_stitches is None:
        upcoming_stitches = list(reversed(stitches))

    lock_stitch_settings = stitches[-1].lock_stitches

    # tie_modus: 0 = both | 1 = before | 2 = after | 3 = neither
    if lock_stitch_settings.tie_modus in [2, 3] or is_manual_stitch(upcoming_stitches):
        return

    lock_stitch = TIES[LOCK_TYPES[pos][lock_stitch_settings.lock_type[pos]]]

    # default to half_stitch if this is a custom lock stitch without a path definition
    if LOCK_TYPES[pos][lock_stitch_settings.lock_type[pos]] == "custom" and not lock_stitch_settings.custom_lock[pos]:
        lock_stitch = TIES['half_stitch']

    # get lock stitch path
    path = lock_stitch['path'] or lock_stitch_settings.custom_lock[pos]

    if lock_stitch['path_type'] == "relative_to_stitch":
        _add_relative_tie(stitches, upcoming_stitches, path)
    elif not re.match("^ *[0-9 .,-]*$", path):
        path = Path(path)
        # fallback to half stitch if the path is invalid
        if not path or len(list(path.end_points)) < 3:
            _add_relative_tie(stitches, upcoming_stitches, TIES['half_stitch']['path'])
        else:
            _add_svg_tie(stitches, upcoming_stitches, path, pos)
    else:
        _add_mm_tie(stitches, upcoming_stitches, path, pos)


def _add_svg_tie(stitches, upcoming_stitches, path, pos):
    # scale
    scale = stitches[-1].lock_stitches.lock_scale_percent[pos] / 100
    path.scale(scale, scale, True)

    end_points = list(path.end_points)

    lock = DirectedLineSegment(end_points[-2], end_points[-1])
    lock_stitch_angle = lock.angle

    stitch = DirectedLineSegment((upcoming_stitches[0].x, upcoming_stitches[0].y),
                                 (upcoming_stitches[1].x, upcoming_stitches[1].y))
    stitch_angle = stitch.angle

    # rotate and translate the lock stitch
    path.rotate(degrees(stitch_angle - lock_stitch_angle), lock.start, True)
    translate = stitch.start - lock.start
    path.translate(translate.x, translate.y, True)

    # Remove direction indicator from path
    # Remove last/first stitch, this is the positino of the first/last stitch of the target path
    path = list(path.end_points)[:-2]

    if pos == 'end':
        path = reversed(path)

    # insert lock stitches
    for i, stitch in enumerate(path):
        stitch = Stitch(stitch[0], stitch[1], tags=("lock_stitch", "lock_stitch_end"))
        if pos == 'start':
            stitches.insert(i, stitch)
        else:
            stitches.append(stitch)


def _add_mm_tie(stitches, upcoming_stitches, path, pos):
    # make sure the path consists of only floats
    path = string_to_floats(path, " ")

    # get the length of our lock stitch path
    # reverse the list to make sure we end with the first stitch of the target path
    if pos == 'start':
        lock_pos = []
        lock = 0
        for tie_path in reversed(path):
            lock = lock - tie_path * stitches[-1].lock_stitches.lock_scale_mm[pos]
            lock_pos.insert(0, lock)
        max_lock_length = max(lock_pos)
    if pos == 'end':
        lock_pos = []
        lock = 0
        for tie_path in path:
            lock = lock + tie_path * upcoming_stitches[0].lock_stitches.lock_scale_mm[pos]
            lock_pos.append(lock)
        max_lock_length = max(lock_pos)

    # calculate the amount stitches we need from the target path
    # and generate a line
    upcoming = [(upcoming_stitches[0].x, upcoming_stitches[0].y)]
    for i, stitch in enumerate(upcoming_stitches[1:]):
        to_start = stitch - stitches[-1]
        upcoming.append((stitch.x, stitch.y))
        if to_start.length() >= max_lock_length:
            break
    line = LineString(upcoming)

    # add tie stitches
    for i, tie_path in enumerate(lock_pos):
        if tie_path < 0:
            stitch = Stitch(upcoming_stitches[0] + tie_path * to_start.unit(), lock_stitches=stitches[-1].lock_stitches)
        else:
            stitch = substring(line, start_dist=tie_path, end_dist=tie_path)
            stitch = Stitch(stitch.x, stitch.y, lock_stitches=stitches[-1].lock_stitches)
        stitch.add_tags(("lock_stitch", "lock_stitch_start"))
        if pos == 'end':
            stitches.append(stitch)
        else:
            stitches.insert(i, stitch)


def _add_relative_tie(stitches, tie_path, path):
    path = string_to_floats(path, " ")

    to_previous = tie_path[1] - tie_path[0]
    length = to_previous.length()

    if length > 0.5 * PIXELS_PER_MM:

        # Travel back one stitch, stopping halfway there.
        # Then go forward one stitch, stopping halfway between
        # again.

        # but travel at most 1.5mm
        length = min(length, 1.5 * PIXELS_PER_MM)

        direction = to_previous.unit()

        for delta in path:
            stitches.append(Stitch(tie_path[0] + delta * length * direction))
    else:
        # Too short to travel part of the way to the previous stitch; just go
        # back and forth to it a couple times.
        for i in (1, 0, 1, 0):
            stitches.append(deepcopy(tie_path[i]))


def is_manual_stitch(tie_path):
    if len(tie_path) < 2 or tie_path[0].no_ties:
        return True
    return False
