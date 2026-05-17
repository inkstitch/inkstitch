from typing import Dict, List, Tuple
from .grid_state import Cell


class Rect:
    """Bounding representation of compressed grid cells."""
    __slots__ = ("row", "col", "width", "height")
    
    def __init__(self, row: int, col: int, width: int = 1, height: int = 1):
        self.row = row
        self.col = col
        self.width = width
        self.height = height


def merge_runs(cells_by_thread: Dict[Tuple[int, int], Cell], horizontal_only: bool = True) -> List[Rect]:
    """
    Compress continuous painted cells of the same color into horizontal chunks.
    
    Args:
        cells_by_thread: Dictionary of (row, col) mapping to Cell objects
                         (assumed to all belong to the SAME thread_id during Phase 1 usage)
        horizontal_only: If true, stops at horizontal sweeps.
        
    Returns:
        List of Rect objects bounding the contiguous cells.
    """
    if not cells_by_thread:
        return []
        
    # Phase 1: Horizontal only
    # Group cells by row, then sort by col to establish contiguous runs
    rows: Dict[int, List[int]] = {}
    for (r, c) in cells_by_thread.keys():
        if r not in rows:
            rows[r] = []
        rows[r].append(c)
        
    rects = []
    
    for r in sorted(rows.keys()):
        cols = sorted(rows[r])
        
        current_col_start = cols[0]
        current_col_prev = cols[0]
        
        for i in range(1, len(cols)):
            c = cols[i]
            if c == current_col_prev + 1:
                # Contiguous
                current_col_prev = c
            else:
                # Run breaks; offload the constructed block
                width = current_col_prev - current_col_start + 1
                rects.append(Rect(row=r, col=current_col_start, width=width, height=1))
                
                # Setup new run
                current_col_start = c
                current_col_prev = c
                
        # Close out the last run in the row trajectory
        width = current_col_prev - current_col_start + 1
        rects.append(Rect(row=r, col=current_col_start, width=width, height=1))
        
    return rects