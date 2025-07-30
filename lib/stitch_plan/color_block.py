# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import List, Optional, Iterator

from ..svg import PIXELS_PER_MM
from ..threads import ThreadColor
from ..utils.geometry import Point
from .stitch import Stitch


class ColorBlock(object):
    """Holds a set of stitches, all with the same thread color."""

    def __init__(self, color=None, stitches=None):
        self.color = color
        self.stitches: Optional[Stitch] = stitches or []

    def __iter__(self) -> Iterator[Stitch]:
        return iter(self.stitches)

    def __len__(self):
        return len(self.stitches)

    def __repr__(self):
        return "ColorBlock(%s, %s)" % (self.color, self.stitches)

    def __getitem__(self, item) -> Stitch:
        return self.stitches[item]

    def __delitem__(self, item):
        del self.stitches[item]

    def __json__(self):
        return dict(color=self.color, stitches=self.stitches)

    def has_color(self):
        return self._color is not None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, ThreadColor):
            self._color = value
        elif value is None:
            self._color = None
        else:
            self._color = ThreadColor(value)

    @property
    def last_stitch(self) -> Stitch:
        if self.stitches:
            return self.stitches[-1]
        else:
            return None

    @property
    def num_stitches(self) -> int:
        """Number of stitches in this color block."""
        return len(self.stitches)

    @property
    def estimated_thread(self) -> float:
        previous_stitch = self.stitches[0]
        length = 0
        for stitch in self.stitches[1:]:
            length += (stitch - previous_stitch).length()
            previous_stitch = stitch
        return length

    @property
    def num_stops(self) -> int:
        """Number of stops in this color block."""

        return sum(1 for stitch in self if stitch.stop)

    @property
    def num_trims(self) -> int:
        """Number of trims in this color block."""

        return sum(1 for stitch in self if stitch.trim)

    @property
    def num_jumps(self):
        """Number of jumps in this color block."""

        return sum(1 for stitch in self if stitch.jump)

    @property
    def stop_after(self) -> bool:
        # TODO: we do not add the stop command necessarily as the last stitch
        # also we do not necessarily start a new color block when a stop command appears
        if self.last_stitch is not None:
            return self.last_stitch.stop
        else:
            return False

    @property
    def trim_after(self) -> bool:
        # If there's a STOP, it will be at the end.  We still want to return
        # True.
        for stitch in reversed(self.stitches):
            if stitch.stop or stitch.jump:
                continue
            elif stitch.trim:
                return True
            else:
                break

        return False

    def filter_duplicate_stitches(self, min_stitch_len=0.1):
        if not self.stitches:
            return

        if min_stitch_len is None:
            min_stitch_len = 0.1
        min_stitch_len *= PIXELS_PER_MM

        stitches = [self.stitches[0]]
        for stitch in self.stitches[1:]:
            if stitches[-1].jump or stitch.stop or stitch.trim or stitch.color_change:
                # Don't consider jumps, stops, color changes, or trims as candidates for filtering
                pass
            elif 'lock_stitch' in stitch.tags:
                # do not filter specific stitches
                pass
            else:
                length = (stitch - stitches[-1]).length()
                min_length = stitch.min_stitch_length or min_stitch_len
                if length <= min_length:
                    # duplicate stitch, skip this one
                    continue

            stitches.append(stitch)

        self.stitches = stitches

    def add_stitch(self, *args, **kwargs):
        if not args:
            # They're adding a command, e.g. `color_block.add_stitch(stop=True)``.
            # Use the position from the last stitch.
            if self.last_stitch:
                args = (self.last_stitch.x, self.last_stitch.y)
            else:
                raise ValueError("internal error: can't add a command to an empty stitch block")
            self.stitches.append(Stitch(*args, **kwargs))
        if isinstance(args[0], Stitch):
            self.stitches.append(Stitch(*args, **kwargs))
        elif isinstance(args[0], Point):
            self.stitches.append(Stitch(args[0].x, args[0].y, *args[1:], **kwargs))

    def add_stitches(self, stitches, *args, **kwargs):
        for stitch in stitches:
            if isinstance(stitch, (Stitch, Point)):
                self.add_stitch(stitch, *args, **kwargs)
            else:
                self.add_stitch(*stitch, *args, **kwargs)

    def replace_stitches(self, stitches):
        self.stitches = stitches

    @property
    def bounding_box(self):
        minx = min(stitch.x for stitch in self)
        miny = min(stitch.y for stitch in self)
        maxx = max(stitch.x for stitch in self)
        maxy = max(stitch.y for stitch in self)

        return minx, miny, maxx, maxy

    def make_offsets(self, offsets: List[Point]):
        first_final_stitch = len(self.stitches)
        while (first_final_stitch > 0 and self.stitches[first_final_stitch-1].is_terminator):
            first_final_stitch -= 1
        if first_final_stitch == 0:
            return self
        final_stitches = self.stitches[first_final_stitch:]
        block_stitches = self.stitches[:first_final_stitch]

        out = ColorBlock(self.color)
        for i, offset in enumerate(offsets):
            out.add_stitches([s.offset(offset) for s in block_stitches])
            if i != len(offsets) - 1:
                out.add_stitch(trim=True)
        out.add_stitches(final_stitches)
        return out
