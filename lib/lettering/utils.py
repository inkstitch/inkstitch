# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

from ..lettering import Font
from ..utils.settings import global_settings
from .paths import get_custom_font_dir, get_font_paths

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


def _iter_font_dirs(font_path, max_depth, root=None):
    """Yield (font_dir, relative_id) under font_path, up to max_depth deep.

    A directory is a font directory if it contains font.json or font.json.xz.
    We do not descend into a font directory (a font cannot contain another
    font), which also prevents deep recursion.

    relative_id is the font directory path relative to the font root, so that
    fonts nested in subdirectories get a unique id (e.g. "category/foo")
    instead of a bare basename that could collide with another font.
    """
    if root is None:
        root = font_path

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
            yield path, os.path.relpath(path, root)
        elif max_depth > 1:
            yield from _iter_font_dirs(path, max_depth - 1, root)


def _iter_all_font_dirs():
    for font_path in get_font_paths():
        yield from _iter_font_dirs(font_path, get_font_search_depth())


def get_font_list(show_font_path_warning=True):
    fonts = []
    for font_dir, relative_id in _iter_all_font_dirs():
        font = _get_font_from_path(font_dir, relative_id, show_font_path_warning)
        if not font or font.marked_custom_font_name == "" or font.marked_custom_font_id == "":
            continue
        fonts.append(font)
    return fonts


def get_fonts_by_id(font_id, show_font_path_warning=True):
    """Return all fonts matching font_id.

    Matches the exact id (or marked_custom_font_id) first.  If none match,
    falls back to matching the directory basename, so that a font moved into
    a subdirectory is still found by the id stored in older SVG documents.

    The exact match compares the relative directory path (which is the font
    id) without constructing a Font object, so a single lookup does not parse
    every font's metadata.
    """
    custom_dir = get_custom_font_dir()

    # Exact match on the relative path (== font.id).  A custom font's
    # marked_custom_font_id is the relative path plus a trailing '*'.
    for font_dir, relative_id in _iter_all_font_dirs():
        is_custom = bool(custom_dir) and custom_dir in font_dir
        if font_id == relative_id or (is_custom and font_id == relative_id + '*'):
            font = _get_font_from_path(font_dir, relative_id, show_font_path_warning)
            if font:
                return [font]

    # Fall back to the directory basename, so that a font moved into a
    # subdirectory is still found by the id stored in older SVG documents.
    basename = os.path.basename(font_id.rstrip('*'))
    matches = []
    for font_dir, relative_id in _iter_all_font_dirs():
        if os.path.basename(relative_id) == basename:
            font = _get_font_from_path(font_dir, relative_id, show_font_path_warning)
            if font:
                matches.append(font)
    return matches


def get_font_by_id(font_id, show_font_path_warning=True):
    matches = get_fonts_by_id(font_id, show_font_path_warning)
    if len(matches) == 1:
        return matches[0]
    return None


def get_font_by_name(font_name, show_font_path_warning=True):
    for font_dir, relative_id in _iter_all_font_dirs():
        font = _get_font_from_path(font_dir, relative_id, show_font_path_warning)
        if font and font_name in [font.name, font.marked_custom_font_name]:
            return font
    return None


def _get_font_from_path(font_dir, relative_id, show_font_path_warning=True):
    if not is_font_dir(font_dir):
        return
    return Font(font_dir, show_font_path_warning, font_id=relative_id)
