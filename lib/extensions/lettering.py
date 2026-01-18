# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import inkex
import wx
import wx.adv

from ..gui.abort_message import AbortMessageApp
from ..gui.lettering import LetteringPanel
from ..gui.simulator import SplitSimulatorWindow
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_LETTERING, SVG_GROUP_TAG
from ..utils.svg_data import get_pagecolor
from .commands import CommandsExtension


class Lettering(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        self.cancelled = False
        CommandsExtension.__init__(self, *args, **kwargs)

    def cancel(self):
        self.cancelled = True

    def get_or_create_group(self):
        if self.svg.selection:
            groups = set()

            for node in self.svg.selection:
                if node.tag == SVG_GROUP_TAG and INKSTITCH_LETTERING in node.attrib:
                    groups.add(node)

                for group in node.iterancestors(SVG_GROUP_TAG):
                    if INKSTITCH_LETTERING in group.attrib:
                        groups.add(group)

            if len(groups) > 1:
                app = AbortMessageApp(
                    _("Please select only one block of text."),
                    _("https://inkstitch.org/docs/lettering/#lettering-tool")
                )
                app.MainLoop()
                sys.exit(1)
            elif len(groups) == 0:
                return self.create_group()
            else:
                return list(groups)[0]
        else:
            return self.create_group()

    def create_group(self):
        group = inkex.Group(attrib={
            INKSCAPE_LABEL: _("Ink/Stitch Lettering"),
            "transform": get_correction_transform(self.get_current_layer(), child=True)
        })
        self.get_current_layer().append(group)
        return group

    def effect(self):
        metadata = self.get_inkstitch_metadata()
        background_color = get_pagecolor(self.svg.namedview)
        app = wx.App()
        frame = SplitSimulatorWindow(
            title=_("Ink/Stitch Lettering"),
            panel_class=LetteringPanel,
            group=self.get_or_create_group(),
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
