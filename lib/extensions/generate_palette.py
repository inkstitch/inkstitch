# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import inkex

from ..i18n import _
from ..utils import guess_inkscape_config_path
from .base import InkstitchExtension


class GeneratePalette(InkstitchExtension):
    # Generate a custom color palette in object related order
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-n", "--palette_name", type=str, default=None, dest="palette_name")
        self.arg_parser.add_argument("-f", "--palette_folder", type=str, default=None, dest="palette_folder")
        self.arg_parser.add_argument("-o", "--options", type=str, default=None, dest="page_options")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_help")

    def effect(self):
        path = self.options.palette_folder
        brand = self.options.palette_name
        file_name = "InkStitch %s.gpl" % brand
        color_palette_name = '\nName: Ink/Stitch: %s' % brand

        if not brand:
            inkex.errormsg(_("Please specify a name for your color palette."))
            return

        if path:
            if not os.path.isdir(path):
                inkex.errormsg(_("Unkown directory path."))
                return
        else:
            path = os.path.join(guess_inkscape_config_path(), 'palettes')
            if not os.path.isdir(path):
                inkex.errormsg(_("Ink/Stitch cannot find your palette folder automatically. Please enter the path manually."))
                return

        elements = self.svg.selection.rendering_order()

        if not elements:
            inkex.errormsg(_("No element selected.\n\nPlease select at least one text element with a fill color."))
            return

        colors = self._get_color_from_elements(elements)

        if not colors:
            inkex.errormsg(_("We couldn't find any fill colors on your text elements. Please read the instructions on our website."))
            return

        colors = ['GIMP Palette', color_palette_name, '\nColumns: 4', '\n# RGB Value\t                    Color Name   Number'] + colors

        file_path = os.path.join(path, file_name)
        with open(file_path, 'w', encoding='utf-8') as gpl:
            gpl.writelines(colors)

    def _get_color_from_elements(self, elements):
        colors = []
        for element in elements:
            if 'fill' not in element.style.keys() or type(element) != inkex.TextElement:
                continue

            color = inkex.Color(element.style['fill']).to_rgb()
            color_name = element.get_text().split(' ')
            if len(color_name) > 1 and color_name[-1].isdigit():
                number = color_name[-1]
                name = ' '.join(color_name[:-1])
            else:
                number = 0
                name = ' '.join(color_name)
            color = "\n%s\t%s\t%s\t%s    %s" % (str(color[0]).rjust(3), str(color[1]).rjust(3), str(color[2]).rjust(3), name.rjust(30), number)
            colors.append(color)

        return colors


if __name__ == '__main__':
    e = GeneratePalette()
    e.affect()
