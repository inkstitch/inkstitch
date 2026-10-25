# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..i18n import _
from ..svg import get_node_transform
from .base import InkstitchExtension


class Reorder(InkstitchExtension):
    # Re-stack elements in the order they were selected.

    def effect(self):
        objects = self.svg.selection
        if len(objects) < 2:
            errormsg(_("Please select at least two elements to reorder."))
            return

        insert_parent = objects[0].getparent()
        moved = list(objects)[1:]

        # Moved elements may come from a different layer/group than
        # insert_parent, with a different accumulated transform. Splicing
        # them in below only reparents -- it doesn't adjust each node's own
        # transform -- so without correction a cross-layer reorder visually
        # shifts/rescales the object. Capture each one's absolute transform
        # (and whether it's actually changing parent) before it's detached.
        needs_correction = [node.getparent() is not insert_parent for node in moved]
        old_absolute_transforms = [
            get_node_transform(node) if needs else None
            for node, needs in zip(moved, needs_correction)
        ]

        # We need to delete the nodes from the document,
        # otherwise the insertion index might get confused
        # and we end up with an incorrect result
        for node in objects:
            if not node == objects.first():
                node.delete()

        insert_pos = insert_parent.index(objects[0]) + 1

        insert_parent[insert_pos:insert_pos] = moved

        new_parent_transform = None
        for node, needs, old_absolute_transform in zip(moved, needs_correction, old_absolute_transforms):
            if not needs:
                continue
            if new_parent_transform is None:
                new_parent_transform = get_node_transform(insert_parent)
            node.set('transform', str((-new_parent_transform) @ old_absolute_transform))


if __name__ == '__main__':
    Reorder().run()
