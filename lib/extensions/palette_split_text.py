# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from .base import InkstitchExtension


class PaletteSplitText(InkstitchExtension):
    # Splits sublines of text into it's own text elements in order to color them with the color picker
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-l", "--line-height", type=int, default=6, dest="line_height")

    def effect(self):
        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more text elements to split lines."))
            return

        line_height = self.options.line_height

        for text in self.svg.selection.get(inkex.elements.TextElement):
            parent = text.getparent()
            content = text.get_text()
            lines = content.split('\n')
            lines.reverse()
            style = text.get('style')
            x = text.get('x')
            y = text.get('y')
            y = float(y) + (len(lines) - 1) * line_height
            for line in lines:
                element = inkex.TextElement()
                element.text = line
                element.set('style', style)
                element.set('x', x)
                element.set('y', str(y))
                y = float(y) - line_height
                parent.insert(0, element)
            parent.remove(text)
