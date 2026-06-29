# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import time
import math
from typing import Protocol, Tuple, Optional, Union, List, Dict, Any, cast

import wx
from numpy import split

from ...debug.debug import debug
from ...i18n import _
from ...svg import PIXELS_PER_MM
from ...utils.settings import global_settings
from ...stitch_plan import StitchPlan
from ...threads import ThreadColor


# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class DrawingPanelParameterHolder(Protocol):
    # A drawing panel will be passed an instance of DrawingPanelParameterHolder
    # that it can use to look up the current render settings.
    # It should use this as the source of truth and only save values for e.g. caching reasons.

    current_stitch: int

    # Camera settings
    zoom: float
    pan: Tuple[float, float]

    # Page/Background settings
    page_specs: dict
    background_color: Optional[wx.Colour]

    # Render options
    show_page: bool

    @property
    def draw_cursor(self) ->  bool: ...

    @property
    def render_jumps(self) -> bool: ...

    @property
    def render_needle_pen_points(self) -> bool: ...


class DrawingPanelProto(Protocol):
    # Any drawing panel must implement these methods
    def set_stitch_plan(self, stitch_plan: StitchPlan) -> None: ...

class SimpleDrawingPanel(wx.Panel):
    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    def __init__(self, parent: wx.Window, params: DrawingPanelParameterHolder, stitch_plan: StitchPlan) -> None:
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


class DrawingPanel(wx.Panel):
    """"""

    # render no faster than this many frames per second
    TARGET_FPS = 30

    def __init__(self, parent, *args, **kwargs) -> None:
        """"""
        self.parent = parent
        self.stitch_plan: Optional[StitchPlan] = kwargs.pop('stitch_plan', None)
        kwargs['style'] = wx.BORDER_SUNKEN

        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.control_panel = parent.cp
        self.view_panel = parent.vp

        self.renderer: Optional[SimpleDrawingPanel] = None

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.Layout()

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        # self.SetMinSize((300, 300))

        self.animating = False
        self.timer = wx.Timer(self)
        self.last_frame_start = 0.0
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.direction = 1
        self.current_stitch = 0
        self.width = 0
        self.height = 0
        self.loaded = False
        self.page_specs: Dict[str, Any] = {}
        self.show_page = global_settings['toggle_page_button_status']
        self.background_color: Optional[wx.Colour] = None

        # Set initial values as they may be accessed before a stitch plan is available
        # for example through a focus action on the stitch box
        self.num_stitches = 1
        self.commands: List[int] = [STITCH]

        # desired simulation speed in stitches per second
        self.speed = global_settings['simulator_speed']

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_TIMER, self.animate)

        # wait for layouts so that panel size is set
        if self.stitch_plan:
            wx.CallLater(50, self.load, self.stitch_plan)

    def on_resize(self, event: wx.SizeEvent) -> None:
        self.choose_zoom_and_pan()
        self.Layout()
        self.Refresh()

    def clamp_current_stitch(self) -> None:
        if self.current_stitch < 1:
            self.current_stitch = 1
        elif self.current_stitch > self.num_stitches:
            self.current_stitch = self.num_stitches

    def stop_if_at_end(self) -> None:
        if self.direction == -1 and self.current_stitch == 1:
            self.stop()
        elif self.direction == 1 and self.current_stitch == self.num_stitches:
            self.stop()

    def start_if_not_at_end(self) -> None:
        if self.direction == -1 and self.current_stitch > 1:
            self.go()
        elif self.direction == 1 and self.current_stitch < self.num_stitches:
            self.go()

    def animate(self, event: Optional[wx.TimerEvent]=None) -> None:
        if not self.animating:
            return

        # Each frame, we need to advance forward some number of stitches to
        # match the speed setting.  The tricky thing is that with bigger
        # designs, it may take a long time to render a frame.  That might
        # mean that we'll fall behind.  Even if we set our Timer to 30 FPS,
        # we may only actually manage to render 20 FPS or fewer, and the
        # duration of each frame may vary.
        #
        # To deal with that, we'll figure out how many stitches to advance
        # based on how long it took to render the last frame.  We'll always
        # be behind by one frame, but it should work out fine.

        now = time.time()
        if self.last_frame_start:
            frame_time = now - self.last_frame_start
        else:
            frame_time = self.target_frame_period
        self.last_frame_start = now

        stitch_increment = self.speed * frame_time
        self.set_current_stitch(self.current_stitch + self.direction * stitch_increment)


    def clear(self) -> None:
        self.loaded = False
        self.Refresh()

    def load(self, stitch_plan: StitchPlan) -> None:
        self.current_stitch = 1
        self.direction = 1
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.dimensions_mm = stitch_plan.dimensions_mm
        self.num_stitches = stitch_plan.num_stitches
        self.num_trims = stitch_plan.num_trims
        self.num_color_changes = stitch_plan.num_color_blocks - 1
        self.num_stops = stitch_plan.num_stops
        self.num_jumps = stitch_plan.num_jumps - 1
        self.parse_stitch_plan(stitch_plan)
        self.choose_zoom_and_pan()
        self.set_current_stitch(0)

        self.set_status_bar(
            _("Dimensions: {:.2f} x {:.2f}").format(
                stitch_plan.dimensions_mm[0],
                stitch_plan.dimensions_mm[1]
            ),
            1
        )

        self.loaded = True

        if self.renderer is None:
            self.renderer = SimpleDrawingPanel(self, self, stitch_plan)

            self.renderer.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_button_down)
            self.renderer.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

            self.sizer.Add(self.renderer, 1, wx.EXPAND)
            self.sizer.Layout()
            self.Layout()
            self.Refresh()
        else:
            self.renderer.set_stitch_plan(stitch_plan)

        if hasattr(self.view_panel, 'info_panel') and self.view_panel.info_panel is not None:
            self.view_panel.info_panel.update()

    def set_status_bar(self, msg: str, pos: int) -> None:
        # This doesn't really belong here.
        tlp = self.GetTopLevelParent()
        if isinstance(tlp, wx.Frame):
            statusbar = tlp.GetStatusBar()
            if statusbar is not None:
                statusbar.SetStatusText(msg, pos)


    def parse_stitch_plan(self, stitch_plan: StitchPlan) -> None:
        # There is no 0th stitch, so add a place-holder.
        self.commands = [STITCH]

        for color_block in stitch_plan:
            for stitch in color_block:

                if stitch.trim:
                    self.commands.append(TRIM)
                elif stitch.jump:
                    self.commands.append(JUMP)
                elif stitch.stop:
                    self.commands.append(STOP)
                elif stitch.color_change:
                    self.commands.append(COLOR_CHANGE)
                else:
                    self.commands.append(STITCH)

    def set_page_specs(self, page_specs) -> None:
        self.SetBackgroundColour(page_specs['desk_color'])
        self.page_specs = page_specs

    def set_background_color(self, color: wx.Colour) -> None:
        self.background_color = color

    def set_show_page(self, show_page: bool) -> None:
        self.show_page = show_page

    def choose_zoom_and_pan(self) -> None:
        # ignore if EVT_SIZE fired before we load the stitch plan
        if not self.width and not self.height:
            return

        # types-wxpython 0.9.7 incorrectly says GetClientSize() has type Rect (???)
        size = cast(wx.Size, self.GetClientSize())

        # add some padding to make stitches at the edge more visible
        width_ratio = size.width / float(self.width + 10)
        height_ratio = size.height / float(self.height + 10)
        self.zoom = max(min(width_ratio, height_ratio), 0.01)

        # center the design
        self.pan = ((size.width - self.zoom * self.width) / 2.0,
                    (size.height - self.zoom * self.height) / 2.0)

    def stop(self) -> None:
        self.animating = False
        self.timer.Stop()
        self.control_panel.on_stop()

    def go(self) -> None:
        if not self.loaded:
            return

        if not self.animating:
            try:
                self.animating = True
                self.last_frame_start = 0
                self.timer.Start(int(self.target_frame_period * 1000))
                self.animate()
                self.control_panel.on_start()
            except RuntimeError:
                pass

    def set_speed(self, speed: int) -> None:
        self.speed = speed
        global_settings['simulator_speed'] = speed

    def forward(self) -> None:
        self.direction = 1
        self.start_if_not_at_end()

    def reverse(self) -> None:
        self.direction = -1
        self.start_if_not_at_end()

    def set_current_stitch(self, stitch: Union[int, float]) -> None: # Todo: Hunt down who's passing `float`s to this
        self.current_stitch = int(stitch)
        self.clamp_current_stitch()
        try:
            command = self.commands[int(self.current_stitch)]
        except IndexError:
            # no stitch plan loaded yet, do nothing for now
            return
        self.control_panel.on_current_stitch(int(self.current_stitch), command)
        self.set_status_bar(_("Command: %s") % COMMAND_NAMES[command], 2)
        self.stop_if_at_end()
        self.Refresh()

    def restart(self) -> None:
        if self.direction == 1:
            self.current_stitch = 1
        elif self.direction == -1:
            self.current_stitch = self.num_stitches

        self.go()

    def one_stitch_forward(self) -> None:
        self.set_current_stitch(self.current_stitch + 1)

    def one_stitch_backward(self) -> None:
        self.set_current_stitch(self.current_stitch - 1)

    def on_left_mouse_button_down(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if self.loaded:
            obj.CaptureMouse()
            self.drag_start = event.GetPosition()
            self.drag_original_pan = self.pan
            obj.Bind(wx.EVT_MOTION, self.on_drag)
            obj.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_drag_end)
            obj.Bind(wx.EVT_LEFT_UP, self.on_drag_end)

    def on_drag(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if obj.HasCapture() and event.Dragging():
            delta = event.GetPosition()
            offset = (
                delta.x - self.drag_start[0], 
                delta.y - self.drag_start[1]
            )
            self.pan = (self.drag_original_pan[0] + offset[0], self.drag_original_pan[1] + offset[1])
            self.Refresh()

    def on_drag_end(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if obj.HasCapture():
            obj.ReleaseMouse()

        obj.Unbind(wx.EVT_MOTION)
        obj.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        obj.Unbind(wx.EVT_LEFT_UP)

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

    @property
    def draw_cursor(self) -> bool:
        return self.view_panel.btnCursor.GetValue()
    
    @property
    def render_jumps(self) -> bool:
        return self.view_panel.btnJump.GetValue()

    @property
    def render_needle_pen_points(self) -> bool:
        return self.view_panel.btnNpp.GetValue()
