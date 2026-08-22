from .utils import safe_get


def resolve_development_config(ini: dict) -> tuple[bool, dict]:
    """Return development mode and its configuration, or an empty user-mode config."""
    development_mode = safe_get(ini, "DEBUG", "development_mode", default=False)
    return development_mode, ini if development_mode else {}
