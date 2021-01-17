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
        self.arg_parser.add_argument("-l", "--leading", type=float, default=5, dest="leading")
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
        # missing_glyph_spacing = kerning.missing_glyph_spacing()

        # collect data
        data = {'name': self.options.font_name,
                'description': self.options.font_description,
                'leading': self.options.leading,
                'auto_satin': self.options.auto_satin,
                'reversible': self.options.reversible,
                'default_glyph': self.options.default_glyph,
                'min_scale': self.options.min_scale,
                'max_scale': self.options.max_scale,
                'horiz_adv_x_default': letter_spacing,
                'horiz_adv_x_space': word_spacing,
                'horiz_adv_x': horiz_adv_x,
                'kerning_pairs': hkern,
                }

        # write data to font.json into the same directory as the font file
        with open(output_path, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)
