# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class EmptyD(ObjectTypeWarning):
    name = _("Empty D-Attribute")
    description = _("There is an invalid path object in the document, the d-attribute is missing.")
    steps_to_solve = [
        _('* Run Extensions > Ink/Stitch > Troubleshoot > Cleanup Document...')
    ]


class EmptyDObject(EmbroideryElement):

    def validation_warnings(self):
        yield EmptyD((0, 0))

    def to_patches(self, last_patch):
        return []
