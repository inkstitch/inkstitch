# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import math
import wx
from numpy import split

from typing import TYPE_CHECKING, Tuple, List, cast

from ...svg import PIXELS_PER_MM
from ...stitch_plan import StitchPlan
from ...threads import ThreadColor
from ...debug.debug import debug
from ...utils.settings import global_settings

if TYPE_CHECKING:
    from .drawing_panel import DrawingPanelParameterHolder


class SimpleDrawingPanel(wx.Panel):
    """
    A "simple" renderer that draws the stitch plan as plain lines, using wxWidgets' drawing APIs
    """

    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    def __init__(self, parent: wx.Window, params: 'DrawingPanelParameterHolder', stitch_plan: StitchPlan) -> None:
        wx.Panel.__init__(self, parent)

        self.params = params
        self.set_stitch_plan(stitch_plan)

        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        # ... This isn't actually a black pen.
        self.black_pen = wx.Pen((128, 128, 128))

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)

        canvas = wx.GraphicsContext.Create(dc)

        self.draw_stitches(canvas)
        self.draw_scale(canvas)

    def draw_page(self, canvas: wx.GraphicsContext) -> None:
        self._update_background_color()

        page_specs = self.params.page_specs
        if not page_specs or not self.params.show_page:
            return

        with debug.log_exceptions():
            border_color = wx.Colour(page_specs['border_color'])
            if page_specs['show_page_shadow']:
                # wx.TRANSPARENT_PEN does exist, but isn't in the types apparently.
                canvas.SetPen(wx.TRANSPARENT_PEN)  # type:ignore[attr-defined]
                canvas.SetBrush(canvas.CreateBrush(wx.Brush(wx.Colour(border_color.Red(), border_color.Green(), border_color.Blue(), alpha=65))))
                canvas.DrawRoundedRectangle(
                    (-page_specs['x'] + 4) * self.PIXEL_DENSITY, (-page_specs['y'] + 4) * self.PIXEL_DENSITY,
                    page_specs['width'] * self.PIXEL_DENSITY, page_specs['height'] * self.PIXEL_DENSITY,
                    1 * self.PIXEL_DENSITY
                )

            pen = canvas.CreatePen(
                wx.GraphicsPenInfo().Colour(wx.Colour(border_color)).Width(1 * self.PIXEL_DENSITY).Join(wx.JOIN_MITER)
            )
            canvas.SetPen(pen)
            canvas.SetBrush(wx.Brush(wx.Colour(self.params.background_color or page_specs['page_color'])))

            canvas.DrawRectangle(
                -page_specs['x'] * self.PIXEL_DENSITY, -page_specs['y'] * self.PIXEL_DENSITY,
                page_specs['width'] * self.PIXEL_DENSITY, page_specs['height'] * self.PIXEL_DENSITY
            )

    def draw_stitches(self, canvas: wx.GraphicsContext) -> None:
        canvas.BeginLayer(1)

        transform = canvas.GetTransform()
        transform.Translate(*self.params.pan)
        transform.Scale(self.params.zoom / self.PIXEL_DENSITY, self.params.zoom / self.PIXEL_DENSITY)
        canvas.SetTransform(transform)

        self.draw_page(canvas)

        stitch = 0
        last_stitch = None

        current_stitch = self.params.current_stitch

        for pen, stitches, jumps in zip(self.pens, self.stitch_blocks, self.jumps):
            canvas.SetPen(pen)
            if stitch + len(stitches) < current_stitch:
                stitch += len(stitches)
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
            else:
                stitches = stitches[:int(current_stitch) - stitch]
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
                break

        if last_stitch and self.params.draw_cursor:
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

        # types-wxpython 0.9.7 incorrectly says GetClientSize() has type Rect (???)
        size = cast(wx.Size, self.GetClientSize())

        one_mm = PIXELS_PER_MM * self.params.zoom
        scale_width = one_mm
        scale_width_mm = 1
        max_width = min(size.width * 0.5, 300)
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
        scale_lower_left_y = size.height - 30

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
        if self.params.render_jumps:
            canvas.StrokeLines(stitches)
        else:
            stitch_blocks = split(stitches, jumps)
            for i, block in enumerate(stitch_blocks):
                if len(block) > 1:
                    canvas.StrokeLines(block)

    def draw_needle_penetration_points(self, canvas: wx.GraphicsContext, pen: wx.Pen, stitches: List[Tuple[float, float]]) -> None:
        if self.params.render_needle_pen_points:
            npp_size = global_settings['simulator_npp_size'] * PIXELS_PER_MM * self.PIXEL_DENSITY
            npp_pen = wx.Pen(pen.GetColour(), width=int(npp_size))
            canvas.SetPen(npp_pen)
            canvas.StrokeLineSegments(stitches, [(stitch[0] + 0.001, stitch[1]) for stitch in stitches])

    def _update_background_color(self) -> None:
        if not self.params.page_specs:
            self.SetBackgroundColour(self.params.background_color or "#FFFFFF")
        else:
            if self.params.show_page:
                self.SetBackgroundColour(self.params.page_specs['desk_color'])
            else:
                self.SetBackgroundColour(self.params.background_color or self.params.page_specs['page_color'])

    def set_stitch_plan(self, stitch_plan: StitchPlan) -> None:
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box

        self.pens: List[wx.Pen] = []
        self.stitch_blocks: List[List[Tuple[float, float]]] = []
        self.jumps: List[List[int]] = []

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)
            stitch_block: List[Tuple[float, float]] = []
            jumps: List[int] = []
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

    def color_to_pen(self, color: ThreadColor) -> wx.Pen:
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        background_color = self.GetBackgroundColour().GetAsString()
        return wx.Pen(list(map(int, color.visible_on_background(background_color).rgb)), int(line_width))

    def update_pen_size(self) -> None:
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        for pen in self.pens:
            pen.SetWidth(int(line_width))
