# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, ShapeElement, errormsg

from ..i18n import _
from .base import InkstitchExtension


class DuplicateParams(InkstitchExtension):
    # Transfer inkstitch namespaced attributes from the first selected element to the rest of selection

    def effect(self):
        objects = self.svg.selection.get(ShapeElement)
        if len(objects) < 2:
            errormsg(_("This function copies Ink/Stitch parameters from the first selected element to the rest of the selection. "
                       "Please select at least two elements."))
            return

        copy_from = objects.first()
        copy_from_attribs = get_inkstitch_attributes(copy_from)

        copy_to = objects

        # remove inkstitch params from copy_to elements
        for element in copy_to:
            if element == copy_to.first():
                continue
            copy_to_attribs = get_inkstitch_attributes(element)
            for attrib in copy_to_attribs:
                element.pop(attrib)

        # paste inkstitch params from copy_from element to copy_to elements
        for attrib in copy_from_attribs:
            for element in copy_to:
                element.attrib[attrib] = copy_from_attribs[attrib]


def get_inkstitch_attributes(node):
    return {k: v for k, v in node.attrib.iteritems() if NSS['inkstitch'] in k}
