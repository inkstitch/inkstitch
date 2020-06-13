from .base import InkstitchExtension
import inkex


class CommandsExtension(InkstitchExtension):
    """Base class for extensions that manipulate commands."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        for command in self.COMMANDS:
            self.arg_parser.add_argument("--%s" % command, type=inkex.utils.Boolean)
