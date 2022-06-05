# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import SatinColumn
from ..i18n import _
from .base import InkstitchExtension


class Flip(InkstitchExtension):
    def flip(self, satin):
        csp = satin.path

        if len(csp) > 1:
            first, second = satin.rail_indices
            csp[first], csp[second] = csp[second], csp[first]

            satin.node.set("d", inkex.paths.CubicSuperPath.to_path(csp))

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more satin columns to flip."))
            return

        for element in self.elements:
            if isinstance(element, SatinColumn):
                self.flip(element)
