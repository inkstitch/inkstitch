# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import deepcopy

import wx
import wx.adv
from inkex import Group, errormsg
import unicodedata

from ..commands import ensure_command_symbols
from ..i18n import _
from ..lettering import get_font_list
from ..marker import ensure_marker_symbols
from ..utils.settings import global_settings
from ..svg.tags import (SODIPODI_INSENSITIVE)


class FontSampleFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        self.layer = kwargs.pop("layer")
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Font Sampling"), *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.fonts = None
        self.font = None
        self.font_variant = None

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

        max_line_width = global_settings['font_sampling_max_line_width']
        self.max_line_width.SetValue(max_line_width)
        scale_spinner = global_settings['font_sampling_scale_spinner']
        self.scale_spinner.SetValue(scale_spinner)

        self.set_font_list()
        select_font = global_settings['last_font']
        self.font_chooser.SetValue(select_font)
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
        selected_font = self.font_chooser.GetValue()
        if selected_font:
            self.font = self.fonts[selected_font]
        else:
            first = list(self.fonts.values())[0].marked_custom_font_name
            self.font = self.fonts[first]
            self.font_chooser.SetValue(first)
        global_settings['last_font'] = self.font.marked_custom_font_name
        self.scale_spinner.SetRange(int(self.font.min_scale * 100), int(self.font.max_scale * 100))
        # font._load_variants()
        self.direction.Clear()
        for variant in self.font.has_variants():
            self.direction.Append(variant)
        self.direction.SetSelection(0)
        if self.font.sortable:
            self.color_sort_label.Enable()
            self.color_sort_checkbox.Enable()
        else:
            self.color_sort_label.Disable()
            self.color_sort_checkbox.Disable()

    def apply(self, event):
        # apply scale to layer and extract for later use
        self.layer.transform.add_scale(self.scale_spinner.GetValue() / 100)
        scale = self.layer.transform.a

        if self.font is None:
            self.GetTopLevelParent().Close()
            return

        # parameters
        line_width = self.max_line_width.GetValue()
        direction = self.direction.GetValue()
        scale_spinner = self.scale_spinner.GetValue()

        global_settings['font_sampling_max_line_width'] = line_width
        global_settings['font_sampling_scale_spinner'] = scale_spinner

        self.font._load_variants()
        self.font_variant = self.font.variants[direction]

        # setup lines of text
        text = ''
        width = 0
        last_glyph = None
        outdated = False

        for glyph in self.font.available_glyphs:
            glyph_obj = self.font_variant[glyph]
            if glyph_obj is None:
                outdated = True
                continue
            if SODIPODI_INSENSITIVE not in glyph_obj.node.attrib:
                if last_glyph is not None:
                    width_to_add = (glyph_obj.min_x - self.font.kerning_pairs.get(f'{last_glyph} {glyph}', 0)) * scale
                    width += width_to_add
                try:
                    width_to_add = (self.font.horiz_adv_x.get(glyph, self.font.horiz_adv_x_default) - glyph_obj.min_x) * scale
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

        self.out_dated_warning(outdated)
        self._render_text(text)
        self.GetTopLevelParent().Close()

    def sortable(self):
        color_sort = self.color_sort_checkbox.GetValue()
        if color_sort and not self.font.sortable:
            color_sort = False
        return color_sort

    def out_dated_warning(self, outdated=False):
        # called with outdated == True when some glyphs present in the font.json glyph list are not present in the svg font file

        update_glyphlist_warning = _(
            "The glyphlist for this font seems to be outdated.\n\n"
            "Please update the glyph list for {font_name}:\n"
            "* Open Extensions > Ink/Stitch > Font Management > Edit JSON\n"
            "* Select this font and apply."
        ).format(font_name=self.font.marked_custom_font_name)

        # warning in case of duplicates in the glyph list of the font.json file
        if len(set(self.font.available_glyphs)) != len(self.font.available_glyphs):
            outdated = True

        # this will cause a warning if some glyphs of the svg font are not present in the font.json glyph list
        if len(set(self.font.available_glyphs)) != len(self.font_variant.glyphs):
            outdated = True

        if outdated:
            errormsg(update_glyphlist_warning)

    def _render_text(self, text):
        lines = text.splitlines()
        position = {'x': 0, 'y': 0}
        for line in lines:
            group = Group()
            label = ""
            # make the label of the group line clearly show the non spacing marks
            for character in line:
                if unicodedata.category(character) != 'Mn':
                    label += character
                else:
                    label += ' ' + character
            group.label = label
            group.set("inkstitch:letter-group", "line")
            glyphs = []
            skip = []
            for i, character in enumerate(line):
                if i in skip:
                    continue
                default_variant = self.font.variants[self.font.json_default_variant]
                glyph, glyph_len = default_variant.get_glyph(character, line[i:])
                glyphs.append(glyph)
                skip = list(range(i, i+glyph_len))

            last_character = None
            for glyph in glyphs:
                if glyph is None:
                    position['x'] += self.font.horiz_adv_x_space
                    last_character = None
                    continue

                position = self._render_glyph(group, glyph, position, glyph.name, last_character)
                last_character = glyph.name
            self.layer.add(group)
            position['x'] = 0
            position['y'] += self.font.leading

        if self.sortable():
            self.font.do_color_sort(self.layer, 1)

        ensure_command_symbols(group)
        ensure_marker_symbols(group)

    def _render_glyph(self, group, glyph, position, character, last_character):
        node = deepcopy(glyph.node)
        if last_character is not None:
            if self.font.text_direction != 'rtl':
                position['x'] += glyph.min_x - self.font.kerning_pairs.get(f'{last_character} {character}', 0)
            else:
                position['x'] += glyph.min_x - self.font.kerning_pairs.get(f'{character} {last_character}', 0)

        transform = f"translate({position['x']}, {position['y']})"
        node.set('transform', transform)

        horiz_adv_x_default = self.font.horiz_adv_x_default
        if horiz_adv_x_default is None:
            horiz_adv_x_default = glyph.width + glyph.min_x

        position['x'] += self.font.horiz_adv_x.get(character, horiz_adv_x_default) - glyph.min_x

        self.font._update_commands(node, glyph)
        self.font._update_clips(group, node, glyph)

        # this is used to recognize a glyph layer later in the process
        # because this is not unique it will be overwritten by inkscape when inserted into the document
        node.set("id", "glyph")
        node.set("inkstitch:letter-group", "glyph")
        # force inkscape to show a label when the glyph is only a non spacing mark
        if len(node.label) == 1 and unicodedata.category(node.label) == 'Mn':
            node.label = ' ' + node.label

        group.add(node)

        return position

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
