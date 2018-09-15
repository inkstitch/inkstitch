import sys

from .base import InkstitchExtension
from ..i18n import _
from ..elements import SatinColumn


class SplitSatin(InkstitchExtension):
    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more satin columns to split."))
            return

        for satin in self.elements:
            if isinstance(satin, SatinColumn):
                command = satin.get_command("satin_split_point")
                split_point = command.target_point
                command.symbol.getparent().remove(command.symbol)
                command.connector.getparent().remove(command.connector)

                new_satins = satin.split(split_point)
                parent = satin.node.getparent()
                index = parent.index(satin.node)
                parent.remove(satin.node)
                for new_satin in new_satins:
                    parent.insert(index, new_satin.node)
                    index += 1
