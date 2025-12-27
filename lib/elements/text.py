# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _
from ..svg.path import get_node_transform
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class TextTypeWarning(ObjectTypeWarning):
    name = _("Text")
    description = _("Ink/Stitch cannot work with objects like text.")
    steps_to_solve = [
        _('* Text: Create your own letters or try the lettering tool:'),
        _('- Extensions > Ink/Stitch > Lettering')
    ]


class TextObject(EmbroideryElement):
    name = "Text"
    element_name = _("Text")

    def pointer(self):
        parent = self.node.getparent()
        assert parent is not None, "This should be part of a tree and therefore have a parent"
        transform = get_node_transform(parent)
        point = self.node.bounding_box(transform).center

        return point

    def validation_warnings(self):
        yield TextTypeWarning(self.pointer())

    def to_stitch_groups(self, last_stitch_group, next_element=None):
        return []

    def first_stitch(self):
        return None
