# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ..i18n import _


class AbortMessageFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message")
        url = kwargs.pop("url")
        wx.Frame.__init__(self, None, wx.ID_ANY, "Ink/Stitch", *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        main_panel = wx.Panel(self, wx.ID_ANY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            main_panel,
            wx.ID_ANY,
            message,
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        main_sizer.Add(help_text, 0, wx.ALL, 10)

        if url is not None:
            main_sizer.Add((10, 10), 0, 0, 0)
            main_sizer.Add(wx.StaticLine(main_panel), 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

            website_info = wx.StaticText(main_panel, wx.ID_ANY, _("More information on our website:"))
            main_sizer.Add(website_info, 0, wx.ALL, 10)

            website_link = wx.adv.HyperlinkCtrl(
                main_panel,
                wx.ID_ANY,
                url,
                url
            )
            main_sizer.Add(website_link, 0, wx.ALL, 10)
        main_sizer.Add((20, 20), 0, 0, 0)

        main_panel.SetSizer(main_sizer)
        self.SetSizeHints(main_sizer.CalcMin())

        self.Layout()


class AbortMessageApp(wx.App):
    def __init__(self, message, url=None):
        self.message = message
        self.url = url
        super().__init__()

    def OnInit(self):
        self.frame = AbortMessageFrame(message=self.message, url=self.url)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
