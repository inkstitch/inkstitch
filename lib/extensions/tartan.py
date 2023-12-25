# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# from ..stitch_plan import stitch_groups_to_stitch_plan

import sys

import wx
import wx.adv
from inkex import errormsg

from ..gui.simulator import SplitSimulatorWindow
from ..gui.tartan import TartanMainPanel
from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_TARTAN, SVG_GROUP_TAG
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
            self._get_elements()

    def _get_elements(self):
        for node in self.svg.selection:
            node = self.get_outline(node)
            if node.style('fill'):
                self.elements.add(node)

    def get_outline(self, node):
        # existing tartans are marked through their outline element
        # we have either selected the element itself or some other element within a tartan group
        if node.get(INKSTITCH_TARTAN, None):
            return node
        if node.get_id().startswith('inkstitch-tartan'):
            for element in node.iterchildren(EMBROIDERABLE_TAGS):
                if element.get(INKSTITCH_TARTAN, None):
                    return element
        for group in node.iterancestors(SVG_GROUP_TAG):
            if group.get_id().startswith('inkstitch-tartan'):
                for element in group.iterchildren(EMBROIDERABLE_TAGS):
                    if element.get(INKSTITCH_TARTAN, None):
                        return element
        # if we don't find an existing tartan, return node
        return node

    def effect(self):
        self.get_tartan_elements()
        if not self.elements:
            errormsg(_("To create a tartan pattern please select at least one element with a fill color."))
            return
        metadata = self.get_inkstitch_metadata()

        app = wx.App()
        frame = SplitSimulatorWindow(
            title=_("Ink/Stitch Tartan"),
            panel_class=TartanMainPanel,
            elements=list(self.elements),
            on_cancel=self.cancel,
            metadata=metadata,
            target_duration=1
        )

        frame.Show()
        app.MainLoop()

        if self.cancelled:
            # This prevents the superclass from outputting the SVG, because we
            # may have modified the DOM.
            sys.exit(0)
