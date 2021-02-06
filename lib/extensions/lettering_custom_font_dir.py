import json
import os

import appdirs
from inkex import errormsg

from ..i18n import _
from .base import InkstitchExtension


class LetteringCustomFontDir(InkstitchExtension):
    '''
    This extension will create a json file to store a custom directory path for additional user fonts
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-d", "--path", type=str, default="", dest="path")

    def effect(self):
        path = self.options.path
        if not os.path.isdir(path):
            errormsg(_("Please specify the directory of your custom fonts."))
            return

        data = {'custom_font_dir': '%s' % path}

        try:
            config_path = appdirs.user_config_dir('inkstitch')
        except ImportError:
            config_path = os.path.expanduser('~/.inkstitch')
        config_path = os.path.join(config_path, 'custom_dirs.json')

        with open(config_path, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)


def get_custom_font_dir():
    custom_font_dir_path = os.path.join(appdirs.user_config_dir('inkstitch'), 'custom_dirs.json')
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
