# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .layer_commands import LayerCommands
from ..commands import GLOBAL_COMMANDS


# It's a bit weird subclassing this from LayerCommands, but global commands
# must still be placed in a layer.  That means the two extensions
# do the same thing and the code is the same.  We keep this as separate
# extensions because we want the user to understand that global commands
# affect the entire document, not just the current layer.

class GlobalCommands(LayerCommands):
    COMMANDS = GLOBAL_COMMANDS
