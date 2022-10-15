# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Transform

from .base import InkstitchExtension


class CommandsScaleSymbols(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-s", "--size", dest="size", type=float, default=1)

    def effect(self):
        size = self.options.size

        svg = self.document.getroot()
        command_symbols = svg.xpath(".//svg:symbol[starts-with(@id,'inkstitch_')]", namespaces=NSS)
        for symbol in command_symbols:
            transform = Transform(symbol.get('transform')).add_scale(size)
            symbol.set('transform', str(transform))

        markers = svg.xpath(".//svg:marker[starts-with(@id, 'inkstitch')]", namespaces=NSS)
        for marker in markers:
            marker_size = float(marker.get('markerWidth', 0.5)) * size
            marker.set('markerWidth', marker_size)
