# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS
from lxml import etree
from ..svg.tags import INKSCAPE_LABEL


class FontFileInfo(object):
    """
    This class reads kerning information from an SVG file
    """
    def __init__(self, path):
        with open(path, 'r', encoding="utf-8") as svg:
            self.svg = etree.parse(svg)

    # horiz_adv_x defines the wdith of specific letters (distance to next letter)
    def horiz_adv_x(self):
        # In XPath 2.0 we could use ".//svg:glyph/(@unicode|@horiz-adv-x)"
        xpath = ".//svg:glyph[@unicode and @horiz-adv-x]/@*[name()='unicode' or name()='horiz-adv-x']"
        hax = self.svg.xpath(xpath, namespaces=NSS)
        if len(hax) == 0:
            return {}
        return dict(zip(hax[0::2], [int(x) for x in hax[1::2]]))

    # kerning (specific distances of two specified letters)
    def hkern(self):
        xpath = ".//svg:hkern[(@u1 or @g1) and (@u1 or @g1) and @k]/@*[contains(name(), '1') or contains(name(), '2') or name()='k']"
        hkern = self.svg.xpath(xpath, namespaces=NSS)

        # the kerning list now contains the kerning values as a list where every first value contains the first letter(s),
        # every second value contains the second letter(s) and every third value contains the kerning
        u_first = [k for k in hkern[0::3]]
        u_second = [k for k in hkern[1::3]]
        k = [int(x) for x in hkern[2::3]]

        # sometimes a font file contains conflicting kerning value for a letter pair
        # in this case the value which is specified as a single pair overrules the one specified in a list of letters
        # therefore we want to sort our list by length of the letter values
        kern_list = list(zip(u_first, u_second, k))
        kern_list.sort(key=lambda x: len(x[0] + x[1]), reverse=True)

        for index, kerning in enumerate(kern_list):
            first, second, key = kerning
            # fontTools.agl will import fontTools.misc.py23 which will output a deprecation warning
            # ignore the warning for now - until the library fixed it
            if index == 0:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    global toUnicode
                    from fontTools.agl import toUnicode
            first = self.split_glyph_list(first)
            second = self.split_glyph_list(second)
            kern_list[index] = (first, second, key)

        hkern = {}
        for first, second, key in kern_list:
            for f in first:
                for s in second:
                    hkern[f+s] = key
        return hkern

    def split_glyph_list(self, glyph):
        glyphs = []
        if len(glyph) > 1:
            # glyph names need to be converted to unicode
            # we need to take into account, that there can be more than one first/second letter in the very same hkern element
            # in this case they will be commas separated and each first letter needs to be combined with each next letter
            # e.g. <hkern g1="A,Agrave,Aacute,Acircumflex,Atilde,Adieresis,Amacron,Abreve,Aogonek" g2="T,Tcaron" k="5" />
            glyph_names = glyph.split(",")
            for glyph_name in glyph_names:
                # each glyph can have additional special markers, e.g. o.cmp
                # toUnicode will not respect those and convert them to a simple letter
                # this behaviour will generate a wrong spacing for this letter.
                # Let's make sure to also transfer the separators and extensions to our json file
                separators = [".", "_"]
                used_separator = False
                for separator in separators:
                    glyph_with_separator = glyph_name.split(separator)
                    if len(glyph_with_separator) == 2:
                        glyphs.append("%s%s%s" % (toUnicode(glyph_with_separator[0]), separator, glyph_with_separator[1]))
                        used_separator = True
                        continue
                # there is no extra separator
                if not used_separator:
                    glyphs.append(toUnicode(glyph_name))
        else:
            glyphs.append(glyph)
        return glyphs

    # the space character
    def word_spacing(self):
        xpath = "string(.//svg:glyph[@glyph-name='space'][1]/@*[name()='horiz-adv-x'])"
        word_spacing = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(word_spacing)
        except ValueError:
            return None

    # default letter spacing
    def letter_spacing(self):
        xpath = "string(.//svg:font[@horiz-adv-x][1]/@*[name()='horiz-adv-x'])"
        letter_spacing = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(letter_spacing)
        except ValueError:
            return None

    # this value will be saved into the json file to preserve it for later font edits
    # additionally it serves to automatically define the line height (leading)
    def units_per_em(self):
        xpath = "string(.//svg:font-face[@units-per-em][1]/@*[name()='units-per-em'])"
        units_per_em = self.svg.xpath(xpath, namespaces=NSS)
        try:
            return int(units_per_em)
        except ValueError:
            return None

    """
    def missing_glyph_spacing(self):
        xpath = "string(.//svg:missing-glyph/@*[name()='horiz-adv-x'])"
        return float(self.svg.xpath(xpath, namespaces=NSS))
    """

    def glyph_list(self):
        """
        Returns a list of available glyphs in the font file
        """
        glyphs = []
        glyph_layers = self.svg.xpath(".//svg:g[starts-with(@inkscape:label, 'GlyphLayer-')]", namespaces=NSS)
        for layer in glyph_layers:
            glyph_name = layer.attrib[INKSCAPE_LABEL].replace("GlyphLayer-", "", 1)
            glyphs.append(glyph_name)
        return glyphs
