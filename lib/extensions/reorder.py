# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..i18n import _
from .base import InkstitchExtension


class Reorder(InkstitchExtension):
    # Re-stack elements in the order they were selected.

    def effect(self):
        objects = self.svg.selection
        if len(objects) < 2:
            errormsg(_("Please select at least two elements to reorder."))
            return

        # We need to delete the nodes from the document,
        # otherwise the insertion index might get confused
        # and we end up with an incorrect result
        for node in objects:
            if not node == objects.first():
                node.delete()

        insert_parent = objects[0].getparent()
        insert_pos = insert_parent.index(objects[0]) + 1

        insert_parent[insert_pos:insert_pos] = list(objects)[1:]


if __name__ == '__main__':
    Reorder().run()
