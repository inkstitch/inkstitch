# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx

from ...i18n import _
from . import SimulatorPanel


class SimulatorWindow(wx.Frame):
    def __init__(self, panel=None, parent=None, **kwargs):
        background_color = kwargs.pop('background_color', 'white')
        super().__init__(None, title=_("Embroidery Simulation"), **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.statusbar = self.CreateStatusBar(3)
        self.statusbar.SetStatusWidths((0, -1, -1))

        if panel and parent:
            self.is_child = True
            self.panel = panel
            self.parent = parent
            self.panel.Reparent(self)
            self.sizer.Add(self.panel, 1, wx.EXPAND)
            self.panel.Show()
        else:
            self.is_child = False
            self.panel = SimulatorPanel(self, background_color=background_color)
            self.sizer.Add(self.panel, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Layout()

        self.SetMinSize(self.sizer.CalcMin())

        if self.is_child:
            self.Bind(wx.EVT_CLOSE, self.on_close)
        else:
            self.Maximize()

    def detach_simulator_panel(self):
        self.sizer.Detach(self.panel)

    def on_close(self, event):
        self.parent.attach_simulator()

    def load(self, stitch_plan):
        self.panel.load(stitch_plan)

    def go(self):
        self.panel.go()

    def set_page_specs(self, page_specs):
        self.panel.set_page_specs(page_specs)
