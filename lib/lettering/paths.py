from ..utils import get_bundled_dir, get_user_dir

import os
import json
from typing import List


def get_custom_font_cfg_file() -> str:
    return get_user_dir('custom_dirs.json')


def get_custom_font_dir() -> str:
    custom_font_dir_path = get_custom_font_cfg_file()
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


def _is_font_root(path: str) -> bool:
    """Return True if *path* contains immediate subdirectories that are fonts.

    A directory is considered a font root if at least one of its immediate
    subdirectories contains a font.json or font.json.xz file.
    """
    if not os.path.isdir(path):
        return False
    try:
        entries = os.listdir(path)
    except OSError:
        return False
    for entry in entries:
        subdir = os.path.join(path, entry)
        if not os.path.isdir(subdir):
            continue
        if os.path.isfile(os.path.join(subdir, "font.json")) or os.path.isfile(os.path.join(subdir, "font.json.xz")):
            return True
    return False


def _get_bundled_font_dir() -> str:
    """Return the bundled fonts directory for the active submodule layout.

    The fonts submodule has been laid out in two ways:
      - fonts/fonts/<font> : intermediate layout used by the refactored submodule
      - fonts/src/<font>   : legacy layout

    In the refactored layout Python source code may live under fonts/src, so
    we cannot simply check for directory existence.  We detect the actual font
    root by looking for font.json/font.json.xz in its immediate subdirectories.
    """
    fonts_root = get_bundled_dir("fonts")
    candidates = [
        os.path.join(fonts_root, "fonts"),
        os.path.join(fonts_root, "src"),
    ]
    for candidate in candidates:
        if _is_font_root(candidate):
            return candidate
    return os.path.join(fonts_root, "fonts")


def get_font_paths() -> List[str]:
    # NOTE: We do not scan the bundled fonts directory recursively here
    # because get_font_list() currently instantiates a Font object for every
    # subdirectory and only filters out invalid ones afterwards (by checking
    # marked_custom_font_name/id).  That would produce user-visible
    # "JSON file missing" warnings for non-font subdirectories such as
    # "ltr" / "rtl" variant folders.  A future improvement could pre-filter
    # directories by the presence of font.json or font.json.xz before
    # instantiating Font.
    font_paths = [
        _get_bundled_font_dir(),
        os.path.expanduser("~/.inkstitch/fonts/"),
        get_user_dir('fonts'),
        get_custom_font_dir()
    ]
    return font_paths
