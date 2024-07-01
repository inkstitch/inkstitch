# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..commands import OBJECT_COMMANDS, add_commands
from ..elements import Clone
from ..i18n import _
from .commands import CommandsExtension


class ObjectCommands(CommandsExtension):
    COMMANDS = OBJECT_COMMANDS

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            errormsg(_("Please select one or more objects to which to attach commands."))
            return

        self.svg = self.document.getroot()

        commands = [command for command in self.COMMANDS if getattr(self.options, command)]

        if not commands:
            errormsg(_("Please choose one or more commands to attach."))
            return

        # Clones currently can't really take any commands, so error if we try to add one to them.
        clones = [e for e in self.elements if isinstance(e, Clone)]
        if clones:
            errormsg(_(
                "Cannot attach commands to Clone element(s) {clones}. "
                "They must be unlinked to add commands.\n"
                "* Select the clone(s)\n"
                "* Run: Extensions > Ink/Stitch > Edit > Unlink Clone"
            ).format(clones=", ".join(c.node.get_id() for c in clones)))

        # Each object (node) in the SVG may correspond to multiple Elements of different
        # types (e.g. stroke + fill).  We only want to process each one once.
        seen_nodes = set()

        for element in self.elements:
            if element.node not in seen_nodes and element.shape and not isinstance(element, Clone):
                add_commands(element, commands)
                seen_nodes.add(element.node)
