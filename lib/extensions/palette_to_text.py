# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import inkex

from ..i18n import _
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL
from ..threads.palette import ThreadPalette
from .base import InkstitchExtension


class PaletteToText(InkstitchExtension):
    # Generate a custom color palette in object related order
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--file", type=str, default=None, dest="file")
        self.arg_parser.add_argument("-o", "--notebook:options", type=str, default=None, dest="page_options")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_help")

    def effect(self):
        palette_file = self.options.file
        if not os.path.isfile(palette_file):
            inkex.errormsg(_("File does not exist."))
            return

        thread_palette = ThreadPalette(palette_file)
        if not thread_palette.is_gimp_palette:
            inkex.errormsg(_("Cannot read palette: invalid GIMP palette header"))
            return

        layer = inkex.Group(attrib={
            'id': '__inkstitch_palette__',
            INKSCAPE_LABEL: _('Thread Palette') + f': {thread_palette.name}',
            INKSCAPE_GROUPMODE: 'layer',
        })
        self.svg.append(layer)

        x = 0
        y = 0
        for color in thread_palette:
            line = "%s %s" % (color.name, color.number)
            element = inkex.TextElement()
            element.text = line
            element.style = "fill:%s;font-size:4px;" % color.to_hex_str()
            element.set('x', x)
            element.set('y', str(y))
            layer.append(element)

            y = float(y) + 5


if __name__ == '__main__':
    e = PaletteToText()
    e.run()
