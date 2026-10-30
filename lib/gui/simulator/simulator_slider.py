# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import math
import os
import sys

import wx

from ...debug.debug import debug
from ...i18n import _
from ...utils import get_resource_dir


class SimulatorSlider(wx.Panel):
    PROXY_EVENTS = (wx.EVT_SLIDER,)

    # Timeline zoom: each wheel notch zooms by this factor, and the view
    # never gets narrower than MIN_VIEW_STITCHES.
    ZOOM_FACTOR = 1.25
    MIN_VIEW_STITCHES = 20
    # Shift + wheel moves the view by this share of its width per notch.
    SCROLL_FRACTION = 0.1
    # When the current stitch leaves the view, the view jumps so the stitch
    # sits this share of the width in from the edge.
    PAGE_MARGIN = 0.1

    def __init__(self, parent, id=wx.ID_ANY, minValue=1, maxValue=2, **kwargs):
        super().__init__(parent, id)
        self.control_panel = parent

        kwargs['style'] = wx.SL_HORIZONTAL | wx.SL_VALUE_LABEL | wx.SL_TOP | wx.ALIGN_TOP

        self._height = self.GetTextExtent("M").y * 6
        self.SetMinSize((self._height, self._height))

        dark_theme = self.control_panel.is_dark_theme() and sys.platform != "win32"
        self.marker_lists = {
            "stop": MarkerList("stop", dark_theme, 0.34),
            "color_change": MarkerList("color_change", dark_theme, 0.34),
            "jump": MarkerList("jump", dark_theme, 0.17),
            "trim": MarkerList("trim", dark_theme)
        }
        if dark_theme:
            self.marker_pen = wx.Pen(wx.Colour(155, 155, 155))
            self.label_colour = wx.Colour(200, 200, 200)
        else:
            self.marker_pen = wx.Pen(wx.Colour(0, 0, 0))
            self.label_colour = wx.Colour(60, 60, 60)
        self.color_sections = []
        self.margin = 15
        self.tab_start = 0
        self.tab_width = 0.15
        self.tab_height = 0.15
        self.color_bar_start = 0.22
        self.color_bar_thickness = 0.17
        self.marker_start = self.color_bar_start
        self.marker_end = 0.5
        self.marker_icon_start = 0.5
        self.marker_icon_size = self._height // 6

        self._min = minValue
        self._max = maxValue
        self._value = 0
        self._tab_rect = None

        # Visible stitch range. None means not zoomed: the whole design shows.
        self._view = None
        self._kept_view = None
        # Leftover partial wheel steps (touchpads send small steps).
        self._scrub_rest = 0.0

        if sys.platform == "darwin":
            self.margin = 8

        self.SetToolTip(_("Wheel: zoom the timeline. Shift+wheel: scroll it. "
                          "Ctrl+wheel: step through stitches. Double-click: show the whole design."))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

    def SetMax(self, value):
        self._max = value
        self._fit_view()
        self.Refresh()

    def SetMin(self, value):
        self._min = value
        self._fit_view()
        self.Refresh()

    def SetValue(self, value):
        if value != self._value:
            self._bring_into_view(value)
        self._value = value
        self.Refresh()

    def GetValue(self):
        return self._value

    def clear(self):
        self.color_sections = []
        self._min = 1
        self._max = 2
        self._value = 0
        self._tab_rect = None
        # Remember the zoom so a reload of the same preview can restore it.
        if self._view is not None:
            self._kept_view = self._view
        self._view = None
        self._scrub_rest = 0.0

        for marker_list in self.marker_lists.values():
            marker_list.clear()

    def add_color_section(self, color, start, end):
        self.color_sections.append(ColorSection(color, start, end))

    def add_marker(self, name, location):
        self.marker_lists[name].append(location)
        self.Refresh()

    def enable_marker_list(self, name, enabled=True):
        self.marker_lists[name].enabled = enabled
        self.Refresh()

    def disable_marker_list(self, name):
        self.marker_lists[name].enabled = False
        self.Refresh()

    def toggle_marker_list(self, name):
        self.marker_lists[name].enabled = not self.marker_lists[name].enabled
        self.Refresh()

    # --- timeline zoom -------------------------------------------------

    def restore_view(self):
        """Bring back the zoom that was in place before the last clear."""
        if self._kept_view is not None:
            self._view = self._kept_view
            self._kept_view = None
            self._fit_view()
            self.Refresh()

    def _visible_range(self):
        if self._view is None:
            return self._min, self._max
        return self._view

    def _fit_view(self):
        # Keep the view inside the design; drop the zoom when it would show
        # the whole design anyway.
        if self._view is None:
            return
        start, end = self._view
        full = self._max - self._min
        width = max(end - start, min(self.MIN_VIEW_STITCHES, full))
        if width >= full:
            # The design got too short for this zoom (also happens while the
            # preview clears before a reload): keep it for restore_view.
            self._kept_view = self._view
            self._view = None
            return
        start = max(self._min, min(start, self._max - width))
        self._view = (start, start + width)

    def _set_view(self, start, end):
        self._view = (start, end)
        self._fit_view()
        self.Refresh()

    def _bring_into_view(self, value):
        if self._view is None:
            return
        start, end = self._view
        width = end - start
        if value > end:
            new_start = value - width * self.PAGE_MARGIN
            self._set_view(new_start, new_start + width)
        elif value < start:
            new_end = value + width * self.PAGE_MARGIN
            self._set_view(new_end - width, new_end)

    def _bar_width(self):
        return max(self.GetSize()[0] - 2 * self.margin, 1)

    def value_to_x(self, value):
        start, end = self._visible_range()
        spread = (end - start) or 1
        return (value - start) * self._bar_width() / spread + self.margin

    def x_to_value(self, x):
        start, end = self._visible_range()
        return start + (x - self.margin) * (end - start) / self._bar_width()

    def zoom(self, steps, x):
        start, end = self._visible_range()
        full = self._max - self._min
        if full <= self.MIN_VIEW_STITCHES:
            return
        # Keep the stitch under the pointer in the same place.
        anchor = self.x_to_value(x)
        width = (end - start) / (self.ZOOM_FACTOR ** steps)
        width = max(self.MIN_VIEW_STITCHES, min(width, full))
        if width >= full:
            self._view = None
            self.Refresh()
            return
        share = (anchor - start) / ((end - start) or 1)
        new_start = anchor - share * width
        self._set_view(new_start, new_start + width)

    def scroll(self, steps):
        if self._view is None:
            return
        start, end = self._view
        shift = (end - start) * self.SCROLL_FRACTION * steps
        self._set_view(start + shift, end + shift)

    def scrub(self, steps):
        self._scrub_rest += steps
        whole = int(self._scrub_rest)
        if not whole:
            return
        self._scrub_rest -= whole
        current = max(self._value, self._min)
        value = max(self._min, min(self._max, current + whole))
        if value != current:
            self._set_value_and_notify(value)

    def reset_zoom(self):
        self._view = None
        self.Refresh()

    def on_mouse_wheel(self, event):
        delta = event.GetWheelDelta() or 120
        steps = event.GetWheelRotation() / delta
        if not steps:
            return
        horizontal = event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL

        if event.ControlDown() or event.CmdDown():
            # Wheel up steps forward, like scrubbing in a video editor.
            self.scrub(steps)
        elif horizontal:
            # GTK may turn Shift + wheel into a sideways scroll, where
            # wheel down arrives as a positive step.
            self.scroll(steps)
        elif event.ShiftDown():
            self.scroll(steps)
        else:
            self.zoom(steps, event.GetPosition().x)

    def on_double_click(self, event):
        self.reset_zoom()

    # --- drawing -------------------------------------------------------

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        if not sys.platform.startswith("win"):
            # Without this, the background color will be white.
            background_brush = wx.Brush(self.GetTopLevelParent().GetBackgroundColour(), wx.SOLID)
            dc.SetBackground(background_brush)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        if self._value < self._min:
            self._value = self._min

        width, height = self.GetSize()
        view_start, view_end = self._visible_range()

        self._draw_color_sections(gc, height, view_start, view_end)
        self._draw_tab(gc, height, view_start, view_end)
        self._draw_markers(gc, height, view_start, view_end)
        if self._view is not None:
            self._draw_range_labels(gc, width, height, view_start, view_end)

    def _draw_color_sections(self, gc, height, view_start, view_end):
        gc.SetPen(wx.NullPen)
        for color_section in self.color_sections:
            # Cut sections at the edges of the visible range.
            start = max(color_section.start, view_start)
            end = min(color_section.end, view_end)
            if end <= start:
                continue
            gc.SetBrush(color_section.brush)

            start_x = self.value_to_x(start)
            end_x = self.value_to_x(end)
            gc.DrawRectangle(start_x, height * self.color_bar_start,
                             end_x - start_x, height * self.color_bar_thickness)

    def _draw_tab(self, gc, height, view_start, view_end):
        if self.control_panel.is_dark_theme() and sys.platform != "win32":
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        else:
            gc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 1))
            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

        if not view_start <= self._value <= view_end:
            self._tab_rect = None
            return

        value_x = self.value_to_x(self._value)
        tab_height = self.tab_height * height
        tab_width = self.tab_width * height
        tab_x = value_x - tab_width / 2
        tab_y = height * self.tab_start
        self._tab_rect = wx.Rect(round(tab_x), round(tab_y), round(tab_width), round(tab_height))
        gc.DrawRectangle(
            value_x - 1.5, 0,
            3, height * (self.color_bar_start + self.color_bar_thickness))
        gc.SetPen(wx.NullPen)
        gc.DrawRectangle(value_x - tab_width/2, height * self.tab_start,
                         tab_width, tab_height)

    def _draw_markers(self, gc, height, view_start, view_end):
        gc.SetPen(self.marker_pen)
        for marker_list in self.marker_lists.values():
            if not marker_list.enabled:
                continue
            for value in marker_list:
                if not view_start <= value <= view_end:
                    continue
                x = self.value_to_x(value)
                gc.StrokeLine(
                    x, height * self.marker_start,
                    x, height * (self.marker_end + marker_list.offset)
                )
                gc.DrawBitmap(
                    marker_list.icon,
                    x - self.marker_icon_size / 2, height * (self.marker_icon_start + marker_list.offset),
                    self.marker_icon_size, self.marker_icon_size
                )

    def _draw_range_labels(self, gc, width, height, view_start, view_end):
        # Show which stitches the zoomed timeline covers.
        font = self.GetFont()
        font.SetPointSize(max(font.GetPointSize() - 2, 6))
        gc.SetFont(font, self.label_colour)
        first = f"{round(view_start)}"
        last = f"{round(view_end)}"
        label_y = height * (self.color_bar_start + self.color_bar_thickness) + 2
        gc.DrawText(first, self.margin, label_y)
        last_width = gc.GetTextExtent(last)[0]
        gc.DrawText(last, width - self.margin - last_width, label_y)

    def on_erase_background(self, event):
        # supposedly this prevents flickering?
        pass

    def is_in_tab(self, point):
        return self._tab_rect and self._tab_rect.Inflate(2).Contains(point)

    def _set_value_and_notify(self, value):
        self.SetValue(value)

        event = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, self.GetId())
        event.SetInt(value)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def set_value_from_position(self, point):
        start, end = self._visible_range()
        value = round(self.x_to_value(point.x))
        # Stay inside the visible range while dragging past the edges.
        value = max(value, self._min, math.ceil(start))
        value = min(value, self._max, math.floor(end))
        self._set_value_and_notify(value)

    def on_mouse_down(self, event):
        click_pos = event.GetPosition()
        if self.is_in_tab(click_pos):
            debug.log("drag start")
            self.CaptureMouse()
            self.set_value_from_position(click_pos)
            self.Refresh()
        else:
            width, height = self.GetSize()
            relative_y = click_pos.y / height
            if relative_y > self.color_bar_start and relative_y - self.color_bar_start < self.color_bar_thickness:
                self.set_value_from_position(click_pos)
                self.Refresh()

    def on_mouse_motion(self, event):
        if self.HasCapture() and event.Dragging() and event.LeftIsDown():
            self.set_value_from_position(event.GetPosition())
            self.Refresh()

    def on_mouse_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
            self.set_value_from_position(event.GetPosition())
            self.Refresh()


class MarkerList(list):
    def __init__(self, icon_name, dark_theme, offset=0, stitch_numbers=()):
        super().__init__(self)
        icons_dir = get_resource_dir("icons")
        self.icon_name = icon_name
        if dark_theme:
            self.icon = wx.Image(os.path.join(icons_dir, f"{icon_name}_dark.png")).ConvertToBitmap()
        else:
            self.icon = wx.Image(os.path.join(icons_dir, f"{icon_name}.png")).ConvertToBitmap()
        self.offset = offset
        self.enabled = False
        self.extend(stitch_numbers)

    def __repr__(self):
        return f"MarkerList({self.icon_name})"


class ColorSection:
    def __init__(self, color, start, end):
        self.color = color
        self.start = start
        self.end = end
        self.brush = wx.Brush(wx.Colour(*color))
