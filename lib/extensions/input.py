import os
import pyembroidery

from inkex import etree
import inkex

from ..stitch_plan import StitchPlan
from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..svg.tags import INKSCAPE_LABEL


class Input(object):
    def affect(self, args):
        embroidery_file = args[0]
        pattern = pyembroidery.read(embroidery_file)
        pattern.convert_jumps_to_trim(3)

        stitch_plan = StitchPlan()
        previous_command = pyembroidery.NO_COMMAND
        pre_previous_command = pyembroidery.NO_COMMAND
        trim_after = False
        for raw_stitches, thread in pattern.get_as_colorblocks():
            color_block = stitch_plan.new_color_block(thread)
            for x, y, command in raw_stitches:
                if command == pyembroidery.END:
                    stitch_plan.previous_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                                end=True)
                elif command == pyembroidery.TRIM and previous_command == pyembroidery.END:
                    stitch_plan.previous_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                                trim=True)
                elif (command == pyembroidery.JUMP and pre_previous_command == pyembroidery.END and
                        previous_command == pyembroidery.TRIM):
                    stitch_plan.last_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                            jump=True)
                    # TODO maybe I should add them as END, end, trim, end trim jump, to be able to handle them?
                    # TODO this should be done as stitch_blocks, not color block changes.
                else:
                    trim_after = False
                if command == pyembroidery.STITCH:
                    if trim_after:
                        color_block.add_stitch(trim=True)
                        trim_after = False
                    color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0)
                if len(color_block) > 0 and command == pyembroidery.TRIM and previous_command != pyembroidery.END:
                    trim_after = True
                pre_previous_command = previous_command
                previous_command = command

        stitch_plan.delete_empty_color_blocks()

        extents = stitch_plan.extents
        svg = etree.Element("svg", nsmap=inkex.NSS, attrib={
            "width": str(extents[0] * 2),
            "height": str(extents[1] * 2),
            "viewBox": "0 0 %s %s" % (extents[0] * 2, extents[1] * 2),
        })
        render_stitch_plan(svg, stitch_plan)

        # rename the Stitch Plan layer so that it doesn't get overwritten by Embroider
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        layer.set(INKSCAPE_LABEL, os.path.basename(embroidery_file.decode("UTF-8")))
        layer.attrib.pop('id')

        # Shift the design so that its origin is at the center of the canvas
        # Note: this is NOT the same as centering the design in the canvas!
        layer.set('transform', 'translate(%s,%s)' % (extents[0], extents[1]))

        print etree.tostring(svg)
