from math import sqrt

import wx

from ..i18n import _
from ..utils.settings import global_settings


class CrossStitchHelperFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings")
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Ink/Stitch - Cross stitch"), *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.widgets_and_panels()
        self.apply_global_settings()
        self.update()
        self.Show()

    def apply_global_settings(self):
        self.x_only_checkbox.SetValue(global_settings['square'])
        self.box_x.SetValue(global_settings['cross_helper_box_x'])
        self.box_y.SetValue(global_settings['cross_helper_box_y'])
        self.apply_to_element.SetValue(global_settings['cross_helper_update_elements'])
        self.pixelize.SetValue(global_settings['cross_helper_pixelize'])
        self.coverage.SetValue(global_settings['cross_helper_coverage'])
        self.nodes.SetValue(global_settings['cross_helper_nodes'])
        self.setup_grid.SetValue(global_settings['cross_helper_set_grid'])
        self.grid_color.SetColour(global_settings['cross_helper_grid_color'])
        self.remove_grids.SetValue(global_settings['cross_helper_remove_grids'])

    def widgets_and_panels(self):
        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings_panel = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.settings_panel, _("Settings"))

        # settings
        settings_main_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_settings_sizer = wx.BoxSizer(wx.VERTICAL)
        apply_settings_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(4, 2, 15, 20)
        grid_sizer.AddGrowableCol(1)

        grid_settings_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid Settings"))
        font = wx.Font(wx.FontInfo().Bold())
        grid_settings_label.SetFont(font)

        x_only_label = wx.StaticText(self.settings_panel, label=_("Square grid"))
        self.x_only_checkbox = wx.CheckBox(self.settings_panel)
        self.x_only_checkbox.SetValue(True)
        self.x_only_checkbox.Bind(wx.EVT_CHECKBOX, self.update)

        box_x_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid horizontal spacing (mm)"))
        self.box_x = wx.SpinCtrlDouble(self.settings_panel, value='3', min=0.5, max=100, initial=3, inc=0.1)
        self.box_x.SetDigits(2)
        self.box_x.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        self.box_y_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid vertical spacing (mm)"))
        self.box_y = wx.SpinCtrlDouble(self.settings_panel, value='3', min=0.5, max=100, initial=3, inc=0.1)
        self.box_y.SetDigits(2)
        self.box_y.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        result_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Stitch_length:"))
        self.result = wx.TextCtrl(self.settings_panel, wx.ID_ANY, style=wx.TE_READONLY)
        self.result.Enable(False)

        grid_sizer.AddMany([
            (x_only_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.x_only_checkbox, 1, wx.EXPAND),
            (box_x_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.box_x, 1, wx.EXPAND),
            (self.box_y_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.box_y, 1, wx.EXPAND),
            (result_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.result, 1, wx.EXPAND)
        ])

        # Apply grid to
        apply_to_settings = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Apply grid settings"))
        apply_to_settings.SetFont(font)

        apply_to_grid_sizer = wx.FlexGridSizer(7, 2, 15, 20)
        apply_to_grid_sizer.AddGrowableCol(1)

        apply_to_element_label = wx.StaticText(self.settings_panel, label=_("Selected fill elements (params)"))
        self.apply_to_element = wx.CheckBox(self.settings_panel)

        pixelize_label = wx.StaticText(self.settings_panel, label=_("Fill element outline (pixelize)"))
        self.pixelize = wx.CheckBox(self.settings_panel)
        self.pixelize.Bind(wx.EVT_CHECKBOX, self.update)

        coverage_label_text = "     " + _("Fill coverage (%)")
        self.coverage_label = wx.StaticText(self.settings_panel, label=coverage_label_text)
        self.coverage = wx.SpinCtrl(self.settings_panel, wx.ID_ANY, min=0, max=100, initial=50)

        node_label_text = "     " + _("Add nodes (grid width distance)")
        self.nodes_label = wx.StaticText(self.settings_panel, label=node_label_text)
        self.nodes = wx.CheckBox(self.settings_panel)

        setup_grid_label = wx.StaticText(self.settings_panel, label=_("Page grid"))
        self.setup_grid = wx.CheckBox(self.settings_panel)
        self.setup_grid.Bind(wx.EVT_CHECKBOX, self.update)

        grid_color_label_text = "     " + _("Grid color")
        self.grid_color_label = wx.StaticText(self.settings_panel, label=grid_color_label_text)
        self.grid_color = wx.ColourPickerCtrl(self.settings_panel, colour=wx.Colour('#00d9e5'))

        remove_grids_label_text = "     " + _("Remove previous page grids")
        self.remove_grids_label = wx.StaticText(self.settings_panel, label=remove_grids_label_text)
        self.remove_grids = wx.CheckBox(self.settings_panel)

        apply_to_grid_sizer.AddMany([
            (apply_to_element_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.apply_to_element, 1, wx.EXPAND),
            (pixelize_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.pixelize, 1, wx.EXPAND),
            (self.coverage_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.coverage, 1, wx.EXPAND),
            (self.nodes_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.nodes, 1, wx.EXPAND),
            (setup_grid_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.setup_grid, 1, wx.EXPAND),
            (self.grid_color_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.grid_color, 1, wx.EXPAND),
            (self.remove_grids_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.remove_grids, 1, wx.EXPAND)
        ])

        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.settings_panel, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self.settings_panel, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        grid_settings_sizer.Add(grid_settings_label, 0, wx.EXPAND | wx.ALL, 5)
        grid_settings_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        apply_settings_sizer.Add(apply_to_settings, 0, wx.EXPAND | wx.ALL, 5)
        apply_settings_sizer.Add(apply_to_grid_sizer, 1, wx.EXPAND | wx.ALL, 10)

        settings_options_sizer.Add(grid_settings_sizer, 1, wx.ALL, 20)
        settings_options_sizer.Add(wx.StaticLine(self.settings_panel, 2, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 20)
        settings_options_sizer.Add(apply_settings_sizer, 1, wx.ALL, 20)

        settings_main_sizer.Add(settings_options_sizer, 1, wx.ALL, 10)
        settings_main_sizer.Add(wx.StaticLine(self.settings_panel, 2, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 20)
        settings_main_sizer.Add(apply_sizer, 1, wx.ALIGN_RIGHT | wx.ALL, 10)

        # help
        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("This extension helps to generate cross stitches in Ink/Stitch. It can:\n\n"
              "* Calculate stitch length for given grid spacing values\n"
              "* Apply cross stitch parameters to selected fill elements.\n"
              "* Pixelize outlines of selected fill elements.\n"
              "* Apply spacing values to page grid."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        help_sizer.Add(help_text, 0, wx.ALL, 8)

        help_sizer.Add((20, 20), 0, 0, 0)

        website_info = wx.StaticText(self.help, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.ALL, 8)

        self.website_link = wx.adv.HyperlinkCtrl(
            self.help,
            wx.ID_ANY,
            _("https://inkstitch.org/docs/tools-fill/#cross-stitch"),
            _("https://inkstitch.org/docs/tools-fill/#cross-stitch")
        )
        help_sizer.Add(self.website_link, 0, wx.ALL, 8)

        self.settings_panel.SetSizer(settings_main_sizer)
        self.help.SetSizer(help_sizer)

        self.main_panel.SetSizerAndFit(notebook_sizer)
        self.Fit()
        self.Layout()

    def update(self, event=None):
        y_on = not self.x_only_checkbox.GetValue()
        self.box_y.Enable(y_on)
        self.box_y_label.Enable(y_on)

        box_x = self.box_x.GetValue()
        box_y = self.box_y.GetValue()
        if not y_on:
            box_y = box_x
            self.box_y.SetValue(box_y)
        result = sqrt(pow(box_x, 2) + pow(box_y, 2))
        self.result.SetValue("{:.2f}".format(result))

        self.coverage_label.Enable(self.pixelize.GetValue())
        self.coverage.Enable(self.pixelize.GetValue())
        self.nodes_label.Enable(self.pixelize.GetValue())
        self.nodes.Enable(self.pixelize.GetValue())

        self.grid_color_label.Enable(self.setup_grid.GetValue())
        self.grid_color.Enable(self.setup_grid.GetValue())
        self.remove_grids_label.Enable(self.setup_grid.GetValue())
        self.remove_grids.Enable(self.setup_grid.GetValue())

    def apply(self, event):
        self.settings['applied'] = True
        self.settings['box_x'] = self.box_x.GetValue()
        self.settings['box_y'] = self.box_y.GetValue()
        self.settings['update_elements'] = self.apply_to_element.GetValue()
        self.settings['pixelize'] = self.pixelize.GetValue()
        self.settings['coverage'] = self.coverage.GetValue()
        self.settings['nodes'] = self.nodes.GetValue()
        self.settings['set_grid'] = self.setup_grid.GetValue()
        self.settings['grid_color'] = self.grid_color.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.settings['remove_grids'] = self.remove_grids.GetValue()

        global_settings['square'] = self.x_only_checkbox.GetValue()
        global_settings['cross_helper_box_x'] = self.box_x.GetValue()
        global_settings['cross_helper_box_y'] = self.box_y.GetValue()
        global_settings['cross_helper_update_elements'] = self.apply_to_element.GetValue()
        global_settings['cross_helper_pixelize'] = self.pixelize.GetValue()
        global_settings['cross_helper_coverage'] = self.coverage.GetValue()
        global_settings['cross_helper_nodes'] = self.nodes.GetValue()
        global_settings['cross_helper_set_grid'] = self.setup_grid.GetValue()
        global_settings['cross_helper_grid_color'] = self.grid_color.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        global_settings['cross_helper_remove_grids'] = self.remove_grids.GetValue()

        self.GetTopLevelParent().Close()
        return

    def cancel(self, event=None):
        self.Destroy()


class CrossStitchHelperApp(wx.App):
    def __init__(self, settings):
        self.settings = settings
        super().__init__()

    def OnInit(self):
        frame = CrossStitchHelperFrame(settings=self.settings)
        self.SetTopWindow(frame)
        frame.Show()
        return True
