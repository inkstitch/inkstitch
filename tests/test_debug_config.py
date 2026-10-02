from lib.debug.config import resolve_development_config


def test_user_mode_discards_debug_toml_settings():
    source_config: dict[str, dict[str, object]] = {
        "DEBUG": {"development_mode": False, "debug_enable": True},
        "LIBRARY": {"prefer_pip_inkex": False},
        "LOGGING": {"log_location": "script"},
        "PROFILE": {"profile_enable": True},
    }

    development_mode, config = resolve_development_config(source_config)

    assert development_mode is False
    assert config == {}
    assert source_config["LIBRARY"]["prefer_pip_inkex"] is False


def test_development_mode_keeps_debug_toml_settings():
    source_config: dict[str, dict[str, object]] = {
        "DEBUG": {"development_mode": True},
        "LIBRARY": {"prefer_pip_inkex": False},
    }

    development_mode, config = resolve_development_config(source_config)

    assert development_mode is True
    assert config is source_config
