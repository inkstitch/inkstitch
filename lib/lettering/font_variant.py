import os

import inkex
from lxml import etree

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
    LEFT_TO_RIGHT = "→"
    RIGHT_TO_LEFT = "←"
    TOP_TO_BOTTOM = "↓"
    BOTTOM_TO_TOP = "↑"
    VARIANT_TYPES = (LEFT_TO_RIGHT, RIGHT_TO_LEFT, TOP_TO_BOTTOM, BOTTOM_TO_TOP)

    @classmethod
    def reversed_variant(cls, variant):
        if variant == cls.LEFT_TO_RIGHT:
            return cls.RIGHT_TO_LEFT
        elif variant == cls.RIGHT_TO_LEFT:
            return cls.LEFT_TO_RIGHT
        elif variant == cls.TOP_TO_BOTTOM:
            return cls.BOTTOM_TO_TOP
        elif variant == cls.BOTTOM_TO_TOP:
            return cls.TOP_TO_BOTTOM
        else:
            return None

    def __init__(self, font_path, variant, default_glyph=None):
        self.path = font_path
        self.variant = variant
        self.default_glyph = default_glyph
        self.glyphs = {}
        self._load_glyphs()

    def _load_glyphs(self):
        svg_path = os.path.join(self.path, "%s.svg" % self.variant)
        with open(svg_path) as svg_file:
            svg = etree.parse(svg_file)

        glyph_layers = svg.xpath(".//svg:g[starts-with(@inkscape:label, 'GlyphLayer-')]", namespaces=inkex.NSS)
        for layer in glyph_layers:
            self._clean_group(layer)
            layer.attrib[INKSCAPE_LABEL] = layer.attrib[INKSCAPE_LABEL].replace("GlyphLayer-", "", 1)
            glyph_name = layer.attrib[INKSCAPE_LABEL]
            self.glyphs[glyph_name] = Glyph(layer)

    def _clean_group(self, group):
        # We'll repurpose the layer as a container group labelled with the
        # glyph.
        del group.attrib[INKSCAPE_GROUPMODE]

        style_text = group.get('style')

        if style_text:
            # The layer may be marked invisible, so we'll clear the 'display'
            # style.
            style = dict(inkex.Style.parse_str(group.get('style')))
            style.pop('display')
            group.set('style', str(inkex.Style(style)))

    def __getitem__(self, character):
        if character in self.glyphs:
            return self.glyphs[character]
        else:
            return self.glyphs.get(self.default_glyph, None)

    def __contains__(self, character):
        return character in self.glyphs
