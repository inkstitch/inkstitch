# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...i18n import _
from . import StripePanel


class CustomizePanel(ScrolledPanel):

    def __init__(self, parent, panel):
        self.panel = panel
        self.mouse_position = None
        ScrolledPanel.__init__(self, parent)

        self.customize_sizer = wx.BoxSizer(wx.VERTICAL)
        general_settings_sizer = wx.BoxSizer(wx.HORIZONTAL)
        positional_settings_sizer = wx.FlexGridSizer(2, 4, 5, 5)
        stripe_header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stripe_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.warp_outer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.weft_outer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.warp_sizer = wx.BoxSizer(wx.VERTICAL)
        self.weft_sizer = wx.BoxSizer(wx.VERTICAL)

        general_settings_headline = wx.StaticText(self, label=_("Pattern Settings"))
        general_settings_headline.SetFont(wx.Font().Bold())
        self.symmetry_checkbox = wx.CheckBox(self, label=_("Symmetrical / reflective sett"))
        self.symmetry_checkbox.SetToolTip(_("Disabled: asymmetrical / repeating sett"))
        self.symmetry_checkbox.Bind(wx.EVT_CHECKBOX, self.update_symmetry)
        self.warp_weft_checkbox = wx.CheckBox(self, label=_("Equal threadcount for warp and weft"))
        self.warp_weft_checkbox.Bind(wx.EVT_CHECKBOX, self._update_warp_weft_event)

        positional_settings_headline = wx.StaticText(self, label=_("Position"))
        positional_settings_headline.SetFont(wx.Font().Bold())
        self.rotate = wx.SpinCtrlDouble(self, min=-180, max=180, initial=0, inc=0.1, style=wx.SP_WRAP)
        self.rotate.SetDigits(2)
        self.rotate.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("rotate", event))
        rotate_label = wx.StaticText(self, label=_("Rotate"))
        self.scale = wx.SpinCtrl(self, min=0, max=1000, initial=100, style=wx.SP_WRAP)
        self.scale.Bind(wx.EVT_SPINCTRL, self.update_scale)
        scale_label = wx.StaticText(self, label=_("Scale (%)"))
        self.offset_x = wx.SpinCtrlDouble(self, min=0, max=500, initial=0, style=wx.SP_WRAP)
        self.offset_x.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("offset_x", event))
        self.offset_x.SetDigits(2)
        offset_x_label = wx.StaticText(self, label=_("Offset X (mm)"))
        self.offset_y = wx.SpinCtrlDouble(self, min=0, max=500, initial=0, style=wx.SP_WRAP)
        self.offset_y.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_change("offset_y", event))
        self.offset_y.SetDigits(2)
        offset_y_label = wx.StaticText(self, label=_("Offset Y (mm)"))

        stripe_settings_headline = wx.StaticText(self, label=_("Stripes"))
        stripe_settings_headline.SetFont(wx.Font().Bold())
        self.link_colors_checkbox = wx.CheckBox(self, label=_("Link colors"))
        self.link_colors_checkbox.SetToolTip(_("When enabled update all equal colors simultaneously."))
        self.warp_headline = wx.StaticText(self, label=_("Warp"))
        self.warp_headline.SetFont(wx.Font().Bold())
        self.weft_headline = wx.StaticText(self, label=_("Weft"))
        self.weft_headline.SetFont(wx.Font().Bold())
        self.add_warp_button = wx.Button(self, label=_("Add"))
        self.add_warp_button.Bind(wx.EVT_BUTTON, self._add_warp_event)
        self.add_weft_button = wx.Button(self, label=_("Add"))
        self.add_weft_button.Bind(wx.EVT_BUTTON, self._add_weft_event)

        # Add to sizers

        general_settings_sizer.Add(self.symmetry_checkbox, 0, wx.CENTER | wx.ALL, 10)
        general_settings_sizer.Add(self.warp_weft_checkbox, 0, wx.CENTER | wx.ALL, 10)

        positional_settings_sizer.Add(rotate_label, 0, wx.ALIGN_CENTRE, 0)
        positional_settings_sizer.Add(self.rotate, 0, wx.EXPAND | wx.RIGHT, 30)
        positional_settings_sizer.Add(offset_x_label, 0, wx.ALIGN_CENTRE, 0)
        positional_settings_sizer.Add(self.offset_x, 0, wx.EXPAND, 0)
        positional_settings_sizer.Add(scale_label, 0, wx.ALIGN_CENTRE, 0)
        positional_settings_sizer.Add(self.scale, 0, wx.EXPAND | wx.RIGHT, 30)
        positional_settings_sizer.Add(offset_y_label, 0, wx.ALIGN_CENTRE, 0)
        positional_settings_sizer.Add(self.offset_y, 0, wx.EXPAND, 0)
        positional_settings_sizer.AddGrowableCol(1)
        positional_settings_sizer.AddGrowableCol(3)

        self.warp_outer_sizer.Add(self.warp_headline, 0, wx.EXPAND, 0)
        self.weft_outer_sizer.Add(self.weft_headline, 0, wx.EXPAND, 0)
        self.warp_outer_sizer.Add(self.warp_sizer, 0, wx.EXPAND, 0)
        self.weft_outer_sizer.Add(self.weft_sizer, 0, wx.EXPAND, 0)
        self.warp_outer_sizer.Add(self.add_warp_button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.weft_outer_sizer.Add(self.add_weft_button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.stripe_sizer.Add(self.warp_outer_sizer, 1, wx.EXPAND, 0)
        self.stripe_sizer.Add(self.weft_outer_sizer, 1, wx.EXPAND, 0)

        stripe_header_sizer.Add(stripe_settings_headline, 0, wx.ALL, 10)
        stripe_header_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 10)
        stripe_header_sizer.Add(self.link_colors_checkbox, 0, wx.ALL, 10)

        self.customize_sizer.Add(positional_settings_headline, 0, wx.ALL, 10)
        self.customize_sizer.Add(positional_settings_sizer, 0, wx.ALL | wx.EXPAND, 10)
        self.customize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.customize_sizer.Add(general_settings_headline, 0, wx.ALL, 10)
        self.customize_sizer.Add(general_settings_sizer, 0, wx.ALL | wx.EXPAND, 10)
        self.customize_sizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 10)
        self.customize_sizer.Add(stripe_header_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.customize_sizer.Add(self.stripe_sizer, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(self.customize_sizer)

    def _add_warp_event(self, event):
        self.add_stripe()

    def _add_weft_event(self, event):
        self.add_stripe(False)

    def add_stripe(self, warp=True, stripe=None, update=True):
        stripe_panel = StripePanel(self)

        if stripe is not None:
            stripe_panel.visibility.Set3StateValue(stripe['render'])
            stripe_panel.colorinfo.SetLabel(wx.Colour(stripe['color']).GetAsString(wx.C2S_HTML_SYNTAX))
            stripe_panel.colorpicker.SetColour(wx.Colour(stripe['color']))
            stripe_panel.stripe_width.SetValue(stripe['width'])

        if warp:
            self.warp_sizer.Add(stripe_panel, 0, wx.EXPAND | wx.ALL, 5)
        else:
            self.weft_sizer.Add(stripe_panel, 0, wx.EXPAND | wx.ALL, 5)

        if update:
            self.panel.update_from_stripes()

        self._hide_first_position_button()
        self.set_stripe_width_color(stripe_panel.stripe_width)
        self.FitInside()

    def _move_stripe_up(self, event):
        stripe = event.GetEventObject()

        main_sizer = None
        i = 0
        panel = stripe.GetParent()
        for i, item in enumerate(self.warp_sizer.GetChildren()):
            if item.GetWindow() == panel:
                main_sizer = self.warp_sizer
                index = i
        if not main_sizer:
            for i, item in enumerate(self.weft_sizer.GetChildren()):
                if item.GetWindow() == panel:
                    main_sizer = self.weft_sizer
                    index = i

        index = max(0, (index - 1))
        if index == 0:
            previous_first = main_sizer.GetChildren()[0].GetWindow()
            previous_first.position.Show()

        main_sizer.Detach(panel)
        main_sizer.Insert(index, panel, 0, wx.EXPAND | wx.ALL, 5)
        self._hide_first_position_button()
        self.panel.update_from_stripes()
        self.FitInside()
        self.Layout()

    def _remove_stripe(self, event):
        panel = event.GetEventObject().GetParent()
        panel.Destroy()
        self._hide_first_position_button()
        self.panel.update_from_stripes()
        self.FitInside()

    def _hide_first_position_button(self):
        if len(self.warp_sizer.GetChildren()) > 0:
            self.warp_sizer.GetChildren()[0].GetWindow().position.Show(False)
        if len(self.weft_sizer.GetChildren()) > 0:
            self.weft_sizer.GetChildren()[0].GetWindow().position.Show(False)

    def on_change(self, attribute, event):
        self.panel.settings[attribute] = event.EventObject.GetValue()
        self.panel.update_preview()

    def update_scale(self, event):
        self.panel.settings['scale'] = event.EventObject.GetValue()
        # self.update_stripes(self.panel.palette.palette_stripes)
        self.update_stripe_width_colors()
        self.panel.update_preview()

    def _update_stripes_event(self, event):
        self.set_stripe_width_color(event.EventObject)
        self.panel.update_from_stripes()

    def update_stripe_width_colors(self):
        for sizer in [self.warp_sizer, self.weft_sizer]:
            for stripe_sizer in sizer.GetChildren():
                stripe_panel = stripe_sizer.GetWindow()
                self.set_stripe_width_color(stripe_panel.stripe_width)

    def set_stripe_width_color(self, stripe_width_ctrl):
        scale = self.scale.GetValue()
        min_stripe_width = self.panel.embroidery_panel.min_stripe_width.GetValue()
        stripe_width = stripe_width_ctrl.GetValue() * scale / 100
        if stripe_width <= min_stripe_width:
            stripe_width_ctrl.SetBackgroundColour(wx.Colour('#efefef'))
            stripe_width_ctrl.SetForegroundColour('black')
        else:
            stripe_width_ctrl.SetBackgroundColour(wx.NullColour)
            stripe_width_ctrl.SetForegroundColour(wx.NullColour)

    def update_stripes(self, stripes):
        self.warp_sizer.Clear(True)
        self.weft_sizer.Clear(True)
        warp = True
        for direction in stripes:
            for stripe in direction:
                self.add_stripe(warp, stripe, False)
            warp = False
        self.panel.update_from_stripes()

    def _update_color(self, event):
        linked = self.link_colors_checkbox.GetValue()
        widget = event.GetEventObject()
        colorinfo = widget.GetPrevSibling()
        old_color = wx.Colour(colorinfo.GetLabel())
        new_color = event.Colour
        if linked:
            self._update_color_picker(old_color, new_color, self.warp_sizer)
            self._update_color_picker(old_color, new_color, self.weft_sizer)
        colorinfo.SetLabel(new_color.GetAsString(wx.C2S_HTML_SYNTAX))
        self.panel.update_from_stripes()

    def _update_color_picker(self, old_color, new_color, sizer):
        for stripe_sizer in sizer.Children:
            stripe_panel = stripe_sizer.GetWindow()
            color = stripe_panel.colorpicker.GetColour()
            if color == old_color:
                stripe_panel.colorpicker.SetColour(new_color)
                stripe_panel.colorinfo.SetLabel(new_color.GetAsString(wx.C2S_HTML_SYNTAX))

    def update_symmetry(self, event=None):
        symmetry = self.symmetry_checkbox.GetValue()
        self.panel.settings['symmetry'] = symmetry
        self.panel.palette.update_symmetry(symmetry)
        self.panel.update_from_stripes()
        self.FitInside()

    def update_warp_weft(self):
        equal_warp_weft = self.warp_weft_checkbox.GetValue()
        if equal_warp_weft:
            self.stripe_sizer.Hide(self.warp_headline, recursive=True)
            self.stripe_sizer.Hide(self.weft_outer_sizer, recursive=True)
        else:
            self.stripe_sizer.Show(self.warp_headline, recursive=True)
            self.stripe_sizer.Show(self.weft_outer_sizer, recursive=True)
            # We just made the weft colorinfo visible. Let's hide it again.
            self._hide_colorinfo()
        self.FitInside()

    def _update_warp_weft_event(self, event):
        self.panel.settings['equal_warp_weft'] = event.GetEventObject().GetValue()
        self.update_warp_weft()
        self.panel.update_from_stripes()

    def _hide_colorinfo(self):
        for stripe_sizer in self.weft_sizer.Children:
            stripe_panel = stripe_sizer.GetWindow()
            stripe_panel.colorinfo.Hide()
