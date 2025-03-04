# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os

from inkex import errormsg

from ..i18n import _
from ..utils import get_user_dir
from .base import InkstitchExtension


class LetteringCustomFontDir(InkstitchExtension):
    '''
    This extension will create a json file to store a custom directory path for additional user fonts
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-d", "--path", type=str, default="", dest="path")

    def effect(self):
        path = self.options.path
        if not os.path.isdir(path):
            errormsg(_("Please specify the directory of your custom fonts."))
            return

        data = {'custom_font_dir': '%s' % path}

        config_path = get_user_dir('custom_dirs.json')
        with open(config_path, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)


def get_custom_font_dir():
    custom_font_dir_path = get_user_dir('custom_dirs.json')
    try:
        with open(custom_font_dir_path, 'r') as custom_dirs:
            custom_dir = json.load(custom_dirs)
    except (IOError, ValueError):
        return ""
    try:
        return custom_dir['custom_font_dir']
    except KeyError:
        pass
    return ""
