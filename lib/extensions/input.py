import os
import pyembroidery

from inkex import etree
import inkex

from ..stitch_plan import StitchPlan
from ..svg import render_stitch_plan
from ..svg.tags import INKSCAPE_LABEL


class Input(object):
    def affect(self, args):
        embroidery_file = args[0]
        pattern = pyembroidery.read(embroidery_file)
        pattern.convert_jumps_to_trim(3)

        stitch_plan = StitchPlan()
        stitch_plan.parse_pattern_to_color_blocks(pattern)

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
