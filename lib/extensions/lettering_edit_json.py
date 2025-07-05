# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
from inkex import Layer

from ..gui.edit_json import LetteringEditJsonPanel
from ..gui.simulator import SplitSimulatorWindow
from ..i18n import _
from ..svg import get_correction_transform
from ..utils.svg_data import get_pagecolor
from .base import InkstitchExtension


class LetteringEditJson(InkstitchExtension):
    '''
    This extension helps font creators modify the JSON file of a lettering font.
    '''
    def effect(self):
        layer = Layer()
        self.svg.add(layer)
        transform = get_correction_transform(layer, child=True)
        layer.transform = transform

        metadata = self.get_inkstitch_metadata()
        background_color = get_pagecolor(self.svg.namedview)

        app = wx.App()
        frame = SplitSimulatorWindow(
            title=_("Ink/Stitch Edit JSON"),
            panel_class=LetteringEditJsonPanel,
            layer=layer,
            metadata=metadata,
            background_color=background_color,
            target_duration=1
        )

        frame.Show()
        app.MainLoop()

        layer.delete()
