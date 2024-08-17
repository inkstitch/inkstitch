# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import wx
import wx.adv

from ..gui.abort_message import AbortMessageApp
from ..gui.simulator import SplitSimulatorWindow
from ..gui.tartan import TartanMainPanel
from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_TARTAN, SVG_GROUP_TAG
from ..utils.svg_data import get_pagecolor
from .base import InkstitchExtension


class Tartan(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        self.elements = set()
        self.cancelled = False
        InkstitchExtension.__init__(self, *args, **kwargs)

    def cancel(self):
        self.cancelled = True

    def get_tartan_elements(self):
        if self.svg.selection:
            for node in self.svg.selection:
                self.get_selection(node)

    def get_selection(self, node):
        if node.TAG == 'g' and not node.get_id().startswith('inkstitch-tartan'):
            for child_node in node.iterchildren():
                self.get_selection(child_node)
        else:
            node = self.get_outline(node)
            if node.tag in EMBROIDERABLE_TAGS and node.style('fill') is not None:
                self.elements.add(node)

    def get_outline(self, node):
        # existing tartans are marked through their outline element
        # we have either selected the element itself or some other element within a tartan group
        if node.get(INKSTITCH_TARTAN, None) is not None:
            return node
        if node.get_id().startswith('inkstitch-tartan'):
            for element in node.iterchildren(EMBROIDERABLE_TAGS):
                if element.get(INKSTITCH_TARTAN, None):
                    return element
        for group in node.iterancestors(SVG_GROUP_TAG):
            if group.get_id().startswith('inkstitch-tartan'):
                for element in group.iterchildren(EMBROIDERABLE_TAGS):
                    if element.get(INKSTITCH_TARTAN, None) is not None:
                        return element
        # if we don't find an existing tartan, return node
        return node

    def effect(self):
        self.get_tartan_elements()

        if not self.elements:
            app = AbortMessageApp(
                _("To create a tartan pattern please select at least one element with a fill color."),
                _("https://inkstitch.org/docs/fill-tools/#tartan")
            )
            app.MainLoop()
            return

        metadata = self.get_inkstitch_metadata()
        background_color = get_pagecolor(self.svg.namedview)

        app = wx.App()
        frame = SplitSimulatorWindow(
            title=_("Ink/Stitch Tartan"),
            panel_class=TartanMainPanel,
            elements=list(self.elements),
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
            sys.exit(0)
