#!/usr/bin/env python
# coding=utf-8

import sys
import wx
import inkex

from lib.gui.grid_state import GridStateManager
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
        old_groups = self.svg.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
        old_group = old_groups[0] if old_groups else None
        
        if old_group is not None:
            serialized_state = old_group.get("inkstitch:grid-state")
            if serialized_state:
                try:
                    initial_state = GridStateManager.from_serialized(serialized_state)
                except Exception as exc:
                    inkex.errormsg(
                        f"Warning: Failed to restore previous cross-stitch canvas state: {exc}\n"
                        "Starting with a clean canvas."
                    )

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
                cell_size=frame.CELL_SIZE,
            )


if __name__ == '__main__':
    CrossStitchCanvas().run()