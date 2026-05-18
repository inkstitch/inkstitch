# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""Coordinate conversion utilities between grid (row, col) and SVG (x, y) space."""

from typing import Tuple


def grid_to_svg(row: int, col: int, cell_size: float) -> Tuple[float, float]:
    """Convert grid cell coordinates to SVG user-unit coordinates.

    The grid origin (0, 0) maps to SVG origin (0, 0), with rows increasing
    downward (Y axis) and columns increasing rightward (X axis).

    Returns:
        (x, y) position of the top-left corner of the cell in SVG units.
    """
    return col * cell_size, row * cell_size


def svg_to_grid(
    x: float,
    y: float,
    cell_size: float,
    max_rows: int,
    max_cols: int,
) -> Tuple[int, int]:
    """Convert an SVG coordinate to the nearest grid cell, clamped to bounds.

    Raises:
        ValueError: if cell_size, max_rows, or max_cols are zero or negative.

    Returns:
        (row, col) of the cell containing the given SVG point.
    """
    if cell_size <= 0:
        raise ValueError(f"cell_size must be positive, got {cell_size!r}")
    if max_rows <= 0 or max_cols <= 0:
        raise ValueError(
            f"max_rows and max_cols must be positive, got {max_rows!r} and {max_cols!r}"
        )

    row = max(0, min(max_rows - 1, int(y // cell_size)))
    col = max(0, min(max_cols - 1, int(x // cell_size)))
    return row, col