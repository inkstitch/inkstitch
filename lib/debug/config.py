import re
from collections.abc import Mapping
from pathlib import Path

from .utils import safe_get


def resolve_development_config(ini: dict) -> tuple[bool, dict]:
    """Return development mode and its configuration, or an empty user-mode config."""
    development_mode = safe_get(ini, "DEBUG", "development_mode", default=False)
    return development_mode, ini if development_mode else {}


def unknown_debug_config_keys(config: dict, template_path: Path) -> list[str]:
    """Return DEBUG.toml keys that are absent from its commented template."""
    section = ""
    allowed_keys: set[tuple[str, str]] = set()

    for line in template_path.read_text(encoding="utf-8").splitlines():
        if match := re.match(r"^\[([^]]+)]$", line.strip()):
            section = match.group(1)
        elif match := re.match(r"^#\s*([A-Za-z_]\w*)\s*=", line.strip()):
            allowed_keys.add((section, match.group(1)))
        elif match := re.match(r"^([A-Za-z_]\w*)\s*=", line.strip()):
            allowed_keys.add((section, match.group(1)))

    return sorted(
        f"{section}.{key}"
        for section, values in config.items()
        if isinstance(values, Mapping)
        for key in values
        if (section, key) not in allowed_keys
    )


def find_legacy_logging_placeholders(config: object) -> list[str]:
    """Return configuration paths that still use the SCRIPTDIR placeholder."""
    matches: list[str] = []

    def visit(value: object, path: str) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                visit(child, f"{path}.{key}" if path else str(key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
        elif isinstance(value, str) and "%(SCRIPTDIR)s" in value:
            matches.append(path)

    visit(config, "")
    return matches
