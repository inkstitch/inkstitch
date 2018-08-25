import os
import inkex
from copy import deepcopy

from .base import InkstitchExtension
from ..utils import get_bundled_dir, cache
from ..svg.tags import SVG_DEFS_TAG


class CommandsExtension(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        for command in self.COMMANDS:
            self.OptionParser.add_option("--%s" % command, type="inkbool")

    @property
    def symbols_path(self):
        return os.path.join(get_bundled_dir("symbols"), "inkstitch.svg")

    @property
    @cache
    def symbols_svg(self):
        with open(self.symbols_path) as symbols_file:
            return inkex.etree.parse(symbols_file)

    @property
    @cache
    def symbol_defs(self):
        return self.symbols_svg.find(SVG_DEFS_TAG)

    @property
    @cache
    def defs(self):
        return self.document.find(SVG_DEFS_TAG)

    def ensure_symbol(self, command):
        path = "./*[@id='inkstitch_%s']" % command
        if self.defs.find(path) is None:
            self.defs.append(deepcopy(self.symbol_defs.find(path)))
