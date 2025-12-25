# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import unicodedata
from collections import defaultdict
from copy import deepcopy
from random import randint

import inkex

from ..commands import add_commands, ensure_command_symbols
from ..elements import SatinColumn, Stroke, nodes_to_elements
from ..exceptions import InkstitchException
from ..extensions.lettering_custom_font_dir import get_custom_font_dir
from ..i18n import _, get_languages
from ..marker import ensure_marker_symbols, has_marker, is_grouped_with_marker
from ..stitches.auto_satin import auto_satin
from ..svg import PIXELS_PER_MM
from ..svg.clip import get_clips
from ..svg.tags import (CONNECTION_END, CONNECTION_START, EMBROIDERABLE_TAGS,
                        INKSCAPE_LABEL, INKSTITCH_ATTRIBS, SVG_GROUP_TAG,
                        SVG_PATH_TAG)
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

    def __init__(self, font_path, show_font_path_warning=True):
        self.path = font_path
        self.metadata = {}
        self.license = None
        self.variants = {}

        self._load_metadata(show_font_path_warning)
        self._load_license()

    def _load_metadata(self, show_font_path_warning=True):
        try:
            with open(os.path.join(self.path, "font.json"), encoding="utf-8-sig") as metadata_file:
                self.metadata = json.load(metadata_file)
        except IOError:
            if not show_font_path_warning:
                return
            path = os.path.join(self.path, "font.json")
            msg = _("JSON file missing. Expected a JSON file at the following location:")
            msg += f"\n{path}\n\n"
            msg += _("Generate the JSON file through:\nExtensions > Ink/Stitch > Font Management > Generate JSON...")
            msg += '\n\n'
            inkex.errormsg(msg)
        except json.decoder.JSONDecodeError as exception:
            if not show_font_path_warning:
                return
            path = os.path.join(self.path, "font.json")
            msg = _("Corrupt JSON file")
            msg += f" ({exception}):\n{path}\n\n"
            msg += _("Regenerate the JSON file through:\nExtensions > Ink/Stitch > Font Management > Generate JSON...")
            msg += '\n\n'
            inkex.errormsg(msg)

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

    name = font_metadata('name', '')
    description = localized_font_metadata('description', '')
    font_license = font_metadata('license', 'SIL Open Font License v1.1')
    keywords = font_metadata('keywords', '')
    original_font = font_metadata('original_font', '')
    original_font_url = font_metadata('original_font_url', '')
    text_direction = font_metadata('text_direction', 'ltr')
    letter_case = font_metadata('letter_case', '')
    default_glyph = font_metadata('default_glyph', "�")
    leading = font_metadata('leading', 100)
    kerning_pairs = font_metadata('kerning_pairs', {})
    auto_satin = font_metadata('auto_satin', True)
    min_scale = font_metadata('min_scale', 1.0)
    max_scale = font_metadata('max_scale', 1.0)
    size = font_metadata('size', 0)
    available_glyphs = font_metadata('glyphs', [])
    json_variant = font_metadata('default_variant', FontVariant.LEFT_TO_RIGHT[1])

    @property
    def json_default_variant(self):
        variant = self.json_variant
        if variant in FontVariant.LEGACY_VARIANT_TYPES:
            index = FontVariant.LEGACY_VARIANT_TYPES.index(variant)
            variant = FontVariant.VARIANT_TYPES[index]
        return variant

    # use values from SVG Font, example:
    # <font horiz-adv-x="45" ...  <glyph .... horiz-adv-x="49" glyph-name="A" /> ... <hkern ... k="3"g1="A" g2="B" /> .... />

    # Example font.json : "horiz_adv_x": {"A":49},
    horiz_adv_x = font_metadata('horiz_adv_x', {})

    # Example font.json : "horiz_adv_x_default" : 45,
    horiz_adv_x_default = font_metadata('horiz_adv_x_default')

    # Define by <glyph glyph-name="space" unicode=" " horiz-adv-x="22" />, Example font.json : "horiz_adv_x_space":22,
    word_spacing = font_metadata('horiz_adv_x_space', 20)

    reversible = font_metadata('reversible', True)
    sortable = font_metadata('sortable', False)
    combine_at_sort_indices = font_metadata('combine_at_sort_indices', [])

    @property
    def id(self):
        return os.path.basename(self.path)

    @property
    def default_variant(self):
        # Set default variant to any existing variant if default font file is missing
        default_variant = self.json_default_variant
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
        for variant, legacy_variant in zip(FontVariant.VARIANT_TYPES, FontVariant.LEGACY_VARIANT_TYPES):
            if self._has_variant(variant) or self._has_variant(legacy_variant):
                font_variants.append(variant)
        if not font_variants:
            # still no variants, raise FontError
            raise FontError(_("The font '%s' has no variants.") % self.name)
        return font_variants

    def _has_variant(self, variant):
        if (os.path.isfile(os.path.join(self.path, "%s.svg" % variant)) or (
                os.path.isdir(os.path.join(self.path, "%s" % variant)) and
                [svg for svg in os.listdir(os.path.join(self.path, "%s" % variant)) if svg.endswith('.svg')])):
            return True
        else:
            return False

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
        custom_dir = get_custom_font_dir()
        if not custom_dir:
            return False
        return custom_dir in self.path

    def render_text(self, text, destination_group, variant=None, back_and_forth=True,  # noqa: C901
                    trim_option=0, use_trim_symbols=False, color_sort=0, text_align=0,
                    letter_spacing=0, word_spacing=0, line_height=0):

        """Render text into an SVG group element."""
        self._load_variants()

        # Normalize the text in the same way that glyph names are normalized (NFC)
        text = unicodedata.normalize('NFC', text)

        if variant is None:
            variant = self.default_variant

        if back_and_forth and self.reversible:
            glyph_sets = [self.get_variant(variant), self.get_variant(FontVariant.reversed_variant(variant))]
        else:
            glyph_sets = [self.get_variant(variant)] * 2

        max_line_width = 0
        position = Point(0, 0)
        for i, line in enumerate(text.splitlines()):
            glyph_set = glyph_sets[i % 2]
            line = line.strip()

            if self.text_direction == "rtl":
                line = line[::-1]

            letter_group = self._render_line(destination_group, line, position, glyph_set, i, letter_spacing, word_spacing)
            if ((variant in FontVariant.LEFT_TO_RIGHT and back_and_forth and self.reversible and i % 2 == 1) or
                    (variant in FontVariant.RIGHT_TO_LEFT and not (back_and_forth and self.reversible and i % 2 == 1))):
                letter_group[:] = reversed(letter_group)
                for group in letter_group:
                    group[:] = reversed(group)

            position.x = 0
            position.y += self.leading + line_height * PIXELS_PER_MM

            # We need to insert the destination_group now, even though it is possibly empty
            # otherwise we could run into a FragmentError in case a glyph contains commands
            destination_group.append(letter_group)
            bounding_box = None
            try:
                bounding_box = letter_group.bounding_box()
            except AttributeError:
                # letter group is None
                continue
            # remove destination_group if it is empty
            if not bounding_box:
                letter_group.delete()
                continue

            line_width = bounding_box.width
            max_line_width = max(max_line_width, line_width)
            # text_align 0: left (default)
            if text_align == 1:
                # 1: align center
                letter_group.transform = f'translate({-line_width/2}, 0)'
            if text_align == 2:
                # 2: align right
                letter_group.transform = f'translate({-line_width}, 0)'

        if text_align in [3, 4]:
            # 3: Block (default) 4: Block (letterspacing)
            for line_group in destination_group.iterchildren():
                if text_align == 4 and len(line_group) == 1:
                    line_group = line_group[0]
                if len(line_group) > 1:
                    try:
                        distance = max_line_width - line_group.bounding_box().width
                    except AttributeError:
                        # line group bounding_box is None
                        continue
                    distance_per_space = distance / (len(line_group) - 1)
                    for i, word in enumerate(line_group.getchildren()[1:]):
                        transform = word.transform
                        translate = distance_per_space * (i + 1)
                        transform.add_translate(translate, 0)

        if self.auto_satin and len(destination_group) > 0:
            self._apply_auto_satin(destination_group)

        self._set_style(destination_group)

        # add trims
        self._add_trims(destination_group, text, trim_option, use_trim_symbols, back_and_forth, color_sort)
        # make sure necessary marker and command symbols are in the defs section
        ensure_command_symbols(destination_group)
        ensure_marker_symbols(destination_group)

        if color_sort != 0 and self.sortable:
            self.do_color_sort(destination_group, color_sort)

        return destination_group

    def _set_style(self, destination_group):
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

    def get_variant(self, variant):
        return self.variants.get(variant, self.variants[self.default_variant])

    def _render_line(self, destination_group, line, position, glyph_set, line_number, letter_spacing=0, word_spacing=0):
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

        group = inkex.Group()
        group.label = line
        if self.text_direction == 'rtl':
            group.label = line[::-1]
        group.set("inkstitch:letter-group", "line")
        last_character = None

        words = line.split(" ")
        for i, word in enumerate(words):

            word_group = inkex.Group()
            label = word
            if self.text_direction == 'rtl':
                label = word[::-1]
            word_group.label = label
            word_group.set("inkstitch:letter-group", "word")

            if self.text_direction == 'rtl':
                glyphs = self._get_word_glyphs(glyph_set, word[::-1])
                glyphs = glyphs[::-1]
            else:
                glyphs = self._get_word_glyphs(glyph_set, word)

            last_character = None
            for j, glyph in enumerate(glyphs):
                if glyph is None:
                    position.x += self.word_spacing
                    last_character = None
                    continue
                node = self._render_glyph(destination_group, glyph, position, glyph.name, last_character, f'{line_number}-{i}-{j}', letter_spacing)
                word_group.append(node)
                last_character = glyph.name
            group.append(word_group)
            position.x += self.word_spacing + word_spacing * PIXELS_PER_MM
        return group

    def _get_word_glyphs(self, glyph_set, word):
        glyphs = []
        skip = []
        previous_is_binding = True

        # forced letter case
        if self.letter_case == "upper":
            word = word.upper()
        elif self.letter_case == "lower":
            word = word.lower()

        for i, character in enumerate(word):
            if i in skip:
                continue

            glyph, glyph_len, binding = glyph_set.get_next_glyph(word, i, previous_is_binding)
            previous_is_binding = binding

            skip = list(range(i, i+glyph_len))

            if glyph is None and self.default_glyph == " ":
                glyphs.append(None)
            else:
                if glyph is None:
                    glyphs.append(glyph_set[self.default_glyph])
                if glyph is not None:
                    glyphs.append(glyph)

        return glyphs

    def _render_glyph(self, destination_group, glyph, position, character, last_character, id_extension, letter_spacing=0):
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
            if self.text_direction != "rtl":
                kerning = self.kerning_pairs.get(f'{last_character} {character}', None)
                if kerning is None:
                    # legacy kerning without space
                    kerning = self.kerning_pairs.get(last_character + character, 0)
                position.x += glyph.min_x - kerning + letter_spacing * PIXELS_PER_MM
            else:
                kerning = self.kerning_pairs.get(f'{character} {last_character}', None)
                if kerning is None:
                    # legacy kerning without space
                    kerning = self.kerning_pairs.get(character + last_character, 0)
                position.x += glyph.min_x - kerning + letter_spacing * PIXELS_PER_MM

        transform = "translate(%s, %s)" % position.as_tuple()
        node.set('transform', transform)

        horiz_adv_x_default = self.horiz_adv_x_default
        if horiz_adv_x_default is None:
            horiz_adv_x_default = glyph.width + glyph.min_x

        position.x += self.horiz_adv_x.get(character, horiz_adv_x_default) - glyph.min_x

        self._update_commands(node, glyph, id_extension)
        self._update_clips(destination_group, node, glyph)

        # this is used to recognize a glyph layer later in the process
        # because this is not unique it will be overwritten by inkscape when inserted into the document
        node.set("id", "glyph")
        node.set("inkstitch:letter-group", "glyph")
        # force inkscape to show a label when the glyph is only a non-spacing mark
        if len(node.label) == 1 and unicodedata.category(node.label) == 'Mn':
            # force inkscape to show a label when the glyph is only a non-spacing mark
            node.label = ' ' + node.label
        return node

    def _update_commands(self, node, glyph, id_extension=""):
        for element, connectors in glyph.commands.items():
            # update element
            el = node.find(".//*[@id='%s']" % element)
            # we cannot get a unique id from the document at this point
            # so let's create a random id which will most probably work as well
            new_element_id = f'{element}-{id_extension}-{randint(0, 9999)}'
            el.set_id(new_element_id)
            for connector, symbol in connectors:
                # update symbol
                new_symbol_id = f'{symbol}-{id_extension}-{randint(0, 9999)}'
                s = node.find(".//*[@id='%s']" % symbol)
                s.set_id(new_symbol_id)
                # update connector
                c = node.find(".//*[@id='%s']" % connector)
                c.set(CONNECTION_END, "#%s" % new_element_id)
                c.set(CONNECTION_START, "#%s" % new_symbol_id)

    def _update_clips(self, destination_group, node, glyph):
        svg = destination_group.getroottree().getroot()
        for node_id, clip in glyph.clips.items():
            if clip not in svg.defs:
                svg.defs.append(clip)
            el = node.find(f".//*[@id='{node_id}']")
            el.clip = clip

    def _add_trims(self, destination_group, text, trim_option, use_trim_symbols, back_and_forth, color_sort):
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
            if not group.get("id", "").startswith("glyph"):
                continue

            i += 1
            while i in space_indices + line_break_indices:
                i += 1

            # letter
            if trim_option == 3:
                self._process_trim(group, use_trim_symbols, color_sort)
            # word
            elif trim_option == 2 and i+1 in space_indices + line_break_indices:
                self._process_trim(group, use_trim_symbols, color_sort)
            # line
            elif trim_option == 1 and i+1 in line_break_indices:
                self._process_trim(group, use_trim_symbols, color_sort)

    def _process_trim(self, group, use_trim_symbols, color_sort):
        if color_sort != 0 and self.sortable:
            elements = defaultdict(list)
            for path_child in group.iterdescendants(EMBROIDERABLE_TAGS):
                if not has_marker(path_child):
                    sort_index = path_child.get('inkstitch:color_sort_index', None)
                    if sort_index is not None:
                        elements[sort_index] = path_child
                    else:
                        elements[404] = path_child
            for value in elements.values():
                self._add_trim_to_element(Stroke(value), use_trim_symbols)
        else:
            nodes = list(group.iterdescendants(EMBROIDERABLE_TAGS))[::-1]
            # find the last path that does not carry a marker or belongs to a visual command and add a trim there
            for path_child in nodes:
                if has_marker(path_child) or path_child.get_id().startswith('command_connector'):
                    continue
                element = Stroke(path_child)
                self._add_trim_to_element(element, use_trim_symbols)
                break

    def _add_trim_to_element(self, element, use_trim_symbols):
        if element.shape:
            element_id = "%s_%s" % (element.node.get('id'), randint(0, 9999))
            element.node.set("id", element_id)
            if use_trim_symbols is False:
                element.node.set(INKSTITCH_ATTRIBS['trim_after'], 'true')
            else:
                add_commands(element, ['trim'])

    def _apply_auto_satin(self, group):
        """Apply Auto-Satin to an SVG XML node tree with an svg:g at its root.

        The group's contents will be replaced with the results of the auto-
        satin operation.  Any nested svg:g elements will be removed.
        """

        elements = nodes_to_elements(group.iterdescendants(EMBROIDERABLE_TAGS))
        elements = [element for element in elements if isinstance(element, SatinColumn) or isinstance(element, Stroke)]

        if elements and any(isinstance(element, SatinColumn) for element in elements):
            auto_satin(elements, preserve_order=True, trim=False)

    def do_color_sort(self, group, color_sort):
        """Sort elements by their color sort index as defined by font author"""

        if color_sort == 1:
            # Whole text
            self._color_sort_group(group, 'line')
        elif color_sort == 2:
            # per line
            groups = group.getchildren()
            for group in groups:
                self._color_sort_group(group, 'word')
        elif color_sort == 3:
            # per word
            line_groups = group.getchildren()
            for line_group in line_groups:
                for group in line_group.iterchildren():
                    self._color_sort_group(group, 'glyph')

    def _color_sort_group(self, group, transform_key):
        elements_by_color = self._get_color_sorted_elements(group, transform_key)

        # there are no sort indexes defined, abort color sorting and return to normal
        if not elements_by_color:
            return

        group.remove_all()
        for index, grouped_elements in sorted(elements_by_color.items()):
            color_group = inkex.Group(attrib={
                INKSCAPE_LABEL: _("Color Group") + f' {index}'
            })

            # combined indices
            if index in self.combine_at_sort_indices:
                path = ""
                for element_list in grouped_elements:
                    for element in element_list:
                        path += element.get("d", "")
                grouped_elements[0][0].set("d", path)
                if grouped_elements[0][0].get("inkstitch:fill_method", False) in ['tartan_fill', 'linear_gradient_fill']:
                    grouped_elements[0][0].set('inkstitch:stop_at_ending_point', True)
                color_group.append(grouped_elements[0][0])
                group.append(color_group)
                continue

            # everything else, create marker groups if applicable
            for element_list in grouped_elements:
                if len(element_list) == 1:
                    color_group.append(element_list[0])
                    continue
                elements_group = inkex.Group()
                for element in element_list:
                    elements_group.append(element)
                color_group.append(elements_group)

            group.append(color_group)

    def _get_color_sorted_elements(self, group, transform_key):  # noqa: C901
        elements_by_color = defaultdict(list)
        last_parent = None

        for element in group.iterdescendants(EMBROIDERABLE_TAGS, SVG_GROUP_TAG):
            sort_index = element.get('inkstitch:color_sort_index', None)

            # Skip command connectors, we only aim for command groups
            # Skip command connectors as well, they will be included with the command group
            if (element.TAG == 'g' and not element.get_id().startswith('command_group')
                    or element.get_id().startswith('command_connector')):
                continue

            clips = get_clips(element)
            if len(clips) > 1:
                # multiple clips: wrap the element into clipped groups
                parent = element.getparent()
                index = parent.index(element)
                for clip in clips:
                    new_group = inkex.Group()
                    new_group.clip = clip
                    parent.insert(index, new_group)
                    new_group.append(element)
                    element = new_group
            elif len(clips) == 1:
                # only one clip: we can apply the clip directly to the element
                element.clip = clips[0]

            # get glyph group to calculate transform
            glyph_group = None
            for ancestor in element.ancestors(group):
                if ancestor.get("inkstitch:letter-group", '') == transform_key:
                    glyph_group = ancestor
                    break
            if glyph_group is None:
                # this should never happen
                continue

            element.transform = element.composed_transform(glyph_group.getparent())
            if sort_index is not None and int(sort_index) in self.combine_at_sort_indices:
                element.apply_transform()

            if not sort_index:
                elements_by_color[404].append([element])
                continue

            if element.get_id().startswith('command_group'):
                elements_by_color[int(sort_index)].append([element])
                continue

            parent = element.getparent()
            if element.clip is None and parent.clip is not None:
                element.clip = parent.clip
            if last_parent != parent or int(sort_index) not in elements_by_color or not is_grouped_with_marker(element):
                elements_by_color[int(sort_index)].append([element])
            else:
                elements_by_color[int(sort_index)][-1].append(element)
            last_parent = parent
        return elements_by_color
