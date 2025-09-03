# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import time
import math

import wx
from numpy import split

from ...debug.debug import debug
from ...i18n import _
from ...svg import PIXELS_PER_MM
from ...utils.settings import global_settings

from ..experimental.gl_renderer import GLStitchPlanRenderer
import wx.glcanvas as glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import moderngl
from typing import Optional

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class DrawingPanel(glcanvas.GLCanvas):
    """"""

    # render no faster than this many frames per second
    TARGET_FPS = 30

    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        self.stitch_plan = kwargs.pop('stitch_plan', None)
        kwargs['style'] = wx.BORDER_SUNKEN

        glcanvas.GLCanvas.__init__(self, parent, *args, **kwargs)
        self.context = glcanvas.GLContext(self)
        self.init = False # Copying this pattern from the other wxwidgets OpenGL Demo, is it needed, or can I do init now?
        self.renderer: Optional[GLStitchPlanRenderer] = None

        self.control_panel = parent.cp
        self.view_panel = parent.vp

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        self.SetMinSize((300, 300))
        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        self.animating = False
        self.timer = wx.Timer(self)
        self.last_frame_start = 0
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.direction = 1
        self.current_stitch = 0
        self.black_pen = wx.Pen((128, 128, 128))
        self.width = 0
        self.height = 0
        self.loaded = False
        self.page_specs = {}
        self.show_page = global_settings['toggle_page_button_status']
        self.background_color = None

        # Set initial values as they may be accessed before a stitch plan is available
        # for example through a focus action on the stitch box
        self.num_stitches = 1
        self.commands = [None]

        # desired simulation speed in stitches per second
        self.speed = global_settings['simulator_speed']

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.choose_zoom_and_pan)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_button_down)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_TIMER, self.animate)

        # wait for layouts so that panel size is set
        if self.stitch_plan:
            wx.CallLater(50, self.load, self.stitch_plan)

    def on_resize(self, event):
        
        self.choose_zoom_and_pan()
        self.Refresh()

    def clamp_current_stitch(self):
        if self.current_stitch < 1:
            self.current_stitch = 1
        elif self.current_stitch > self.num_stitches:
            self.current_stitch = self.num_stitches

    def stop_if_at_end(self):
        if self.direction == -1 and self.current_stitch == 1:
            self.stop()
        elif self.direction == 1 and self.current_stitch == self.num_stitches:
            self.stop()

    def start_if_not_at_end(self):
        if self.direction == -1 and self.current_stitch > 1:
            self.go()
        elif self.direction == 1 and self.current_stitch < self.num_stitches:
            self.go()

    def animate(self, event=None):
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

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        
        # if not self.loaded:
        #     dc.Clear()
        #     return

        # canvas = wx.GraphicsContext.Create(dc)

        # self.draw_stitches(canvas)
        # self.draw_scale(canvas)

        self.SetCurrent(self.context)
        if not self.init:
            self.ctx = moderngl.get_context()
            if self.stitch_plan:
                self.renderer = GLStitchPlanRenderer(self.ctx, self.stitch_plan)
                size =  self.GetClientSize()
                self.renderer.resize(size.width, size.height)
            self.init = True

        ctx = self.ctx

        fb = ctx.detect_framebuffer()

        fb.use()
        desk_color = wx.Colour(self.page_specs['desk_color'])
        fb.clear(desk_color.Red()/255, desk_color.Green()/255, desk_color.Blue()/255, 1)
        # glClearColor(0.6, 0.7, 1.0, 1.0)
        # glClear(GL_COLOR_BUFFER_BIT)

        if self.renderer:
            self.renderer.set_pan((self.pan[0]-self.minx*self.zoom, self.pan[1]-self.miny*self.zoom))
            self.renderer.set_zoom(self.zoom)
            self.renderer.render(int(self.current_stitch))

        self.SwapBuffers()

        # Interestingly, these graphics can be "stacked", but it seems like it's a little glitchy.
        canvas = wx.GraphicsContext.Create(dc)

        self.draw_scale(canvas)


    def draw_page(self, canvas):
        self._update_background_color()

        if not self.page_specs or not self.show_page:
            return

        with debug.log_exceptions():
            border_color = wx.Colour(self.page_specs['border_color'])
            if self.page_specs['show_page_shadow']:
                canvas.SetPen(wx.TRANSPARENT_PEN)
                canvas.SetBrush(canvas.CreateBrush(wx.Brush(wx.Colour(border_color.Red(), border_color.Green(), border_color.Blue(), alpha=65))))
                canvas.DrawRoundedRectangle(
                    (-self.page_specs['x'] + 4) * self.PIXEL_DENSITY, (-self.page_specs['y'] + 4) * self.PIXEL_DENSITY,
                    self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY,
                    1 * self.PIXEL_DENSITY
                )

            pen = canvas.CreatePen(
                wx.GraphicsPenInfo(wx.Colour(border_color)).Width(1 * self.PIXEL_DENSITY).Join(wx.JOIN_MITER)
            )
            canvas.SetPen(pen)
            canvas.SetBrush(wx.Brush(wx.Colour(self.background_color or self.page_specs['page_color'])))

            canvas.DrawRectangle(
                -self.page_specs['x'] * self.PIXEL_DENSITY, -self.page_specs['y'] * self.PIXEL_DENSITY,
                self.page_specs['width'] * self.PIXEL_DENSITY, self.page_specs['height'] * self.PIXEL_DENSITY
            )

    def draw_stitches(self, canvas):
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
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
            else:
                stitches = stitches[:int(self.current_stitch) - stitch]
                if len(stitches) > 1:
                    self.draw_stitch_lines(canvas, pen, stitches, jumps)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                    last_stitch = stitches[-1]
                break

        if last_stitch and self.view_panel.btnCursor.GetValue():
            self.draw_crosshair(last_stitch[0], last_stitch[1], canvas, transform)

        canvas.EndLayer()

    def draw_crosshair(self, x, y, canvas, transform):
        x, y = transform.TransformPoint(float(x), float(y))
        canvas.SetTransform(canvas.CreateMatrix())
        crosshair_radius = 10
        canvas.SetPen(self.black_pen)
        canvas.StrokeLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
        canvas.StrokeLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))

    def draw_scale(self, canvas):
        canvas.SetTransform(canvas.CreateMatrix())
        canvas.BeginLayer(1)

        canvas_width, canvas_height = self.GetClientSize()

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

    def draw_stitch_lines(self, canvas, pen, stitches, jumps):
        render_jumps = self.view_panel.btnJump.GetValue()
        if render_jumps:
            canvas.StrokeLines(stitches)
        else:
            stitch_blocks = split(stitches, jumps)
            for i, block in enumerate(stitch_blocks):
                if len(block) > 1:
                    canvas.StrokeLines(block)

    def draw_needle_penetration_points(self, canvas, pen, stitches):
        if self.view_panel.btnNpp.GetValue():
            npp_size = global_settings['simulator_npp_size'] * PIXELS_PER_MM * self.PIXEL_DENSITY
            npp_pen = wx.Pen(pen.GetColour(), width=int(npp_size))
            canvas.SetPen(npp_pen)
            canvas.StrokeLineSegments(stitches, [(stitch[0] + 0.001, stitch[1]) for stitch in stitches])

    def clear(self):
        self.loaded = False
        self.Refresh()

    def load(self, stitch_plan):
        self.stitch_plan = stitch_plan
        if self.renderer:
            self.renderer.set_stitch_plan(stitch_plan)

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
        statusbar = self.GetTopLevelParent().statusbar
        statusbar.SetStatusText(
            _("Dimensions: {:.2f} x {:.2f}").format(
                stitch_plan.dimensions_mm[0],
                stitch_plan.dimensions_mm[1]
            ),
            1
        )
        self.loaded = True
        self.go()
        if hasattr(self.view_panel, 'info_panel') and self.view_panel.info_panel is not None:
            self.view_panel.info_panel.update()

    def set_page_specs(self, page_specs):
        self.SetBackgroundColour(page_specs['desk_color'])
        self.page_specs = page_specs

    def set_background_color(self, color):
        self.background_color = color
        self._update_background_color()

    def _update_background_color(self):
        if not self.page_specs:
            self.SetBackgroundColour(self.background_color or "#FFFFFF")
        else:
            if self.show_page:
                self.SetBackgroundColour(self.page_specs['desk_color'])
            else:
                self.SetBackgroundColour(self.background_color or self.page_specs['page_color'])

    def set_show_page(self, show_page):
        self.show_page = show_page
        self._update_background_color()

    def choose_zoom_and_pan(self, event=None):
        # ignore if EVT_SIZE fired before we load the stitch plan
        if not self.width and not self.height and event is not None:
            return

        panel_width, panel_height = self.GetClientSize()

        # add some padding to make stitches at the edge more visible
        width_ratio = panel_width / float(self.width + 10)
        height_ratio = panel_height / float(self.height + 10)
        self.zoom = max(min(width_ratio, height_ratio), 0.01)

        # center the design
        self.pan = ((panel_width - self.zoom * self.width) / 2.0,
                    (panel_height - self.zoom * self.height) / 2.0)

    def stop(self):
        self.animating = False
        self.timer.Stop()
        self.control_panel.on_stop()

    def go(self):
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

    def color_to_pen(self, color):
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        background_color = self.GetBackgroundColour().GetAsString()
        return wx.Pen(list(map(int, color.visible_on_background(background_color).rgb)), int(line_width))

    def update_pen_size(self):
        line_width = global_settings['simulator_line_width'] * PIXELS_PER_MM * self.PIXEL_DENSITY
        for pen in self.pens:
            pen.SetWidth(int(line_width))

    def parse_stitch_plan(self, stitch_plan):
        self.pens = []
        self.stitch_blocks = []
        self.jumps = []

        # There is no 0th stitch, so add a place-holder.
        self.commands = [None]

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

                if stitch.trim:
                    self.commands.append(TRIM)
                elif stitch.jump:
                    self.commands.append(JUMP)
                    jumps.append(stitch_index)
                elif stitch.stop:
                    self.commands.append(STOP)
                elif stitch.color_change:
                    self.commands.append(COLOR_CHANGE)
                else:
                    self.commands.append(STITCH)

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

    def set_speed(self, speed):
        self.speed = speed
        global_settings['simulator_speed'] = speed

    def forward(self):
        self.direction = 1
        self.start_if_not_at_end()

    def reverse(self):
        self.direction = -1
        self.start_if_not_at_end()

    def set_current_stitch(self, stitch):
        self.current_stitch = stitch
        self.clamp_current_stitch()
        try:
            command = self.commands[int(self.current_stitch)]
        except IndexError:
            # no stitch plan loaded yet, do nothing for now
            return
        self.control_panel.on_current_stitch(int(self.current_stitch), command)
        statusbar = self.GetTopLevelParent().statusbar
        statusbar.SetStatusText(_("Command: %s") % COMMAND_NAMES[command], 2)
        self.stop_if_at_end()
        self.Refresh()

    def restart(self):
        if self.direction == 1:
            self.current_stitch = 1
        elif self.direction == -1:
            self.current_stitch = self.num_stitches

        self.go()

    def one_stitch_forward(self):
        self.set_current_stitch(self.current_stitch + 1)

    def one_stitch_backward(self):
        self.set_current_stitch(self.current_stitch - 1)

    def on_left_mouse_button_down(self, event):
        if self.loaded:
            self.CaptureMouse()
            self.drag_start = event.GetPosition()
            self.drag_original_pan = self.pan
            self.Bind(wx.EVT_MOTION, self.on_drag)
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_drag_end)
            self.Bind(wx.EVT_LEFT_UP, self.on_drag_end)

    def on_drag(self, event):
        if self.HasCapture() and event.Dragging():
            delta = event.GetPosition()
            offset = (delta[0] - self.drag_start[0], delta[1] - self.drag_start[1])
            self.pan = (self.drag_original_pan[0] + offset[0], self.drag_original_pan[1] + offset[1])
            self.Refresh()

    def on_drag_end(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        self.Unbind(wx.EVT_LEFT_UP)

    def on_mouse_wheel(self, event):
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
