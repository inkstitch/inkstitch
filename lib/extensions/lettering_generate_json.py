# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os

from inkex import Boolean, errormsg

from ..i18n import _
from ..lettering.categories import FONT_CATEGORIES
from ..lettering.font_info import FontFileInfo
from .base import InkstitchExtension


class LetteringGenerateJson(InkstitchExtension):
    '''
    This extension helps font creators to generate the json file for the lettering tool
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")

        self.arg_parser.add_argument("-n", "--font-name", type=str, default="Font", dest="font_name")
        self.arg_parser.add_argument("-d", "--font-description", type=str, default="Description", dest="font_description")
        self.arg_parser.add_argument("--font_license", type=str, default="SIL Open Font License v1.1", dest="font_license")
        self.arg_parser.add_argument("-v", "--default_variant", type=str, default="ltr", dest="default_variant")
        self.arg_parser.add_argument("-x", "--text_direction", type=str, default="ltr", dest="text_direction")
        self.arg_parser.add_argument("-s", "--auto-satin", type=Boolean, default="true", dest="auto_satin")
        self.arg_parser.add_argument("-r", "--reversible", type=Boolean, default="true", dest="reversible")
        self.arg_parser.add_argument("-o", "--combine-at-sort-indices", type=str, default="", dest="combine_at_sort_indices")
        self.arg_parser.add_argument("-t", "--sortable", type=Boolean, default="false", dest="sortable")
        self.arg_parser.add_argument("-u", "--letter-case", type=str, default="", dest="letter_case")
        self.arg_parser.add_argument("-g", "--default-glyph", type=str, default="", dest="default_glyph")
        self.arg_parser.add_argument("-z", "--size", type=float, default=15, dest="size")
        self.arg_parser.add_argument("-i", "--min-scale", type=float, default=1.0, dest="min_scale")
        self.arg_parser.add_argument("-a", "--max-scale", type=float, default=1.0, dest="max_scale")
        self.arg_parser.add_argument("--use-custom-leading", type=Boolean, default="false", dest="use_custom_leading")
        self.arg_parser.add_argument("--use-custom-spacing", type=Boolean, default="false", dest="use_custom_spacing")
        self.arg_parser.add_argument("--use-custom-letter-spacing", type=Boolean, default="false", dest="use_custom_letter_spacing")
        self.arg_parser.add_argument("--use-glyph-width", type=Boolean, default="false", dest="use_glyph_width")
        self.arg_parser.add_argument("-l", "--leading", type=int, default=100, dest="leading")
        self.arg_parser.add_argument("-w", "--word-spacing", type=int, default=20, dest="word_spacing")
        self.arg_parser.add_argument("-b", "--letter-spacing", type=int, default=100, dest="letter_spacing")
        self.arg_parser.add_argument("-p", "--font-file", type=str, default="", dest="path")
        self.arg_parser.add_argument("--original_font", type=str, default="", dest="original_font")
        self.arg_parser.add_argument("--original_font_url", type=str, default="", dest="original_font_url")

        for category in FONT_CATEGORIES:
            self.arg_parser.add_argument(f"--{category.id}", type=Boolean, default="false", dest=category.id)

    def effect(self):
        # file paths
        path = self.options.path
        if not os.path.isfile(path):
            errormsg(_("Please specify a font file."))
            return
        output_path = os.path.join(os.path.dirname(path), 'font.json')

        # font info (kerning, glyphs)
        font_info = FontFileInfo(path)

        horiz_adv_x = font_info.horiz_adv_x()
        hkern = font_info.hkern()
        custom_leading = self.options.use_custom_leading
        custom_spacing = self.options.use_custom_spacing
        word_spacing = font_info.word_spacing()
        # use user input in case that the default word spacing is not defined
        # in the svg file or the user forces custom values
        if custom_spacing or not word_spacing:
            word_spacing = self.options.word_spacing

        letter_spacing = self._get_letter_spacing(font_info)

        units_per_em = font_info.units_per_em() or self.options.leading
        # use units_per_em for leading (line height) if defined in the font file,
        # unless the user wishes to overwrite the value
        if units_per_em and not custom_leading:
            leading = units_per_em
        else:
            leading = self.options.leading

        glyphs = font_info.glyph_list()

        keywords = []
        for category in FONT_CATEGORIES:
            if getattr(self.options, category.id):
                keywords.append(category.id)

        combine_at_sort_indices = self.options.combine_at_sort_indices.split(',')
        combine_at_sort_indices = set([index.strip() for index in combine_at_sort_indices if index.strip()])

        # collect data
        data = {'name': self.options.font_name,
                'description': self.options.font_description,
                'font_license': self.options.font_license,
                'default_variant': self.options.default_variant,
                'text_direction': self.options.text_direction,
                'keywords': keywords,
                'original_font': self.options.original_font,
                'original_font_url': self.options.original_font_url,
                'leading': leading,
                'auto_satin': self.options.auto_satin,
                'reversible': self.options.reversible,
                'sortable': self.options.sortable,
                'combine_at_sort_indices': list(combine_at_sort_indices),
                'letter_case': self.options.letter_case,
                'default_glyph': self.options.default_glyph,
                'size': self.options.size,
                'min_scale': round(self.options.min_scale, 1),
                'max_scale': round(self.options.max_scale, 1),
                'horiz_adv_x_default': letter_spacing,
                'horiz_adv_x_space': word_spacing,
                'units_per_em': units_per_em,
                'horiz_adv_x': horiz_adv_x,
                'kerning_pairs': hkern,
                'glyphs': glyphs
                }

        # write data to font.json into the same directory as the font file
        with open(output_path, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)

    def _get_letter_spacing(self, font_info):
        letter_spacing = font_info.letter_spacing()
        # use user input in case that the default word spacing is not defined
        # in the svg file or the user forces custom values
        if self.options.use_custom_letter_spacing or not letter_spacing:
            letter_spacing = self.options.letter_spacing
        if self.options.use_glyph_width:
            letter_spacing = None
        return letter_spacing
