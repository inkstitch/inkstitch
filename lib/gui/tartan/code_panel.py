# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ...i18n import _


class CodePanel(wx.Panel):
    def __init__(self, parent, panel):
        self.panel = panel
        wx.Panel.__init__(self, parent)
        code_sizer = wx.BoxSizer(wx.VERTICAL)
        load_palette_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tt_unit_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.threadcount_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.threadcount_text.Bind(wx.EVT_TEXT, self.set_tt_unit_status)
        code_sizer.Add(self.threadcount_text, 1, wx.EXPAND | wx.ALL, 10)

        self.tt_unit_label = wx.StaticText(self, label=_("1 Tartan thread equals (mm)"))
        self.tt_unit_spin = wx.SpinCtrlDouble(self, min=0.01, max=50, initial=0.2, inc=0.1, style=wx.SP_WRAP)
        self.tt_unit_spin.SetDigits(2)
        tt_unit_sizer.Add(self.tt_unit_label, 0, wx.CENTER | wx.ALL, 10)
        tt_unit_sizer.Add(self.tt_unit_spin, 0, wx.ALL, 10)
        self.tt_unit_label.SetToolTip(_("Used only for Threadcount code (The Scottish Register of Tartans)"))
        self.tt_unit_spin.SetToolTip(_("Used only for Threadcount code (The Scottish Register of Tartans)"))

        code_sizer.Add(tt_unit_sizer, 0, wx.ALL, 10)

        load_button = wx.Button(self, label="Apply Code")
        load_button.Bind(wx.EVT_BUTTON, self._load_palette_code)
        load_palette_sizer.Add(load_button, 0, wx.ALL, 10)

        code_sizer.Add(load_palette_sizer, 0, wx.ALL, 10)

        self.SetSizer(code_sizer)

    def _load_palette_code(self, event):
        self.panel.palette.tt_unit = self.tt_unit_spin.GetValue()
        self.panel.update_from_code()
        self.panel.settings['palette'] = self.threadcount_text.GetValue()

    def set_tt_unit_status(self, event):
        # we always want to convert the width into mm
        # when threadcount code is given we have to enable the threadcount unit field
        # so they can define the mm-width of one tartan thread
        threadcount_text = self.threadcount_text.GetValue()
        if '(' in threadcount_text and 'Threadcount' not in threadcount_text:
            # depending on how much of the mailed text is copied into the code field,
            # we may have brackets in there (1997). So let's also check for "threadcount"
            self.tt_unit_label.Enable(False)
            self.tt_unit_spin.Enable(False)
        else:
            self.tt_unit_label.Enable(True)
            self.tt_unit_spin.Enable(True)
