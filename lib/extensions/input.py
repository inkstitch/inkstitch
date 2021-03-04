import os

import inkex
from lxml import etree

import pyembroidery

from ..stitch_plan import StitchPlan
from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..svg.tags import INKSCAPE_LABEL


class Input(object):
    def run(self, args):
        embroidery_file = args[0]
        pattern = pyembroidery.read(embroidery_file)

        stitch_plan = StitchPlan()
        color_block = None

        for raw_stitches, thread in pattern.get_as_colorblocks():
            color_block = stitch_plan.new_color_block(thread)
            for x, y, command in raw_stitches:
                if command == pyembroidery.STITCH:
                    color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0)
                if len(color_block) > 0:
                    if command == pyembroidery.TRIM:
                        color_block.add_stitch(trim=True)
                    elif command == pyembroidery.STOP:
                        color_block.add_stitch(stop=True)
                        color_block = stitch_plan.new_color_block(thread)

        stitch_plan.delete_empty_color_blocks()

        if stitch_plan.last_color_block:
            if stitch_plan.last_color_block.last_stitch:
                if stitch_plan.last_color_block.last_stitch.stop:
                    # ending with a STOP command is redundant, so remove it
                    del stitch_plan.last_color_block[-1]

        extents = stitch_plan.extents
        svg = etree.Element("svg", nsmap=inkex.NSS, attrib={
            "width": str(extents[0] * 2),
            "height": str(extents[1] * 2),
            "viewBox": "0 0 %s %s" % (extents[0] * 2, extents[1] * 2),
        })
        render_stitch_plan(svg, stitch_plan)

        # rename the Stitch Plan layer so that it doesn't get overwritten by Embroider
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        layer.set(INKSCAPE_LABEL, os.path.basename(embroidery_file))
        layer.attrib.pop('id')

        # Shift the design so that its origin is at the center of the canvas
        # Note: this is NOT the same as centering the design in the canvas!
        layer.set('transform', 'translate(%s,%s)' % (extents[0], extents[1]))

        print(etree.tostring(svg).decode('utf-8'))
