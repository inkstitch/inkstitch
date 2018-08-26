import sys
import wx
from wx.lib.intctrl import IntCtrl
import time
from itertools import izip

from .svg import color_block_to_point_lists
from .i18n import _

class ControlPanel(wx.Panel):
    """"""
    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        self.drawing_panel = kwargs.pop('drawing_panel')
        self.stitch_plan = kwargs.pop('stitch_plan')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.num_stitches = self.stitch_plan.num_stitches

        # Widgets
        self.btnMinus = wx.Button(self, -1, label='-')
        self.btnMinus.Bind(wx.EVT_BUTTON, self.OnSpeedMinus)
        self.btnPlus = wx.Button(self, -1, label='+')
        self.btnPlus.Bind(wx.EVT_BUTTON, self.OnSpeedPlus)
        self.direction = wx.Button(self, -1, label='>>')
        self.direction.Bind(wx.EVT_BUTTON, self.OnDirection)
        self.pauseBtn = wx.Button(self, -1, label='Pause')
        self.pauseBtn.Bind(wx.EVT_BUTTON, self.OnPauseStart)
        self.restartBtn = wx.Button(self, -1, label='Restart')
        self.restartBtn.Bind(wx.EVT_BUTTON, self.on_restart)
        self.quitBtn = wx.Button(self, -1, label='Quit')
        self.quitBtn.Bind(wx.EVT_BUTTON, self.on_quit)
        self.slider = wx.Slider(self, -1, value=1, minValue=1, maxValue=self.num_stitches,
                                style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider)
        self.stitchBox = IntCtrl(self, -1, value=0, min=0, max=self.num_stitches, limited=True, allow_none=False)
        self.stitchBox.Bind(wx.EVT_TEXT, self.on_stitch_box)
        self.speedST = wx.StaticText(self, -1, label='', style=wx.ALIGN_CENTER)

        # Layout
        self.vbSizer = vbSizer = wx.BoxSizer(wx.VERTICAL)
        self.hbSizer1 = hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbSizer2 = hbSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer1.Add(self.slider, 1, wx.EXPAND | wx.ALL, 3)
        hbSizer1.Add(self.stitchBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        vbSizer.Add(hbSizer1, 1, wx.EXPAND | wx.ALL, 3)
        hbSizer2.Add(self.speedST, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hbSizer2.AddStretchSpacer(prop=1)
        hbSizer2.Add(self.btnMinus, 0, wx.ALL, 2)
        hbSizer2.Add(self.btnPlus, 0, wx.ALL, 2)
        hbSizer2.Add(self.direction, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.pauseBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.restartBtn, 0, wx.EXPAND | wx.ALL, 2)
        hbSizer2.Add(self.quitBtn, 0, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(hbSizer2, 0, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(vbSizer)

        self.set_speed(16)

    def OnDirection(self, event):
        """
        Handles the ``wx.EVT_BUTTON`` event.

        :param `event`: A `wx.CommandEvent` to be processed.
        :type `event`: `wx.CommandEvent`
        """
        evtObj = event.GetEventObject()
        lbl = evtObj.GetLabel()
        if lbl == '>>':
            evtObj.SetLabel('<<')
            self.drawing_panel.reverse()
        else:
            evtObj.SetLabel('>>')
            self.drawing_panel.forward()

    def set_speed(self, speed):
        self.speed = int(max(speed, 1))
        self.drawing_panel.set_speed(self.speed)
        self.speedST.SetLabel('Speed: %s stitches/sec' % self.speed)
        self.hbSizer2.Layout()

    def on_slider(self, event):
        stitch = event.GetEventObject().GetValue()
        self.stitchBox.SetValue(stitch)
        self.drawing_panel.set_current_stitch(stitch)

    def set_current_stitch(self, stitch):
        self.slider.SetValue(stitch)
        self.stitchBox.SetValue(stitch)

    def set_stitch_label(self, stitch):
        self.st1.SetLabel("Stitch # %d/%d" % (stitch, self.num_stitches))

    def on_stitch_box(self, event):
        stitch = self.stitchBox.GetValue()
        self.slider.SetValue(stitch)
        self.drawing_panel.set_current_stitch(stitch)

    def OnSpeedMinus(self, event):
        """"""
        self.set_speed(self.speed / 2.0)

    def OnSpeedPlus(self, event):
        """"""
        self.set_speed(self.speed * 2.0)

    def OnPauseStart(self, event):
        """"""
        evtObj = event.GetEventObject()
        lbl = evtObj.GetLabel()
        if lbl == 'Pause':
            self.drawing_panel.stop()
            evtObj.SetLabel('Start')
        else:
            self.drawing_panel.go()
            evtObj.SetLabel('Pause')

    def on_quit(self, event):
        self.parent.quit()

    def on_restart(self, event):
        self.drawing_panel.restart()

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
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)

        self.SetBackgroundColour('#FFFFFF')
        self.SetDoubleBuffered(True)

        self.animating = False
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.last_frame_duration = 0
        self.direction = 1
        self.current_stitch = 0
        self.control_panel = None

        # desired simulation speed in stitches per second
        self.speed = 10

        self.black_pen = self.create_pen((0, 0, 0))

        self.load(self.stitch_plan)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def set_control_panel(self, control_panel):
        self.control_panel = control_panel

    def clamp_current_stitch(self):
        if self.current_stitch < 0:
            self.current_stitch = 0
        elif self.current_stitch > self.num_stitches:
            self.current_stitch = self.num_stitches

    def stop_if_at_end(self):
        if self.direction == -1 and self.current_stitch == 0:
            self.stop()
        elif self.direction == 1 and self.current_stitch == self.num_stitches:
            self.stop()

    def start_if_not_at_end(self):
        if self.direction == -1 and self.current_stitch > 0:
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

        #print >> sys.stderr, time.time(), "animate", self.current_stitch, stitch_increment, self.last_frame_duration, frame_time

        self.current_stitch += self.direction * stitch_increment
        self.clamp_current_stitch()
        self.stop_if_at_end()

        if self.control_panel:
            self.control_panel.set_current_stitch(self.current_stitch)

        self.Refresh()

        wx.CallLater(int(1000 * max(0.001, frame_time - self.last_frame_duration)), self.animate)

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        canvas = wx.GraphicsContext.Create(dc)

        transform = canvas.GetTransform()
        transform.Scale(2.0 / self.PIXEL_DENSITY, 2.0 / self.PIXEL_DENSITY)
        canvas.SetTransform(transform)

        stitch = 0
        last_stitch = None

        start = time.time()
        for pen, stitches in izip(self.pens, self.stitch_blocks):
            canvas.SetPen(pen)
            if stitch + len(stitches) < self.current_stitch:
                stitch += len(stitches)
                canvas.DrawLines(stitches)
                last_stitch = stitches[-1]
            else:
                stitches = stitches[:self.current_stitch - stitch]
                if len(stitches) > 1:
                    canvas.DrawLines(stitches)
                    last_stitch = stitches[-1]
                break
        self.last_frame_duration = time.time() - start

        if last_stitch:
            x = last_stitch[0]
            y = last_stitch[1]
            crosshair_radius = 4 * self.PIXEL_DENSITY
            canvas.SetPen(self.black_pen)
            canvas.DrawLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
            canvas.DrawLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))


    def load(self, stitch_plan=None):
        if stitch_plan:
            self.num_stitches = stitch_plan.num_stitches
            self.parse_stitch_plan(stitch_plan)
            self.move_to_top_left()
            return

    def stop(self):
        self.animating = False

    def go(self):
        if not self.animating:
            self.animating = True
            self.animate()

    def create_pen(self, rgb):
        return wx.Pen(rgb, width=int(0.4 * self.PIXEL_DENSITY))

    def color_to_pen(self, color):
        return self.create_pen(color.visible_on_white.rgb)

    def parse_stitch_plan(self, stitch_plan):
        self.pens = []
        self.stitch_blocks = []

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)

            for point_list in color_block_to_point_lists(color_block):
                self.pens.append(pen)
                self.stitch_blocks.append(point_list)

    def move_to_top_left(self):
        """remove any unnecessary whitespace around the design"""

        minx, miny, maxx, maxy = self.stitch_plan.bounding_box

        for block in self.stitch_blocks:
            stitches = []
            for stitch in block:
                stitches.append((self.PIXEL_DENSITY * (stitch[0] - minx), self.PIXEL_DENSITY * (stitch[1] - miny)))
            block[:] = stitches

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
        self.stop_if_at_end()
        self.Refresh()

    def restart(self):
        if self.direction == 1:
            self.current_stitch = 0
        elif self.direction == -1:
            self.current_stitch = self.num_stitches

        self.go()


class SimulatorPanel(wx.Panel):
    """"""
    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        stitch_plan = kwargs.pop('stitch_plan')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.dp = DrawingPanel(self, stitch_plan=stitch_plan)
        self.cp = ControlPanel(self, stitch_plan=stitch_plan, drawing_panel=self.dp)
        self.dp.set_control_panel(self.cp)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(self.cp, 0, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(vbSizer)

        self.dp.go()

    def quit(self):
        self.parent.quit()

    def stop(self):
        self.dp.stop()


class EmbroiderySimulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        stitch_plan = kwargs.pop('stitch_plan', None)
        self.x_position = kwargs.pop('x_position', None)
        self.on_close_hook = kwargs.pop('on_close', None)
        self.frame_period = kwargs.pop('frame_period', 80)
        self.stitches_per_frame = kwargs.pop('stitches_per_frame', 1)
        self.target_duration = kwargs.pop('target_duration', None)
        self.max_height = kwargs.pop('max_height', None)
        self.max_width = kwargs.pop('max_width', None)
        wx.Frame.__init__(self, *args, **kwargs)

        # self.status_bar = self.CreateStatusBar()
        # self.status_bar.SetStatusText(text)

        self.simulator_panel = SimulatorPanel(self, stitch_plan=stitch_plan)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def quit(self):
        self.Close()

    def on_close(self, event):
        self.simulator_panel.stop()

        if self.on_close_hook:
            self.on_close_hook()

        self.Destroy()

    def go(self):
        pass


class OldEmbroiderySimulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        stitch_plan = kwargs.pop('stitch_plan', None)
        self.x_position = kwargs.pop('x_position', None)
        self.on_close_hook = kwargs.pop('on_close', None)
        self.frame_period = kwargs.pop('frame_period', 80)
        self.stitches_per_frame = kwargs.pop('stitches_per_frame', 1)
        self.target_duration = kwargs.pop('target_duration', None)

        self.margin = 30

        screen_rect = self.get_current_screen_rect()
        self.max_width = kwargs.pop('max_width', screen_rect[2])
        self.max_height = kwargs.pop('max_height', screen_rect[3])
        self.scale = 1

        self.min_width = 600
        if self.max_width < self.min_width:
            self.max_width = self.min_width

        self.load(stitch_plan)

        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.SetBackgroundColour('white')

        self.slider_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.set_slider()

        self.button_sizer = wx.StdDialogButtonSizer()
        self.button_label = (
            # Switch direction button (currently not in use - would this be better?)
            #[_('>>'), _('Switch direction | Play reverse (arrow left) | Play forward (arrow right)'), self.animation_switch_direction],
            [_('<<'), _('Play reverse (arrow left)'), self.animation_reverse],
            [_('-'), _('Play one frame backward (+)'), self.animation_one_frame_back],
            [_('+'), _('Play one frame forward (+)'), self.animation_one_frame_forward],
            [_('>>'), _('Play forward (arrow right)'), self.animation_forward],
            [_('^'), _('Speed up (arrow up)'), self.animation_speed_up],
            [_('v'), _('Slow down (arrow down)'), self.animation_slow_down],
            [_('Pause'), _('Pause (P)'), self.animation_pause],
            [_('Restart'), _('Restart (R)'), self.animation_restart],
            [_('Quit'), _('Close (Q)'), self.animation_quit])

        self.buttons = []
        for i in range(0, len(self.button_label)):
            self.buttons.append(wx.Button(self, -1, self.button_label[i][0]))
            self.button_sizer.Add(self.buttons[i], 1, wx.EXPAND)
            self.buttons[i].SetToolTip(self.button_label[i][1])
            self.buttons[i].Bind(wx.EVT_BUTTON, self.button_label[i][2])

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.sizer.Add(self.slider_sizer, 0, wx.EXPAND)
        self.sizer.Add(self.button_sizer, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.calculate_dimensions()

        if self.target_duration:
            self.adjust_speed(self.target_duration)

        self.buffer = wx.Bitmap(
            self.width * self.scale + self.margin * 2,
            self.height * self.scale + self.margin * 2)
        self.dc = wx.BufferedDC()
        self.dc.SelectObject(self.buffer)
        self.canvas = wx.GraphicsContext.Create(self.dc)

        self.clear()

        self.current_frame = 0
        self.animation_direction = 1
        self.set_stitch_counter(0)

        shortcut_keys = [
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, self.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_RIGHT, self.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, self.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_LEFT, self.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('+'), self.animation_one_frame_forward),
            (wx.ACCEL_NORMAL, ord('='), self.animation_one_frame_forward),
            (wx.ACCEL_SHIFT, ord('='), self.animation_one_frame_forward),
            (wx.ACCEL_NORMAL, wx.WXK_ADD, self.animation_one_frame_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, self.animation_one_frame_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.animation_one_frame_forward),
            (wx.ACCEL_NORMAL, ord('-'), self.animation_one_frame_back),
            (wx.ACCEL_NORMAL, ord('_'), self.animation_one_frame_back),
            (wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, self.animation_one_frame_back),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, self.animation_one_frame_back),
            (wx.ACCEL_NORMAL, ord('r'), self.animation_restart),
            (wx.ACCEL_NORMAL, ord('p'), self.animation_pause),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, self.animation_pause),
            (wx.ACCEL_NORMAL, ord('q'), self.animation_quit)]

        accel_entries = []

        for shortcut_key in shortcut_keys:
            eventId = wx.NewId()
            accel_entries.append((shortcut_key[0], shortcut_key[1], eventId))
            self.Bind(wx.EVT_MENU, shortcut_key[2], id=eventId)

        accel_table = wx.AcceleratorTable(accel_entries)
        self.SetAcceleratorTable(accel_table)

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_SLIDER, self.on_slider)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)

        self.panel.SetFocus()

        self.timer = None

        self.last_pos = None

    def get_current_screen_rect(self):
        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        screen_rect = display.GetClientArea()
        return screen_rect

    def load(self, stitch_plan=None):
        if stitch_plan:
            self.mirror = False
            self.stitch_plan_to_lines(stitch_plan)
            self.move_to_top_left()
            return

    def adjust_speed(self, duration):
        self.frame_period = 1000 * float(duration) / len(self.lines)
        self.stitches_per_frame = 1

        while self.frame_period < 1.0:
            self.frame_period *= 2
            self.stitches_per_frame *= 2

    # Switch direction button (currently not in use - would this be better?)
    def animation_switch_direction(self, event):
        direction_button = event.GetEventObject()
        lbl = direction_button.GetLabel()
        if self.animation_direction == 1:
            self.animation_reverse('backward')
            direction_button.SetLabel('<<')
        else:
            self.animation_forward('forward')
            direction_button.SetLabel('>>')

    def animation_forward(self, event):
        self.animation_direction = 1
        if not self.timer.IsRunning():
            self.timer.StartOnce(self.frame_period)

    def animation_reverse(self, event):
        self.animation_direction = -1
        if not self.timer.IsRunning():
            self.timer.StartOnce(self.frame_period)

    def animation_one_frame_forward(self, event):
        if self.current_frame < len(self.lines):
            self.timer.Stop()
            self.current_frame = self.current_frame + 1
            self.draw_one_frame()
            self.set_stitch_counter(self.current_frame)
            self.set_stitch_slider(self.current_frame)

    def animation_one_frame_back(self, event):
        if self.current_frame > 1:
            self.timer.Stop()
            self.current_frame = self.current_frame - 1
            self.draw_one_frame()
            self.set_stitch_counter(self.current_frame)
            self.set_stitch_slider(self.current_frame)

    def animation_speed_up(self, event):
        if self.stitches_per_frame <= 1280:
            if self.frame_period == 1:
                self.stitches_per_frame *= 2
            else:
                self.frame_period = self.frame_period / 2
        self.animation_update_timer()

    def animation_slow_down(self, event):
        if self.frame_period <= 1280:
            if self.stitches_per_frame == 1:
                self.frame_period *= 2
            else:
                self.stitches_per_frame /= 2
        self.animation_update_timer()

    def animation_restart(self, event):
        self.current_frame = 1
        self.stop()
        self.clear()
        self.go()

    def animation_pause(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.StartOnce(self.frame_period)

    def animation_quit(self, event):
        self.Close()

    def animation_update_timer(self):
        self.frame_period = max(1, self.frame_period)
        self.stitches_per_frame = max(self.stitches_per_frame, 1)
        self.set_stitch_counter(self.current_frame)
        if self.timer.IsRunning():
            self.timer.Stop()
            self.timer.StartOnce(self.frame_period)

    def set_stitch_counter(self, current_frame):
        self.dc.SetTextForeground('red')
        stitch_counter_text = _("Stitch # ") + \
            str(current_frame) + ' / ' + str(len(self.lines))
        self.dc.DrawText(stitch_counter_text, 30, 5)

    def on_slider(self, event):
        self.panel.SetFocus()
        self.draw_one_frame()
        obj = event.GetEventObject()
        self.current_frame = obj.GetValue()
        self.animation_update_timer()

    def set_slider(self):
        self.stitch_slider = wx.Slider(
            self, value=1, minValue=1, maxValue=len(
                self.lines), style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider_sizer.Add(self.stitch_slider, 1, wx.EXPAND)

    def set_stitch_slider(self, val):
        self.stitch_slider.SetValue(val)

    def _strip_quotes(self, string):
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]

        return string

    def color_to_pen(self, color):
        return wx.Pen(color.visible_on_white.rgb)

    def stitch_plan_to_lines(self, stitch_plan):
        self.pens = []
        self.lines = []

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)

            for i, point_list in enumerate(
                    color_block_to_point_lists(color_block)):
                if i == 0:
                    # add the first stitch
                    first_x, first_y = point_list[0]
                    self.lines.append((first_x, first_y, first_x, first_y))
                    self.pens.append(pen)

                # if there's only one point, there's nothing to do, so skip
                if len(point_list) < 2:
                    continue

                for start, end in izip(point_list[:-1], point_list[1:]):
                    line = (start[0], start[1], end[0], end[1])
                    self.lines.append(line)
                    self.pens.append(pen)

    def move_to_top_left(self):
        """remove any unnecessary whitespace around the design"""

        min_x = sys.maxsize
        min_y = sys.maxsize

        for x1, y1, x2, y2 in self.lines:
            min_x = min(min_x, x2)
            min_y = min(min_y, y2)

        new_lines = []

        for line in self.lines:
            (start, end, start1, end1) = line
            new_lines.append(
                (start - min_x,
                 end - min_y,
                 start1 - min_x,
                 end1 - min_y))

        self.lines = new_lines

    def calculate_dimensions(self):
        # 0.01 avoids a division by zero below for designs with no width or
        # height (e.g. a straight vertical or horizontal line)
        width = 0.01
        height = 0.01

        for x1, y1, x2, y2 in self.lines:
            width = max(width, x2)
            height = max(height, y2)

        self.width = width
        self.height = height

        button_width, button_height = self.buttons[0].GetSize()
        slider_width, slider_height = self.stitch_slider.GetSize()
        self.controls_height = button_height + slider_height

        self.scale = min(
            float(
                self.max_width -
                self.margin *
                2) /
            width,
            float(
                self.max_height -
                self.margin *
                2 -
                self.controls_height) /
            height)

        # make room for decorations and the margin
        self.scale *= 0.95

        for i, point in enumerate(self.lines):
            x1, x2, y1, y2 = point
            x1 = x1 * self.scale + self.margin
            y1 = y1 * self.scale + self.margin
            x2 = x2 * self.scale + self.margin
            y2 = y2 * self.scale + self.margin

            self.lines[i] = (x1, x2, y1, y2)

    def go(self):
        self.clear()

        self.current_frame = 0

        if not self.timer:
            self.timer = wx.PyTimer(self.iterate_frames)

        self.timer.StartOnce(self.frame_period)

    def on_close(self, event):
        self.stop()

        if self.on_close_hook:
            self.on_close_hook()

        # If we keep a reference here, wx crashes when the process exits.
        self.canvas = None

        self.Destroy()

    def stop(self):
        if self.timer:
            self.timer.Stop()

    def clear(self):
        self.dc.SetBackground(wx.Brush('white'))
        self.dc.Clear()
        self.last_pos = None
        self.Refresh()

    def on_size(self, e):
        # ensure that the whole canvas is visible
        window_width, window_height = self.GetSize()
        client_width, client_height = self.GetClientSize()

        decorations_width = window_width - client_width
        decorations_height = window_height - client_height

        setsize_window_width = self.width * self.scale + \
            decorations_width + self.margin * 2
        setsize_window_height = self.height * self.scale + \
            decorations_height + self.controls_height + self.margin * 2

        # set minimum width (force space for control buttons)
        if setsize_window_width < self.min_width:
            setsize_window_width = self.min_width

        self.SetSize((setsize_window_width, setsize_window_height))

        # center the simulation on screen if not called by params
        # else center vertically
        if self.x_position is None:
            self.Centre()
        else:
            display_rect = self.get_current_screen_rect()
            self.SetPosition(
                (self.x_position,
                 display_rect[3] /
                 2 -
                 setsize_window_height /
                 2))

        e.Skip()

    def on_paint(self, e):
        dc = wx.AutoBufferedPaintDC(self.panel)
        dc.Blit(
            0,
            0,
            self.buffer.GetWidth(),
            self.buffer.GetHeight(),
            self.dc,
            0,
            0)

        self.last_pos_x, self.last_pos_y, self.last_pos_x1, self.last_pos_y1 = self.lines[0]

        if hasattr(self, 'visible_lines'):
            if len(self.visible_lines) > 0:
                self.last_pos_x1, self.last_pos_y1, self.last_pos_x, self.last_pos_y = self.visible_lines[-1]

        dc.DrawLine(
            self.last_pos_x - 10,
            self.last_pos_y,
            self.last_pos_x + 10,
            self.last_pos_y)
        dc.DrawLine(
            self.last_pos_x,
            self.last_pos_y - 10,
            self.last_pos_x,
            self.last_pos_y + 10)

    def iterate_frames(self):
        self.current_frame += self.stitches_per_frame * self.animation_direction

        if self.current_frame <= len(self.lines) and self.current_frame >= 1:
            # calculate time_to_next_frame
            start = time.time()
            self.draw_one_frame()
            duration = time.time() - start
            duration_ms = int(duration * 1000)
            time_to_next_frame = self.frame_period - duration_ms
            time_to_next_frame = max(1, time_to_next_frame)
            self.timer.StartOnce(time_to_next_frame)
        elif self.current_frame > len(self.lines):
            self.current_frame = len(self.lines)
            self.draw_one_frame()
        elif self.current_frame < 1:
            self.current_frame = 1
            self.draw_one_frame()
        else:
            self.timer.Stop()

        self.set_stitch_counter(self.current_frame)
        self.set_stitch_slider(self.current_frame)

    def draw_one_frame(self):
        self.clear()
        self.visible_lines = self.lines[:self.current_frame]
        self.dc.DrawLineList(self.visible_lines,
                             self.pens[:self.current_frame])
