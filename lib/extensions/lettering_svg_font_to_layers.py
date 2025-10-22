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
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# Adapted for the inkstitch lettering module to allow glyph annotations for characters
# in specific positions or settings, also allows scaling.Changes: see git history
"""Extension for converting svg fonts to layers"""

from inkex import Layer, PathElement, errormsg

from .base import InkstitchExtension

from ..svg import PIXELS_PER_MM


class LetteringSvgFontToLayers(InkstitchExtension):
    """
    An Ink/Stitch extension for converting SVG font glyphs into separate layers.
    This extension processes an SVG font embedded in an SVG document, scaling and converting each glyph into its own layer for
    further manipulation or embroidery digitization. It provides options to control the number of glyphs processed,
    the reference character for scaling, and the desired reference height in millimeters.
    Attributes:
        None explicitly defined.
    Methods:
        add_arguments(pars):
            Adds command-line arguments for glyph count, reference character, and reference height.
        scale_hkerning(scale_by):
        flip_cordinate_system(elem, emsize, baseline, scale_by):
            Scales and translates the element's path to match the desired coordinate system.
        reference_size(font, reference):
        set_view_port(font, scale_by):
            Sets the SVG viewport size and viewBox based on the scaled em size, return the width (= height) of the viewport
        set_guide_lines(font, scale_by):
            Adds guide lines for baseline, ascender, caps, x-height, and descender to the SVG. Return the baseline position
        convert_glyph_to_layer(glyph, emsize, baseline, scale_by, hide_layer):
            Converts a single glyph into a new SVG layer, applying scaling and coordinate transformation.
        effect():
            Main entry point for the extension. Processes the SVG font, scales glyphs, creates layers, and applies kerning scaling.

    Usage:
        This extension is intended to be used within the Ink/Stitch environment as a command-line or GUI extension for converting
        SVG font glyphs into layers suitable for embroidery design.
    """

    def add_arguments(self, pars) -> None:
        """ Adds command-line arguments for glyph count, reference character, and reference height.
        """
        pars.add_argument(
            "--reference",
            type=str,
            default="M",
            help="Reference character for size"
        )
        pars.add_argument(
            "--height",
            type=float,
            default=20.0,
            help="Reference character height in mm"
        )

    def scale_hkerning(self, scale_by) -> None:
        """
         Scales all horizontal kerning (hkern) values in the font by the given factor.
        """
        font = self.svg.defs.findone("svg:font")
        for hkern in font.findall("svg:hkern"):
            k = hkern.get("k", None)
            if k is not None:
                k = round(float(k) * scale_by, 2)
                hkern.set(("k"), str(k))

    def flip_cordinate_system(self, elem, emsize, baseline, scale_by):
        """
        Scale and translate the element's path, returns the path object
        """
        path = elem.path
        path.scale(scale_by, -scale_by, inplace=True)
        path.translate(0, float(emsize) - float(baseline), inplace=True)
        return path

    def reference_size(self, font, reference):
        """
        Returns the height of the reference glyph used for scaling.
        """
        for glyph in font.findall("svg:glyph"):
            if glyph.get("glyph-name") == str(reference):
                path = glyph.path
                return path.bounding_box().height
                break

    def set_view_port(self, font, scale_by) -> float:
        """
        Sets the SVG viewport size and viewBox based on the scaled em size, return the width (= height) of the viewport
        """
        fontface = font.findone("svg:font-face")

        emsize = fontface.get("units-per-em")
        emsize = round(float(emsize) * scale_by, 2)
        fontface.set("units-per-em", str(emsize))

        self.svg.set("width", str(emsize))
        self.svg.set("height", str(emsize))
        self.svg.set("viewBox", "0 0 " + str(emsize) + " " + str(emsize))
        return emsize

    def set_guide_lines(self, font, scale_by) -> float:
        """
        Adds guide lines for baseline, ascender, caps, x-height, and descender to the SVG. Return the baseline position_
        """

        baseline = font.get("horiz-origin-y")
        horiz_adv_x = round(float(font.get("horiz-adv-x", 0)) * scale_by, 2)
        font.set("horiz-adv-x", str(horiz_adv_x))

        fontface = font.findone("svg:font-face")
        if baseline is None:
            baseline = 0
        else:
            baseline = float(baseline) * scale_by

        guidebase = (self.svg.viewbox_height) - float(baseline)

        caps = round(float(fontface.get("cap-height", 0)) * scale_by, 2)
        xheight = round(float(fontface.get("x-height", 0)) * scale_by, 2)
        ascender = round(float(fontface.get("ascent", 0)) * scale_by, 2)
        descender = round(float(fontface.get("descent", 0)) * scale_by, 2)

        fontface.set("cap-height", str(caps))
        fontface.set("x-height", str(xheight))
        fontface.set("ascent", str(ascender))
        fontface.set("descent", str(descender))

        self.svg.namedview.add_guide(guidebase, True, "baseline")
        self.svg.namedview.add_guide(guidebase - ascender, True, "ascender")
        self.svg.namedview.add_guide(guidebase - caps, True, "caps")
        self.svg.namedview.add_guide(guidebase - xheight, True, "xheight")
        self.svg.namedview.add_guide(guidebase - descender, True, "decender")

        return baseline

    def convert_glyph_to_layer(self, glyph, emsize, baseline, scale_by, hide_layer):  # noqa C901
        """
        Converts a single glyph into a new SVG layer, applying scaling and coordinate transformation.
        """
        unicode_char = glyph.get("unicode")

        glyph_name = glyph.get("glyph-name").split('.')
        # if we are in the PUA zone, then we need to find the information in the glyph_name
        if unicode_char is None or ord(unicode_char[0]) >= 57344:
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

        # glyph layers (except the first one) are initially hidden
        if hide_layer:
            layer.style["display"] = "none"

        # Using curve description in d attribute of svg:glyph
        path = layer.add(PathElement())
        path.path = self.flip_cordinate_system(glyph, emsize, baseline, scale_by)

        unicode_char = glyph.get("unicode")
        if unicode_char is None:

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

            # glyph layers (except the first one) are initially hidden
            if hide_layer:
                layer.style["display"] = "none"

            # Using curve description in d attribute of svg:glyph
            path = layer.add(PathElement())
            path.path = self.flip_cordinate_system(glyph, emsize, baseline, scale_by)

    def effect(self) -> None:
        # Current code only reads the first svgfont instance
        font = self.svg.defs.findone("svg:font")
        if font is None:
            return errormsg("There are no svg fonts")

        reference_size = self.reference_size(font, self.options.reference)
        if reference_size is None:
            return errormsg("Reference glyph not found in the font")

        scale_by = self.options.height * PIXELS_PER_MM / reference_size
        emsize = self.set_view_port(font, scale_by)
        baseline = self.set_guide_lines(font, scale_by)

        count = 0
        for glyph in font.findall("svg:glyph"):
            hide_layer = count != 0
            hax = glyph.get("horiz-adv-x", None)
            if hax is not None:
                hax = round(float(hax) * scale_by, 2)
                glyph.set(("horiz-adv-x"), str(hax))
            self.convert_glyph_to_layer(glyph, emsize, baseline, scale_by, hide_layer=hide_layer)
            count += 1
        self.scale_hkerning(scale_by)


if __name__ == "__main__":
    LetteringSvgFontToLayers().run()
