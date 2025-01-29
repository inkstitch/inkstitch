# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os

import wx

from ...debug.debug import debug
from ...utils import get_resource_dir
from ...utils.settings import global_settings
from . import SimulatorPanel, SimulatorWindow


class SplitSimulatorWindow(wx.Frame):
    def __init__(self, panel_class, title, target_duration=None, **kwargs):
        super().__init__(None, title=title)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.statusbar = self.CreateStatusBar(3)

        self.detached_simulator_frame = None
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        background_color = kwargs.pop('background_color', 'white')
        self.cancel_hook = kwargs.pop('on_cancel', None)
        self.simulator_panel = SimulatorPanel(
            self.splitter,
            background_color=background_color,
            target_duration=target_duration,
            detach_callback=self.toggle_detach_simulator
        )
        self.settings_panel = panel_class(self.splitter, simulator=self.simulator_panel, **kwargs)

        self.splitter.SplitVertically(self.settings_panel, self.simulator_panel)
        self.splitter.SetMinimumPaneSize(100)

        icon = wx.Icon(os.path.join(get_resource_dir("icons"), "inkstitch256x256.png"))
        self.SetIcon(icon)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.SetMinSize(self.sizer.CalcMin())

        self.simulator_panel.SetFocus()
        self.Maximize()
        self.Show()
        wx.CallLater(100, self.set_sash_position)

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.splitter_resize)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        if global_settings['pop_out_simulator']:
            self.detach_simulator()

    def splitter_resize(self, event):
        self.statusbar.SetStatusWidths((self.simulator_panel.GetScreenPosition()[0], -1, -1))

    def set_sash_position(self):
        settings_panel_min_size = self.settings_panel.GetSizer().CalcMin()
        debug.log(f"{settings_panel_min_size=}")
        self.splitter.SetSashPosition(settings_panel_min_size.width)
        self.statusbar.SetStatusWidths((settings_panel_min_size.width, -1, -1))

    def cancel(self, event=None):
        if self.cancel_hook:
            self.cancel_hook()
        try:
            if not self.settings_panel.confirm_close():
                event.Veto()
                return
        except AttributeError:
            pass

        self.close(None)

    def close(self, event=None):
        self.simulator_panel.stop()
        if self.detached_simulator_frame:
            self.detached_simulator_frame.Destroy()
        self.Destroy()

    def toggle_detach_simulator(self):
        if self.detached_simulator_frame:
            self.attach_simulator()
        else:
            self.detach_simulator()

    def attach_simulator(self):
        self.detached_simulator_frame.detach_simulator_panel()
        self.simulator_panel.Reparent(self.splitter)
        self.splitter.SplitVertically(self.settings_panel, self.simulator_panel)

        self.GetStatusBar().SetStatusText(self.detached_simulator_frame.GetStatusBar().GetStatusText(1), 2)

        self.detached_simulator_frame.Destroy()
        self.detached_simulator_frame = None
        self.Maximize()
        self.splitter.UpdateSize()
        self.simulator_panel.SetFocus()
        self.Raise()
        wx.CallLater(100, self.set_sash_position)
        global_settings['pop_out_simulator'] = False

    def detach_simulator(self):
        self.splitter.Unsplit()
        self.detached_simulator_frame = SimulatorWindow(panel=self.simulator_panel, parent=self)
        self.splitter.SetMinimumPaneSize(100)

        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        screen_rect = display.GetClientArea()
        settings_panel_size = self.settings_panel.GetSizer().CalcMin()
        self.SetMinSize(settings_panel_size)
        self.Maximize(False)
        self.SetSize((settings_panel_size.width, screen_rect.height))
        self.SetPosition((screen_rect.left, screen_rect.top))

        self.detached_simulator_frame.SetSize((screen_rect.width - settings_panel_size.width, screen_rect.height))
        self.detached_simulator_frame.SetPosition((settings_panel_size.width, screen_rect.top))

        self.detached_simulator_frame.GetStatusBar().SetStatusText(self.GetStatusBar().GetStatusText(1), 2)
        self.GetStatusBar().SetStatusText("", 1)

        self.detached_simulator_frame.Show()

        global_settings['pop_out_simulator'] = True
