# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _
from ...utils.param import ParamOption


class EmbroideryPanel(wx.Panel):
    def __init__(self, parent, panel):
        self.panel = panel
        wx.Panel.__init__(self, parent)

        self.embroidery_sizer = wx.BoxSizer(wx.VERTICAL)
        self.embroidery_element_sizer = wx.FlexGridSizer(6, 2, 5, 5)
        self.embroidery_element_sizer.AddGrowableCol(1)
        self.svg_elements_sizer = wx.FlexGridSizer(6, 2, 5, 5)
        self.svg_elements_sizer.AddGrowableCol(1)
        self.common_settings_sizer = wx.FlexGridSizer(1, 2, 5, 5)
        self.common_settings_sizer.AddGrowableCol(1)

        help_text = wx.StaticText(self, -1, _("Embroidery settings can be refined in the params dialog."))

        # Method
        self.output_method = wx.ComboBox(self, choices=[], style=wx.CB_READONLY)
        for choice in embroider_choices:
            self.output_method.Append(choice.name, choice)
        self.output_method.SetSelection(0)
        self.output_method.Bind(wx.EVT_COMBOBOX, self.update_output_method)

        # Embroidery Element Params
        stitch_angle_label = wx.StaticText(self, label=_("Angle of lines of stitches"))
        stitch_angle_label.SetToolTip(_('Relative to the tartan stripe direction.'))
        self.stitch_angle = wx.SpinCtrlDouble(self, min=-90, max=90, initial=-45, style=wx.SP_WRAP)
        self.stitch_angle.SetDigits(2)
        self.stitch_angle.SetIncrement(1)
        self.stitch_angle.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_param_change("tartan_angle", event))

        rows_per_thread_label = wx.StaticText(self, label=_("Rows per tartan thread"))
        self.rows_per_thread = wx.SpinCtrl(self, min=1, max=50, initial=2, style=wx.SP_WRAP)
        lines_text = _("Consecutive rows of the same color")
        rows_per_thread_label.SetToolTip(lines_text)
        self.rows_per_thread.SetToolTip(lines_text)
        self.rows_per_thread.Bind(wx.EVT_SPINCTRL, lambda event: self.on_param_change("rows_per_thread", event))

        row_spacing_label = wx.StaticText(self, label=_("Row spacing (mm)"))
        self.row_spacing = wx.SpinCtrlDouble(self, min=0.01, max=500, initial=0.25, style=wx.SP_WRAP)
        self.row_spacing.SetDigits(2)
        self.row_spacing.SetIncrement(0.01)
        self.row_spacing.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_param_change("row_spacing_mm", event))

        underlay_label = wx.StaticText(self, label=_("Underlay"))
        self.underlay = wx.CheckBox(self)
        self.underlay.Bind(wx.EVT_CHECKBOX, lambda event: self.on_param_change("fill_underlay", event))

        herringbone_label = wx.StaticText(self, label=_("Herringbone width (mm)"))
        self.herringbone = wx.SpinCtrlDouble(self, min=0, max=500, initial=0, style=wx.SP_WRAP)
        self.herringbone.SetDigits(2)
        self.herringbone.SetIncrement(1)
        self.herringbone.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_param_change("herringbone_width_mm", event))

        bean_stitch_repeats_label = wx.StaticText(self, label=_("Bean stitch repeats"))
        self.bean_stitch_repeats = wx.TextCtrl(self)
        self.bean_stitch_repeats.Bind(wx.EVT_TEXT, lambda event: self.on_param_change("bean_stitch_repeats", event))

        # SVG Output Settings
        stitch_type_label = wx.StaticText(self, label=_("Stitch type"))
        self.stitch_type = wx.ComboBox(self, choices=[], style=wx.CB_READONLY)
        for choice in stitch_type_choices:
            self.stitch_type.Append(choice.name, choice)
        self.stitch_type.SetSelection(0)
        self.stitch_type.Bind(wx.EVT_COMBOBOX, self.on_change_stitch_type)

        svg_row_spacing_label = wx.StaticText(self, label=_("Row spacing"))
        self.svg_row_spacing = wx.SpinCtrlDouble(self, min=0.01, max=500, initial=1, style=wx.SP_WRAP)
        self.svg_row_spacing.SetDigits(2)
        self.row_spacing.SetIncrement(0.01)
        self.svg_row_spacing.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("row_spacing", event))

        angle_warp_label = wx.StaticText(self, label=_("Stitch angle (warp)"))
        self.angle_warp = wx.SpinCtrl(self, min=-90, max=90, initial=0, style=wx.SP_WRAP)
        self.angle_warp.Bind(wx.EVT_SPINCTRL, lambda event: self.on_change("angle_warp", event))

        angle_weft_label = wx.StaticText(self, label=_("Stitch angle (weft)"))
        self.angle_weft = wx.SpinCtrl(self, min=-90, max=90, initial=90, style=wx.SP_WRAP)
        self.angle_weft.Bind(wx.EVT_SPINCTRL, lambda event: self.on_change("angle_weft", event))

        min_stripe_width_label = wx.StaticText(self, label=_("Minimum stripe width for fills"))
        self.min_stripe_width = wx.SpinCtrlDouble(self, min=0, max=100, initial=1, style=wx.SP_WRAP)
        self.min_stripe_width.SetDigits(2)
        self.row_spacing.SetIncrement(0.1)
        min_width_text = _("Stripes smaller than this will be stitched as a running stitch")
        min_stripe_width_label.SetToolTip(min_width_text)
        self.min_stripe_width.SetToolTip(min_width_text)
        self.min_stripe_width.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("min_stripe_width", event))

        svg_bean_stitch_repeats_label = wx.StaticText(self, label=_("Bean stitch repeats"))
        self.svg_bean_stitch_repeats = wx.SpinCtrl(self, min=0, max=10, initial=0, style=wx.SP_WRAP)
        self.svg_bean_stitch_repeats.Bind(wx.EVT_SPINCTRL, lambda event: self.on_change("bean_stitch_repeats", event))

        # Add to sizers
        self.embroidery_element_sizer.Add(stitch_angle_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.stitch_angle, 0, wx.EXPAND, 0)
        self.embroidery_element_sizer.Add(rows_per_thread_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.rows_per_thread, 0, wx.EXPAND, 0)
        self.embroidery_element_sizer.Add(row_spacing_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.row_spacing, 0, wx.EXPAND, 0)
        self.embroidery_element_sizer.Add(herringbone_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.herringbone, 0, wx.EXPAND, 0)
        self.embroidery_element_sizer.Add(underlay_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.underlay, 0, wx.EXPAND, 0)
        self.embroidery_element_sizer.Add(bean_stitch_repeats_label, 0, wx.ALIGN_CENTRE, 0)
        self.embroidery_element_sizer.Add(self.bean_stitch_repeats, 0, wx.EXPAND, 0)

        self.svg_elements_sizer.Add(stitch_type_label, 0, wx.ALIGN_CENTRE, 0)
        self.svg_elements_sizer.Add(self.stitch_type, 0, wx.EXPAND, 0)
        self.svg_elements_sizer.Add(svg_row_spacing_label, 0, wx.ALIGN_CENTRE, 0)
        self.svg_elements_sizer.Add(self.svg_row_spacing, 0, wx.EXPAND, 0)
        self.svg_elements_sizer.Add(angle_warp_label, 0, wx.ALIGN_CENTRE, 0)
        self.svg_elements_sizer.Add(self.angle_warp, 0, wx.EXPAND, 0)
        self.svg_elements_sizer.Add(angle_weft_label, 0, wx.ALIGN_CENTRE, 0)
        self.svg_elements_sizer.Add(self.angle_weft, 0, wx.EXPAND, 0)
        self.svg_elements_sizer.Add(svg_bean_stitch_repeats_label, 0, wx.ALIGN_CENTRE, 0)
        self.svg_elements_sizer.Add(self.svg_bean_stitch_repeats, 0, wx.EXPAND, 0)

        self.common_settings_sizer.Add(min_stripe_width_label, 0, wx.ALIGN_CENTRE, 0)
        self.common_settings_sizer.Add(self.min_stripe_width, 0, wx.EXPAND, 0)

        self.embroidery_sizer.Add(self.output_method, 0, wx.EXPAND | wx.ALL, 10)
        self.embroidery_sizer.Add(self.embroidery_element_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.embroidery_sizer.Add(self.svg_elements_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.embroidery_sizer.Add(self.common_settings_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.embroidery_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.embroidery_sizer.Add(help_text, 0, wx.EXPAND | wx.ALL, 10)
        self.embroidery_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)

        self.embroidery_sizer.Hide(self.svg_elements_sizer)
        self.SetSizer(self.embroidery_sizer)

    def update_output_method(self, event):
        output = self.output_method.GetClientData(self.output_method.GetSelection()).id
        if output == "svg":
            self.embroidery_sizer.Show(self.svg_elements_sizer)
            self.embroidery_sizer.Hide(self.embroidery_element_sizer)
            for element in self.panel.elements:
                element.pop('inkstitch:fill_method')
        else:
            self.embroidery_sizer.Show(self.embroidery_element_sizer)
            self.embroidery_sizer.Hide(self.svg_elements_sizer)
            for element in self.panel.elements:
                element.set('inkstitch:fill_method', 'tartan_fill')
        self.panel.settings['output'] = output
        self.Layout()
        self.panel.update_preview()

    def set_output(self, choice):
        for option in embroider_choices:
            if option.id == choice:
                self.output_method.SetValue(option.name)
                self.update_output_method(None)
                break

    def on_change(self, attribute, event):
        self.panel.settings[attribute] = event.GetEventObject().GetValue()
        self.panel.update_preview()

    def on_change_stitch_type(self, event):
        stitch_type = self.stitch_type.GetClientData(self.stitch_type.GetSelection()).id
        self.panel.settings['stitch_type'] = stitch_type
        self.panel.update_preview()

    def on_param_change(self, attribute, event):
        for element in self.panel.elements:
            element.set(f'inkstitch:{attribute}', str(event.GetEventObject().GetValue()))
        self.panel.update_preview()

    def set_stitch_type(self, choice):
        for option in stitch_type_choices:
            if option.id == choice:
                self.stitch_type.SetValue(option.name)
                break


embroider_choices = [
    ParamOption("embroidery", _("Embroidery Element")),
    ParamOption("svg", _("SVG Elements"))
]


stitch_type_choices = [
    ParamOption("auto_fill", _("AutoFill")),
    ParamOption("legacy_fill", _("Legacy Fill"))
]
