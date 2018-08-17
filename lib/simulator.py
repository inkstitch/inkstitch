import sys
import numpy
import wx
import colorsys
from itertools import izip

from .svg import PIXELS_PER_MM, color_block_to_point_lists


class EmbroiderySimulator(wx.Frame):
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

        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self, wx.ID_ANY)

        self.panel.SetDoubleBuffered(True)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.button_label = (
            [_("Speed up"), _('Press + or arrow up to speed up'), self.animation_speed_up],
            [_("Slow down"), _('Press - or arrow down to slow down'), self.animation_slow_down],
            [_("Pause"), _("Press P to pause the animation"), self.animation_pause],
            [_("Restart"), _("Press R to restart the animation"), self.animation_restart],
            [_("Quit"), _("Press Q to close the simulation window"), self.animation_quit])
        self.buttons = []
        for i in range(0, len(self.button_label)):
            self.buttons.append(wx.Button(self, -1, self.button_label[i][0]))
            self.button_sizer.Add(self.buttons[i], 1, wx.EXPAND)
            self.buttons[i].SetToolTip(self.button_label[i][1])
            self.buttons[i].Bind(wx.EVT_BUTTON, self.button_label[i][2])

        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.sizer.Add(self.button_sizer, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.load(stitch_plan)

        if self.target_duration:
            self.adjust_speed(self.target_duration)

        self.buffer = wx.Bitmap(self.width * self.scale + self.margin * 2, self.height * self.scale + self.margin * 2)
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.buffer)
        self.canvas = wx.GraphicsContext.Create(self.dc)

        self.clear()

        self.set_stitch_counter(1)

        shortcut_keys = [
            (wx.ACCEL_NORMAL, ord('+'), self.animation_speed_up),
            (wx.ACCEL_NORMAL, ord('='), self.animation_speed_up),
            (wx.ACCEL_SHIFT,  ord('='), self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_ADD, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_UP, self.animation_speed_up),
            (wx.ACCEL_NORMAL, ord('-'), self.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('_'), self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, self.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('r'), self.animation_restart),
            (wx.ACCEL_NORMAL, ord('p'), self.animation_pause),
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
            self.segments = self._stitch_plan_to_segments(stitch_plan)
        else:
            return

        self.trim_margins()
        self.calculate_dimensions()

    def adjust_speed(self, duration):
        self.frame_period = 1000 * float(duration) / len(self.segments)
        self.stitches_per_frame = 1

        while self.frame_period < 1.0:
            self.frame_period *= 2
            self.stitches_per_frame *= 2

    def animation_speed_up(self, event):
        if self.frame_period == 1:
            self.stitches_per_frame *= 2
        else:
            self.frame_period = self.frame_period / 2
        self.animation_update_timer()

    def animation_slow_down(self, event):
        if self.stitches_per_frame == 1:
            self.frame_period *= 2
        else:
            self.stitches_per_frame /= 2
        self.animation_update_timer()

    def animation_restart(self, event):
        self.stop()
        self.clear()
        self.go()

    def animation_pause(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.Start(self.frame_period)

    def animation_quit(self, event):
        self.Close()

    def animation_update_timer(self):
        self.frame_period = max(1, self.frame_period)
        self.stitches_per_frame = max(self.stitches_per_frame, 1)
        if self.timer.IsRunning():
            self.timer.Stop()
            self.timer.Start(self.frame_period)

    def set_stitch_counter(self, current_stitch):
        if hasattr(self.panel, 'stitch_counter'):
            self.panel.stitch_counter.SetLabel(_("Stitch # ") + str(current_stitch) + ' / ' + str(len(self.segments) + 1))
        else:
            self.font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            self.panel.stitch_counter = wx.StaticText(self, label=_("Stitch #") + '1 / ' + str(len(self.segments)), pos=(30, 10))
            self.panel.stitch_counter.SetFont(self.font)
            self.panel.stitch_counter.SetForegroundColour('red')
            self.panel.stitch_counter.SetBackgroundColour('white')

    def _strip_quotes(self, string):
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]

        return string

    def color_to_pen(self, color):
        return wx.Pen(color.visible_on_white.rgb)

    def _stitch_plan_to_segments(self, stitch_plan):
        segments = []

        for color_block in stitch_plan:
            pen = self.color_to_pen(color_block.color)

            for point_list in color_block_to_point_lists(color_block):
                # if there's only one point, there's nothing to do, so skip
                if len(point_list) < 2:
                    continue

                for start, end in izip(point_list[:-1], point_list[1:]):
                    segments.append(((start, end), pen))

        return segments

    def all_coordinates(self):
        for segment in self.segments:
            start, end = segment[0]

            yield start
            yield end

    def trim_margins(self):
        """remove any unnecessary whitespace around the design"""

        min_x = sys.maxint
        min_y = sys.maxint

        for x, y in self.all_coordinates():
            min_x = min(min_x, x)
            min_y = min(min_y, y)

        new_segments = []

        for segment in self.segments:
            (start, end), color = segment

            new_segment = (
                           (
                            (start[0] - min_x, start[1] - min_y),
                            (end[0] - min_x, end[1] - min_y),
                           ),
                           color
                          )

            new_segments.append(new_segment)

        self.segments = new_segments

    def calculate_dimensions(self):
        # 0.01 avoids a division by zero below for designs with no width or
        # height (e.g. a straight vertical or horizontal line)
        width = 0.01
        height = 0.01

        for x, y in self.all_coordinates():
            width = max(width, x)
            height = max(height, y)

        self.width = width
        self.height = height
        self.scale = min(float(self.max_width - self.margin * 2) / width, float(self.max_height - self.margin * 2 - 40) / height)

        # make room for decorations and the margin
        self.scale *= 0.95

    def go(self):
        self.clear()

        self.current_stitch = 0

        if not self.timer:
            self.timer = wx.PyTimer(self.draw_one_frame)

        self.timer.Start(self.frame_period)

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
        decorations_height = window_height - client_height + 40

        setsize_window_width = self.width * self.scale + decorations_width + self.margin * 2
        setsize_window_height = (self.height) * self.scale + decorations_height + self.margin * 2

        # set minimum width (force space for control buttons)
        if setsize_window_width < self.min_width:
            setsize_window_width = self.min_width

        self.SetSize(( setsize_window_width, setsize_window_height))

        # center the simulation on screen if not called by params
        # else center vertically
        if self.x_position == None:
            self.Centre()
        else:
            display_rect = self.get_current_screen_rect()
            self.SetPosition((self.x_position, display_rect[3] / 2 - setsize_window_height / 2))

        e.Skip()

    def on_paint(self, e):
        dc = wx.PaintDC(self.panel)
        dc.Blit(0, 0, self.buffer.GetWidth(), self.buffer.GetHeight(), self.dc, 0, 0)

        if self.last_pos:
            dc.DrawLine(self.last_pos[0] - 10, self.last_pos[1],      self.last_pos[0] + 10, self.last_pos[1])
            dc.DrawLine(self.last_pos[0],      self.last_pos[1] - 10, self.last_pos[0],      self.last_pos[1] + 10)

    def draw_one_frame(self):
        for i in xrange(self.stitches_per_frame):
            try:
                ((x1, y1), (x2, y2)), color = self.segments[self.current_stitch]

                if self.mirror:
                    y1 = self.height - y1
                    y2 = self.height - y2

                x1 = x1 * self.scale + self.margin
                y1 = y1 * self.scale + self.margin
                x2 = x2 * self.scale + self.margin
                y2 = y2 * self.scale + self.margin

                self.canvas.SetPen(color)
                self.canvas.DrawLines(((x1, y1), (x2, y2)))
                self.Refresh()

                self.current_stitch += 1
                self.last_pos = (x2, y2)

                self.set_stitch_counter(self.current_stitch + 1)

            except IndexError:
                self.timer.Stop()
