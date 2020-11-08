import sys
import time
import traceback
from threading import Event, Thread

import wx
from wx.lib.intctrl import IntCtrl

from ..i18n import _
from ..stitch_plan import patches_to_stitch_plan, stitch_plan_from_file
from ..svg import PIXELS_PER_MM
from .dialogs import info_dialog

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class ControlPanel(wx.Panel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        self.stitch_plan = kwargs.pop('stitch_plan')
        self.target_stitches_per_second = kwargs.pop('stitches_per_second')
        self.target_duration = kwargs.pop('target_duration')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.statusbar = self.GetTopLevelParent().statusbar

        self.drawing_panel = None
        self.num_stitches = 1
        self.current_stitch = 1
        self.speed = 1
        self.direction = 1

        # Widgets
        self.btnMinus = wx.Button(self, -1, label='-')
        self.btnMinus.Bind(wx.EVT_BUTTON, self.animation_slow_down)
        self.btnMinus.SetToolTip(_('Slow down (arrow down)'))
        self.btnPlus = wx.Button(self, -1, label='+')
        self.btnPlus.Bind(wx.EVT_BUTTON, self.animation_speed_up)
        self.btnPlus.SetToolTip(_('Speed up (arrow up)'))
        self.btnBackwardStitch = wx.Button(self, -1, label='<|')
        self.btnBackwardStitch.Bind(wx.EVT_BUTTON, self.animation_one_stitch_backward)
        self.btnBackwardStitch.SetToolTip(_('Go on step backward (-)'))
        self.btnForwardStitch = wx.Button(self, -1, label='|>')
        self.btnForwardStitch.Bind(wx.EVT_BUTTON, self.animation_one_stitch_forward)
        self.btnForwardStitch.SetToolTip(_('Go on step forward (+)'))
        self.directionBtn = wx.Button(self, -1, label='<<')
        self.directionBtn.Bind(wx.EVT_BUTTON, self.on_direction_button)
        self.directionBtn.SetToolTip(_('Switch direction (arrow left | arrow right)'))
        self.pauseBtn = wx.Button(self, -1, label=_('Pause'))
        self.pauseBtn.Bind(wx.EVT_BUTTON, self.on_pause_start_button)
        self.pauseBtn.SetToolTip(_('Pause (P)'))
        self.restartBtn = wx.Button(self, -1, label=_('Restart'))
        self.restartBtn.Bind(wx.EVT_BUTTON, self.animation_restart)
        self.restartBtn.SetToolTip(_('Restart (R)'))
        self.nppBtn = wx.ToggleButton(self, -1, label=_('O'))
        self.nppBtn.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_npp)
        self.nppBtn.SetToolTip(_('Display needle penetration point (O)'))
        self.quitBtn = wx.Button(self, -1, label=_('Quit'))
        self.quitBtn.Bind(wx.EVT_BUTTON, self.animation_quit)
        self.quitBtn.SetToolTip(_('Quit (Q)'))
        self.slider = wx.Slider(self, -1, value=1, minValue=1, maxValue=2,
                                style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider)
        self.stitchBox = IntCtrl(self, -1, value=1, min=1, max=2, limited=True, allow_none=True, style=wx.TE_PROCESS_ENTER)
        self.stitchBox.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_SET_FOCUS, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_TEXT_ENTER, self.on_stitch_box_focusout)
        self.stitchBox.Bind(wx.EVT_KILL_FOCUS, self.on_stitch_box_focusout)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focusout)

        # Layout
        self.vbSizer = vbSizer = wx.BoxSizer(wx.VERTICAL)
        self.hbSizer1 = hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbSizer2 = hbSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer1.Add(self.slider, 1, wx.EXPAND | wx.ALL, 3)
        hbSizer1.Add(self.stitchBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        vbSizer.Add(hbSizer1, 1, wx.EXPAND | wx.ALL, 3)
        hbSizer2.Add(self.btnMinus, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.btnPlus, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.btnBackwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.btnForwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.directionBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.pauseBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.restartBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.nppBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.quitBtn, 0, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(hbSizer2, 0, wx.EXPAND | wx.ALL, 3)
        self.SetSizerAndFit(vbSizer)

        # Keyboard Shortcuts
        shortcut_keys = [
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, self.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_RIGHT, self.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, self.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_LEFT, self.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('+'), self.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('='), self.animation_one_stitch_forward),
            (wx.ACCEL_SHIFT, ord('='), self.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_ADD, self.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, self.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('-'), self.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('_'), self.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, self.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, self.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('r'), self.animation_restart),
            (wx.ACCEL_NORMAL, ord('o'), self.on_toggle_npp_shortcut),
            (wx.ACCEL_NORMAL, ord('p'), self.on_pause_start_button),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, self.on_pause_start_button),
            (wx.ACCEL_NORMAL, ord('q'), self.animation_quit)]

        self.accel_entries = []

        for shortcut_key in shortcut_keys:
            eventId = wx.NewIdRef()
            self.accel_entries.append((shortcut_key[0], shortcut_key[1], eventId))
            self.Bind(wx.EVT_MENU, shortcut_key[2], id=eventId)

        self.accel_table = wx.AcceleratorTable(self.accel_entries)
        self.SetAcceleratorTable(self.accel_table)
        self.SetFocus()

    def set_drawing_panel(self, drawing_panel):
        self.drawing_panel = drawing_panel
        self.drawing_panel.set_speed(self.speed)

    def set_num_stitches(self, num_stitches):
        if num_stitches < 2:
            # otherwise the slider and intctrl get mad
            num_stitches = 2
        self.num_stitches = num_stitches
        self.stitchBox.SetMax(num_stitches)
        self.slider.SetMax(num_stitches)
        self.choose_speed()

    def choose_speed(self):
        if self.target_duration:
            self.set_speed(int(self.num_stitches / float(self.target_duration)))
        else:
            self.set_speed(self.target_stitches_per_second)

    def animation_forward(self, event=None):
        self.directionBtn.SetLabel("<<")
        self.drawing_panel.forward()
        self.direction = 1
        self.update_speed_text()

    def animation_reverse(self, event=None):
        self.directionBtn.SetLabel(">>")
        self.drawing_panel.reverse()
        self.direction = -1
        self.update_speed_text()

    def on_direction_button(self, event):
        if self.direction == 1:
            self.animation_reverse()
        else:
            self.animation_forward()

    def set_speed(self, speed):
        self.speed = int(max(speed, 1))
        self.update_speed_text()

        if self.drawing_panel:
            self.drawing_panel.set_speed(self.speed)

    def update_speed_text(self):
        self.statusbar.SetStatusText(_('Speed: %d stitches/sec') % (self.speed * self.direction), 0)
        self.hbSizer2.Layout()

    def on_slider(self, event):
        stitch = event.GetEventObject().GetValue()
        self.stitchBox.SetValue(stitch)

        if self.drawing_panel:
            self.drawing_panel.set_current_stitch(stitch)

        self.parent.SetFocus()

    def on_current_stitch(self, stitch, command):
        if self.current_stitch != stitch:
            self.current_stitch = stitch
            self.slider.SetValue(stitch)
            self.stitchBox.SetValue(stitch)
            self.statusbar.SetStatusText(COMMAND_NAMES[command], 1)

    def on_stitch_box_focus(self, event):
        self.animation_pause()
        self.SetAcceleratorTable(wx.AcceleratorTable([]))
        event.Skip()

    def on_stitch_box_focusout(self, event):
        self.SetAcceleratorTable(self.accel_table)
        stitch = self.stitchBox.GetValue()
        self.parent.SetFocus()

        if stitch is None:
            stitch = 1
            self.stitchBox.SetValue(1)

        self.slider.SetValue(stitch)

        if self.drawing_panel:
            self.drawing_panel.set_current_stitch(stitch)

    def animation_slow_down(self, event):
        """"""
        self.set_speed(self.speed / 2.0)

    def animation_speed_up(self, event):
        """"""
        self.set_speed(self.speed * 2.0)

    def animation_pause(self, event=None):
        self.drawing_panel.stop()

    def animation_start(self, event=None):
        self.drawing_panel.go()

    def on_start(self):
        self.pauseBtn.SetLabel(_('Pause'))

    def on_stop(self):
        self.pauseBtn.SetLabel(_('Start'))

    def on_pause_start_button(self, event):
        """"""
        if self.pauseBtn.GetLabel() == _('Pause'):
            self.animation_pause()
        else:
            self.animation_start()

    def animation_one_stitch_forward(self, event):
        self.animation_pause()
        self.drawing_panel.one_stitch_forward()

    def animation_one_stitch_backward(self, event):
        self.animation_pause()
        self.drawing_panel.one_stitch_backward()

    def animation_quit(self, event):
        self.parent.quit()

    def animation_restart(self, event):
        self.drawing_panel.restart()

    def on_toggle_npp_shortcut(self, event):
        self.nppBtn.SetValue(not self.nppBtn.GetValue())
        self.toggle_npp(event)

    def toggle_npp(self, event):
        if self.pauseBtn.GetLabel() == _('Start'):
            stitch = self.stitchBox.GetValue()
            self.drawing_panel.set_current_stitch(stitch)


class DrawingPanel(wx.Panel):
    """"""

    # render no faster than this many frames per second
    TARGET_FPS = 30

    # It's not possible to specify a line thickness less than 1 pixel, even
    # though we're drawing anti-aliased lines.  To get around this we scale
    # the stitch positions up by this factor and then scale down by a
    # corresponding amount during rendering.
    PIXEL_DENSITY = 10

    # Line width in pixels.
    LINE_THICKNESS = 0.4

    def __init__(self, *args, **kwargs):
        """"""
        self.stitch_plan = kwargs.pop('stitch_plan')
        self.control_panel = kwargs.pop('control_panel')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        self.SetMinSize((100, 100))
        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        self.animating = False
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.last_frame_duration = 0
        self.direction = 1
        self.current_stitch = 0
        self.black_pen = wx.Pen((128, 128, 128))
        self.width = 0
        self.height = 0
        self.loaded = False

        # desired simulation speed in stitches per second
        self.speed = 16

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.choose_zoom_and_pan)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_button_down)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

        # wait for layouts so that panel size is set
        wx.CallLater(50, self.load, self.stitch_plan)

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

    def animate(self):
        if not self.animating:
            return

        frame_time = max(self.target_frame_period, self.last_frame_duration)

        # No sense in rendering more frames per second than our desired stitches
        # per second.
        frame_time = max(frame_time, 1.0 / self.speed)

        stitch_increment = int(self.speed * frame_time)

        self.set_current_stitch(self.current_stitch + self.direction * stitch_increment)
        wx.CallLater(int(1000 * frame_time), self.animate)

    def OnPaint(self, e):
        if not self.loaded:
            return

        dc = wx.PaintDC(self)
        canvas = wx.GraphicsContext.Create(dc)

        self.draw_stitches(canvas)
        self.draw_scale(canvas)

    def draw_stitches(self, canvas):
        canvas.BeginLayer(1)

        transform = canvas.GetTransform()
        transform.Translate(*self.pan)
        transform.Scale(self.zoom / self.PIXEL_DENSITY, self.zoom / self.PIXEL_DENSITY)
        canvas.SetTransform(transform)

        stitch = 0
        last_stitch = None

        start = time.time()
        for pen, stitches in zip(self.pens, self.stitch_blocks):
            canvas.SetPen(pen)
            if stitch + len(stitches) < self.current_stitch:
                stitch += len(stitches)
                if len(stitches) > 1:
                    canvas.DrawLines(stitches)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                last_stitch = stitches[-1]
            else:
                stitches = stitches[:self.current_stitch - stitch]
                if len(stitches) > 1:
                    canvas.DrawLines(stitches)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                last_stitch = stitches[-1]
                break
        self.last_frame_duration = time.time() - start

        if last_stitch:
            self.draw_crosshair(last_stitch[0], last_stitch[1], canvas, transform)

        canvas.EndLayer()

    def draw_crosshair(self, x, y, canvas, transform):
        x, y = transform.TransformPoint(float(x), float(y))
        canvas.SetTransform(canvas.CreateMatrix())
        crosshair_radius = 10
        canvas.SetPen(self.black_pen)
        canvas.DrawLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
        canvas.DrawLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))

    def draw_scale(self, canvas):
        canvas.BeginLayer(1)

        canvas_width, canvas_height = self.GetClientSize()

        one_mm = PIXELS_PER_MM * self.zoom
        scale_width = one_mm
        max_width = min(canvas_width * 0.5, 300)

        while scale_width > max_width:
            scale_width /= 2.0

        while scale_width < 50:
            scale_width += one_mm

        scale_width_mm = scale_width / self.zoom / PIXELS_PER_MM

        # The scale bar looks like this:
        #
        # |           |
        # |_____|_____|

        scale_lower_left_x = 20
        scale_lower_left_y = canvas_height - 20

        canvas.DrawLines(((scale_lower_left_x, scale_lower_left_y - 6),
                          (scale_lower_left_x, scale_lower_left_y),
                          (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y),
                          (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y - 3),
                          (scale_lower_left_x + scale_width / 2.0, scale_lower_left_y),
                          (scale_lower_left_x + scale_width, scale_lower_left_y),
                          (scale_lower_left_x + scale_width, scale_lower_left_y - 5)))

        canvas.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL), wx.Colour((0, 0, 0)))
        canvas.DrawText("%s mm" % scale_width_mm, scale_lower_left_x, scale_lower_left_y + 5)

        canvas.EndLayer()

    def draw_needle_penetration_points(self, canvas, pen, stitches):
        if self.control_panel.nppBtn.GetValue():
            npp_pen = wx.Pen(pen.GetColour(), width=int(0.3 * PIXELS_PER_MM * self.PIXEL_DENSITY))
            canvas.SetPen(npp_pen)
            canvas.StrokeLineSegments(stitches, stitches)

    def clear(self):
        dc = wx.ClientDC(self)
        dc.Clear()

    def load(self, stitch_plan):
        self.current_stitch = 1
        self.direction = 1
        self.last_frame_duration = 0
        self.num_stitches = stitch_plan.num_stitches
        self.control_panel.set_num_stitches(self.num_stitches)
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.parse_stitch_plan(stitch_plan)
        self.choose_zoom_and_pan()
        self.set_current_stitch(0)
        self.loaded = True
        self.go()

    def choose_zoom_and_pan(self, event=None):
        # ignore if EVT_SIZE fired before we load the stitch plan
        if not self.width and not self.height and event is not None:
            return

        panel_width, panel_height = self.GetClientSize()

        # add some padding to make stitches at the edge more visible
        width_ratio = panel_width / float(self.width + 10)
        height_ratio = panel_height / float(self.height + 10)
        self.zoom = min(width_ratio, height_ratio)

        # center the design
        self.pan = ((panel_width - self.zoom * self.width) / 2.0,
                    (panel_height - self.zoom * self.height) / 2.0)

    def stop(self):
        self.animating = False
        self.control_panel.on_stop()

    def go(self):
        if not self.loaded:
            return

        if not self.animating:
            self.animating = True
            self.animate()
            self.control_panel.on_start()

    def color_to_pen(self, color):
        # We draw the thread with a thickness of 0.1mm.  Real thread has a
        # thickness of ~0.4mm, but if we did that, we wouldn't be able to
        # see the individual stitches.
        return wx.Pen(list(map(int, color.visible_on_white.rgb)), int(0.1 * PIXELS_PER_MM * self.PIXEL_DENSITY))

    def parse_stitch_plan(self, stitch_plan):
        self.pens = []
        self.stitch_blocks = []

        # There is no 0th stitch, so add a place-holder.
        self.commands = [None]

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)
            stitch_block = []

            for stitch in color_block:
                # trim any whitespace on the left and top and scale to the
                # pixel density
                stitch_block.append((self.PIXEL_DENSITY * (stitch.x - self.minx),
                                     self.PIXEL_DENSITY * (stitch.y - self.miny)))

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

                if stitch.trim or stitch.stop or stitch.color_change:
                    self.pens.append(pen)
                    self.stitch_blocks.append(stitch_block)
                    stitch_block = []

            if stitch_block:
                self.pens.append(pen)
                self.stitch_blocks.append(stitch_block)

    def set_speed(self, speed):
        self.speed = speed

    def forward(self):
        self.direction = 1
        self.start_if_not_at_end()

    def reverse(self):
        self.direction = -1
        self.start_if_not_at_end()

    def set_current_stitch(self, stitch):
        self.current_stitch = stitch
        self.clamp_current_stitch()
        self.control_panel.on_current_stitch(self.current_stitch, self.commands[self.current_stitch])
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


class SimulatorPanel(wx.Panel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        stitch_plan = kwargs.pop('stitch_plan')
        target_duration = kwargs.pop('target_duration')
        stitches_per_second = kwargs.pop('stitches_per_second')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.cp = ControlPanel(self,
                               stitch_plan=stitch_plan,
                               stitches_per_second=stitches_per_second,
                               target_duration=target_duration)
        self.dp = DrawingPanel(self, stitch_plan=stitch_plan, control_panel=self.cp)
        self.cp.set_drawing_panel(self.dp)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(self.cp, 0, wx.EXPAND | wx.ALL, 2)
        self.SetSizerAndFit(vbSizer)

    def quit(self):
        self.parent.quit()

    def go(self):
        self.dp.go()

    def stop(self):
        self.dp.stop()

    def load(self, stitch_plan):
        self.dp.load(stitch_plan)

    def clear(self):
        self.dp.clear()


class EmbroiderySimulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.on_close_hook = kwargs.pop('on_close', None)
        stitch_plan = kwargs.pop('stitch_plan', None)
        stitches_per_second = kwargs.pop('stitches_per_second', 16)
        target_duration = kwargs.pop('target_duration', None)
        size = kwargs.get('size', (0, 0))
        wx.Frame.__init__(self, *args, **kwargs)
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([250, -1])

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.simulator_panel = SimulatorPanel(self,
                                              stitch_plan=stitch_plan,
                                              target_duration=target_duration,
                                              stitches_per_second=stitches_per_second)
        sizer.Add(self.simulator_panel, 1, wx.EXPAND)

        # self.SetSizerAndFit() sets the minimum size so that the buttons don't
        # get squished.  But it then also shrinks the window down to that size.
        self.SetSizerAndFit(sizer)

        # Therefore we have to reapply the size that the caller asked for.
        self.SetSize(size)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def quit(self):
        self.Close()

    def on_close(self, event):
        self.simulator_panel.stop()

        if self.on_close_hook:
            self.on_close_hook()

        self.SetFocus()
        self.Destroy()

    def go(self):
        self.simulator_panel.go()

    def stop(self):
        self.simulator_panel.stop()

    def load(self, stitch_plan):
        self.simulator_panel.load(stitch_plan)

    def clear(self):
        self.simulator_panel.clear()


class SimulatorPreview(Thread):
    """Manages a preview simulation and a background thread for generating patches."""

    def __init__(self, parent, *args, **kwargs):
        """Construct a SimulatorPreview.

        The parent is expected to be a wx.Window and also implement the following methods:

            def generate_patches(self, abort_event):
                Produce an list of Patch instances.  This method will be
                invoked in a background thread and it is expected that it may
                take awhile.

                If possible, this method should periodically check
                abort_event.is_set(), and if True, stop early.  The return
                value will be ignored in this case.
        """
        self.parent = parent
        self.target_duration = kwargs.pop('target_duration', 5)
        super(SimulatorPreview, self).__init__(*args, **kwargs)
        self.daemon = True

        self.simulate_window = None
        self.refresh_needed = Event()

        # used when closing to avoid having the window reopen at the last second
        self._disabled = False

        wx.CallLater(1000, self.update)

    def disable(self):
        self._disabled = True

    def update(self):
        """Request an update of the simulator preview with freshly-generated patches."""

        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.clear()

        if self._disabled:
            return

        if not self.is_alive():
            self.start()

        self.refresh_needed.set()

    def run(self):
        while True:
            self.refresh_needed.wait()
            self.refresh_needed.clear()
            self.update_patches()

    def update_patches(self):
        try:
            patches = self.parent.generate_patches(self.refresh_needed)
        except:  # noqa: E722
            # If something goes wrong when rendering patches, it's not great,
            # but we don't really want the simulator thread to crash.  Instead,
            # just swallow the exception and abort.  It'll show up when they
            # try to actually embroider the shape.
            return

        if patches and not self.refresh_needed.is_set():
            stitch_plan = patches_to_stitch_plan(patches)

            # GUI stuff needs to happen in the main thread, so we ask the main
            # thread to call refresh_simulator().
            wx.CallAfter(self.refresh_simulator, patches, stitch_plan)

    def refresh_simulator(self, patches, stitch_plan):
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.load(stitch_plan)
        else:
            params_rect = self.parent.GetScreenRect()
            simulator_pos = params_rect.GetTopRight()
            simulator_pos.x += 5

            current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
            display = wx.Display(current_screen)
            screen_rect = display.GetClientArea()
            simulator_pos.y = screen_rect.GetTop()

            width = screen_rect.GetWidth() - params_rect.GetWidth()
            height = screen_rect.GetHeight()

            try:
                self.simulate_window = EmbroiderySimulator(None, -1, _("Preview"),
                                                           simulator_pos,
                                                           size=(width, height),
                                                           stitch_plan=stitch_plan,
                                                           on_close=self.simulate_window_closed,
                                                           target_duration=self.target_duration)
            except Exception:
                error = traceback.format_exc()

                try:
                    # a window may have been created, so we need to destroy it
                    # or the app will never exit
                    wx.Window.FindWindowByName(_("Preview")).Destroy()
                except Exception:
                    pass

                info_dialog(self, error, _("Internal Error"))

            self.simulate_window.Show()
            wx.CallLater(10, self.parent.Raise)

        wx.CallAfter(self.simulate_window.go)

    def simulate_window_closed(self):
        self.simulate_window = None

    def close(self):
        self.disable()
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.Close()


def show_simulator(stitch_plan):
    app = wx.App()
    current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
    display = wx.Display(current_screen)
    screen_rect = display.GetClientArea()

    simulator_pos = (screen_rect[0], screen_rect[1])

    # subtract 1 because otherwise the window becomes maximized on Linux
    width = screen_rect[2] - 1
    height = screen_rect[3] - 1

    frame = EmbroiderySimulator(None, -1, _("Embroidery Simulation"), pos=simulator_pos, size=(width, height), stitch_plan=stitch_plan)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    show_simulator(stitch_plan)
