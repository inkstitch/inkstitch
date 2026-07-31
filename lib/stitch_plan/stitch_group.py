# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from typing import Optional, Literal, Sequence

from inkex import Color
from shapely import geometry as shgeo

from .lock_stitch import LockStitch
from .stitch import Stitch
from ..utils import Point

LockStitches = tuple[LockStitch | None, LockStitch | None]


class StitchGroup:
    """A collection of Stitch objects with attached instructions and attributes.

    StitchGroups will later be combined to make ColorBlocks, which in turn are
    combined to make a StitchPlan.  Jump stitches are allowed between
    StitchGroups, but not between stitches inside a StitchGroup.  This means
    that EmbroideryElement classes should produce multiple StitchGroups only if
    they want to allow for the possibility of jump stitches to be added in
    between them by the stitch plan generation code.
    """

    color: Optional[Color] = None
    stitches: list[Stitch]
    min_jump_stitch_length: bool = False
    trim_after: bool = False
    stop_after: bool = False
    lock_stitches: LockStitches = (None, None)

    def __init__(
        self,
        color: Optional[Color] = None,
        stitches: Optional[list[Stitch]] = None,
        min_jump_stitch_length: bool = False,
        trim_after: bool = False,
        stop_after: bool = False,
        lock_stitches: Optional[tuple[LockStitch | None, LockStitch | None]] = None,
        force_lock_stitches: bool = False,
        tags: Optional[Sequence[str]] = None
    ):
        # DANGER: if you add new attributes, you MUST also set their default
        # values in __new__() below.  Otherwise, cached stitch plans can be
        # loaded and create objects without those properties defined, because
        # unpickling does not call __init__()!

        self.color = color
        self.trim_after = trim_after
        self.stop_after = stop_after
        self.lock_stitches = lock_stitches or (None, None)
        self.force_lock_stitches = force_lock_stitches
        self.min_jump_stitch_length = min_jump_stitch_length
        self.stitches = []

        if stitches:
            self.add_stitches(stitches)

        if tags:
            self.add_tags(tags)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        # Set default values for any new attributes here (see note in __init__() above)
        # instance.foo = None

        instance.lock_stitches = (None, None)

        return instance

    def __add__(self, other):
        if isinstance(other, StitchGroup):
            return StitchGroup(self.color, self.stitches + other.stitches,
                               lock_stitches=self.lock_stitches, force_lock_stitches=self.force_lock_stitches)
        else:
            raise TypeError("StitchGroup can only be added to another StitchGroup")

    def __len__(self):
        # This method allows `len(stitch_group)` and `if stitch_group:
        return len(self.stitches)

    def set_minimum_stitch_length(self, min_stitch_length):
        for stitch in self.stitches:
            stitch.min_stitch_length = min_stitch_length

    def add_stitches(self, stitches: Sequence[Stitch | Point | shgeo.Point], tags: Optional[Sequence[str]] = None):
        for stitch in stitches:
            self.add_stitch(stitch, tags=tags)

    def add_stitch(self, stitch: Stitch | Point | shgeo.Point, tags: Optional[Sequence[str]] = None):
        if isinstance(stitch, (Point, shgeo.Point)):
            stitch = Stitch(stitch, tags=tags)
        elif not isinstance(stitch, Stitch):
            raise TypeError("Expected a Stitch or Point object, got %s" % type(stitch))

        self.stitches.append(stitch)

    def reverse(self):
        return StitchGroup(self.color, self.stitches[::-1])

    def add_tags(self, tags: Sequence[str]) -> None:
        for stitch in self.stitches:
            stitch.add_tags(tags)

    def add_tag(self, tag: str) -> None:
        for stitch in self.stitches:
            stitch.add_tag(tag)

    def get_lock_stitches(self, pos: Literal['start'] | Literal['end'], disable_ties: bool = False) -> Optional[LockStitches]:
        if disable_ties or len(self.stitches) < 2:
            return None

        lock_pos = 0 if pos == "start" else 1
        lock_stitches = self.lock_stitches[lock_pos]
        if lock_stitches is None:
            return None

        stitches = lock_stitches.stitches(self.stitches, pos)
        return stitches
