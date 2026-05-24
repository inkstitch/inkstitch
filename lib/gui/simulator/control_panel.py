# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os
from sys import platform

import wx
from wx.lib.intctrl import IntCtrl

from ...debug.debug import debug
from ...i18n import _
from ...utils import get_resource_dir
from ...utils.settings import global_settings
from . import SimulatorSlider


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
        self.num_stitches = 0
        self.current_stitch = 0
        self.speed = global_settings['simulator_speed']
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
        self.btnDirection = wx.Button(self, -1, style=self.button_style)
        self.btnDirection.Bind(wx.EVT_BUTTON, self.on_direction_button)
        self.btnDirection.SetBitmap(self.load_icon('direction'))
        self.btnDirection.SetToolTip(_('Switch animation direction (arrow left, arrow right)'))
        self.btnPlay = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnPlay.Bind(wx.EVT_TOGGLEBUTTON, self.on_play_button)
        self.btnPlay.SetBitmap(self.load_icon('play'))
        self.btnPlay.SetToolTip(_('Play (P)'))
        self.btnRestart = wx.Button(self, -1, style=self.button_style)
        self.btnRestart.Bind(wx.EVT_BUTTON, self.animation_restart)
        self.btnRestart.SetBitmap(self.load_icon('restart'))
        self.btnRestart.SetToolTip(_('Restart (R)'))
        self.slider = SimulatorSlider(self, -1, value=1, minValue=1, maxValue=2)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider)
        self.stitchBox = IntCtrl(self, -1, value=1, min=1, max=2, limited=True, allow_none=True,
                                 size=((100, -1)), style=wx.TE_PROCESS_ENTER)
        self.stitchBox.Clear()
        self.stitchBox.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_SET_FOCUS, self.on_stitch_box_focus)
        self.stitchBox.Bind(wx.EVT_TEXT_ENTER, self.on_stitch_box_focusout)
        self.stitchBox.Bind(wx.EVT_KILL_FOCUS, self.on_stitch_box_focusout)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_stitch_box_focusout)
        self.totalstitchText = wx.StaticText(self, -1, label="")
        extent = self.totalstitchText.GetTextExtent("0000000")
        self.totalstitchText.SetMinSize(extent)

        # Layout
        self.hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbSizer1.Add(self.slider, 1, wx.EXPAND | wx.RIGHT, 10)
        self.hbSizer1.Add(self.stitchBox, 0, wx.ALIGN_TOP | wx.TOP, 25)
        self.hbSizer1.Add((1, 1), 0, wx.RIGHT, 10)
        self.hbSizer1.Add(self.totalstitchText, 0, wx.ALIGN_TOP | wx.TOP, 25)
        self.hbSizer1.Add((1, 1), 0, wx.RIGHT, 10)

        self.controls_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Controls")), wx.HORIZONTAL)
        self.controls_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.controls_inner_sizer.Add(self.btnBackwardCommand, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnBackwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnForwardStitch, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnForwardCommand, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnDirection, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnPlay, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_inner_sizer.Add(self.btnRestart, 0, wx.EXPAND | wx.ALL, 2)
        self.controls_sizer.Add((1, 1), 1)
        self.controls_sizer.Add(self.controls_inner_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.controls_sizer.Add((1, 1), 1)

        self.speed_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Speed")), wx.VERTICAL)

        self.speed_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.speed_buttons_sizer.Add((1, 1), 1)
        self.speed_buttons_sizer.Add(self.btnMinus, 0, wx.ALL, 2)
        self.speed_buttons_sizer.Add(self.btnPlus, 0, wx.ALL, 2)
        self.speed_buttons_sizer.Add((1, 1), 1)
        self.speed_sizer.Add(self.speed_buttons_sizer, 0, wx.EXPAND | wx.ALL)
        self.speed_text = wx.StaticText(self, wx.ID_ANY, label="", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        self.speed_text.SetFont(wx.Font(wx.FontInfo(10).Bold()))
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

        self.vbSizer = vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.hbSizer1, 1, wx.EXPAND | wx.ALL, 10)
        vbSizer.Add(self.control_row2_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizerAndFit(vbSizer)

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
        self.stitchBox.SetValue(1)
        self.stitchBox.SetMax(num_stitches)
        self.slider.SetMax(num_stitches)
        self.totalstitchText.SetLabel(f"/ { num_stitches }")
        self.choose_speed()

    def clear(self):
        self.stitches = []
        self._set_num_stitches(0)
        self.slider.clear()
        self.stitchBox.Clear()
        self.totalstitchText.SetLabel("")

    def load(self, stitch_plan):
        self.clear()
        self.stitches = []
        self._set_num_stitches(stitch_plan.num_stitches)

        stitch_num = 0
        last_block_end = 1
        for color_block in stitch_plan.color_blocks:
            self.stitches.extend(color_block.stitches)

            start = stitch_num + 1
            end = start + color_block.num_stitches - 1
            self.slider.add_color_section(color_block.color.rgb, last_block_end, end)
            last_block_end = end

            for stitch_num, stitch in enumerate(color_block.stitches, start):
                if stitch.trim:
                    self.slider.add_marker("trim", stitch_num)
                elif stitch.stop:
                    self.slider.add_marker("stop", stitch_num)
                elif stitch.jump:
                    self.slider.add_marker("jump", stitch_num)
                elif stitch.color_change:
                    self.slider.add_marker("color_change", stitch_num)

    def is_dark_theme(self):
        return wx.SystemSettings().GetAppearance().IsDark()

    def load_icon(self, icon_name):
        if self.is_dark_theme() and platform != "win32":
            icon = wx.Image(os.path.join(self.icons_dir, f"{icon_name}_dark.png"))
        else:
            icon = wx.Image(os.path.join(self.icons_dir, f"{icon_name}.png"))
        icon.Rescale(self.button_size, self.button_size, wx.IMAGE_QUALITY_HIGH)
        return icon.ConvertToBitmap()

    def choose_speed(self):
        if not global_settings['simulator_adaptive_speed']:
            self.set_speed(global_settings['simulator_speed'])
            return
        if self.target_duration:
            stitches_per_second = round(self.num_stitches / float(self.target_duration))
            if stitches_per_second < 10:
                # otherwise it just looks weirdly slow
                stitches_per_second = 10
            self.set_speed(stitches_per_second)
        else:
            self.set_speed(self.target_stitches_per_second)

    def animation_forward(self, event=None):
        self.drawing_panel.forward()
        self.direction = 1
        self.update_speed_text()

    def animation_reverse(self, event=None):
        self.drawing_panel.reverse()
        self.direction = -1
        self.update_speed_text()

    def on_direction_button(self, event):
        if self.direction == -1:
            self.animation_forward()
        else:
            self.animation_reverse()

    def set_speed(self, speed):
        global_settings['simulator_speed'] = speed
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
            stitch = min(self.stitchBox.GetMax(), stitch)
            self.stitchBox.SetValue(stitch)

    def on_stitch_box_focus(self, event):
        self.animation_pause()
        self.parent.SetAcceleratorTable(wx.AcceleratorTable([]))
        event.Skip()

    def on_stitch_box_focusout(self, event):
        self.parent.SetAcceleratorTable(self.parent.accel_table)
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

    def animation_start(self, event=None):
        self.drawing_panel.go()

    def on_start(self):
        self.btnPlay.SetValue(True)

    def on_stop(self):
        self.btnPlay.SetValue(False)

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
