# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..svg.tags import INKSCAPE_GROUPMODE, SVG_GROUP_TAG
from .base import InkstitchExtension


class StitchPlanPreviewUndo(InkstitchExtension):
    def effect(self):
        # delete old stitch plan
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        if layer is not None:
            del layer[:]

        # if there are layers with reduced opacity, remove opacity attribute
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            style = g.specified_style()
            # check groupmode and check for the specific opacity value of 0.4 (as used by the stitch plan)
            if (g.get(INKSCAPE_GROUPMODE) == "layer" and float(style.get('opacity', 1)) == 0.4 and not style.get('display', 'inline') == 'none'):
                g.style['opacity'] = 1
