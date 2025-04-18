# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from time import time

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...i18n import _
from . import ColorPanel


class ColorizePanel(ScrolledPanel):

    def __init__(self, parent, panel):
        self.panel = panel
        ScrolledPanel.__init__(self, parent)

        self.colorize_sizer = wx.BoxSizer(wx.VERTICAL)
        general_settings_sizer = wx.FlexGridSizer(8, 2, 10, 20)
        color_header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.color_sizer = wx.BoxSizer(wx.VERTICAL)

        # general settings
        general_settings_headline = wx.StaticText(self, label=_("General Settings"))
        general_settings_headline.SetFont(wx.Font().Bold())

        equististance_label = wx.StaticText(self, label=_("Equidistant colors"))
        equististance_label.SetToolTip(_("Whether colors should be equidistant or have varying widths."))
        self.equististance = wx.CheckBox(self)
        self.equististance.SetValue(True)
        self.equististance.Bind(wx.EVT_CHECKBOX, self._on_update_equidistance)

        self.monochrome_width_label = wx.StaticText(self, label=_("Monochrome color width"))
        self.monochrome_width_label.SetToolTip(_("Adapt color width here when equidistance is enabled."))
        self.monochrome_width = wx.SpinCtrlDouble(self, min=0, max=100, initial=100, inc=1, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.monochrome_width.SetDigits(2)
        self.monochrome_width.Bind(wx.EVT_SPINCTRLDOUBLE, self._on_update_monochrome_width)
        self.monochrome_width.Bind(wx.EVT_TEXT_ENTER, self._on_update_monochrome_width)

        overflow_left_label = wx.StaticText(self, label=_("Overflow left"))
        self.overflow_left = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.overflow_left.SetDigits(2)
        self.overflow_left.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)
        self.overflow_left.Bind(wx.EVT_TEXT_ENTER, self._update)

        overflow_right_label = wx.StaticText(self, label=_("Overflow right"))
        self.overflow_right = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.overflow_right.SetDigits(2)
        self.overflow_right.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)
        self.overflow_right.Bind(wx.EVT_TEXT_ENTER, self._update)

        pull_compensation_label = wx.StaticText(self, label=_("Pull compensation (mm)"))
        self.pull_compensation = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP | wx.TE_PROCESS_ENTER)
        self.pull_compensation.SetDigits(2)
        self.pull_compensation.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)
        self.pull_compensation.Bind(wx.EVT_TEXT_ENTER, self._update)

        seed_label = wx.StaticText(self, label=_("Random seed"))
        self.seed = wx.TextCtrl(self)
        self.seed.SetValue(str(time()))
        self.seed.Bind(wx.EVT_TEXT, self._update)

        # embroidery settings
        keep_original_label = wx.StaticText(self, label=_("Keep original satin"))
        self.keep_original = wx.CheckBox(self)
        self.keep_original.SetValue(True)

        adjust_underlay_per_color_label = wx.StaticText(self, label=_("Adjust underlay per color"))
        self.adjust_underlay_per_color = wx.CheckBox(self)
        self.adjust_underlay_per_color.Bind(wx.EVT_CHECKBOX, self._update_underlay)
        equististance_label.SetToolTip(_("When disabled existing underlay is applied only to the first color."))

        # Colors
        color_settings_headline = wx.StaticText(self, label=_("Colors"))
        color_settings_headline.SetFont(wx.Font().Bold())

        self.total_width = wx.StaticText(self)
        self.total_width.SetToolTip(_("Overflow excluded"))

        self.add_color_button = wx.Button(self, label=_("Add"))
        self.add_color_button.Bind(wx.EVT_BUTTON, self._add_color_event)

        # Add to sizers
        general_settings_sizer.Add(equististance_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.equististance, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(self.monochrome_width_label, 0, wx.LEFT, 30)
        general_settings_sizer.Add(self.monochrome_width, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(overflow_left_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.overflow_left, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(overflow_right_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.overflow_right, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(pull_compensation_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.pull_compensation, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(seed_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.seed, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.Add(keep_original_label, 0, wx.TOP, 30)
        general_settings_sizer.Add(self.keep_original, 0, wx.TOP | wx.EXPAND, 30)
        general_settings_sizer.Add(adjust_underlay_per_color_label, 0, wx.ALL, 0)
        general_settings_sizer.Add(self.adjust_underlay_per_color, 0, wx.ALL | wx.EXPAND, 0)
        general_settings_sizer.AddGrowableCol(1)

        color_header_sizer.Add(color_settings_headline, 0, wx.ALL, 10)
        color_header_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 10)
        color_header_sizer.Add(self.total_width, 0, wx.ALL, 10)

        self.colorize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.colorize_sizer.Add(general_settings_headline, 0, wx.ALL, 10)
        self.colorize_sizer.Add(general_settings_sizer, 0, wx.ALL | wx.EXPAND, 20)
        self.colorize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.colorize_sizer.Add(color_header_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.colorize_sizer.Add(self.color_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.colorize_sizer.Add(self.add_color_button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(self.colorize_sizer)

    def _on_update_monochrome_width(self, event):
        equidistance = self.equististance.GetValue()
        if not equidistance:
            return
        self._update(event)
        self._update_colors()

    def _add_color_event(self, event):
        self.add_color()

    def add_color(self, color='black'):
        color_panel = ColorPanel(self, color)
        self.color_sizer.Add(color_panel, 0, wx.EXPAND | wx.ALL, 10)

        if self.equististance.GetValue():
            color_panel.color_margin_right.Enable(False)
            color_panel.color_width.Enable(False)
        else:
            color_panel.color_margin_right.Enable(True)
            color_panel.color_width.Enable(True)

        self._update_colors()

        color_panel.color_margin_right.Show(False)
        if len(self.color_sizer.GetChildren()) > 1:
            self.color_sizer.GetChildren()[-2].GetWindow().color_margin_right.Show()

        self._update()

        self.FitInside()
        self.Layout()

    def _move_color_up(self, event):
        color = event.GetEventObject()

        sizer = color.GetParent()
        main_sizer = self.color_sizer

        for i, item in enumerate(main_sizer.GetChildren()):
            if item.GetWindow() == sizer:
                index = i
                break

        if index == len(main_sizer.GetChildren()) - 1:
            last_sizer = main_sizer.GetChildren()[-2].GetWindow()
            last_sizer.color_margin_right.Show(False)
            sizer.color_margin_right.Show()

        index = max(0, (index - 1))
        if index == 0:
            previous_first = main_sizer.GetChildren()[0].GetWindow()
            previous_first.position.Show()
            sizer.position.Show(False)

        main_sizer.Detach(sizer)
        main_sizer.Insert(index, sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.FitInside()
        self._update()
        self.Layout()

    def _remove_color(self, event):
        panel = event.GetEventObject().GetParent()
        panel.Destroy()
        self.FitInside()

        self._update_colors()
        self._update()

    def _on_update_equidistance(self, event=None):
        if self.equististance.GetValue():
            self.monochrome_width_label.Enable(True)
            self.monochrome_width.Enable(True)
            self._set_widget_status(False)
            self._update_colors()
        else:
            self.monochrome_width_label.Enable(False)
            self.monochrome_width.Enable(False)
            self._set_widget_status(True)
        self._update()

    def _set_widget_status(self, status):
        for color in self.color_sizer.GetChildren():
            color_panel = color.GetWindow()
            color_panel.color_width.Enable(status)
            color_panel.color_margin_right.Enable(status)

    def _set_widget_width_value(self, width, margin=0):
        first = True
        for color in self.color_sizer.GetChildren():
            color_panel = color.GetWindow()
            if first:
                color_panel.position.Hide()
                first = False
            color_panel.color_width.SetValue(width)
            color_panel.color_margin_right.SetValue(margin)

    def get_total_width(self):
        width = 0
        colors = self.color_sizer.GetChildren()
        for color in colors:
            color_panel = color.GetWindow()
            width += color_panel.color_width.GetValue()
            width += color_panel.color_margin_right.GetValue()
        last_margin = color_panel.color_margin_right.GetValue()
        width -= last_margin
        return round(width, 2)

    def _update(self, event=None):
        # Hack primarily for Windows: Make sure that the values of spin controls are updated
        if event is not None and event.EventType == wx.EVT_TEXT_ENTER.typeId:
            try:
                event.EventObject.SetValue(event.String)
            except Exception:
                return

        width = self.get_total_width()
        self.total_width.SetLabel(_("Total width: {width}%").format(width=width))
        if width > 100:
            self.total_width.SetForegroundColour("red")
        else:
            self.total_width.SetForegroundColour(wx.NullColour)
        self.panel.update_preview()

    def _update_colors(self):
        equidistance = self.equististance.GetValue()
        num_colors = len(self.color_sizer.GetChildren())
        if equidistance:
            max_width = 100 / max(1, num_colors)
            monochrome_value = self.monochrome_width.GetValue()
            if monochrome_value > max_width:
                self._set_widget_width_value(max_width)
            else:
                margin = (100 - monochrome_value * num_colors) / max(1, num_colors - 1)
                self._set_widget_width_value(monochrome_value, margin)
            self.monochrome_width.SetMax(max_width)
        self.Refresh()
        self._update()

    def _update_underlay(self, event):
        self.panel.update_preview()
