# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ..i18n import _


class ElementInfoFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        self.list_items = kwargs.pop("list_items")
        self.index = 0
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Element Info"), *args, **kwargs)

        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.info = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.info, _("Info"))

        info_sizer = wx.BoxSizer(wx.VERTICAL)

        self.info_list = wx.ListCtrl(self.info, wx.ID_ANY, style=wx.BORDER_SUNKEN | wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.info_list.AppendColumn(_("Name"), format=wx.LIST_FORMAT_LEFT)
        self.info_list.AppendColumn(_("Value"), format=wx.LIST_FORMAT_LEFT)
        self._fill_info_list()
        self.info_list.SetColumnWidth(0, -1)
        self.info_list.SetColumnWidth(1, -1)
        info_sizer.Add(self.info_list, 1, wx.ALL | wx.EXPAND, 10)

        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("This extension informs about various parameters of selected stitch elements."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        help_sizer.Add(help_text, 0, wx.ALL, 8)

        help_sizer.Add((20, 20), 0, 0, 0)

        website_info = wx.StaticText(self.help, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.ALL, 8)

        self.website_link = wx.adv.HyperlinkCtrl(self.help, wx.ID_ANY, "https://inkstitch.org/bla", "https://inkstitch.org/troubleshoot#element-info")
        help_sizer.Add(self.website_link, 0, wx.ALL, 8)

        self.help.SetSizer(help_sizer)
        self.info.SetSizer(info_sizer)
        self.main_panel.SetSizer(notebook_sizer)

        self.SetSizeHints(notebook_sizer.CalcMin())

        self.Layout()

    def _fill_info_list(self):
        for item in self.list_items:
            self.info_list.InsertItem(self.index, item.name)
            if item.headline:
                self.info_list.SetItemBackgroundColour(self.index, "black")
                self.info_list.SetItemTextColour(self.index, "white")
            else:
                self.info_list.SetItem(self.index, 1, item.value)
            self.index += 1


class ElementInfoApp(wx.App):
    def __init__(self, list_items):
        self.list_items = list_items
        super().__init__()

    def OnInit(self):
        self.frame = ElementInfoFrame(list_items=self.list_items)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
