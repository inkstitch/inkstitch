import wx

from ...i18n import _
from ...lettering.categories import FONT_CATEGORIES, FontCategory


class LetteringOptionsPanel(wx.Panel):
    def __init__(self, parent, panel):
        self.panel = panel
        wx.Panel.__init__(self, parent)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # font selection
        self.font_chooser = wx.adv.BitmapComboBox(self, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT)
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.panel.on_font_changed)

        self.font_description = wx.StaticText(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_SIZE, self.panel.resize)

        font_description_sizer = wx.BoxSizer(wx.HORIZONTAL)
        size_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bold_font = wx.Font(wx.FontInfo().Bold())
        size_info_label = wx.StaticText(self, wx.ID_ANY, _("Height: "))
        size_info_label.SetFont(bold_font)
        self.size_info = wx.StaticText(self, wx.ID_ANY, "10")
        size_info_unit = wx.StaticText(self, wx.ID_ANY, "mm")
        scale_info_label = wx.StaticText(self, wx.ID_ANY, _("Scale:"))
        scale_info_label.SetFont(bold_font)
        self.min_scale_info = wx.StaticText(self, wx.ID_ANY, '0')
        middle_scale = wx.StaticText(self, wx.ID_ANY, '% - ')
        self.max_scale_info = wx.StaticText(self, wx.ID_ANY, '200')
        end_scale = wx.StaticText(self, wx.ID_ANY, '%')
        size_info_sizer.Add(size_info_label, 0, wx.LEFT, 0)
        size_info_sizer.Add(self.size_info, 0, wx.LEFT, 0)
        size_info_sizer.Add(size_info_unit, 0, wx.LEFT, 0)
        size_info_sizer.Add(scale_info_label, 0, wx.LEFT, 10)
        size_info_sizer.Add(self.min_scale_info, 0, wx.LEFT, 5)
        size_info_sizer.Add(middle_scale, 0, wx.LEFT, 0)
        size_info_sizer.Add(self.max_scale_info, 0, wx.LEFT, 0)
        size_info_sizer.Add(end_scale, 0, wx.LEFT, 0)
        font_description_sizer.Add(size_info_sizer, 0, wx.ALL, 0)

        self.font_selector_box = wx.StaticBox(self, wx.ID_ANY, label=_("Font"))
        font_selector_sizer = wx.StaticBoxSizer(self.font_selector_box, wx.VERTICAL)
        font_selector_box = wx.BoxSizer(wx.HORIZONTAL)
        font_selector_box.Add(self.font_chooser, 4, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
        font_selector_sizer.Add(font_selector_box, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        font_selector_sizer.Add(self.font_description, 1, wx.EXPAND | wx.ALL, 10)
        font_selector_sizer.Add(font_description_sizer, 1, wx.EXPAND | wx.ALL, 10)
        outer_sizer.Add(font_selector_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # filter font list
        self.font_size_filter = wx.SpinCtrlDouble(self, min=0, max=100, inc=0.1, initial=0, style=wx.SP_WRAP)
        self.font_size_filter.SetDigits(2)
        self.font_size_filter.Bind(wx.EVT_SPINCTRLDOUBLE, self.panel.on_filter_changed)
        self.font_size_filter.SetToolTip(_("Font size filter (mm). 0 for all sizes."))

        self.font_glyph_filter = wx.CheckBox(self, label=_("Glyphs"))
        self.font_glyph_filter.Bind(wx.EVT_CHECKBOX, self.panel.on_filter_changed)
        self.font_glyph_filter.SetToolTip(_("Filter fonts by available glyphs."))

        self.font_category_filter = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        unfiltered = FontCategory('unfiltered', "---")
        self.font_category_filter.Append(unfiltered.name, unfiltered)
        for category in FONT_CATEGORIES:
            self.font_category_filter.Append(category.name, category)
        self.font_category_filter.SetToolTip(_("Filter fonts by category."))
        self.font_category_filter.SetSelection(0)
        self.font_category_filter.Bind(wx.EVT_COMBOBOX, self.panel.on_filter_changed)

        self.filter_box = wx.StaticBox(self, wx.ID_ANY, label=_("Font Filter"))
        filter_sizer = wx.StaticBoxSizer(self.filter_box, wx.HORIZONTAL)
        filter_size_label = wx.StaticText(self, wx.ID_ANY, _("Size"))
        filter_sizer.Add(filter_size_label, 0, wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        filter_sizer.AddSpacer(5)
        filter_sizer.Add(self.font_size_filter, 1, wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        filter_sizer.AddSpacer(5)
        filter_sizer.Add(self.font_glyph_filter, 1, wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        filter_sizer.Add(self.font_category_filter, 1, wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        outer_sizer.Add(filter_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # options
        self.scale_spinner = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=1000, initial=100)
        self.scale_spinner.Bind(wx.EVT_SPINCTRL, lambda event: self.panel.on_change("scale", event))

        self.back_and_forth_checkbox = wx.CheckBox(self, label=_("Stitch lines of text back and forth"))
        self.back_and_forth_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.panel.on_change("back_and_forth", event))

        self.color_sort_checkbox = wx.CheckBox(self, label=_("Color sort"))
        self.color_sort_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.panel.on_change("color_sort", event))
        self.color_sort_checkbox.SetToolTip(_("Sort multicolor fonts. Unifies tartan patterns."))

        self.trim_option_choice = wx.Choice(self, choices=[_("Never"), _("after each line"), _("after each word"), _("after each letter")],
                                            name=_("Add trim command"))
        self.trim_option_choice.Bind(wx.EVT_CHOICE, lambda event: self.panel.on_trim_option_change(event))

        self.use_trim_symbols = wx.CheckBox(self, label=_("Use command symbols"))
        self.use_trim_symbols.Bind(wx.EVT_CHECKBOX, lambda event: self.panel.on_change("use_trim_symbols", event))
        self.use_trim_symbols.SetToolTip(_('Uses command symbols if enabled. When disabled inserts trim commands as params.'))

        left_option_sizer = wx.BoxSizer(wx.VERTICAL)

        font_scale_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, _("Scale")), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 0)
        font_scale_sizer.Add(self.scale_spinner, 0, wx.LEFT, 10)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, "%"), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 3)
        left_option_sizer.Add(font_scale_sizer, 0, wx.ALIGN_LEFT, 5)

        left_option_sizer.Add(self.back_and_forth_checkbox, 1, wx.LEFT | wx.TOP | wx.RIGHT, 5)
        left_option_sizer.Add(self.color_sort_checkbox, 1, wx.LEFT | wx.TOP | wx.RIGHT, 5)

        right_option_sizer = wx.BoxSizer(wx.VERTICAL)

        right_option_sizer.Add(wx.StaticText(self, wx.ID_ANY, _("Add trims")), 0, wx.LEFT | wx.ALIGN_TOP, 5)
        right_option_sizer.Add(self.trim_option_choice, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, 5)
        right_option_sizer.Add(self.use_trim_symbols, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, 5)

        self.options_box = wx.StaticBox(self, wx.ID_ANY, label=_("Options"))
        options_sizer = wx.StaticBoxSizer(self.options_box, wx.HORIZONTAL)
        options_sizer.Add(left_option_sizer, 1, wx.LEFT | wx.RIGHT, 10)
        options_sizer.Add(right_option_sizer, 0, wx.RIGHT, 10)
        outer_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # text input
        self.text_input_box = wx.StaticBox(self, wx.ID_ANY, label=_("Text"))
        self.text_editor = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP)
        self.text_editor.Bind(wx.EVT_TEXT, lambda event: self.panel.on_change("text", event))

        text_input_sizer = wx.StaticBoxSizer(self.text_input_box, wx.VERTICAL)
        text_input_sizer.Add(self.text_editor, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(text_input_sizer, 2, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # set panel sizer
        self.SetSizerAndFit(outer_sizer)
