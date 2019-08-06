import inkex

from .base import InkstitchExtension


class ResetEmbroiderySettings(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.OptionParser.add_option("-p", "--del_params", dest="del_params", type="inkbool", default=True)
        self.OptionParser.add_option("-c", "--del_commands", dest="del_commands", type="inkbool", default=False)
        self.OptionParser.add_option("-d", "--del_print", dest="del_print", type="inkbool", default=False)

    def effect(self):
        if self.options.del_params:
            self.remove_params()
        if self.options.del_commands:
            self.remove_commands()
        if self.options.del_print:
            self.remove_print_settings()

    def remove_print_settings(self):
        print_settings = "svg:metadata//*"
        print_settings = self.find_elements(print_settings)
        for print_setting in print_settings:
            if print_setting.prefix == "inkstitch":
                self.remove_element(print_setting)

    def remove_params(self):
        if not self.selected:
            xpath = ".//svg:path"
            elements = self.find_elements(xpath)
            self.remove_embroider_attributes(elements)
        else:
            for node in self.selected:
                elements = self.get_selected_elements(node)
                self.remove_embroider_attributes(elements)

    def remove_commands(self):
        if not self.selected:
            commands = ".//*[starts-with(@inkscape:label, 'Ink/Stitch Command:')]"
            self.remove_elements(commands)

            symbols = ".//*[starts-with(@id, 'inkstitch_')]"
            self.remove_elements(symbols)
        else:
            for node in self.selected:
                elements = self.get_selected_elements(node)
                for element in elements:
                    xpath = (".//svg:path[@inkscape:connection-start='#%(id)s' or @inkscape:connection-end='#%(id)s']/parent::*" %
                             dict(id=element.get('id')))
                    commands = self.remove_elements(xpath)

    def get_selected_elements(self, element_id):
        xpath = ".//svg:path[@id='%s']" % element_id
        elements = self.find_elements(xpath)
        if not elements:
            xpath = ".//svg:g[@id='%s']//svg:path" % element_id
            elements = self.find_elements(xpath)
        return elements

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

    def remove_embroider_attributes(self, elements):
        for element in elements:
            for attrib in element.attrib:
                if attrib.startswith('embroider_'):
                    del element.attrib[attrib]
