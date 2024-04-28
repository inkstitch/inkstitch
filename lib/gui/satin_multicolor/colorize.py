# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from time import time

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...i18n import _


class ColorizePanel(ScrolledPanel):

    def __init__(self, parent, panel):
        self.panel = panel
        ScrolledPanel.__init__(self, parent)

        self.colorize_sizer = wx.BoxSizer(wx.VERTICAL)
        general_settings_sizer = wx.FlexGridSizer(6, 2, 5, 5)
        color_header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.color_sizer = wx.BoxSizer(wx.VERTICAL)

        # general settings
        equististance_label = wx.StaticText(self, label=_("Equidistant colors"))
        equististance_label.SetToolTip(_("Whether colors should be equidistant or have varying widths."))
        self.equististance = wx.CheckBox(self)
        self.equististance.SetValue(True)
        self.equististance.Bind(wx.EVT_CHECKBOX, self._on_update_equidistance)

        self.monochrome_width_label = wx.StaticText(self, label=_("     Monochrome color width"))
        self.monochrome_width_label.SetToolTip(_("Adapt color width here when equidistance is enabled."))
        self.monochrome_width = wx.SpinCtrlDouble(self, min=0, max=100, initial=100, inc=1, style=wx.SP_WRAP)
        self.monochrome_width.SetDigits(2)
        self.monochrome_width.Bind(wx.EVT_SPINCTRLDOUBLE, self._on_update_monochrome_width)

        overflow_left_label = wx.StaticText(self, label=_("Overflow left"))
        self.overflow_left = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP)
        self.overflow_left.SetDigits(2)
        self.overflow_left.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)

        overflow_right_label = wx.StaticText(self, label=_("Overflow right"))
        self.overflow_right = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP)
        self.overflow_right.SetDigits(2)
        self.overflow_right.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)

        pull_compensation_label = wx.StaticText(self, label=_("Pull compensation (mm)"))
        self.pull_compensation = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, inc=0.1, style=wx.SP_WRAP)
        self.pull_compensation.SetDigits(2)
        self.pull_compensation.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)

        seed_label = wx.StaticText(self, label=_("Random seed"))
        self.seed = wx.TextCtrl(self)
        self.seed.SetValue(str(time()))
        self.seed.Bind(wx.EVT_TEXT, self._update)

        general_settings_headline = wx.StaticText(self, label=_("General Settings"))
        general_settings_headline.SetFont(wx.Font().Bold())

        color_settings_headline = wx.StaticText(self, label=_("Colors"))
        color_settings_headline.SetFont(wx.Font().Bold())

        self.total_width = wx.StaticText(self)
        self.total_width.SetToolTip(_("Overflow excluded"))

        self.add_color_button = wx.Button(self, label=_("Add"))
        self.add_color_button.Bind(wx.EVT_BUTTON, self._add_color_event)

        # Add to sizers
        general_settings_sizer.Add(equististance_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.equististance, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.Add(self.monochrome_width_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.monochrome_width, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.Add(overflow_left_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.overflow_left, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.Add(overflow_right_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.overflow_right, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.Add(pull_compensation_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.pull_compensation, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.Add(seed_label, 0, wx.ALL, 10)
        general_settings_sizer.Add(self.seed, 0, wx.ALL | wx.EXPAND, 10)
        general_settings_sizer.AddGrowableCol(1)

        color_header_sizer.Add(color_settings_headline, 0, wx.ALL, 10)
        color_header_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 10)
        color_header_sizer.Add(self.total_width, 0, wx.ALL, 10)

        self.colorize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.colorize_sizer.Add(general_settings_headline, 0, wx.ALL, 10)
        self.colorize_sizer.Add(general_settings_sizer, 0, wx.ALL | wx.EXPAND, 10)
        self.colorize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.colorize_sizer.Add(color_header_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.colorize_sizer.Add(self.color_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.colorize_sizer.Add(self.add_color_button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(self.colorize_sizer)

    def _on_update_monochrome_width(self, event):
        equidistance = self.equististance.GetValue()
        if not equidistance:
            return
        width = self.monochrome_width.GetValue()
        num_colors = len(self.color_sizer.GetChildren())
        margin = (100 - width * num_colors) / max(num_colors - 1, 1)
        self._set_widget_width_value(width, margin)
        self._update()

    def _add_color_event(self, event):
        self.add_color()

    def add_color(self, color='black'):
        colorsizer = wx.BoxSizer(wx.HORIZONTAL)

        position = wx.Button(self, label='↑', style=wx.BU_EXACTFIT)
        position.SetToolTip(_("Click to move color up."))
        position.Bind(wx.EVT_BUTTON, self._move_color_up)

        colorpicker = wx.ColourPickerCtrl(self, colour=wx.Colour(color))
        colorpicker.SetToolTip(_("Select color"))
        colorpicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self._update)

        color_width = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, style=wx.SP_WRAP)
        color_width.SetDigits(2)
        color_width.SetToolTip(_("Monochrome width. Can be changed individually when equidistance is disabled."))
        color_width.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)

        color_margin_right = wx.SpinCtrlDouble(self, min=0, max=100, initial=0, style=wx.SP_WRAP)
        color_margin_right.SetDigits(2)
        color_margin_right.SetToolTip(_("Margin right (bicolor section). Can be changed individually when equidistance is disabled."))
        color_margin_right.Bind(wx.EVT_SPINCTRLDOUBLE, self._update)

        remove_button = wx.Button(self, label='X')
        remove_button.SetToolTip(_("Remove color"))
        remove_button.Bind(wx.EVT_BUTTON, self._remove_color)

        colorsizer.Add(position, 0, wx.CENTER | wx.RIGHT | wx.TOP | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
        colorsizer.Add(colorpicker, 0, wx.RIGHT | wx.TOP, 5)
        colorsizer.Add(color_width, 1, wx.RIGHT | wx.TOP, 5)
        colorsizer.Add(color_margin_right, 1, wx.RIGHT | wx.TOP | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)
        colorsizer.Add(remove_button, 0, wx.CENTER | wx.TOP, 5)

        self.color_sizer.Add(colorsizer, 0, wx.EXPAND | wx.ALL, 10)

        if self.equististance.GetValue():
            color_margin_right.Enable(False)
            color_width.Enable(False)
        else:
            color_margin_right.Enable(True)
            color_width.Enable(True)

        self._update_colors()

        color_margin_right.Show(False)
        if len(self.color_sizer.GetChildren()) > 1:
            self.color_sizer.GetChildren()[-2].GetSizer().GetChildren()[3].GetWindow().Show()

        self._update()

        self.FitInside()
        self.Layout()

    def _move_color_up(self, event):
        color = event.GetEventObject()
        sizer = color.GetContainingSizer()
        main_sizer = self.color_sizer
        for i, item in enumerate(main_sizer.GetChildren()):
            if item.GetSizer() == sizer:
                index = i
                break
        if index == len(main_sizer.GetChildren()) - 1:
            last_sizer = main_sizer.GetChildren()[-2].GetSizer().GetChildren()
            last_sizer[2].GetWindow().Show(False)
            sizer.GetChildren()[2].GetWindow().Show()
        index = max(0, (index - 1))
        if index == 0:
            previous_first = main_sizer.GetChildren()[0].GetSizer().GetChildren()
            previous_first[0].GetWindow().Show()
            sizer.GetChildren()[0].GetWindow().Show(False)

        main_sizer.Detach(sizer)
        main_sizer.Insert(index, sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.FitInside()
        self._update()
        self.Layout()

    def _remove_color(self, event):
        sizer = event.GetEventObject().GetContainingSizer()
        sizer.Clear(True)
        self.color_sizer.Remove(sizer)
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
            inner_sizer = color.GetSizer()
            for color_widget in inner_sizer:
                widget = color_widget.GetWindow()
                if isinstance(widget, wx.SpinCtrlDouble):
                    widget.Enable(status)

    def _set_widget_width_value(self, value, margin=0):
        first = True
        for color in self.color_sizer.GetChildren():
            inner_sizer = color.GetSizer()
            for color_widget in inner_sizer:
                widget = color_widget.GetWindow()
                if first and widget.Label == "↑":
                    inner_sizer.Hide(widget)
                    first = False
                if isinstance(widget, wx.SpinCtrlDouble):
                    widget.SetValue(value)
                    widget.GetNextSibling().SetValue(margin)
                    break

    def get_total_width(self):
        width = 0
        colors = self.color_sizer.GetChildren()
        for color in colors:
            inner_sizer = color.GetSizer()
            for color_widget in inner_sizer:
                widget = color_widget.GetWindow()
                if isinstance(widget, wx.SpinCtrlDouble):
                    width += widget.GetValue()
        last_margin = inner_sizer.GetChildren()[3].GetWindow().GetValue()
        width -= last_margin
        return round(width, 2)

    def _update(self, event=None):
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
