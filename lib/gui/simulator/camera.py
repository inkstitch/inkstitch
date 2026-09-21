# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx
from typing import Optional, cast

from ...stitch_plan import StitchPlan


class Camera:
    """ Camera control for a drawing panel. """
    def __init__(self, panel: wx.Panel, stitch_plan: Optional[StitchPlan]) -> None:
        self.panel = panel
        self.stitch_plan = stitch_plan
        self.pan = (0.0, 0.0)
        self.zoom = 1.0

        self._choose_zoom_and_pan()

        self._bind_handlers()

    def _bind_handlers(self) -> None:
        self.panel.Bind(wx.EVT_SIZE, self._on_resize)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self._on_left_mouse_button_down)
        self.panel.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)

    def _choose_zoom_and_pan(self) -> None:
        if self.stitch_plan is None:
            return

        minx, miny, maxx, maxy = self.stitch_plan.bounding_box
        width = maxx-minx
        height = maxy-miny
        # The types are wrong here, GetClientSize returns a Size
        panel_size = cast(wx.Size, self.panel.GetClientSize())

        # add some padding to make stitches at the edge more visible
        width_ratio = panel_size.width / float(width + 10)
        height_ratio = panel_size.height / float(height + 10)
        self.zoom = max(min(width_ratio, height_ratio), 0.01)

        # center the design
        self.pan = ((panel_size.width - self.zoom * (minx + maxx)) / 2.0,
                    (panel_size.height - self.zoom * (miny + maxy)) / 2.0)

    def set_stitch_plan(self, stitch_plan: Optional[StitchPlan]) -> None:
        self.stitch_plan = stitch_plan
        self._choose_zoom_and_pan()

    def _on_resize(self, event: wx.SizeEvent) -> None:
        self._choose_zoom_and_pan()
        self.panel.Refresh()

    def _on_left_mouse_button_down(self, event: wx.MouseEvent) -> None:
        if self.stitch_plan is not None:
            self.panel.CaptureMouse()
            self.drag_start = event.GetPosition()
            self.drag_original_pan = self.pan
            self.panel.Bind(wx.EVT_MOTION, self._on_drag)
            self.panel.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._on_drag_end)
            self.panel.Bind(wx.EVT_LEFT_UP, self._on_drag_end)

    def _on_drag(self, event: wx.MouseEvent) -> None:
        if self.panel.HasCapture() and event.Dragging():
            delta = event.GetPosition()
            offset = (delta.x - self.drag_start.x, delta.y - self.drag_start.y)
            self.pan = (self.drag_original_pan[0] + offset[0], self.drag_original_pan[1] + offset[1])
            self.panel.Refresh()

    def _on_drag_end(self, event: wx.MouseEvent) -> None:
        if self.panel.HasCapture():
            self.panel.ReleaseMouse()

        self.panel.Unbind(wx.EVT_MOTION)
        self.panel.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        self.panel.Unbind(wx.EVT_LEFT_UP)

    def _on_mouse_wheel(self, event: wx.MouseEvent) -> None:
        if event.GetWheelRotation() > 0:
            zoom_delta = 1.03
        else:
            zoom_delta = 0.97

        # If we just change the zoom, the design will appear to move on the
        # screen.  We have to adjust the pan to compensate.  We want to keep
        # the part of the design under the mouse pointer in the same spot
        # after we zoom, so that we appear to be zooming centered on the
        # mouse pointer.

        # This will create a matrix that takes a point in the design and
        # converts it to screen coordinates:
        matrix = wx.AffineMatrix2D()
        matrix.Translate(*self.pan)
        matrix.Scale(self.zoom, self.zoom)

        # First, figure out where the mouse pointer is in the coordinate system
        # of the design:
        pos = event.GetPosition()
        inverse_matrix = wx.AffineMatrix2D()
        inverse_matrix.Set(*matrix.Get())
        inverse_matrix.Invert()
        pos = inverse_matrix.TransformPoint(*pos)

        # Next, see how that point changes position on screen before and after
        # we apply the zoom change:
        x_old, y_old = matrix.TransformPoint(*pos)
        matrix.Scale(zoom_delta, zoom_delta)
        x_new, y_new = matrix.TransformPoint(*pos)
        x_delta = x_new - x_old
        y_delta = y_new - y_old

        # Finally, compensate for that change in position:
        self.pan = (self.pan[0] - x_delta, self.pan[1] - y_delta)

        self.zoom *= zoom_delta

        self.panel.Refresh()
