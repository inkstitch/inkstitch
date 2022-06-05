# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..utils.geometry import Point
from copy import deepcopy


class Stitch(Point):
    """A stitch is a Point with extra information telling how to sew it."""

    def __init__(self, x, y=None, color=None, jump=False, stop=False, trim=False, color_change=False,
                 tie_modus=0, force_lock_stitches=False, no_ties=False, tags=None):
        if isinstance(x, Stitch):
            # Allow creating a Stitch from another Stitch.  Attributes passed as
            # arguments will override any existing attributes.
            vars(self).update(deepcopy(vars(x)))
        elif isinstance(x, Point):
            # Allow creating a Stitch from a Point
            point = x
            self.x = point.x
            self.y = point.y
        else:
            Point.__init__(self, x, y)

        self.color = color
        self.jump = jump
        self.trim = trim
        self.stop = stop
        self.color_change = color_change
        self.force_lock_stitches = force_lock_stitches
        self.tie_modus = tie_modus
        self.no_ties = no_ties
        self.tags = set()

        self.add_tags(tags or [])

    def __repr__(self):
        return "Stitch(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (self.x,
                                                                   self.y,
                                                                   self.color,
                                                                   "JUMP" if self.jump else " ",
                                                                   "TRIM" if self.trim else " ",
                                                                   "STOP" if self.stop else " ",
                                                                   "TIE MODUS" if self.tie_modus else " ",
                                                                   "FORCE LOCK STITCHES" if self.force_lock_stitches else " ",
                                                                   "NO TIES" if self.no_ties else " ",
                                                                   "COLOR CHANGE" if self.color_change else " ")

    def add_tags(self, tags):
        for tag in tags:
            self.add_tag(tag)

    def add_tag(self, tag):
        """Store arbitrary information about a stitch.

        Tags can be used to store any information about a stitch.  This can be
        used by other parts of the code to keep track of where a Stitch came
        from.  The Stitch treats tags as opaque.

        Use strings as tags.  Python automatically optimizes this kind of
        usage of strings, and it doesn't have to constantly do string
        comparisons.  More details here:

          https://stackabuse.com/guide-to-string-interning-in-python
        """
        self.tags.add(tag)

    def has_tag(self, tag):
        return tag in self.tags

    def copy(self):
        return Stitch(self.x, self.y, self.color, self.jump, self.stop, self.trim, self.color_change,
                      self.tie_modus, self.force_lock_stitches, self.no_ties, self.tags)

    def __json__(self):
        attributes = dict(vars(self))
        attributes['tags'] = list(attributes['tags'])
        return attributes
