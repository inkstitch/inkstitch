# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _


class StripePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        self.panel = parent
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)

        stripesizer = wx.BoxSizer(wx.HORIZONTAL)

        self.position = wx.Button(self, label='↑', style=wx.BU_EXACTFIT)
        self.position.SetToolTip(_("Click to move color up."))
        self.position.Bind(wx.EVT_BUTTON, self.panel._move_stripe_up)

        self.visibility = wx.CheckBox(self, style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.visibility.SetToolTip(_("Checked: stitch this stripe | Minus: spacer for strokes only | Disabled: spacer for fill and stroke"))
        self.visibility.Set3StateValue(1)
        self.visibility.Bind(wx.EVT_CHECKBOX, self.panel._update_stripes_event)

        # hidden label used for linked colors
        # there seems to be no native way to catch the old color setting
        self.colorinfo = wx.StaticText(self, label='black')
        self.colorinfo.Hide()

        self.colorpicker = wx.ColourPickerCtrl(self, colour=wx.Colour('black'))
        self.colorpicker.SetToolTip(_("Select stripe color"))
        self.colorpicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.panel._update_color)

        self.stripe_width = wx.SpinCtrlDouble(self, min=0.0, max=500, initial=5, style=wx.SP_WRAP)
        self.stripe_width.SetDigits(2)
        self.stripe_width.SetToolTip(_("Set stripe width (mm)"))
        self.stripe_width.Bind(wx.EVT_SPINCTRLDOUBLE, self.panel._update_stripes_event)

        self.remove_button = wx.Button(self, label='X')
        self.remove_button.SetToolTip(_("Remove stripe"))
        self.remove_button.Bind(wx.EVT_BUTTON, self.panel._remove_stripe)

        stripesizer.Add(self.position, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.CENTER | wx.RIGHT | wx.TOP, 5)
        stripesizer.Add(self.visibility, 0, wx.CENTER | wx.RIGHT | wx.TOP, 5)
        stripesizer.Add(self.colorinfo, 0, wx.RIGHT | wx.TOP, 5)
        stripesizer.Add(self.colorpicker, 0, wx.RIGHT | wx.TOP, 5)
        stripesizer.Add(self.stripe_width, 1, wx.RIGHT | wx.TOP, 5)
        stripesizer.Add(self.remove_button, 0, wx.CENTER | wx.TOP, 5)

        self.SetSizer(stripesizer)
