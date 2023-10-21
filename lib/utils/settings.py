from collections.abc import MutableMapping
import json
import os

from .paths import get_user_dir

# These settings are the defaults for SVG metadata settings of the same name in
# lib.extensions.base.InkstitchMetadata
DEFAULT_METADATA = {
    "min_stitch_len_mm": 0,
    "collapse_len_mm": 3,
}

DEFAULT_SETTINGS = {
    "cache_size": 100,
    "pop_out_simulator": False
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
