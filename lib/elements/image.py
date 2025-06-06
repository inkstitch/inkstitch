# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _
from ..svg.path import get_node_transform
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class ImageTypeWarning(ObjectTypeWarning):
    name = _("Image")
    description = _("Ink/Stitch can't work with objects like images.")
    steps_to_solve = [
        _('* Convert your image into a path: Path > Trace Bitmap... (Shift+Alt+B) '
          '(further steps might be required)'),
        _('* Alternatively redraw the image with the pen (P) or bezier (B) tool')
    ]


class ImageObject(EmbroideryElement):
    name = "Image"

    def center(self):
        parent = self.node.getparent()
        assert parent is not None, "This should be part of a tree and therefore have a parent"
        transform = get_node_transform(parent)
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        yield ImageTypeWarning(self.center())

    def to_stitch_groups(self, last_stitch_group, next_element):
        return []

    def first_stitch(self):
        return None
