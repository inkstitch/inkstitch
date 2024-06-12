# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _


class SimulatorPreferenceDialog(wx.Dialog):
    """A dialog to set simulator preferences
    """

    def __init__(self, *args, **kwargs):
        super(SimulatorPreferenceDialog, self).__init__(*args, **kwargs)

        self.view_panel = self.GetParent()

        sizer = wx.BoxSizer(wx.VERTICAL)
        settings_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        line_width_label = wx.StaticText(self, label=_("Line width (mm)"))
        self.line_width = wx.SpinCtrlDouble(self, min=0.01, max=2, initial=0.1, inc=0.01, style=wx.SP_WRAP | wx.SP_ARROW_KEYS)
        self.line_width.SetDigits(2)
        self.line_width.SetValue(self.view_panel.line_width)
        npp_size_label = wx.StaticText(self, label=_("Needle penetration point size (mm)"))
        self.npp_size = wx.SpinCtrlDouble(self, min=0.01, max=2, initial=0.5, inc=0.01, style=wx.SP_WRAP | wx.SP_ARROW_KEYS)
        self.npp_size.SetDigits(2)
        self.npp_size.SetValue(self.view_panel.npp_size)
        settings_sizer.Add(line_width_label, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        settings_sizer.Add(self.line_width, 0, wx.EXPAND | wx.ALL, 10)
        settings_sizer.Add(npp_size_label, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        settings_sizer.Add(self.npp_size, 0, wx.EXPAND | wx.ALL, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_cancel = wx.Button(self, label=_('Cancel'))
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        btn_apply = wx.Button(self, id=wx.ID_OK, label=_('Apply'))
        btn_apply.Bind(wx.EVT_BUTTON, self.on_apply)
        button_sizer.Add(btn_cancel, 0, wx.RIGHT, 10)
        button_sizer.Add(btn_apply, 0, wx.RIGHT, 10)

        sizer.Add(settings_sizer)
        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer)

    def on_apply(self, event):
        self.view_panel.line_width = self.line_width.GetValue()
        self.view_panel.npp_size = self.npp_size.GetValue()
        self.Destroy()

    def on_cancel(self, event):
        self.Destroy()
