# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import math

import wx
from numpy import split


from ...debug.debug import debug
from ...svg import PIXELS_PER_MM
from ...utils.settings import global_settings
from ...stitch_plan import StitchPlan
from ...threads.color import ThreadColor

from typing import Optional, List, Tuple, Dict, Any


class DrawingPanel(wx.Panel):
    """"""
    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    pan: Tuple[float, float]
    zoom: float

    def __init__(self, parent, *args, **kwargs) -> None:
        """"""
        self.stitch_plan: Optional[StitchPlan] = kwargs.pop('stitch_plan', None)
        kwargs['style'] = wx.BORDER_SUNKEN

        wx.Panel.__init__(self, parent, *args, **kwargs)

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        self.SetMinSize((300, 300))
        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        self.black_pen = wx.Pen((128, 128, 128))
        self.width = 0
        self.height = 0
        self.loaded = False
        self.page_specs: Dict[Any, Any] = {}
        self.show_page = global_settings['toggle_page_button_status']
        self.background_color = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.choose_zoom_and_pan)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_button_down)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event: wx.SizeEvent) -> None:
        self.choose_zoom_and_pan()
        self.Refresh()

    def OnPaint(self, e: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)

        if not self.loaded:
            dc.Clear()
            return

        canvas = wx.GraphicsContext.Create(dc)

        self.draw_stitches(canvas)
        self.draw_scale(canvas)

    def draw_page(self, canvas: wx.GraphicsContext) -> None:
        self._update_background_color()

        if not self.page_specs or not self.show_page:
            return

        with debug.log_exceptions():
            border_color = wx.Colour(self.page_specs['border_color'])
            if self.page_specs['show_page_shadow']:
                # TRANSPARENT_PEN isn't in the types, but it is defined.
                canvas.SetPen(wx.TRANSPARENT_PEN)  # type: ignore[attr-defined]
                canvas.SetBrush(canvas.CreateBrush(wx.Brush(wx.Colour(border_color.Red(), border_color.Green(), border_color.Blue(), alpha=65))))
                canvas.DrawRoundedRectangle(
                    (-self.page_specs['x'] + 4) * self.PIXEL_DENSITY, (-self.page_specs['y'] + 4) * self.PIXEL_DENSITY,
                    self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY,
                    1 * self.PIXEL_DENSITY
                )

            pen = canvas.CreatePen(
                wx.GraphicsPenInfo().Colour(wx.Colour(border_color)).Width(1 * self.PIXEL_DENSITY).Join(wx.JOIN_MITER)
            )
            canvas.SetPen(pen)
            canvas.SetBrush(wx.Brush(wx.Colour(self.background_color or self.page_specs['page_color'])))

            canvas.DrawRectangle(
                -self.page_specs['x'] * self.PIXEL_DENSITY, -self.page_specs['y'] * self.PIXEL_DENSITY,
                self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY
            )

    def draw_stitches(self, canvas: wx.GraphicsContext) -> None:
        canvas.BeginLayer(1)

        transform = canvas.GetTransform()
        transform.Translate(*self.pan)
        transform.Scale(self.zoom / self.PIXEL_DENSITY, self.zoom / self.PIXEL_DENSITY)
        canvas.SetTransform(transform)

        self.draw_page(canvas)

        stitch = 0
        last_stitch = None

        for pen, stitches, jumps in zip(self.pens, self.stitch_blocks, self.jumps):
            canvas.SetPen(pen)
            if stitch + len(stitches) < self.current_stitch:
                stitch += len(stitches)
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
            else:
                stitches = stitches[:int(self.current_stitch) - stitch]
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
                break

        if last_stitch and global_settings['display_crosshair']:
            self.draw_crosshair(last_stitch[0], last_stitch[1], canvas, transform)

        canvas.EndLayer()

    def draw_crosshair(self, x: float, y: float, canvas: wx.GraphicsContext, transform: wx.GraphicsMatrix) -> None:
        x, y = transform.TransformPoint(float(x), float(y))
        canvas.SetTransform(canvas.CreateMatrix())
        crosshair_radius = global_settings['simulator_crosshair_radius']
        crosshair_pen = wx.Pen(wx.Colour(global_settings['simulator_crosshair_colour']), width=global_settings['simulator_crosshair_thickness'])
        canvas.SetPen(crosshair_pen)
        canvas.StrokeLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
        canvas.StrokeLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))

    def draw_scale(self, canvas: wx.GraphicsContext) -> None:
        canvas.SetTransform(canvas.CreateMatrix())
        canvas.BeginLayer(1)

        size: wx.Rect = self.GetClientSize()
        canvas_width = size.Width
        canvas_height = size.Height

        one_mm = PIXELS_PER_MM * self.zoom
        scale_width = one_mm
        scale_width_mm = 1
        max_width = min(canvas_width * 0.5, 300)
        min_width = 50

        if scale_width > max_width:
            # max_width = one_mm * 2 ^ x
            # x = log2(max_width/one_mm)
            exponent = math.floor(math.log2(max_width/one_mm))
            if exponent < -6:
                canvas.EndLayer()
                return

            scale_width = one_mm * 2 ** exponent
            scale_width_mm = round(2 ** exponent, 2)

        if scale_width < min_width:
            scale_width_mm = int(min_width / one_mm)
            scale_width = one_mm * scale_width_mm

        # The scale bar looks like this:
        #
        # |           |
        # |_____|_____|

        scale_lower_left_x = 20
        scale_lower_left_y = canvas_height - 30

        canvas.SetPen(self.black_pen)
        canvas.StrokeLines(((scale_lower_left_x, scale_lower_left_y - 6),
                            (scale_lower_left_x, scale_lower_left_y),
                            (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y),
                            (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y - 3),
                            (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y),
                            (scale_lower_left_x + scale_width, scale_lower_left_y),
                            (scale_lower_left_x + scale_width, scale_lower_left_y - 6)))

        canvas.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL), wx.Colour((0, 0, 0)))
        canvas.DrawText("%s mm" % scale_width_mm, scale_lower_left_x, scale_lower_left_y + 5)

        canvas.EndLayer()

    def draw_stitch_lines(self, canvas: wx.GraphicsContext, stitches: List[Tuple[float, float]], jumps: List[int]) -> None:
        render_jumps = global_settings['jump_button_status']
        if render_jumps:
            canvas.StrokeLines(stitches)
        else:
            stitch_blocks = split(stitches, jumps)
            for i, block in enumerate(stitch_blocks):
                if len(block) > 1:
                    canvas.StrokeLines(block)

    def draw_needle_penetration_points(self, canvas: wx.GraphicsContext, pen: wx.Pen, stitches: List[Tuple[float, float]]) -> None:
        if global_settings['npp_button_status']:
            npp_size = global_settings['simulator_npp_size'] * PIXELS_PER_MM * self.PIXEL_DENSITY
            npp_pen = wx.Pen(pen.GetColour(), width=int(npp_size))
            canvas.SetPen(npp_pen)
            canvas.StrokeLineSegments(stitches, [(stitch[0] + 0.001, stitch[1]) for stitch in stitches])

    def load(self, stitch_plan: StitchPlan) -> None:
        self.direction = 1
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.parse_stitch_plan(stitch_plan)
        self.choose_zoom_and_pan()
        self.loaded = True

    def clear(self):
        self.loaded = False
        self.Refresh()

    def set_page_specs(self, page_specs) -> None:
        self.SetBackgroundColour(page_specs['desk_color'])
        self.page_specs = page_specs

    def set_background_color(self, color) -> None:
        self.background_color = color
        self._update_background_color()

    def _update_background_color(self) -> None:
        if not self.page_specs:
            self.SetBackgroundColour(self.background_color or "#FFFFFF")
        else:
            if self.show_page:
                self.SetBackgroundColour(self.page_specs['desk_color'])
            else:
                self.SetBackgroundColour(self.background_color or self.page_specs['page_color'])

    def set_show_page(self, show_page) -> None:
        self.show_page = show_page
        self._update_background_color()

    def choose_zoom_and_pan(self, event: Optional[wx.SizeEvent] = None) -> None:
        # ignore if EVT_SIZE fired before we load the stitch plan
        if not self.width and not self.height and event is not None:
            return

        size: wx.Rect = self.GetClientSize()
        panel_width = size.Width
        panel_height = size.Height

        # add some padding to make stitches at the edge more visible
        width_ratio = panel_width / float(self.width + 10)
        height_ratio = panel_height / float(self.height + 10)
        self.zoom = max(min(width_ratio, height_ratio), 0.01)

        # center the design
        self.pan = ((panel_width - self.zoom * self.width) / 2.0,
                    (panel_height - self.zoom * self.height) / 2.0)

    def color_to_pen(self, color: ThreadColor) -> wx.Pen:
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        background_color = self.GetBackgroundColour().GetAsString()
        return wx.Pen(list(map(int, color.visible_on_background(background_color).rgb)), int(line_width))

    def update_pen_size(self) -> None:
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        for pen in self.pens:
            pen.SetWidth(int(line_width))

    def parse_stitch_plan(self, stitch_plan: StitchPlan) -> None:
        self.pens = []
        self.stitch_blocks = []
        self.jumps = []

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)
            stitch_block = []
            jumps = []
            stitch_index = 0

            for stitch in color_block:
                # trim any whitespace on the left and top and scale to the
                # pixel density
                stitch_block.append((self.PIXEL_DENSITY * (stitch.x - self.minx),
                                     self.PIXEL_DENSITY * (stitch.y - self.miny)))

                if stitch.jump:
                    jumps.append(stitch_index)

                if stitch.trim or stitch.stop or stitch.color_change:
                    self.pens.append(pen)
                    self.stitch_blocks.append(stitch_block)
                    stitch_block = []
                    self.jumps.append(jumps)
                    jumps = []
                    stitch_index = 0
                else:
                    stitch_index += 1

            if stitch_block:
                self.pens.append(pen)
                self.stitch_blocks.append(stitch_block)
                self.jumps.append(jumps)

    def set_current_stitch(self, stitch: int) -> None:
        self.current_stitch = stitch
        self.Refresh()

    def on_left_mouse_button_down(self, event: wx.MouseEvent) -> None:
        if self.loaded:
            self.CaptureMouse()
            self.drag_start = event.GetPosition()
            self.drag_original_pan = self.pan
            self.Bind(wx.EVT_MOTION, self.on_drag)
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_drag_end)
            self.Bind(wx.EVT_LEFT_UP, self.on_drag_end)

    def on_drag(self, event: wx.MouseEvent) -> None:
        if self.HasCapture() and event.Dragging():
            delta = event.GetPosition()
            offset = (delta.x - self.drag_start[0], delta.y - self.drag_start[1])
            self.pan = (self.drag_original_pan[0] + offset[0], self.drag_original_pan[1] + offset[1])
            self.Refresh()

    def on_drag_end(self, event: wx.MouseEvent) -> None:
        if self.HasCapture():
            self.ReleaseMouse()

        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        self.Unbind(wx.EVT_LEFT_UP)

    def on_mouse_wheel(self, event: wx.MouseEvent) -> None:
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

        self.Refresh()
