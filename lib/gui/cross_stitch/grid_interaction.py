# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import Optional, Tuple, List
from .grid_state import GridStateManager, Cell
from .grid_mapper import svg_to_grid
from .grid_visualizer import GridVisualizer
from .undo_manager import UndoManager


class GridInteractionEngine:
    def __init__(self, visualizer: GridVisualizer, state: GridStateManager, undo_mgr: UndoManager):
        self.visualizer = visualizer
        self.state = state
        self.undo_mgr = undo_mgr

        # Toolstate (Default Phase 1 implementations)
        self.current_tool = "pencil"  # "eraser", "pencil"
        self.active_thread: Optional[str] = None

        # Drag sequence tracking
        self.is_dragging = False
        self.last_cell: Optional[Tuple[int, int]] = None

    def screen_to_logical(self, screen_x: float, screen_y: float) -> Tuple[int, int]:
        """
        Inverse math transforming GUI input coordinates through HiDPI, Zoom, and Pan into local SVG coordinates.
        """
        # 1. Reverse HiDPI tracking
        zoom_x = screen_x / self.visualizer.dpi_scale
        zoom_y = screen_y / self.visualizer.dpi_scale

        # 2. Reverse User Zoom/Pan
        svg_x = (zoom_x - self.visualizer.offset_x) / self.visualizer.scale
        svg_y = (zoom_y - self.visualizer.offset_y) / self.visualizer.scale

        # 3. Resolve using pure domain mapper (Handles bounds clamping automatically)
        return svg_to_grid(svg_x, svg_y, self.visualizer.cell_size, self.state.rows, self.state.cols)

    def on_mouse_down(self, x: float, y: float) -> None:
        self.is_dragging = True

        # UX Rule: Snapshots MUST trigger only once at the beginning of an action
        # (Allows sweeping strokes to act as 1 undo frame)
        self.undo_mgr.save_state(self.state)

        r, c = self.screen_to_logical(x, y)
        self._apply_tool(r, c)
        self.last_cell = (r, c)

        # Fire single emission
        self.visualizer.request_render(self.state)

    def on_mouse_up(self, x: float, y: float) -> bool:
        self.is_dragging = False
        self.last_cell = None
        return False

    def on_mouse_move(self, x: float, y: float) -> bool:
        if not self.is_dragging:
            return False

        if self.current_tool in ("fill", "fill_eraser"):
            return False

        r, c = self.screen_to_logical(x, y)

        # Critical Draw Coalescing Limit: block out stuttering updates and redundant undo frames
        if (r, c) == self.last_cell:
            return False

        modified = False
        # Draw Bresenham interpolation line avoiding chopped drag trails when OS event polling lags
        if self.last_cell:
            for br, bc in self._bresenham_line(self.last_cell[0], self.last_cell[1], r, c):
                if self._apply_tool(br, bc):
                    modified = True
        else:
            if self._apply_tool(r, c):
                modified = True

        self.last_cell = (r, c)

        # Queue emission bound to CallAfter region bounds to prevent synchronous stall
        self.visualizer.request_render(self.state)
        return modified

    def _apply_tool(self, r: int, c: int) -> bool:
        """Mutates the data layer according to tool context. Returns True if a change actually occurred."""
        if self.current_tool == "pencil":
            existing = self.state.get_cell(r, c)
            if existing and existing.thread_id == self.active_thread and existing.stitch_type == "full":
                return False
            # Immutable instantiation pattern
            new_cell = Cell(
                thread_id=self.active_thread,
                stitch_type="full",
                direction=None,
                locked=False
            )
            self.state.set_cell(r, c, new_cell)
            self.visualizer.mark_dirty(r, c)
            return True
        elif self.current_tool == "eraser":
            existing = self.state.get_cell(r, c)
            if existing is None:
                return False
            self.state.clear_cell(r, c)
            self.visualizer.mark_dirty(r, c)
            return True
        elif self.current_tool == "fill":
            return self._flood_fill(r, c, self.active_thread)
        elif self.current_tool == "fill_eraser":
            return self._flood_fill(r, c, None)
        return False

    def _flood_fill(self, r: int, c: int, replacement_color: Optional[str]) -> bool:
        """
        Flood fill starting at (r, c).
        Fills contiguous cells that have the same thread_id as the clicked cell with replacement_color.
        """
        if not self.state.in_bounds(r, c):
            return False

        # Find the starting thread ID
        start_cell = self.state.get_cell(r, c)
        target_color = start_cell.thread_id if start_cell else None

        # If the target color is already the replacement color, nothing to do!
        if target_color == replacement_color:
            return False

        # Queue for BFS (breadth-first search)
        queue = [(r, c)]
        visited = {(r, c)}

        # Collect all cells to change
        cells_to_change = []

        while queue:
            curr_r, curr_c = queue.pop(0)
            cells_to_change.append((curr_r, curr_c))

            # Check 4-connected neighbors: up, down, left, right
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = curr_r + dr, curr_c + dc
                if self.state.in_bounds(nr, nc) and (nr, nc) not in visited:
                    neighbor_cell = self.state.get_cell(nr, nc)
                    neighbor_color = neighbor_cell.thread_id if neighbor_cell else None
                    if neighbor_color == target_color:
                        visited.add((nr, nc))
                        queue.append((nr, nc))

        # Now apply the replacement to all identified cells
        if not cells_to_change:
            return False

        for cr, cc in cells_to_change:
            if replacement_color is None:
                self.state.clear_cell(cr, cc)
            else:
                new_cell = Cell(
                    thread_id=replacement_color,
                    stitch_type="full",
                    direction=None,
                    locked=False
                )
                self.state.set_cell(cr, cc, new_cell)
            self.visualizer.mark_dirty(cr, cc)

        return True

    def _bresenham_line(self, r0: int, c0: int, r1: int, c1: int) -> List[Tuple[int, int]]:
        """
        Fill every grid cell on the straight line between two points.

        Why this is necessary: OS mouse-move events fire at 60–125 Hz, but a
        user can physically move the mouse fast enough to jump 5–10 cells between
        consecutive EVT_MOTION events. Without interpolation, fast strokes leave
        visible gaps in the painted trail. Bresenham gives us the exact integer
        cell path between the last reported cell and the current one, so every
        intermediate cell is painted even when the OS skipped reporting it.
        """
        pixels = []
        dr = abs(r1 - r0)
        dc = abs(c1 - c0)

        sr = 1 if r0 < r1 else -1
        sc = 1 if c0 < c1 else -1

        err = dc - dr

        while True:
            pixels.append((r0, c0))
            if r0 == r1 and c0 == c1:
                break
            e2 = 2 * err
            if e2 > -dr:
                err -= dr
                c0 += sc
            if e2 < dc:
                err += dc
                r0 += sr
        return pixels