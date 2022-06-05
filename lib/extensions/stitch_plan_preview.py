# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, Style
from lxml import etree

from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from ..svg.tags import (INKSCAPE_GROUPMODE, SVG_DEFS_TAG, SVG_GROUP_TAG,
                        SVG_PATH_TAG)
from .base import InkstitchExtension


class StitchPlanPreview(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-s", "--move-to-side", type=Boolean, default=True, dest="move_to_side")
        self.arg_parser.add_argument("-v", "--layer-visibility", type=int, default=0, dest="layer_visibility")
        self.arg_parser.add_argument("-n", "--needle-points", type=Boolean, default=False, dest="needle_points")

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
        patches = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(patches, collapse_len=collapse_len)
        render_stitch_plan(svg, stitch_plan, realistic)

        # apply options
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")

        # update layer visibility 0 = unchanged, 1 = hidden, 2 = lower opacity
        if self.options.layer_visibility == 1:
            self.hide_all_layers()
            layer.set('style', None)
        elif self.options.layer_visibility == 2:
            for g in self.document.getroot().findall(SVG_GROUP_TAG):
                style = g.specified_style()
                # check groupmode and exclude stitch_plan layer
                # exclude objects which are not displayed at all or already have opacity < 0.4
                if (g.get(INKSCAPE_GROUPMODE) == "layer" and not g == layer and
                        float(style.get('opacity', 1)) > 0.4 and not style.get('display', 'inline') == 'none'):
                    style += Style('opacity:0.4')
                    g.set("style", style)

        # translate stitch plan to the right side of the canvas
        if self.options.move_to_side:
            layer.set('transform', 'translate(%s)' % svg.get('viewBox', '0 0 800 0').split(' ')[2])
        else:
            layer.set('transform', None)

        # display needle points
        if self.options.needle_points:
            markers = 'marker-mid:url(#inkstitch-needle-point);marker-start:url(#inkstitch-needle-point);marker-end:url(#inkstitch-needle-point)'
            for element in layer.iterdescendants(SVG_PATH_TAG):
                style = ';'.join([element.get('style'), markers])
                element.set('style', style)
            self.ensure_marker()

    def ensure_marker(self):
        xpath = ".//svg:marker[@id='inkstitch-needle-point']"
        point_marker = self.document.getroot().xpath(xpath)

        if not point_marker:
            # get or create def element
            defs = self.document.find(SVG_DEFS_TAG)
            if defs is None:
                defs = etree.SubElement(self.document, SVG_DEFS_TAG)

            # insert marker
            marker = """<marker
                      orient="auto"
                      id="inkstitch-needle-point">
                         <circle
                                 cx="0" cy="0" r="1.5"
                                 style="fill:context-stroke;opacity:0.8;" />
                     </marker>"""
            defs.append(etree.fromstring(marker))
