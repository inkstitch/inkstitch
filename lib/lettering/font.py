# -*- coding: UTF-8 -*-

from copy import deepcopy
import json
import os

import inkex

from ..elements import nodes_to_elements
from ..stitches.auto_satin import auto_satin
from ..svg import PIXELS_PER_MM
from ..svg.tags import SVG_GROUP_TAG, SVG_PATH_TAG, INKSCAPE_LABEL
from ..utils import Point, flatten
from .font_variant import FontVariant


def font_metadata(name, default=None, multiplier=None):
    def getter(self):
        value = self.metadata.get(name, default)

        if multiplier is not None:
            value *= multiplier

        return value

    return property(getter)


class Font(object):
    """Represents a font with multiple variants.

    Each font may have multiple FontVariants for left-to-right, right-to-left,
    etc.  Each variant has a set of Glyphs, one per character.

    Properties:
      path     -- the path to the directory containing this font
      metadata -- A dict of information about the font.
      name     -- Shortcut property for metadata["name"]
      license  -- contents of the font's LICENSE file, or None if no LICENSE file exists.
      variants -- A dict of FontVariants, with keys in FontVariant.VARIANT_TYPES.
    """

    def __init__(self, font_path):
        self.path = font_path
        self._load_metadata()
        self._load_license()
        self._load_variants()

    def _load_metadata(self):
        try:
            with open(os.path.join(self.path, "font.json")) as metadata_file:
                self.metadata = json.load(metadata_file)
        except IOError:
            self.metadata = {}

    def _load_license(self):
        try:
            with open(os.path.join(self.path, "LICENSE")) as license_file:
                self.license = license_file.read()
        except IOError:
            self.license = None

    def _load_variants(self):
        self.variants = {}

        for variant in FontVariant.VARIANT_TYPES:
            try:
                self.variants[variant] = FontVariant(self.path, variant, self.default_glyph)
            except IOError:
                # we'll deal with missing variants when we apply lettering
                pass

    name = font_metadata('name', '')
    description = font_metadata('description', '')
    default_variant = font_metadata('default_variant', FontVariant.LEFT_TO_RIGHT)
    default_glyph = font_metadata('defalt_glyph', u"�")
    letter_spacing = font_metadata('letter_spacing', 1.5, multiplier=PIXELS_PER_MM)
    leading = font_metadata('leading', 5, multiplier=PIXELS_PER_MM)
    word_spacing = font_metadata('word_spacing', 3, multiplier=PIXELS_PER_MM)
    kerning_pairs = font_metadata('kerning_pairs', {})
    auto_satin = font_metadata('auto_satin', True)

    def render_text(self, text, variant=None):
        glyph_set = self.variants.get(variant, self.variants[self.default_variant])

        lines = []
        position = Point(0, 0)
        last_character = None
        for line in text.splitlines():
            line = line.strip()
            current_line = inkex.etree.Element(SVG_GROUP_TAG, {
                INKSCAPE_LABEL: line
            })
            for character in line:
                if character == " ":
                    position.x += self.word_spacing
                    last_character = None
                else:
                    glyph = glyph_set[character] or glyph_set[self.default_glyph]

                    if glyph is not None:
                        node = deepcopy(glyph.node)

                        if last_character is not None:
                            position.x += self.letter_spacing + self.kerning_pairs.get(last_character + character, 0) * PIXELS_PER_MM

                        transform = "translate(%s, %s)" % position.as_tuple()
                        node.set('transform', transform)
                        current_line.append(node)
                        position.x += glyph.width

                    last_character = character

            current_line = nodes_to_elements(current_line.iterdescendants())

            if self.auto_satin:
                elements, trim_indices = auto_satin(current_line)
                current_line[:] = elements

            lines.append(current_line)

            last_character = None
            position.y += self.leading
            position.x = 0

        return lines

    def _get_kerning(self, character1, character2):
        if character1 is None:
            return self.kerning

        pair = character1 + character2
        if pair in self.kerning_pairs:
            return self.kerning_pairs[pair] * PIXELS_PER_MM
        else:
            return self.kerning
