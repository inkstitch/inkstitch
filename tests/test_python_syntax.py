from __future__ import annotations

from pathlib import Path
import tokenize

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
}
EXCLUDED_PATH_PARTS = {
    "site-packages",
    "dist-packages",
}


def _find_virtualenv_roots(root: Path) -> set[Path]:
    return {path.parent.resolve() for path in root.rglob("pyvenv.cfg")}


VIRTUALENV_ROOTS = _find_virtualenv_roots(REPO_ROOT)


def _is_in_virtualenv(path: Path) -> bool:
    resolved = path.resolve()
    return any(resolved.is_relative_to(env_root) for env_root in VIRTUALENV_ROOTS)


def _iter_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if any(part in EXCLUDED_PATH_PARTS for part in path.parts):
            continue
        if _is_in_virtualenv(path):
            continue
        files.append(path)

    return sorted(files)


PYTHON_FILES = _iter_python_files(REPO_ROOT)


@pytest.mark.parametrize(
    "python_file",
    PYTHON_FILES,
    ids=[str(path.relative_to(REPO_ROOT)) for path in PYTHON_FILES],
)
def test_python_file_has_valid_syntax(python_file: Path) -> None:
    # tokenize.open() respects PEP 263 encoding declarations.
    with tokenize.open(python_file) as handle:
        source = handle.read()

    compile(source, str(python_file), "exec")
