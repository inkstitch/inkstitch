# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, errormsg

from ..i18n import _
from .base import InkstitchExtension


class ApplyAttribute(InkstitchExtension):
    '''
    Applies a given attribute to all selected elements
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-n", "--namespace", dest="namespace", type=str, default='inkstitch')
        self.arg_parser.add_argument("-k", "--key", dest="key", type=str, default='')
        self.arg_parser.add_argument("-v", "--value", dest="value", type=str, default='')
        self.arg_parser.add_argument("-r", "--remove", dest="remove", type=Boolean, default=False)

    def effect(self):
        self.get_elements()
        if not self.elements:
            errormsg(_("Please select at least one element."))
            return

        if not self.options.key:
            errormsg(_("Please enter the attribute name."))
            return

        key = ''
        if self.options.namespace:
            key = f'{self.options.namespace}:'
        key += self.options.key

        if self.options.remove:
            for element in self.elements:
                element.node.pop(key)
        else:
            if not self.options.value:
                errormsg(_("Please enter a value."))
                return
            for element in self.elements:
                element.node.set(key, self.options.value)
