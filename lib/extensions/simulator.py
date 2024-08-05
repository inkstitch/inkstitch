# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ..gui.simulator import SimulatorWindow
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import convert_length
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
        width = int(screen_rect.width * 0.8)
        height = int(screen_rect.height * 0.8)
        simulator = SimulatorWindow(size=(width, height), background_color=background_color)
        wx.CallLater(100, simulator.Centre)
        app.SetTopWindow(simulator)
        simulator.Show()
        simulator.load(stitch_plan)
        simulator.set_page_specs(self.get_page_specs(stitch_plan))
        simulator.go()
        app.MainLoop()

    def get_page_specs(self, stitch_plan):
        svg = self.document.getroot()
        width = svg.get('width', 0)
        height = svg.get('height', 0)
        page_color = "white"
        desk_color = "white"
        border_color = "black"
        show_page_shadow = "true"

        named_view = svg.namedview
        if named_view is not None:
            page_color = named_view.get('pagecolor', page_color)
            desk_color = named_view.get('inkscape:deskcolor', desk_color)
            border_color = named_view.get('bordercolor', border_color)
            show_page_shadow = named_view.get('inkscape:showpageshadow', show_page_shadow) in ['true', 'yes', 'y', '1', '2']

        return {
            "width": convert_length(width),
            "height": convert_length(height),
            "x": stitch_plan.bounding_box[0],
            "y": stitch_plan.bounding_box[1],
            "page_color": page_color,
            "desk_color": desk_color,
            "border_color": border_color,
            "show_page_shadow": show_page_shadow
        }
