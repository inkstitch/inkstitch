def process_stop(color_block):
    """Handle the "stop after" checkbox.

    The user wants the machine to pause after this patch.  This can
    be useful for applique and similar on multi-needle machines that
    normally would not stop between colors.

    On such machines, the user assigns needles to the colors in the
    design before starting stitching.  C01, C02, etc are normal
    needles, but C00 is special.  For a block of stitches assigned
    to C00, the machine will continue sewing with the last color it
    had and pause after it completes the C00 block.

    That means we need to introduce an artificial color change
    shortly before the current stitch so that the user can set that
    to C00.  We'll go back 3 stitches and do that:
    """

    if len(color_block.stitches) >= 3:
        # make a copy of the stitch and turn it into a STOP code
        stitch = color_block.stitches[-3].copy()
        stitch.stop = True

        # insert it after the stitch
        color_block.stitches.insert(-2, stitch)

    # and also add a color change on this stitch, completing the C00
    # block:

    stitch = color_block.stitches[-1].copy()
    stitch.stop = True
    color_block.add_stitch(stitch)

    # reference for the above: https://github.com/lexelby/inkstitch/pull/29#issuecomment-359175447
