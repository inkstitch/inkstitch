# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _
from ...utils.settings import global_settings


class SimulatorPreferenceDialog(wx.Dialog):
    """A dialog to set simulator preferences
    """

    def __init__(self, *args, **kwargs):
        super(SimulatorPreferenceDialog, self).__init__(*args, **kwargs)
        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.view_panel = self.GetParent()
        self.drawing_panel = self.view_panel.drawing_panel
        self.control_panel = self.view_panel.control_panel

        self.adaptive_speed_value = global_settings['simulator_adaptive_speed']
        self.line_width_value = global_settings['simulator_line_width']
        self.npp_size_value = global_settings['simulator_npp_size']

        sizer = wx.BoxSizer(wx.VERTICAL)
        settings_sizer = wx.FlexGridSizer(3, 2, 5, 5)
        speed_label = wx.StaticText(self, label=_("Adapt speed to stitch count"))
        self.adaptive_speed = wx.CheckBox(self)
        self.adaptive_speed.SetToolTip(_("When enabled simulation speed adapts itself to the stitch count."))
        self.adaptive_speed.SetValue(self.adaptive_speed_value)
        self.adaptive_speed.Bind(wx.EVT_CHECKBOX, self.on_adaptive_speed_changed)
        line_width_label = wx.StaticText(self, label=_("Line width (mm)"))
        self.line_width = wx.SpinCtrlDouble(self, min=0.03, max=2, initial=0.1, inc=0.01, style=wx.SP_WRAP | wx.SP_ARROW_KEYS)
        self.line_width.SetDigits(2)
        self.line_width.SetValue(self.line_width_value)
        self.line_width.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("simulator_line_width", event))
        npp_size_label = wx.StaticText(self, label=_("Needle penetration point size (mm)"))
        self.npp_size = wx.SpinCtrlDouble(self, min=0.03, max=2, initial=0.5, inc=0.01, style=wx.SP_WRAP | wx.SP_ARROW_KEYS)
        self.npp_size.SetDigits(2)
        self.npp_size.SetValue(self.npp_size_value)
        self.npp_size.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("simulator_npp_size", event))
        settings_sizer.Add(speed_label, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        settings_sizer.Add(self.adaptive_speed, 0, wx.EXPAND | wx.ALL, 10)
        settings_sizer.Add(line_width_label, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        settings_sizer.Add(self.line_width, 0, wx.EXPAND | wx.ALL, 10)
        settings_sizer.Add(npp_size_label, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        settings_sizer.Add(self.npp_size, 0, wx.EXPAND | wx.ALL, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_cancel = wx.Button(self, id=wx.ID_CANCEL, label=_('Cancel'))
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        btn_apply = wx.Button(self, id=wx.ID_OK, label=_('Apply'))
        btn_apply.Bind(wx.EVT_BUTTON, self.on_apply)
        button_sizer.Add(btn_cancel, 0, wx.RIGHT, 10)
        button_sizer.Add(btn_apply, 0, wx.RIGHT, 10)

        sizer.Add(settings_sizer, 1, wx.ALL, 10)
        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def on_change(self, attribute, event):
        global_settings[attribute] = event.EventObject.GetValue()
        if self.drawing_panel.loaded and attribute == 'simulator_line_width':
            self.drawing_panel.update_pen_size()
        self.drawing_panel.Refresh()

    def on_adaptive_speed_changed(self, event=None):
        adaptive_speed = self.adaptive_speed.GetValue()
        global_settings['simulator_adaptive_speed'] = adaptive_speed
        self.control_panel.choose_speed()
        self.control_panel.Refresh()

    def save_settings(self):
        global_settings['simulator_line_width'] = self.line_width.GetValue()
        global_settings['simulator_npp_size'] = self.npp_size.GetValue()

    def on_apply(self, event):
        self.save_settings()
        self.Close()

    def on_cancel(self, event):
        self.save_settings()
        if self.drawing_panel.loaded:
            self.drawing_panel.update_pen_size()
            self.drawing_panel.Refresh()
        self.Close()
