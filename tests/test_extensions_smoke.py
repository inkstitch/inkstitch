from __future__ import annotations

from importlib import import_module
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS_DIR = REPO_ROOT / "lib" / "extensions"


def _iter_extension_modules() -> list[str]:
    modules: list[str] = []
    for path in sorted(EXTENSIONS_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue

        relative = path.relative_to(REPO_ROOT).with_suffix("")
        module_name = ".".join(relative.parts)
        modules.append(module_name)

    return modules


EXTENSION_MODULES = _iter_extension_modules()
OPTIONAL_IMPORT_ROOTS = {"wx", "winutils"}


@pytest.mark.parametrize("module_name", EXTENSION_MODULES)
def test_extension_module_import_smoke(module_name: str) -> None:
    try:
        import_module(module_name)
    except ModuleNotFoundError as error:
        missing_root = (error.name or "").split(".")[0]
        if missing_root in OPTIONAL_IMPORT_ROOTS:
            pytest.skip(f"Optional dependency is missing for smoke import: {error.name}")
        raise
