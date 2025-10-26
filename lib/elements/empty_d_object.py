# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _
from ..svg.tags import INKSCAPE_LABEL
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class EmptyD(ObjectTypeWarning):
    name = _("Empty Path")
    description = _("There is an invalid object in the document without geometry information.")
    steps_to_solve = [
        _('* Run Extensions > Ink/Stitch > Troubleshoot > Cleanup Document...')
    ]


class EmptyDObject(EmbroideryElement):

    def validation_warnings(self):
        label = self.node.get(INKSCAPE_LABEL) or self.node.get("id")
        yield EmptyD((0, 0), label)

    @property
    def shape(self):
        return

    @property
    def first_stitch(self):
        return None

    @property
    def color(self):
        # We are not able to sitch this element, but some method calling the element may require a color definition.
        # So let's simply define a black color
        return 'black'

    def to_stitch_groups(self, last_stitch_group, next_element=None):
        return []
