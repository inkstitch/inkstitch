from .. import Stitch, Point
from .stop import process_stop
from .trim import process_trim
from .ties import add_ties


def patches_to_stitch_plan(patches, collapse_len=3.0):
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
        color_block.add_stitches(patch.stitches)

        if patch.trim_after:
            # a trim needs to be followed by a jump to the next stitch, so
            # we'll process it when we start the next patch
            need_trim = True

        if patch.stop_after:
            process_stop_after(color_block)

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


class ColorBlock(object):
    """Holds a set of stitches, all with the same thread color."""

    def __init__(self, color=None, stitches=None):
        self._color = color
        self.stitches = stitches or []

    def __iter__(self):
        return iter(self.stitches)

    def has_color(self):
        return self._color is not None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        # TODO: this will use a ThreadColor object in the future
        self._color = value

    @property
    def last_stitch(self):
        if self.stitches:
            return self.stitches[-1]
        else:
            return None

    def filter_duplicate_stitches(self):
        if not self.stitches:
            return

        stitches = [self.stitches[0]]

        for stitch in self.stitches[1:]:
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
            self.stitches.append(Stitch(args[0].x, args[0].y))
        else:
            self.stitches.append(Stitch(*args, **kwargs))

    def add_stitches(self, stitches):
        for stitch in stitches:
            if isinstance(stitch, (Stitch, Point)):
                self.add_stitch(stitch)
            else:
                self.add_stitch(*stitch)

    def replace_stitches(self, stitches):
        self.stitches = stitches
