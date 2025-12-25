# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _
from ...lettering.categories import FONT_CATEGORIES
from .combo_prompt import PromptingComboBox
from .editable_list import EditableListCtrl


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent()
        wx.Panel.__init__(self, parent)
        # settings
        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        self.font_chooser = wx.adv.BitmapComboBox(self, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT, size=(600, 40))
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.parent.on_font_changed)

        text_before_label = wx.StaticText(self, label=_("Text before"))
        text_before = wx.TextCtrl(self)
        text_before.Bind(wx.EVT_TEXT, self.parent.on_text_before_changed)
        text_after_label = wx.StaticText(self, label=_("Text after"))
        text_after = wx.TextCtrl(self)
        text_after.Bind(wx.EVT_TEXT, self.parent.on_text_after_changed)
        grid_text_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        grid_text_sizer.AddGrowableCol(1)
        grid_text_sizer.AddMany([
            (text_before_label, 1, wx.ALL, 0),
            (text_before, 1, wx.EXPAND, 0),
            (text_after_label, 1, wx.ALL, 0),
            (text_after, 1, wx.EXPAND, 0)
        ])

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.parent.update_preview)

        self.font_info = FontInfo(self.notebook)
        self.notebook.AddPage(self.font_info, _("Font Info"))

        self.font_settings = FontSettings(self.notebook)
        self.notebook.AddPage(self.font_settings, _("Font Settings"))

        self.font_kerning = GeneralKerning(self.notebook)
        self.notebook.AddPage(self.font_kerning, _("General Kerning"))

        glyph_list = GlyphList(self.notebook)
        self.notebook.AddPage(glyph_list, _("Horizontal advance"))
        self.glyph_list = glyph_list.glyph_list

        kerning_pairs = KerningPairs(self.notebook)
        self.notebook.AddPage(kerning_pairs, _("Kerning pairs"))
        self.kerning_list = kerning_pairs.kerning_list
        self.kerning_filter = kerning_pairs.filter_kerning

        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.parent.cancel)
        self.apply_button = wx.Button(self, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.parent.apply)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        settings_sizer.Add(self.font_chooser, 0, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(grid_text_sizer, 0, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(notebook_sizer, 2, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(apply_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(settings_sizer)


class FontInfo(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent().parent
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(20, 2, 10, 10)
        grid_sizer.AddGrowableCol(1)

        name_label = wx.StaticText(self, label=_("Name"))
        self.name = wx.TextCtrl(self)
        self.name.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("name", False, event)
        )

        description_label = wx.StaticText(self, label=_("Description"))
        self.description = wx.TextCtrl(self, size=wx.Size(10, 100), style=wx.TE_MULTILINE)
        self.description.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("description", False, event)
        )

        license_label = wx.StaticText(self, label=_("font_license"))
        self.font_license = wx.TextCtrl(self)
        self.font_license.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("font_license", False, event)
        )

        text_direction_label = wx.StaticText(self, label=_("Text direction"))
        self.text_direction = wx.Choice(self, choices=[_("Left to Right"), _("Right to Left")])
        self.text_direction.Bind(wx.EVT_CHOICE, self.parent.on_text_direction_changed)

        keywords_label = wx.StaticText(self, label=_("Keywords"))
        self.keywords = wx.ListBox(
            self,
            size=wx.Size(10, 400),
            choices=[cat.name for cat in FONT_CATEGORIES],
            style=wx.CB_SORT | wx.LB_EXTENDED
        )
        self.keywords.Bind(wx.EVT_LISTBOX, self.parent.on_keyword_changed)

        original_font_label = wx.StaticText(self, label=_("Original Font Name"))
        self.original_font = wx.TextCtrl(self)
        self.original_font.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("original_font", False, event)
        )

        original_font_url_label = wx.StaticText(self, label=_("Original Font URL"))
        self.original_font_url = wx.TextCtrl(self)
        self.original_font_url.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("original_font_url", False, event)
        )

        grid_sizer.AddMany([
            (name_label, 0, wx.ALL, 0),
            (self.name, 0, wx.ALL | wx.EXPAND, 0),
            (description_label, 0, wx.ALL, 0),
            (self.description, 1, wx.ALL | wx.EXPAND, 0),
            (license_label, 0, wx.ALL, 0),
            (self.font_license, 1, wx.ALL | wx.EXPAND, 0),
            (text_direction_label, 0, wx.ALL, 0),
            (self.text_direction, 1, wx.ALL | wx.EXPAND, 0),
            (keywords_label, 0, wx.ALL, 0),
            (self.keywords, 1, wx.ALL | wx.EXPAND, 0),
            (original_font_label, 0, wx.ALL, 0),
            (self.original_font, 0, wx.ALL | wx.EXPAND, 0),
            (original_font_url_label, 0, wx.ALL, 0),
            (self.original_font_url, 0, wx.ALL | wx.EXPAND, 0)
        ])

        sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)


class FontSettings(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent().parent
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(20, 2, 10, 10)
        grid_sizer.AddGrowableCol(1)

        default_variant_label = wx.StaticText(self, label=_("Default Variant"))
        self.default_variant = wx.Choice(self, choices=["→", "←", "↓", "↑"])
        self.default_variant.Bind(wx.EVT_CHOICE, self.parent.on_default_variant_change)

        default_glyph_label = wx.StaticText(self, label=_("Default glyph"))
        self.default_glyph = wx.TextCtrl(self)
        self.default_glyph.Bind(
            wx.EVT_TEXT,
            lambda event: self.parent.on_font_meta_value_changed("default_glyph", True, event)
        )

        auto_satin_label = wx.StaticText(self, label=_("AutoSatin"))
        self.auto_satin = wx.CheckBox(self)
        self.auto_satin.Bind(
            wx.EVT_CHECKBOX,
            lambda event: self.parent.on_font_meta_value_changed("auto_satin", False, event)
        )

        letter_case_label = wx.StaticText(self, label=_("Letter case"))
        self.letter_case = wx.Choice(self, choices=[_("None"), _("Upper"), _("Lower")])
        self.letter_case.Bind(wx.EVT_CHOICE, self.parent.on_letter_case_change)

        reversible_label = wx.StaticText(self, label=_("Reversible"))
        self.reversible = wx.CheckBox(self)
        self.reversible.Bind(
            wx.EVT_CHECKBOX,
            lambda event: self.parent.on_font_meta_value_changed("reversible", False, event)
        )

        sortable_label = wx.StaticText(self, label=_("Sortable"))
        self.sortable = wx.CheckBox(self)
        self.sortable.Bind(
            wx.EVT_CHECKBOX,
            lambda event: self.parent.on_font_meta_value_changed("sortable", False, event)
        )

        combine_indices_label = wx.StaticText(self, label=_("Combine Indices"))
        self.combine_at_sort_indices = wx.TextCtrl(self)
        self.combine_at_sort_indices.Bind(wx.EVT_TEXT, self.parent.on_combine_indices_changed)

        grid_sizer.AddMany([
            (default_variant_label, 0, wx.ALL, 0),
            (self.default_variant, 1, wx.ALL | wx.EXPAND, 0),
            (default_glyph_label, 0, wx.ALL, 0),
            (self.default_glyph, 1, wx.ALL | wx.EXPAND, 0),
            (auto_satin_label, 0, wx.ALL, 0),
            (self.auto_satin, 1, wx.ALL | wx.EXPAND, 0),
            (letter_case_label, 0, wx.ALL, 0),
            (self.letter_case, 1, wx.ALL | wx.EXPAND, 0),
            (reversible_label, 0, wx.ALL, 0),
            (self.reversible, 1, wx.ALL | wx.EXPAND, 0),
            (sortable_label, 0, wx.ALL, 0),
            (self.sortable, 1, wx.ALL | wx.EXPAND, 0),
            (combine_indices_label, 0, wx.ALL, 0),
            (self.combine_at_sort_indices, 1, wx.ALL | wx.EXPAND, 0)
        ])
        sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)


class GeneralKerning(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent().parent
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(20, 3, 10, 10)
        grid_sizer.AddGrowableCol(1)

        size_label = wx.StaticText(self, label=_("Size"))
        self.size = wx.SpinCtrlDouble(self, min=0, max=10000, inc=0.1, initial=50, style=wx.SP_WRAP)
        self.size.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            lambda event: self.parent.on_font_meta_value_changed("size", True, event)
        )
        min_scale_label = wx.StaticText(self, label=_("Min Scale"))
        self.min_scale = wx.SpinCtrlDouble(self, min=0, max=100, inc=0.1, initial=1, style=wx.SP_WRAP)
        self.min_scale.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            lambda event: self.parent.on_font_meta_value_changed("min_scale", True, event)
        )
        self.min_scale.SetDigits(2)
        max_scale_label = wx.StaticText(self, label=_("Max Scale"))
        self.max_scale = wx.SpinCtrlDouble(self, min=0, max=100, inc=0.1, initial=1, style=wx.SP_WRAP)
        self.max_scale.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            lambda event: self.parent.on_font_meta_value_changed("max_scale", True, event)
        )
        self.max_scale.SetDigits(2)
        leading_label = wx.StaticText(self, label=_("Leading"))
        self.leading = wx.SpinCtrlDouble(self, min=0, max=10000, inc=1, initial=0, style=wx.SP_WRAP)
        self.leading.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            lambda event: self.parent.on_font_meta_value_changed("leading", False, event)
        )
        horiz_adv_x_default_label = wx.StaticText(self, label=_("Horizontal advance x"))
        self.horiz_adv_x_default = wx.SpinCtrlDouble(self, min=0, max=10000, inc=0.1, initial=50, style=wx.SP_WRAP)
        self.horiz_adv_x_default.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            self.parent.on_horiz_adv_x_default_changed
        )
        self.horiz_adv_x_default_null_checkbox = wx.CheckBox(self, label=_("Glyph width"))
        self.horiz_adv_x_default_null_checkbox.SetToolTip(_("Use the width of the individual glyphs."))
        self.horiz_adv_x_default_null_checkbox.Bind(
            wx.EVT_CHECKBOX,
            self.parent.on_horiz_adv_x_default_checkbox_changed
        )
        horiz_adv_x_space_label = wx.StaticText(self, label=_("Horizontal advance x space"))
        self.horiz_adv_x_space = wx.SpinCtrlDouble(self, min=0, max=10000, inc=0.1, initial=50, style=wx.SP_WRAP)
        self.horiz_adv_x_space.Bind(
            wx.EVT_SPINCTRLDOUBLE,
            lambda event: self.parent.on_font_meta_value_changed("horiz_adv_x_space", True, event)
        )

        grid_sizer.AddMany([
            (size_label, 0, wx.ALL, 0),
            (self.size, 1, wx.ALL | wx.EXPAND, 0),
            (wx.StaticText(self), 1, wx.ALL | wx.EXPAND, 0),

            (min_scale_label, 0, wx.ALL, 0),
            (self.min_scale, 1, wx.ALL | wx.EXPAND, 0),
            (wx.StaticText(self), 1, wx.ALL | wx.EXPAND, 0),

            (max_scale_label, 0, wx.ALL, 0),
            (self.max_scale, 1, wx.ALL | wx.EXPAND, 0),
            (wx.StaticText(self), 1, wx.ALL | wx.EXPAND, 0),

            (leading_label, 0, wx.ALL, 0),
            (self.leading, 1, wx.ALL | wx.EXPAND, 0),
            (wx.StaticText(self), 1, wx.ALL | wx.EXPAND, 0),

            (horiz_adv_x_default_label, 0, wx.ALL, 0),
            (self.horiz_adv_x_default, 1, wx.ALL | wx.EXPAND, 0),
            (self.horiz_adv_x_default_null_checkbox, 1, wx.ALL | wx.EXPAND, 0),

            (horiz_adv_x_space_label, 0, wx.ALL, 0),
            (self.horiz_adv_x_space, 1, wx.ALL | wx.EXPAND, 0),
            (wx.StaticText(self), 1, wx.ALL | wx.EXPAND, 0)
        ])

        sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)


class GlyphList(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent().parent
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.glyph_list = EditableListCtrl(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER, editable_column=3)
        self.glyph_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.parent.on_kerning_list_select)
        self.glyph_list.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.parent.on_glyphlist_update)
        self.glyph_list.Bind(wx.EVT_LIST_ITEM_CHECKED, self.parent.on_glyph_item_checked)
        self.glyph_list.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.parent.on_glyph_item_checked)
        self.glyph_list.EnableCheckBoxes()

        sizer.Add(self.glyph_list, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)


class KerningPairs(wx.Panel):
    def __init__(self, parent):
        self.parent = parent.GetParent().parent
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        choices = [' '] + self.parent.glyphs
        self.filter_kerning = PromptingComboBox(self, choices=choices, style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.filter_kerning, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.kerning_list = EditableListCtrl(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.kerning_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.parent.on_kerning_list_select)
        self.kerning_list.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.parent.on_kerning_update)

        sizer.Add(self.kerning_list, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)

    def on_combobox_change(self, event):
        combobox = event.GetEventObject()
        value = combobox.GetValue().strip()
        if value and value != " ":
            self.parent.update_kerning_list(value)
        else:
            self.parent.update_kerning_list()
