# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os
import sys

import wx

from ...debug.debug import debug
from ...utils import get_resource_dir


class SimulatorSlider(wx.Panel):
    PROXY_EVENTS = (wx.EVT_SLIDER,)

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
        else:
            self.marker_pen = wx.Pen(wx.Colour(0, 0, 0))
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

        if sys.platform == "darwin":
            self.margin = 8

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)

    def SetMax(self, value):
        self._max = value
        self.Refresh()

    def SetMin(self, value):
        self._min = value
        self.Refresh()

    def SetValue(self, value):
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

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        if not sys.platform.startswith("win"):
            # Without this, the background color will be white.
            background_brush = wx.Brush(self.GetTopLevelParent().GetBackgroundColour(), wx.SOLID)
            dc.SetBackground(background_brush)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        if self._value < self._min:
            return

        width, height = self.GetSize()
        min_value = self._min
        max_value = self._max
        spread = max_value - min_value

        def _value_to_x(value):
            return (value - min_value) * (width - 2 * self.margin) / spread + self.margin

        gc.SetPen(wx.NullPen)
        for color_section in self.color_sections:
            gc.SetBrush(color_section.brush)

            start_x = _value_to_x(color_section.start)
            end_x = _value_to_x(color_section.end)
            gc.DrawRectangle(start_x, height * self.color_bar_start,
                             end_x - start_x, height * self.color_bar_thickness)

        if self.control_panel.is_dark_theme() and sys.platform != "win32":
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        else:
            gc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 1))
            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

        value_x = _value_to_x(self._value)
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

        gc.SetPen(self.marker_pen)
        for marker_list in self.marker_lists.values():
            if marker_list.enabled:
                for value in marker_list:
                    x = _value_to_x(value)
                    gc.StrokeLine(
                        x, height * self.marker_start,
                        x, height * (self.marker_end + marker_list.offset)
                    )
                    gc.DrawBitmap(
                        marker_list.icon,
                        x - self.marker_icon_size / 2, height * (self.marker_icon_start + marker_list.offset),
                        self.marker_icon_size, self.marker_icon_size
                    )

    def on_erase_background(self, event):
        # supposedly this prevents flickering?
        pass

    def is_in_tab(self, point):
        return self._tab_rect and self._tab_rect.Inflate(2).Contains(point)

    def set_value_from_position(self, point):
        width, height = self.GetSize()
        min_value = self._min
        max_value = self._max
        spread = max_value - min_value
        value = round((point.x - self.margin) * spread / (width - 2 * self.margin))
        value = max(value, self._min)
        value = min(value, self._max)
        self.SetValue(round(value))

        event = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, self.GetId())
        event.SetInt(value)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

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
