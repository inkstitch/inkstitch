# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

import inkex

from ..elements import SatinColumn, Stroke
from ..i18n import _
from ..stitches.auto_satin import auto_satin
from .commands import CommandsExtension


class AutoSatin(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-p", "--preserve_order", dest="preserve_order", type=inkex.Boolean, default=False)
        self.arg_parser.add_argument("-k", "--keep_originals", dest="keep_originals", type=inkex.Boolean, default=False)

    def get_starting_point(self):
        return self.get_point("autoroute_start")

    def get_ending_point(self):
        return self.get_point("autoroute_end")

    def get_point(self, command_type):
        command = None
        for satin in self.elements:
            this_command = satin.get_command(command_type)
            if command is not None and this_command:
                inkex.errormsg(_("Please ensure that at most one start and end command is attached to the selected satin columns."))
                self.skip_output()
                return None
            elif this_command:
                command = this_command

        if command is not None:
            return command.target_point

    def check_selection(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            # L10N auto-route satin columns extension
            inkex.errormsg(_("Please select one or more satin columns."))
            return False

        satincolumns = [element for element in self.elements if isinstance(element, SatinColumn)]
        if len(satincolumns) == 0:
            inkex.errormsg(_("Please select at least one satin column."))
            return False

        return True

    def _get_parent_and_index(self):
        last_element = self.svg.selection[-1]
        if last_element.TAG == 'g':
            parent = last_element.getparent()
            return parent, parent.index(last_element) + 1
        return None, None

    def effect(self):
        if not self.check_selection():
            return

        starting_point = self.get_starting_point()
        ending_point = self.get_ending_point()

        # Ignore fills and zero length satins
        elements = [element for element in self.elements if (isinstance(element, SatinColumn) and element.center_line.length != 0) or
                    (isinstance(element, Stroke) and element.as_multi_line_string().length != 0)]

        # at this point we possibly removed all the elements, in this case stop here
        if not elements:
            return

        parent, index = self._get_parent_and_index()
        auto_satin(elements, self.options.preserve_order, starting_point, ending_point, self.options.trim, self.options.keep_originals, parent, index)
