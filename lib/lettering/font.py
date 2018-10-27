from copy import deepcopy
import json
import os

from ..svg import PIXELS_PER_MM
from ..utils import Point
from .font_variant import FontVariant


def font_metadata(name, default=None):
    def getter(self):
        return self.metadata.get(name, default)

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
                self.license = json.load(license_file)
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

    name = font_metadata('name')
    default_variant = font_metadata('default_variant', FontVariant.LEFT_TO_RIGHT)
    default_glyph = font_metadata('defalt_glyph', u"�")
    kerning = font_metadata('kerning', 2 * PIXELS_PER_MM)
    leading = font_metadata('leading', 5 * PIXELS_PER_MM)

    def render_text(self, text, variant=None):
        glyph_set = self.variants.get(variant, self.default_variant)

        nodes = []
        position = Point(0, 0)
        for line in text.splitlines():
            line = line.strip()
            for character in line:
                glyph = glyph_set[character]
                node = deepcopy(glyph.node)
                transform = "translate(%s, %s)" % position.as_tuple()
                glyph.set('transform', transform)
                nodes.append(node)
                position.x += self.kerning

            position.y += self.leading
            position.x = 0

        return nodes
