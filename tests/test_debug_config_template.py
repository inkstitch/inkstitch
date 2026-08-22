import tomllib
from pathlib import Path

import pytest

from lib.debug.config import find_legacy_logging_placeholders, unknown_debug_config_keys
from lib.debug import logging as debug_logging


ROOT = Path(__file__).parents[1]


def test_debug_toml_keys_are_documented_in_template():
    debug_config = ROOT / "DEBUG.toml"
    if not debug_config.exists():
        pytest.skip("DEBUG.toml is optional developer configuration")

    with debug_config.open("rb") as config_file:
        config = tomllib.load(config_file)

    assert unknown_debug_config_keys(config, ROOT / "DEBUG_template.toml") == []


def test_unknown_debug_toml_keys_are_reported(tmp_path):
    template = tmp_path / "DEBUG_template.toml"
    template.write_text("[DEBUG]\n# development_mode = true\n", encoding="utf-8")

    assert unknown_debug_config_keys(
        {"DEBUG": {"development_mode": True, "removed_option": True}}, template
    ) == ["DEBUG.removed_option"]


def test_legacy_script_directory_placeholder_is_reported():
    config = {
        "handlers": {
            "file": {"filename": "%(SCRIPTDIR)s/inkstitch.log"},
            "console": {"filename": "%(LOGDIR)s/inkstitch.log"},
        }
    }

    assert find_legacy_logging_placeholders(config) == ["handlers.file.filename"]


def test_legacy_script_directory_placeholder_warns_developer(monkeypatch, tmp_path, capsys):
    logging_config = tmp_path / "LOGGING.toml"
    logging_config.write_text(
        '[handlers.file]\nfilename = "%(SCRIPTDIR)s/inkstitch.log"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(debug_logging, "configure_logging", lambda *_args: None)

    debug_logging.activate_for_development(
        {"LOGGING": {"log_config_file": str(logging_config)}}, tmp_path
    )

    assert "deprecated %(SCRIPTDIR)s" in capsys.readouterr().err