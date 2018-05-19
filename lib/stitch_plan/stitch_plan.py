from .stitch import Stitch
from .stop import process_stop
from .trim import process_trim
from .ties import add_ties
from ..svg import PIXELS_PER_MM
from ..utils.geometry import Point
from ..threads import ThreadColor


def patches_to_stitch_plan(patches, collapse_len=3.0 * PIXELS_PER_MM):
    """Convert a collection of inkstitch.element.Patch objects to a StitchPlan.

    * applies instructions embedded in the Patch such as trim_after and stop_after
    * adds tie-ins and tie-offs
    * adds jump-stitches between patches if necessary
    """

    stitch_plan = StitchPlan()
    color_block = stitch_plan.new_color_block()

    need_trim = False
    for patch in patches:
        if not patch.stitches:
            continue

        if need_trim:
            process_trim(color_block, patch.stitches[0])
            need_trim = False

        if not color_block.has_color():
            # set the color for the first color block
            color_block.color = patch.color

        if color_block.color == patch.color:
            # add a jump stitch between patches if the distance is more
            # than the collapse length
            if color_block.last_stitch:
                if (patch.stitches[0] - color_block.last_stitch).length() > collapse_len:
                    color_block.add_stitch(patch.stitches[0].x, patch.stitches[0].y, jump=True)

        else:
            # add a color change
            color_block.add_stitch(color_block.last_stitch.x, color_block.last_stitch.y, stop=True)
            color_block = stitch_plan.new_color_block()
            color_block.color = patch.color

        color_block.filter_duplicate_stitches()
        color_block.add_stitches(patch.stitches, no_ties=patch.stitch_as_is)

        if patch.trim_after:
            # a trim needs to be followed by a jump to the next stitch, so
            # we'll process it when we start the next patch
            need_trim = True

        if patch.stop_after:
            process_stop(color_block)

    add_ties(stitch_plan)

    return stitch_plan


class StitchPlan(object):
    """Holds a set of color blocks, each containing stitches."""

    def __init__(self):
        self.color_blocks = []

    def new_color_block(self, *args, **kwargs):
        color_block = ColorBlock(*args, **kwargs)
        self.color_blocks.append(color_block)
        return color_block

    def __iter__(self):
        return iter(self.color_blocks)

    def __len__(self):
        return len(self.color_blocks)

    def __repr__(self):
        return "StitchPlan(%s)" % ", ".join(repr(cb) for cb in self.color_blocks)

    @property
    def num_colors(self):
        """Number of unique colors in the stitch plan."""
        return len({block.color for block in self})

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
    def bounding_box(self):
        color_block_bounding_boxes = [cb.bounding_box for cb in self]
        minx = min(bb[0] for bb in color_block_bounding_boxes)
        miny = min(bb[1] for bb in color_block_bounding_boxes)
        maxx = max(bb[2] for bb in color_block_bounding_boxes)
        maxy = max(bb[3] for bb in color_block_bounding_boxes)

        return minx, miny, maxx, maxy

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


class ColorBlock(object):
    """Holds a set of stitches, all with the same thread color."""

    def __init__(self, color=None, stitches=None):
        self.color = color
        self.stitches = stitches or []

    def __iter__(self):
        return iter(self.stitches)

    def __repr__(self):
        return "ColorBlock(%s, %s)" % (self.color, self.stitches)

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
    def last_stitch(self):
        if self.stitches:
            return self.stitches[-1]
        else:
            return None

    @property
    def num_stitches(self):
        """Number of stitches in this color block."""
        return len(self.stitches)

    @property
    def num_stops(self):
        """Number of pauses in this color block."""

        # Stops are encoded using two STOP stitches each.  See the comment in
        # stop.py for an explanation.

        return sum(1 for stitch in self if stitch.stop) / 2

    @property
    def num_trims(self):
        """Number of trims in this color block."""

        return sum(1 for stitch in self if stitch.trim)

    def filter_duplicate_stitches(self):
        if not self.stitches:
            return

        stitches = [self.stitches[0]]

        for stitch in self.stitches[1:]:
            if stitches[-1].jump or stitch.stop or stitch.trim:
                # Don't consider jumps, stops, or trims as candidates for filtering
                pass
            else:
                l = (stitch - stitches[-1]).length()
                if l <= 0.1:
                    # duplicate stitch, skip this one
                    continue

            stitches.append(stitch)

        self.stitches = stitches

    def add_stitch(self, *args, **kwargs):
        if isinstance(args[0], Stitch):
            self.stitches.append(args[0])
        elif isinstance(args[0], Point):
            self.stitches.append(Stitch(args[0].x, args[0].y, *args[1:], **kwargs))
        else:
            self.stitches.append(Stitch(*args, **kwargs))

    def add_stitches(self, stitches, *args, **kwargs):
        for stitch in stitches:
            if isinstance(stitch, (Stitch, Point)):
                self.add_stitch(stitch, *args, **kwargs)
            else:
                self.add_stitch(*(list(stitch) + args), **kwargs)

    def replace_stitches(self, stitches):
        self.stitches = stitches

    @property
    def bounding_box(self):
        minx = min(stitch.x for stitch in self)
        miny = min(stitch.y for stitch in self)
        maxx = max(stitch.x for stitch in self)
        maxy = max(stitch.y for stitch in self)

        return minx, miny, maxx, maxy
