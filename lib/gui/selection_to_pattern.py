import wx

from ..i18n import _


class SelectionToPatternFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings")
        wx.Frame.__init__(self, None, wx.ID_ANY, "Ink/Stitch", *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.widgets_and_panels()
        self.Show()

    def widgets_and_panels(self):
        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings_panel = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.settings_panel, _("Settings"))

        # settings
        settings_sizer = wx.FlexGridSizer(3, 2, 15, 20)
        settings_sizer.AddGrowableCol(1)

        interval = wx.StaticText(self.settings_panel, label=_("Interval"))
        self.interval = wx.TextCtrl(self.settings_panel, value="1")
        if len(self.settings['interval']):
            self.interval.SetValue(self.settings['interval'][0])

        start_offset = wx.StaticText(self.settings_panel, label=_("Start offset"))
        self.start_offset = wx.SpinCtrl(self.settings_panel, min=0, max=100, initial=0)
        if len(self.settings['start_offset']):
            self.start_offset.SetValue(self.settings['start_offset'][0])

        remove = wx.StaticText(self.settings_panel, label=_("Remove pattern marker"))
        self.remove = wx.CheckBox(self.settings_panel)
        self.remove.SetValue(False)

        settings_sizer.AddMany([
            (interval, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10),
            (self.interval, 1, wx.EXPAND | wx.RIGHT, 10),
            (start_offset, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10),
            (self.start_offset, 1, wx.EXPAND | wx.RIGHT, 10),
            (remove, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 10),
            (self.remove, 1, wx.EXPAND | wx.RIGHT | wx.TOP, 10),
        ])

        # help
        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("Patterns add or remove nodes from embroidery elements.\n"
              "Targeted embroidery elements have to be in the same group with this pattern.\n\n"
              "- Stroke patterns add nodes\n"
              "  A predefined interval allows stroke patterns to skip intersection points\n"
              "- Fill patterns remove nodes"),
            style=wx.ALIGN_LEFT,
            size=(600, 230)
        )
        help_sizer.Add(help_text, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 20)

        help_sizer.AddSpacer(5)

        website_info = wx.StaticText(self.help, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.TOP | wx.LEFT | wx.RIGHT, 20)

        self.website_link = wx.adv.HyperlinkCtrl(
            self.help,
            wx.ID_ANY,
            _("https://inkstitch.org/docs/stitches/patterns/"),
            _("https://inkstitch.org/docs/stitches/patterns/")
        )
        help_sizer.Add(self.website_link, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, 20)

        # apply or cancel
        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.main_panel, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self.main_panel, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.AddStretchSpacer(prop=1)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 10)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        notebook_sizer.Add(apply_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # set sizers
        self.settings_panel.SetSizer(settings_sizer)
        self.help.SetSizer(help_sizer)

        self.main_panel.SetSizerAndFit(notebook_sizer)
        self.Fit()
        self.Layout()

    def apply(self, event):
        self.settings['apply'] = True
        self.settings['interval'] = self.interval.GetValue()
        self.settings['start_offset'] = self.start_offset.GetValue()
        self.settings['remove'] = self.remove.GetValue()

        self.GetTopLevelParent().Close()
        return

    def cancel(self, event=None):
        self.Destroy()


class SelectionToPatternApp(wx.App):
    def __init__(self, settings):
        self.settings = settings
        super().__init__()

    def OnInit(self):
        frame = SelectionToPatternFrame(settings=self.settings)
        self.SetTopWindow(frame)
        frame.Show()
        return True
