import json
import os
import re

import wx

from ..i18n import _
from ..utils import cache
from .dialogs import info_dialog


class PresetsPanel(wx.Panel):
    """A wx.Panel for loading, saving, and applying presets.

    A preset is a named collection of settings.  From the perspective of this
    class, a preset is an opaque JSON-serializable object.

    The PresetsPanel will handle interaction with the user and inform the
    instantiator of events such as a preset being loaded.  Presets starting
    and ending with "__" will not be shown to the user.  This allows for the
    instantiator to manage hidden presets such as "__LAST__".
    """

    HIDDEN_PRESET_RE = re.compile('^__.*__$')

    def __init__(self, parent, *args, **kwargs):
        """Construct a PresetsPanel.

        The parent is the parent window for this wx.Panel.  The parent is
        expected to implement the following methods:

            def get_preset_data(self)
                returns a JSON object representing the current state as a preset

            def apply_preset_data(self, preset_data):
                apply the preset data to the GUI, updating GUI elements as necessary

            def get_preset_suite_name(self):
                Return a string used in the presets filename, e.g. "lettering" -> "lettering_presets.json".
                If not defined, "presets.json" will be used.
        """

        kwargs.setdefault('style', wx.BORDER_NONE)
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)
        self.parent = parent

        self.presets_box = wx.StaticBox(self, wx.ID_ANY, label=_("Presets"))

        self.preset_chooser = wx.ComboBox(self, wx.ID_ANY)
        self.update_preset_list()
        self.preset_chooser.SetSelection(-1)

        self.load_preset_button = wx.Button(self, wx.ID_ANY, _("Load"))
        self.load_preset_button.Bind(wx.EVT_BUTTON, self.load_selected_preset)

        self.add_preset_button = wx.Button(self, wx.ID_ANY, _("Add"))
        self.add_preset_button.Bind(wx.EVT_BUTTON, self.add_preset)

        self.overwrite_preset_button = wx.Button(self, wx.ID_ANY, _("Overwrite"))
        self.overwrite_preset_button.Bind(wx.EVT_BUTTON, self.overwrite_preset)

        self.delete_preset_button = wx.Button(self, wx.ID_ANY, _("Delete"))
        self.delete_preset_button.Bind(wx.EVT_BUTTON, self.delete_preset)

        presets_sizer = wx.StaticBoxSizer(self.presets_box, wx.HORIZONTAL)
        self.preset_chooser.SetMinSize((200, -1))
        presets_sizer.Add(self.preset_chooser, 1, wx.LEFT | wx.BOTTOM | wx.EXPAND, 10)
        presets_sizer.Add(self.load_preset_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, 10)
        presets_sizer.Add(self.add_preset_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, 10)
        presets_sizer.Add(self.overwrite_preset_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, 10)
        presets_sizer.Add(self.delete_preset_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT | wx.RIGHT, 10)

        self.SetSizerAndFit(presets_sizer)
        self.Layout()

    @property
    @cache
    def suite_name(self):
        try:
            return self.parent.get_preset_suite_name() + "_presets"
        except AttributeError:
            return "presets"

    @cache
    def presets_path(self):
        try:
            import appdirs
            config_path = appdirs.user_config_dir('inkstitch')
        except ImportError:
            config_path = os.path.expanduser('~/.inkstitch')

        if not os.path.exists(config_path):
            os.makedirs(config_path)
        return os.path.join(config_path, '%s.json' % self.suite_name)

    def _load_presets(self):
        try:
            with open(self.presets_path(), 'r') as presets:
                presets = json.load(presets)
                return presets
        except (IOError, ValueError):
            return {}

    def _save_presets(self, presets):
        with open(self.presets_path(), 'w') as presets_file:
            json.dump(presets, presets_file)

    def update_preset_list(self):
        preset_names = list(self._load_presets().keys())
        preset_names = [preset for preset in preset_names if not self.is_hidden(preset)]
        self.preset_chooser.SetItems(sorted(preset_names))

    def is_hidden(self, preset_name):
        return self.HIDDEN_PRESET_RE.match(preset_name)

    def get_preset_name(self):
        preset_name = self.preset_chooser.GetValue().strip()
        if preset_name:
            return preset_name
        else:
            info_dialog(self, _("Please enter or select a preset name first."), caption=_('Preset'))
            return

    def check_and_load_preset(self, preset_name):
        preset = self._load_presets().get(preset_name)
        if not preset:
            info_dialog(self, _('Preset "%s" not found.') % preset_name, caption=_('Preset'))

        return preset

    def store_preset(self, preset_name, data):
        presets = self._load_presets()
        presets[preset_name] = data
        self._save_presets(presets)
        self.update_preset_list()

    def add_preset(self, event, overwrite=False):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        if not overwrite and preset_name in self._load_presets():
            info_dialog(self, _('Preset "%s" already exists.  Please use another name or press "Overwrite"') % preset_name, caption=_('Preset'))

        self.store_preset(preset_name, self.parent.get_preset_data())

        event.Skip()

    def overwrite_preset(self, event):
        self.add_preset(event, overwrite=True)

    def load_preset(self, preset_name):
        preset = self.check_and_load_preset(preset_name)
        if not preset:
            return

        self.parent.apply_preset_data(preset)

    def load_selected_preset(self, event):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        self.load_preset(preset_name)

        event.Skip()

    def delete_preset(self, event):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        preset = self.check_and_load_preset(preset_name)
        if not preset:
            return

        presets = self._load_presets()
        presets.pop(preset_name, None)
        self._save_presets(presets)

        self.update_preset_list()
        self.preset_chooser.SetValue("")

        event.Skip()
