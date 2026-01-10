# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from sys import exit
from typing import List

from inkex import errormsg

from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..utils.geometry import Point
from ..utils.threading import check_stop_flag
from .color_block import ColorBlock


def stitch_groups_to_stitch_plan(stitch_groups, collapse_len=None, min_stitch_len=0.1, disable_ties=False):  # noqa: C901

    """Convert a collection of StitchGroups to a StitchPlan.

    * applies instructions embedded in the StitchGroup such as trim_after and stop_after
    * adds tie-ins and tie-offs
    * adds jump-stitches between stitch_group if necessary
    """

    if not stitch_groups:
        errormsg(_("There is no selected stitchable element. Please run "
                   "Extensions > Ink/Stitch > Troubleshoot > Troubleshoot objects in case you have expected a stitchout."))
        exit(1)

    if collapse_len is None:
        collapse_len = 3.0
    collapse_len = float(collapse_len) * PIXELS_PER_MM

    stitch_plan = StitchPlan()
    color_block = stitch_plan.new_color_block(color=stitch_groups[0].color)

    previous_stitch_group = None
    need_tie_in = True

    for stitch_group in stitch_groups:
        check_stop_flag()

        if not stitch_group.stitches:
            continue

        if color_block.color != stitch_group.color:
            # add a lock stitch to the last element of the previous group
            if not need_tie_in:
                lock_stitches = previous_stitch_group.get_lock_stitches("end", disable_ties)
                if lock_stitches:
                    color_block.add_stitches(stitches=lock_stitches)
                need_tie_in = True

            # end the previous block with a color change
            color_block.add_stitch(color_change=True)

            # make a new block of our color
            color_block = stitch_plan.new_color_block(color=stitch_group.color)
        else:
            add_lock = False
            if len(color_block) and not need_tie_in:
                distance_to_previous_stitch = (stitch_group.stitches[0] - color_block.stitches[-1]).length()
                if previous_stitch_group.force_lock_stitches:
                    add_lock = True
                elif previous_stitch_group.min_jump_stitch_length:
                    # object based minimum jump stitch length overrides the global collapse_len setting
                    if distance_to_previous_stitch > previous_stitch_group.min_jump_stitch_length:
                        add_lock = True
                elif distance_to_previous_stitch > collapse_len:
                    add_lock = True

                if add_lock:
                    lock_stitches = previous_stitch_group.get_lock_stitches("end", disable_ties)
                    need_tie_in = True
                    if lock_stitches:
                        color_block.add_stitches(stitches=lock_stitches)

        if need_tie_in is True:
            lock_stitches = stitch_group.get_lock_stitches("start", disable_ties)
            if lock_stitches:
                color_block.add_stitch(lock_stitches[0], jump=True)
                color_block.add_stitches(stitches=lock_stitches)
            else:
                color_block.add_stitch(stitch_group.stitches[0], jump=True)
            need_tie_in = False

        color_block.add_stitches(stitches=stitch_group.stitches)

        if stitch_group.trim_after or stitch_group.stop_after:
            lock_stitches = stitch_group.get_lock_stitches("end", disable_ties)
            if lock_stitches:
                color_block.add_stitches(stitches=lock_stitches)
            need_tie_in = True

        if stitch_group.trim_after:
            color_block.add_stitch(trim=True)

        if stitch_group.stop_after:
            color_block.add_stitch(stop=True)

        previous_stitch_group = stitch_group

    if not need_tie_in:
        # tie off at the end if we haven't already
        lock_stitches = stitch_group.get_lock_stitches("end", disable_ties)
        if lock_stitches:
            color_block.add_stitches(stitches=lock_stitches)

    if len(color_block) == 0:
        # last block ended in a stop, so now we have an empty block
        del stitch_plan.color_blocks[-1]

    stitch_plan.filter_duplicate_stitches(min_stitch_len)

    return stitch_plan


class StitchPlan(object):
    """Holds a set of color blocks, each containing stitches."""

    def __init__(self):
        self.color_blocks = []

    def new_color_block(self, *args, **kwargs):
        color_block = ColorBlock(*args, **kwargs)
        self.color_blocks.append(color_block)
        return color_block

    def delete_empty_color_blocks(self):
        color_blocks = []
        for color_block in self.color_blocks:
            if len(color_block) > 0:
                color_blocks.append(color_block)

        self.color_blocks = color_blocks

    def add_color_block(self, color_block):
        self.color_blocks.append(color_block)

    def filter_duplicate_stitches(self, min_stitch_len):
        for color_block in self:
            color_block.filter_duplicate_stitches(min_stitch_len)

    def __iter__(self):
        return iter(self.color_blocks)

    def __len__(self):
        return len(self.color_blocks)

    def __repr__(self):
        return "StitchPlan(%s)" % ", ".join(repr(cb) for cb in self.color_blocks)

    def __json__(self):
        return dict(color_blocks=self.color_blocks,
                    num_stops=self.num_stops,
                    num_trims=self.num_trims,
                    num_stitches=self.num_stitches,
                    bounding_box=self.bounding_box,
                    estimated_thread=self.estimated_thread
                    )

    @property
    def num_colors(self):
        """Number of unique colors in the stitch plan."""
        return len({block.color for block in self})

    @property
    def num_color_blocks(self):
        return len(self.color_blocks)

    @property
    def num_stops(self):
        return sum(block.num_stops for block in self)

    @property
    def num_trims(self):
        return sum(block.num_trims for block in self)

    @property
    def num_stitches(self):
        return sum(block.num_stitches for block in self)

    @property
    def num_jumps(self):
        return sum(block.num_jumps for block in self)

    @property
    def bounding_box(self):
        color_block_bounding_boxes = [cb.bounding_box for cb in self if len(cb) > 0]
        if not color_block_bounding_boxes:
            # Return zero-size bounding box at origin if no stitches
            return (0, 0, 0, 0)
        minx = min(bb[0] for bb in color_block_bounding_boxes)
        miny = min(bb[1] for bb in color_block_bounding_boxes)
        maxx = max(bb[2] for bb in color_block_bounding_boxes)
        maxy = max(bb[3] for bb in color_block_bounding_boxes)

        return minx, miny, maxx, maxy

    @property
    def estimated_thread(self):
        thread_meter = sum(block.estimated_thread for block in self) / PIXELS_PER_MM / 1000
        return round(thread_meter, 2)

    @property
    def dimensions(self):
        minx, miny, maxx, maxy = self.bounding_box
        return (maxx - minx, maxy - miny)

    @property
    def extents(self):
        minx, miny, maxx, maxy = self.bounding_box

        return max(-minx, maxx), max(-miny, maxy)

    @property
    def dimensions_mm(self):
        dimensions = self.dimensions
        return (dimensions[0] / PIXELS_PER_MM, dimensions[1] / PIXELS_PER_MM)

    @property
    def last_color_block(self):
        if self.color_blocks:
            return self.color_blocks[-1]
        else:
            return None

    def make_offsets(self, offsets: List[Point]):
        out = StitchPlan()
        out.color_blocks = [block.make_offsets(offsets) for block in self]
        return out
