# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os
import sys
import time
from threading import Event, Thread

import wx
from wx.lib.intctrl import IntCtrl

from lib.debug import debug
from lib.utils import get_resource_dir
from lib.utils.threading import ExitThread
from ..i18n import _
from ..stitch_plan import stitch_plan_from_file
from ..svg import PIXELS_PER_MM

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class ControlPanel(wx.Panel):
    """"""

    @debug.time
    def __init__(self, parent, *args, **kwargs):
        """"""
        self.parent = parent
        self.stitch_plan = kwargs.pop('stitch_plan', None)
        self.detach_callback = kwargs.pop('detach_callback', None)
        self.target_stitches_per_second = kwargs.pop('stitches_per_second')
        self.target_duration = kwargs.pop('target_duration')
        kwargs['style'] = wx.BORDER_SUNKEN
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.drawing_panel = None
        self.num_stitches = 1
        self.current_stitch = 1
        self.speed = 1
        self.direction = 1
        self._last_color_block_end = 0

        self.icons_dir = get_resource_dir("icons")

        # Widgets
        self.button_size = self.GetTextExtent("M").y * 2
        self.button_style = wx.BU_EXACTFIT | wx.BU_NOTEXT
        self.btnMinus = wx.Button(self, -1, style=self.button_style)
        self.btnMinus.Bind(wx.EVT_BUTTON, self.animation_slow_down)
        self.btnMinus.SetBitmap(self.load_icon('slower'))
        self.btnMinus.SetToolTip(_('Slow down (arrow down)'))
        self.btnPlus = wx.Button(self, -1, style=self.button_style)
        self.btnPlus.Bind(wx.EVT_BUTTON, self.animation_speed_up)
        self.btnPlus.SetBitmap(self.load_icon('faster'))
        self.btnPlus.SetToolTip(_('Speed up (arrow up)'))
        self.btnBackwardStitch = wx.Button(self, -1, style=self.button_style)
        self.btnBackwardStitch.Bind(wx.EVT_BUTTON, self.animation_one_stitch_backward)
        self.btnBackwardStitch.SetBitmap(self.load_icon('backward_stitch'))
        self.btnBackwardStitch.SetToolTip(_('Go backward one stitch (-)'))
        self.btnForwardStitch = wx.Button(self, -1, style=self.button_style)
        self.btnForwardStitch.Bind(wx.EVT_BUTTON, self.animation_one_stitch_forward)
        self.btnForwardStitch.SetBitmap(self.load_icon('forward_stitch'))
        self.btnForwardStitch.SetToolTip(_('Go forward one stitch (+)'))
        self.btnBackwardCommand = wx.Button(self, -1, style=self.button_style)
        self.btnBackwardCommand.Bind(wx.EVT_BUTTON, self.animation_one_command_backward)
        self.btnBackwardCommand.SetBitmap(self.load_icon('backward_command'))
        self.btnBackwardCommand.SetToolTip(_('Go backward one command (page-down)'))
        self.btnForwardCommand = wx.Button(self, -1, style=self.button_style)
        self.btnForwardCommand.Bind(wx.EVT_BUTTON, self.animation_one_command_forward)
        self.btnForwardCommand.SetBitmap(self.load_icon('forward_command'))
        self.btnForwardCommand.SetToolTip(_('Go forward one command (page-up)'))
        self.btnForward = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnForward.SetValue(True)
        self.btnForward.Bind(wx.EVT_TOGGLEBUTTON, self.on_forward_button)
        self.btnForward.SetBitmap(self.load_icon('forward'))
        self.btnForward.SetToolTip(_('Animate forward (arrow right)'))
        self.btnReverse = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnReverse.Bind(wx.EVT_TOGGLEBUTTON, self.on_reverse_button)
        self.btnReverse.SetBitmap(self.load_icon('reverse'))
        self.btnReverse.SetToolTip(_('Animate in reverse (arrow left)'))
        self.btnPlay = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnPlay.Bind(wx.EVT_TOGGLEBUTTON, self.on_play_button)
        self.btnPlay.SetBitmap(self.load_icon('play'))
        self.btnPlay.SetToolTip(_('Play (P)'))
        self.btnRestart = wx.Button(self, -1, style=self.button_style)
        self.btnRestart.Bind(wx.EVT_BUTTON, self.animation_restart)
        self.btnRestart.SetBitmap(self.load_icon('restart'))
        self.btnRestart.SetToolTip(_('Restart (R)'))
        self.btnNpp = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnNpp.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_npp)
        self.btnNpp.SetBitmap(self.load_icon('npp'))
        self.btnNpp.SetToolTip(_('Display needle penetration point (O)'))
        self.slider = SimulatorSlider(self, -1, value=1, minValue=1, maxValue=self.stitch_plan.num_stitches)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider)
        self.stitchBox = IntCtrl(self, -1, value=1, min=1, max=self.stitch_plan.num_stitches,
                                 size=((100, -1)), limited=True, allow_none=True, style=wx.TE_PROCESS_ENTER)
        self.stitchBox.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_SET_FOCUS, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_TEXT_ENTER, self.on_stitch_box_focusout)
        self.stitchBox.Bind(wx.EVT_KILL_FOCUS, self.on_stitch_box_focusout)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focusout)
        self.totalstitchText = wx.StaticText(self, -1, label=f"/ { self.stitch_plan.num_stitches }")
        self.btnJump = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnJump.SetToolTip(_('Show jump stitches'))
        self.btnJump.SetBitmap(self.load_icon('jump'))
        self.btnJump.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('jump', event))
        self.btnTrim = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnTrim.SetToolTip(_('Show trims'))
        self.btnTrim.SetBitmap(self.load_icon('trim'))
        self.btnTrim.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('trim', event))
        self.btnStop = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnStop.SetToolTip(_('Show stops'))
        self.btnStop.SetBitmap(self.load_icon('stop'))
        self.btnStop.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('stop', event))
        self.btnColorChange = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnColorChange.SetToolTip(_('Show color changes'))
        self.btnColorChange.SetBitmap(self.load_icon('color_change'))
        self.btnColorChange.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('color_change', event))
        if self.detach_callback:
            self.btnDetachSimulator = wx.BitmapButton(self, -1, style=self.button_style)
            self.btnDetachSimulator.SetToolTip(_('Detach/attach simulator window'))
            self.btnDetachSimulator.SetBitmap(self.load_icon('detach_window'))
            self.btnDetachSimulator.Bind(wx.EVT_BUTTON, lambda event: self.detach_callback())

        # Layout
        self.hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbSizer1.Add(self.slider, 1, wx.EXPAND | wx.RIGHT, 10)
        self.hbSizer1.Add(self.stitchBox, 0, wx.ALIGN_CENTER | wx.RIGHT, 10)
        self.hbSizer1.Add(self.totalstitchText, 0, wx.ALIGN_CENTER | wx.RIGHT, 10)

        self.controls_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Controls")), wx.HORIZONTAL)
        self.controls_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.controls_inner_sizer.Add(self.btnBackwardCommand, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnBackwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnForwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnForwardCommand, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnReverse, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnForward, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnPlay, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnRestart, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_sizer.Add((1, 1), 1)
        self.controls_sizer.Add(self.controls_inner_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.controls_sizer.Add((1, 1), 1)

        self.show_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Show")), wx.HORIZONTAL)
        self.show_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.show_inner_sizer.Add(self.btnNpp, 0, wx.EXPAND | wx.ALL, 2)
        self.show_inner_sizer.Add(self.btnJump, 0, wx.ALL, 2)
        self.show_inner_sizer.Add(self.btnTrim, 0, wx.ALL, 2)
        self.show_inner_sizer.Add(self.btnStop, 0, wx.ALL, 2)
        self.show_inner_sizer.Add(self.btnColorChange, 0, wx.ALL, 2)
        if self.detach_callback:
            self.show_inner_sizer.Add(self.btnDetachSimulator, 0, wx.ALL, 2)
        self.show_sizer.Add((1, 1), 1)
        self.show_sizer.Add(self.show_inner_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.show_sizer.Add((1, 1), 1)

        self.speed_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Speed")), wx.VERTICAL)

        self.speed_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.speed_buttons_sizer.Add((1, 1), 1)
        self.speed_buttons_sizer.Add(self.btnMinus, 0, wx.ALL, 2)
        self.speed_buttons_sizer.Add(self.btnPlus, 0, wx.ALL, 2)
        self.speed_buttons_sizer.Add((1, 1), 1)
        self.speed_sizer.Add(self.speed_buttons_sizer, 0, wx.EXPAND | wx.ALL)
        self.speed_text = wx.StaticText(self, wx.ID_ANY, label="", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        self.speed_text.SetFont(wx.Font(wx.FontInfo(15).Bold()))
        extent = self.speed_text.GetTextExtent(self.format_speed_text(100000))
        self.speed_text.SetMinSize(extent)
        self.speed_sizer.Add(self.speed_text, 0, wx.EXPAND | wx.ALL, 5)

        # A normal BoxSizer can only make child components the same or
        # proportional size.  A FlexGridSizer can split up the available extra
        # space evenly among all growable columns.
        self.control_row2_sizer = wx.FlexGridSizer(cols=3, vgap=0, hgap=5)
        self.control_row2_sizer.AddGrowableCol(0)
        self.control_row2_sizer.AddGrowableCol(1)
        self.control_row2_sizer.AddGrowableCol(2)
        self.control_row2_sizer.Add(self.controls_sizer, 0, wx.EXPAND)
        self.control_row2_sizer.Add(self.speed_sizer, 0, wx.EXPAND)
        self.control_row2_sizer.Add(self.show_sizer, 0, wx.EXPAND)

        self.vbSizer = vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.hbSizer1, 1, wx.EXPAND | wx.ALL, 10)
        vbSizer.Add(self.control_row2_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
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
            (wx.ACCEL_NORMAL, ord('p'), self.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, self.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEDOWN, self.animation_one_command_backward),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEUP, self.animation_one_command_forward),

        ]

        self.accel_entries = []

        for shortcut_key in shortcut_keys:
            eventId = wx.NewIdRef()
            self.accel_entries.append((shortcut_key[0], shortcut_key[1], eventId))
            self.Bind(wx.EVT_MENU, shortcut_key[2], id=eventId)

        self.accel_table = wx.AcceleratorTable(self.accel_entries)
        self.SetAcceleratorTable(self.accel_table)
        self.SetFocus()

        # wait for layouts so that panel size is set
        if self.stitch_plan:
            wx.CallLater(50, self.load, self.stitch_plan)

    def set_drawing_panel(self, drawing_panel):
        self.drawing_panel = drawing_panel
        self.drawing_panel.set_speed(self.speed)

    def _set_num_stitches(self, num_stitches):
        if num_stitches < 2:
            # otherwise the slider and intctrl get mad
            num_stitches = 2
        self.num_stitches = num_stitches
        self.stitchBox.SetMax(num_stitches)
        self.slider.SetMax(num_stitches)
        self.choose_speed()

    def add_color(self, color, num_stitches):
        start = self._last_color_block_end + 1
        self.slider.add_color_section(ColorSection(color.rgb, start, start + num_stitches - 1))
        self._last_color_block_end = self._last_color_block_end + num_stitches

    def load(self, stitch_plan):
        self.stitches = []
        self._set_num_stitches(stitch_plan.num_stitches)

        stitch_num = 0
        for color_block in stitch_plan.color_blocks:
            self.stitches.extend(color_block.stitches)

            start = stitch_num + 1
            end = start + color_block.num_stitches
            self.slider.add_color_section(color_block.color.rgb, start, end)

            for stitch_num, stitch in enumerate(color_block.stitches, start):
                if stitch.trim:
                    self.slider.add_marker("trim", stitch_num)
                elif stitch.stop:
                    self.slider.add_marker("stop", stitch_num)
                elif stitch.jump:
                    self.slider.add_marker("jump", stitch_num)
                elif stitch.color_change:
                    self.slider.add_marker("color_change", stitch_num)

    def load_icon(self, icon_name):
        icon = wx.Image(os.path.join(self.icons_dir, f"{icon_name}.png"))
        icon.Rescale(self.button_size, self.button_size, wx.IMAGE_QUALITY_HIGH)
        return icon.ConvertToBitmap()

    def on_marker_button(self, marker_type, event):
        self.slider.enable_marker_list(marker_type, event.GetEventObject().GetValue())

    def choose_speed(self):
        if self.target_duration:
            self.set_speed(int(self.num_stitches / float(self.target_duration)))
        else:
            self.set_speed(self.target_stitches_per_second)

    def animation_forward(self, event=None):
        self.btnForward.SetValue(True)
        self.btnReverse.SetValue(False)
        self.drawing_panel.forward()
        self.direction = 1
        self.update_speed_text()

    def animation_reverse(self, event=None):
        self.btnForward.SetValue(False)
        self.btnReverse.SetValue(True)
        self.drawing_panel.reverse()
        self.direction = -1
        self.update_speed_text()

    def on_forward_button(self, event):
        self.animation_forward()

    def on_reverse_button(self, event):
        self.animation_reverse()

    def set_speed(self, speed):
        self.speed = int(max(speed, 1))
        self.update_speed_text()

        if self.drawing_panel:
            self.drawing_panel.set_speed(self.speed)

    def format_speed_text(self, speed):
        return _('%d stitches/sec') % speed

    def update_speed_text(self):
        self.speed_text.SetLabel(self.format_speed_text(self.speed * self.direction))

    def on_slider(self, event):
        self.animation_pause()
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

    def on_stitch_box_focus(self, event):
        self.animation_pause()
        self.SetAcceleratorTable(wx.AcceleratorTable([]))
        event.Skip()

    def on_stitch_box_focusout(self, event):
        self.SetAcceleratorTable(self.accel_table)
        stitch = self.stitchBox.GetValue()
        # We now want to remove the focus from the stitchBox.
        # In Windows it won't work if we set focus to self.parent, while setting the focus to the
        # top level would work. This in turn would activate the trim button in Linux. So let's
        # set the focus on the slider instead where it doesn't cause any harm in any of the operating systems
        self.slider.SetFocus()

        if stitch is None:
            stitch = 1
            self.stitchBox.SetValue(1)

        self.slider.SetValue(stitch)

        if self.drawing_panel:
            self.drawing_panel.set_current_stitch(stitch)
        event.Skip()

    def animation_slow_down(self, event):
        """"""
        self.set_speed(self.speed / 2.0)

    def animation_speed_up(self, event):
        """"""
        self.set_speed(self.speed * 2.0)

    def animation_pause(self, event=None):
        self.drawing_panel.stop()
        self.btnPlay.SetBitmap(self.load_icon('play'))

    def animation_start(self, event=None):
        self.drawing_panel.go()
        self.btnPlay.SetBitmap(self.load_icon('pause'))

    def on_start(self):
        self.btnPlay.SetValue(True)
        self.btnPlay.SetBitmap(self.load_icon('pause'))

    def on_stop(self):
        self.btnPlay.SetValue(False)
        self.btnPlay.SetBitmap(self.load_icon('play'))

    def on_play_button(self, event):
        play = self.btnPlay.GetValue()
        if play:
            self.animation_start()
        else:
            self.animation_pause()

    def play_or_pause(self, event):
        if self.drawing_panel.animating:
            self.animation_pause()
        else:
            self.animation_start()

    def animation_one_stitch_forward(self, event):
        self.animation_pause()
        self.drawing_panel.one_stitch_forward()

    def animation_one_stitch_backward(self, event):
        self.animation_pause()
        self.drawing_panel.one_stitch_backward()

    def animation_one_command_backward(self, event):
        self.animation_pause()
        stitch_number = self.current_stitch - 1
        while stitch_number >= 1:
            # stitch number shown to the user starts at 1
            stitch = self.stitches[stitch_number - 1]
            if stitch.jump or stitch.trim or stitch.stop or stitch.color_change:
                break
            stitch_number -= 1
        self.drawing_panel.set_current_stitch(stitch_number)

    def animation_one_command_forward(self, event):
        self.animation_pause()
        stitch_number = self.current_stitch + 1
        while stitch_number <= self.num_stitches:
            # stitch number shown to the user starts at 1
            stitch = self.stitches[stitch_number - 1]
            if stitch.jump or stitch.trim or stitch.stop or stitch.color_change:
                break
            stitch_number += 1
        self.drawing_panel.set_current_stitch(stitch_number)

    def animation_restart(self, event):
        self.drawing_panel.restart()

    def on_toggle_npp_shortcut(self, event):
        self.btnNpp.SetValue(not self.btnNpp.GetValue())
        self.toggle_npp(event)

    def toggle_npp(self, event):
        self.drawing_panel.Refresh()


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
        self.stitch_plan = kwargs.pop('stitch_plan', None)
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

        self.SetMinSize((400, 400))

        # wait for layouts so that panel size is set
        if self.stitch_plan:
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
        dc = wx.PaintDC(self)

        if not self.loaded:
            dc.Clear()
            return

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
                    canvas.StrokeLines(stitches)
                    self.draw_needle_penetration_points(canvas, pen, stitches)
                last_stitch = stitches[-1]
            else:
                stitches = stitches[:self.current_stitch - stitch]
                if len(stitches) > 1:
                    canvas.StrokeLines(stitches)
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
        canvas.StrokeLines(((x - crosshair_radius, y), (x + crosshair_radius, y)))
        canvas.StrokeLines(((x, y - crosshair_radius), (x, y + crosshair_radius)))

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

        scale_width_mm = int(scale_width / self.zoom / PIXELS_PER_MM)

        # The scale bar looks like this:
        #
        # |           |
        # |_____|_____|

        scale_lower_left_x = 20
        scale_lower_left_y = canvas_height - 30

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

    def draw_needle_penetration_points(self, canvas, pen, stitches):
        if self.control_panel.btnNpp.GetValue():
            npp_pen = wx.Pen(pen.GetColour(), width=int(0.5 * PIXELS_PER_MM * self.PIXEL_DENSITY))
            canvas.SetPen(npp_pen)
            canvas.StrokeLineSegments(stitches, [(stitch[0] + 0.001, stitch[1]) for stitch in stitches])

    def clear(self):
        self.loaded = False
        self.Refresh()

    def load(self, stitch_plan):
        self.current_stitch = 1
        self.direction = 1
        self.last_frame_duration = 0
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.num_stitches = stitch_plan.num_stitches
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
        command = self.commands[self.current_stitch]
        self.control_panel.on_current_stitch(self.current_stitch, command)
        statusbar = self.GetTopLevelParent().statusbar
        statusbar.SetStatusText(_("Command: %s") % COMMAND_NAMES[command])
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


class MarkerList(list):
    def __init__(self, icon_name, stitch_numbers=()):
        super().__init__(self)
        icons_dir = get_resource_dir("icons")
        self.icon_name = icon_name
        self.icon = wx.Image(os.path.join(icons_dir, f"{icon_name}.png")).ConvertToBitmap()
        self.enabled = False
        self.extend(stitch_numbers)

    def __repr__(self):
        return f"MarkerList({self.icon_name})"


class ColorSection:
    def __init__(self, color, start, end):
        self.color = color
        self.start = start
        self.end = end
        self.brush = wx.Brush(wx.Colour(*color))


class SimulatorSlider(wx.Panel):
    PROXY_EVENTS = (wx.EVT_SLIDER,)

    def __init__(self, parent, id=wx.ID_ANY, minValue=0, maxValue=1, **kwargs):
        super().__init__(parent, id)

        kwargs['style'] = wx.SL_HORIZONTAL | wx.SL_VALUE_LABEL | wx.SL_TOP | wx.ALIGN_TOP

        self._height = self.GetTextExtent("M").y * 4
        self.SetMinSize((self._height, self._height))

        self.marker_lists = {
            "trim": MarkerList("trim"),
            "stop": MarkerList("stop"),
            "jump": MarkerList("jump"),
            "color_change": MarkerList("color_change"),
        }
        self.marker_pen = wx.Pen(wx.Colour(0, 0, 0))
        self.color_sections = []
        self.margin = 15
        self.tab_start = 0
        self.tab_width = 0.2
        self.tab_height = 0.2
        self.color_bar_start = 0.3
        self.color_bar_thickness = 0.25
        self.marker_start = self.color_bar_start
        self.marker_end = 0.75
        self.marker_icon_start = 0.75
        self.marker_icon_size = self._height // 4

        self._min = minValue
        self._max = maxValue
        self._value = 0
        self._tab_rect = None

        if sys.platform == "darwin":
            self.margin = 8

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)

    def SetMax(self, value):
        self._max = value
        self.Refresh()

    def SetMin(self, value):
        self._min = value
        self.Refresh()

    def SetValue(self, value):
        self._value = value
        self.Refresh()

    def GetValue(self):
        return self._value

    def add_color_section(self, color, start, end):
        self.color_sections.append(ColorSection(color, start, end))

    def add_marker(self, name, location):
        self.marker_lists[name].append(location)
        self.Refresh()

    def enable_marker_list(self, name, enabled=True):
        self.marker_lists[name].enabled = enabled
        self.Refresh()

    def disable_marker_list(self, name):
        self.marker_lists[name].enabled = False
        self.Refresh()

    def toggle_marker_list(self, name):
        self.marker_lists[name].enabled = not self.marker_lists[name].enabled
        self.Refresh()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        if not sys.platform.startswith("win"):
            # Without this, the background color will be white.
            background_brush = wx.Brush(self.GetTopLevelParent().GetBackgroundColour(), wx.SOLID)
            dc.SetBackground(background_brush)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        width, height = self.GetSize()
        min_value = self._min
        max_value = self._max
        spread = max_value - min_value

        def _value_to_x(value):
            return (value - min_value) * (width - 2 * self.margin) / spread + self.margin

        gc.SetPen(wx.NullPen)
        for color_section in self.color_sections:
            gc.SetBrush(color_section.brush)

            start_x = _value_to_x(color_section.start)
            end_x = _value_to_x(color_section.end)
            gc.DrawRectangle(start_x, height * self.color_bar_start,
                             end_x - start_x, height * self.color_bar_thickness)

        gc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 1))
        gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

        value_x = _value_to_x(self._value)
        tab_height = self.tab_height * height
        tab_width = self.tab_width * height
        tab_x = value_x - tab_width / 2
        tab_y = height * self.tab_start
        self._tab_rect = wx.Rect(round(tab_x), round(tab_y), round(tab_width), round(tab_height))
        gc.DrawRectangle(
            value_x - 1.5, 0,
            3, height * (self.color_bar_start + self.color_bar_thickness))
        gc.SetPen(wx.NullPen)
        gc.DrawRectangle(value_x - tab_width/2, height * self.tab_start,
                         tab_width, tab_height)

        gc.SetPen(self.marker_pen)
        for marker_list in self.marker_lists.values():
            if marker_list.enabled:
                for value in marker_list:
                    x = _value_to_x(value)
                    gc.StrokeLine(
                        x, height * self.marker_start,
                        x, height * self.marker_end
                    )
                    gc.DrawBitmap(
                        marker_list.icon,
                        x - self.marker_icon_size / 2, height * self.marker_icon_start,
                        self.marker_icon_size, self.marker_icon_size
                    )

    def on_erase_background(self, event):
        # supposedly this prevents flickering?
        pass

    def is_in_tab(self, point):
        return self._tab_rect and self._tab_rect.Inflate(2).Contains(point)

    def set_value_from_position(self, point):
        width, height = self.GetSize()
        min_value = self._min
        max_value = self._max
        spread = max_value - min_value
        value = round((point.x - self.margin) * spread / (width - 2 * self.margin))
        value = max(value, self._min)
        value = min(value, self._max)
        self.SetValue(round(value))

        event = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, self.GetId())
        event.SetInt(value)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def on_mouse_down(self, event):
        click_pos = event.GetPosition()
        if self.is_in_tab(click_pos):
            debug.log("drag start")
            self.CaptureMouse()
            self.set_value_from_position(click_pos)
            self.Refresh()
        else:
            width, height = self.GetSize()
            relative_y = click_pos.y / height
            if relative_y > self.color_bar_start and relative_y - self.color_bar_start < self.color_bar_thickness:
                self.set_value_from_position(click_pos)
                self.Refresh()

    def on_mouse_motion(self, event):
        if self.HasCapture() and event.Dragging() and event.LeftIsDown():
            self.set_value_from_position(event.GetPosition())
            self.Refresh()

    def on_mouse_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
            self.set_value_from_position(event.GetPosition())
            self.Refresh()


class SimulatorPanel(wx.Panel):
    """"""

    def __init__(self, parent, stitch_plan=None, target_duration=5, stitches_per_second=16, detach_callback=None):
        """"""
        super().__init__(parent, style=wx.BORDER_SUNKEN)

        self.cp = ControlPanel(self,
                               stitch_plan=stitch_plan,
                               stitches_per_second=stitches_per_second,
                               target_duration=target_duration,
                               detach_callback=detach_callback)
        self.dp = DrawingPanel(self, stitch_plan=stitch_plan, control_panel=self.cp)
        self.cp.set_drawing_panel(self.dp)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(self.cp, 0, wx.EXPAND | wx.ALL, 2)
        self.SetSizerAndFit(vbSizer)

    def go(self):
        self.dp.go()

    def stop(self):
        self.dp.stop()

    def load(self, stitch_plan):
        self.dp.load(stitch_plan)
        self.cp.load(stitch_plan)

    def clear(self):
        self.dp.clear()


class EmbroiderySimulator(wx.Panel):
    def __init__(self, parent, stitch_plan=None, stitches_per_second=16, target_duration=None):
        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.simulator_panel = SimulatorPanel(self,
                                              stitch_plan=stitch_plan,
                                              target_duration=target_duration,
                                              stitches_per_second=stitches_per_second)
        sizer.Add(self.simulator_panel, 1, wx.EXPAND)

        self.SetSizerAndFit(sizer)

    def quit(self):
        self.simulator_panel.stop()

    def go(self):
        self.simulator_panel.go()

    def stop(self):
        self.simulator_panel.stop()

    def load(self, stitch_plan):
        self.simulator_panel.load(stitch_plan)

    def clear(self):
        self.simulator_panel.clear()


class SimulatorWindow(wx.Frame):
    def __init__(self, panel=None, parent=None):
        super().__init__(None, title="Simulator")

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        if panel and parent:
            self.is_child = True
            self.panel = panel
            self.parent = parent
            self.panel.Reparent(self)
            self.sizer.Add(self.panel, 1, wx.EXPAND)
            self.panel.Show()
        else:
            self.is_child = False
            self.simulator_panel = SimulatorPanel(self)
            self.sizer.Add(self.simulator_panel, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Layout()
        self.SetSizeHints(self.sizer.CalcMin())

        if self.is_child:
            self.Bind(wx.EVT_CLOSE, self.on_close)

    def detach_simulator_panel(self):
        self.sizer.Detach(self.panel)

    def on_close(self, event):
        self.parent.attach_simulator()


class PreviewRenderer(Thread):
    """Render stitch plan in a background thread."""

    def __init__(self, render_stitch_plan_hook, rendering_completed_hook):
        super(PreviewRenderer, self).__init__()
        self.daemon = True
        self.refresh_needed = Event()

        self.render_stitch_plan_hook = render_stitch_plan_hook
        self.rendering_completed_hook = rendering_completed_hook

        # This is read by utils.threading.check_stop_flag() to abort stitch plan
        # generation.
        self.stop = Event()

    def update(self):
        """Request to render a new stitch plan.

        self.render_stitch_plan_hook() will be called in a background thread, and then
        self.rendering_completed_hook() will be called with the resulting stitch plan.
        """

        if not self.is_alive():
            self.start()

        self.stop.set()
        self.refresh_needed.set()

    def run(self):
        while True:
            self.refresh_needed.wait()
            self.refresh_needed.clear()
            self.stop.clear()

            try:
                debug.log("update_patches")
                self.render_stitch_plan()
            except ExitThread:
                debug.log("ExitThread caught")
                self.stop.clear()

    def render_stitch_plan(self):
        try:
            stitch_plan = self.render_stitch_plan_hook()
            if stitch_plan:
                # rendering_completed() will be called in the main thread.
                wx.CallAfter(self.rendering_completed_hook, stitch_plan)
        except ExitThread:
            raise
        except:  # noqa: E722
            import traceback
            debug.log("unhandled exception in PreviewRenderer.render_stitch_plan(): " + traceback.format_exc())


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
