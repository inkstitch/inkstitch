# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Boolean, ShapeElement

from ..commands import OBJECT_COMMANDS, find_commands, is_command_symbol
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
        elements = self.get_elements()
        self.remove_inkstitch_attributes(elements, self.options.del_params)

    def remove_all_commands(self):
        xpath = ".//svg:g[starts-with(@id,'command_group')]"
        groups = find_elements(self.svg, xpath)
        for group in groups:
            group.delete()

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
                group.delete()

        # remove standalone commands and ungrouped object commands
        standalone_commands = ".//svg:use[starts-with(@xlink:href, '#inkstitch_{command}')]"
        self.remove_elements(standalone_commands)

        # let's remove the symbols (defs), we won't need them in the document
        symbols = f".//*[starts-with(@id, 'inkstitch_{command}')]"
        self.remove_elements(symbols)

    def remove_commands_from_selection(self, elements, del_option):
        for element in elements:
            if is_command_symbol(element) and (del_option in element.get('xlink:href') or del_option == 'all'):
                group = element.getparent()
                if group.getparent() is not None:
                    if group.get_id().startswith("command_group"):
                        group.delete()
                    else:
                        element.delete()
                continue
            for command in find_commands(element):
                if del_option in ('all', command.command):
                    group = command.connector.getparent()
                    group.delete()

    def remove_commands(self):
        elements = self.get_elements()
        del_option = self.options.del_commands

        # trim and stop params are percepted as commands,
        # so let's remove them as well
        if del_option in ['all', 'trim']:
            self.remove_inkstitch_attributes(elements, 'trim_after')
        elif del_option in ['all', 'stop']:
            self.remove_inkstitch_attributes(elements, 'stop_after')

        if self.svg.selection:
            self.remove_commands_from_selection(elements, del_option)
        elif self.options.del_commands == "all":
            self.remove_all_commands()
        else:
            self.remove_specific_commands(self.options.del_commands)

    def get_elements(self):
        if self.svg.selection:
            return self.svg.selection.get(ShapeElement)
        else:
            return self.svg.descendants().filter(ShapeElement)

    def remove_elements(self, xpath):
        elements = find_elements(self.svg, xpath)
        for element in elements:
            self.remove_element(element)

    def remove_element(self, element):
        element.delete()

    def remove_inkstitch_attributes(self, elements, param_to_remove):
        for element in elements:
            for attrib in element.attrib:
                if attrib.startswith(NSS['inkstitch'], 1):
                    if param_to_remove == 'all' or attrib.endswith(param_to_remove):
                        del element.attrib[attrib]
