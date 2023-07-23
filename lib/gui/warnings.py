# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ..i18n import _


class WarningPanel(wx.Panel):
    """A wx.Panel for to display warnings.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.warning = wx.StaticText(self)
        self.warning.SetLabel(_("An internal error occurred while rendering the stitch plan:"))
        self.warning.SetForegroundColour(wx.Colour(255, 25, 25))
        self.main_sizer.Add(self.warning, 1, wx.LEFT | wx.BOTTOM | wx.EXPAND, 10)

        tc_style = wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL | wx.HSCROLL | wx.TE_RICH2
        self.warning_text = wx.TextCtrl(self, size=(300, 100), style=tc_style)
        font = self.warning_text.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        self.warning_text.SetFont(font)
        self.main_sizer.Add(self.warning_text, 3, wx.LEFT | wx.BOTTOM | wx.EXPAND, 10)

        self.SetSizerAndFit(self.main_sizer)
        self.Layout()

    def set_warning_text(self, text):
        self.warning_text.SetValue(text)

    def clear(self):
        self.warning_text.SetValue("")
