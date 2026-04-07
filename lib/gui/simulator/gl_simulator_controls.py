# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
from ...i18n import _
from ..experimental.gl_renderer import GLStitchPlanRenderer

import math

class LightPointer(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.drawing_panel: "DrawingPanel" = kwargs.pop("drawing_panel")
        self.renderer: GLStitchPlanRenderer = self.drawing_panel.renderer

        super().__init__(*args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        self.SetMinSize((128, 128))


    def OnPaint(self, e: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)
        size = self.GetClientSize()
        center = (size.width//2, size.height//2)
        minor_radius = min(size.width,size.height)//2

        dc.Clear()

        circle_brush = wx.Brush(wx.Colour(128, 128, 255))
        dc.SetBrush(circle_brush)
        dc.DrawCircle(*center, minor_radius)

        crosshair_pen = wx.Pen(wx.BLACK, 2)
        dc.SetPen(crosshair_pen)
        dc.DrawLine(center[0]-minor_radius, center[1], center[0]+minor_radius, center[1])
        dc.DrawLine(center[0], center[1]-minor_radius, center[0], center[1]+minor_radius)

    def OnLeftDown(self, e:wx.MouseEvent) -> None:
        self._position(e.GetPosition())
        self.Bind(wx.EVT_MOTION, self.on_drag)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_drag_end)
        self.Bind(wx.EVT_LEFT_UP, self.on_drag_end)

    def on_drag(self, e:wx.MouseEvent) -> None:
        self._position(e.GetPosition())

    def on_drag_end(self, e: wx.MouseEvent) -> None:
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        self.Unbind(wx.EVT_LEFT_UP)

    def _position(self, position: wx.Point) -> None:
        size = self.GetClientSize()
        center = (size.width//2, size.height//2)
        minor_radius = min(size.width,size.height)//2

        x,y = position
        lx = (x-center[0])/minor_radius
        ly = (y-center[1])/minor_radius
        l2 = lx*lx + ly*ly
        if l2 > 1:
            l_len = math.sqrt(l2)
            lx /= l_len
            ly /= l_len
        lz = math.sqrt(max(1 - lx*lx - ly*ly, 0))
        self.renderer.set_light_vector([lx,-ly,lz])
        self.drawing_panel.Refresh()


class GLSimulatorControlsFrame(wx.Frame):
    # Todo: better integrate this into the GUI. Collapsible panel?
    def __init__(self, parent, **kwargs):
        self.drawing_panel: "DrawingPanel" = parent

        super().__init__(parent, title=_("OpenGL Debug Simulator Controls"), **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)
        self.sizer.Add(LightPointer(self, drawing_panel = self.drawing_panel), 0, wx.EXPAND, 0)
        self.sizer.SetSizeHints(self)
        self.Layout()

        self.SetMinSize(self.sizer.CalcMin())

