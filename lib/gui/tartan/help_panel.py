# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _


class HelpPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self,
            wx.ID_ANY,
            _("This extension fills shapes with a tartan (or tartan like) pattern."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        help_sizer.Add(help_text, 0, wx.ALL, 8)

        help_sizer.Add((20, 20), 0, 0, 0)

        website_info = wx.StaticText(self, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.ALL, 8)

        website_link = wx.adv.HyperlinkCtrl(
            self,
            wx.ID_ANY,
            _("https://inkstitch.org/docs/stitches/tartan-fill"),
            _("https://inkstitch.org/docs/stitches/tartan-fill")
        )
        website_link.Bind(wx.adv.EVT_HYPERLINK, self.on_link_clicked)
        help_sizer.Add(website_link, 0, wx.ALL, 8)

        self.SetSizer(help_sizer)

    def on_link_clicked(self, event):
        event.Skip()
