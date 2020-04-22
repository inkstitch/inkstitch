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
        self.OptionParser.add_option("-f", "--filepath", type="str", default="", dest="filepath")
        self.OptionParser.add_option("-m", "--method", type="int", default=1, dest="method")
        self.OptionParser.add_option("-t", "--palette", type="str", default=None, dest="palette")

    def effect(self):
        # Remove selection, we want all the elements in the document
        self.selected = {}

        path = self.options.filepath
        if not os.path.exists(path):
            print >> sys.stderr, _("File not found.")
            sys.exit(1)

        method = self.options.method
        if method == 1:
            colors = self.parse_inkstitch_threadlist(path)
        else:
            colors = self.parse_threadlist_by_catalog_number(path)

        if all(c is None for c in colors):
            print >>sys.stderr, _("Couldn't find any matching colors in the file.")
            if method == 1:
                print >>sys.stderr, _('Please try to import as "other threadlist" and specify a color palette below.')
            else:
                print >>sys.stderr, _("Please chose an other color palette for your design.")
            sys.exit(1)

        # Iterate through the color blocks to aplly colors
        for i, color in enumerate(colors):
            xpath = ".//svg:g[@id='__color_block_%d__']//svg:path" % i
            elements = self.find_elements(xpath)

            # Color Block not found, no need to move on
            if not elements:
                break

            for element in elements:
                style = re.sub(r"#[0-9A-Fa-f]{6}", "%s" % colors[i], element.get('style'))
                element.set('style', style)

    def parse_inkstitch_threadlist(self, path):
        colors = []
        with open(path) as threadlist:
            for line in threadlist:
                if line[0].isdigit():
                    m = re.search(r"\((#[0-9A-Fa-f]{6})\)", line)
                    if m:
                        colors.append(m.group(1))
                    else:
                        # No color found
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
