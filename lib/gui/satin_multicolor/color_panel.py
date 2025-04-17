# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _


class ColorPanel(wx.Panel):
    def __init__(self, parent, color, *args, **kwargs):
        self.panel = parent
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)

        colorsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.position = wx.Button(self, label='↑', style=wx.BU_EXACTFIT)
        self.position.SetToolTip(_("Click to move color up."))
        self.position.Bind(wx.EVT_BUTTON, self.panel._move_color_up)

        self.colorpicker = wx.ColourPickerCtrl(self, colour=wx.Colour(color))
        self.colorpicker.SetToolTip(_("Select color"))
        self.colorpicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.panel._update)

        self.color_width = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.color_width.SetDigits(2)
        self.color_width.SetToolTip(_("Monochrome width. Can be changed individually when equidistance is disabled."))
        self.color_width.Bind(wx.EVT_SPINCTRLDOUBLE, self.panel._update)
        self.color_width.Bind(wx.EVT_TEXT_ENTER, self.panel._update)

        self.color_margin_right = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.color_margin_right.SetDigits(2)
        self.color_margin_right.SetToolTip(_("Margin right (bicolor section). Can be changed individually when equidistance is disabled."))
        self.color_margin_right.Bind(wx.EVT_SPINCTRLDOUBLE, self.panel._update)
        self.color_margin_right.Bind(wx.EVT_TEXT_ENTER, self.panel._update)

        self.remove_button = wx.Button(self, label='X')
        self.remove_button.SetToolTip(_("Remove color"))
        self.remove_button.Bind(wx.EVT_BUTTON, self.panel._remove_color)

        colorsizer.Add(self.position, 0, wx.CENTER | wx.RIGHT | wx.TOP | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
        colorsizer.Add(self.colorpicker, 0, wx.RIGHT | wx.TOP, 5)
        colorsizer.Add(self.color_width, 1, wx.RIGHT | wx.TOP, 5)
        colorsizer.Add(self.color_margin_right, 1, wx.RIGHT | wx.TOP | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
        colorsizer.Add(self.remove_button, 0, wx.CENTER | wx.TOP, 5)

        self.SetSizer(colorsizer)
