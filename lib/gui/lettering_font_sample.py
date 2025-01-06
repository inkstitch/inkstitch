# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
import wx.adv
from inkex import errormsg

from ..i18n import _
from ..lettering import get_font_list


class FontSampleFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        self.layer = kwargs.pop("layer")
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Font Sampling"), *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.fonts = None

        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.settings, _("Settings"))

        # settings
        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        self.font_chooser = wx.adv.BitmapComboBox(self.settings, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT, size=((800, 20)))
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.on_font_changed)

        grid_settings_sizer = wx.FlexGridSizer(7, 2, 5, 5)
        grid_settings_sizer.AddGrowableCol(1)

        direction_label = wx.StaticText(self.settings, label=_("Stitch direction"))
        self.direction = wx.ComboBox(self.settings, choices=[], style=wx.CB_READONLY)
        scale_spinner_label = wx.StaticText(self.settings, label=_("Scale (%)"))
        self.scale_spinner = wx.SpinCtrl(self.settings, wx.ID_ANY, min=0, max=1000, initial=100)
        max_line_width_label = wx.StaticText(self.settings, label=_("Max. line width"))
        self.max_line_width = wx.SpinCtrl(self.settings, wx.ID_ANY, min=0, max=5000, initial=180)
        self.color_sort_label = wx.StaticText(self.settings, label=_("Color sort"))
        self.color_sort_checkbox = wx.CheckBox(self.settings)

        grid_settings_sizer.Add(direction_label, 0, wx.ALIGN_LEFT, 0)
        grid_settings_sizer.Add(self.direction, 0, wx.EXPAND, 0)
        grid_settings_sizer.Add(scale_spinner_label, 0, wx.ALIGN_LEFT, 0)
        grid_settings_sizer.Add(self.scale_spinner, 0, wx.EXPAND, 0)
        grid_settings_sizer.Add(max_line_width_label, 0, wx.ALIGN_LEFT, 0)
        grid_settings_sizer.Add(self.max_line_width, 0, wx.EXPAND, 0)
        grid_settings_sizer.Add(self.color_sort_label, 0, wx.ALIGN_LEFT, 0)
        grid_settings_sizer.Add(self.color_sort_checkbox, 0, wx.EXPAND, 0)

        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.settings, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self.settings, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        settings_sizer.Add(self.font_chooser, 1, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(grid_settings_sizer, 1, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(apply_sizer, 1, wx.ALIGN_RIGHT | wx.ALL, 10)

        # help
        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("    This extension helps font creators to generate an output of every glyph from a selected font."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        help_sizer.Add(help_text, 0, wx.ALL, 8)

        help_sizer.Add((20, 20), 0, 0, 0)

        website_info = wx.StaticText(self.help, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.ALL, 8)

        self.website_link = wx.adv.HyperlinkCtrl(
            self.help,
            wx.ID_ANY,
            _("https://inkstitch.org/docs/font-tools/#font-sampling"),
            _("https://inkstitch.org/docs/font-tools/#font-sampling")
        )
        help_sizer.Add(self.website_link, 0, wx.ALL, 8)

        self.help.SetSizer(help_sizer)
        self.settings.SetSizer(settings_sizer)
        self.main_panel.SetSizer(notebook_sizer)

        self.set_font_list()
        self.font_chooser.SetValue(list(self.fonts.values())[0].marked_custom_font_name)
        self.on_font_changed()

        self.SetSizeHints(notebook_sizer.CalcMin())

        self.Layout()

    def set_font_list(self):
        self.fonts = {}
        font_list = get_font_list()
        for font in font_list:
            self.fonts[font.marked_custom_font_name] = font
            image = font.preview_image
            if image is not None:
                image = wx.Image(image)
                # Windows requires all images to have the exact same size
                image.Rescale(300, 20, quality=wx.IMAGE_QUALITY_HIGH)
                self.font_chooser.Append(font.marked_custom_font_name, wx.Bitmap(image))
            else:
                self.font_chooser.Append(font.marked_custom_font_name)

    def on_font_changed(self, event=None):
        font = self.fonts.get(self.font_chooser.GetValue(), list(self.fonts.values())[0].marked_custom_font_name)
        self.scale_spinner.SetRange(int(font.min_scale * 100), int(font.max_scale * 100))
        # font._load_variants()
        self.direction.Clear()
        for variant in font.has_variants():
            self.direction.Append(variant)
        self.direction.SetSelection(0)
        if font.sortable:
            self.color_sort_label.Enable()
            self.color_sort_checkbox.Enable()
        else:
            self.color_sort_label.Disable()
            self.color_sort_checkbox.Disable()

    def apply(self, event):
        # apply scale to layer and extract for later use
        self.layer.transform.add_scale(self.scale_spinner.GetValue() / 100)
        scale = self.layer.transform.a

        # set font
        font = self.fonts.get(self.font_chooser.GetValue())
        if font is None:
            self.GetTopLevelParent().Close()
            return

        # parameters
        line_width = self.max_line_width.GetValue()
        direction = self.direction.GetValue()
        color_sort = self.sortable(font)

        font._load_variants()
        font_variant = font.variants[direction]

        # setup lines of text
        text = ''
        width = 0
        last_glyph = None
        printed_warning = False
        update_glyphlist_warning = _(
            "The glyphlist for this font seems to be outdated.\n\n"
            "Please update the glyph list for %s:\n"
            "open Extensions > Ink/Stitch > Font Management > Edit JSON "
            "select this font and apply. No other changes necessary."
            % font.marked_custom_font_name
        )

        self.duplicate_warning(font)

        # font variant glyph list length falls short if a single quote sign is available
        # let's add it in the length comparison
        if len(set(font.available_glyphs)) != len(font_variant.glyphs):
            errormsg(update_glyphlist_warning)
            printed_warning = True

        for glyph in font.available_glyphs:
            glyph_obj = font_variant[glyph]
            if glyph_obj is None:
                if not printed_warning:
                    errormsg(update_glyphlist_warning)
                printed_warning = True
                continue
            if last_glyph is not None:
                width_to_add = (glyph_obj.min_x - font.kerning_pairs.get(last_glyph + glyph, 0)) * scale
                width += width_to_add

            try:
                width_to_add = (font.horiz_adv_x.get(glyph, font.horiz_adv_x_default) - glyph_obj.min_x) * scale
            except TypeError:
                width_to_add = glyph_obj.width

            if width + width_to_add > line_width:
                text += '\n'
                width = 0
                last_glyph = None
            else:
                last_glyph = glyph
            text += glyph
            width += width_to_add

        # render text and close
        font.render_text(text, self.layer, variant=direction, back_and_forth=False, color_sort=color_sort)
        self.GetTopLevelParent().Close()

    def sortable(self, font):
        color_sort = self.color_sort_checkbox.GetValue()
        if color_sort and not font.sortable:
            color_sort = False
        return color_sort

    def duplicate_warning(self, font):
        # warn about duplicated glyphs
        if len(set(font.available_glyphs)) != len(font.available_glyphs):
            duplicated_glyphs = " ".join(
                [glyph for glyph in set(font.available_glyphs) if font.available_glyphs.count(glyph) > 1]
            )
            errormsg(_("Found duplicated glyphs in font file: {duplicated_glyphs}").format(duplicated_glyphs=duplicated_glyphs))

    def cancel(self, event):
        self.GetTopLevelParent().Close()


class LetteringFontSampleApp(wx.App):
    def __init__(self, layer):
        self.layer = layer
        super().__init__()

    def OnInit(self):
        self.frame = FontSampleFrame(layer=self.layer)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
