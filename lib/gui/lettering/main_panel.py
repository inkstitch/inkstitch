# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from base64 import b64decode

import inkex
import wx
import wx.adv

from ...elements import iterate_nodes, nodes_to_elements
from ...i18n import _
from ...lettering import FontError, get_font_list
from ...lettering.categories import FONT_CATEGORIES
from ...stitch_plan import stitch_groups_to_stitch_plan
from ...svg.tags import INKSTITCH_LETTERING
from ...utils import DotDict, cache
from ...utils.settings import global_settings
from ...utils.threading import ExitThread, check_stop_flag
from .. import PresetsPanel, PreviewRenderer, info_dialog
from . import LetteringHelpPanel, LetteringOptionsPanel


class LetteringPanel(wx.Panel):
    def __init__(self, parent, simulator, group, metadata=None, background_color='white'):
        self.parent = parent
        self.simulator = simulator
        self.group = group
        self.metadata = metadata or dict()
        self.background_color = background_color

        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)

        # notebook
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.options_panel = LetteringOptionsPanel(self.notebook, self)
        self.notebook.AddPage(self.options_panel, _("Options"))
        help_panel = LetteringHelpPanel(self.notebook)
        self.notebook.AddPage(help_panel, _("Help"))
        outer_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)

        # presets
        self.presets_panel = PresetsPanel(self)
        outer_sizer.Add(self.presets_panel, 0, wx.EXPAND | wx.ALL, 10)

        # buttons
        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.cancel_button, 0, wx.RIGHT, 10)
        buttons_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT, 10)

        # set font list
        self.update_font_list()
        self.set_font_list()

        self.SetSizerAndFit(outer_sizer)

        self.load_settings()
        self.apply_settings()

    def load_settings(self):
        """Load the settings saved into the SVG group element"""

        self.settings = DotDict({
            "text": "",
            "text_align": global_settings['lettering_align_text'],
            "back_and_forth": False,
            "font": None,
            "scale": 100,
            "trim_option": global_settings['lettering_trim_option'],
            "use_trim_symbols": global_settings['lettering_use_command_symbols'],
            "color_sort": 0,
            "letter_spacing": 0,
            "word_spacing": 0,
            "line_height": 0
        })

        if INKSTITCH_LETTERING in self.group.attrib:
            try:
                self.settings.update(json.loads(self.group.get(INKSTITCH_LETTERING)))
            except json.decoder.JSONDecodeError:
                # legacy base64 encoded (changed in v2.0)
                try:
                    self.settings.update(json.loads(b64decode(self.group.get(INKSTITCH_LETTERING))))
                except (TypeError, ValueError):
                    pass
            except (TypeError, ValueError):
                pass

    def apply_settings(self):
        """Make the settings in self.settings visible in the UI."""
        self.options_panel.align_text_choice.SetSelection(self.settings.text_align)
        self.options_panel.color_sort_choice.SetSelection(self.settings.color_sort)
        self.options_panel.back_and_forth_checkbox.SetValue(bool(self.settings.back_and_forth))
        self.options_panel.trim_option_choice.SetSelection(self.settings.trim_option)
        self.options_panel.use_trim_symbols.SetValue(bool(self.settings.use_trim_symbols))
        self.options_panel.text_editor.SetValue(self.settings.text)
        self.options_panel.scale_spinner.SetValue(self.settings.scale)
        self.options_panel.letter_spacing.SetValue(self.settings.letter_spacing)
        self.options_panel.word_spacing.SetValue(self.settings.word_spacing)
        self.options_panel.line_height.SetValue(self.settings.line_height)
        self.set_initial_font(self.settings.font)

    def save_settings(self):
        """Save the settings into the SVG group element."""
        self.group.set(INKSTITCH_LETTERING, json.dumps(self.settings))

    @property
    @cache
    def font_list(self):
        return get_font_list(False)

    def update_font_list(self):
        self.fonts = {}
        self.fonts_by_id = {}

        # font size filter value

        filter_size = self.options_panel.font_size_filter.GetValue()
        filter_glyph = self.options_panel.font_glyph_filter.GetValue()
        filter_category = self.options_panel.font_category_filter.GetSelection() - 1

        # Set of all glyphs in input string (except whitespace characters), normalized in the same way that we normalize font glyphs
        # do not normalize the glyphs yet, available_glyphs are not normalized in the font json file
        # glyphs = set(l for l  in  unicodedata.normalize("NFC", self.options_panel.text_editor.GetValue().replace(r"\s", "")))

        glyphs = set(letter for letter in self.options_panel.text_editor.GetValue().replace(r"\s", ""))

        for font in self.font_list:
            if filter_glyph and glyphs and not glyphs.issubset(font.available_glyphs):
                continue

            if filter_category != -1:
                category = FONT_CATEGORIES[filter_category].id
                if category not in font.keywords:
                    continue

            if filter_size != 0 and (filter_size < font.size * font.min_scale or filter_size > font.size * font.max_scale):
                continue

            self.fonts[font.marked_custom_font_name] = font
            self.fonts_by_id[font.marked_custom_font_id] = font

    def set_font_list(self):
        self.options_panel.font_chooser.Clear()
        for font in self.fonts.values():
            image = font.preview_image

            if image is not None:
                image = wx.Image(image)
                """
                # I would like to do this but Windows requires all images to be the exact same size
                # It might work with an updated wxpython version - so let's keep it here

                # Scale to max 20 height
                img_height = 20
                width, height = image.GetSize()
                scale_factor = height / img_height
                width = int(width / scale_factor)
                image.Rescale(width, img_height, quality=wx.IMAGE_QUALITY_HIGH)
                """
                # Windows requires all images to have the exact same size
                image.Rescale(300, 20, quality=wx.IMAGE_QUALITY_HIGH)
                self.options_panel.font_chooser.Append(font.marked_custom_font_name, wx.Bitmap(image))
            else:
                self.options_panel.font_chooser.Append(font.marked_custom_font_name)

    def set_initial_font(self, font_id):
        if font_id:
            if font_id not in self.fonts_by_id:
                message = '''This text was created using the font "%s", but Ink/Stitch can't find that font.  ''' \
                          '''A default font will be substituted.'''
                info_dialog(self, _(message) % font_id)
        try:
            font = self.fonts_by_id[font_id].marked_custom_font_name
        except KeyError:
            font = self.default_font.marked_custom_font_name
        self.options_panel.font_chooser.SetValue(font)

        self.on_font_changed()

    @property
    def default_font(self):
        try:
            return self.fonts[global_settings['last_font']]
        except KeyError:
            return list(self.fonts.values())[0]

    def on_change(self, attribute, event):
        value = event.GetEventObject().GetValue()
        self.settings[attribute] = value
        if attribute == "text" and self.options_panel.font_glyph_filter.GetValue() is True:
            self.on_filter_changed()
        if attribute == "use_trim_symbols":
            global_settings['lettering_use_command_symbols'] = value
        self.update_preview()

    def on_color_sort_change(self, event=None):
        if self.options_panel.color_sort_choice.IsEnabled():
            self.settings.color_sort = self.options_panel.color_sort_choice.GetCurrentSelection()
        else:
            self.settings.color_sort = 0
        self.update_preview()

    def on_choice_change(self, attribute, event=None):
        value = event.GetEventObject().GetCurrentSelection()
        self.settings[attribute] = value
        if attribute == 'trim_option':
            global_settings['lettering_trim_option'] = value
        elif attribute == 'text_align':
            global_settings['lettering_align_text'] = value
        self.update_preview()

    def on_font_changed(self, event=None):
        font = self.fonts.get(self.options_panel.font_chooser.GetValue(), self.default_font)
        self.settings.font = font.marked_custom_font_id
        global_settings['last_font'] = font.marked_custom_font_name

        filter_size = self.options_panel.font_size_filter.GetValue()
        self.options_panel.scale_spinner.SetRange(int(font.min_scale * 100), int(font.max_scale * 100))
        if filter_size != 0:
            self.options_panel.scale_spinner.SetValue(int(filter_size / font.size * 100))
        self.settings['scale'] = self.options_panel.scale_spinner.GetValue()

        font_variants = []
        try:
            font_variants = font.has_variants()
        except FontError:
            pass

        # Update font description
        color = wx.NullColour
        description = font.description
        if len(font_variants) == 0:
            color = (255, 0, 0)
            description = _('This font has no available font variant. Please update or remove the font.')
        self.options_panel.font_description.SetLabel(description)
        self.options_panel.font_description.SetForegroundColour(color)
        self.options_panel.font_description.Wrap(self.options_panel.GetSize().width - 50)
        self.options_panel.size_info.SetLabel(str(font.size))
        self.options_panel.scale_info_percent.SetLabel(f'{int(font.min_scale * 100)}% - {int(font.max_scale * 100)}%')
        self.options_panel.scale_info_mm.SetLabel(f' ({round(font.size * font.min_scale, 2)}mm - {round(font.size * font.max_scale, 2)}mm)')

        if font.reversible:
            self.options_panel.back_and_forth_checkbox.Enable()
            self.options_panel.back_and_forth_checkbox.SetValue(bool(self.settings.back_and_forth))
        else:
            # The creator of the font banned the possibility of writing in reverse with json file: "reversible": false
            self.options_panel.back_and_forth_checkbox.Disable()
            self.options_panel.back_and_forth_checkbox.SetValue(False)

        if font.sortable:
            # The creator of the font allowed color sorting: "sortable": true
            self.options_panel.color_sort_choice.Enable()
        else:
            self.options_panel.color_sort_choice.Disable()

        self.options_panel.Layout()
        self.update_preview()

    def on_filter_changed(self, event=None):
        self.update_font_list()

        if not self.fonts:
            # No fonts for filtered size
            self.options_panel.font_chooser.Clear()
            self.options_panel.filter_box.SetForegroundColour("red")
            return
        else:
            self.options_panel.filter_box.SetForegroundColour(wx.NullColour)

        filter_size = self.options_panel.font_size_filter.GetValue()
        previous_font = self.options_panel.font_chooser.GetValue()
        self.set_font_list()
        font = self.fonts.get(previous_font, self.default_font)
        self.options_panel.font_chooser.SetValue(font.marked_custom_font_name)
        if font.marked_custom_font_name != previous_font:
            self.on_font_changed()
        elif filter_size != 0:
            self.options_panel.scale_spinner.SetValue(int(filter_size / font.size * 100))
            self.settings['scale'] = self.options_panel.scale_spinner.GetValue()
            self.update_preview()

    def resize(self, event=None):
        description = self.options_panel.font_description.GetLabel().replace("\n", " ")
        self.options_panel.font_description.SetLabel(description)
        self.options_panel.font_description.Wrap(self.options_panel.GetSize().width - 50)
        self.Layout()

    def update_preview(self, event=None):
        self.preview_renderer.update()

    def update_lettering(self, raise_error=False):
        # return if there is no font in the font list (possibly due to a font size filter)
        if not self.options_panel.font_chooser.GetValue():
            return

        del self.group[:]

        destination_group = inkex.Group()
        self.group.append(destination_group)

        font = self.fonts.get(self.options_panel.font_chooser.GetValue(), self.default_font)
        destination_group.label = f"{font.name} {_('scale')} {self.settings.scale}%"
        try:
            font.render_text(
                self.settings.text, destination_group, back_and_forth=self.settings.back_and_forth,
                trim_option=self.settings.trim_option, use_trim_symbols=self.settings.use_trim_symbols,
                color_sort=self.settings.color_sort, text_align=self.settings.text_align,
                letter_spacing=self.settings.letter_spacing, word_spacing=self.settings.word_spacing, line_height=self.settings.line_height
            )
        except FontError as e:
            if raise_error:
                inkex.errormsg(_("Error: Text cannot be applied to the document.\n%s") % e)
                return
            else:
                pass

        # the text scaling group label is dependent on the user language, so it would break in international file exchange if we used it
        # scaling (correction transform) on the parent group is already applied, so let's use that for recognition
        if destination_group.get('transform', None) is None:
            destination_group.attrib['transform'] = 'scale(%s)' % (self.settings.scale / 100.0)

    def render_stitch_plan(self):
        stitch_groups = []

        try:
            self.update_lettering()
            nodes = iterate_nodes(self.group)
            elements = nodes_to_elements(nodes)

            last_stitch_group = None
            next_elements = [None]
            if len(elements) > 1:
                next_elements = elements[1:] + next_elements
            for element, next_element in zip(elements, next_elements):
                check_stop_flag()

                stitch_groups.extend(element.embroider(last_stitch_group, next_element))

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

    def get_preset_data(self):
        # called by self.presets_panel
        settings = dict(self.settings)
        del settings["text"]
        return settings

    def apply_preset_data(self, preset_data):
        settings = DotDict(preset_data)
        settings["text"] = self.settings.text
        self.settings = settings
        self.apply_settings()

    def get_preset_suite_name(self):
        # called by self.presets_panel
        return "lettering"

    def apply(self, event):
        self.update_lettering(True)
        self.save_settings()
        self.close()

    def close(self):
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().close)

    def cancel(self, event):
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().cancel)
