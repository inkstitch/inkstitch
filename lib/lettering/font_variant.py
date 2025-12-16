# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
from collections import defaultdict
from unicodedata import normalize, category

import inkex

from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SVG_GROUP_TAG,
                        SVG_PATH_TAG, SVG_USE_TAG)
from ..update import update_inkstitch_document
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
    LEFT_TO_RIGHT = ["→", "ltr"]
    RIGHT_TO_LEFT = ["←", "rtl"]
    TOP_TO_BOTTOM = ["↓", "ttb"]
    BOTTOM_TO_TOP = ["↑", "btt"]
    VARIANT_TYPES = (LEFT_TO_RIGHT[1], RIGHT_TO_LEFT[1], TOP_TO_BOTTOM[1], BOTTOM_TO_TOP[1])
    LEGACY_VARIANT_TYPES = (LEFT_TO_RIGHT[0], RIGHT_TO_LEFT[0], TOP_TO_BOTTOM[0], BOTTOM_TO_TOP[0])
    LEGACY_VARIANT_CONVERSION_DICT = {"ltr": "→", "rtl": "←", "ttb": "↓", "btt": "↑"}

    @classmethod
    def reversed_variant(cls, variant):
        if variant in cls.LEFT_TO_RIGHT:
            return cls.RIGHT_TO_LEFT[1]
        elif variant in cls.RIGHT_TO_LEFT:
            return cls.LEFT_TO_RIGHT[1]
        elif variant in cls.TOP_TO_BOTTOM:
            return cls.BOTTOM_TO_TOP[1]
        elif variant in cls.BOTTOM_TO_TOP:
            return cls.TOP_TO_BOTTOM[1]
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
        variant_file_paths = self._get_variant_file_paths()
        if not variant_file_paths:
            # need to check for legacy file names
            variant_file_paths = self._get_variant_file_paths(True)
        for svg_path in variant_file_paths:
            document = inkex.load_svg(svg_path)
            update_inkstitch_document(document, warn_unversioned=False)
            svg = document.getroot()
            svg = self._apply_transforms(svg)

            glyph_layers = svg.xpath(".//svg:g[starts-with(@inkscape:label, 'GlyphLayer-')]", namespaces=inkex.NSS)
            for layer in glyph_layers:
                self._clean_group(layer)
                layer.attrib[INKSCAPE_LABEL] = layer.attrib[INKSCAPE_LABEL].replace("GlyphLayer-", "", 1)
                glyph_name = normalize('NFC', layer.attrib[INKSCAPE_LABEL])
                try:
                    self.glyphs[glyph_name] = Glyph(layer)
                except (AttributeError, ValueError):
                    pass

    def _get_variant_file_paths(self, legacy=False):
        variant = self.variant
        if legacy:
            variant = self.LEGACY_VARIANT_CONVERSION_DICT[variant]

        file_paths = []
        direct_path = os.path.join(self.path, "%s.svg" % variant)
        if os.path.isfile(direct_path):
            file_paths.append(direct_path)
        elif os.path.isdir(os.path.join(self.path, "%s" % variant)):
            path = os.path.join(self.path, "%s" % self.variant)
            file_paths.extend([os.path.join(path, svg) for svg in os.listdir(path) if svg.endswith('.svg')])
        return file_paths

    def _clean_group(self, group):
        # We'll repurpose the layer as a container group labelled with the
        # glyph.
        del group.attrib[INKSCAPE_GROUPMODE]

        # The layer may be marked invisible, so we'll clear the 'display'
        # style and presentation attribute.
        group.style.pop('display', None)
        group.attrib.pop('display', None)

    def _apply_transforms(self, svg):
        self.clip_transforms = defaultdict(list)
        # apply transforms to paths and use tags
        for element in svg.iterdescendants((SVG_PATH_TAG, SVG_USE_TAG, SVG_GROUP_TAG)):
            transform = element.composed_transform()

            if element.clip is not None:
                self.clip_transforms[element.clip] = element.composed_transform()
            if element.tag == SVG_GROUP_TAG:
                continue
            if element.tag == SVG_PATH_TAG:
                path = element.path.transform(transform)
                element.set_path(path)
                element.attrib.pop("transform", None)
            elif element.tag == SVG_USE_TAG:
                oldx = element.get('x', 0)
                oldy = element.get('y', 0)
                newx, newy = transform.apply_to_point((oldx, oldy))
                element.set('x', newx)
                element.set('y', newy)
                element.attrib.pop("transform", None)

        for clip, transform in self.clip_transforms.items():
            for element in clip.iterdescendants():
                if element.tag == SVG_PATH_TAG:
                    path = element.path.transform(transform)
                    element.set_path(path)
                    element.attrib.pop("transform", None)

        # remove transforms after they have been applied
        for group in svg.iterdescendants(SVG_GROUP_TAG):
            group.attrib.pop('transform', None)

        return svg

    def glyphs_start_with(self, character):
        glyph_selection = [glyph_name for glyph_name, glyph_layer in self.glyphs.items() if glyph_name.startswith(character)]
        return sorted(glyph_selection, key=lambda glyph: (len(glyph.split('.')[0]), len(glyph)), reverse=True)

    def is_binding(self, character):
        # after  a non binding letter a letter can only be in isol or fina shape.
        # binding glyph only have  two shapes, isol and fina

        non_binding_char = ['ا', 'أ', 'ﺇ', 'آ', 'ٱ', 'د', 'ذ', 'ر', 'ز', 'و', 'ؤ']
        normalized_non_binding_char = [normalize('NFC', letter) for letter in non_binding_char]
        return not (character in normalized_non_binding_char)

    def is_mark(self, character):
        # this category includes all the combining diacritics.

        return (category(character)[0] == 'M')

    def is_letter(self, character):

        return (category(character)[0] == 'L')

    def get_glyph(self, character, word):
        """
        Returns the glyph for the given character, searching for combined glyphs first
        This expects glyph annotations to be within the given word, for example: a.init

        Returns glyph node and length of the glyph name
        """
        glyph_selection = self.glyphs_start_with(character)
        for glyph in glyph_selection:
            if word.startswith(glyph):
                return self.glyphs[glyph], len(glyph)
        return self.glyphs.get(self.default_glyph, None), 1

    def get_next_glyph_shape(self, word, starting, ending, previous_is_binding):
        # in arabic each letter (or ligature) may have up to 4 different shapes, hence 4 glyphs
        # this computes the shape of the glyph that represents word[starting:ending+1]

        # punctuation   or a combining accent is not really part of the word
        # they may appear at begining or end of words
        # computes where the actual word begins and ends up
        last_char_index = len(word)-1
        first_char_index = 0

        while not self.is_letter(word[last_char_index]):
            last_char_index = last_char_index - 1

        while not self.is_letter(word[first_char_index]):
            first_char_index = first_char_index + 1

        # first glyph is either isol or init depending if it is also the last glyph of the actual word
        if starting == first_char_index:
            if not self.is_binding(word[ending]) or len(word) == 1:
                shape = 'isol'
            else:
                shape = 'init'
        # last glyph  is  final if previous is binding, isol otherwise
        # a non binding  glyph behaves like the last glyph
        elif ending == last_char_index or not self.is_binding(word[ending]):
            if previous_is_binding:
                shape = 'fina'
            else:
                shape = 'isol'
        # in the middle of the actual word, the shape of a glyph is medi if previous glyph is binding,  init otherwise
        elif previous_is_binding:
            shape = 'medi'
        else:
            shape = 'init'

        return shape

    def get_next_glyph(self, word, i, previous_is_binding):
        # word[:i] has been processed, this function returns the glyph starting at word[i]
        # taking into acount the previous glyph binding status

        # find  all the glyphs in the font that start with first letter of the glyph
        glyph_selection = self.glyphs_start_with(word[i])

        # find the longest glyph that match
        for glyph in glyph_selection:
            glyph_name = glyph.split('.')
            if len(glyph_name) == 2 and glyph_name[1] in ['isol', 'init', 'medi', 'fina']:
                is_binding = self.is_binding(glyph_name[0][-1])
                if len(word) < i + len(glyph_name[0]):
                    continue
                shape = self.get_next_glyph_shape(word, i, i + len(glyph_name[0]) - 1, previous_is_binding)
                if glyph_name[1] == shape and word[i:].startswith(glyph_name[0]):
                    return self.glyphs[glyph], len(glyph_name[0]),  is_binding
            elif word[i:].startswith(glyph):
                if self.is_mark(word[i]):
                    return self.glyphs[glyph], len(glyph), previous_is_binding
                else:
                    return self.glyphs[glyph], len(glyph), True
        # nothing was found
        return self.glyphs.get(self.default_glyph, None), 1, True

    def __getitem__(self, character):
        if character in self.glyphs:
            return self.glyphs[character]
        else:
            return self.glyphs.get(self.default_glyph, None)

    def __contains__(self, character):
        return character in self.glyphs
