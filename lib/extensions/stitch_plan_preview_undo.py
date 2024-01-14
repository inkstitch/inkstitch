# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..svg.tags import INKSCAPE_GROUPMODE, INKSTITCH_ATTRIBS, SVG_GROUP_TAG
from .base import InkstitchExtension


class StitchPlanPreviewUndo(InkstitchExtension):
    def effect(self):
        reset_stitch_plan(self.document.getroot())


def reset_stitch_plan(svg, delete_stitch_plan=True):
    # delete old stitch plan
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    # get previously invisible layers (they still should be hidden afterwards)
    if layer is not None:
        display_method = layer.get(INKSTITCH_ATTRIBS['layer_visibility'], 'unchanged')
        invisible_layers = layer.get(INKSTITCH_ATTRIBS['invisible_layers'], '').split(",")
        if delete_stitch_plan:
            layer.getparent().remove(layer)

        if display_method == "unchanged":
            return

        # if there are layers with reduced opacity, remove opacity attribute or unhide hidden layers
        for g in svg.findall(SVG_GROUP_TAG):
            style = g.specified_style()
            if (g.get(INKSCAPE_GROUPMODE) == "layer" and float(style.get('opacity', 1)) == 0.4 or style.get('display', 'inline') == 'none'):
                if g.get_id() in invisible_layers:
                    continue

                g.style['opacity'] = 1
                g.style['display'] = 'inline'
