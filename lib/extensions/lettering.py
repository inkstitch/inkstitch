# -*- coding: UTF-8 -*-

from base64 import b64encode, b64decode
import json
import os
import sys

import appdirs
import inkex
import wx

from ..elements import nodes_to_elements
from ..gui import PresetsPanel, SimulatorPreview, info_dialog, SubtitleComboBox
from ..i18n import _
from ..lettering import Font, FontError
from ..svg import get_correction_transform
from ..svg.tags import SVG_PATH_TAG, SVG_GROUP_TAG, INKSCAPE_LABEL, INKSTITCH_LETTERING
from ..utils import get_bundled_dir, DotDict, cache
from .commands import CommandsExtension


class LetteringFrame(wx.Frame):
    DEFAULT_FONT = "small_font"

    def __init__(self, *args, **kwargs):
        # begin wxGlade: MyFrame.__init__
        self.group = kwargs.pop('group')
        self.cancel_hook = kwargs.pop('on_cancel', None)
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          _("Ink/Stitch Lettering")
                          )

        self.preview = SimulatorPreview(self, target_duration=1)
        self.presets_panel = PresetsPanel(self)

        self.load_settings()

        # options
        self.options_box = wx.StaticBox(self, wx.ID_ANY, label=_("Options"))

        self.back_and_forth_checkbox = wx.CheckBox(self, label=_("Stitch lines of text back and forth"))
        self.back_and_forth_checkbox.SetValue(self.settings.back_and_forth)
        self.back_and_forth_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.on_change("back_and_forth", event))

        self.trim_checkbox = wx.CheckBox(self, label=_("Add trims"))
        self.trim_checkbox.SetValue(bool(self.settings.trim))
        self.trim_checkbox.Bind(wx.EVT_CHECKBOX, lambda event: self.on_change("trim", event))

        # text editor
        self.text_editor_box = wx.StaticBox(self, wx.ID_ANY, label=_("Text"))

        self.update_font_list()
        self.font_chooser = SubtitleComboBox(self, wx.ID_ANY, choices=self.get_font_names(),
                                             subtitles=self.get_font_descriptions(), style=wx.CB_READONLY)
        self.font_chooser.Bind(wx.EVT_COMBOBOX, self.update_preview)
        self.set_initial_font(self.settings.font)

        self.text_editor = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, value=self.settings.text)
        self.Bind(wx.EVT_TEXT, lambda event: self.on_change("text", event))

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__do_layout()
        # end wxGlade

    def load_settings(self):
        try:
            if INKSTITCH_LETTERING in self.group.attrib:
                self.settings = DotDict(json.loads(b64decode(self.group.get(INKSTITCH_LETTERING))))
                return
        except (TypeError, ValueError):
            pass

        self.settings = DotDict({
            "text": u"",
            "back_and_forth": True,
            "font": None
        })

    def save_settings(self):
        # We base64 encode the string before storing it in an XML attribute.
        # In theory, lxml should properly html-encode the string, using HTML
        # entities like &#10; as necessary.  However, we've found that Inkscape
        # incorrectly interpolates the HTML entities upon reading the
        # extension's output, rather than leaving them as is.
        #
        # Details:
        #   https://bugs.launchpad.net/inkscape/+bug/1804346
        self.group.set(INKSTITCH_LETTERING, b64encode(json.dumps(self.settings)))

    def update_font_list(self):
        font_paths = {
            get_bundled_dir("fonts"),
            os.path.expanduser("~/.inkstitch/fonts"),
            os.path.join(appdirs.user_config_dir('inkstitch'), 'fonts'),
        }

        self.fonts = {}
        self.fonts_by_id = {}

        for font_path in font_paths:
            try:
                font_dirs = os.listdir(font_path)
            except OSError:
                continue

            try:
                for font_dir in font_dirs:
                    font = Font(os.path.join(font_path, font_dir))
                    self.fonts[font.name] = font
                    self.fonts_by_id[font.id] = font
            except FontError:
                pass

        if len(self.fonts) == 0:
            info_dialog(self, _("Unable to find any fonts!  Please try reinstalling Ink/Stitch."))
            self.cancel()

    def get_font_names(self):
        font_names = [font.name for font in self.fonts.itervalues()]
        font_names.sort()

        return font_names

    def get_font_descriptions(self):
        return {font.name: font.description for font in self.fonts.itervalues()}

    def set_initial_font(self, font_id):
        if font_id is not None:
            if font_id not in self.fonts_by_id:
                info_dialog(self, _(
                    '''This text was created using the font "%s", but Ink/Stitch can't find that font.  A default font will be substituted.''') % font_id)

        try:
            self.font_chooser.SetValueByUser(self.fonts_by_id[font_id].name)
        except KeyError:
            self.font_chooser.SetValueByUser(self.default_font.name)

    @property
    @cache
    def default_font(self):
        try:
            return self.fonts[self.DEFAULT_FONT]
        except KeyError:
            return self.fonts.values()[0]

    def on_change(self, attribute, event):
        self.settings[attribute] = event.GetEventObject().GetValue()
        self.preview.update()

    def update_preview(self, event=None):
        self.preview.update()

    def update_lettering(self):
        font = self.fonts.get(self.font_chooser.GetValue(), self.default_font)
        del self.group[:]
        font.render_text(self.settings.text, self.group, back_and_forth=self.settings.back_and_forth, trim=self.settings.trim)

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
        preset = {}
        return preset

    def apply_preset_data(self):
        # called by self.presets_panel
        return

    def get_preset_suite_name(self):
        # called by self.presets_panel
        return "lettering"

    def apply(self, event):
        self.preview.disable()
        self.update_lettering()
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

        options_sizer = wx.StaticBoxSizer(self.options_box, wx.VERTICAL)
        options_sizer.Add(self.back_and_forth_checkbox, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 5)
        options_sizer.Add(self.trim_checkbox, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, 5)
        outer_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        font_chooser_sizer = wx.BoxSizer(wx.VERTICAL)
        font_chooser_sizer.Add(self.font_chooser, 0, wx.ALL | wx.EXPAND, 10)

        text_editor_sizer = wx.StaticBoxSizer(self.text_editor_box, wx.VERTICAL)
        text_editor_sizer.Add(font_chooser_sizer, 0, wx.RIGHT | wx.EXPAND, 100)
        text_editor_sizer.Add(self.text_editor, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(text_editor_sizer, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        outer_sizer.Add(self.presets_panel, 0, wx.EXPAND | wx.EXPAND | wx.ALL, 10)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
        buttons_sizer.Add(self.apply_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)
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
        if self.selected:
            groups = set()

            for node in self.selected.itervalues():
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
            self.ensure_current_layer()
            return inkex.etree.SubElement(self.current_layer, SVG_GROUP_TAG, {
                INKSCAPE_LABEL: _("Ink/Stitch Lettering"),
                "transform": get_correction_transform(self.current_layer, child=True)
            })

    def effect(self):
        app = wx.App()
        frame = LetteringFrame(group=self.get_or_create_group(), on_cancel=self.cancel)

        # position left, center
        current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
        display = wx.Display(current_screen)
        display_size = display.GetClientArea()
        frame_size = frame.GetSize()
        frame.SetPosition((display_size[0], display_size[3] / 2 - frame_size[1] / 2))

        frame.Show()
        app.MainLoop()

        if self.cancelled:
            # This prevents the superclass from outputting the SVG, because we
            # may have modified the DOM.
            sys.exit(0)
