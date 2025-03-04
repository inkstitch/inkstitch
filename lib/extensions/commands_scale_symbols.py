# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Transform

from .base import InkstitchExtension


class CommandsScaleSymbols(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-s", "--size", dest="size", type=int, default=100)

    def effect(self):
        # by default commands are scaled down to 0.2
        size = 0.25 * self.options.size / 100

        # scale symbols
        svg = self.document.getroot()
        command_symbols = svg.xpath(".//svg:symbol[starts-with(@id,'inkstitch_')]", namespaces=NSS)
        for symbol in command_symbols:
            transform = Transform(f'scale({size})')
            symbol.set('transform', str(transform))

        # scale markers
        markers = svg.xpath(".//svg:marker[starts-with(@id, 'inkstitch')]", namespaces=NSS)
        for marker in markers:
            marker.set('markerWidth', str(size / 2))
