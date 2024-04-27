# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import appdirs

from ..extensions.lettering_custom_font_dir import get_custom_font_dir
from ..lettering import Font
from ..utils import get_bundled_dir


def get_font_list():
    fonts = []
    font_paths = {
        get_bundled_dir("fonts"),
        os.path.expanduser("~/.inkstitch/fonts"),
        os.path.join(appdirs.user_config_dir('inkstitch'), 'fonts'),
        get_custom_font_dir()
    }

    for font_path in font_paths:
        try:
            font_dirs = os.listdir(font_path)
        except OSError:
            continue

        for font_dir in font_dirs:
            font = Font(os.path.join(font_path, font_dir))
            if font.marked_custom_font_name == "" or font.marked_custom_font_id == "":
                continue
            fonts.append(font)
    return fonts
