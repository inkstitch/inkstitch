# -*- coding: UTF-8 -*-

from base64 import b64encode, b64decode
import json
import os
import sys
from threading import Thread, Event
import traceback

import inkex
import wx

from ..elements import nodes_to_elements
from ..gui import EmbroiderySimulator, PresetsPanel
from ..i18n import _
from ..lettering import Font
from ..stitch_plan import patches_to_stitch_plan
from ..svg.tags import SVG_PATH_TAG, SVG_GROUP_TAG, INKSCAPE_LABEL, INKSTITCH_TEXT
from ..utils import get_bundled_dir
from .commands import CommandsExtension


class LetteringFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        # begin wxGlade: MyFrame.__init__
        self.group = kwargs.pop('group')
        self.cancel_hook = kwargs.pop('on_cancel', None)
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          _("Ink/Stitch Lettering")
                          )

        self.simulate_window = None
        self.simulate_thread = None
        self.simulate_refresh_needed = Event()

        # used when closing to avoid having the window reopen at the last second
        self.disable_simulate_window = False

        wx.CallLater(1000, self.update_simulator)

        # options
        self.options_box = wx.StaticBox(self, wx.ID_ANY, label=_("Options"))

        self.back_and_forth_checkbox = wx.CheckBox(self, label=_("Stitch lines of text back and forth"))
        self.back_and_forth_checkbox.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.update_simulator)

        # text editor
        self.text_editor_box = wx.StaticBox(self, wx.ID_ANY, label=_("Text"))

        self.font_chooser = wx.ComboBox(self, wx.ID_ANY)
        self.update_font_list()

        self.text_editor = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, value=self.text)
        self.Bind(wx.EVT_TEXT, self.text_changed)

        # presets
        self.presets_panel = PresetsPanel(self)

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__do_layout()
        # end wxGlade

    @property
    def text(self):
        try:
            if INKSTITCH_TEXT in self.group.attrib:
                return b64decode(self.group.get(INKSTITCH_TEXT)).decode('UTF-8')
        except TypeError:
            pass

        return u''

    @text.setter
    def text(self, value):
        # We base64 encode the string before storign it in an XML attribute.
        # In theory, lxml should properly html-encode the string, using HTML
        # entities like &#10; as necessary.  However, we've found that Inkscape
        # incorrectly interpolates the HTML entities upon reading the
        # extension's output, rather than leaving them as is.
        #
        # Details:
        #   https://bugs.launchpad.net/inkscape/+bug/1804346
        self.group.set(INKSTITCH_TEXT, b64encode(value.encode("UTF-8")))

    def text_changed(self, event):
        self.text = self.text_editor.GetValue()
        self.update_simulator()

    def update_simulator(self, event=None):
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.clear()

        if self.disable_simulate_window:
            return

        if not self.simulate_thread or not self.simulate_thread.is_alive():
            self.simulate_thread = Thread(target=self.simulate_worker)
            self.simulate_thread.daemon = True
            self.simulate_thread.start()

        self.simulate_refresh_needed.set()

    def simulate_worker(self):
        while True:
            self.simulate_refresh_needed.wait()
            self.simulate_refresh_needed.clear()
            self.update_patches()

    def update_patches(self):
        patches = self.generate_patches()

        if patches and not self.simulate_refresh_needed.is_set():
            wx.CallAfter(self.refresh_simulator, patches)

    def refresh_simulator(self, patches):
        stitch_plan = patches_to_stitch_plan(patches)

        if self.disable_simulate_window:
            return

        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.load(stitch_plan)
        else:
            params_rect = self.GetScreenRect()
            simulator_pos = params_rect.GetTopRight()
            simulator_pos.x += 5

            current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
            display = wx.Display(current_screen)
            screen_rect = display.GetClientArea()
            simulator_pos.y = screen_rect.GetTop()

            width = screen_rect.GetWidth() - params_rect.GetWidth()
            height = screen_rect.GetHeight()

            try:
                self.simulate_window = EmbroiderySimulator(None, -1, _("Preview"),
                                                           simulator_pos,
                                                           size=(width, height),
                                                           stitch_plan=stitch_plan,
                                                           on_close=self.simulate_window_closed,
                                                           target_duration=1)
            except Exception:
                error = traceback.format_exc()

                try:
                    # a window may have been created, so we need to destroy it
                    # or the app will never exit
                    wx.Window.FindWindowByName(_("Preview")).Destroy()
                except Exception:
                    pass

                info_dialog(self, error, _("Internal Error"))

            self.simulate_window.Show()
            wx.CallLater(10, self.Raise)

        wx.CallAfter(self.simulate_window.go)

    def simulate_window_closed(self):
        self.simulate_window = None

    def generate_patches(self):
        patches = []

        font_path = os.path.join(get_bundled_dir("fonts"), "small_font")
        font = Font(font_path)

        try:
            lines = font.render_text(self.text, back_and_forth=self.back_and_forth_checkbox.GetValue())
            self.group[:] = lines
            elements = nodes_to_elements(self.group.iterdescendants(SVG_PATH_TAG))

            for element in elements:
                if self.simulate_refresh_needed.is_set():
                    # cancel; params were updated and we need to start over
                    return []

                # Making a copy of the embroidery element is an easy
                # way to drop the cache in the @cache decorators used
                # for many params in embroider.py.

                patches.extend(element.embroider(None))
        except SystemExit:
            raise
        except Exception:
            raise
            # Ignore errors.  This can be things like incorrect paths for
            # satins or division by zero caused by incorrect param values.
            pass

        return patches

    def update_font_list(self):
        pass

    def update_preset_list(self):
        preset_names = load_presets().keys()
        preset_names = [preset for preset in preset_names if preset != "__LAST__"]
        self.preset_chooser.SetItems(sorted(preset_names))

    def get_preset_name(self):
        preset_name = self.preset_chooser.GetValue().strip()
        if preset_name:
            return preset_name
        else:
            info_dialog(self, _("Please enter or select a preset name first."), caption=_('Preset'))
            return

    def check_and_load_preset(self, preset_name):
        preset = load_preset(preset_name)
        if not preset:
            info_dialog(self, _('Preset "%s" not found.') % preset_name, caption=_('Preset'))

        return preset

    def get_preset_data(self):
        preset = {}

        current_tab = self.tabs[self.notebook.GetSelection()]
        while current_tab.parent_tab:
            current_tab = current_tab.parent_tab

        tabs = [current_tab]
        if current_tab.paired_tab:
            tabs.append(current_tab.paired_tab)
            tabs.extend(current_tab.paired_tab.dependent_tabs)
        tabs.extend(current_tab.dependent_tabs)

        for tab in tabs:
            tab.save_preset(preset)

        return preset

    def add_preset(self, event, overwrite=False):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        if not overwrite and load_preset(preset_name):
            info_dialog(self, _('Preset "%s" already exists.  Please use another name or press "Overwrite"') % preset_name, caption=_('Preset'))

        save_preset(preset_name, self.get_preset_data())
        self.update_preset_list()

        event.Skip()

    def overwrite_preset(self, event):
        self.add_preset(event, overwrite=True)

    def _load_preset(self, preset_name):
        preset = self.check_and_load_preset(preset_name)
        if not preset:
            return

        for tab in self.tabs:
            tab.load_preset(preset)

    def load_preset(self, event):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        self._load_preset(preset_name)

        event.Skip()

    def delete_preset(self, event):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        preset = self.check_and_load_preset(preset_name)
        if not preset:
            return

        delete_preset(preset_name)
        self.update_preset_list()
        self.preset_chooser.SetValue("")

        event.Skip()

    def apply(self, event):
        self.close()
        self.generate_patches()

    def close(self):
        self.disable_simulate_window = True
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.Close()

        self.Destroy()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()

        self.close()

    def __do_layout(self):
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        options_sizer = wx.StaticBoxSizer(self.options_box, wx.VERTICAL)
        options_sizer.Add(self.back_and_forth_checkbox, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        outer_sizer.Add(options_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)

        text_editor_sizer = wx.StaticBoxSizer(self.text_editor_box, wx.VERTICAL)
        text_editor_sizer.Add(self.font_chooser, 0, wx.ALL, 10)
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
                if node.tag == SVG_GROUP_TAG and INKSTITCH_TEXT in node.attrib:
                    groups.add(node)

                for group in node.iterancestors(SVG_GROUP_TAG):
                    if INKSTITCH_TEXT in group.attrib:
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
                INKSCAPE_LABEL: _("Ink/Stitch Lettering")
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
