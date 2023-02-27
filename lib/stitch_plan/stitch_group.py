# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .stitch import Stitch


class StitchGroup:
    """A collection of Stitch objects with attached instructions and attributes.

    StitchGroups will later be combined to make ColorBlocks, which in turn are
    combined to make a StitchPlan.  Jump stitches are allowed between
    StitchGroups, but not between stitches inside a StitchGroup.  This means
    that EmbroideryElement classes should produce multiple StitchGroups only if
    they want to allow for the possibility of jump stitches to be added in
    between them by the stitch plan generation code.
    """

    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False,
                 lock_stitches=(None, None), force_lock_stitches=False, tags=None):
        # DANGER: if you add new attributes, you MUST also set their default
        # values in __new__() below.  Otherwise, cached stitch plans can be
        # loaded and create objects without those properties defined, because
        # unpickling does not call __init__()!

        self.color = color
        self.trim_after = trim_after
        self.stop_after = stop_after
        self.lock_stitches = lock_stitches
        self.force_lock_stitches = force_lock_stitches
        self.stitches = []

        if stitches:
            self.add_stitches(stitches)

        if tags:
            self.add_tags(tags)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        # Set default values for any new attributes here (see note in __init__() above)
        # instance.foo = None

        instance.lock_stitches = None
        
        return instance

    def __add__(self, other):
        if isinstance(other, StitchGroup):
            return StitchGroup(self.color, self.stitches + other.stitches,
                               lock_stitches=self.lock_stitches, force_lock_stitches=self.force_lock_stitches)
        else:
            raise TypeError("StitchGroup can only be added to another StitchGroup")

    def __len__(self):
        # This method allows `len(patch)` and `if patch:
        return len(self.stitches)

    def add_stitches(self, stitches, tags=None):
        for stitch in stitches:
            self.add_stitch(stitch, tags=tags)

    def add_stitch(self, stitch, tags=None):
        if not isinstance(stitch, Stitch):
            # probably a Point
            stitch = Stitch(stitch, tags=tags)

        self.stitches.append(stitch)

    def reverse(self):
        return StitchGroup(self.color, self.stitches[::-1])

    def add_tags(self, tags):
        for stitch in self.stitches:
            stitch.add_tags(tags)

    def add_tag(self, tag):
        for stitch in self.stitches:
            stitch.add_tag(tag)

    def get_lock_stitches(self, pos, disable_ties=False):
        if len(self.stitches) < 2:
            return []

        lock_pos = 0 if pos == "start" else 1
        if disable_ties or self.lock_stitches[lock_pos] is None:
            return

        stitches = self.lock_stitches[lock_pos].stitches(self.stitches, pos)
        return stitches
