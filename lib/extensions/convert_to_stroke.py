# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from lxml import etree

from ..elements import SatinColumn
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG
from .base import InkstitchExtension


class ConvertToStroke(InkstitchExtension):
    """Convert a satin column into a running stitch."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-k", "--keep_satin", type=inkex.Boolean, default=False, dest="keep_satin")

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            inkex.errormsg(_("Please select at least one satin column to convert to a running stitch."))
            return

        if not any(isinstance(item, SatinColumn) for item in self.elements):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Please select at least one satin column to convert to a running stitch."))
            return

        for element in self.elements:
            if not isinstance(element, SatinColumn):
                continue

            parent = element.node.getparent()
            center_line = element.center_line.simplify(0.05)

            d = "M"
            for x, y in center_line.coords:
                d += "%s,%s " % (x, y)
                d += " "

            stroke_element = etree.Element(SVG_PATH_TAG,
                                           {
                                            "id": self.uniqueId("path"),
                                            "style": self.path_style(element),
                                            "transform": get_correction_transform(element.node),
                                            "d": d
                                           })
            parent.insert(parent.index(element.node), stroke_element)
            if not self.options.keep_satin:
                parent.remove(element.node)

    def path_style(self, element):
        color = element.get_style('stroke', '#000000')
        return "stroke:%s;stroke-width:1px;stroke-dasharray:3, 1;fill:none" % (color)
