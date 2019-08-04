import inkex
import wx
from ..i18n import _

from .base import InkstitchExtension


class ResetFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.selected = kwargs.pop('elements', None)
        self.svg = kwargs.pop('svg', None)
        wx.Frame.__init__(self, *args, **kwargs)

        panel = wx.Panel(self)

        # Text
        text = (_('Choose specified information that should be removed from your SVG document.'))
        static_text = wx.StaticText(panel, label=text)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        static_text.SetFont(font)

        # Options
        static_line0 = wx.StaticLine(panel)
        self.del_all = wx.CheckBox(panel, label=_("Remove settings from whole document"))
        self.del_all.SetToolTip(_('Remove specified settings not only from selection, but from the whole document.'))
        static_line1 = wx.StaticLine(panel)
        self.del_params = wx.CheckBox(panel, label=_("Remove Params"))
        self.del_commands = wx.CheckBox(panel, label=_("Remove Commands"))
        self.del_print = wx.CheckBox(panel, label=_("Document Print Settings"))
        static_line2 = wx.StaticLine(panel)

        # Buttons
        apply_button = wx.Button(panel, wx.ID_ANY, _("Apply"))
        cancel_button = wx.Button(panel, wx.ID_CANCEL, _("Cancel"))

        # Layout
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer.Add(static_text, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)

        options_sizer = wx.BoxSizer(wx.VERTICAL)
        options_sizer.Add(static_line0, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(self.del_all, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(static_line1, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(self.del_params, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(self.del_commands, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(self.del_print, proportion=0, flag=wx.EXPAND, border=5)
        options_sizer.Add(static_line2, proportion=0, flag=wx.EXPAND, border=5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(apply_button, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        buttons_sizer.Add(cancel_button, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(options_sizer, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(buttons_sizer, proportion=1, flag=wx.ALIGN_RIGHT | wx.ALIGN_RIGHT, border=5)

        panel.SetSizerAndFit(sizer)
        panel.Layout()

        # Events
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_clicked)
        apply_button.Bind(wx.EVT_BUTTON, self.apply_button_clicked)

        # Presets
        if not self.selected:
            self.del_all.SetValue(True)
            self.del_all.Disable()

        self.del_params.SetValue(True)

    def cancel_button_clicked(self, event):
        self.Destroy()

    def apply_button_clicked(self, event):
        self.reset_embroidery_settings()
        self.Destroy()

    def reset_embroidery_settings(self):
        self.del_all = self.del_all.GetValue()

        if self.del_print.GetValue():
            self.remove_print_settings()

        if self.del_params.GetValue():
            self.remove_params()

        if self.del_commands.GetValue():
            self.remove_commands()

    def find_elements(self, xpath):
        elements = self.svg.xpath(xpath, namespaces=inkex.NSS)
        return elements

    def remove_elements(self, xpath):
        elements = self.find_elements(xpath)
        for element in elements:
            self.remove_element(element)

    def remove_element(self, element):
        element.getparent().remove(element)

    def remove_embroider_attributes(self, element):
        for attrib in element.attrib:
            if attrib.startswith('embroider_'):
                del element.attrib[attrib]

    def remove_print_settings(self):
        print_settings = "svg:metadata//*"
        print_settings = self.find_elements(print_settings)
        for print_setting in print_settings:
            if print_setting.prefix == "inkstitch":
                self.remove_element(print_setting)

    def remove_params(self):
        if self.del_all:
            xpath = ".//svg:path"
            path_elements = self.find_elements(xpath)
            for element in path_elements:
                self.remove_embroider_attributes(element)
        else:
            for node in self.selected:
                xpath = ".//*[@id='%s']" % node
                element = self.find_elements(xpath)[0]
                self.remove_embroider_attributes(element)

    def remove_commands(self):
        if self.del_all:
            commands = ".//*[starts-with(@inkscape:label, 'Ink/Stitch Command:')]"
            self.remove_elements(commands)

            symbols = ".//*[starts-with(@id, 'inkstitch_')]"
            self.remove_elements(symbols)
        else:
            for node in self.selected:
                xpath = (".//svg:path[@inkscape:connection-start='#%(id)s' or @inkscape:connection-end='#%(id)s']/parent::*" %
                         dict(id=node))
                commands = self.remove_elements(xpath)


class ResetEmbroiderySettings(InkstitchExtension):
    def effect(self):
        app = wx.App()
        reset_frame = ResetFrame(parent=None, title=_("Reset embroidery settings"), svg=self.document.getroot(), elements=self.selected)
        reset_frame.Show()
        app.MainLoop()
