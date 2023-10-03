#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv

from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS


class GenerateSwatchesFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.extension = kwargs.pop("extension")
        self.choices = kwargs.pop("choices")
        wx.Frame.__init__(self, *args, **kwargs)
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Generate Swatches"), *args, **kwargs)

        self.panel = wx.Panel(self, wx.ID_ANY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self.panel, wx.ID_ANY)
        main_sizer.Add(self.notebook, 0, wx.ALL | wx.EXPAND, 10)

        self.options = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.options, _("Options"))

        options_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_main_sizer = wx.FlexGridSizer(6, 2, 10, 10)
        options_sizer.Add(grid_main_sizer, 0, wx.ALL, 10)

        param_label = wx.StaticText(self.options, wx.ID_ANY, _("Param"))
        grid_main_sizer.Add(param_label, 0, 0, 0)

        self.param = wx.ComboBox(self.options, wx.ID_ANY, choices=[])
        for choice in self.choices:
            self.param.Append(choice.name, choice)
        self.param.SetSelection(0)
        grid_main_sizer.Add(self.param, 0, 0, 0)

        start_value_label = wx.StaticText(self.options, wx.ID_ANY, _("Start Value"))
        grid_main_sizer.Add(start_value_label, 0, 0, 0)

        self.start_value = wx.SpinCtrlDouble(self.options, wx.ID_ANY, initial=2.5, min=0.0, max=500.0)
        self.start_value.SetDigits(2)
        grid_main_sizer.Add(self.start_value, 0, 0, 0)

        step_label = wx.StaticText(self.options, wx.ID_ANY, _("Increase by"))
        grid_main_sizer.Add(step_label, 0, 0, 0)

        self.step = wx.SpinCtrlDouble(self.options, wx.ID_ANY, initial=0.5, min=0.01, max=500.0)
        self.step.SetDigits(2)
        grid_main_sizer.Add(self.step, 0, 0, 0)

        cols_label = wx.StaticText(self.options, wx.ID_ANY, _("Columns"))
        grid_main_sizer.Add(cols_label, 0, 0, 0)

        self.columns = wx.SpinCtrl(self.options, wx.ID_ANY, "0", min=1, max=100)
        grid_main_sizer.Add(self.columns, 0, 0, 0)

        rows_label = wx.StaticText(self.options, wx.ID_ANY, _("Rows"))
        grid_main_sizer.Add(rows_label, 0, 0, 0)

        self.rows = wx.SpinCtrl(self.options, wx.ID_ANY, "0", min=1, max=100)
        grid_main_sizer.Add(self.rows, 0, 0, 0)

        spacing_label = wx.StaticText(self.options, wx.ID_ANY, _("Spacing"))
        grid_main_sizer.Add(spacing_label, 0, 0, 0)

        self.spacing = wx.SpinCtrlDouble(self.options, wx.ID_ANY, initial=5, min=0.0, max=100.0)
        self.spacing.SetDigits(2)
        grid_main_sizer.Add(self.spacing, 0, 0, 0)

        self.info = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.info, _("Help"))

        info_sizer = wx.BoxSizer(wx.VERTICAL)

        info_text_label = wx.StaticText(
            self.info,
            wx.ID_ANY,
            _("This extension generates test swatches from a selection.\n"
              "Test swatches help to find best stitch settings for your design.\n"
              "Sew them out with the same thread and fabric as the final designs."),
            style=wx.ALIGN_LEFT
        )
        info_text_label.Wrap(500)
        info_sizer.Add(info_text_label, 0, wx.ALL, 8)

        info_sizer.Add((20, 20), 0, 0, 0)

        more_info_label = wx.StaticText(self.info, wx.ID_ANY, _("Get more information on our website"))
        info_sizer.Add(more_info_label, 0, wx.ALL, 8)

        self.help_link = wx.adv.HyperlinkCtrl(
            self.info,
            wx.ID_ANY,
            "https://inkstitch.org/docs/edit/#generate-test-swatches-from-selection",
            "https://inkstitch.org/docs/edit/#generate-test-swatches-from-selection",
            style=wx.adv.HL_ALIGN_CENTRE
        )
        info_sizer.Add(self.help_link, 0, 0, 0)

        button_sizer = wx.StdDialogButtonSizer()
        main_sizer.Add(button_sizer, 1, wx.BOTTOM | wx.EXPAND, 10)

        button_sizer.Add((0, 0), 1, 0, 0)

        self.apply_button = wx.Button(self.panel, wx.ID_ANY, _("Apply"))
        button_sizer.Add(self.apply_button, 0, wx.RIGHT, 10)

        self.options.SetSizer(options_sizer)
        self.info.SetSizer(info_sizer)
        self.panel.SetSizer(main_sizer)

        main_sizer.Fit(self)
        self.Layout()
        self.SetSizeHints(main_sizer.CalcMin())

        self.param.Bind(wx.EVT_TEXT, self.on_text_input)
        self.Bind(wx.EVT_BUTTON, self.apply_button_clicked, self.apply_button)

    def on_text_input(self, event):
        # this will allow us to catch manual text input, but
        # we only want to catch it when we actually create the swatches
        pass

    def apply_button_clicked(self, event):
        self.apply()
        self.Destroy()

    def apply(self):
        num_cols = self.columns.GetValue()
        num_rows = self.rows.GetValue()
        spacing = self.spacing.GetValue()

        start_value = self.start_value.GetValue()
        step = self.step.GetValue()

        choice_names = [choice.name for choice in self.choices]
        if self.param.GetValue() not in choice_names:
            # catch manual text input
            param = self.param.GetValue()
            if param.startswith("inkstitch:"):
                param = param[10:]
        else:
            param = self.choices[self.param.GetSelection()].id

        for element in self.extension.svg.selection:
            dimensions = element.bounding_box()
            param_value = start_value
            for rows in range(0, num_rows):
                for cols in range(0, num_cols):
                    new_element = element.duplicate()
                    translate_x = cols * dimensions.width + cols * spacing
                    translate_y = rows * dimensions.height + rows * spacing
                    new_element.transform.add_translate((translate_x, translate_y))
                    if new_element.TAG == "g":
                        for embroidery_element in new_element.iterdescendants(EMBROIDERABLE_TAGS):
                            # Since this won't effect functionality, we can simply ignore the fact
                            # that this will also set the value to patterns, guide lines etc.
                            self._set_param(embroidery_element, param, param_value)
                    else:
                        self._set_param(new_element, param, param_value)
                    param_value += step
            # remove old element
            element.getparent().remove(element)

    def _set_param(self, element, param, value):
        element.set(f'inkstitch:{ param }', value)


class GenerateSwatchesApp(wx.App):
    def __init__(self, extension, choices):
        self.extension = extension
        self.choices = choices
        super().__init__()

    def OnInit(self):
        self.frame = GenerateSwatchesFrame(extension=self.extension, choices=self.choices)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
