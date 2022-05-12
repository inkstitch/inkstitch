# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import Stroke
from ..i18n import _
from ..stitches.auto_run import autorun
from .commands import CommandsExtension


class AutoRun(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)

        self.arg_parser.add_argument("-b", "--break_up", dest="break_up", type=inkex.Boolean, default=True)
        self.arg_parser.add_argument("-p", "--preserve_order", dest="preserve_order", type=inkex.Boolean, default=False)
        self.arg_parser.add_argument("-o", "--options", dest="options", type=str, default="")
        self.arg_parser.add_argument("-i", "--info", dest="help", type=str, default="")

    def effect(self):
        elements = self.check_selection()
        if not elements:
            return

        starting_point = self.get_starting_point()
        ending_point = self.get_ending_point()

        break_up = self.options.break_up

        autorun(elements, self.options.preserve_order, break_up, starting_point, ending_point, self.options.trim)

    def get_starting_point(self):
        point = self.get_marker_point("marker-start", "autorun_start", 0)
        if not point:
            point = self.get_command_point("satin_start")
        return point

    def get_ending_point(self):
        point = self.get_marker_point("marker-end", "autorun_end", -1)
        if not point:
            point = self.get_command_point("satin_end")
        return point

    def get_command_point(self, command_type):
        command = None
        for stroke in self.elements:
            command = stroke.get_command(command_type)
            # return the first occurence directly
            if command:
                return command.target_point

    def get_marker_point(self, style_key, marker_id, path_position):
        for stroke in self.elements:
            marker = stroke.node.style(style_key)
            if marker is not None:
                stroke_marker_id = marker.get_id()
                if stroke_marker_id == "inkstitch-%s-marker" % marker_id:
                    # return on first occurence
                    return stroke.paths[path_position][path_position]

    def check_selection(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            # L10N auto-route running stitch columns extension
            inkex.errormsg(_("Please select one or more stroke elements."))
            return False

        elements = [element for element in self.elements if isinstance(element, Stroke)]
        if len(elements) == 0:
            inkex.errormsg(_("Please select at least one stroke element."))
            return False

        return elements
