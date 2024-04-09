# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import Clone
from ..i18n import _
from .base import InkstitchExtension


class UnlinkClone(InkstitchExtension):
    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more clones to unlink."))
            return

        clones_to_remove = []
        for element in self.elements:
            if isinstance(element, Clone):
                element.resolve_clone()
                clones_to_remove.append(element.node)

        for clone in clones_to_remove:
            clone.getparent().remove(clone)
