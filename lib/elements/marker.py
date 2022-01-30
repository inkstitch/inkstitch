# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class MarkerWarning(ObjectTypeWarning):
    name = _("Marker Element")
    description = _("This element will not be embroidered. "
                    "It will be applied to objects in the same group. Objects in sub-groups will be ignored.")
    steps_to_solve = [
        _("Turn back to normal embroidery element mode, remove the marker:"),
        _('* Open the Fill and Stroke panel (Objects > Fill and Stroke)'),
        _('* Go to the Stroke style tab'),
        _('* Under "Markers" choose the first (empty) option in the first dropdown list.')
    ]


class MarkerObject(EmbroideryElement):

    def validation_warnings(self):
        repr_point = next(inkex.Path(self.parse_path()).end_points)
        yield MarkerWarning(repr_point)

    def to_stitch_groups(self, last_patch):
        return []
