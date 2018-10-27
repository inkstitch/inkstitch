# -*- coding: UTF-8 -*-

import os

import inkex

from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL
from .glyph import Glyph


class FontVariant(object):
    """Represents a single variant of a font.

    Each font may have multiple variants for left-to-right, right-to-left,
    etc.  Each variant has a set of Glyphs, one per character.

    A FontVariant instance can be accessed as a dict by using a unicode
    character as a key.

    Properties:
      path    -- the path to the directory containing this font
      variant -- the font variant, specified using one of the constants below
      glyphs  -- a dict of Glyphs, with the glyphs' unicode characters as keys.
    """

    # We use unicode characters rather than English strings for font file names
    # in order to be more approachable for languages other than English.
    LEFT_TO_RIGHT = u"→"
    RIGHT_TO_LEFT = u"←"
    TOP_TO_BOTTOM = u"↓"
    BOTTOM_TO_TOP = u"↑"
    VARIANT_TYPES = (LEFT_TO_RIGHT, RIGHT_TO_LEFT, TOP_TO_BOTTOM, BOTTOM_TO_TOP)

    def __init__(self, font_path, variant, default_glyph=None):
        self.path = font_path
        self.variant = variant
        self.default_glyph = default_glyph
        self.glyphs = {}
        self._load_glyphs(font_path, variant)

    def _load_glyphs(self):
        svg_path = os.path.join(self.font_path, u"%s.svg" % self.variant)
        svg = inkex.etree.parse(svg_path)

        glyph_layers = svg.xpath(".//svg:g[starts-with(@inkscape:label, 'GlyphLayer-')]", namespaces=inkex.NSS)
        for layer in glyph_layers:
            # We'll repurpose the layer as a container group labelled with the
            # glyph.
            del layer.attrib[INKSCAPE_GROUPMODE]
            layer.attrib[INKSCAPE_LABEL] = layer.attrib[INKSCAPE_LABEL].replace("GlyphLayer-", "", 1)

            glyph_name = layer.attrib[INKSCAPE_LABEL]
            self.glyphs[glyph_name] = Glyph([layer])

    def __getitem__(self, character):
        if character in self.glyphs:
            return self.glyphs[character]
        else:
            return self.glyphs.get(self.default_glyph, None)

    def __contains__(self, character):
        return character in self.glyphs
