# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from typing import Tuple


def grid_to_svg(row: int, col: int, cell_size: float) -> Tuple[float, float]:
    return col * cell_size,row * cell_size

def svg_to_grid(
    x: float,
    y: float,
    cell_size: float,
    max_rows: int,
    max_cols: int,
) -> Tuple[int, int]:
    if cell_size <= 0:
        raise ValueError(f"cell_size must be positive, got {cell_size!r}")

    row = max(0, min(max_rows - 1, int(y // cell_size)))
    col = max(0, min(max_cols - 1, int(x // cell_size)))
    return row, col