# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ..i18n import _
from ..threads import ThreadCatalog
from ..utils.settings import global_settings


class ApplyPaletteFrame(wx.Frame):

    def __init__(self, title, **kwargs):
        super().__init__(None, title=title)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.apply_hook = kwargs.pop('on_apply', None)

        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.palettes = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.palettes, _("Palettes"))

        palette_sizer = wx.BoxSizer(wx.VERTICAL)
        palette_text = wx.StaticText(self.palettes, -1, _("Select color palette"))
        self.palette_list = wx.Choice(self.palettes, choices=ThreadCatalog().palette_names())
        last_selected_pallete = self.palette_list.FindString(global_settings['last_applied_palette'])
        self.palette_list.SetSelection(last_selected_pallete)

        palette_sizer.Add(palette_text, 0, wx.ALL | wx.EXPAND, 10)
        palette_sizer.Add(self.palette_list, 0, wx.ALL | wx.EXPAND, 10)

        button_sizer = wx.StdDialogButtonSizer()
        palette_sizer.Add(button_sizer, 1, wx.BOTTOM | wx.EXPAND, 10)
        button_sizer.Add((0, 0), 1, 0, 0)
        self.apply_button = wx.Button(self.palettes, wx.ID_ANY, _("Apply"))
        button_sizer.Add(self.apply_button, 0, wx.RIGHT, 10)
        self.Bind(wx.EVT_BUTTON, self.apply_button_clicked, self.apply_button)

        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("This extension applies nearest colors from chosen color palette to the elements in this document."),
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
            _("https://inkstitch.org/docs/thread-color/#apply-palette"),
            _("https://inkstitch.org/docs/thread-color/#apply-palette")
        )
        help_sizer.Add(self.website_link, 0, wx.ALL, 8)

        self.help.SetSizer(help_sizer)
        self.palettes.SetSizer(palette_sizer)
        self.main_panel.SetSizer(notebook_sizer)

        self.SetSizeHints(notebook_sizer.CalcMin())

        self.Layout()

    def apply_button_clicked(self, event):
        if self.apply_hook:
            self.apply_hook()
        self.Destroy()


class ApplyPaletteApp(wx.App):
    def __init__(self):
        self.palette = None

        app = wx.App()
        self.frame = ApplyPaletteFrame(
            title="Ink/Stitch",
            on_apply=self.set_palette,
        )
        self.frame.Show()
        app.MainLoop()

    def set_palette(self):
        if self.frame.palette_list.GetSelection() == -1:
            return
        self.palette = self.frame.palette_list.GetString(self.frame.palette_list.GetSelection())
        global_settings['last_applied_palette'] = self.palette
