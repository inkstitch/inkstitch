# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import sys

from inkex import Boolean

from ..i18n import _
from ..lettering.kerning import FontKerning
from .base import InkstitchExtension


class LetteringGenerateJson(InkstitchExtension):
    '''
    This extension helps font creators to generate the json file for the lettering tool
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-n", "--font-name", type=str, default="Font", dest="font_name")
        self.arg_parser.add_argument("-d", "--font-description", type=str, default="Description", dest="font_description")
        self.arg_parser.add_argument("-s", "--auto-satin", type=Boolean, default="true", dest="auto_satin")
        self.arg_parser.add_argument("-r", "--reversible", type=Boolean, default="true", dest="reversible")
        self.arg_parser.add_argument("-g", "--default-glyph", type=str, default="", dest="default_glyph")
        self.arg_parser.add_argument("-i", "--min-scale", type=float, default=1, dest="min_scale")
        self.arg_parser.add_argument("-a", "--max-scale", type=float, default=1, dest="max_scale")
        self.arg_parser.add_argument("-l", "--leading", type=int, default=0, dest="leading")
        self.arg_parser.add_argument("-p", "--font-file", type=str, default="", dest="path")

    def effect(self):
        # file paths
        path = self.options.path
        if not os.path.isfile(path):
            print(_("Please specify a font file."), file=sys.stderr)
            return
        output_path = os.path.join(os.path.dirname(path), 'font.json')

        # kerning
        kerning = FontKerning(path)

        horiz_adv_x = kerning.horiz_adv_x()
        hkern = kerning.hkern()
        word_spacing = kerning.word_spacing()
        letter_spacing = kerning.letter_spacing()
        units_per_em = kerning.units_per_em()
        # missing_glyph_spacing = kerning.missing_glyph_spacing()

        # if letter spacing returns 0, it hasn't been specified in the font file
        # Ink/Stitch will calculate the width of each letter automatically
        if letter_spacing == 0:
            letter_spacing = None

        # if leading (line height) is set to 0, the font author wants Ink/Stitch to use units_per_em
        # if units_per_em is not defined in the font file a default value will be returned
        if self.options.leading == 0:
            leading = units_per_em
        else:
            leading = self.options.leading

        # collect data
        data = {'name': self.options.font_name,
                'description': self.options.font_description,
                'leading': leading,
                'auto_satin': self.options.auto_satin,
                'reversible': self.options.reversible,
                'default_glyph': self.options.default_glyph,
                'min_scale': self.options.min_scale,
                'max_scale': self.options.max_scale,
                'horiz_adv_x_default': letter_spacing,
                'horiz_adv_x_space': word_spacing,
                'units_per_em': units_per_em,
                'horiz_adv_x': horiz_adv_x,
                'kerning_pairs': hkern
                }

        # write data to font.json into the same directory as the font file
        with open(output_path, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)
