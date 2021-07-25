# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..commands import LAYER_COMMANDS, add_layer_commands
from ..i18n import _
from .commands import CommandsExtension


class LayerCommands(CommandsExtension):
    COMMANDS = LAYER_COMMANDS

    def effect(self):
        commands = [command for command in self.COMMANDS if getattr(self.options, command)]

        if not commands:
            inkex.errormsg(_("Please choose one or more commands to add."))
            return

        add_layer_commands(self.svg.get_current_layer(), commands)
