# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean

from ..marker import set_marker
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSTITCH_ATTRIBS,
                        SODIPODI_INSENSITIVE, SVG_GROUP_TAG, SVG_PATH_TAG)
from .base import InkstitchExtension
from .stitch_plan_preview_undo import reset_stitch_plan


class StitchPlanPreview(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-s", "--move-to-side", type=Boolean, default=True, dest="move_to_side")
        self.arg_parser.add_argument("-v", "--layer-visibility", type=str, default="unchanged", dest="layer_visibility")
        self.arg_parser.add_argument("-n", "--needle-points", type=Boolean, default=False, dest="needle_points")
        self.arg_parser.add_argument("-i", "--insensitive", type=Boolean, default=False, dest="insensitive")
        self.arg_parser.add_argument("-c", "--visual-commands", type=Boolean, default="symbols", dest="visual_commands")
        self.arg_parser.add_argument("-o", "--overwrite", type=Boolean, default=True, dest="overwrite")

    def effect(self):
        # delete old stitch plan
        self.remove_old()

        # create new stitch plan
        if not self.get_elements():
            return

        svg = self.document.getroot()
        realistic = False
        visual_commands = self.options.visual_commands
        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        patches = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(patches, collapse_len=collapse_len, min_stitch_len=min_stitch_len)
        render_stitch_plan(svg, stitch_plan, realistic, visual_commands)

        # apply options
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")

        # update layer visibility (unchanged, hidden, lower opacity)
        groups = self.document.getroot().findall(SVG_GROUP_TAG)
        self.set_invisible_layers_attribute(groups, layer)
        self.set_visibility(groups, layer)

        self.set_sensitivity(layer)
        self.translate(svg, layer)
        self.set_needle_points(layer)

    def remove_old(self):
        svg = self.document.getroot()
        if self.options.overwrite:
            reset_stitch_plan(svg)
        else:
            layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
            if layer is not None:
                layer.set('id', svg.get_unique_id('inkstitch_stitch_plan_'))

    def set_invisible_layers_attribute(self, groups, layer):
        invisible_layers = []
        for g in groups:
            if g.get(INKSCAPE_GROUPMODE) == "layer" and 'display' in g.style and g.style['display'] == 'none':
                invisible_layers.append(g.get_id())
        layer.set(INKSTITCH_ATTRIBS['invisible_layers'], ",".join(invisible_layers))
        layer.set(INKSTITCH_ATTRIBS['layer_visibility'], self.options.layer_visibility)

    def set_visibility(self, groups, layer):
        if self.options.layer_visibility == "hidden":
            self.hide_all_layers()
            layer.style['display'] = "inline"
        elif self.options.layer_visibility == "lower_opacity":
            for g in groups:
                style = g.specified_style()
                # check groupmode and exclude stitch_plan layer
                # exclude objects which are not displayed at all or already have opacity < 0.4
                if (g.get(INKSCAPE_GROUPMODE) == "layer" and not g == layer and
                        float(style.get('opacity', 1)) > 0.4 and not style.get('display', 'inline') == 'none'):
                    g.style['opacity'] = 0.4

    def set_sensitivity(self, layer):
        if self.options.insensitive is True:
            layer.set(SODIPODI_INSENSITIVE, True)
        else:
            layer.pop(SODIPODI_INSENSITIVE)

    def translate(self, svg, layer):
        if self.options.move_to_side:
            # translate stitch plan to the right side of the canvas
            translate = svg.get('viewBox', '0 0 800 0').split(' ')[2]
            layer.set('transform', f'translate({ translate })')
        else:
            layer.set('transform', None)

    def set_needle_points(self, layer):
        if self.options.needle_points:
            for element in layer.iterdescendants(SVG_PATH_TAG):
                set_marker(element, 'start', 'needle-point')
                set_marker(element, 'mid', 'needle-point')
                set_marker(element, 'end', 'needle-point')
