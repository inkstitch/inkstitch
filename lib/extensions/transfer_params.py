# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_GROUP_TAG
from .base import InkstitchExtension


class TransferParams(InkstitchExtension):
    # Transfer inkstitch namespaced attributes from the first selected element to the rest of selection

    def effect(self):
        objects = self.get_selected_in_order()
        if len(objects) < 2:
            inkex.errormsg(_("This function transfers Ink/Stitch parameters from the first selected element to the rest of the selection. "
                             "Please select at least two elements."))
            return

        copy_from = objects[0]
        copy_to = objects[1:]

        # extract copy_to group elements
        for i, element in enumerate(copy_to):
            if element.tag == SVG_GROUP_TAG:
                for descendant in element.iterdescendants():
                    if descendant.tag in EMBROIDERABLE_TAGS:
                        copy_to.append(descendant)
                copy_to.pop(i)

        # remove inkstitch params from copy_to elements
        for element in copy_to:
            attribs = self.get_inkstitch_attributes(copy_to[0])
            for attrib in attribs:
                element.pop(attrib)

        # paste inkstitch params from copy_from element to copy_to elements
        for attrib in self.get_inkstitch_attributes(copy_from):
            for element in copy_to:
                element.attrib[attrib] = copy_from.attrib[attrib]

    def get_inkstitch_attributes(self, node):
        return {k: v for k, v in node.attrib.iteritems() if inkex.NSS['inkstitch'] in k}

    def get_selected_in_order(self):
        selected = []
        for i in self.options.ids:
            path = '//*[@id="%s"]' % i
            for node in self.document.xpath(path, namespaces=inkex.NSS):
                selected.append(node)
        return selected
