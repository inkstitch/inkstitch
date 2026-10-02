import logging
from pathlib import Path

import pytest

from lib.debug import logging as debug_logging


@pytest.mark.parametrize(
    ("development_mode", "log_location", "expected"),
    [
        (False, "script", None),
        (False, "", None),
        (True, "", None),
        (True, "unknown", None),
        (True, "document", None),
    ],
)
def test_resolve_log_dir_disables_file_logging_for_disabled_locations(
    monkeypatch, tmp_path, development_mode, log_location, expected
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)

    assert (
        debug_logging.resolve_log_dir(development_mode, log_location, tmp_path)
        == expected
    )


def test_resolve_log_dir_environment_override_works_in_user_and_dev_modes(
    monkeypatch, tmp_path
):
    override = tmp_path / "override"
    monkeypatch.setenv("INKSTITCH_LOG_DIR", str(override))

    for development_mode in (False, True):
        assert (
            debug_logging.resolve_log_dir(development_mode, "script", tmp_path)
            == override
        )

    assert override.is_dir()


@pytest.mark.parametrize(
    ("log_location", "environment", "expected"),
    [
        ("script", {}, "script/log"),
        ("document", {"DOCUMENT_PATH": "document.svg"}, "."),
        ("doc", {"DOCUMENT_PATH": "document.svg"}, "."),
        ("temp", {}, "temp/log"),
        ("tmp", {}, "temp/log"),
    ],
)
def test_resolve_log_dir_development_locations(
    monkeypatch, tmp_path, log_location, environment, expected
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    monkeypatch.delenv("DOCUMENT_PATH", raising=False)

    document = tmp_path / "document.svg"
    if environment:
        document.touch()
        monkeypatch.setenv("DOCUMENT_PATH", str(document))

    if expected == "script/log":
        expected_path = tmp_path / "log"
    elif expected == ".":
        expected_path = document.parent
    else:
        temporary_dir = tmp_path / "temporary"
        monkeypatch.setattr("tempfile.gettempdir", lambda: str(temporary_dir))
        expected_path = temporary_dir / "inkstitch" / "log"

    assert debug_logging.resolve_log_dir(True, log_location, tmp_path) == expected_path
    assert expected_path.is_dir()


@pytest.mark.parametrize("log_location", ["user", "usr"])
def test_resolve_log_dir_uses_platform_user_log_directory(
    monkeypatch, tmp_path, log_location
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    user_log_dir = tmp_path / "user-log"
    monkeypatch.setattr("platformdirs.user_log_dir", lambda _app: str(user_log_dir))

    assert (
        debug_logging.resolve_log_dir(True, log_location, tmp_path)
        == user_log_dir
    )
    assert user_log_dir.is_dir()


@pytest.mark.parametrize("log_location", ["script", "user", "temp"])
def test_resolve_log_dir_does_not_nest_log_directories(
    monkeypatch, tmp_path, log_location
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    monkeypatch.delenv("DOCUMENT_PATH", raising=False)
    monkeypatch.setattr("platformdirs.user_log_dir", lambda _app: str(tmp_path / "user" / "log"))
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path / "temporary"))

    log_dir = debug_logging.resolve_log_dir(True, log_location, tmp_path / "script")

    assert log_dir is not None
    assert log_dir.name == "log"
    assert log_dir.parent.name != "log"


def test_resolve_log_dir_accepts_absolute_directory_and_existing_file(monkeypatch, tmp_path):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    directory = tmp_path / "logs"
    log_file = tmp_path / "inkstitch.log"
    log_file.touch()

    assert debug_logging.resolve_log_dir(True, str(directory), tmp_path) == directory
    assert debug_logging.resolve_log_dir(True, str(log_file), tmp_path) == tmp_path


def test_resolve_log_dir_disables_file_logging_when_directory_is_not_writable(
    monkeypatch, tmp_path
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    monkeypatch.setattr(debug_logging.debug_utils, "can_write_to_directory", lambda _path: False)

    assert debug_logging.resolve_log_dir(True, "script", tmp_path) is None


def test_resolve_log_dir_disables_file_logging_when_directory_cannot_be_created(
    monkeypatch, tmp_path
):
    monkeypatch.delenv("INKSTITCH_LOG_DIR", raising=False)
    target = tmp_path / "cannot-create"

    def fail_mkdir(*_args, **_kwargs):
        raise PermissionError("access denied")

    monkeypatch.setattr(Path, "mkdir", fail_mkdir)

    assert debug_logging.resolve_log_dir(True, str(target), tmp_path) is None


def test_activate_logging_disables_logging_when_log_directory_is_unavailable(monkeypatch, tmp_path):
    monkeypatch.setattr(debug_logging, "resolve_log_dir", lambda *_args: None)
    disabled = []
    monkeypatch.setattr(logging, "disable", lambda *args: disabled.append(args))
    monkeypatch.setattr(debug_logging, "disable_warnings", lambda: disabled.append("warnings"))

    assert debug_logging.activate_logging(False, "", {}, tmp_path) is None
    assert disabled == [(), "warnings"]
