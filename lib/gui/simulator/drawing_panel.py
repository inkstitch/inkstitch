# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import math

import wx
from numpy import split
from typing import List, Optional, Tuple, cast

from ...stitch_plan import StitchPlan
from ...threads import ThreadColor
from ...debug.debug import debug
from ...i18n import _
from ...svg import PIXELS_PER_MM
from ...utils.settings import global_settings
from .camera import Camera
from .animator import Animator
from .status_bar_updater import StatusBarUpdater


class LoadingIndicator:
    """ Loading indicator that is shown while generating the stitch plan """
    RENDERING = _("Stitching...")
    PADDING = 10  # Padding around the text in px
    CORNER_RADIUS = 10  # px

    def __init__(self) -> None:
        self.font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bg_brush = wx.Brush(wx.Colour(0, 0, 0, alpha=100))
        self.bounds: Optional[Tuple[float, float]] = None

    def paint(self, canvas: wx.GraphicsContext) -> None:
        panel_width, panel_height = canvas.GetSize()

        canvas.SetFont(self.font, wx.WHITE)
        if self.bounds is None:
            t_w, t_h, t_d, t_el = canvas.GetFullTextExtent(self.RENDERING)
            self.bounds = (t_w, t_h)

        w, h = self.bounds
        # TRANSPARENT_PEN is there, but it's not in the types for some reason.
        canvas.SetPen(wx.TRANSPARENT_PEN)  # type:ignore[attr-defined]
        canvas.SetBrush(self.bg_brush)
        canvas.DrawRoundedRectangle(
            ((panel_width-w)/2)-self.PADDING,
            ((panel_height-h)/2)-self.PADDING,
            w+2*self.PADDING,
            h+2*self.PADDING,
            self.CORNER_RADIUS
        )
        canvas.DrawText(self.RENDERING, (panel_width-w)/2, (panel_height-h)/2)


class DrawingPanel(wx.Panel):
    """"""

    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    # Render circles once their shape is visible instead of using fast squares.
    CIRCLE_MARKER_MIN_SCREEN_SIZE = 4

    def __init__(self, parent, *args, **kwargs) -> None:
        """"""
        self.parent = parent
        self.stitch_plan: Optional[StitchPlan] = kwargs.pop('stitch_plan', None)
        kwargs['style'] = wx.BORDER_SUNKEN

        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.control_panel = parent.cp
        self.view_panel = parent.vp

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        self.SetMinSize((300, 300))
        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        self.loading = False
        self.loading_indicator = LoadingIndicator()

        self.black_pen = wx.Pen((128, 128, 128))
        self.page_specs: dict = {}
        self.show_page = global_settings['toggle_page_button_status']
        self.background_color: Optional[wx.Colour] = None

        self.pens: List[wx.Pen] = []
        self.stitch_blocks: List[List[Tuple[float, float]]] = []
        self.jumps: List[List[int]] = []

        self.animator = Animator(self.stitch_plan)
        self.animator.add_callback(self._on_current_stitch)
        self.status_bar_updater = StatusBarUpdater(self, self.animator)
        self.camera = Camera(self, self.stitch_plan)

        if self.stitch_plan is not None:
            self.load(self.stitch_plan)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def _on_current_stitch(self, current_stitch: int, animating: bool) -> None:
        self.current_stitch = current_stitch
        self.control_panel.on_current_stitch(self.current_stitch, animating)

        self.Refresh()

    def OnPaint(self, e: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)
        canvas = wx.GraphicsContext.Create(dc)

        if self.stitch_plan is not None:
            self.draw_stitches(canvas)
            self.draw_scale(canvas)

        if self.loading:
            self.loading_indicator.paint(canvas)

    def draw_page(self, canvas: wx.GraphicsContext) -> None:
        self._update_background_color()

        if not self.page_specs or not self.show_page:
            return

        with debug.log_exceptions():
            border_color = wx.Colour(self.page_specs['border_color'])
            if self.page_specs['show_page_shadow']:
                # TRANSPARENT_PEN is there, but it's not in the types for some reason.
                canvas.SetPen(wx.TRANSPARENT_PEN)  # type:ignore[attr-defined]
                canvas.SetBrush(canvas.CreateBrush(wx.Brush(wx.Colour(border_color.Red(), border_color.Green(), border_color.Blue(), alpha=65))))
                canvas.DrawRoundedRectangle(
                    4 * self.PIXEL_DENSITY, 4 * self.PIXEL_DENSITY,
                    self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY,
                    1 * self.PIXEL_DENSITY
                )

            pen = canvas.CreatePen(
                wx.GraphicsPenInfo().Colour(wx.Colour(border_color)).Width(1 * self.PIXEL_DENSITY).Join(wx.JOIN_MITER)
            )
            canvas.SetPen(pen)
            canvas.SetBrush(wx.Brush(wx.Colour(self.background_color or self.page_specs['page_color'])))

            canvas.DrawRectangle(
                0.0, 0.0,
                self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY
            )

    def draw_stitches(self, canvas: wx.GraphicsContext) -> None:
        canvas.BeginLayer(1)

        transform = canvas.GetTransform()
        transform.Translate(*self.camera.pan)
        transform.Scale(self.camera.zoom / self.PIXEL_DENSITY, self.camera.zoom / self.PIXEL_DENSITY)
        canvas.SetTransform(transform)

        self.draw_page(canvas)

        stitch = 0
        last_stitch = None

        for pen, stitches, jumps in zip(self.pens, self.stitch_blocks, self.jumps):
            canvas.SetPen(pen)
            if stitch + len(stitches) < self.current_stitch:
                stitch += len(stitches)
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
            else:
                stitches = stitches[:self.current_stitch - stitch]
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
                break

        if last_stitch and self.view_panel.btnCursor.GetValue():
            self.draw_crosshair(last_stitch[0], last_stitch[1], canvas, transform)

        canvas.EndLayer()

    def draw_crosshair(self, x: float, y: float, canvas: wx.GraphicsContext, transform: wx.GraphicsMatrix) -> None:
        x, y = transform.TransformPoint(float(x), float(y))
        canvas.SetTransform(canvas.CreateMatrix())
        crosshair_radius = global_settings['simulator_crosshair_radius']
        crosshair_width = round(global_settings['simulator_crosshair_thickness'] * self.GetContentScaleFactor())
        crosshair_pen = wx.Pen(wx.Colour(global_settings['simulator_crosshair_colour']), width=crosshair_width)
        canvas.SetPen(crosshair_pen)
        canvas.StrokeLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
        canvas.StrokeLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))

    def draw_scale(self, canvas: wx.GraphicsContext) -> None:
        canvas.SetTransform(canvas.CreateMatrix())
        canvas.BeginLayer(1)

        # The types are wrong here, GetClientSize returns a Size
        panel_size = cast(wx.Size, self.GetClientSize())
        canvas_width = panel_size.Width
        canvas_height = panel_size.Height

        one_mm = PIXELS_PER_MM * self.camera.zoom
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

    def draw_stitch_lines(self, canvas: wx.GraphicsContext, pen: wx.Pen, stitches: List[Tuple[float, float]], jumps: List[int]) -> None:
        render_jumps = self.view_panel.btnJump.GetValue()
        if render_jumps:
            canvas.StrokeLines(stitches)
        else:
            stitch_blocks = split(stitches, jumps)
            for i, block in enumerate(stitch_blocks):
                if len(block) > 1:
                    canvas.StrokeLines(block)

    def draw_needle_penetration_points(self, canvas: wx.GraphicsContext, pen: wx.Pen, stitches: List[Tuple[float, float]]) -> None:
        if self.view_panel.btnNpp.GetValue():
            npp_size = global_settings['simulator_npp_size'] * PIXELS_PER_MM * self.PIXEL_DENSITY
            npp_brush = canvas.CreateBrush(wx.Brush(pen.GetColour()))
            canvas.SetBrush(npp_brush)
            # Drawing thousands of ellipses is expensive. Use fast squares by
            # default and only switch to circles when heavily zoomed in.
            canvas.SetPen(wx.TRANSPARENT_PEN)
            square_size = max(1.0, float(npp_size))
            half_size = square_size / 2.0
            marker_screen_size = square_size * self.zoom / self.PIXEL_DENSITY

            if stitches:
                # Use winding fill so overlapping markers remain filled.
                path = canvas.CreatePath()
                for x, y in stitches:
                    if marker_screen_size >= self.CIRCLE_MARKER_MIN_SCREEN_SIZE:
                        path.AddEllipse(x - half_size, y - half_size, square_size, square_size)
                    else:
                        path.AddRectangle(x - half_size, y - half_size, square_size, square_size)
                canvas.FillPath(path, fillStyle=wx.WINDING_RULE)

    def clear(self) -> None:
        self.stitch_plan = None
        self.camera.set_stitch_plan(None)
        self.animator.set_stitch_plan(None)
        self.Refresh()

    def load(self, stitch_plan: StitchPlan) -> None:
        self.stitch_plan = stitch_plan
        self.camera.set_stitch_plan(stitch_plan)
        self.status_bar_updater.set_stitch_plan(stitch_plan)
        self.parse_stitch_plan(stitch_plan)
        # Animator has to be last, because all other parts will need to have loaded the stitch plan first
        self.animator.set_stitch_plan(stitch_plan)
        self.animator.go()

    def set_page_specs(self, page_specs: dict) -> None:
        self.SetBackgroundColour(page_specs['desk_color'])
        self.page_specs = page_specs

    def set_background_color(self, color: wx.Colour) -> None:
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

    def set_show_page(self, show_page: bool) -> None:
        self.show_page = show_page
        self._update_background_color()

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
                # scale to the pixel density
                stitch_block.append((self.PIXEL_DENSITY * (stitch.x),
                                     self.PIXEL_DENSITY * (stitch.y)))

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

    def set_loading(self, loading: bool) -> None:
        self.loading = loading
        self.Refresh()

    # Exposed animator methods
    def stop(self) -> None:
        self.animator.stop()

    def go(self) -> None:
        self.animator.go()

    def forward(self) -> None:
        self.animator.forward()

    def reverse(self) -> None:
        self.animator.reverse()

    def set_current_stitch(self, stitch: int) -> None:
        self.animator.set_current_stitch(stitch)

    def restart(self) -> None:
        self.animator.restart()

    def one_stitch_forward(self) -> None:
        self.animator.one_stitch_forward()

    def one_stitch_backward(self) -> None:
        self.animator.one_stitch_backward()

    def set_speed(self, speed: int) -> None:
        self.animator.set_speed(speed)
