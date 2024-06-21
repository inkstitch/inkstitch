# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import wx
import wx.adv

from ..i18n import _
from ..utils import get_resource_dir
from ..utils.version import get_inkstitch_version, get_inkstitch_license


class AboutFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, wx.ID_ANY, _("About Ink/Stitch"), *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        notebook = wx.Notebook(main_panel, wx.ID_ANY)
        notebook_sizer.Add(notebook, 1, wx.EXPAND, 0)

        info_panel = wx.Panel(notebook, wx.ID_ANY)
        notebook.AddPage(info_panel, _("About"))

        info_sizer = wx.BoxSizer(wx.VERTICAL)

        inkstitch_logo = wx.Image(
            os.path.join(
                get_resource_dir('icons'),
                "inkstitch_colour_logo.png"
            )
        ).ConvertToBitmap()

        inkstitch_logo = wx.StaticBitmap(info_panel, -1, inkstitch_logo, (10, 5), (inkstitch_logo.GetWidth(), inkstitch_logo.GetHeight()))

        inkstitch_version = get_inkstitch_version()
        inkstitch_version = wx.StaticText(info_panel, label=inkstitch_version)
        version_font = wx.Font().Bold()
        inkstitch_version.SetFont(version_font)

        inkstitch_description = _("An open-source machine embroidery design platform based on Inkscape.")
        inkstitch_description = wx.StaticText(info_panel, label=inkstitch_description)

        inkstitch_link = wx.adv.HyperlinkCtrl(
            info_panel,
            wx.ID_ANY,
            _("https://inkstitch.org"),
            _("https://inkstitch.org")
        )
        inkstitch_link.Bind(wx.adv.EVT_HYPERLINK, self.on_link_clicked)

        info_sizer.Add(inkstitch_logo, 1, wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER, 20)
        info_sizer.Add(inkstitch_version, 0, wx.RIGHT | wx.LEFT, 20)
        info_sizer.Add(inkstitch_description, 0, wx.RIGHT | wx.LEFT, 20)
        info_sizer.Add(0, 10, 0)
        info_sizer.Add(inkstitch_link, 0, wx.RIGHT | wx.LEFT, 20)
        info_sizer.Add(0, 40, 0)

        license_panel = wx.Panel(notebook, wx.ID_ANY)
        notebook.AddPage(license_panel, _("License"))

        license_sizer = wx.BoxSizer(wx.VERTICAL)
        license_text = get_inkstitch_license()
        license_text = wx.TextCtrl(
            license_panel,
            size=(600, 500),
            value=license_text,
            style=wx.TE_MULTILINE | wx.SUNKEN_BORDER | wx.TE_READONLY | wx.HSCROLL
        )
        license_sizer.Add(license_text, 0, wx.EXPAND | wx.ALL, 8)

        info_panel.SetSizer(info_sizer)
        license_panel.SetSizer(license_sizer)
        main_panel.SetSizer(notebook_sizer)

        self.SetSizeHints(notebook_sizer.CalcMin())

        self.Layout()

    def on_link_clicked(self, event):
        event.Skip()


class AboutInkstitchApp(wx.App):
    def __init__(self):
        super().__init__()

    def OnInit(self):
        self.frame = AboutFrame()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
