# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _
from .element import EmbroideryElement
from .validation import ObjectTypeWarning
from ..svg.path import get_node_transform


class TextTypeWarning(ObjectTypeWarning):
    name = _("Text")
    description = _("Ink/Stitch cannot work with objects like text.")
    steps_to_solve = [
        _('* Text: Create your own letters or try the lettering tool:'),
        _('- Extensions > Ink/Stitch > Lettering')
    ]


class TextObject(EmbroideryElement):

    def pointer(self):
        transform = get_node_transform(self.node.getparent())
        point = self.node.bounding_box(transform).center

        return point

    def validation_warnings(self):
        yield TextTypeWarning(self.pointer())

    def to_stitch_groups(self, last_stitch_group):
        return []
