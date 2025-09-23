# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from math import atan2, degrees

from inkex import Transform, errormsg
from inkex.units import convert_unit

from ..elements import Stroke
from ..i18n import _
from ..lettering import get_font_by_id
from ..svg import get_correction_transform
from ..svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_LETTERING, SVG_GROUP_TAG
from ..utils import DotDict
from ..utils import Point as InkstitchPoint
from .base import InkstitchExtension


class LetteringAlongPath(InkstitchExtension):
    '''
    This extension aligns an Ink/Stitch Lettering group along a path
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-p", "--text-position", type=str, default='left', dest="text_position")

    def effect(self):
        # we ignore everything but the first path/text
        text, path = self.get_selection()
        if text is None or path is None:
            errormsg(_("Please select one path and one Ink/Stitch lettering group."))
            return

        TextAlongPath(self.svg, text, path, self.options.text_position)

    def get_selection(self):
        groups = list()
        paths = list()

        for node in self.svg.selection:
            lettering = False
            if node.tag == SVG_GROUP_TAG and INKSTITCH_LETTERING in node.attrib:
                groups.append(node)
                lettering = True
                continue

            for group in node.iterancestors(SVG_GROUP_TAG):
                if INKSTITCH_LETTERING in group.attrib:
                    groups.append(group)
                    lettering = True
                    break

            if not lettering and node.tag in EMBROIDERABLE_TAGS:
                paths.append(node)

        if not groups or not paths:
            return [None, None]

        return [groups[0], paths[0]]


class TextAlongPath:
    '''
    Aligns an Ink/Stitch Lettering group along a path
    '''
    def __init__(self, svg, text, path, text_position):
        self.svg = svg
        self.text = text
        self.path = Stroke(path).as_multi_line_string().geoms[0]
        self.text_position = text_position

        self.glyphs = [glyph for glyph in self.text.iterdescendants(SVG_GROUP_TAG) if glyph.get('inkstitch:letter-group', '') == 'glyph']
        if not self.glyphs:
            errormsg(_("The text doesn't contain any glyphs."))
            return

        self.load_settings()
        self.font = get_font_by_id(self.settings.font, False)
        if self.font is None:
            errormsg(_("Couldn't identify the font specified in the lettering group."))
            return

        self.font_scale = self.settings.scale / 100
        self._reset_glyph_transforms()

        hidden_commands = self.hide_commands()
        self.glyphs_along_path()
        self.restore_commands(hidden_commands)

    def _reset_glyph_transforms(self):
        # reset text transforms
        self.text.set('transform', get_correction_transform(self.text))

        if self.font is not None:
            try:
                text_group = list(self.text.iterchildren(SVG_GROUP_TAG))[0]
                text_group.set('transform', f'scale({self.font_scale})')
            except IndexError:
                pass
            for glyph in text_group.iterchildren():
                glyph.delete()
            rendered_text = self.font.render_text(
                self.settings.text,
                text_group,
                None,  # we don't know the font variant (?)
                self.settings.back_and_forth,
                self.settings.trim_option,
                self.settings.use_trim_symbols
            )
            self.glyphs = [glyph for glyph in rendered_text.iterdescendants(SVG_GROUP_TAG) if glyph.get('inkstitch:letter-group', '') == 'glyph']
            self.bake_transforms_recursively(text_group)

    def bake_transforms_recursively(self, element):
        '''applies transforms of the text group to the glyph group'''
        for child in element:
            child.transform = element.transform @ child.transform
            if child.tag == SVG_GROUP_TAG and not child.get('inkstitch:letter-group', '') == 'glyph':
                self.bake_transforms_recursively(child)
        element.transform = None

    def glyphs_along_path(self):
        path = self.path
        for i, text_line in enumerate(self.text.getchildren()[0].iterchildren()):
            self.transform_glyphs(path, text_line, i)

            # offset path for the next line
            line_offset = self.font.leading * self.font_scale
            path = path.offset_curve(line_offset)

    def transform_glyphs(self, path, line, iterator):
        text_width = line.bounding_box().width
        text_baseline = line.bounding_box().bottom
        backwards = self.settings.back_and_forth and iterator % 1 == 1

        if self.text_position == 'stretch':
            num_spaces = len(line) - 1

            line_glyphs = [glyph for glyph in line.iterdescendants(SVG_GROUP_TAG) if glyph.get('inkstitch:letter-group', '') == 'glyph']
            total_stretch_spaces = len(line_glyphs) - 1 + num_spaces

            stretch_space = (path.length - text_width) / total_stretch_spaces
        else:
            stretch_space = 0

        start_position = self.get_start_position(text_width, path.length)
        distance = start_position
        old_bbox = None

        words = line.getchildren()
        if backwards:
            words.reverse()
        if self.font.text_direction == "rtl":
            words.reverse()
        for word in words:
            glyphs = word.getchildren()
            if backwards:
                glyphs.reverse()
            if self.font.text_direction == "rtl":
                glyphs.reverse()
            for glyph in glyphs:
                # dimensions
                bbox = glyph.bounding_box()
                transformed_bbox = glyph.bounding_box(word.composed_transform())
                left = bbox.left
                transformed_left = transformed_bbox.left
                width = convert_unit(transformed_bbox.width, 'px', self.svg.unit)

                # adjust position
                if old_bbox:
                    distance += convert_unit(transformed_left - old_bbox.right, 'px', self.svg.unit) + stretch_space

                new_distance = distance + width

                # calculate and apply transform
                first = path.interpolate(distance)
                last = path.interpolate(new_distance)

                if not first or not last:
                    # unusable path, nothing we can do
                    continue

                angle = degrees(atan2(last.y - first.y, last.x - first.x)) % 360
                translate = InkstitchPoint(first.x, first.y) - InkstitchPoint(left, text_baseline)

                transform = Transform(f"rotate({angle}, {first.x}, {first.y}) translate({translate.x} {translate.y})")
                correction_transform = Transform(get_correction_transform(glyph))
                glyph.transform = correction_transform @ transform @ glyph.transform

                # set values for next iteration
                distance = new_distance
                old_bbox = transformed_bbox

            distance += stretch_space

    def get_start_position(self, text_length, path_length):
        start_position = 0
        if self.text_position == 'center':
            start_position = (path_length - text_length) / 2
        if self.text_position == 'right':
            start_position = path_length - text_length
        return start_position

    def text_length(self, line):
        return convert_unit(line.bounding_box().width, 'px', self.svg.unit)

    def hide_commands(self):
        # hide commmands for bounding box calculation
        hidden_commands = []
        for glyph in self.glyphs:
            for group in glyph.iterdescendants(SVG_GROUP_TAG):
                if group.get_id().startswith("command_group") and group.style('display', 'inline') != 'none':
                    hidden_commands.append(group)
                    group.style['display'] = 'none'
        return hidden_commands

    def restore_commands(self, hidden_commands):
        for command in hidden_commands:
            command.style['display'] = "inline"

    def load_settings(self):
        """Load the settings saved into the text element"""

        self.settings = DotDict({
            "text": "",
            "back_and_forth": False,
            "font": None,
            "scale": 100,
            "trim_option": 0,
            "use_trim_symbols": False
        })

        if INKSTITCH_LETTERING in self.text.attrib:
            try:
                self.settings.update(json.loads(self.text.get(INKSTITCH_LETTERING)))
            except (TypeError, ValueError):
                pass
