import wx
from lib.stitch_plan.stitch import STITCH, JUMP, TRIM, STOP, COLOR_CHANGE, END, PIXEL_DENSITY
from lib.svg import PIXELS_PER_MM


class StitchBlocks:
    def __init__(self):
        self.stitch_blocks = []
        self.pens = []
        self.commands = []

    @property
    def num_stitch_blocks(self):
        if self.stitch_blocks is None:
            return 0
        else:
            return len(self.stitch_blocks)

    def stitches_for_stitch_block_index(self, this_stitch_block):
        if this_stitch_block <= self.num_stitch_blocks:
            return self.stitch_blocks[this_stitch_block]
        else:
            return []

    def previous_stitch_block(self, current_stitch_block):
        if current_stitch_block <= 0:
            return 0
        if current_stitch_block >= self.num_stitch_blocks:
            return self.num_stitch_blocks - 1
        return current_stitch_block - 1

    def next_stitch_block(self, current_stitch_block):
        if current_stitch_block >= self.num_stitch_blocks - 1:
            return self.num_stitch_blocks - 1
        if current_stitch_block < 0:
            return 0
        return current_stitch_block + 1

    def previous_command(self, current_stitch):
        # current_stitch_block = self.get_stitch_block_for_stitch(current_stitch)
        # stitches_in_previous_blocks = self.stitches_in_previous_stitch_blocks(current_stitch_block)
        # stitch_in_this_block = current_stitch - stitches_in_previous_blocks
        # first we adjust from wanted_stitch being 1-based, and then we exclude current stitch from the search
        #  the last is done by xrange itself
        for this_command in reversed(xrange(current_stitch)):
            if self.commands[this_command] != STITCH:
                return this_command
        return 0

    def next_command(self, current_stitch):
        for this_command in xrange(current_stitch + 1, len(self.commands)):
            if self.commands[this_command] != STITCH:
                return this_command
        return len(self.commands) - 1

    def stitches_in_previous_stitch_blocks(self, current_block):
        stitches_in_previous_blocks = 0
        for this_block in xrange(current_block):
            stitches_in_previous_blocks += len(self.stitch_blocks[this_block])
        return stitches_in_previous_blocks

    def stitch_block_from_stitch(self, current_stitch):
        stitches_in_previous_blocks = 0
        for this_block in xrange(self.num_stitch_blocks):
            if current_stitch - stitches_in_previous_blocks < len(self.stitch_blocks[this_block]):
                return this_block
            else:
                stitches_in_previous_blocks += len(self.stitch_blocks[this_block])
        return None

    def stitches_before_stitch_block_start(self, stitch_block):
        stitches_before = 0
        for this_block in xrange(stitch_block):
            stitches_before += len(self.stitch_blocks[this_block])
        return stitches_before

    def parse_stitch_plan(self, minx, miny, stitch_plan):
        self.stitch_blocks = []
        self.pens = []

        # We want the same indexing and length on commands as on stitch info.
        # self.commands = [None]

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)
            stitch_block = []

            for stitch in color_block:
                # trim any whitespace on the left and top and scale to the
                # pixel density
                stitch_block.append((PIXEL_DENSITY * (stitch.x - minx),
                                     PIXEL_DENSITY * (stitch.y - miny)))

                if stitch.trim:
                    self.commands.append(TRIM)
                    # TODO looks like simulator does not show trim and jump and end when read in fro svg????
                elif stitch.jump:
                    self.commands.append(JUMP)
                elif stitch.stop:
                    self.commands.append(STOP)
                elif stitch.color_change:
                    self.commands.append(COLOR_CHANGE)
                elif stitch.end:
                    self.commands.append(END)
                else:
                    self.commands.append(STITCH)

                if stitch.trim or stitch.stop or stitch.color_change:
                    self.pens.append(pen)
                    self.stitch_blocks.append(stitch_block)
                    stitch_block = []

            if stitch_block:
                self.pens.append(pen)
                self.stitch_blocks.append(stitch_block)

    def color_to_pen(self, color):
        # We draw the thread with a thickness of 0.1mm.  Real thread has a
        # thickness of ~0.4mm, but if we did that, we wouldn't be able to
        # see the individual stitches.
        return wx.Pen(color.visible_on_white.rgb, width=int(0.1 * PIXELS_PER_MM * PIXEL_DENSITY))
