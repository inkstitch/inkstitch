# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# Fully lazy __init__.py — submodules loaded on first attribute access
_SUBMODULE_MAP = {
    # cache.py
    'cache': ('.cache', 'cache'),
    # dotdict.py
    'DotDict': ('.dotdict', 'DotDict'),
    # geometry.py
    'cut': ('.geometry', 'cut'),
    'cut_multiple': ('.geometry', 'cut_multiple'),
    'roll_linear_ring': ('.geometry', 'roll_linear_ring'),
    'reverse_line_string': ('.geometry', 'reverse_line_string'),
    'ensure_multi_line_string': ('.geometry', 'ensure_multi_line_string'),
    'ensure_geometry_collection': ('.geometry', 'ensure_geometry_collection'),
    'ensure_multi_polygon': ('.geometry', 'ensure_multi_polygon'),
    'ensure_multi_point': ('.geometry', 'ensure_multi_point'),
    'ensure_polygon': ('.geometry', 'ensure_polygon'),
    'cut_path': ('.geometry', 'cut_path'),
    'offset_points': ('.geometry', 'offset_points'),
    'remove_duplicate_points': ('.geometry', 'remove_duplicate_points'),
    'Point': ('.geometry', 'Point'),
    'line_string_to_point_list': ('.geometry', 'line_string_to_point_list'),
    'coordinate_list_to_point_list': ('.geometry', 'coordinate_list_to_point_list'),
    # io.py
    'save_stderr': ('.io', 'save_stderr'),
    'restore_stderr': ('.io', 'restore_stderr'),
    'save_stdout': ('.io', 'save_stdout'),
    'restore_stdout': ('.io', 'restore_stdout'),
    # paths.py
    'get_bundled_dir': ('.paths', 'get_bundled_dir'),
    'get_resource_dir': ('.paths', 'get_resource_dir'),
    'get_user_dir': ('.paths', 'get_user_dir'),
    'get_ini': ('.paths', 'get_ini'),
    # string.py
    'string_to_floats': ('.string', 'string_to_floats'),
    'remove_suffix': ('.string', 'remove_suffix'),
    # inkscape.py
    'guess_inkscape_config_path': ('.inkscape', 'guess_inkscape_config_path'),
}

def __getattr__(name):
    entry = _SUBMODULE_MAP.get(name)
    if entry is not None:
        mod_path, attr = entry
        import importlib
        mod = importlib.import_module(mod_path, __name__)
        val = getattr(mod, attr)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
