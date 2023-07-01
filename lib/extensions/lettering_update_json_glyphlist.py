# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import sys

from ..i18n import _
from ..lettering.font_info import FontFileInfo
from .base import InkstitchExtension


class LetteringUpdateJsonGlyphlist(InkstitchExtension):
    '''
    This extension helps font creators to generate the json file for the lettering tool
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--font-file", type=str, default="", dest="font_file")
        self.arg_parser.add_argument("-j", "--json-file", type=str, default="", dest="json_file")

    def effect(self):
        # file paths
        font_file = self.options.font_file
        json_file = self.options.json_file
        if not os.path.isfile(font_file) or not os.path.isfile(json_file):
            print(_("Please verify file locations."), file=sys.stderr)
            return

        glyphs = FontFileInfo(font_file).glyph_list()

        with open(json_file, 'r') as font_data:
            data = json.load(font_data)

        data['glyphs'] = glyphs

        # write data to font.json into the same directory as the font file
        with open(json_file, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)
