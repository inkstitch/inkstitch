"""
Main window wrapper assembling the Cross Stitch Canvas GUI components.
Left toolbar, right palette panel (recently used + color picker),
ruler canvas, zoom/pan, and status bar.
"""

from __future__ import annotations

import logging
from typing import Callable, Dict, List, Optional, Set, Tuple

import wx
from .grid_state import GridStateManager
from .grid_visualizer import GridVisualizer
from .grid_interaction import GridInteractionEngine
from .undo_manager import UndoManager

logger = logging.getLogger(__name__)


class ThreadSwatchPanel(wx.Panel):
    """Clickable color swatch grid for 'Recently used colors'."""

    SWATCH_SIZE = 26

    def __init__(self, parent: wx.Window, callback: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.callback = callback
        self.colors: List[str] = []
        self.SetMinSize((-1, 80))
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)

    def set_colors(self, hex_list: List[str]) -> None:
        self.colors = hex_list[-15:]  # keep last 15
        self.Refresh()

    def _on_paint(self, _event: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)
        s = self.SWATCH_SIZE
        cols = max(1, self.GetSize().width // (s + 2))
        for i, hex_col in enumerate(self.colors):
            row, col = divmod(i, cols)
            x, y = col * (s + 2), row * (s + 2)
            dc.SetBrush(wx.Brush(wx.Colour(hex_col)))
            dc.SetPen(wx.Pen(wx.Colour(180, 180, 180), 1))
            dc.DrawRectangle(x, y, s, s)

    def _on_click(self, event: wx.MouseEvent) -> None:
        s = self.SWATCH_SIZE
        cols = max(1, self.GetSize().width // (s + 2))
        col = event.GetX() // (s + 2)
        row = event.GetY() // (s + 2)
        idx = row * cols + col
        if 0 <= idx < len(self.colors):
            self.callback(self.colors[idx])


class CrossStitchCanvasWindow(wx.Frame):
    def __init__(
        self,
        parent: Optional[wx.Window],
        title: str = "Cross Stitch Canvas",
        state: Optional[GridStateManager] = None,
    ) -> None:
        super().__init__(parent, title=title, size=(1280, 820))
        self.SetMinSize((900, 600))

        self.state = state or GridStateManager(rows=80, cols=80)
        self.undo_mgr = UndoManager(self.state)

        # Pan tracking
        self._pan_dragging = False
        self._pan_start = None

        # Recently used colors (ordered list, no dups)
        self._recent_colors = []

        # Per-thread stitch counts {hex: count}
        self._thread_counts = {}

        # Set True only when user explicitly clicks "Export to Inkscape".
        # Closing via the window X button leaves this False → extension skips export.
        self.export_confirmed = False

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self._init_ui()
        self._set_thread("#000000")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _init_ui(self) -> None:
        root = wx.BoxSizer(wx.HORIZONTAL)

        # ── Left vertical toolbar ──────────────────────────────────────
        root.Add(self._make_left_toolbar(), 0, wx.EXPAND)

        # ── Centre: ruler + canvas + status bar ───────────────────────
        centre = wx.BoxSizer(wx.VERTICAL)
        centre.Add(self._make_canvas_area(), 1, wx.EXPAND)
        centre.Add(self._make_status_bar(), 0, wx.EXPAND)
        root.Add(centre, 1, wx.EXPAND)

        # ── Right palette panel ────────────────────────────────────────
        root.Add(self._make_palette_panel(), 0, wx.EXPAND)

        self.SetSizer(root)
        self.Layout()

    # ── Left toolbar ───────────────────────────────────────────────────
    def _make_left_toolbar(self) -> wx.Panel:
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        panel.SetMinSize((48, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(8)

        def tb_btn(label, tip, handler):
            btn = wx.Button(panel, label=label, size=(40, 40),
                            style=wx.BORDER_NONE | wx.BU_EXACTFIT)
            btn.SetToolTip(tip)
            btn.Bind(wx.EVT_BUTTON, handler)
            sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER, 3)
            return btn

        tb_btn("Undo",   "Undo",         self.on_undo)
        tb_btn("Redo",   "Redo",         self.on_redo)
        sizer.AddSpacer(10)
        self._btn_pencil = tb_btn("Pencil", "Pencil", lambda e: self._select_tool("pencil"))
        self._btn_eraser = tb_btn("Eraser", "Eraser", lambda e: self._select_tool("eraser"))
        sizer.AddSpacer(10)
        tb_btn("Pick",   "Color Picker",  self.on_eyedropper)
        self._btn_pan    = tb_btn("Pan",  "Pan / Scroll", lambda e: self._select_tool("pan"))

        panel.SetSizer(sizer)
        self._highlight_tool("pencil")
        return panel

    # ── Canvas area (ruler + drawable panel) ──────────────────────────
    def _make_canvas_area(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Top horizontal ruler
        self.h_ruler = wx.Panel(self)
        self.h_ruler.SetMinSize((-1, 24))
        self.h_ruler.SetBackgroundColour(wx.Colour(230, 230, 230))
        self.h_ruler.Bind(wx.EVT_PAINT, self._on_paint_h_ruler)
        sizer.Add(self.h_ruler, 0, wx.EXPAND)

        # Row sizer for left vertical ruler + canvas
        row = wx.BoxSizer(wx.HORIZONTAL)

        self.v_ruler = wx.Panel(self)
        self.v_ruler.SetMinSize((28, -1))
        self.v_ruler.SetBackgroundColour(wx.Colour(230, 230, 230))
        self.v_ruler.Bind(wx.EVT_PAINT, self._on_paint_v_ruler)
        row.Add(self.v_ruler, 0, wx.EXPAND)

        # Main drawable canvas
        self.canvas_panel = wx.Panel(self)
        self.canvas_panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.canvas_panel.SetCursor(wx.Cursor(wx.CURSOR_PENCIL))

        cell_size = 12.0
        self.visualizer = GridVisualizer(self.canvas_panel, cell_size=cell_size)
        self.visualizer.offset_x = 0
        self.visualizer.offset_y = 0
        self.interaction = GridInteractionEngine(
            self.visualizer, self.state, self.undo_mgr
        )
        self.interaction.active_thread = "#000000"

        # Canvas events
        self.canvas_panel.Bind(wx.EVT_PAINT,       self.on_paint)
        self.canvas_panel.Bind(wx.EVT_LEFT_DOWN,   self.on_mouse_down)
        self.canvas_panel.Bind(wx.EVT_LEFT_UP,     self.on_mouse_up)
        self.canvas_panel.Bind(wx.EVT_MOTION,      self.on_mouse_move)
        self.canvas_panel.Bind(wx.EVT_MOUSEWHEEL,  self.on_mousewheel)
        self.canvas_panel.Bind(wx.EVT_MIDDLE_DOWN,  self.on_pan_start)
        self.canvas_panel.Bind(wx.EVT_MIDDLE_UP,   self.on_pan_end)

        row.Add(self.canvas_panel, 1, wx.EXPAND)
        sizer.Add(row, 1, wx.EXPAND)
        return sizer

    # ── Status bar ────────────────────────────────────────────────────
    def _make_status_bar(self) -> wx.Panel:
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(235, 235, 235))
        panel.SetMinSize((-1, 28))
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(wx.StaticText(panel, label="Zoom:"), 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)
        self._zoom_slider = wx.Slider(panel, minValue=25, maxValue=400,
                                      value=100, size=(120, -1))
        self._zoom_slider.Bind(wx.EVT_SLIDER, self.on_zoom_slider)
        sizer.Add(self._zoom_slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 4)

        self._zoom_label = wx.StaticText(panel, label="100%")
        sizer.Add(self._zoom_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 4)

        sizer.AddSpacer(20)
        self._coord_label = wx.StaticText(panel, label="Mouse: --:--")
        sizer.Add(self._coord_label, 0, wx.ALIGN_CENTER_VERTICAL)

        sizer.AddSpacer(20)
        self._tool_label = wx.StaticText(panel, label="Current Tool: Pencil")
        sizer.Add(self._tool_label, 0, wx.ALIGN_CENTER_VERTICAL)

        sizer.AddSpacer(20)
        self._count_label = wx.StaticText(panel, label="Total: 0")
        sizer.Add(self._count_label, 0, wx.ALIGN_CENTER_VERTICAL)

        panel.SetSizer(sizer)
        return panel

    # ── Right palette panel ───────────────────────────────────────────
    def _make_palette_panel(self) -> wx.Panel:
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(252, 252, 252))
        panel.SetMinSize((220, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Color & Palette")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                              wx.FONTWEIGHT_BOLD))
        sizer.Add(title, 0, wx.ALL, 10)

        # ── Current color ──────────────────────────────────────────────
        sizer.Add(wx.StaticText(panel, label="Current Color"), 0,
                  wx.LEFT | wx.RIGHT, 10)
        curr_row = wx.BoxSizer(wx.HORIZONTAL)
        self._curr_swatch = wx.Panel(panel, size=(36, 36))
        self._curr_swatch.SetBackgroundColour(wx.Colour("#000000"))
        curr_row.Add(self._curr_swatch, 0, wx.ALL, 4)
        info_col = wx.BoxSizer(wx.VERTICAL)
        self._curr_hex   = wx.StaticText(panel, label="#000000")
        self._curr_count = wx.StaticText(panel, label="Count    0")
        self._curr_hex.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        info_col.Add(self._curr_hex,   0)
        info_col.Add(self._curr_count, 0)
        curr_row.Add(info_col, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(curr_row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 6)

        # ── Color picker ───────────────────────────────────────────────
        sizer.Add(wx.StaticText(panel, label="Pick Color"), 0,
                  wx.LEFT | wx.RIGHT | wx.BOTTOM, 4)
        self._color_picker = wx.ColourPickerCtrl(panel, colour=wx.Colour("#000000"))
        self._color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, self._on_color_picked)
        sizer.Add(self._color_picker, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 6)

        # ── Recently used ─────────────────────────────────────────────
        sizer.Add(wx.StaticText(panel, label="Recently Used"), 0,
                  wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        self._recent_panel = ThreadSwatchPanel(panel, self._on_recent_swatch_click)
        sizer.Add(self._recent_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        sizer.AddStretchSpacer()
        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 6)

        # ── Export / Cancel ───────────────────────────────────────────
        export_btn = wx.Button(panel, label="Export to Inkscape")
        export_btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        export_btn.SetBackgroundColour(wx.Colour(60, 140, 60))
        export_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        export_btn.SetToolTip("Write the cross-stitch grid back into the Inkscape document and close")
        export_btn.Bind(wx.EVT_BUTTON, self.on_export)
        sizer.Add(export_btn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.SetToolTip("Close without exporting")
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        sizer.Add(cancel_btn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(sizer)
        return panel

    # ------------------------------------------------------------------
    # Color selection helpers
    # ------------------------------------------------------------------
    def _set_thread(self, hex_col: str) -> None:
        """Set the active drawing color and update UI."""
        self.interaction.active_thread = hex_col
        self._curr_swatch.SetBackgroundColour(wx.Colour(hex_col))
        self._curr_swatch.Refresh()
        self._curr_hex.SetLabel(hex_col.upper())
        cnt = self._thread_counts.get(hex_col, 0)
        self._curr_count.SetLabel(f"Count    {cnt}")
        # Update recently used list (dedup, most-recent last)
        if hex_col in self._recent_colors:
            self._recent_colors.remove(hex_col)
        self._recent_colors.append(hex_col)
        self._recent_panel.set_colors(self._recent_colors)

    def _on_color_picked(self, event: wx.ColourPickerEvent) -> None:
        col = self._color_picker.GetColour()  # read from widget, not event (more reliable)
        hex_col = "#%02X%02X%02X" % (col.Red(), col.Green(), col.Blue())
        self._set_thread(hex_col)

    def _on_recent_swatch_click(self, hex_col: str) -> None:
        self._set_thread(hex_col)
        # Sync the colour picker to show the selected colour
        self._color_picker.SetColour(wx.Colour(hex_col))

    # ------------------------------------------------------------------
    # Tool selection
    # ------------------------------------------------------------------
    def _select_tool(self, tool: str) -> None:
        self.interaction.current_tool = tool
        self._highlight_tool(tool)
        self._tool_label.SetLabel(f"Current Tool: {tool.capitalize()}")
        if tool == "pan":
            self.canvas_panel.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        elif tool == "eraser":
            self.canvas_panel.SetCursor(wx.Cursor(wx.CURSOR_BULLSEYE))
        else:
            self.canvas_panel.SetCursor(wx.Cursor(wx.CURSOR_PENCIL))

    def _highlight_tool(self, tool: str) -> None:
        for attr, t in [("_btn_pencil", "pencil"),
                        ("_btn_eraser", "eraser"),
                        ("_btn_pan",    "pan")]:
            btn = getattr(self, attr, None)
            if btn:
                btn.SetBackgroundColour(
                    wx.Colour(180, 210, 255) if t == tool else wx.NullColour)
                btn.Refresh()

    # ------------------------------------------------------------------
    # Ruler painting
    # ------------------------------------------------------------------
    def _on_paint_h_ruler(self, _event: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self.h_ruler)
        dc.SetBackground(wx.Brush(wx.Colour(230, 230, 230)))
        dc.Clear()
        dc.SetFont(wx.Font(7, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        cell = self.visualizer.cell_size * self.visualizer.scale
        offset = self.visualizer.offset_x
        left_margin = self.v_ruler.GetSize().width
        width = self.h_ruler.GetClientSize().width
        for col in range(self.state.cols + 1):
            x = int(col * cell + offset + left_margin)
            if x < -20 or x > width + 20:
                continue
            if col % 10 == 0:
                dc.DrawLine(x, 14, x, 24)
                dc.DrawText(str(col), x + 2, 2)
            elif col % 5 == 0:
                dc.DrawLine(x, 18, x, 24)

    def _on_paint_v_ruler(self, _event: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self.v_ruler)
        dc.SetBackground(wx.Brush(wx.Colour(230, 230, 230)))
        dc.Clear()
        dc.SetFont(wx.Font(7, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        cell = self.visualizer.cell_size * self.visualizer.scale
        offset = self.visualizer.offset_y
        for row in range(self.state.rows + 1):
            y = int(row * cell + offset)
            if row % 10 == 0:
                dc.DrawLine(18, y, 28, y)
                dc.DrawText(str(row), 1, y + 2)
            elif row % 5 == 0:
                dc.DrawLine(22, y, 28, y)

    # ------------------------------------------------------------------
    # Canvas events
    # ------------------------------------------------------------------
    def on_paint(self, event: wx.PaintEvent) -> None:
        palette = {tid: tid for tid in self._get_unique_threads()}
        self.visualizer.on_paint(event, self.state, palette)

    def on_mouse_down(self, event: wx.MouseEvent) -> None:
        if self.interaction.current_tool == "pan":
            self._pan_dragging = True
            self._pan_start = event.GetPosition()
            return
        self.interaction.on_mouse_down(event.GetX(), event.GetY())
        self._update_counts()

    def on_mouse_up(self, event: wx.MouseEvent) -> None:
        self._pan_dragging = False
        self._pan_start = None
        self.interaction.on_mouse_up(event.GetX(), event.GetY())

    def on_mouse_move(self, event: wx.MouseEvent) -> None:
        x, y = event.GetX(), event.GetY()
        r, c = self.interaction.screen_to_logical(x, y)
        self._coord_label.SetLabel(f"Mouse: {r}:{c}")

        if self._pan_dragging and self._pan_start:
            dx = x - self._pan_start[0]
            dy = y - self._pan_start[1]
            self.visualizer.offset_x += dx
            self.visualizer.offset_y += dy
            self._pan_start = event.GetPosition()
            self._refresh_rulers()
            self.canvas_panel.Refresh()
            return

        if event.Dragging() and event.LeftIsDown():
            self.interaction.on_mouse_move(x, y)
            self._update_counts()

    def on_mousewheel(self, event: wx.MouseEvent) -> None:
        rotation = event.GetWheelRotation()
        factor = 1.1 if rotation > 0 else 0.9
        old_scale = self.visualizer.scale
        new_scale = max(0.25, min(4.0, old_scale * factor))
        mx, my = event.GetX(), event.GetY()
        self.visualizer.offset_x = mx - (mx - self.visualizer.offset_x) * (new_scale / old_scale)
        self.visualizer.offset_y = my - (my - self.visualizer.offset_y) * (new_scale / old_scale)
        self.visualizer.scale = new_scale
        pct = int(new_scale * 100)
        self._zoom_slider.SetValue(pct)
        self._zoom_label.SetLabel(f"{pct}%")
        self._refresh_rulers()
        self.canvas_panel.Refresh()

    def on_zoom_slider(self, event: wx.CommandEvent) -> None:
        pct = self._zoom_slider.GetValue()
        self.visualizer.scale = pct / 100.0
        self._zoom_label.SetLabel(f"{pct}%")
        self._refresh_rulers()
        self.canvas_panel.Refresh()

    def on_pan_start(self, event: wx.MouseEvent) -> None:
        self._pan_dragging = True
        self._pan_start = event.GetPosition()

    def on_pan_end(self, _event: wx.MouseEvent) -> None:
        self._pan_dragging = False
        self._pan_start = None

    def on_eyedropper(self, _event):
        """Open color dialog to pick any custom color."""
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            col = dlg.GetColourData().GetColour()
            hex_col = "#%02X%02X%02X" % (col.Red(), col.Green(), col.Blue())
            self._set_thread(hex_col)
            self._color_picker.SetColour(wx.Colour(hex_col))
        dlg.Destroy()

    def on_undo(self, _event: wx.CommandEvent) -> None:
        new_state = self.undo_mgr.undo(self.state)
        if new_state is not self.state:
            self.state = new_state
            self.interaction.state = self.state
            self.visualizer.mark_all_dirty(self.state)
            self.canvas_panel.Refresh()
            self._update_counts()

    def on_redo(self, _event: wx.CommandEvent) -> None:
        new_state = self.undo_mgr.redo(self.state)
        if new_state is not self.state:
            self.state = new_state
            self.interaction.state = self.state
            self.visualizer.mark_all_dirty(self.state)
            self.canvas_panel.Refresh()
            self._update_counts()

    def on_export(self, _event: wx.CommandEvent) -> None:
        """User explicitly confirmed — flag for the extension then close."""
        self.export_confirmed = True
        self.Close()

    def on_close(self, event: wx.CloseEvent) -> None:
        # Veto is not needed; just destroy. export_confirmed already encodes intent.
        self.Destroy()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_unique_threads(self) -> Set[str]:
        return set(cell.thread_id for cell in self.state.cells.values()
                   if cell.thread_id)

    def _update_counts(self) -> None:
        counts = {}
        for cell in self.state.cells.values():
            tid = cell.thread_id or "#444444"
            counts[tid] = counts.get(tid, 0) + 1
        self._thread_counts = counts
        total = sum(counts.values())
        parts = [f"{tid}: {n}" for tid, n in list(counts.items())[:3]]
        self._count_label.SetLabel("  ".join(parts) + f"  Total: {total}")
        # active_thread is Optional[str]; guard before using as a dict key so the
        # type checker can confirm the lookup is always str → int, never None → int.
        cur = self.interaction.active_thread or ""
        cnt = counts.get(cur, 0)
        self._curr_count.SetLabel(f"Count    {cnt}")

    def _refresh_rulers(self) -> None:
        self.h_ruler.Refresh()
        self.v_ruler.Refresh()