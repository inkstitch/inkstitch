# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx

from . import ControlPanel, DrawingPanel, ViewPanel


class SimulatorPanel(wx.Panel):
    """"""

    def __init__(self, parent, stitch_plan=None, background_color='white', target_duration=5, stitches_per_second=16, detach_callback=None):
        """"""
        super().__init__(parent, style=wx.BORDER_SUNKEN)

        self.cp = ControlPanel(
            self,
            stitch_plan=stitch_plan,
            stitches_per_second=stitches_per_second,
            target_duration=target_duration,
            detach_callback=detach_callback
        )

        self.vp = ViewPanel(
            self,
            detach_callback
        )
        self.dp = DrawingPanel(self, stitch_plan=stitch_plan)
        self.cp.set_drawing_panel(self.dp)
        self.vp.set_drawing_panel(self.dp)
        self.vp.set_background_color(wx.Colour(background_color))
        self.dp.set_background_color(wx.Colour(background_color))

        dvSizer = wx.BoxSizer(wx.HORIZONTAL)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(self.cp, 0, wx.EXPAND | wx.ALL, 2)

        dvSizer.Add(vbSizer, 1, wx.EXPAND | wx.ALL, 2)
        dvSizer.Add(self.vp, 0, wx.ALL, 2)

        self.SetSizerAndFit(dvSizer)

        # Keyboard Shortcuts
        shortcut_keys = [
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, self.cp.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_RIGHT, self.cp.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, self.cp.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_LEFT, self.cp.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_UP, self.cp.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.cp.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, self.cp.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DOWN, self.cp.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('+'), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('='), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_SHIFT, ord('='), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_ADD, self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('-'), self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('_'), self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('r'), self.cp.animation_restart),
            (wx.ACCEL_NORMAL, ord('p'), self.cp.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, self.cp.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEDOWN, self.cp.animation_one_command_backward),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEUP, self.cp.animation_one_command_forward),
            (wx.ACCEL_NORMAL, ord('o'), self.vp.on_toggle_npp_shortcut)
        ]

        self.accel_entries = []

        for shortcut_key in shortcut_keys:
            eventId = wx.NewIdRef()
            self.accel_entries.append((shortcut_key[0], shortcut_key[1], eventId))
            self.Bind(wx.EVT_MENU, shortcut_key[2], id=eventId)

        self.accel_table = wx.AcceleratorTable(self.accel_entries)
        self.SetAcceleratorTable(self.accel_table)

    def go(self):
        self.dp.go()

    def stop(self):
        self.dp.stop()

    def load(self, stitch_plan):
        self.dp.load(stitch_plan)
        self.cp.load(stitch_plan)

    def clear(self):
        self.dp.clear()
        self.cp.clear()

    def set_page_specs(self, page_specs):
        self.dp.set_page_specs(page_specs)
