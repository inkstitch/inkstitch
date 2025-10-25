import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...i18n import _
from ...lettering.categories import FONT_CATEGORIES, FontCategory


class LetteringOptionsPanel(ScrolledPanel):
    def __init__(self, parent, panel):
        self.panel = panel
        ScrolledPanel.__init__(self, parent)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

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
        self.scale_info_percent = wx.StaticText(self, wx.ID_ANY, '0% - 200%')
        self.scale_info_mm = wx.StaticText(self, wx.ID_ANY, ' (10mm - 100mm)')
        size_info_sizer.Add(size_info_label, 0, wx.LEFT, 0)
        size_info_sizer.Add(self.size_info, 0, wx.LEFT, 0)
        size_info_sizer.Add(size_info_unit, 0, wx.LEFT, 0)
        size_info_sizer.Add(scale_info_label, 0, wx.LEFT, 10)
        size_info_sizer.Add(self.scale_info_percent, 0, wx.LEFT, 5)
        size_info_sizer.Add(self.scale_info_mm, 0, wx.LEFT, 0)
        font_description_sizer.Add(size_info_sizer, 0, wx.ALL, 0)

        self.font_selector_box = wx.StaticBox(self, wx.ID_ANY, label=_("Font"))
        font_selector_sizer = wx.StaticBoxSizer(self.font_selector_box, wx.VERTICAL)
        font_selector_box = wx.BoxSizer(wx.HORIZONTAL)
        font_selector_box.Add(self.font_chooser, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
        font_selector_sizer.Add(font_selector_box, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        font_selector_sizer.Add(self.font_description, 0, wx.EXPAND | wx.ALL, 10)
        font_selector_sizer.Add(font_description_sizer, 0, wx.EXPAND | wx.ALL, 10)
        outer_sizer.Add(font_selector_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # options
        self.scale_spinner = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=1000, initial=100)
        self.scale_spinner.Bind(wx.EVT_SPINCTRL, lambda event: self.panel.on_change("scale", event))

        self.back_and_forth_checkbox = wx.CheckBox(self, label=_("Stitch lines of text back and forth"))
        self.back_and_forth_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.panel.on_change("back_and_forth", event))

        align_text_label = wx.StaticText(self, wx.ID_ANY, _("Align Text"))
        self.align_text_choice = wx.Choice(
            self,
            choices=[_("Left"), _("Center"), _("Right"), _("Block (default)"), _("Block (letterspacing)")]
        )
        self.align_text_choice.Bind(wx.EVT_CHOICE, lambda event: self.panel.on_choice_change("text_align", event))

        color_sort_label = wx.StaticText(self, wx.ID_ANY, _("Color sort"))
        color_sort_label.SetToolTip(_("Sort multicolor fonts. Unifies tartan patterns."))
        self.color_sort_choice = wx.Choice(self, choices=[_("Off"), _("Whole text"), _("Line"), _("Word")], name=_("Color sort"))
        self.color_sort_choice.SetToolTip(_("Sort multicolor fonts. Unifies tartan patterns."))
        self.color_sort_choice.Bind(wx.EVT_CHOICE, self.panel.on_color_sort_change)

        trim_label = wx.StaticText(self, wx.ID_ANY, _("Add trims"))
        self.trim_option_choice = wx.Choice(self, choices=[_("Never"), _("after each line"), _("after each word"), _("after each letter")],
                                            name=_("Add trim command"))
        self.trim_option_choice.Bind(wx.EVT_CHOICE, lambda event: self.panel.on_choice_change("trim_option", event))

        self.use_trim_symbols = wx.CheckBox(self, label=_("Use command symbols"))
        self.use_trim_symbols.Bind(wx.EVT_CHECKBOX, lambda event: self.panel.on_change("use_trim_symbols", event))
        self.use_trim_symbols.SetToolTip(_('Uses command symbols if enabled. When disabled inserts trim commands as params.'))

        left_option_sizer = wx.BoxSizer(wx.VERTICAL)

        font_scale_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, _("Scale")), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 0)
        font_scale_sizer.Add(self.scale_spinner, 0, wx.LEFT, 10)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, "%"), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 3)
        left_option_sizer.Add(font_scale_sizer, 0, wx.ALL, 5)

        left_option_sizer.Add(self.back_and_forth_checkbox, 1, wx.LEFT | wx.TOP | wx.RIGHT, 5)

        align_sizer = wx.BoxSizer(wx.HORIZONTAL)
        align_sizer.Add(align_text_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        align_sizer.Add(self.align_text_choice, 0, wx.ALL, 5)
        left_option_sizer.Add(align_sizer, 0, wx.ALL, 5)

        right_option_sizer = wx.BoxSizer(wx.VERTICAL)

        color_sort_sizer = wx.BoxSizer(wx.HORIZONTAL)
        color_sort_sizer.Add(color_sort_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        color_sort_sizer.Add(self.color_sort_choice, 1, wx.ALL, 5)
        right_option_sizer.Add(color_sort_sizer, 0, wx.ALIGN_LEFT, 5)

        trim_sizer = wx.BoxSizer(wx.HORIZONTAL)
        trim_sizer.Add(trim_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        trim_sizer.Add(self.trim_option_choice, 0, wx.ALL, 5)
        right_option_sizer.Add(trim_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 5)

        right_option_sizer.Add(self.use_trim_symbols, 0, wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)

        self.options_box = wx.StaticBox(self, wx.ID_ANY, label=_("Options"))
        options_sizer = wx.StaticBoxSizer(self.options_box, wx.HORIZONTAL)
        options_sizer.Add(left_option_sizer, 1, wx.ALL, 10)
        options_sizer.Add(right_option_sizer, 0, wx.ALL, 10)
        outer_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # spacing
        self.spacing_box = wx.StaticBox(self, wx.ID_ANY, label=_("Spacing"))
        letter_spacing_label = wx.StaticText(self, wx.ID_ANY, _("Letter spacing"))
        letter_spacing_label.SetToolTip(_("Additional letter spacing in mm."))
        self.letter_spacing = wx.SpinCtrlDouble(self, min=-500, max=500, inc=0.01, initial=0, style=wx.SP_WRAP)
        word_spacing_label = wx.StaticText(self, wx.ID_ANY, _("Word spacing"))
        word_spacing_label.SetToolTip(_("Additional word spacing in mm."))
        self.word_spacing = wx.SpinCtrlDouble(self, min=-500, max=500, inc=0.01, initial=0, style=wx.SP_WRAP)
        line_height_label = wx.StaticText(self, wx.ID_ANY, _("Line height"))
        line_height_label.SetToolTip(_("Additional line height in mm."))
        self.line_height = wx.SpinCtrlDouble(self, min=-500, max=500, inc=0.01, initial=0, style=wx.SP_WRAP)

        self.letter_spacing.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.panel.on_change("letter_spacing", event))
        self.word_spacing.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.panel.on_change("word_spacing", event))
        self.line_height.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.panel.on_change("line_height", event))

        spacing_sizer = wx.StaticBoxSizer(self.spacing_box, wx.HORIZONTAL)
        spacing_sizer.Add(letter_spacing_label, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTRE_VERTICAL, 5)
        spacing_sizer.Add(self.letter_spacing, 0, wx.LEFT | wx.BOTTOM, 5)
        spacing_sizer.Add(word_spacing_label, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTRE_VERTICAL, 5)
        spacing_sizer.Add(self.word_spacing, 0, wx.LEFT | wx.BOTTOM, 5)
        spacing_sizer.Add(line_height_label, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTRE_VERTICAL, 5)
        spacing_sizer.Add(self.line_height, 0, wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)
        outer_sizer.Add(spacing_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # text input
        self.text_input_box = wx.StaticBox(self, wx.ID_ANY, label=_("Text"))
        self.text_editor = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, size=(50, 100))
        self.text_editor.Bind(wx.EVT_TEXT, lambda event: self.panel.on_change("text", event))

        text_input_sizer = wx.StaticBoxSizer(self.text_input_box, wx.VERTICAL)
        text_input_sizer.Add(self.text_editor, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(text_input_sizer, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # set panel sizer
        self.SetSizer(outer_sizer)
        self.SetupScrolling()
