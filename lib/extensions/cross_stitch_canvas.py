#!/usr/bin/env python
# coding=utf-8

import wx
import inkex

from lib.gui.cross_stitch.cross_stitch_canvas import CrossStitchCanvasWindow
from lib.gui.cross_stitch.grid_export import export_to_svg


class CrossStitchCanvas(inkex.EffectExtension):
    """Launch the interactive wxPython cross-stitch canvas tool."""
    DEVELOPMENT_ONLY = False

    @classmethod
    def name(cls) -> str:  # type: ignore[override]
        return "cross_stitch_canvas"

    def add_arguments(self, pars):
        pass

    def effect(self):
        layer = self.svg.get_current_layer()

        from lib.gui.cross_stitch.grid_export import import_from_svg
        initial_state = None
        try:
            cell_sz = CrossStitchCanvasWindow.CELL_SIZE
            initial_state = import_from_svg(self.svg, cell_sz)
        except Exception as exc:
            inkex.errormsg(
                f"Warning: Failed to restore previous state: {exc}\n"
                "Starting with a clean canvas."
            )

        app = wx.App(False)
        frame = CrossStitchCanvasWindow(None, state=initial_state)
        frame.Show()
        app.MainLoop()

        # Only export if the user explicitly clicked "Export to Inkscape".
        # Closing via X or Cancel leaves export_confirmed=False.
        if getattr(frame, 'export_confirmed', False):
            from lib.gui.cross_stitch.grid_export import EXPORT_GROUP_ID
            from lib.svg.path import get_node_transform
            from lib.svg import get_correction_transform

            tx, ty = 0.0, 0.0
            old_groups = self.svg.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
            if old_groups:
                try:
                    global_trans = get_node_transform(old_groups[0])
                    tx = global_trans.e
                    ty = global_trans.f
                except Exception:
                    pass

            cell_size = frame.CELL_SIZE
            tx_snapped = round(tx / cell_size) * cell_size
            ty_snapped = round(ty / cell_size) * cell_size

            corr_str = get_correction_transform(layer, child=True)
            corr_transform = (
                inkex.Transform(corr_str) if corr_str else inkex.Transform()
            )

            snap_t = inkex.Transform().add_translate(tx_snapped, ty_snapped)
            final_transform = corr_transform @ snap_t

            export_to_svg(
                svg_doc=self.svg,
                layer=layer,
                grid_state=frame.state,
                cell_size=cell_size,
                correction_transform=final_transform,
            )


if __name__ == '__main__':
    CrossStitchCanvas().run()