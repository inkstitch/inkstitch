import sys
from libembroidery import *
from inkex import etree
import inkex
from inkstitch import PIXELS_PER_MM, _
from inkstitch.stitch_plan import StitchPlan
from inkstitch.svg import render_stitch_plan


def pattern_stitches(pattern):
    stitch_pointer = pattern.stitchList
    while stitch_pointer:
        yield stitch_pointer.stitch
        stitch_pointer = stitch_pointer.next


def main(embroidery_file):
    pattern = embPattern_create()
    embPattern_read(pattern, embroidery_file)
    embPattern_flipVertical(pattern)

    stitch_plan = StitchPlan()
    color_block = None
    current_color = None

    for stitch in pattern_stitches(pattern):
        if stitch.color != current_color:
            thread = embThreadList_getAt(pattern.threadList, stitch.color)
            color = thread.color
            color_block = stitch_plan.new_color_block((color.r, color.g, color.b))
            current_color = stitch.color

        if not stitch.flags & END:
            color_block.add_stitch(stitch.xx * PIXELS_PER_MM, stitch.yy * PIXELS_PER_MM,
                                   jump=stitch.flags & JUMP,
                                   stop=stitch.flags & STOP,
                                   trim=stitch.flags & TRIM)

    dimensions = stitch_plan.dimensions
    svg = etree.Element("svg", nsmap=inkex.NSS, attrib=
                        {
                            "width": "%s" % dimensions[0],
                            "height": "%s" % dimensions[1],
                            "viewBox": "0 0 %s %s" % dimensions,
                        })
    render_stitch_plan(svg, stitch_plan)

    print etree.tostring(svg)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
