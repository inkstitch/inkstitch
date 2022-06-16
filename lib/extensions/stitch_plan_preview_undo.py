# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..svg.tags import INKSCAPE_GROUPMODE, INKSTITCH_ATTRIBS, SVG_GROUP_TAG
from .base import InkstitchExtension


class StitchPlanPreviewUndo(InkstitchExtension):
    def effect(self):
        reset_stitch_plan(self.document.getroot())


def reset_stitch_plan(svg):
    # delete old stitch plan
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    # get previously invisible layers (they still should be hidden afterwards)
    if layer is not None:
        invisible_layers = layer.get(INKSTITCH_ATTRIBS['invisible_layers'], '').split(",")
        layer.getparent().remove(layer)

        # if there are layers with reduced opacity, remove opacity attribute or unhide hidden layers
        for g in svg.findall(SVG_GROUP_TAG):
            style = g.specified_style()
            if (g.get(INKSCAPE_GROUPMODE) == "layer" and float(style.get('opacity', 1)) == 0.4 or style.get('display', 'inline') == 'none'):
                if g.get_id() in invisible_layers:
                    continue

                g.style['opacity'] = 1
                g.style['display'] = 'inline'
