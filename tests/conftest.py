import pytest

import lib.utils.settings


@pytest.fixture(scope="session", autouse=True)
def disable_cache():
    # We disable the cache because Nix executes our tests with a non-writable HOME directory.
    lib.utils.settings.global_settings._settings['cache_size'] = 0
    lib.utils.settings.global_settings._settings['font_cache_size'] = 0
