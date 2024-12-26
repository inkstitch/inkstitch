# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os

from inkex import errormsg

from ..i18n import _
from ..lettering import Font
from .base import InkstitchExtension


class LetteringUpdateJsonGlyphlist(InkstitchExtension):
    '''
    This extension helps font creators to generate the json file for the lettering tool
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-d", "--font-dir", type=str, default="", dest="font_dir")

    def effect(self):
        # file paths
        font_dir = self.options.font_dir
        if not os.path.isdir(font_dir):
            errormsg(_("Please verify font folder path."))
            return
        json_file = self._get_json_file(font_dir)

        # glyphs
        font = Font(font_dir)
        font._load_variants()
        glyphs = font.get_variant(font.default_variant).glyphs
        glyphs = list(glyphs.keys())

        if not glyphs:
            return

        # read json file
        with open(json_file, 'r') as font_data:
            data = json.load(font_data)

        data['glyphs'] = glyphs

        # write data to the.json file
        with open(json_file, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)

    def _get_json_file(self, font_dir):
        json_file = os.path.join(font_dir, "font.json")
        if not os.path.isfile(json_file):
            errormsg(_("Could not find json file. Please create one with Extensions > Ink/Stitch > Font Management > Generate JSON..."))
        return json_file
