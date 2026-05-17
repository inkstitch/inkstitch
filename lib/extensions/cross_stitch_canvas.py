#!/usr/bin/env python
# coding=utf-8


import sys
import wx
import inkex

from lib.gui.cross_stitch_canvas import CrossStitchCanvasWindow
from lib.gui.grid_export import EXPORT_GROUP_ID, export_to_svg


class CrossStitchCanvas(inkex.EffectExtension):
    """
    Standard Inkstitch Hook implementation launching our new specialized interactive GUI.
    """
    DEVELOPMENT_ONLY = False

    @classmethod
    def name(cls) -> str:
  
        return "cross_stitch_canvas"

    def add_arguments(self, pars):
        pass

    def effect(self):

        layer = self.svg.get_current_layer()
        initial_state = None
        app = wx.App(False)
        frame = CrossStitchCanvasWindow(None, state=initial_state)
        frame.Show()
        app.MainLoop()
        
        # Only export if the user explicitly clicked "Export to Inkscape".
        # Closing via the window X button or Cancel leaves export_confirmed=False.
        if getattr(frame, 'export_confirmed', False):
            export_to_svg(
                svg_doc=self.svg,
                layer=layer,
                grid_state=frame.state,
                cell_size=15.0,  # Match canvas cell_size
                correction_transform=layer.transform
            )
            
if __name__ == '__main__':
    CrossStitchCanvas().run()