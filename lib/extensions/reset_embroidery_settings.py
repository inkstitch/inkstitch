import inkex

from .base import InkstitchExtension


class ResetEmbroiderySettings(InkstitchExtension):
    def effect(self):
        # TODO: Extension does not work for ignored layers/objects
        if not self.get_elements():
            return

        for element in self.elements:
            node = element.node
            for attrib in node.attrib:
                if self.selected:
                    xpath = (".//svg:path[@inkscape:connection-start='#%(id)s' or @inkscape:connection-end='#%(id)s']/parent::*" %
                             dict(id=node.get('id')))
                    commands = self.remove_elements(xpath)
                if attrib.startswith('embroider_'):
                    del node.attrib[attrib]

        # Delete all commands and print information if no object is selected
        if not self.selected:
            commands = ".//*[starts-with(@inkscape:label, 'Ink/Stitch Command:')]"
            self.remove_elements(commands)

            symbols = ".//*[starts-with(@id, 'inkstitch_')]"
            self.remove_elements(symbols)

            print_settings = "svg:metadata//*"
            print_settings = self.find_elements(print_settings)
            for print_setting in print_settings:
                if print_setting.prefix == "inkstitch":
                    self.remove_element(print_setting)

    def find_elements(self, xpath):
        svg = self.document.getroot()
        elements = svg.xpath(xpath, namespaces=inkex.NSS)
        return elements

    def remove_elements(self, xpath):
        elements = self.find_elements(xpath)
        for element in elements:
            self.remove_element(element)

    def remove_element(self, element):
        element.getparent().remove(element)
