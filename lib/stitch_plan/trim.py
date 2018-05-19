def process_trim(color_block, next_stitch):
    """Handle the "trim after" checkbox.

    DST (and maybe other formats?) has no actual TRIM instruction.
    Instead, 3 sequential JUMPs cause the machine to trim the thread.

    To support both DST and other formats, we'll add a TRIM and two
    JUMPs.  The TRIM will be converted to a JUMP by libembroidery
    if saving to DST, resulting in the 3-jump sequence.
    """

    delta = next_stitch - color_block.last_stitch
    delta = delta * (1/4.0)

    pos = color_block.last_stitch

    for i in xrange(3):
        pos += delta
        color_block.add_stitch(pos.x, pos.y, jump=True)

    # first one should be TRIM instead of JUMP
    color_block.stitches[-3].jump = False
    color_block.stitches[-3].trim = True
