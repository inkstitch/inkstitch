import os
import re
import sys

import inkex

from ..i18n import _
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class ImportThreadlist(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--filepath", type=str, default="", dest="filepath")
        self.arg_parser.add_argument("-m", "--method", type=int, default=1, dest="method")
        self.arg_parser.add_argument("-t", "--palette", type=str, default=None, dest="palette")

    def effect(self):
        # Remove selection, we want all the elements in the document
        self.svg.selected.clear()

        if not self.get_elements():
            return

        path = self.options.filepath
        if not os.path.exists(path):
            print(_("File not found."), file=sys.stderr)
            sys.exit(1)
        if os.path.isdir(path):
            print(_("The filepath specified is not a file but a dictionary.\nPlease choose a threadlist file to import."), file=sys.stderr)
            sys.exit(1)

        method = self.options.method
        if method == 1:
            colors = self.parse_inkstitch_threadlist(path)
        else:
            colors = self.parse_threadlist_by_catalog_number(path)

        if all(c is None for c in colors):
            print(_("Couldn't find any matching colors in the file."), file=sys.stderr)
            if method == 1:
                print(_('Please try to import as "other threadlist" and specify a color palette below.'), file=sys.stderr)
            else:
                print(_("Please chose an other color palette for your design."), file=sys.stderr)
            sys.exit(1)

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

            style = element.node.get('style').replace("%s" % element_color, "%s" % colors[i])
            element.node.set('style', style)

    def parse_inkstitch_threadlist(self, path):
        colors = []
        with open(path) as threadlist:
            for line in threadlist:
                if line[0].isdigit():
                    m = re.search(r"\((#[0-9A-Fa-f]{6})\)", line)
                    if m:
                        colors.append(m.group(1))
                    else:
                        # Color not found
                        colors.append(None)
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
                    # some threadlists may add a # in front of the catalof number
                    # let's remove it from the entire string before splitting it up
                    thread = line.replace('#', '').split()
                    catalog_number = set(thread[1:]).intersection(palette_numbers)
                    if catalog_number:
                        color_index = palette_numbers.index(next(iter(catalog_number)))
                        colors.append(palette_colors[color_index])
                    else:
                        # No color found
                        colors.append(None)
        return colors

    def find_elements(self, xpath):
        svg = self.document.getroot()
        elements = svg.xpath(xpath, namespaces=inkex.NSS)
        return elements
