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
            default=150,
            help="Stop making layers after this number of glyphs."
        )
        pars.add_argument(
            "--scale",
            type=float,
            default=1.0,
            help="Scale the font (1 = no scaling)"
        )
    def create_horizontal_guideline(self, name: str, position):
        """Create a horizontal guideline with name and position

        Args:
            name (str): the name of the guideline
            position (Union[int, float]): the vertical position of the guideline

        Returns:
            inkex.BaseElement: the created guideline
        """
        return self.svg.namedview.add_guide(
            self.svg.height - position, True, name
         #    self.svg.viewbox_height - position, True, name
        )

    def flip_cordinate_system(self, elem, emsize, baseline):
        """Scale and translate the element's path, returns the path object"""
        path = elem.path
        path.scale(self.options.scale, -self.options.scale, inplace=True)
        path.translate(0, int(emsize) - int(baseline), inplace=True)
        return path

    def effect(self):
        scale_by = self.options.scale
        # Current code only reads the first svgfont instance
        font = self.svg.defs.findone("svg:font")
        if font is None:
            return errormsg("There are no svg fonts")
        # setwidth = font.get("horiz-adv-x")
        baseline = font.get("horiz-origin-y")
        if baseline is None:
            baseline = 0
        else:
            baseline = baseline * scale_by

        guidebase = (self.svg.viewbox_height * scale_by) - baseline

        fontface = font.findone("svg:font-face")

        emsize = fontface.get("units-per-em") 
        emsize = float(emsize) * scale_by
        self.svg.set("width", str(emsize))
        self.svg.set("height", str(emsize))
        self.svg.set("viewBox", "0 0 " + str(emsize) + " " + str(emsize))

        # TODO: should we guarantee that <svg:font horiz-adv-x> equals <svg:font-face units-per-em> ?
        caps = float(fontface.get("cap-height", 0)) * scale_by  
        xheight = float(fontface.get("x-height", 0)) * scale_by
        ascender = float(fontface.get("ascent", 0)) * scale_by
        descender = float(fontface.get("descent", 0)) * scale_by
        fontface.set("cap-height",str(caps))
        fontface.set("x-height", str(xheight))
        fontface.set("ascent", str(ascender))
        fontface.set("descent", str(descender))

       

        baseline = descender
        # Create guidelines
        self.create_horizontal_guideline(_("baseline"), baseline)
        self.create_horizontal_guideline(_("ascender"), baseline + ascender)
        self.create_horizontal_guideline(_("caps"), baseline + caps)
        self.create_horizontal_guideline(_("xheight"), baseline + xheight)
        self.create_horizontal_guideline(_("descender"), baseline - descender)
      

        namedview = self.svg.namedview
        namedview.set("inkscape:document-units", "px")
        namedview.set("inkscape:cx", str(emsize / 2.0))
        namedview.set("inkscape:cy", str(emsize / 2.0))
       # self.svg.namedview.add_guide(guidebase, True, "baseline")
        # self.svg.namedview.add_guide(guidebase - ascender, True, "ascender")
        # self.svg.namedview.add_guide(guidebase - caps, True, "caps")
        # self.svg.namedview.add_guide(guidebase - xheight, True, "xheight")
        # self.svg.namedview.add_guide(guidebase + descender, True, "decender")
        count = 0
        for glyph in font.findall("svg:glyph"):
            hide_layer = count != 0
            hax = glyph.get("horiz-adv-x", None)
            if hax is not None:
                hax = float(hax) * scale_by
                glyph.set(("horiz-adv-x"), str(hax))
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
