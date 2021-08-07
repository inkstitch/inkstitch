# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from .base import InkstitchExtension


class StitchPlanPreview(InkstitchExtension):
    def effect(self):
        # delete old stitch plan
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        if layer is not None:
            del layer[:]

        # create new stitch plan
        if not self.get_elements():
            return

        realistic = False
        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        patches = self.elements_to_patches(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(patches, collapse_len=collapse_len)
        render_stitch_plan(svg, stitch_plan, realistic)

        # translate stitch plan to the right side of the canvas
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        layer.set('transform', 'translate(%s)' % svg.get('viewBox', '0 0 800 0').split(' ')[2])
