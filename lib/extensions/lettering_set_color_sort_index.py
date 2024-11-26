# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .base import InkstitchExtension


class LetteringSetColorSortIndex(InkstitchExtension):
    '''
    This extension sets a color sort index to selected elements.
    It enables font authors to define the order of elements in multicolor fonts when color sorted.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-i", "--color-sort-index", type=int, default=0, dest="color_sort_index")

    def effect(self):
        selection = self.svg.selection
        self.set_index(selection)

    def set_index(self, element_list):
        for element in element_list:
            if element.TAG == "path":
                element.set('inkstitch:color_sort_index', self.options.color_sort_index)
            elif element.TAG == "g":
                if element.get_id().startswith('command_group'):
                    element.set('inkstitch:color_sort_index', self.options.color_sort_index)
                else:
                    self.set_index(element.getchildren())
