# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
from typing import Set, Tuple, Dict, Union
from .grid_state import GridStateManager, Cell, DEFAULT_THREAD_COLOR
from .grid_mapper import grid_to_svg

# Aida/linen look colours
_BG_COLOUR       = wx.Colour(237, 232, 220)   # parchment/linen
_GRID_MINOR      = wx.Colour(195, 185, 170)   # subtle minor lines
_GRID_MAJOR      = wx.Colour(150, 138, 120)   # every-10 major lines
_GRID_MINOR5     = wx.Colour(170, 160, 145)   # every-5 lines

# Proportion of cell width used as padding so stitches don't touch grid lines.
# Must match _CROSS_MARGIN_RATIO in build_export.py to keep screen and export consistent.
_CELL_PAD_RATIO = 0.15

# Stroke width as a fraction of cell size; approximates real thread thickness visually.
_STROKE_WIDTH_RATIO = 0.13


class GridVisualizer:
    _DIRTY_ALL = object()  # sentinel meaning "repaint the entire canvas"

    def __init__(self, parent_window: wx.Window, cell_size: float):
        self.window    = parent_window
        self.cell_size = cell_size          
        self.scale:    float = 1.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0

        self.dpi_scale: float = self._compute_dpi_scale()
        self.dirty_cells: Union[Set[Tuple[int, int]], object] = set()

    # ── DPI ─────────────────────────────────────────────────────────────
    def _compute_dpi_scale(self) -> float:
        if hasattr(self.window, "GetContentScaleFactor"):
            return self.window.GetContentScaleFactor()
        elif hasattr(self.window, "GetDPIScaleFactor"):
            return self.window.GetDPIScaleFactor()
        return 1.0

    # ── Dirty region management ──────────────────────────────────────────
    def mark_dirty(self, row: int, col: int) -> None:
        if self.dirty_cells is self._DIRTY_ALL:
            return
        self.dirty_cells.add((row, col))  # type: ignore[union-attr]

    def mark_all_dirty(self, _state: GridStateManager) -> None:
        """Signal that the entire canvas needs repainting on next render."""
        self.dirty_cells = self._DIRTY_ALL

    def request_render(self, state: GridStateManager) -> None:
        if not self.dirty_cells:
            return
        if self.dirty_cells is self._DIRTY_ALL:
            self.dirty_cells = set()
            wx.CallAfter(self._flush_dirty_as_region, self._DIRTY_ALL, state)
            return
        cells = self.dirty_cells.copy()  # type: ignore[union-attr]
        self.dirty_cells.clear()  # type: ignore[union-attr]
        wx.CallAfter(self._flush_dirty_as_region, cells, state)

    def _flush_dirty_as_region(self, cells: Union[Set[Tuple[int, int]], object],
                                state: GridStateManager) -> None:
        if not cells:
            return
        if cells is self._DIRTY_ALL:
            self.window.Refresh()
            return
            
        threshold = state.rows * state.cols * 0.30
        if len(cells) > threshold:  # type: ignore[arg-type]
            self.window.Refresh()
            return

        min_r = min_c = float('inf')
        max_r = max_c = float('-inf')
        for r, c in cells:  # type: ignore[union-attr]
            if r < min_r: min_r = r
            if r > max_r: max_r = r
            if c < min_c: min_c = c
            if c > max_c: max_c = c

        x1, y1 = self.logical_to_screen(int(min_r), int(min_c))
        x2, y2 = self.logical_to_screen(int(max_r) + 1, int(max_c) + 1)
        rect = wx.Rect(int(x1) - 2, int(y1) - 2,
                       int(x2 - x1) + 4, int(y2 - y1) + 4)
        self.window.RefreshRect(rect, eraseBackground=False)

    # ── Coordinate helpers ───────────────────────────────────────────────
    def logical_to_screen(self, row: int, col: int) -> Tuple[float, float]:
        """Grid (row, col) → screen pixel, applying zoom and pan only.

        HiDPI scaling is handled by wx internally when drawing with
        wx.BufferedPaintDC; we must NOT double-apply it here.
        """
        svg_x, svg_y = grid_to_svg(row, col, self.cell_size)
        screen_x = svg_x * self.scale + self.offset_x
        screen_y = svg_y * self.scale + self.offset_y
        return screen_x, screen_y

    def screen_cell_size(self) -> float:
        """Effective cell size in screen pixels at current zoom."""
        return self.cell_size * self.scale

    # ── Main paint entry point ───────────────────────────────────────────
    def on_paint(self, event: wx.PaintEvent, state: GridStateManager,
                 palette_colors: Dict[str, str]) -> None:
        """Handle a wx paint event by redrawing the full canvas.
        
        palette_colors maps thread_id strings to hex colour strings.
        Falls back to DEFAULT_THREAD_COLOR for any thread_id not in the palette.
        """
        dc = wx.BufferedPaintDC(self.window)
        dc.SetBackground(wx.Brush(_BG_COLOUR))
        dc.Clear()
        self._draw_grid_lines(dc, state)
        for (r, c), cell in state.cells.items():
            self._draw_cell(dc, r, c, cell, palette_colors)

    # ── Grid lines ───────────────────────────────────────────────────────
    def _draw_grid_lines(self, dc: wx.DC, state: GridStateManager) -> None:
        """Draw major and minor grid lines on the DC.
        
        Clips drawing to the visible screen area to optimize rendering performance.
        """
        # Pre-create pens ONCE — wx.Pen allocates a native GDI handle;
        # constructing one per grid-line (160+ per frame) causes GDI handle churn.
        pen_major = wx.Pen(_GRID_MAJOR, 1)
        pen_minor5 = wx.Pen(_GRID_MINOR5, 1)
        pen_minor  = wx.Pen(_GRID_MINOR,  1)

        # Clip to visible area so we skip off-screen lines cheaply
        size = self.window.GetClientSize()
        w, h = size.GetWidth(), size.GetHeight()

        for r in range(state.rows + 1):
            start_x, start_y = self.logical_to_screen(r, 0)
            screen_y = int(start_y)
            if screen_y < -2 or screen_y > h + 2:
                continue
            if r % 10 == 0:
                dc.SetPen(pen_major)
            elif r % 5 == 0:
                dc.SetPen(pen_minor5)
            else:
                dc.SetPen(pen_minor)
            end_x, _ = self.logical_to_screen(r, state.cols)
            dc.DrawLine(int(start_x), screen_y, int(end_x), screen_y)

        for c in range(state.cols + 1):
            start_x, start_y = self.logical_to_screen(0, c)
            screen_x = int(start_x)
            if screen_x < -2 or screen_x > w + 2:
                continue
            if c % 10 == 0:
                dc.SetPen(pen_major)
            elif c % 5 == 0:
                dc.SetPen(pen_minor5)
            else:
                dc.SetPen(pen_minor)
            _, end_y = self.logical_to_screen(state.rows, c)
            dc.DrawLine(screen_x, int(start_y), screen_x, int(end_y))

    # ── Cross stitch cell rendering ──────────────────────────────────────
    def _draw_cell(self, dc: wx.DC, r: int, c: int, cell: Cell,
                   palette_colors: Dict[str, str]) -> None:
        """Draw an individual cross-stitch cell as a diagonal X.
        
        Applies cell padding ratio and stroke width ratio for premium visual rendering.
        """
        tid = cell.thread_id or DEFAULT_THREAD_COLOR
        hex_col = palette_colors.get(tid, DEFAULT_THREAD_COLOR)

        sx1, sy1 = self.logical_to_screen(r,     c)
        sx2, sy2 = self.logical_to_screen(r + 1, c + 1)
        cell_px = sx2 - sx1

        stroke_w = max(1.0, cell_px * _STROKE_WIDTH_RATIO)
        colour   = wx.Colour(hex_col)

        pen = wx.Pen(colour, round(stroke_w), wx.PENSTYLE_SOLID)
        pen.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 0), wx.BRUSHSTYLE_TRANSPARENT))

        # Inset so stitches don't touch the grid lines
        pad = cell_px * _CELL_PAD_RATIO
        x1, y1 = sx1 + pad, sy1 + pad
        x2, y2 = sx2 - pad, sy2 - pad

        dc.DrawLine(int(x1), int(y1), int(x2), int(y2))
        dc.DrawLine(int(x1), int(y2), int(x2), int(y1))
        