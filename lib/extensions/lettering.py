# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import sys
from base64 import b64decode

import appdirs
import inkex
import wx
import wx.adv
import wx.lib.agw.floatspin as fs

from ..elements import nodes_to_elements
from ..gui import PresetsPanel, SimulatorPreview, info_dialog
from ..i18n import _
from ..lettering import Font, FontError
from ..svg import get_correction_transform
from ..svg.tags import (INKSCAPE_LABEL, INKSTITCH_LETTERING, SVG_GROUP_TAG,
                        SVG_PATH_TAG)
from ..utils import DotDict, cache, get_bundled_dir, get_resource_dir
from .commands import CommandsExtension
from .lettering_custom_font_dir import get_custom_font_dir


class LetteringFrame(wx.Frame):
    DEFAULT_FONT = "small_font"

    def __init__(self, *args, **kwargs):
        # This is necessary because of https://github.com/inkstitch/inkstitch/issues/1186
        if sys.platform.startswith('win'):
            import locale
            locale.setlocale(locale.LC_ALL, "C")
            lc = wx.Locale()
            lc.Init(wx.LANGUAGE_DEFAULT)

        # begin wxGlade: MyFrame.__init__
        self.group = kwargs.pop('group')
        self.cancel_hook = kwargs.pop('on_cancel', None)
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          _("Ink/Stitch Lettering")
                          )

        icon = wx.Icon(os.path.join(get_resource_dir("icons"), "inkstitch256x256.png"))
        self.SetIcon(icon)

        self.preview = SimulatorPreview(self, target_duration=1)
        self.presets_panel = PresetsPanel(self)

        # font
        self.font_selector_box = wx.StaticBox(self, wx.ID_ANY, label=_("Font"))

        self.font_chooser = wx.adv.BitmapComboBox(self, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT)
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.on_font_changed)

        self.font_filter = fs.FloatSpin(self, min_val=0, max_val=None, increment=1, value="0")
        self.font_filter.SetFormat("%f")
        self.font_filter.SetDigits(2)
        self.font_filter.Bind(fs.EVT_FLOATSPIN, self.on_filter_changed)
        self.font_filter.SetToolTip(_("Font size filter (mm)"))

        self.update_font_list()
        self.set_font_list()

        # font details
        self.font_description = wx.StaticText(self, wx.ID_ANY)
        self.Bind(wx.EVT_SIZE, self.resize)

        # options
        self.options_box = wx.StaticBox(self, wx.ID_ANY, label=_("Options"))

        self.scale_spinner = wx.SpinCtrl(self, wx.ID_ANY, min=100, max=100, initial=100)
        self.scale_spinner.Bind(wx.EVT_SPINCTRL, lambda event: self.on_change("scale", event))

        self.back_and_forth_checkbox = wx.CheckBox(self, label=_("Stitch lines of text back and forth"))
        self.back_and_forth_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.on_change("back_and_forth", event))

        self.trim_checkbox = wx.CheckBox(self, label=_("Add trims"))
        self.trim_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.on_change("trim", event))

        # text editor
        self.text_input_box = wx.StaticBox(self, wx.ID_ANY, label=_("Text"))

        self.text_editor = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP)
        self.text_editor.Bind(wx.EVT_TEXT, lambda event: self.on_change("text", event))

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__do_layout()

        self.load_settings()
        self.apply_settings()

    def load_settings(self):
        """Load the settings saved into the SVG group element"""

        self.settings = DotDict({
            "text": "",
            "back_and_forth": False,
            "font": None,
            "scale": 100
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
        self.back_and_forth_checkbox.SetValue(bool(self.settings.back_and_forth))
        self.trim_checkbox.SetValue(bool(self.settings.trim))
        self.set_initial_font(self.settings.font)
        self.text_editor.SetValue(self.settings.text)
        self.scale_spinner.SetValue(self.settings.scale)

    def save_settings(self):
        """Save the settings into the SVG group element."""
        self.group.set(INKSTITCH_LETTERING, json.dumps(self.settings))

    @property
    @cache
    def font_list(self):
        fonts = []
        font_paths = {
            get_bundled_dir("fonts"),
            os.path.expanduser("~/.inkstitch/fonts"),
            os.path.join(appdirs.user_config_dir('inkstitch'), 'fonts'),
            get_custom_font_dir()
        }

        for font_path in font_paths:
            try:
                font_dirs = os.listdir(font_path)
            except OSError:
                continue

            for font_dir in font_dirs:
                font = Font(os.path.join(font_path, font_dir))
                if font.marked_custom_font_name == "" or font.marked_custom_font_id == "":
                    continue
                fonts.append(font)
        return fonts

    def update_font_list(self):
        self.fonts = {}
        self.fonts_by_id = {}

        filter_size = self.font_filter.GetValue()
        for font in self.font_list:
            if filter_size != 0 and (filter_size < font.size * font.min_scale or filter_size > font.size * font.max_scale):
                continue
            self.fonts[font.marked_custom_font_name] = font
            self.fonts_by_id[font.marked_custom_font_id] = font

    def set_font_list(self):
        self.font_chooser.Clear()
        for font in self.fonts.values():
            image = font.preview_image

            if image is not None:
                image = wx.Image(font.preview_image)
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
                self.font_chooser.Append(font.marked_custom_font_name, wx.Bitmap(image))
            else:
                self.font_chooser.Append(font.marked_custom_font_name)

    def get_font_descriptions(self):
        return {font.name: font.description for font in self.fonts.values()}

    def set_initial_font(self, font_id):
        if font_id:
            if font_id not in self.fonts_by_id:
                message = '''This text was created using the font "%s", but Ink/Stitch can't find that font.  ''' \
                          '''A default font will be substituted.'''
                info_dialog(self, _(message) % font_id)
        try:
            font = self.fonts_by_id[font_id].marked_custom_font_name
        except KeyError:
            font = self.default_font.name
        self.font_chooser.SetValue(font)

        self.on_font_changed()

    @property
    def default_font(self):
        try:
            return self.fonts_by_id[self.DEFAULT_FONT]
        except KeyError:
            return list(self.fonts.values())[0]

    def on_change(self, attribute, event):
        self.settings[attribute] = event.GetEventObject().GetValue()
        self.preview.update()

    def on_font_changed(self, event=None):
        font = self.fonts.get(self.font_chooser.GetValue(), self.default_font)
        self.settings.font = font.marked_custom_font_id

        self.scale_spinner.SetRange(int(font.min_scale * 100), int(font.max_scale * 100))
        self.settings['scale'] = self.scale_spinner.GetValue()

        font_variants = []
        try:
            font_variants = font.has_variants()
        except FontError:
            pass

        # Update font description
        color = (0, 0, 0)
        description = font.description
        if len(font_variants) == 0:
            color = (255, 0, 0)
            description = _('This font has no available font variant. Please update or remove the font.')
        self.font_description.SetLabel(description)
        self.font_description.SetForegroundColour(color)
        self.font_description.Wrap(self.GetSize().width - 35)

        if font.reversible:
            self.back_and_forth_checkbox.Enable()
            self.back_and_forth_checkbox.SetValue(bool(self.settings.back_and_forth))
        else:
            # The creator of the font banned the possibility of writing in reverse with json file: "reversible": false
            self.back_and_forth_checkbox.Disable()
            self.back_and_forth_checkbox.SetValue(False)

        if font.auto_satin:
            self.trim_checkbox.Enable()
            self.trim_checkbox.SetValue(bool(self.settings.trim))
        else:
            self.trim_checkbox.Disable()
            self.trim_checkbox.SetValue(False)

        self.update_preview()
        self.Layout()

    def on_filter_changed(self, event=None):
        self.update_font_list()

        if not self.fonts:
            # No fonts for filtered size
            self.font_chooser.Clear()
            self.filter_label.SetForegroundColour("red")
            return
        else:
            self.filter_label.SetForegroundColour("black")

        previous_font = self.font_chooser.GetValue()
        self.set_font_list()
        font = self.fonts.get(previous_font, self.default_font)
        self.font_chooser.SetValue(font.name)
        if font.name != previous_font:
            self.on_font_changed()

    def resize(self, event=None):
        description = self.font_description.GetLabel().replace("\n", " ")
        self.font_description.SetLabel(description)
        self.font_description.Wrap(self.GetSize().width - 35)
        self.Layout()

    def update_preview(self, event=None):
        self.preview.update()

    def update_lettering(self, raise_error=False):
        # return if there is no font in the font list (possibly due to a font size filter)
        if not self.font_chooser.GetValue():
            return

        del self.group[:]

        if self.settings.scale == 100:
            destination_group = self.group
        else:
            destination_group = inkex.Group(attrib={
                # L10N The user has chosen to scale the text by some percentage
                # (50%, 200%, etc).  If you need to use the percentage symbol,
                # make sure to double it (%%).
                INKSCAPE_LABEL: _("Text scale %s%%") % self.settings.scale
            })
            self.group.append(destination_group)

        font = self.fonts.get(self.font_chooser.GetValue(), self.default_font)
        try:
            font.render_text(self.settings.text, destination_group, back_and_forth=self.settings.back_and_forth, trim=self.settings.trim)
        except FontError as e:
            if raise_error:
                inkex.errormsg(_("Error: Text cannot be applied to the document.\n%s") % e)
                return
            else:
                pass

        # destination_group isn't always the text scaling group (but also the parent group)
        # the text scaling group label is dependend on the user language, so it would break in international file exchange if we used it
        # scaling (correction transform) on the parent group is already applied, so let's use that for recognition
        if self.settings.scale != 100 and not destination_group.get('transform', None):
            destination_group.attrib['transform'] = 'scale(%s)' % (self.settings.scale / 100.0)

    def generate_patches(self, abort_early=None):
        patches = []

        try:
            self.update_lettering()
            elements = nodes_to_elements(self.group.iterdescendants(SVG_PATH_TAG))

            for element in elements:
                if abort_early and abort_early.is_set():
                    # cancel; settings were updated and we need to start over
                    return []

                patches.extend(element.embroider(None))
        except SystemExit:
            raise
        except Exception:
            raise
            # Ignore errors.  This can be things like incorrect paths for
            # satins or division by zero caused by incorrect param values.
            pass

        return patches

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
        self.preview.disable()
        self.update_lettering(True)
        self.save_settings()
        self.close()

    def close(self):
        self.preview.close()
        self.Destroy()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()

        self.close()

    def __do_layout(self):
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # font selection
        font_selector_sizer = wx.StaticBoxSizer(self.font_selector_box, wx.VERTICAL)
        font_selector_box = wx.BoxSizer(wx.HORIZONTAL)
        font_selector_box.Add(self.font_chooser, 4, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
        self.filter_label = wx.StaticText(self, wx.ID_ANY, "Filter")
        font_selector_box.Add(self.filter_label, 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 0)
        font_selector_box.Add(self.font_filter, 1, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 5)
        font_selector_sizer.Add(font_selector_box, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        font_selector_sizer.Add(self.font_description, 1, wx.EXPAND | wx.ALL, 10)
        outer_sizer.Add(font_selector_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # options
        left_option_sizer = wx.BoxSizer(wx.VERTICAL)
        left_option_sizer.Add(self.back_and_forth_checkbox, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 5)
        left_option_sizer.Add(self.trim_checkbox, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, 5)

        font_scale_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Scale"), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 0)
        font_scale_sizer.Add(self.scale_spinner, 0, wx.LEFT, 10)
        font_scale_sizer.Add(wx.StaticText(self, wx.ID_ANY, "%"), 0, wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, 3)

        options_sizer = wx.StaticBoxSizer(self.options_box, wx.HORIZONTAL)
        options_sizer.Add(left_option_sizer, 1, wx.EXPAND, 10)
        options_sizer.Add(font_scale_sizer, 0, wx.RIGHT, 10)

        outer_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # text input
        text_input_sizer = wx.StaticBoxSizer(self.text_input_box, wx.VERTICAL)
        text_input_sizer.Add(self.text_editor, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(text_input_sizer, 2, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        # presets
        outer_sizer.Add(self.presets_panel, 0, wx.EXPAND | wx.EXPAND | wx.ALL, 10)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.cancel_button, 0, wx.RIGHT, 10)
        buttons_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT, 10)

        self.SetSizerAndFit(outer_sizer)
        self.Layout()

        # SetSizerAndFit determined the minimum size that fits all the controls
        # and set the window's minimum size so that the user can't make it
        # smaller.  It also set the window to that size.  We'd like to give the
        # user a bit more room for text, so we'll add some height.
        size = self.GetSize()
        size.height = size.height + 200
        self.SetSize(size)


class Lettering(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        self.cancelled = False
        CommandsExtension.__init__(self, *args, **kwargs)

    def cancel(self):
        self.cancelled = True

    def get_or_create_group(self):
        if self.svg.selection:
            groups = set()

            for node in self.svg.selection:
                if node.tag == SVG_GROUP_TAG and INKSTITCH_LETTERING in node.attrib:
                    groups.add(node)

                for group in node.iterancestors(SVG_GROUP_TAG):
                    if INKSTITCH_LETTERING in group.attrib:
                        groups.add(group)

            if len(groups) > 1:
                inkex.errormsg(_("Please select only one block of text."))
                sys.exit(1)
            elif len(groups) == 0:
                inkex.errormsg(_("You've selected objects that were not created by the Lettering extension.  "
                                 "Please clear your selection or select different objects before running Lettering again."))
                sys.exit(1)
            else:
                return list(groups)[0]
        else:
            group = inkex.Group(attrib={
                INKSCAPE_LABEL: _("Ink/Stitch Lettering"),
                "transform": get_correction_transform(self.get_current_layer(), child=True)
            })
            self.get_current_layer().append(group)
            return group

    def effect(self):
        app = wx.App()
        frame = LetteringFrame(group=self.get_or_create_group(), on_cancel=self.cancel)

        # position left, center
        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        display_size = display.GetClientArea()
        frame_size = frame.GetSize()
        frame.SetPosition((int(display_size[0]), int(display_size[3] / 2 - frame_size[1] / 2)))

        frame.Show()
        app.MainLoop()

        if self.cancelled:
            # This prevents the superclass from outputting the SVG, because we
            # may have modified the DOM.
            sys.exit(0)
