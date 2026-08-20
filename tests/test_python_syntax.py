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


def _iter_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
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
