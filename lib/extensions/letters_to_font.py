# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
from html import escape, unescape
from pathlib import Path

import inkex
from inkex import errormsg

from ..commands import ensure_symbol
from ..i18n import _
from ..stitch_plan import generate_stitch_plan
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSCAPE_GROUPMODE, INKSCAPE_LABEL,
                        SVG_GROUP_TAG, SVG_PATH_TAG)
from .base import InkstitchExtension


class LettersToFont(InkstitchExtension):
    '''
    This extension will create a json file to store a custom directory path for additional user fonts
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-d", "--font-dir", type=str, default="", dest="font_dir")
        self.arg_parser.add_argument("-f", "--file-format", type=str, default="", dest="file_format")
        self.arg_parser.add_argument("-m", "--margin-left", type=float, default=0, dest="margin_left")
        self.arg_parser.add_argument("-c", "--import-commands", type=str, default="params", dest="import_commands")

    def effect(self) -> None:
        font_dir = self.options.font_dir
        file_format = self.options.file_format
        margin_left = self.options.margin_left * PIXELS_PER_MM

        if not os.path.isdir(font_dir):
            errormsg(_("Font directory not found. Please specify an existing directory."))

        # up from python 3.12 we will be able to use a case_sensitive attribute for this
        glyphs = list(Path(font_dir).rglob(file_format))
        glyphs += list(Path(font_dir).rglob(file_format.lower()))

        document = self.document.getroot()  # type: ignore
        unit_multiplier = self.svg.viewport_to_unit(1)
        page_bbox = self.svg.get_page_bbox()
        container_group = inkex.Group()
        group = None
        for glyph in glyphs:
            letter = self.get_glyph_element(glyph)
            if not letter:
                continue
            label = unescape(letter.get(INKSCAPE_LABEL, ' ')).split('.')[0][-1]
            label = f"GlyphLayer-{ label }"
            group = inkex.Group(attrib={
                INKSCAPE_LABEL: label,
                INKSCAPE_GROUPMODE: "layer",
                "transform": get_correction_transform(document, child=True)
            })

            # remove color block groups if we import without commands
            # there will only be one object per color block anyway
            if self.options.import_commands == "none":
                for element in letter.iter(SVG_PATH_TAG):
                    group.append(element)
            else:
                group.append(letter)

            container_group.append(group)

            # move letter to the bottom left of the page
            bbox = group.bounding_box()
            if bbox is not None:
                translate_x = margin_left - bbox.left / unit_multiplier
                translate_y = (page_bbox.bottom - bbox.bottom) / unit_multiplier
                group.transform @= inkex.Transform(f'translate({translate_x}, {translate_y})')

            group.set('style', 'display:none')

        # We found no glyphs, no need to proceed
        if group is None:
            return

        if self.options.import_commands == "symbols":
            # In most cases trims are inserted with the imported letters.
            # Let's make sure the trim symbol exists in the defs section
            ensure_symbol(document, 'trim')

        # insert sorted glyph list
        self.insert_sorted_glyphs_to_document(document, container_group)

        # insert baseline
        self.insert_baseline(page_bbox.bottom)

    def get_glyph_element(self, glyph: Path) -> inkex.Group:
        label = os.path.basename(glyph)
        if self.options.file_format.endswith('SVG'):
            stitch_plan = self.get_svg_elements(glyph)
        else:
            stitch_plan = generate_stitch_plan(str(glyph), self.options.import_commands)
            # we received a stitch plan wrapped in an svg document, we only need the stitch_plan group
            # this group carries the name of the file, so we can search for it.
            search_string = f'.//*[@inkscape:label="{ escape(label) }"]'
            stitch_plan = stitch_plan.xpath(search_string, namespaces=inkex.NSS)[0]
            stitch_plan.attrib.pop(INKSCAPE_GROUPMODE)
        stitch_plan.label = label
        return stitch_plan

    def get_svg_elements(self, glyph: Path) -> inkex.Group:
        glyph_svg = self.load(glyph).getroot()
        glyph_group = inkex.Group()
        # move all embroiderable child elements and groups of the svg file into a group
        for child in glyph_svg.iterchildren((SVG_GROUP_TAG, EMBROIDERABLE_TAGS)):
            glyph_group.add(child)
        return glyph_group

    def insert_baseline(self, page_bottom: float) -> None:
        self.svg.namedview.add_guide(position=page_bottom, name="baseline")

    def insert_sorted_glyphs_to_document(self, document: inkex.Group, container_group: inkex.Group) -> None:
        container_group[:] = sorted(container_group, key=lambda glyph: glyph.label, reverse=True)
        for group in container_group:
            document.append(group)
        # users may be confused if they get an empty document
        # make last letter visible
        group.set('style', None)
