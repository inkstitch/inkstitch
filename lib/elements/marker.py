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
    name = "Marker"

    def validation_warnings(self):
        # Get the first point from the parsed path instead of using inkex.Path
        path = self.parse_path()
        if path and path[0]:
            repr_point = path[0][0][1]  # First point from first subpath
        else:
            # Fallback to a default point if no path available
            repr_point = (0, 0)
        return [MarkerWarning(repr_point)]

    def to_stitch_groups(self, last_stitch_group, next_element=None):
        return []

    @property
    def first_stitch(self):
        return None
