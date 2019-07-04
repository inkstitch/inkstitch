from .base import InkstitchExtension


class CommandsExtension(InkstitchExtension):
    """Base class for extensions that manipulate commands."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        for command in self.COMMANDS:
            self.OptionParser.add_option("--%s" % command, type="inkbool")
