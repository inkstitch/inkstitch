import sys
import inkex
import cubicsuperpath

from .base import InkstitchExtension
from ..i18n import _
from ..elements import SatinColumn

class Flip(InkstitchExtension):
    def flip(self, satin):
        csp = cubicsuperpath.parsePath(satin.node.get("d"))

        if len(csp) > 1:
            # find the rails (the two longest paths) and swap them
            indices = range(len(csp))
            indices.sort(key=lambda i: len(csp[i]), reverse=True)

            first = indices[0]
            second = indices[1]
            csp[first], csp[second] = csp[second], csp[first]

            satin.node.set("d", cubicsuperpath.formatPath(csp))

    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more satin columns to flip."))
            return

        for element in self.elements:
            if isinstance(element, SatinColumn):
                self.flip(element)
