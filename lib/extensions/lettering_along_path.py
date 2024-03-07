# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from math import atan2, degrees

from inkex import Boolean, Transform, errormsg
from inkex.units import convert_unit

from ..elements import Stroke
from ..i18n import _
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
        self.arg_parser.add_argument("-o", "--options", type=str, default=None, dest="page_1")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_2")
        self.arg_parser.add_argument("-s", "--stretch-spaces", type=Boolean, default=False, dest="stretch_spaces")

    def effect(self):
        # we ignore everything but the first path/text
        text, path = self.get_selection()
        if text is None or path is None:
            errormsg(_("Please select one path and one Ink/Stitch lettering group."))
            return

        glyphs = [glyph for glyph in text.iterdescendants(SVG_GROUP_TAG) if glyph.label and len(glyph.label) == 1]
        if not glyphs:
            errormsg(_("The text doesn't contain any glyphs."))
            return

        self.load_settings(text)
        path = Stroke(path).as_multi_line_string().geoms[0]
        hidden_commands = self.hide_commands(glyphs)
        space_indices, stretch_space, text_baseline = self.get_position_and_stretch_values(path, text, glyphs)
        self.transform_glyphs(glyphs, path, stretch_space, space_indices, text_baseline)
        self.restore_commands(hidden_commands)

    def get_position_and_stretch_values(self, path, text, glyphs):
        text_bbox = glyphs[0].getparent().bounding_box()
        text_baseline = text_bbox.bottom

        if self.options.stretch_spaces:
            text_content = self.settings["text"]
            space_indices = [i for i, t in enumerate(text_content) if t == " "]
            text_bbox = text.bounding_box()
            text_width = convert_unit(text_bbox.width, 'px', self.svg.unit)

            if len(text_content) - 1 != 0:
                path_length = path.length
                stretch_space = (path_length - text_width) / (len(text_content) - 1)
            else:
                stretch_space = 0
        else:
            stretch_space = 0
            space_indices = []

        return space_indices, stretch_space, text_baseline

    def hide_commands(self, glyphs):
        # hide commmands for bounding box calculation
        hidden_commands = []
        for glyph in glyphs:
            for group in glyph.iterdescendants(SVG_GROUP_TAG):
                if group.get_id().startswith("command_group") and group.style('display', 'inline') != 'none':
                    hidden_commands.append(group)
                    group.style['display'] = 'none'
        return hidden_commands

    def restore_commands(self, hidden_commands):
        for command in hidden_commands:
            command.style['display'] = "inline"

    def transform_glyphs(self, glyphs, path, stretch_space, space_indices, text_baseline):
        text_scale = Transform(f'scale({self.settings["scale"] / 100})')
        distance = 0
        old_bbox = None
        i = 0

        for glyph in glyphs:
            # dimensions
            bbox = glyph.bounding_box()
            transformed_bbox = glyph.bounding_box(glyph.getparent().composed_transform())
            left = bbox.left
            transformed_left = transformed_bbox.left
            width = convert_unit(transformed_bbox.width, 'px', self.svg.unit)

            # adjust position
            if old_bbox:
                distance += convert_unit(transformed_left - old_bbox.right, 'px', self.svg.unit) + stretch_space

            if self.options.stretch_spaces and i in space_indices:
                distance += stretch_space
                i += 1

            new_distance = distance + width

            # calculate and apply transform
            first = path.interpolate(distance)
            last = path.interpolate(new_distance)

            angle = degrees(atan2(last.y - first.y, last.x - first.x)) % 360
            translate = InkstitchPoint(first.x, first.y) - InkstitchPoint(left, text_baseline)

            transform = Transform(f"rotate({angle}, {first.x}, {first.y}) translate({translate.x} {translate.y})")
            correction_transform = Transform(get_correction_transform(glyph))
            glyph.transform = correction_transform @ transform @ glyph.transform @ text_scale

            # set values for next iteration
            distance = new_distance
            old_bbox = transformed_bbox
            i += 1

    def load_settings(self, text):
        """Load the settings saved into the text element"""

        self.settings = DotDict({
            "text": "",
            "back_and_forth": False,
            "font": None,
            "scale": 100,
            "trim_option": 0
        })

        if INKSTITCH_LETTERING in text.attrib:
            try:
                self.settings.update(json.loads(text.get(INKSTITCH_LETTERING)))
            except (TypeError, ValueError):
                pass

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
