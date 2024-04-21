# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ..gui.simulator import SimulatorWindow
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..utils.svg_data import get_pagecolor
from .base import InkstitchExtension


class Simulator(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        if not self.get_elements():
            return

        metadata = self.get_inkstitch_metadata()
        collapse_len = metadata['collapse_len_mm']
        min_stitch_len = metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)
        background_color = get_pagecolor(self.svg.namedview)

        app = wx.App()
        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        screen_rect = display.GetClientArea()
        height = int(screen_rect[3] * 0.8)
        simulator = SimulatorWindow(size=(0, height), background_color=background_color)
        wx.CallLater(100, simulator.Centre)
        app.SetTopWindow(simulator)
        simulator.Show()
        simulator.load(stitch_plan)
        simulator.go()
        app.MainLoop()
