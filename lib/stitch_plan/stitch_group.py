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

    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False, tie_modus=0, stitch_as_is=False):
        self.color = color
        self.trim_after = trim_after
        self.stop_after = stop_after
        self.tie_modus = tie_modus
        self.stitch_as_is = stitch_as_is
        self.stitches = []

        if stitches:
            self.add_stitches(stitches)

    def __add__(self, other):
        if isinstance(other, StitchGroup):
            return StitchGroup(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("StitchGroup can only be added to another StitchGroup")

    def __len__(self):
        # This method allows `len(patch)` and `if patch:
        return len(self.stitches)

    def add_stitches(self, stitches):
        for stitch in stitches:
            self.add_stitch(stitch)

    def add_stitch(self, stitch):
        if not isinstance(stitch, Stitch):
            # probably a Point
            stitch = Stitch(stitch)

        self.stitches.append(stitch)

    def reverse(self):
        return StitchGroup(self.color, self.stitches[::-1])
