# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..elements import FillStitch
from ..threads import ThreadCatalog, ThreadColor
from .base import InkstitchExtension


class ApplyPalette(InkstitchExtension):
    '''
    Applies colors of a color palette to elements
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-o", "--tabs")
        self.arg_parser.add_argument("-t", "--palette", type=str, default=None, dest="palette")

    def effect(self):
        # Remove selection, we want all the elements in the document
        self.svg.selection.clear()

        if not self.get_elements():
            return

        palette_name = self.options.palette
        palette = ThreadCatalog().get_palette_by_name(palette_name)

        # Iterate through the color blocks to apply colors
        for element in self.elements:
            nearest_color = palette.nearest_color(ThreadColor(element.color))
            if isinstance(element, FillStitch):
                element.node.style['fill'] = nearest_color.to_hex_str()
            else:
                element.node.style['stroke'] = nearest_color.to_hex_str()

        metadata = self.get_inkstitch_metadata()
        metadata['thread-palette'] = palette_name
