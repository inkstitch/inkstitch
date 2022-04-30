# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean

from .base import InkstitchExtension


class CommandsExtension(InkstitchExtension):
    """Base class for extensions that manipulate commands."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        for command in self.COMMANDS:
            self.arg_parser.add_argument("--%s" % command, type=Boolean)

        self.arg_parser.add_argument("--autorun_start", dest="autorun_start", type=Boolean, default=False)
        self.arg_parser.add_argument("--autorun_end", dest="autorun_end", type=Boolean, default=False)
