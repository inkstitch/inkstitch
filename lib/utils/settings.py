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
    # apply palette
    "last_applied_palette": "",
    # sew stack editor
    "stitch_layer_editor_sash_position": -200,
}


class GlobalSettings(MutableMapping):
    def __init__(self):
        super().__init__()
        self.__settings_file = os.path.join(get_user_dir(), "settings.json")
        self.__settings = {}

        for name, value in DEFAULT_METADATA.items():
            self.__settings[f"default_{name}"] = value

        self.__settings.update(DEFAULT_SETTINGS)

        try:
            with open(self.__settings_file, 'r') as settings_file:
                self.__settings.update(json.load(settings_file))
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    def __setitem__(self, item, value):
        self.__settings[item] = value

        with open(self.__settings_file, 'w') as settings_file:
            json.dump(self.__settings, settings_file)

    def __getitem__(self, item):
        return self.__settings[item]

    def __delitem__(self, item):
        del self.__settings[item]

    def __iter__(self):
        return iter(self.__settings)

    def __len__(self):
        return len(self.__settings)

    def __json__(self):
        return self.__settings


global_settings = GlobalSettings()
