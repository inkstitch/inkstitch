# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys

import inkex

from ..i18n import _
from ..svg.tags import XLINK_HREF
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
            sys.exit()

        if path:
            if not os.path.isdir(path):
                inkex.errormsg(_("Unkown directory path."))
                sys.exit()
        else:
            path = os.path.join(guess_inkscape_config_path(), 'palettes')
            if not os.path.isdir(path):
                inkex.errormsg(_("Ink/Stitch cannot find your palette folder automatically. Please install your palette manually."))
                sys.exit()

        elements = self.svg.selected

        if not elements:
            inkex.errormsg(_("No element selected.\n\nPlease select at least one element with a color swatch fill."))
            sys.exit()

        colors = self._get_swatch_color_from_elements(elements)

        if not colors:
            inkex.errormsg(_("We couldn't find any colors in the Inkscape auto-color palette. Please read the instructions on our website."))
            sys.exit()

        colors = ['GIMP Palette', color_palette_name, '\nColumns: 4', '\n# RGB Value\t\tColor Name   Number'] + colors

        file_path = os.path.join(path, file_name)
        with open(file_path, 'w', encoding='utf-8') as gpl:
            gpl.writelines(colors)

    def _get_swatch_color_from_elements(self, elements):
        colors = []
        for element in elements:
            fill = element.style['fill']
            if not fill.startswith("url"):
                continue

            # I hope there will be a better way, but for now we seem to have to
            # grab the first gradient element, which contains a link to the next gradient element
            # which contains a stop element which reveals the actual color info
            linear_gradient = inkex.properties.match_url_and_return_element(fill, self.svg)
            color_name = linear_gradient.get(XLINK_HREF)[1:]
            xpath = "(.//svg:linearGradient[@id='%s']/svg:stop)[1]" % color_name
            color = self.document.xpath(xpath, namespaces=inkex.NSS)
            if color:
                color = inkex.Color(color[0].style["stop-color"]).to_rgb()
                color_name = color_name.split("_")
                if len(color_name) > 1 and color_name[-1].isdigit():
                    number = color_name[-1]
                    name = ' '.join(color_name[:-1])
                else:
                    name = color_name[0]
                    number = 0
                color = "\n%s\t%s\t%s\t%s   %s" % (color[0], color[1], color[2], name, number)
                colors.append(color)

        return colors


if __name__ == '__main__':
    e = GeneratePalette()
    e.affect()
