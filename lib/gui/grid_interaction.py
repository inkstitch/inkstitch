"""
Interaction Engine.

Maps raw physical events (drag, click) into pure geometric cell coordinates, generating
state payloads that the visualizer and data manager consume.
"""

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
        self.current_tool = "pencil" # "eraser", "pencil"
        self.active_thread = None
        
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

    def on_mouse_up(self, x: float, y: float) -> None:
        self.is_dragging = False
        self.last_cell = None

    def on_mouse_move(self, x: float, y: float) -> None:
        if not self.is_dragging:
            return
            
        r, c = self.screen_to_logical(x, y)
        
        # Critical Draw Coalescing Limit: block out stuttering updates and redundant undo frames
        if (r, c) == self.last_cell:
            return
            
        # Draw Bresenham interpolation line avoiding chopped drag trails when OS event polling lags
        if self.last_cell:
            for br, bc in self._bresenham_line(self.last_cell[0], self.last_cell[1], r, c):
                self._apply_tool(br, bc)
        else:
            self._apply_tool(r, c)
            
        self.last_cell = (r, c)
        
        # Queue emission bound to CallAfter region bounds to prevent synchronous stall
        self.visualizer.request_render(self.state)

    def _apply_tool(self, r: int, c: int) -> None:
        """Mutates the data layer according to tool context."""
        if self.current_tool == "pencil":
            # Immutable instantiation pattern
            new_cell = Cell(
                thread_id=self.active_thread, 
                stitch_type="full", 
                direction=None, 
                locked=False
            )
            self.state.set_cell(r, c, new_cell)
            self.visualizer.mark_dirty(r, c)
            
        elif self.current_tool == "eraser":
            self.state.clear_cell(r, c)
            self.visualizer.mark_dirty(r, c)

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