# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

from ..lettering import Font
from ..utils.settings import global_settings
from .paths import get_font_paths

# Hard cap on the font search depth, to prevent runaway recursion into
# arbitrary directory trees.  The user-configurable value is clamped to this.
MAX_FONT_SEARCH_DEPTH = 5


def is_font_dir(path):
    """Return True if the directory contains a font definition.

    A font directory must contain a font.json or font.json.xz file.  This is
    the single source of truth for font detection.
    """
    if not os.path.isdir(path):
        return False
    return (os.path.isfile(os.path.join(path, "font.json")) or
            os.path.isfile(os.path.join(path, "font.json.xz")))


def get_font_search_depth():
    """Return the configured font search depth, clamped to a safe range."""
    try:
        depth = int(global_settings.get('font_search_depth', 2))
    except (TypeError, ValueError):
        depth = 2
    return max(1, min(depth, MAX_FONT_SEARCH_DEPTH))


def _iter_font_dirs(font_path, max_depth):
    """Yield font directory paths under font_path, up to max_depth levels deep.

    A directory is a font directory if it contains font.json or font.json.xz.
    We do not descend into a font directory (a font cannot contain another
    font), which also prevents deep recursion.
    """
    try:
        entries = sorted(os.listdir(font_path))
    except OSError:
        return

    for entry in entries:
        if entry.startswith('.'):
            continue
        path = os.path.join(font_path, entry)
        if not os.path.isdir(path):
            continue
        if is_font_dir(path):
            yield path
        elif max_depth > 1:
            yield from _iter_font_dirs(path, max_depth - 1)


def _iter_all_font_dirs():
    for font_path in get_font_paths():
        yield from _iter_font_dirs(font_path, get_font_search_depth())


def get_font_list(show_font_path_warning=True):
    fonts = []
    for font_dir in _iter_all_font_dirs():
        font = _get_font_from_path(font_dir, show_font_path_warning)
        if not font or font.marked_custom_font_name == "" or font.marked_custom_font_id == "":
            continue
        fonts.append(font)
    return fonts


def get_font_by_id(font_id, show_font_path_warning=True):
    for font_dir in _iter_all_font_dirs():
        font = _get_font_from_path(font_dir, show_font_path_warning)
        if font and font_id in [font.id, font.marked_custom_font_id]:
            return font
    return None


def get_font_by_name(font_name, show_font_path_warning=True):
    for font_dir in _iter_all_font_dirs():
        font = _get_font_from_path(font_dir, show_font_path_warning)
        if font and font_name in [font.name, font.marked_custom_font_name]:
            return font
    return None


def _get_font_from_path(font_dir, show_font_path_warning=True):
    if not is_font_dir(font_dir):
        return
    return Font(font_dir, show_font_path_warning)
