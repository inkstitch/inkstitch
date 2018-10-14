import inkex
import sys

from .commands import CommandsExtension
from ..i18n import _
from ..elements import SatinColumn
from ..stitches.auto_satin import auto_satin
from ..svg import get_correction_transform
from ..svg.tags import SVG_GROUP_TAG, INKSCAPE_LABEL


class AutoSatin(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)

        self.OptionParser.add_option("-p", "--preserve_order", dest="preserve_order", type="inkbool", default=False)

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
        if not self.check_selection():
            return

        group = self.create_group()
        new_elements, trim_indices = self.auto_satin()

        # The ordering is careful here.  Some of the original satins may have
        # been used unmodified.  That's why we remove all of the original
        # satins _first_ before adding new_elements back into the SVG.
        self.remove_original_satins()
        self.add_elements(group, new_elements)

        self.add_trims(new_elements, trim_indices)

    def check_selection(self):
        if not self.get_elements():
            return

        if not self.selected:
            # L10N auto-route satin columns extension
            inkex.errormsg(_("Please select one or more satin columns."))
            return False

        for element in self.elements:
            if not isinstance(element, SatinColumn):
                inkex.errormsg(_("Please only select satin columns."))
                return False

        return True

    def create_group(self):
        first = self.elements[0].node
        parent = first.getparent()
        insert_index = parent.index(first)
        group = inkex.etree.Element(SVG_GROUP_TAG, {
            "transform": get_correction_transform(parent, child=True)
        })
        parent.insert(insert_index, group)

        return group

    def auto_satin(self):
        starting_point = self.get_starting_point()
        ending_point = self.get_ending_point()
        return auto_satin(self.elements, self.options.preserve_order, starting_point, ending_point)

    def remove_original_satins(self):
        for element in self.elements:
            for command in element.commands:
                command.connector.getparent().remove(command.connector)
                command.use.getparent().remove(command.use)
            element.node.getparent().remove(element.node)

    def add_elements(self, group, new_elements):
        for i, element in enumerate(new_elements):
            if isinstance(element, SatinColumn):
                element.node.set("id", self.uniqueId("autosatin"))

                # L10N Label for a satin column created by Auto-Route Satin Columns extension
                element.node.set(INKSCAPE_LABEL, _("AutoSatin %d") % (i + 1))
            else:
                element.node.set("id", self.uniqueId("autosatinrun"))

                # L10N Label for running stitch (underpathing) created by Auto-Route Satin Columns extension
                element.node.set(INKSCAPE_LABEL, _("AutoSatin Running Stitch %d") % (i + 1))

            group.append(element.node)

    def add_trims(self, new_elements, trim_indices):
        if self.options.trim and trim_indices:
            self.ensure_symbol("trim")
            for i in trim_indices:
                self.add_commands(new_elements[i], ["trim"])
