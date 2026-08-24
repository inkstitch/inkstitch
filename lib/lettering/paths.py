from ..utils import get_bundled_dir, get_user_dir

import os
import json
import inkstitch_fonts  # type: ignore[import-untyped]


def get_custom_font_cfg_file() -> str:
    return get_user_dir('custom_dirs.json')


def get_custom_font_dir() -> str:
    custom_font_dir_path = get_custom_font_cfg_file()
    try:
        with open(custom_font_dir_path, 'r') as custom_dirs:
            custom_dir = json.load(custom_dirs)
    except (OSError, ValueError):
        return ""
    try:
        return custom_dir['custom_font_dir']
    except KeyError:
        pass
    return ""


def get_font_paths() -> list[str]:
    pkg_root = os.path.dirname(inkstitch_fonts.get_fonts_dir())
    font_paths = [
        os.path.join(pkg_root, "fonts"),
        os.path.join(get_bundled_dir("fonts"), "src"),
        os.path.expanduser("~/.inkstitch/fonts/"),
        get_user_dir('fonts'),
        get_custom_font_dir()
    ]
    return font_paths
