# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
from copy import deepcopy
from random import randint

import inkex

from ..commands import add_commands, ensure_symbol
from ..elements import FillStitch, SatinColumn, Stroke, nodes_to_elements
from ..exceptions import InkstitchException
from ..extensions.lettering_custom_font_dir import get_custom_font_dir
from ..i18n import _, get_languages
from ..marker import MARKER, ensure_marker, has_marker
from ..stitches.auto_satin import auto_satin
from ..svg.tags import (CONNECTION_END, CONNECTION_START, EMBROIDERABLE_TAGS,
                        INKSCAPE_LABEL, SVG_GROUP_TAG, SVG_PATH_TAG,
                        SVG_USE_TAG, XLINK_HREF)
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
            original_metadata = self.metadata.get(name)
            localized_metadata = ""
            if original_metadata != "":
                localized_metadata = _(original_metadata)
            return localized_metadata
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
            with open(os.path.join(self.path, "font.json"), encoding="utf-8-sig") as metadata_file:
                self.metadata = json.load(metadata_file)
        except IOError:
            pass

    def _load_license(self):
        try:
            with open(os.path.join(self.path, "LICENSE"), encoding="utf-8-sig") as license_file:
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

    name = localized_font_metadata('name', '')
    description = localized_font_metadata('description', '')
    letter_case = font_metadata('letter_case', '')
    default_glyph = font_metadata('default_glyph', "�")
    leading = font_metadata('leading', 100)
    kerning_pairs = font_metadata('kerning_pairs', {})
    auto_satin = font_metadata('auto_satin', True)
    min_scale = font_metadata('min_scale', 1.0)
    max_scale = font_metadata('max_scale', 1.0)
    size = font_metadata('size', 0)

    # use values from SVG Font, example:
    # <font horiz-adv-x="45" ...  <glyph .... horiz-adv-x="49" glyph-name="A" /> ... <hkern ... k="3"g1="A" g2="B" /> .... />

    # Example font.json : "horiz_adv_x": {"A":49},
    horiz_adv_x = font_metadata('horiz_adv_x', {})

    # Example font.json : "horiz_adv_x_default" : 45,
    horiz_adv_x_default = font_metadata('horiz_adv_x_default')

    # Define by <glyph glyph-name="space" unicode=" " horiz-adv-x="22" />, Example font.json : "horiz_adv_x_space":22,
    word_spacing = font_metadata('horiz_adv_x_space', 20)

    reversible = font_metadata('reversible', True)

    @property
    def id(self):
        return os.path.basename(self.path)

    @property
    def default_variant(self):
        # Set default variant to any existing variant if default font file is missing
        default_variant = font_metadata('default_variant', FontVariant.LEFT_TO_RIGHT)
        font_variants = self.has_variants()
        if default_variant not in font_variants and len(font_variants) > 0:
            default_variant = font_variants[0]
        return default_variant

    @property
    def preview_image(self):
        preview_image_path = os.path.join(self.path, "preview.png")
        if os.path.isfile(preview_image_path):
            return preview_image_path
        return None

    def has_variants(self):
        # returns available variants
        font_variants = []
        for variant in FontVariant.VARIANT_TYPES:
            if os.path.isfile(os.path.join(self.path, "%s.svg" % variant)):
                font_variants.append(variant)
        if not font_variants:
            raise FontError(_("The font '%s' has no variants.") % self.name)
        return font_variants

    @property
    def marked_custom_font_id(self):
        if not self.is_custom_font():
            return self.id
        else:
            return self.id + '*'

    @property
    def marked_custom_font_name(self):
        if not self.is_custom_font():
            return self.name
        else:
            return self.name + '*'

    def is_custom_font(self):
        return get_custom_font_dir() in self.path

    def render_text(self, text, destination_group, variant=None, back_and_forth=True, trim_option=0):

        """Render text into an SVG group element."""
        self._load_variants()

        if variant is None:
            variant = self.default_variant

        if back_and_forth and self.reversible:
            glyph_sets = [self.get_variant(variant), self.get_variant(FontVariant.reversed_variant(variant))]
        else:
            glyph_sets = [self.get_variant(variant)] * 2

        position = Point(0, 0)
        for i, line in enumerate(text.splitlines()):
            glyph_set = glyph_sets[i % 2]
            line = line.strip()

            letter_group = self._render_line(line, position, glyph_set)
            if back_and_forth and self.reversible and i % 2 == 1:
                letter_group[:] = reversed(letter_group)
            destination_group.append(letter_group)

            position.x = 0
            position.y += self.leading

        if self.auto_satin and len(destination_group) > 0:
            self._apply_auto_satin(destination_group)

        # make sure font stroke styles have always a similar look
        for element in destination_group.iterdescendants(SVG_PATH_TAG):
            style = inkex.Style(element.get('style'))
            if style.get('fill') == 'none':
                style += inkex.Style("stroke-width:1px")
                if style.get('stroke-dasharray') and style.get('stroke-dasharray') != 'none':
                    style += inkex.Style("stroke-dasharray:3, 1")
                    # Set a smaller width to auto-route running stitches
                    if self.auto_satin or element.get_id().startswith("autosatinrun"):
                        style += inkex.Style("stroke-width:0.5px")
                element.set('style', '%s' % style.to_str())

        # add trims
        self._add_trims(destination_group, text, trim_option, back_and_forth)
        # make sure necessary marker and command symbols are in the defs section
        self._ensure_command_symbols(destination_group)
        self._ensure_marker_symbols(destination_group)

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

        group = inkex.Group(attrib={
            INKSCAPE_LABEL: line
        })

        last_character = None
        for character in line:
            if self.letter_case == "upper":
                character = character.upper()
            elif self.letter_case == "lower":
                character = character.lower()

            glyph = glyph_set[character]

            if character == " " or (glyph is None and self.default_glyph == " "):
                position.x += self.word_spacing
                last_character = None
            else:
                if glyph is None:
                    glyph = glyph_set[self.default_glyph]

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

        # Concerning min_x: I add it before moving the letter because it is to
        # take into account the margin in the drawing of the letter. With respect
        # to point 0 the letter can start at 5 or -5. The letters have a defined
        # place in the drawing that's important.
        # Then to calculate the position of x for the next letter I have to remove
        # the min_x margin because the horizontal adv is calculated from point 0 of the drawing.

        node = deepcopy(glyph.node)
        if last_character is not None:
            position.x += glyph.min_x - self.kerning_pairs.get(last_character + character, 0)

        transform = "translate(%s, %s)" % position.as_tuple()
        node.set('transform', transform)

        horiz_adv_x_default = self.horiz_adv_x_default
        if horiz_adv_x_default is None:
            horiz_adv_x_default = glyph.width + glyph.min_x

        position.x += self.horiz_adv_x.get(character, horiz_adv_x_default) - glyph.min_x

        self._update_commands(node, glyph)

        # this is used to recognize a glyph layer later in the process
        # because this is not unique it will be overwritten by inkscape when inserted into the document
        node.set("id", "glyph")

        return node

    def _update_commands(self, node, glyph):
        for element, connectors in glyph.commands.items():
            # update element
            el = node.find(".//*[@id='%s']" % element)
            # we cannot get a unique id from the document at this point
            # so let's create a random id which will most probably work as well
            new_element_id = "%s_%s" % (element, randint(0, 9999))
            el.set_id(new_element_id)
            for connector, symbol in connectors:
                # update symbol
                new_symbol_id = "%s_%s" % (symbol, randint(0, 9999))
                s = node.find(".//*[@id='%s']" % symbol)
                s.set_id(new_symbol_id)
                # update connector
                c = node.find(".//*[@id='%s']" % connector)
                c.set(CONNECTION_END, "#%s" % new_element_id)
                c.set(CONNECTION_START, "#%s" % new_symbol_id)

    def _add_trims(self, destination_group, text, trim_option, back_and_forth):
        """
        trim_option == 0  --> no trims
        trim_option == 1  --> trim at the end of each line
        trim_option == 2  --> trim after each word
        trim_option == 3  --> trim after each letter
        """
        if trim_option == 0:
            return

        # reverse every second line of text if back and forth is true and strip spaces
        text = text.splitlines()
        text = [t[::-1].strip() if i % 2 != 0 and back_and_forth else t.strip() for i, t in enumerate(text)]
        text = "\n".join(text)

        i = -1
        space_indices = [i for i, t in enumerate(text) if t == " "]
        line_break_indices = [i for i, t in enumerate(text) if t == "\n"]
        for group in destination_group.iterdescendants(SVG_GROUP_TAG):
            # make sure we are only looking at glyph groups
            if group.get("id") != "glyph":
                continue

            i += 1
            while i in space_indices + line_break_indices:
                i += 1

            # letter
            if trim_option == 3:
                self._process_trim(group)
            # word
            elif trim_option == 2 and i+1 in space_indices + line_break_indices:
                self._process_trim(group)
            # line
            elif trim_option == 1 and i+1 in line_break_indices:
                self._process_trim(group)

    def _process_trim(self, group):
        # find the last path that does not carry a marker and add a trim there
        for path_child in group.iterdescendants(EMBROIDERABLE_TAGS):
            if not has_marker(path_child):
                path = path_child
        if path.get('style') and "fill" in path.get('style'):
            element = FillStitch(path)
        else:
            element = Stroke(path)

        if element.shape:
            element_id = "%s_%s" % (element.node.get('id'), randint(0, 9999))
            element.node.set("id", element_id)
            add_commands(element, ['trim'])

    def _ensure_command_symbols(self, group):
        # collect commands
        commands = set()
        for element in group.iterdescendants(SVG_USE_TAG):
            xlink = element.get(XLINK_HREF, ' ')
            if xlink.startswith('#inkstitch_'):
                commands.add(xlink[11:])
        # make sure all necessary command symbols are in the document
        for command in commands:
            ensure_symbol(group.getroottree().getroot(), command)

    def _ensure_marker_symbols(self, group):
        for marker in MARKER:
            xpath = ".//*[contains(@style, 'marker-start:url(#inkstitch-%s-marker')]" % marker
            marked_elements = group.xpath(xpath, namespaces=inkex.NSS)
            if marked_elements:
                ensure_marker(group.getroottree().getroot(), marker)
                for element in marked_elements:
                    element.style['marker-start'] = "url(#inkstitch-%s-marker)" % marker

    def _apply_auto_satin(self, group):
        """Apply Auto-Satin to an SVG XML node tree with an svg:g at its root.

        The group's contents will be replaced with the results of the auto-
        satin operation.  Any nested svg:g elements will be removed.
        """

        elements = nodes_to_elements(group.iterdescendants(SVG_PATH_TAG))
        elements = [element for element in elements if isinstance(element, SatinColumn) or isinstance(element, Stroke)]

        if elements:
            auto_satin(elements, preserve_order=True, trim=False)
