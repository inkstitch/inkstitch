# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Boolean, ShapeElement

from ..commands import OBJECT_COMMANDS, find_commands
from ..svg.svg import find_elements
from .base import InkstitchExtension


class RemoveEmbroiderySettings(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--tabs")
        self.arg_parser.add_argument("-p", "--del_params", dest="del_params", type=str, default=True)
        self.arg_parser.add_argument("-c", "--del_commands", dest="del_commands", type=str, default="none")
        self.arg_parser.add_argument("-d", "--del_print", dest="del_print", type=Boolean, default=False)

    def effect(self):
        self.svg = self.document.getroot()

        if self.options.del_params != 'none':
            self.remove_params()
        if self.options.del_commands != 'none':
            self.remove_commands()
        if self.options.del_print:
            self.remove_print_settings()

    def remove_print_settings(self):
        print_settings = "svg:metadata//*"
        print_settings = find_elements(self.svg, print_settings)
        for print_setting in print_settings:
            if print_setting.prefix == "inkstitch":
                self.remove_element(print_setting)

    def remove_params(self):
        if not self.svg.selection:
            xpath = ".//svg:path|.//svg:circle|.//svg:rect|.//svg:ellipse"
            elements = find_elements(self.svg, xpath)
            self.remove_inkstitch_attributes(elements)
        else:
            elements = self.get_selected_elements()
            self.remove_inkstitch_attributes(elements)

    def remove_all_commands(self):
        xpath = ".//svg:g[starts-with(@id,'command_group')]"
        groups = find_elements(self.svg, xpath)
        for group in groups:
            group.getparent().remove(group)

        # remove standalone commands and ungrouped object commands
        standalone_commands = ".//svg:use[starts-with(@xlink:href, '#inkstitch_')]|.//svg:path[starts-with(@id, 'command_connector')]"
        self.remove_elements(standalone_commands)

        # let's remove the symbols (defs), we won't need them in the document
        symbols = ".//*[starts-with(@id, 'inkstitch_')]"
        self.remove_elements(symbols)

    def remove_specific_commands(self, command):
        # remove object commands
        if command in OBJECT_COMMANDS:
            xlink = f"#inkstitch_{command}"
            xpath = f".//svg:use[starts-with(@xlink:href, '{xlink}')]"
            connectors = find_elements(self.svg, xpath)
            for connector in connectors:
                group = connector.getparent()
                group.getparent().remove(group)

        # remove standalone commands and ungrouped object commands
        standalone_commands = ".//svg:use[starts-with(@xlink:href, '#inkstitch_{command}')]"
        self.remove_elements(standalone_commands)

        # let's remove the symbols (defs), we won't need them in the document
        symbols = f".//*[starts-with(@id, 'inkstitch_{command}')]"
        self.remove_elements(symbols)

    def remove_selected_commands(self):
        elements = self.get_selected_elements()
        for element in elements:
            for command in find_commands(element):
                if self.options.del_commands in ('all', command.command):
                    group = command.connector.getparent()
                    group.getparent().remove(group)

    def remove_commands(self):
        if self.svg.selection:
            self.remove_selected_commands()
        elif self.options.del_commands == "all":
            self.remove_all_commands()
        else:
            self.remove_specific_commands(self.options.del_commands)

    def get_selected_elements(self):
        return self.svg.selection.get(ShapeElement)

    def remove_elements(self, xpath):
        elements = find_elements(self.svg, xpath)
        for element in elements:
            self.remove_element(element)

    def remove_element(self, element):
        element.getparent().remove(element)

    def remove_inkstitch_attributes(self, elements):
        param_to_remove = self.options.del_params
        for element in elements:
            for attrib in element.attrib:
                if attrib.startswith(NSS['inkstitch'], 1):
                    if param_to_remove == 'all' or attrib.endswith(param_to_remove):
                        del element.attrib[attrib]
