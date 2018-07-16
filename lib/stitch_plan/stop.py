from ..svg import PIXELS_PER_MM

def process_stop(stitch_plan):
    """Handle the "stop after" checkbox.

    The user wants the machine to pause after this patch.  This can
    be useful for applique and similar on multi-needle machines that
    normally would not stop between colors.

    In most machine embroidery file formats, there's no such thing as
    an actual "STOP" instruction.  All that exists is a "color change"
    command.

    On multi-needle machines, the user assigns needles to the colors in
    the design before starting stitching.  C01, C02, etc are the normal
    needles, but C00 is special.  For a block of stitches assigned
    to C00, the machine will continue sewing with the last color it
    had and pause after it completes the C00 block.  Machines that don't
    call it C00 still have a similar concept.

    We'll add a STOP instruction at the end of this color block.
    Unfortunately, we have a bit of a catch-22: the user needs to set
    C00 (or equivalent) for the _start_ of this block to get the
    machine to stop at the end of this block.  That means it will use
    the previous color, which isn't the right color at all!

    For the first STOP in a given thread color, we'll need to
    introduce an extra color change.  The user can then set the correct
    color for the first section and C00 for the second, resulting in
    a stop where we want it.

    We'll try to find a logical place to split the color block, like
    a TRIM or a really long stitch.  Failing that, we'll just split
    it in half.
    """

    if not stitch_plan.last_color_block or len(stitch_plan.last_color_block) < 2:
        return

    last_stitch = stitch_plan.last_color_block.last_stitch
    stitch_plan.last_color_block.add_stitch(last_stitch.x, last_stitch.y, stop=True)

    if len(stitch_plan) > 1:
        # if this isn't the first stop in this color, then we're done
        if stitch_plan.color_blocks[-2].stop_after and \
            stitch_plan.color_blocks[-2].color == stitch_plan.last_color_block.color:
                return

    # We need to split this color block.  Pick the last TRIM or
    # the last long stitch (probably between distant patches).

    for i in xrange(len(stitch_plan.last_color_block) - 2, -1, -1):
        stitch = stitch_plan.last_color_block.stitches[i]

        if stitch.trim:
            # ignore the trim right before the stop we just added
            if i < len(stitch_plan.last_color_block) - 2:
                # split after the trim
                i = i + 1
                break

        if i > 0:
            next_stitch = stitch_plan.last_color_block.stitches[i + 1]

            if (stitch - next_stitch).length() > 20 * PIXELS_PER_MM:
                break

    if i == 0:
        # Darn, we didn't find a TRIM or long stitch.  Just chop the
        # block in half.
        i = len(stitch_plan.last_color_block) / 2

    new_color_block = stitch_plan.last_color_block.split_at(i)
    stitch_plan.last_color_block.add_stitch(color_change=True, fake_color_change=True)
    stitch_plan.add_color_block(new_color_block)
