from inkex import NSS, Boolean

from ..commands import find_commands
from ..svg.svg import find_elements
from .base import InkstitchExtension


class RemoveEmbroiderySettings(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-p", "--del_params", dest="del_params", type=Boolean, default=True)
        self.arg_parser.add_argument("-c", "--del_commands", dest="del_commands", type=Boolean, default=False)
        self.arg_parser.add_argument("-d", "--del_print", dest="del_print", type=Boolean, default=False)

    def effect(self):
        self.svg = self.document.getroot()

        if self.options.del_params:
            self.remove_params()
        if self.options.del_commands:
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
        if not self.svg.selected:
            xpath = ".//svg:path"
            elements = find_elements(self.svg, xpath)
            self.remove_inkstitch_attributes(elements)
        else:
            for node in self.svg.selected:
                elements = self.get_selected_elements(node)
                self.remove_inkstitch_attributes(elements)

    def remove_commands(self):
        if not self.svg.selected:
            # we are not able to grab commands by a specific id
            # so let's move through every object instead and see if it has a command
            xpath = ".//svg:path|.//svg:circle|.//svg:rect|.//svg:ellipse"
            elements = find_elements(self.svg, xpath)
        else:
            elements = []
            for node in self.svg.selected:
                elements.extend(self.get_selected_elements(node))

        if elements:
            for element in elements:
                for command in find_commands(element):
                    group = command.connector.getparent()
                    group.getparent().remove(group)

        if not self.svg.selected:
            # remove standalone commands
            standalone_commands = ".//svg:use[starts-with(@xlink:href, '#inkstitch_')]"
            self.remove_elements(standalone_commands)

            # let's remove the symbols (defs), we won't need them in the document
            symbols = ".//*[starts-with(@id, 'inkstitch_')]"
            self.remove_elements(symbols)

    def get_selected_elements(self, element_id):
        xpath = ".//svg:g[@id='%(id)s']//svg:path|.//svg:g[@id='%(id)s']//svg:use" % dict(id=element_id)
        elements = find_elements(self.svg, xpath)
        if not elements:
            xpath = ".//*[@id='%s']" % element_id
            elements = find_elements(self.svg, xpath)
        return elements

    def remove_elements(self, xpath):
        elements = find_elements(self.svg, xpath)
        for element in elements:
            self.remove_element(element)

    def remove_element(self, element):
        element.getparent().remove(element)

    def remove_inkstitch_attributes(self, elements):
        for element in elements:
            for attrib in element.attrib:
                if attrib.startswith(NSS['inkstitch'], 1):
                    del element.attrib[attrib]
