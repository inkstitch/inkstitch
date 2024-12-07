# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ..i18n import _


class RequestUpdateFrame(wx.Frame):

    def __init__(self, title, **kwargs):
        super().__init__(None, title=title)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.cancel_hook = kwargs.pop('on_cancel', None)

        main_panel = wx.Panel(self, wx.ID_ANY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        help_text = wx.StaticText(
            main_panel,
            wx.ID_ANY,
            _("Unversioned Ink/Stitch SVG file detected.\n\n"
              "* If you opened an old design file, please update.\n"
              "* If you copy pasted objects into an empty file, please cancel."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)

        cancel_button = wx.Button(main_panel, wx.ID_CANCEL, "")
        ok_button = wx.Button(main_panel, wx.ID_OK, _("Update"))

        button_sizer.Add((0, 0), 1, 0, 0)
        button_sizer.Add(cancel_button, 0, wx.RIGHT, 10)
        button_sizer.Add(ok_button, 0, 0, 0)

        main_sizer.Add(help_text, 0, wx.ALL, 10)
        main_sizer.Add(button_sizer, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        main_panel.SetSizer(main_sizer)
        self.SetSizeHints(main_sizer.CalcMin())

        main_sizer.Fit(self)
        self.Layout()
        self.SetSizeHints(main_sizer.CalcMin())

        self.Bind(wx.EVT_BUTTON, self.cancel_button_clicked, cancel_button)
        self.Bind(wx.EVT_BUTTON, self.update_button_clicked, ok_button)
        self.Bind(wx.EVT_CLOSE, self.cancel)

    def cancel(self, event=None):
        if self.cancel_hook:
            self.cancel_hook()
        self.Destroy()

    def cancel_button_clicked(self, event):
        self.cancel()

    def update_button_clicked(self, event):
        self.Destroy()


class RequestUpdate:
    def __init__(self):
        self.cancelled = False

        app = wx.App()
        frame = RequestUpdateFrame(
            title="Ink/Stitch",
            on_cancel=self.cancel_update,
        )
        frame.Show()
        app.MainLoop()

    def cancel_update(self):
        self.cancelled = True
