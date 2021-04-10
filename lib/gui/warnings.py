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

        self.warning_box = wx.StaticBox(self, wx.ID_ANY)

        self.warning = wx.StaticText(self)
        self.warning.SetLabel(_("Cannot load simulator.\nClose Params to get full error message."))
        self.warning.SetForegroundColour(wx.Colour(255, 25, 25))

        warning_sizer = wx.StaticBoxSizer(self.warning_box, wx.HORIZONTAL)
        warning_sizer.Add(self.warning, 1, wx.LEFT | wx.BOTTOM | wx.EXPAND, 10)

        self.SetSizerAndFit(warning_sizer)
        self.Layout()
