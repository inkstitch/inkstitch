# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..commands import OBJECT_COMMANDS, add_commands
from ..i18n import _
from .commands import CommandsExtension
from ..marker import set_marker


class ObjectCommands(CommandsExtension):
    COMMANDS = OBJECT_COMMANDS
    MARKERS = ['autorun_start', 'autorun_end']

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more objects to which to attach commands."))
            return

        self.svg = self.document.getroot()

        commands = [command for command in self.COMMANDS if getattr(self.options, command)]
        markers = [marker for marker in self.MARKERS if getattr(self.options, marker)]

        if not commands and not markers:
            inkex.errormsg(_("Please choose one or more commands to attach."))
            return

        # Each object (node) in the SVG may correspond to multiple Elements of different
        # types (e.g. stroke + fill).  We only want to process each one once.
        seen_nodes = set()

        for element in self.elements:
            if element.node not in seen_nodes:
                add_commands(element, commands)
                self.add_markers(element, markers)
                seen_nodes.add(element.node)

    def add_markers(self, element, markers):
        for marker in markers:
            position = "start" if "start" in marker else "end"
            set_marker(element.node, position, marker)
