# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from copy import deepcopy
from itertools import combinations_with_replacement
from os import path

import wx
import wx.adv
from inkex import errormsg
from wx.lib.mixins.listctrl import TextEditMixin

from ..elements import nodes_to_elements
from ..i18n import _
from ..lettering import get_font_list
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg.tags import SVG_PATH_TAG
from ..utils.threading import ExitThread, check_stop_flag
from . import PreviewRenderer


class LetteringKerningPanel(wx.Panel):

    def __init__(self, parent, simulator, layer, metadata=None, background_color='white'):
        self.parent = parent
        self.simulator = simulator
        self.layer = layer
        self.metadata = metadata or dict()
        self.background_color = background_color

        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.fonts = None
        self.font = None
        self.kerning_pairs = None
        self.kerning_combinations = []
        self.text_before = ''
        self.text_after = ''

        # preview
        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.settings, _("Settings"))

        # settings
        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        self.font_chooser = wx.adv.BitmapComboBox(self.settings, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT, size=(600, 40))
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.on_font_changed)

        text_before_label = wx.StaticText(self.settings, label=_("Text before"))
        text_before = wx.TextCtrl(self.settings)
        text_before.Bind(wx.EVT_TEXT, self.on_text_before_changed)
        text_after_label = wx.StaticText(self.settings, label=_("Text after"))
        text_after = wx.TextCtrl(self.settings)
        text_after.Bind(wx.EVT_TEXT, self.on_text_after_changed)
        grid_text_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        grid_text_sizer.AddGrowableCol(1)
        grid_text_sizer.AddMany([
            (text_before_label, 1, wx.ALL, 0),
            (text_before, 1, wx.EXPAND, 0),
            (text_after_label, 1, wx.ALL, 0),
            (text_after, 1, wx.EXPAND, 0)
        ])

        self.kerning_list = EditableListCtrl(self.settings, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.kerning_list.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.on_kerning_list_focus)
        self.kerning_list.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.on_kerning_update)

        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.settings, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self.settings, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        settings_sizer.Add(self.font_chooser, 0, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(grid_text_sizer, 0, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(self.kerning_list, 2, wx.ALL | wx.EXPAND, 10)
        settings_sizer.Add(apply_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

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
        self.SetSizer(notebook_sizer)

        self.set_font_list()
        self.font_chooser.SetValue(list(self.fonts.values())[0].marked_custom_font_name)
        self.on_font_changed()

        self.SetSizeHints(notebook_sizer.CalcMin())
        self.Layout()

    def on_text_before_changed(self, event):
        self.text_before = event.GetEventObject().GetValue()
        self.update_preview()

    def on_text_after_changed(self, event):
        self.text_after = event.GetEventObject().GetValue()
        self.update_preview()

    def on_kerning_update(self, event=None):
        self.preview_renderer.update()

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

    def on_kerning_list_focus(self, event=None):
        self.preview_renderer.update()

    def get_active_kerning_pair(self):
        selection = self.kerning_list.GetFirstSelected()
        if selection == -1:
            return ''
        kerning_pair = self.kerning_list.GetItem(selection, 0).Text
        kerning = float(self.kerning_list.GetItem(selection, 1).Text)
        if self.kerning_list.GetItem(selection, 2).Text:
            try:
                kerning = float(self.kerning_list.GetItem(selection, 2).Text)
            except ValueError:
                pass
        self.kerning_pairs[kerning_pair] = float(kerning)
        return kerning_pair

    def on_font_changed(self, event=None):
        self.font = self.fonts.get(self.font_chooser.GetValue(), list(self.fonts.values())[0].marked_custom_font_name)
        self.kerning_pairs = self.font.kerning_pairs
        self.font._load_variants()
        kerning_combinations = combinations_with_replacement(self.font.available_glyphs, 2)
        self.kerning_combinations = [''.join(combination) for combination in kerning_combinations]
        self.kerning_combinations.extend([combination[1] + combination[0] for combination in self.kerning_combinations])
        self.kerning_combinations = list(set(self.kerning_combinations))
        self.kerning_combinations.sort()

        # Add the rows
        self.kerning_list.ClearAll()
        # Add some columns
        self.kerning_list.InsertColumn(0, "Kerning pair")
        self.kerning_list.InsertColumn(1, "Current kerning")
        self.kerning_list.InsertColumn(2, "New kerning")
        # Set the width of the columns
        self.kerning_list.SetColumnWidth(0, 120)
        self.kerning_list.SetColumnWidth(1, 120)
        self.kerning_list.SetColumnWidth(2, 120)
        for kerning_pair in self.kerning_combinations:
            index = self.kerning_list.InsertItem(self.kerning_list.GetItemCount(), kerning_pair)
            self.kerning_list.SetItem(index, 0, kerning_pair)
            self.kerning_list.SetItem(index, 1, str(self.kerning_pairs.get(kerning_pair, 0.0)))
        if self.kerning_list.GetItemCount() != 0:
            self.kerning_list.Focus(0)
            self.kerning_list.Select(0)

        self.update_preview()

    def apply(self, event):
        json_file = path.join(self.font.path, 'font.json')

        if not path.isfile(json_file) or not path.isfile(json_file):
            errormsg(_("Could not read json file."))
            return

        with open(json_file, 'r') as font_data:
            data = json.load(font_data)

        kerning_pairs = {key: val for key, val in self.kerning_pairs.items() if val != 0}
        data['kerning_pairs'] = kerning_pairs

        # write data to font.json into the same directory as the font file
        with open(json_file, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)

        self.GetTopLevelParent().Close()

    def duplicate_warning(self):
        # warn about duplicated glyphs
        if len(set(self.font.available_glyphs)) != len(self.font.available_glyphs):
            duplicated_glyphs = " ".join(
                [glyph for glyph in set(self.font.available_glyphs) if self.font.available_glyphs.count(glyph) > 1]
            )
            errormsg(_("Found duplicated glyphs in font file: {duplicated_glyphs}").format(duplicated_glyphs=duplicated_glyphs))

    def cancel(self, event):
        self.GetTopLevelParent().Close()

    def update_preview(self, event=None):
        self.preview_renderer.update()

    def update_lettering(self):
        del self.layer[:]

        variant = self.font.variants[self.font.default_variant]
        text = self.get_active_kerning_pair()
        if not text:
            return

        text = self.text_before + text + self.text_after

        last_character = None
        position_x = 0
        for character in text:
            glyph = variant[character]
            if character == " " or (glyph is None and self.font.default_glyph == " "):
                position_x += self.font.word_spacing
                last_character = None
            else:
                if glyph is None:
                    glyph = variant[self.font.default_glyph]

                if glyph is not None:
                    node = deepcopy(glyph.node)
                    if last_character is not None:
                        position_x += glyph.min_x - self.kerning_pairs.get(last_character + character, 0)

                    transform = f"translate({position_x}, 0)"
                    node.set('transform', transform)

                    horiz_adv_x_default = self.font.horiz_adv_x_default
                    if horiz_adv_x_default is None:
                        horiz_adv_x_default = glyph.width + glyph.min_x

                    position_x += self.font.horiz_adv_x.get(character, horiz_adv_x_default) - glyph.min_x

                    self.font._update_commands(node, glyph)
                    self.font._update_clips(self.layer, node, glyph)

                    # this is used to recognize a glyph layer later in the process
                    # because this is not unique it will be overwritten by inkscape when inserted into the document
                    node.set("id", "glyph")
                    self.layer.add(node)
                    last_character = character

    def render_stitch_plan(self):
        stitch_groups = []
        try:
            self.update_lettering()
            elements = nodes_to_elements(self.layer.iterdescendants(SVG_PATH_TAG))
            last_stitch_group = None
            for element in elements:
                check_stop_flag()
                stitch_groups.extend(element.embroider(last_stitch_group))
                if stitch_groups:
                    last_stitch_group = stitch_groups[-1]

            if stitch_groups:
                return stitch_groups_to_stitch_plan(
                    stitch_groups,
                    collapse_len=self.metadata['collapse_len_mm'],
                    min_stitch_len=self.metadata['min_stitch_len_mm']
                )
        except SystemExit:
            raise
        except ExitThread:
            raise
        except Exception:
            raise
            # Ignore errors.  This can be things like incorrect paths for
            # satins or division by zero caused by incorrect param values.
            pass

    def on_stitch_plan_rendered(self, stitch_plan):
        self.simulator.stop()
        self.simulator.load(stitch_plan)
        self.simulator.go()


class EditableListCtrl(wx.ListCtrl, TextEditMixin):

    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        TextEditMixin.__init__(self)

    def OpenEditor(self, column, row):
        self.original_data = self.GetItemText(row, column)
        if column == 2:
            TextEditMixin.OpenEditor(self, column, row)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_escape)

    def on_escape(self, event=None):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.CloseEditor(event=None, swap=True)
        event.Skip()

    def CloseEditor(self, event=None, swap=False):
        text = self.editor.GetValue()
        if swap:
            self.editor.Hide()
            TextEditMixin.CloseEditor(self, event)
            return

        if text:
            try:
                float(text)
            except ValueError:
                swap = True

            if swap:
                self.editor.SetValue(self.original_data)

        TextEditMixin.CloseEditor(self, event)
