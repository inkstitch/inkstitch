# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from ..marker import set_marker
from ..svg.tags import EMBROIDERABLE_TAGS
from .base import InkstitchExtension


class SelectionToGuideLine(InkstitchExtension):

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selected:
            inkex.errormsg(_("Please select at least one object to be marked as a guide line."))
            return

        for pattern in self.get_nodes():
            if pattern.tag in EMBROIDERABLE_TAGS:
                set_marker(pattern, 'start', 'guide-line')
