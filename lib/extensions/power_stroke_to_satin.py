# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import SatinColumn
from ..elements.power_stroke import is_power_stroke
from ..i18n import _
from ..svg.tags import INKSTITCH_ATTRIBS
from .base import InkstitchExtension


class PowerStrokeToSatin(InkstitchExtension):
    """Convert a power stroke to a satin column"""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-k", "--keep_satin", type=inkex.Boolean, default=False, dest="keep_satin")

    def effect(self):

        if (not self.get_elements() or not self.svg.selection or
                not any(isinstance(item, SatinColumn) and is_power_stroke(item.node) for item in self.elements)):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Please select at least one power stroke to convert to a satin column."))
            return

        for element in self.elements:
            if not isinstance(element, SatinColumn) and not is_power_stroke(element.node):
                continue

            parent = element.node.getparent()
            index = parent.index(element.node) + 1
            path_style = self.path_style(element)
            d = str(element.path)

            satin = inkex.PathElement(attrib={
                "id": self.uniqueId("path"),
                "style": path_style,
                "d": d,
                INKSTITCH_ATTRIBS['satin_column']: "true",
            })
            parent.insert(index, satin)

            if not self.options.keep_satin:
                parent.remove(element.node)
            else:
                element.node.style['display'] = 'none'
        return

    def path_style(self, element):
        color = element.get_style('fill', None) or element.get_style('stroke', 'black')
        return "stroke:%s;stroke-width:1px;fill:none;" % (color)
