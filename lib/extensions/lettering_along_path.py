# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from math import atan2, degrees

from inkex import BaseElement, Group, Transform, errormsg
from inkex.units import convert_unit
from shapely.geometry import LineString, Point

from ..elements import Stroke
from ..i18n import _
from ..lettering import get_font_by_id
from ..svg import get_correction_transform
from ..svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_LETTERING, SVG_GROUP_TAG
from ..utils import DotDict
from ..utils import Point as InkstitchPoint
from ..utils import ensure_multi_line_string
from .base import InkstitchExtension


class LetteringAlongPath(InkstitchExtension):
    '''
    This extension aligns an Ink/Stitch Lettering group along a path
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-p", "--text-position", type=str, default='left', dest="text_position")
        self.arg_parser.add_argument("-v", "--vertical-alignment", type=str, default='left', dest="vertical_alignment")

    def effect(self) -> None:
        # we ignore everything but the first path/text
        text, path = self.get_selection()
        if text is None or path is None:
            errormsg(_("Please select one path and one Ink/Stitch lettering group."))
            return

        TextAlongPath(self.svg, text, path, self.options.text_position, self.options.vertical_alignment)

    def get_selection(self) -> tuple[Group | None, BaseElement | None]:
        lettering_groups: list[Group] = list()
        paths: list[BaseElement] = list()

        for node in self.svg.selection:
            if lettering_groups and paths:
                break

            lettering, target_paths = self.get_selected_elements(node)
            lettering_groups.extend(lettering)
            paths.extend(target_paths)

        if not lettering_groups or not paths:
            return None, None

        return lettering_groups[0], paths[0]

    def get_selected_elements(self, node: BaseElement) -> tuple[list[Group], list[BaseElement]]:
        lettering_groups: list[Group] = list()
        paths: list[BaseElement] = list()

        lettering_group = self.get_lettering_group(node)
        if lettering_group:
            lettering_groups.append(lettering_group)
        elif isinstance(node, Group):
            for child in node.iterchildren():
                lettering, target_paths = self.get_selected_elements(child)
                lettering_groups.extend(lettering)
                paths.extend(target_paths)
        elif node.tag in EMBROIDERABLE_TAGS:
            paths.append(node)

        return lettering_groups, paths

    def get_lettering_group(self, node: BaseElement) -> Group | None:
        if isinstance(node, Group) and INKSTITCH_LETTERING in node.attrib:
            return node

        for group in node.iterancestors(SVG_GROUP_TAG):
            # checking for group again (after filtering for it), doesn't seem to make sense
            # but it makes mypy happy
            if isinstance(group, Group) and INKSTITCH_LETTERING in group.attrib:
                return group

        return None


class TextAlongPath:
    '''
    Aligns an Ink/Stitch Lettering group along a path
    '''
    def __init__(self, svg: BaseElement, text: Group, path: BaseElement, text_position: str, vertical_alignment: str):
        self.svg = svg
        self.text = text
        self.path: LineString = Stroke(path).as_multi_line_string().geoms[0]
        self.text_position = text_position
        self.vertical_alignment = vertical_alignment
        self.glyphs: list[Group] = []

        self.load_settings()
        self.font = get_font_by_id(self.settings.font, False)
        if self.font is None:
            errormsg(_("Couldn't identify the font specified in the lettering group."))
            return

        self.font_scale = self.settings.scale / 100
        self._reset_glyph_transforms()

        if not self.glyphs:
            errormsg(_("The text doesn't contain any glyphs."))
            return

        hidden_commands = self.hide_commands()
        self.glyphs_along_path()
        self.restore_commands(hidden_commands)

    def _reset_glyph_transforms(self) -> None:
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
                self.settings.use_trim_symbols,
                0,  # color sort breaks the glyph structure needed for this method
                self.settings.text_align,
                self.settings.letter_spacing,
                self.settings.word_spacing,
                self.settings.line_height
            )

            self.glyphs = [glyph for glyph in rendered_text.iterdescendants(SVG_GROUP_TAG) if glyph.get('inkstitch:letter-group', '') == 'glyph']
            self.bake_transforms_recursively(text_group)

    def bake_transforms_recursively(self, element: Group) -> None:
        '''applies transforms of the text group to the glyph group'''
        for child in element:
            child.transform = element.transform @ child.transform
            if isinstance(child, Group) and not child.get('inkstitch:letter-group', '') == 'glyph':
                self.bake_transforms_recursively(child)
        element.transform = Transform()

    def glyphs_along_path(self) -> None:
        path = self.path
        for i, text_line in enumerate(self.text.getchildren()[0].iterchildren()):
            self.transform_glyphs(path, text_line, i)

            # offset path for the next line
            line_offset = (self.font.leading + self.settings.line_height ) * self.font_scale
            offset_path = ensure_multi_line_string(path.offset_curve(line_offset))
            if not offset_path.is_empty:
                path = offset_path.geoms[0]

    def transform_glyphs(self, path: LineString, line: Group, iterator: int) -> None:
        bbox = line.bounding_box()
        if not bbox:
            return

        text_width = bbox.width
        backwards = self.settings.back_and_forth and iterator % 1 == 1
        text_baseline = self._get_baseline(line, iterator)

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
                if not bbox or not transformed_bbox:
                    continue

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

                self._set_transform_info(glyph, angle, first)

                # set values for next iteration
                distance = new_distance
                old_bbox = transformed_bbox

            distance += stretch_space

    def _get_baseline(self, line: Group, iterator: int) -> float:
        bbox = line.bounding_box()
        if not bbox:
            return 0

        if self.vertical_alignment == 'bottom':
            # text is below the line
            return bbox.top
        elif self.vertical_alignment == 'baseline':
            # the baseline of the text is aligned with the line
            return (self.font.leading + self.settings.line_height) * iterator * self.font_scale
        else:
            # text is on top of the line
            return bbox.bottom

    def _set_transform_info(self, glyph: Group, angle: float, origin: Point) -> None:
        # apply angle and rotation center values if the font contains cross stitch elements
        # cross stitch will use these values to apply the rotation, this way we can make sure, that the cross stitch shapes
        # still stitch as intended, even when we rotate the element
        if 'crossstitch' in self.font.metadata['keywords']:
            for element in glyph.iterdescendants(EMBROIDERABLE_TAGS):
                if element.get_id().startswith('command_connector'):
                    continue
                # the rotation center in Inkscape is an offset to the center of the bounding box in document units
                element_transform = element.composed_transform()
                bbox = element.bounding_box(element_transform)
                if not bbox:
                    continue

                center = bbox.center
                rotation_center = (element.viewport_to_unit(origin.x), element.viewport_to_unit(origin.y))

                element.set('inkstitch:cross_rotation', str(angle))
                element.set('inkscape:transform-center-x', str(rotation_center[0] - center.x))
                element.set('inkscape:transform-center-y', str(center.y - rotation_center[1]))

    def get_start_position(self, text_length: float, path_length: float) -> float:
        start_position: float = 0
        if self.text_position == 'center':
            start_position = (path_length - text_length) / 2
        if self.text_position == 'right':
            start_position = path_length - text_length
        return start_position


    def hide_commands(self) -> list[Group]:
        # hide commmands for bounding box calculation
        hidden_commands: list[Group] = []
        for glyph in self.glyphs:
            for group in glyph.iterdescendants(SVG_GROUP_TAG):
                if group.get_id().startswith("command_group") and group.style('display', 'inline') != 'none':
                    hidden_commands.append(group)
                    group.style['display'] = 'none'
        return hidden_commands

    def restore_commands(self, hidden_commands) -> None:
        for command in hidden_commands:
            command.style['display'] = "inline"

    def load_settings(self) -> None:
        """Load the settings saved into the text element"""

        self.settings = DotDict({
            "text": "",
            "back_and_forth": False,
            "font": None,
            "scale": 100,
            "trim_option": 0,
            "use_trim_symbols": False,
            "color_sort": 0,
            "text_align": 0,
            "letter_spacing": 0,
            "word_spacing": 0,
            "line_height": 0
        })

        if INKSTITCH_LETTERING in self.text.attrib:
            try:
                self.settings.update(json.loads(self.text.get(INKSTITCH_LETTERING)))
            except (TypeError, ValueError):
                pass
