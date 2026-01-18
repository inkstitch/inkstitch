# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import wx
import wx.adv

from ..elements import SatinColumn
from ..gui.abort_message import AbortMessageApp
from ..gui.satin_multicolor import MultiColorSatinPanel
from ..gui.simulator import SplitSimulatorWindow
from ..i18n import _
from ..utils.svg_data import get_pagecolor
from .base import InkstitchExtension


class SatinMulticolor(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        self.elements = set()
        self.cancelled = False
        InkstitchExtension.__init__(self, *args, **kwargs)

    def cancel(self):
        self.cancelled = True

    def effect(self):
        self.get_elements()
        satins = [element for element in self.elements if isinstance(element, SatinColumn)]
        if not satins:
            app = AbortMessageApp(
                _("Please select at least one satin column."),
                _("https://inkstitch.org/docs/satin-tools/#multicolor-satin")
            )
            app.MainLoop()
            return

        metadata = self.get_inkstitch_metadata()
        background_color = get_pagecolor(self.svg.namedview)

        app = wx.App()
        frame = SplitSimulatorWindow(
            title=_("Ink/Stitch Multicolor Satin"),
            panel_class=MultiColorSatinPanel,
            elements=satins,
            on_cancel=self.cancel,
            metadata=metadata,
            background_color=background_color,
            target_duration=1
        )

        frame.Show()
        app.MainLoop()

        if self.cancelled:
            # This prevents the superclass from outputting the SVG, because we
            # may have modified the DOM.
            self.skip_output()
