# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..i18n import _
from .base import InkstitchExtension


class Reorder(InkstitchExtension):
    # Remove selected objects from the document and re-add them in the order they
    # were selected.

    def effect(self):
        objects = self.svg.selection

        if not objects:
            errormsg(_("Please select at least two elements to reorder."))
            return

        for obj in objects:
            if not obj == objects.first():
                obj.getparent().remove(obj)

        insert_parent = objects[0].getparent()
        insert_pos = insert_parent.index(objects[0])

        insert_parent.remove(objects[0])

        insert_parent[insert_pos:insert_pos] = objects


if __name__ == '__main__':
    e = Reorder()
    e.affect()
