import json
import os
from collections.abc import MutableMapping

from .paths import get_user_dir

# These settings are the defaults for SVG metadata settings of the same name in
# lib.extensions.base.InkstitchMetadata
DEFAULT_METADATA = {
    "min_stitch_len_mm": 0.1,
    "collapse_len_mm": 3,
}

DEFAULT_SETTINGS = {
    # Ink/Stitch preferences
    "cache_size": 100,
    "pop_out_simulator": False,
    # simulator
    "simulator_adaptive_speed": True,
    "simulator_speed": 16,
    "simulator_line_width": 0.1,
    "simulator_npp_size": 0.5,
    "npp_button_status": False,
    "jump_button_status": False,
    "trim_button_status": False,
    "stop_button_status": False,
    "color_change_button_status": False,
    "toggle_page_button_status": True,
    "display_crosshair": True,
    # apply palette
    "last_applied_palette": "",
    # sew stack editor
    "stitch_layer_editor_sash_position": -200,
    # lettering (all lettering applications)
    "last_font": "Ink/Stitch Small Font",
    # lettering
    "lettering_align_text": 0,
    "lettering_trim_option": 0,
    "lettering_use_command_symbols": False,
    # font sampling
    "font_sampling_max_line_width": 180,
    "font_sampling_scale_spinner": 100,
    # cross stitch grid helper
    'square': True,
    'cross_helper_box_x': 3,
    'cross_helper_box_y': 3,
    'cross_helper_set_params': True,
    'cross_helper_cross_method': 'simple_cross',
    'cross_helper_pixelize': False,
    'cross_helper_pixelize_combined': True,
    'cross_helper_coverage': 50,
    'cross_helper_grid_offset': '0',
    'cross_helper_align_with_canvas': True,
    'cross_helper_nodes': False,
    'cross_helper_set_grid': False,
    'cross_helper_grid_color': (0, 153, 229),
    'cross_helper_remove_grids': True,
    'cross_helper_convert_bitmap': False,
    'cross_helper_color_method': 0,
    'cross_bitmap_num_colors': 5,
    'cross_bitmap_quantize_method': 1,
    'cross_bitmap_rgb_colors': '',
    'cross_bitmap_gimp_palette': '',
    'cross_bitmap_saturation': 1,
    'cross_bitmap_brightness': 1,
    'cross_bitmap_contrast': 1,
    'cross_bitmap_background_color': (0, 0, 0),
    'cross_bitmap_remove_background': 0
}


class GlobalSettings(MutableMapping):
    def __init__(self):
        super().__init__()
        # We set create=False here because this code is executed on module load
        # and via imports also runs on generate-inx-files, which with the Nix
        # package manager is executed with a non-writable home directory.
        user_dir = get_user_dir(create=False)
        self._settings_file = os.path.join(user_dir, "settings.json")
        self._settings = {}

        for name, value in DEFAULT_METADATA.items():
            self._settings[f"default_{name}"] = value

        self._settings.update(DEFAULT_SETTINGS)

        try:
            with open(self._settings_file, 'r') as settings_file:
                self._settings.update(json.load(settings_file))
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    def __setitem__(self, item, value):
        self._settings[item] = value

        try:
            with open(self._settings_file, 'w') as settings_file:
                json.dump(self._settings, settings_file)
        except FileNotFoundError:
            pass

    def __getitem__(self, item):
        return self._settings[item]

    def __delitem__(self, item):
        del self._settings[item]

    def __iter__(self):
        return iter(self._settings)

    def __len__(self):
        return len(self._settings)

    def __json__(self):
        return self._settings


global_settings = GlobalSettings()
