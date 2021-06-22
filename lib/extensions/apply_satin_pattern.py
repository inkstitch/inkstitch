# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from ..svg.tags import INKSTITCH_ATTRIBS
from .base import InkstitchExtension
from ..elements import SatinColumn


class ApplySatinPattern(InkstitchExtension):
    # Add inkstitch:pattern attribute to selected patterns. The patterns will be projected on a satin column, which must be in the selection too

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selected or not any(isinstance(item, SatinColumn) for item in self.elements) or len(self.svg.selected) < 2:
            inkex.errormsg(_("Please select at least one satin column and a pattern."))
            return

        if sum(isinstance(item, SatinColumn) for item in self.elements) > 1:
            inkex.errormsg(_("Please select only one satin column."))
            return

        satin_id = self.get_satin_column().node.get('id', None)
        patterns = self.get_patterns()

        for pattern in patterns:
            pattern.node.set(INKSTITCH_ATTRIBS['pattern'], satin_id)

    def get_satin_column(self):
        return list(filter(lambda satin: isinstance(satin, SatinColumn), self.elements))[0]

    def get_patterns(self):
        return list(filter(lambda satin: not isinstance(satin, SatinColumn), self.elements))
