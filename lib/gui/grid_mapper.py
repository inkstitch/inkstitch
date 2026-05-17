"""
Coordinate mapping for the Cross Stitch Canvas tool.

Provides the single source of truth for converting between logical grid
cell indices and local SVG space coordinates.

All functions produce and consume LOCAL coordinates only — they are unaware
of document scaling, SVG layer transforms, or device HiDPI scaling.
Callers are responsible for:
    - Applying `correction_transform` at the group level before export.
    - Translating mouse coordinates (HiDPI + zoom/pan) into local space
      before calling `svg_to_grid`.
"""

from typing import Tuple


def grid_to_svg(row: int, col: int, cell_size: float) -> Tuple[float, float]:
    """
    Convert a grid cell index to local SVG coordinates.

    Returns the top-left corner of the cell, not its centre.

    Args:
        row: 0-based row index (0 = top).
        col: 0-based column index (0 = left).
        cell_size: Cell size in document units (mm).

    Returns:
        (x, y) local SVG coordinates of the cell's top-left corner.
    """
    return col * cell_size,row * cell_size

def svg_to_grid(
    x: float,
    y: float,
    cell_size: float,
    max_rows: int,
    max_cols: int,
) -> Tuple[int, int]:
    """
    Convert local SVG coordinates to grid cell indices.

    Clamps results to valid grid bounds, so out-of-range mouse positions
    (e.g. drags past the canvas edge) map safely to the nearest cell.

    Args:
        x: Local SVG x coordinate.
        y: Local SVG y coordinate.
        cell_size: Cell size in document units (mm). Must be positive.
        max_rows: Number of rows in the grid (exclusive upper bound).
        max_cols: Number of columns in the grid (exclusive upper bound).

    Returns:
        (row, col) clamped to [0, max_rows - 1] × [0, max_cols - 1].

    Raises:
        ValueError: If cell_size is zero or negative.
    """
    if cell_size <= 0:
        raise ValueError(f"cell_size must be positive, got {cell_size!r}")

    row = max(0, min(max_rows - 1, int(y // cell_size)))
    col = max(0, min(max_cols - 1, int(x // cell_size)))
    return row, col