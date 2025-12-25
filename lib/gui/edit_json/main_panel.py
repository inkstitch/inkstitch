# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
from collections import defaultdict
from copy import deepcopy
from itertools import combinations_with_replacement
from os import path

import wx
import wx.adv
from inkex import errormsg

from ...elements import nodes_to_elements
from ...exceptions import InkstitchException, format_uncaught_exception
from ...i18n import _
from ...lettering import get_font_list
from ...lettering.categories import FONT_CATEGORIES
from ...lettering.font_variant import FontVariant
from ...stitch_plan import stitch_groups_to_stitch_plan
from ...svg.tags import SVG_PATH_TAG
from ...utils.settings import global_settings
from ...utils.threading import ExitThread, check_stop_flag
from .. import PreviewRenderer, WarningPanel
from . import HelpPanel, SettingsPanel

LETTER_CASE = {0: '', 1: 'upper', 2: 'lower'}


class LetteringEditJsonPanel(wx.Panel):

    def __init__(self, parent, simulator, layer, metadata=None, background_color='white'):
        self.parent = parent
        self.simulator = simulator
        self.layer = layer
        self.metadata = metadata or dict()
        self.background_color = background_color

        self.fonts = None
        self.font = None
        self.default_variant = None
        self.font_meta = defaultdict(list)
        self.glyphs = []
        self.kerning_pairs = None
        self.kerning_combinations = []
        self.horiz_adv_x = {}

        self.text_before = ''
        self.text_after = ''

        self.last_notebook_selection = 4

        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        # preview
        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)

        # warning
        self.warning_panel = WarningPanel(self)
        self.warning_panel.Hide()

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        notebook_sizer.Add(self.warning_panel, 0, wx.EXPAND | wx.ALL, 10)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings = wx.Panel(self.notebook, wx.ID_ANY)
        self.settings_panel = SettingsPanel(self.notebook)
        self.notebook.AddPage(self.settings_panel, _("Settings"))
        self.notebook.AddPage(HelpPanel(self.notebook), _("Help"))

        self.SetSizer(notebook_sizer)

        self.set_font_list()
        select_font = global_settings['last_font']
        self.settings_panel.font_chooser.SetValue(select_font)
        self.on_font_changed()

        self.SetSizeHints(notebook_sizer.CalcMin())
        self.Layout()

    def _hide_warning(self):
        self.warning_panel.clear()
        self.warning_panel.Hide()
        self.Layout()

    def _show_warning(self, warning_text):
        self.warning_panel.set_warning_text(warning_text)
        self.warning_panel.Show()
        self.Layout()

    def on_text_before_changed(self, event):
        self.text_before = event.GetEventObject().GetValue()
        self.update_preview()

    def on_text_after_changed(self, event):
        self.text_after = event.GetEventObject().GetValue()
        self.update_preview()

    def on_glyphlist_update(self, event=None):
        item = event.GetItem()
        value = None
        try:
            value = float(item.GetText())
        except ValueError:
            pass
        if value == self.font_meta['horiz_adv_x_default']:
            self.settings_panel.glyph_list.CheckItem(event.Index)
        else:
            self.settings_panel.glyph_list.CheckItem(event.Index, False)
        self.update_preview()
        event.Skip()

    def on_kerning_update(self, event=None):
        self.update_preview()
        event.Skip()

    def on_kerning_list_select(self, event=None):
        self.update_preview()
        event.Skip()

    def on_horiz_adv_x_default_changed(self, event=None):
        value = event.GetValue()
        if not self.settings_panel.font_kerning.horiz_adv_x_default_null_checkbox.IsChecked():
            self.update_horiz_adv_x_default(value)

    def on_horiz_adv_x_default_checkbox_changed(self, event=None):
        value = event.IsChecked()
        if value is False:
            value = self.settings_panel.font_kerning.horiz_adv_x_default.GetValue()
        else:
            value = None
        self.update_horiz_adv_x_default(value)

    def update_horiz_adv_x_default(self, value):
        self.font_meta['horiz_adv_x_default'] = value
        glyph_list = self.settings_panel.glyph_list
        for i in range(glyph_list.ItemCount):
            checked = glyph_list.IsItemChecked(i)
            glyph = glyph_list.GetItem(i, 1).Text
            if checked:
                self.horiz_adv_x[glyph] = self.font_meta['horiz_adv_x_default']
            self.update_preview()

    def on_font_meta_value_changed(self, name, needs_update, event=None):
        self.font_meta[name] = event.GetEventObject().GetValue()
        if needs_update:
            self.update_preview()

    def on_keyword_changed(self, event=None):
        keywords = []
        selections = self.settings_panel.font_info.keywords.GetSelections()
        for selection in selections:
            cat_name = self.settings_panel.font_info.keywords.GetString(selection)
            for category in FONT_CATEGORIES:
                if cat_name == category.name:
                    keywords.append(category.id)
        self.font_meta['keywords'] = keywords

    def on_combine_indices_changed(self, event=None):
        indices = self.settings_panel.font_settings.combine_at_sort_indices.GetValue()
        if not indices:
            self.font_meta['combine_at_sort_indices'] = ''
            return
        indices = indices.split(',')
        try:
            indices = [int(i) for i in indices]
        except ValueError:
            self.settings_panel.font_settings.combine_at_sort_indices.SetForegroundColour('red')
            return
        self.settings_panel.font_settings.combine_at_sort_indices.SetForegroundColour(wx.NullColour)
        self.font_meta['combine_at_sort_indices'] = indices

    def on_default_variant_change(self, event=None):
        selection = self.settings_panel.font_settings.default_variant.GetSelection()
        value = 'ltr'
        if selection == 1:
            value = 'rtl'
        elif selection == 2:
            value = 'ttb'
        elif selection == 3:
            value = 'btt'
        self.font_meta['default_variant'] = value
        self.update_preview()

    def on_text_direction_changed(self, event=None):
        selection = self.settings_panel.font_info.text_direction.GetSelection()
        value = 'ltr'
        if selection == 1:
            value = 'rtl'
        self.font_meta['text_direction'] = value
        self.update_preview()

    def on_letter_case_change(self, event=None):
        selection = self.settings_panel.font_settings.letter_case.GetSelection()
        value = ''
        if selection == 1:
            value = 'upper'
        elif selection == 2:
            value = 'lower'
        self.font_meta['letter_case'] = value

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
                self.settings_panel.font_chooser.Append(font.marked_custom_font_name, wx.Bitmap(image))
            else:
                self.settings_panel.font_chooser.Append(font.marked_custom_font_name)

    def get_active_kerning_pair(self):
        kerning_list = self.settings_panel.kerning_list
        selection = kerning_list.GetFirstSelected()
        if selection == -1:
            return ''
        kerning_pair = kerning_list.GetItem(selection, 0).Text
        kerning = float(kerning_list.GetItem(selection, 1).Text)
        if kerning_list.GetItem(selection, 2).Text:
            try:
                kerning = float(kerning_list.GetItem(selection, 2).Text)
                self.kerning_pairs[kerning_pair] = float(kerning)
            except (ValueError, IndexError):
                pass
        return kerning_pair

    def on_glyph_item_checked(self, event=None):
        self.get_active_glyph(event.Index)
        self.update_preview()

    def get_active_glyph(self, index=None):
        glyph_list = self.settings_panel.glyph_list
        if index is not None:
            selection = index
        else:
            selection = glyph_list.GetFirstSelected()
        if selection == -1:
            return ''
        glyph = glyph_list.GetItem(selection, 1).Text
        if glyph_list.IsItemChecked(selection):
            self.horiz_adv_x[glyph] = self.font_meta['horiz_adv_x_default']
            return glyph
        horiz_adv_x = None
        try:
            horiz_adv_x = float(glyph_list.GetItem(selection, 2).Text)
        except (ValueError, IndexError):
            pass
        if glyph_list.GetItem(selection, 3).Text:
            try:
                horiz_adv_x = float(glyph_list.GetItem(selection, 3).Text)
                self.horiz_adv_x[glyph] = float(horiz_adv_x)
            except (ValueError, IndexError):
                pass
        return glyph

    def on_font_changed(self, event=None):
        selected_font = self.settings_panel.font_chooser.GetValue()
        if selected_font:
            self.font = self.fonts[selected_font]
        else:
            first = list(self.fonts.values())[0].marked_custom_font_name
            self.font = self.fonts[first]
            self.settings_panel.font_chooser.SetValue(first)
        global_settings['last_font'] = self.font.marked_custom_font_name
        self.kerning_pairs = self.font.kerning_pairs
        self.font._load_variants()
        self.default_variant = self.font.variants[self.font.json_default_variant]
        self.glyphs = list(self.default_variant.glyphs.keys())
        self.glyphs.sort()
        self.horiz_adv_x = self.font.horiz_adv_x

        kerning_combinations = combinations_with_replacement(self.glyphs, 2)
        self.kerning_combinations = []
        for combination in kerning_combinations:
            self.kerning_combinations.append(f'{combination[0]} {combination[1]}')
            self.kerning_combinations.append(f'{combination[1]} {combination[0]}')
        self.kerning_combinations = list(set(self.kerning_combinations))
        self.kerning_combinations.sort()

        self.update_legacy_kerning_pairs()
        self.update_settings()
        self.update_kerning_list()
        self.update_filter_list()
        self.update_glyph_list()
        self.update_preview()
        self.writability_warning()

    def update_legacy_kerning_pairs(self):
        new_list = defaultdict(list)
        for kerning_pair, value in self.kerning_pairs.items():
            if " " in kerning_pair:
                # legacy kerning pairs do not use a space
                return
            if len(kerning_pair) < 2:
                continue
            pair = f'{kerning_pair[0]} {kerning_pair[1]}'
            new_list[pair] = value
        self.kerning_pairs = new_list

    def update_settings(self):
        # reset font_meta
        self.font_meta = defaultdict(list)
        self.font_meta['name'] = self.font.name
        self.font_meta['description'] = self.font.metadata['description']  # untranslated description
        self.font_meta['font_license'] = self.font.metadata['font_license']
        self.font_meta['text_direction'] = self.font.text_direction
        self.font_meta['keywords'] = self.font.keywords
        self.font_meta['original_font'] = self.font.original_font
        self.font_meta['original_font_url'] = self.font.original_font_url
        self.font_meta['default_variant'] = self.font.json_default_variant
        self.font_meta['default_glyph'] = self.font.default_glyph
        self.font_meta['auto_satin'] = self.font.auto_satin
        self.font_meta['letter_case'] = self.font.letter_case
        self.font_meta['reversible'] = self.font.reversible
        self.font_meta['sortable'] = self.font.sortable
        self.font_meta['combine_at_sort_indices'] = self.font.combine_at_sort_indices
        self.font_meta['leading'] = self.font.leading
        self.font_meta['size'] = self.font.size
        self.font_meta['max_scale'] = self.font.max_scale
        self.font_meta['min_scale'] = self.font.min_scale
        self.font_meta['horiz_adv_x_default'] = self.font.horiz_adv_x_default
        self.font_meta['horiz_adv_x_space'] = self.font.word_spacing

        # update ctrl
        self.settings_panel.font_info.name.ChangeValue(self.font.name)
        self.settings_panel.font_info.description.ChangeValue(self.font.metadata['description'])
        self.settings_panel.font_info.font_license.ChangeValue(self.font.metadata['font_license'])
        selection = ['ltr', 'rtl', 'ttb', 'btt'].index(self.font.json_default_variant)
        self.settings_panel.font_settings.default_variant.SetSelection(selection)
        selection = ['ltr', 'rtl'].index(self.font.text_direction)
        self.settings_panel.font_info.text_direction.SetSelection(selection)
        self.settings_panel.font_info.keywords.SetSelection(-1)
        for category in FONT_CATEGORIES:
            if category.id in self.font.keywords:
                self.settings_panel.font_info.keywords.SetStringSelection(category.name)
        self.settings_panel.font_info.original_font.ChangeValue(self.font.original_font)
        self.settings_panel.font_info.original_font_url.ChangeValue(self.font.original_font_url)
        self.settings_panel.font_settings.default_glyph.ChangeValue(self.font.default_glyph)
        self.settings_panel.font_settings.auto_satin.SetValue(self.font.auto_satin)
        selection = list(LETTER_CASE.keys())[list(LETTER_CASE.values()).index(self.font.letter_case)]
        self.settings_panel.font_settings.letter_case.SetSelection(selection)
        self.settings_panel.font_settings.reversible.SetValue(self.font.reversible)
        self.settings_panel.font_settings.sortable.SetValue(self.font.sortable)
        self.settings_panel.font_settings.combine_at_sort_indices.ChangeValue(
            ', '.join([str(i) for i in self.font.combine_at_sort_indices])
        )
        self.settings_panel.font_kerning.leading.SetValue(self.font.leading)
        self.settings_panel.font_kerning.size.SetValue(self.font.size)
        self.settings_panel.font_kerning.max_scale.SetValue(self.font.max_scale)
        self.settings_panel.font_kerning.min_scale.SetValue(self.font.min_scale)
        if self.font.horiz_adv_x_default is None:
            self.settings_panel.font_kerning.horiz_adv_x_default.SetValue(0.0)
            self.settings_panel.font_kerning.horiz_adv_x_default_null_checkbox.SetValue(True)
        else:
            self.settings_panel.font_kerning.horiz_adv_x_default.SetValue(self.font.horiz_adv_x_default)
            self.settings_panel.font_kerning.horiz_adv_x_default_null_checkbox.SetValue(False)
        self.settings_panel.font_kerning.horiz_adv_x_space.SetValue(self.font.word_spacing)

    def update_filter_list(self):
        # Update filter list
        self.settings_panel.kerning_filter.Clear()
        choices = [' '] + self.glyphs
        self.settings_panel.kerning_filter.AppendItems(choices)
        self.settings_panel.kerning_filter.update_choices(choices)

    def update_kerning_list(self, filter_value=None):
        kerning_list = self.settings_panel.kerning_list
        # Add the rows
        kerning_list.ClearAll()
        # Add some columns
        kerning_list.AppendColumn("Kerning pair", width=wx.LIST_AUTOSIZE_USEHEADER)
        kerning_list.AppendColumn("Current kerning", width=wx.LIST_AUTOSIZE_USEHEADER)
        kerning_list.AppendColumn("New kerning", width=wx.LIST_AUTOSIZE_USEHEADER)
        for kerning_pair in self.kerning_combinations:
            if filter_value is not None and filter_value.strip() not in kerning_pair:
                continue
            if self.font_meta['text_direction'] == 'rtl':
                pair = kerning_pair.split()
                kerning_pair = ' '.join(pair[::-1])
            index = kerning_list.InsertItem(kerning_list.GetItemCount(), kerning_pair)
            # kerning_list.SetItem(index, 0, kerning_pair)
            kerning_list.SetItem(index, 1, str(self.kerning_pairs.get(kerning_pair, 0.0)))
        if kerning_list.GetItemCount() != 0:
            kerning_list.Select(0)
            kerning_list.Focus(0)

    def update_glyph_list(self):
        glyph_list = self.settings_panel.glyph_list
        # Add the rows
        glyph_list.ClearAll()
        # Add some columns
        glyph_list.AppendColumn("Use default", width=wx.LIST_AUTOSIZE_USEHEADER)
        glyph_list.AppendColumn("Glyph", width=wx.LIST_AUTOSIZE_USEHEADER)
        glyph_list.AppendColumn("Current horizontal advance", width=wx.LIST_AUTOSIZE_USEHEADER)
        glyph_list.AppendColumn("New horizontal advance", width=wx.LIST_AUTOSIZE_USEHEADER)
        horiz_adv_x_default = self.font.horiz_adv_x_default
        for glyph in self.glyphs:
            index = glyph_list.InsertItem(glyph_list.GetItemCount(), '')
            horiz_adv = self.font.horiz_adv_x.get(glyph, horiz_adv_x_default)
            if horiz_adv == horiz_adv_x_default:
                glyph_list.CheckItem(index)
            glyph_list.SetItem(index, 1, glyph)
            glyph_list.SetItem(index, 2, str(horiz_adv))
        if glyph_list.GetItemCount() != 0:
            glyph_list.Select(0)
            glyph_list.Focus(0)

    def writability_warning(self):
        json_file = path.join(self.font.path, 'font.json')

        if not path.isfile(json_file) or not path.isfile(json_file):
            self._show_warning(_("Could not read json file."))
            return

        if not os.access(json_file, os.W_OK):
            self._show_warning(_("Changes will not be saved: cannot write to json file (permission denied)."))
            return

        self._hide_warning()

    def apply(self, event):
        json_file = path.join(self.font.path, 'font.json')

        if not path.isfile(json_file) or not path.isfile(json_file):
            errormsg(_("Could not read json file."))
            self.cancel()
            return

        if not os.access(json_file, os.W_OK):
            errormsg(_("Could not write to json file: permission denied."))
            self.cancel()
            return

        with open(json_file, 'r') as font_data:
            data = json.load(font_data)

        for key, val in self.font_meta.items():
            data[key] = val
        horiz_adv_x = {key: val for key, val in self.horiz_adv_x.items() if key and val != self.font_meta['horiz_adv_x_default']}
        kerning_pairs = {key: val for key, val in self.kerning_pairs.items() if val != 0}
        data['horiz_adv_x'] = horiz_adv_x
        data['kerning_pairs'] = kerning_pairs
        data['glyphs'] = self.glyphs

        # write data to font.json into the same directory as the font file
        with open(json_file, 'w', encoding="utf8") as font_data:
            json.dump(data, font_data, indent=4, ensure_ascii=False)

        self.GetTopLevelParent().Close()

    def cancel(self, event):
        self.GetTopLevelParent().Close()

    def update_preview(self, event=None):
        self.preview_renderer.update()

    def update_lettering(self):
        del self.layer[:]

        if self.settings_panel.notebook.GetSelection() in [3, 4]:
            self.last_notebook_selection = self.settings_panel.notebook.GetSelection()

        if self.last_notebook_selection == 3:
            text = self.get_active_glyph()
        else:
            kerning = self.get_active_kerning_pair()
            kerning = kerning.split()
            text = ''.join(kerning)
            if self.font_meta['text_direction'] == 'rtl':
                text = ''.join(kerning[::-1])
        if not text:
            return

        position_x = self._render_text(self.text_before, 0, True)
        position_x = self._render_text(text, position_x, False)
        self._render_text(self.text_after, position_x, True)

        if self.default_variant.variant == FontVariant.RIGHT_TO_LEFT:
            self.layer[:] = reversed(self.layer)
            for group in self.layer:
                group[:] = reversed(group)

    def _render_text(self, text, position_x, use_character_position):
        words = text.split()
        for i, word in enumerate(words):
            glyphs = []
            skip = []
            previous_is_binding = False
            for i, character in enumerate(word):
                if i in skip:
                    continue
                if use_character_position:
                    glyph, glyph_len, previous_is_binding = self.default_variant.get_next_glyph(word, i, previous_is_binding)
                else:
                    glyph, glyph_len = self.default_variant.get_glyph(character, word[i:])
                glyphs.append(glyph)
                skip = list(range(i, i+glyph_len))

            last_character = None
            for glyph in glyphs:
                if glyph is None:
                    position_x += self.font_meta['horiz_adv_x_space']
                    last_character = None
                    continue

                position_x = self._render_glyph(glyph, position_x, glyph.name, last_character)
                last_character = glyph.name
            position_x += self.font_meta['horiz_adv_x_space']
        position_x -= self.font_meta['horiz_adv_x_space']
        return position_x

    def _render_glyph(self, glyph, position_x, character, last_character):
        node = deepcopy(glyph.node)
        if last_character is not None:
            if self.font_meta['text_direction'] != 'rtl':
                position_x += glyph.min_x - self.kerning_pairs.get(f'{last_character} {character}', 0)
            else:
                position_x += glyph.min_x - self.kerning_pairs.get(f'{character} {last_character}', 0)

        transform = f"translate({position_x}, 0)"
        node.set('transform', transform)

        horiz_adv_x_default = self.font_meta['horiz_adv_x_default']
        if horiz_adv_x_default is None:
            horiz_adv_x_default = glyph.width + glyph.min_x

        horiz_adv_x = self.font.horiz_adv_x.get(character, horiz_adv_x_default)
        # in some rare cases, horiz_adv_x for a character returns None
        # so we need to really ensure that the default is used in this case
        if horiz_adv_x is None:
            horiz_adv_x = horiz_adv_x_default
        position_x += horiz_adv_x - glyph.min_x

        self.font._update_commands(node, glyph)
        self.font._update_clips(self.layer, node, glyph)

        # this is used to recognize a glyph layer later in the process
        # because this is not unique it will be overwritten by inkscape when inserted into the document
        node.set("id", "glyph")
        self.layer.add(node)
        return position_x

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
        except (SystemExit, ExitThread):
            raise
        except InkstitchException as exc:
            wx.CallAfter(self._show_warning, str(exc))
        except Exception:
            wx.CallAfter(self._show_warning, format_uncaught_exception())

    def on_stitch_plan_rendered(self, stitch_plan):
        self.simulator.stop()
        self.simulator.load(stitch_plan)
        self.simulator.go()
