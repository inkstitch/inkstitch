# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from .base import InkstitchExtension
from ..gui.simulator import SimulatorWindow
from ..stitch_plan import stitch_groups_to_stitch_plan


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

        app = wx.App()
        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        screen_rect = display.GetClientArea()

        simulator_pos = (screen_rect[0], screen_rect[1])

        # subtract 1 because otherwise the window becomes maximized on Linux
        width = screen_rect[2] - 1
        height = screen_rect[3] - 1

        simulator = SimulatorWindow(pos=simulator_pos, size=(width, height))
        app.SetTopWindow(simulator)
        simulator.Show()
        simulator.load(stitch_plan)
        simulator.go()
        app.MainLoop()
