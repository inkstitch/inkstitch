#!/usr/bin/env python
# coding=utf-8

"""
Entry point for the Cross Stitch Canvas inkstitch extension.
"""

import sys
import wx
import inkex

# For Ink/Stitch standard routing we mock sys.path in standard extensions if needed,
# however since these scripts are run dynamically within an Inkstitch context we path 
# relative components.
from lib.gui.cross_stitch_canvas import CrossStitchCanvasWindow
from lib.gui.grid_export import EXPORT_GROUP_ID, export_to_svg


class CrossStitchCanvas(inkex.EffectExtension):
    """
    Standard Inkstitch Hook implementation launching our new specialized interactive GUI.
    """
    DEVELOPMENT_ONLY = False

    @classmethod
    def name(cls) -> str:
        # Must match the template filename: templates/cross_stitch_canvas.xml
        # The visible Inkscape menu label is defined inside that XML template.
        return "cross_stitch_canvas"

    def add_arguments(self, pars):
        # No parameters needed for MVP; stub retained for INX generator compatibility.
        pass

    def effect(self):
        # Get active layer pointer to enforce SVG grouping behavior
        # (Using a stubbed fallback for get_current_layer to run correctly without breaking if refactored)
        layer = self.svg.get_current_layer()
        
        # State restore from serialized SVG attribute is deferred to Phase 2.
        # from_serialized is not yet implemented; start fresh every time.
        initial_state = None

        # Initiate underlying Wx Python context with any restored state.
        app = wx.App(False)
        frame = CrossStitchCanvasWindow(None, state=initial_state)
        
        # Ink/Stitch UI panels must block program thread so they can run safely
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