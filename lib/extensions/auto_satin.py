import inkex
import sys

from .commands import CommandsExtension
from ..i18n import _
from ..elements import SatinColumn
from ..stitches.auto_satin import auto_satin
from ..svg import get_correction_transform
from ..svg.tags import SVG_GROUP_TAG


class AutoSatin(CommandsExtension):
    COMMANDS = ["trim"]

    def get_starting_point(self):
        return self.get_point("satin_start")

    def get_ending_point(self):
        return self.get_point("satin_end")

    def get_point(self, command_type):
        command = None
        for satin in self.elements:
            this_command = satin.get_command(command_type)
            if command is not None and this_command:
                inkex.errormsg(_("Please ensure that at most one start and end command is attached to the selected satin columns."))
                sys.exit(0)
            elif this_command:
                command = this_command

        if command is not None:
            return command.target_point

    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more satin columns to cut."))
            return

        for element in self.elements:
            if not isinstance(element, SatinColumn):
                inkex.errormsg(_("Please only select satin columns."))
                return

        first = self.elements[0].node
        parent = first.getparent()
        insert_index = parent.index(first)
        group = inkex.etree.Element(SVG_GROUP_TAG, {
            "transform": get_correction_transform(parent, child=True)
        })
        parent.insert(insert_index, group)

        # The ordering is careful here.  Some of the original satins may have
        # been used unmodified.  That's why we remove all of the original
        # satins _first_ before adding new_nodes back into the SVG.
        starting_point = self.get_starting_point()
        ending_point = self.get_ending_point()
        new_elements, trim_indices = auto_satin(self.elements, starting_point, ending_point)

        for element in self.elements:
            for command in element.commands:
                command.connector.getparent().remove(command.connector)
                command.use.getparent().remove(command.use)
            element.node.getparent().remove(element.node)

        for element in new_elements:
            element.node.set("id", self.uniqueId("autosatin"))
            group.append(element.node)

        if self.options.trim and trim_indices:
            self.ensure_symbol("trim")
            for i in trim_indices:
                self.add_commands(new_elements[i], ["trim"])
