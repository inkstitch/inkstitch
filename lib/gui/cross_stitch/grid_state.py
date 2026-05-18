# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.
# See the file LICENSE for details.
from typing import Dict, Tuple, Optional

# Enforce maximum bounds early to prevent performance disasters
MAX_ROWS = 100
MAX_COLS = 100

DEFAULT_STITCH = "full"
DEFAULT_THREAD = None
DEFAULT_THREAD_COLOR = "#444444"  # fallback for cells with no assigned thread


class Cell:
    """
    Explicit lightweight representation of a single stitch to minimize memory.

    Immutability Contract: Cell objects must never be mutated after insertion.
    Always replace the entire Cell object in the GridStateManager to prevent
    subtle undo corruption.
    """
    __slots__ = ("thread_id", "stitch_type", "direction", "locked")

    def __init__(self, thread_id: Optional[str] = DEFAULT_THREAD,
                 stitch_type: str = DEFAULT_STITCH,
                 direction: Optional[str] = None,
                 locked: bool = False):
        self.thread_id = thread_id
        self.stitch_type = stitch_type
        self.direction = direction
        self.locked = locked


class GridStateManager:
    """
    Pure logic state container supporting sparse mapping for optimization.
    """
    def __init__(self, rows: int = 50, cols: int = 50):
        if not (1 <= rows <= MAX_ROWS):
            raise ValueError(f"rows must be between 1 and {MAX_ROWS}")
        if not (1 <= cols <= MAX_COLS):
            raise ValueError(f"cols must be between 1 and {MAX_COLS}")

        self.rows = rows
        self.cols = cols
        # Sparse Cell Storage: stores only painted cells
        self.cells: Dict[Tuple[int, int], Cell] = {}

    def in_bounds(self, row: int, col: int) -> bool:
        """Check if grid coordinates are valid."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def set_cell(self, row: int, col: int, cell: Cell) -> None:
        """
        Assign a Cell object to a grid coordinate.
        Must replace the object, never mutate an existing one.
        """
        if not self.in_bounds(row, col):
            raise ValueError(f"Coordinate ({row}, {col}) out of bounds")
        self.cells[(row, col)] = cell

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get the specific cell or None if empty/unpainted."""
        if not self.in_bounds(row, col):
            raise ValueError(f"Coordinate ({row}, {col}) out of bounds")
        return self.cells.get((row, col))

    def clear_cell(self, row: int, col: int) -> None:
        """Remove a cell from the sparse mapping."""
        if not self.in_bounds(row, col):
            raise ValueError(f"Coordinate ({row}, {col}) out of bounds")
        if (row, col) in self.cells:
            del self.cells[(row, col)]

    def clone(self) -> 'GridStateManager':
        """High-speed sparse dict copy.

        Creates an independent deep copy with no shared cell references,
        completely avoiding Python's slow copy.deepcopy() to hit
        performance targets.
        """
        new_state = GridStateManager(self.rows, self.cols)
        # Reinstantiate each Cell manually to enforce undo immutability
        for pos, cell in self.cells.items():
            new_state.cells[pos] = Cell(
                thread_id=cell.thread_id,
                stitch_type=cell.stitch_type,
                direction=cell.direction,
                locked=cell.locked
            )
        return new_state