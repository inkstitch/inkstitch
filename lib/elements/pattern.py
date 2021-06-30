# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class PatternWarning(ObjectTypeWarning):
    name = _("Pattern Element")
    description = _("This element will not be embroidered. "
                    "It will appear as a pattern in objects of it's group in the object panel. "
                    "Sub-group objects will be ignored.")
    steps_to_solve = [
        _("Turn the pattern marker off:"),
        _('* Open the Fill and Stroke panel (Objects > Fill and Stroke)'),
        _('* Go to the Stroke style tab'),
        _('* Under "Markers" choose the first (empty) option in the first dropdown list.')
    ]


class PatternObject(EmbroideryElement):

    def validation_warnings(self):
        repr_point = next(inkex.Path(self.parse_path()).end_points)
        yield PatternWarning(repr_point)

    def to_patches(self, last_patch):
        return []
