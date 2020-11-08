import inkex

from ..commands import OBJECT_COMMANDS, add_commands
from ..i18n import _
from .commands import CommandsExtension


class ObjectCommands(CommandsExtension):
    COMMANDS = OBJECT_COMMANDS

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selected:
            inkex.errormsg(_("Please select one or more objects to which to attach commands."))
            return

        self.svg = self.document.getroot()

        commands = [command for command in self.COMMANDS if getattr(self.options, command)]

        if not commands:
            inkex.errormsg(_("Please choose one or more commands to attach."))
            return

        # Each object (node) in the SVG may correspond to multiple Elements of different
        # types (e.g. stroke + fill).  We only want to process each one once.
        seen_nodes = set()

        for element in self.elements:
            if element.node not in seen_nodes:
                add_commands(element, commands)
                seen_nodes.add(element.node)
