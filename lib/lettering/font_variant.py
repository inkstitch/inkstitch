# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import inkex

from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SVG_GROUP_TAG,
                        SVG_PATH_TAG, SVG_USE_TAG)
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
        # If the font variant file does not exist, this constructor will
        # raise an exception.  The caller should catch it and decide
        # what to do.

        self.path = font_path
        self.variant = variant
        self.default_glyph = default_glyph
        self.glyphs = {}
        self._load_glyphs()

    def _load_glyphs(self):
        svg_path = os.path.join(self.path, "%s.svg" % self.variant)
        svg = inkex.load_svg(svg_path).getroot()
        svg = self._apply_transforms(svg)

        glyph_layers = svg.xpath(".//svg:g[starts-with(@inkscape:label, 'GlyphLayer-')]", namespaces=inkex.NSS)
        for layer in glyph_layers:
            self._clean_group(layer)
            layer.attrib[INKSCAPE_LABEL] = layer.attrib[INKSCAPE_LABEL].replace("GlyphLayer-", "", 1)
            glyph_name = layer.attrib[INKSCAPE_LABEL]
            try:
                self.glyphs[glyph_name] = Glyph(layer)
            except AttributeError:
                pass

    def _clean_group(self, group):
        # We'll repurpose the layer as a container group labelled with the
        # glyph.
        del group.attrib[INKSCAPE_GROUPMODE]

        # The layer may be marked invisible, so we'll clear the 'display'
        # style and presentation attribute.
        group.style.pop('display', None)
        group.attrib.pop('display', None)

    def _apply_transforms(self, svg):
        # apply transforms to paths and use tags
        for element in svg.iterdescendants((SVG_PATH_TAG, SVG_USE_TAG)):
            transform = element.composed_transform()
            if element.tag == SVG_PATH_TAG:
                path = element.path.transform(transform)
                element.set_path(path)
                element.attrib.pop("transform", None)

            if element.tag == SVG_USE_TAG:
                oldx = element.get('x', 0)
                oldy = element.get('y', 0)
                newx, newy = transform.apply_to_point((oldx, oldy))
                element.set('x', newx)
                element.set('y', newy)
                element.attrib.pop("transform", None)

        # remove transforms after they have been applied
        for group in svg.iterdescendants(SVG_GROUP_TAG):
            group.attrib.pop('transform', None)

        return svg

    def __getitem__(self, character):
        if character in self.glyphs:
            return self.glyphs[character]
        else:
            return self.glyphs.get(self.default_glyph, None)

    def __contains__(self, character):
        return character in self.glyphs
