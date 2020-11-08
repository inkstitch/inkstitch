# -*- coding: UTF-8 -*-

import json
import os
from copy import deepcopy

from lxml import etree

from ..elements import nodes_to_elements
from ..exceptions import InkstitchException
from ..i18n import _, get_languages
from ..stitches.auto_satin import auto_satin
from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSCAPE_LABEL, SVG_GROUP_TAG, SVG_PATH_TAG
from ..utils import Point
from .font_variant import FontVariant


class FontError(InkstitchException):
    pass


def font_metadata(name, default=None, multiplier=None):
    def getter(self):
        value = self.metadata.get(name, default)

        if multiplier is not None:
            value *= multiplier

        return value

    return property(getter)


def localized_font_metadata(name, default=None):
    def getter(self):
        # If the font contains a localized version of the attribute, use it.
        for language in get_languages():
            attr = "%s_%s" % (name, language)
            if attr in self.metadata:
                return self.metadata.get(attr)

        if name in self.metadata:
            # This may be a font packaged with Ink/Stitch, in which case the
            # text will have been sent to CrowdIn for community translation.
            # Try to fetch the translated version.
            return _(self.metadata.get(name))
        else:
            return default

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
        self.metadata = {}
        self.license = None
        self.variants = {}

        self._load_metadata()
        self._load_license()

    def _load_metadata(self):
        try:
            with open(os.path.join(self.path, "font.json")) as metadata_file:
                self.metadata = json.load(metadata_file)
        except IOError:
            pass

    def _load_license(self):
        try:
            with open(os.path.join(self.path, "LICENSE"), encoding="utf-8") as license_file:
                self.license = license_file.read()
        except IOError:
            pass

    def _load_variants(self):
        if not self.variants:
            for variant in FontVariant.VARIANT_TYPES:
                try:
                    self.variants[variant] = FontVariant(self.path, variant, self.default_glyph)
                except IOError:
                    # we'll deal with missing variants when we apply lettering
                    pass

    def _check_variants(self):
        if self.variants.get(self.default_variant) is None:
            raise FontError("font not found or has no default variant")

    name = localized_font_metadata('name', '')
    description = localized_font_metadata('description', '')
    default_variant = font_metadata('default_variant', FontVariant.LEFT_TO_RIGHT)
    default_glyph = font_metadata('defalt_glyph', "�")
    letter_spacing = font_metadata('letter_spacing', 1.5, multiplier=PIXELS_PER_MM)
    leading = font_metadata('leading', 5, multiplier=PIXELS_PER_MM)
    word_spacing = font_metadata('word_spacing', 3, multiplier=PIXELS_PER_MM)
    kerning_pairs = font_metadata('kerning_pairs', {})
    auto_satin = font_metadata('auto_satin', True)
    min_scale = font_metadata('min_scale', 1.0)
    max_scale = font_metadata('max_scale', 1.0)

    @property
    def id(self):
        return os.path.basename(self.path)

    def render_text(self, text, destination_group, variant=None, back_and_forth=True, trim=False):
        """Render text into an SVG group element."""
        self._load_variants()

        if variant is None:
            variant = self.default_variant

        if back_and_forth:
            glyph_sets = [self.get_variant(variant), self.get_variant(FontVariant.reversed_variant(variant))]
        else:
            glyph_sets = [self.get_variant(variant)] * 2

        position = Point(0, 0)
        for i, line in enumerate(text.splitlines()):
            glyph_set = glyph_sets[i % 2]
            line = line.strip()

            letter_group = self._render_line(line, position, glyph_set)
            if glyph_set.variant == FontVariant.RIGHT_TO_LEFT:
                letter_group[:] = reversed(letter_group)
            destination_group.append(letter_group)

            position.x = 0
            position.y += self.leading

        if self.auto_satin and len(destination_group) > 0:
            self._apply_auto_satin(destination_group, trim)

        # set stroke width because it is almost invisible otherwise
        for element in destination_group.iterdescendants(SVG_PATH_TAG):
            style = ['stroke-width:0.5' if s.startswith('stroke-width') else s for s in element.get('style').split(';')]
            style = ';'.join(style)
            element.set('style', '%s' % style)

        return destination_group

    def get_variant(self, variant):
        return self.variants.get(variant, self.variants[self.default_variant])

    def _render_line(self, line, position, glyph_set):
        """Render a line of text.

        An SVG XML node tree will be returned, with an svg:g at its root.  If
        the font metadata requests it, Auto-Satin will be applied.

        Parameters:
            line -- the line of text to render.
            position -- Current position.  Will be updated to point to the spot
                        immediately after the last character.
            glyph_set -- a FontVariant instance.

        Returns:
            An svg:g element containing the rendered text.
        """
        group = etree.Element(SVG_GROUP_TAG, {
            INKSCAPE_LABEL: line
        })

        last_character = None
        for character in line:
            if character == " ":
                position.x += self.word_spacing
                last_character = None
            else:
                glyph = glyph_set[character] or glyph_set[self.default_glyph]

                if glyph is not None:
                    node = self._render_glyph(glyph, position, character, last_character)
                    group.append(node)

                last_character = character

        return group

    def _render_glyph(self, glyph, position, character, last_character):
        """Render a single glyph.

        An SVG XML node tree will be returned, with an svg:g at its root.

        Parameters:
            glyph -- a Glyph instance
            position -- Current position.  Will be updated based on the width
                        of this character and the letter spacing.
            character -- the current Unicode character.
            last_character -- the previous character in the line, or None if
                              we're at the start of the line or a word.
        """

        node = deepcopy(glyph.node)

        if last_character is not None:
            position.x += self.letter_spacing + self.kerning_pairs.get(last_character + character, 0) * PIXELS_PER_MM

        transform = "translate(%s, %s)" % position.as_tuple()
        node.set('transform', transform)
        position.x += glyph.width

        return node

    def _apply_auto_satin(self, group, trim):
        """Apply Auto-Satin to an SVG XML node tree with an svg:g at its root.

        The group's contents will be replaced with the results of the auto-
        satin operation.  Any nested svg:g elements will be removed.
        """

        elements = nodes_to_elements(group.iterdescendants(SVG_PATH_TAG))
        auto_satin(elements, preserve_order=True, trim=trim)
