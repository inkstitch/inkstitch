# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

from ..lettering import Font
from .paths import get_font_paths


def get_font_list(show_font_path_warning=True):
    font_paths = get_font_paths()

    fonts = []
    for font_path in font_paths:
        try:
            font_dirs = os.listdir(font_path)
        except OSError:
            continue

        for font_dir in font_dirs:
            font = _get_font_from_path(font_path, font_dir, show_font_path_warning)
            if not font or font.marked_custom_font_name == "" or font.marked_custom_font_id == "":
                continue
            fonts.append(font)
    return fonts


def get_font_by_id(font_id, show_font_path_warning=True):
    font_paths = get_font_paths()
    for font_path in font_paths:
        try:
            font_dirs = os.listdir(font_path)
        except OSError:
            continue
        for font_dir in font_dirs:
            font = _get_font_from_path(font_path, font_dir, show_font_path_warning)
            if font and font_id in [font.id, font.marked_custom_font_id]:
                return font
    return None


def get_font_by_name(font_name, show_font_path_warning=True):
    font_paths = get_font_paths()
    for font_path in font_paths:
        try:
            font_dirs = os.listdir(font_path)
        except OSError:
            continue
        for font_dir in font_dirs:
            font = _get_font_from_path(font_path, font_dir, show_font_path_warning)
            if font and font_name in [font.name, font.marked_custom_font_name]:
                return font
    return None


def _get_font_from_path(font_path, font_dir, show_font_path_warning=True):
    if not os.path.isdir(os.path.join(font_path, font_dir)) or font_dir.startswith('.'):
        return
    return Font(os.path.join(font_path, font_dir), show_font_path_warning)
