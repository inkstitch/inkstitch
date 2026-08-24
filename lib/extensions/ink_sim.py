# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import os
import sys
import tempfile

# from ..gui.simulator import SimulatorWindow
# from ..svg import convert_length
# from ..utils.svg_data import get_pagecolor
# from .base import InkstitchExtension


from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class InkSim(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        print("InkSim: hello")

        if not self.get_elements():
            sys.exit(0)

        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        print("InkSim: metadata:", self.metadata)

        stitch_groups = self.elements_to_stitch_groups(self.elements)
        print("InkSim: stitch_groups:", stitch_groups)

        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, disable_ties=False,
                                                   min_stitch_len=min_stitch_len)
        print("InkSim: stitch_plan:")

        ThreadCatalog().match_and_apply_palette(stitch_plan, self.metadata['thread-palette'])
        print("InkSim: stitch_plan after palette:")

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file_name = temp_file.name
        print(f"InkSim: temporary file created at {temp_file_name}")

        write_embroidery_file(temp_file_name, stitch_plan, self.document.getroot())

        print(f"InkSim: wrote embroidery file to {temp_file_name}")

        # if sys.platform == "win32":
        #     import msvcrt
        #     msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        # with open(temp_file.name, "rb") as output_file:
        #     sys.stdout.buffer.write(output_file.read())
        #     sys.stdout.flush()

        # clean up the temp file
        # os.remove(temp_file.name)

        # don't let inkex output the SVG!
        # sys.exit(0)

    def effect_old(self):
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
        ink_sim = SimulatorWindow(size=(width, height), background_color=background_color)
        wx.CallLater(100, ink_sim.Centre)
        app.SetTopWindow(ink_sim)
        ink_sim.Show()
        ink_sim.load(stitch_plan)
        ink_sim.set_page_specs(self.get_page_specs(stitch_plan))
        ink_sim.go()
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
