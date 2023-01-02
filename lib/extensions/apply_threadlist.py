# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import re
import sys

import inkex

import pyembroidery

from ..i18n import _
from ..svg.tags import INKSTITCH_ATTRIBS
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class ApplyThreadlist(InkstitchExtension):
    '''
    Applies colors of a thread list to elements
    Count of colors and elements should fit together
    Use case: reapply colors to e.g. a dst file
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-o", "--options", type=str, default=None, dest="page_1")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_2")
        self.arg_parser.add_argument("-f", "--filepath", type=str, default="", dest="filepath")
        self.arg_parser.add_argument("-m", "--method", type=int, default=1, dest="method")
        self.arg_parser.add_argument("-t", "--palette", type=str, default=None, dest="palette")

    def effect(self):
        # Remove selection, we want all the elements in the document
        self.svg.selection.clear()

        if not self.get_elements():
            return

        path = self.options.filepath
        self.verify_path(path)

        method = self.options.method

        # colors: [[color, cutwork_needle],[...]]
        if path.endswith(('col', 'inf', 'edr')):
            colors = self.parse_color_format(path)
        elif method == 1:
            colors = self.parse_inkstitch_threadlist(path)
        else:
            colors = self.parse_threadlist_by_catalog_number(path)

        self.verify_colors(colors, method)

        # Iterate through the color blocks to apply colors
        element_color = ""
        i = -1
        for element in self.elements:
            if element.color != element_color:
                element_color = element.color
                i += 1

            # No more colors in the list, stop here
            if i == len(colors):
                break

            style = element.node.get('style').replace("%s" % element_color, "%s" % colors[i][0])
            element.node.set('style', style)

            # apply cutwork
            if colors[i][1] is not None:
                element.node.set(INKSTITCH_ATTRIBS['cutwork_needle'], colors[i][1])

    def verify_path(self, path):
        if not os.path.exists(path):
            inkex.errormsg(_("File not found."))
            sys.exit(1)
        if os.path.isdir(path):
            inkex.errormsg(_("The filepath specified is not a file but a dictionary.\nPlease choose a threadlist file to import."))
            sys.exit(1)

    def verify_colors(self, colors, method):
        if all(c is None for c in colors):
            inkex.errormsg(_("Couldn't find any matching colors in the file."))
            if method == 1:
                inkex.errormsg(_('Please try to import as "other threadlist" and specify a color palette below.'))
            else:
                inkex.errormsg(_("Please chose an other color palette for your design."))
            sys.exit(1)

    def parse_inkstitch_threadlist(self, path):
        colors = []
        with open(path) as threadlist:
            for line in threadlist:
                if line[0].isdigit():
                    m = re.search(r"\((#[0-9A-Fa-f]{6})\)", line)
                    if m:
                        colors.append([m.group(1), None])
                    else:
                        # Color not found
                        colors.append([None, None])
        return colors

    def parse_color_format(self, path):
        colors = []
        threads = pyembroidery.read(path).threadlist
        for color in threads:
            if color.description.startswith("Cut"):
                # there is a maximum of 4 needles, we can simply take the last element from the description string
                colors.append([color.hex_color(), color.description[-1]])
            else:
                colors.append([color.hex_color(), None])
        return colors

    def parse_threadlist_by_catalog_number(self, path):
        palette_name = self.options.palette
        palette = ThreadCatalog().get_palette_by_name(palette_name)

        colors = []
        palette_numbers = []
        palette_colors = []

        for color in palette:
            palette_numbers.append(color.number)
            palette_colors.append('#%s' % color.hex_digits.lower())
        with open(path) as threadlist:
            for line in threadlist:
                if line[0].isdigit():
                    # some threadlists may add a # in front of the catalog number
                    # let's remove it from the entire string before splitting it up
                    thread = line.replace('#', '').split()
                    catalog_number = set(thread[1:]).intersection(palette_numbers)
                    if catalog_number:
                        color_index = palette_numbers.index(next(iter(catalog_number)))
                        colors.append([palette_colors[color_index], None])
                    else:
                        # No color found
                        colors.append([None, None])
        return colors
