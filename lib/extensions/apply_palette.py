# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..elements import Clone, FillStitch
from ..gui.abort_message import AbortMessageApp
from ..gui.apply_palette import ApplyPaletteApp
from ..i18n import _
from ..threads import ThreadCatalog, ThreadColor
from .base import InkstitchExtension


class ApplyPalette(InkstitchExtension):
    '''
    Applies colors of a color palette to elements
    '''

    def effect(self) -> None:
        # Remove selection, we want all the elements in the document
        self.svg.selection.clear()

        if not self.get_elements():
            app = AbortMessageApp(
                _("There is no stitchable element in the document."),
                _("https://inkstitch.org/")
            )
            app.MainLoop()
            return

        palette_choice = ApplyPaletteApp()
        if palette_choice.palette:
            self.apply_palette(palette_choice.palette)

    def apply_palette(self, palette_name: str) -> None:
        palette = ThreadCatalog().get_palette_by_name(palette_name)

        # Iterate through the color blocks to apply colors
        for element in self.elements:
            if isinstance(element, Clone):
                # clones use the color of their source element
                continue
            elif hasattr(element, 'gradient') and element.gradient is not None:
                # apply colors to each gradient stop
                for i, gradient_style in enumerate(element.gradient.stop_styles):
                    color = gradient_style['stop-color']
                    gradient_style['stop-color'] = palette.nearest_color(ThreadColor(color)).to_hex_str()
                continue

            nearest_color = palette.nearest_color(ThreadColor(element.color))
            if isinstance(element, FillStitch):
                element.node.style['fill'] = nearest_color.to_hex_str()
            else:
                element.node.style['stroke'] = nearest_color.to_hex_str()

        metadata = self.get_inkstitch_metadata()
        metadata['thread-palette'] = palette_name
