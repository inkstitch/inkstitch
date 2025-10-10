# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

from inkex import NSS
from lxml import etree

from .base import InkstitchExtension


class LetteringRemoveKerning(InkstitchExtension):
    '''
    This extension helps font creators to generate the json file for the lettering tool
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-p", "--font-files", type=str, default="", dest="paths")

    def effect(self):
        # file paths
        paths = self.options.paths.split("|")
        for path in paths:
            if not os.path.isfile(path):
                continue
            with open(path, 'r+', encoding="utf-8") as fontfile:
                svg = etree.parse(fontfile)
                xpath = ".//svg:font[1]"
                kerning = svg.xpath(xpath, namespaces=NSS)
                if kerning:
                    kerning[0].getparent().remove(kerning[0])
                    fontfile.seek(0)
                    fontfile.write(etree.tostring(svg).decode('utf-8'))
                    fontfile.truncate()
