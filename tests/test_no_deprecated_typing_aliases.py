from __future__ import annotations

import ast
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

# PEP 585: collection-style typing aliases from typing are deprecated in favor
# of built-in generics (list[str], dict[str, int], type[Foo], ...).
DEPRECATED_TYPING_ALIASES = {
    "AbstractSet",
    "AsyncContextManager",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "ByteString",
    "Callable",
    "ChainMap",
    "Collection",
    "Container",
    "ContextManager",
    "Coroutine",
    "Counter",
    "DefaultDict",
    "Deque",
    "Dict",
    "FrozenSet",
    "Generator",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "List",
    "Mapping",
    "MappingView",
    "Match",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "OrderedDict",
    "Pattern",
    "Reversible",
    "Sequence",
    "Set",
    "Tuple",
    "Type",
    "ValuesView",
}


class DeprecatedTypingAliasVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.typing_module_aliases: set[str] = set()
        self.issues: list[tuple[int, int, str]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name == "typing":
                self.typing_module_aliases.add(alias.asname or "typing")

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "typing":
            for alias in node.names:
                if alias.name in DEPRECATED_TYPING_ALIASES:
                    self.issues.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f"from typing import {alias.name}",
                        )
                    )

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name):
            if node.value.id in self.typing_module_aliases and node.attr in DEPRECATED_TYPING_ALIASES:
                self.issues.append(
                    (
                        node.lineno,
                        node.col_offset,
                        f"{node.value.id}.{node.attr}",
                    )
                )

        self.generic_visit(node)


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


def test_no_deprecated_typing_aliases() -> None:
    violations: list[str] = []

    for python_file in _iter_python_files(REPO_ROOT):
        with tokenize.open(python_file) as handle:
            source = handle.read()

        tree = ast.parse(source, filename=str(python_file))
        visitor = DeprecatedTypingAliasVisitor()
        visitor.visit(tree)

        for line, col, symbol in visitor.issues:
            rel_path = python_file.relative_to(REPO_ROOT)
            violations.append(f"{rel_path}:{line}:{col + 1}: deprecated typing alias '{symbol}'")

    if violations:
        details = "\n".join(violations)
        pytest.fail(
            "Deprecated typing aliases from 'typing' were found. "
            "Use built-in generics (list/dict/tuple/type/...) for Python >= 3.9.\n"
            f"{details}"
        )
