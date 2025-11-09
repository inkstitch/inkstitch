# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import Any, List, Optional, Union

from inkex import Boolean, Group, Vector2d, errormsg

from ..elements import Stroke
from ..i18n import _
from ..stitches.auto_run import autorun
from ..svg.svg import delete_empty_groups
from .commands import CommandsExtension


class AutoRun(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)

        self.arg_parser.add_argument("-b", "--break_up", dest="break_up", type=Boolean, default=True)
        self.arg_parser.add_argument("-p", "--preserve_order", dest="preserve_order", type=Boolean, default=False)
        self.arg_parser.add_argument("-o", "--options", dest="options", type=str, default="")
        self.arg_parser.add_argument("-i", "--info", dest="help", type=str, default="")

    def effect(self) -> None:
        elements = self.check_selection()
        if not elements:
            return

        starting_point = self.get_starting_point()
        ending_point = self.get_ending_point()

        break_up = self.options.break_up

        group = self._create_group()
        autorun(elements, self.options.preserve_order, break_up, starting_point, ending_point, self.options.trim, group)
        delete_empty_groups(self.svg.selection)

    def get_starting_point(self) -> Optional[Vector2d]:
        return self.get_command_point("autoroute_start")

    def get_ending_point(self) -> Optional[Vector2d]:
        return self.get_command_point("autoroute_end")

    def get_command_point(self, command_type: str) -> Optional[Vector2d]:
        command = None
        for stroke in self.elements:
            command = stroke.get_command(command_type)
            # return the first occurence directly
            if command:
                return command.target_point
        return None

    def check_selection(self) -> List[Union[Stroke, Any]]:
        if not self.svg.selection:
            # L10N auto-route running stitch columns extension
            errormsg(_("Please select one or more stroke elements."))

        self.get_elements()
        elements = [element for element in self.elements if isinstance(element, Stroke)]
        if len(elements) == 0:
            errormsg(_("Please select at least one stroke element."))

        return elements

    def _create_group(self):
        if self.options.preserve_order:
            return None
        node = self.svg.selection.rendering_order()[-1]
        parent = node.getparent()
        index = parent.index(node) + 1
        group = Group()
        group.label = _("Auto-Route")
        parent.insert(index, group)
        return group
