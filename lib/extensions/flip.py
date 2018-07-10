import sys
import inkex
import cubicsuperpath
from shapely import geometry as shgeo

from .base import InkstitchExtension
from ..i18n import _
from ..elements import SatinColumn

class Flip(InkstitchExtension):
    def subpath_to_linestring(self, subpath):
        return shgeo.LineString()

    def flip(self, satin):
        csp = satin.path

        if len(csp) > 1:
            flattened = satin.flatten(csp)

            # find the rails (the two longest paths) and swap them
            indices = range(len(csp))
            indices.sort(key=lambda i: shgeo.LineString(flattened[i]).length, reverse=True)

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
