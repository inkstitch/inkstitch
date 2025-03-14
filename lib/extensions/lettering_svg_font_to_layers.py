#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (C) 2011 Felipe Correa da Silva Sanches <juca@members.fsf.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
# Adapted for the inkstitch lettering module to allow glyph annotations for characters
# in specific positions or settings. Changes: see git history
"""Extension for converting svg fonts to layers"""

from inkex import Layer, PathElement, errormsg

from .base import InkstitchExtension


class LetteringSvgFontToLayers(InkstitchExtension):
    """Convert an svg font to layers"""

    def add_arguments(self, pars):
        pars.add_argument(
            "--count",
            type=int,
            default=30,
            help="Stop making layers after this number of glyphs.",
        )

    def flip_cordinate_system(self, elem, emsize, baseline):
        """Scale and translate the element's path, returns the path object"""
        path = elem.path
        path.scale(1, -1, inplace=True)
        path.translate(0, int(emsize) - int(baseline), inplace=True)
        return path

    def effect(self):
        # Current code only reads the first svgfont instance
        font = self.svg.defs.findone("svg:font")
        if font is None:
            return errormsg("There are no svg fonts")
        # setwidth = font.get("horiz-adv-x")
        baseline = font.get("horiz-origin-y")
        if baseline is None:
            baseline = 0

        guidebase = self.svg.viewbox_height - baseline

        fontface = font.findone("svg:font-face")

        emsize = fontface.get("units-per-em")

        # TODO: should we guarantee that <svg:font horiz-adv-x> equals <svg:font-face units-per-em> ?
        caps = float(fontface.get("cap-height", 0))
        xheight = float(fontface.get("x-height", 0))
        ascender = float(fontface.get("ascent", 0))
        descender = float(fontface.get("descent", 0))

        self.svg.set("width", emsize)
        self.svg.namedview.add_guide(guidebase, True, "baseline")
        self.svg.namedview.add_guide(guidebase - ascender, True, "ascender")
        self.svg.namedview.add_guide(guidebase - caps, True, "caps")
        self.svg.namedview.add_guide(guidebase - xheight, True, "xheight")
        self.svg.namedview.add_guide(guidebase + descender, True, "decender")

        count = 0
        for glyph in font.findall("svg:glyph"):
            hide_layer = count != 0
            self.convert_glyph_to_layer(glyph, emsize, baseline, hide_layer=hide_layer)
            count += 1
            if count >= self.options.count:
                break

    def convert_glyph_to_layer(self, glyph, emsize, baseline, hide_layer):
        unicode_char = glyph.get("unicode")

        glyph_name = glyph.get("glyph-name").split('.')
        if unicode_char is None:
            if len(glyph_name) == 2:
                unicode_char = glyph_name[0]
            else:
                return

        typographic_feature = ''
        if len(glyph_name) == 2:
            typographic_feature = glyph_name[1]
        else:
            arabic_form = glyph.get('arabic-form', None)
            if arabic_form is not None and len(arabic_form) > 4:
                typographic_feature = arabic_form[:4]
        if typographic_feature:
            typographic_feature = f".{typographic_feature}"

        layer = self.svg.add(Layer.new(f"GlyphLayer-{unicode_char}{typographic_feature}"))

        # glyph layers (except the first one) are innitially hidden
        if hide_layer:
            layer.style["display"] = "none"

        # Using curve description in d attribute of svg:glyph
        path = layer.add(PathElement())
        path.path = self.flip_cordinate_system(glyph, emsize, baseline)


if __name__ == "__main__":
    LetteringSvgFontToLayers().run()
