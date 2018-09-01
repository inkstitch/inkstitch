# -*- coding: UTF-8 -*-

import os
import sys
import json
import traceback
import time
from threading import Thread, Event
from copy import copy
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from collections import defaultdict
from functools import partial
from itertools import groupby

from .base import InkstitchExtension
from ..i18n import _
from ..stitch_plan import patches_to_stitch_plan
from ..elements import EmbroideryElement, Fill, AutoFill, Stroke, SatinColumn
from ..utils import save_stderr, restore_stderr, get_bundled_dir
from ..simulator import EmbroiderySimulator
from ..commands import is_command


def presets_path():
    try:
        import appdirs
        config_path = appdirs.user_config_dir('inkstitch')
    except ImportError:
        config_path = os.path.expanduser('~/.inkstitch')

    if not os.path.exists(config_path):
        os.makedirs(config_path)
    return os.path.join(config_path, 'presets.json')


def load_presets():
    try:
        with open(presets_path(), 'r') as presets:
            presets = json.load(presets)
            return presets
    except:
        return {}


def save_presets(presets):
    with open(presets_path(), 'w') as presets_file:
        json.dump(presets, presets_file)


def load_preset(name):
    return load_presets().get(name)


def save_preset(name, data):
    presets = load_presets()
    presets[name] = data
    save_presets(presets)


def delete_preset(name):
    presets = load_presets()
    presets.pop(name, None)
    save_presets(presets)


def confirm_dialog(parent, question, caption = 'ink/stitch'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def info_dialog(parent, message, caption = 'ink/stitch'):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


class ParamsTab(ScrolledPanel):
    def __init__(self, *args, **kwargs):
        self.params = kwargs.pop('params', [])
        self.name = kwargs.pop('name', None)
        self.nodes = kwargs.pop('nodes')
        kwargs["style"] = wx.TAB_TRAVERSAL
        ScrolledPanel.__init__(self, *args, **kwargs)
        self.SetupScrolling()

        self.changed_inputs = set()
        self.dependent_tabs = []
        self.parent_tab = None
        self.param_inputs = {}
        self.paired_tab = None
        self.disable_notify_pair = False

        toggles = [param for param in self.params if param.type == 'toggle']

        if toggles:
            self.toggle = toggles[0]
            self.params.remove(self.toggle)
            self.toggle_checkbox = wx.CheckBox(self, label=self.toggle.description)

            value = any(self.toggle.values)
            if self.toggle.inverse:
                value = not value
            self.toggle_checkbox.SetValue(value)

            self.toggle_checkbox.Bind(wx.EVT_CHECKBOX, self.update_toggle_state)
            self.toggle_checkbox.Bind(wx.EVT_CHECKBOX, self.changed)

            self.param_inputs[self.toggle.name] = self.toggle_checkbox
        else:
            self.toggle = None

        self.param_change_indicators = {}

        self.settings_grid = wx.FlexGridSizer(rows=0, cols=4, hgap=10, vgap=15)
        self.settings_grid.AddGrowableCol(1, 2)
        self.settings_grid.SetFlexibleDirection(wx.HORIZONTAL)

        self.pencil_icon = wx.Image(os.path.join(get_bundled_dir("icons"), "pencil_20x20.png")).ConvertToBitmap()

        self.__set_properties()
        self.__do_layout()

        if self.toggle:
            self.update_toggle_state()
        # end wxGlade

    def pair(self, tab):
        # print self.name, "paired with", tab.name
        self.paired_tab = tab
        self.update_description()

    def add_dependent_tab(self, tab):
        self.dependent_tabs.append(tab)
        self.update_description()

    def set_parent_tab(self, tab):
        self.parent_tab = tab

    def is_dependent_tab(self):
        return self.parent_tab is not None

    def enabled(self):
        if self.toggle_checkbox:
            return self.toggle_checkbox.IsChecked()
        else:
            return True

    def update_toggle_state(self, event=None, notify_pair=True):
        enable = self.enabled()
        # print self.name, "update_toggle_state", enable
        for child in self.settings_grid.GetChildren():
            widget = child.GetWindow()
            if widget:
                child.GetWindow().Enable(enable)

        if notify_pair and self.paired_tab:
            self.paired_tab.pair_changed(enable)

        for tab in self.dependent_tabs:
            tab.dependent_enable(enable)

        if event:
            event.Skip()

    def pair_changed(self, value):
        # print self.name, "pair_changed", value
        new_value = not value

        if self.enabled() != new_value:
            self.set_toggle_state(not value)
            self.update_toggle_state(notify_pair=False)

            if self.on_change_hook:
                self.on_change_hook(self)

    def dependent_enable(self, enable):
        if enable:
            self.toggle_checkbox.Enable()
        else:
            self.set_toggle_state(False)
            self.toggle_checkbox.Disable()
            self.update_toggle_state()

        if self.on_change_hook:
            self.on_change_hook(self)

    def set_toggle_state(self, value):
        if self.toggle_checkbox:
            self.toggle_checkbox.SetValue(value)
            self.changed_inputs.add(self.toggle_checkbox)

    def get_values(self):
        values = {}

        if self.toggle:
            checked = self.enabled()
            if self.toggle_checkbox in self.changed_inputs and not self.toggle.inverse:
                values[self.toggle.name] = checked

            if not checked:
                # Ignore params on this tab if the toggle is unchecked,
                # because they're grayed out anyway.
                return values

        for name, input in self.param_inputs.iteritems():
            if input in self.changed_inputs and input != self.toggle_checkbox:
                values[name] = input.GetValue()

        return values

    def apply(self):
        values = self.get_values()
        for node in self.nodes:
            # print >> sys.stderr, "apply: ", self.name, node.id, values
            for name, value in values.iteritems():
                node.set_param(name, value)

    def on_change(self, callable):
        self.on_change_hook = callable

    def changed(self, event):
        input = event.GetEventObject()
        self.changed_inputs.add(input)

        param = self.inputs_to_params[input]
        self.enable_change_indicator(param)
        event.Skip()

        if self.on_change_hook:
            self.on_change_hook(self)

    def load_preset(self, preset):
        preset_data = preset.get(self.name, {})

        for name, value in preset_data.iteritems():
            if name in self.param_inputs:
                self.param_inputs[name].SetValue(value)
                self.changed_inputs.add(self.param_inputs[name])

        self.update_toggle_state()

    def save_preset(self, storage):
        storage[self.name] = self.get_values()

    def update_description(self):
        if len(self.nodes) == 1:
            description = _("These settings will be applied to 1 object.")
        else:
            description = _("These settings will be applied to %d objects.") % len(self.nodes)

        if any(len(param.values) > 1 for param in self.params):
            description += "\n • " + _("Some settings had different values across objects.  Select a value from the dropdown or enter a new one.")

        if self.dependent_tabs:
            if len(self.dependent_tabs) == 1:
                description += "\n • " + _("Disabling this tab will disable the following %d tabs.") % len(self.dependent_tabs)
            else:
                description += "\n • " + _("Disabling this tab will disable the following tab.")

        if self.paired_tab:
            description += "\n • " + _("Enabling this tab will disable %s and vice-versa.") % self.paired_tab.name

        self.description_text = description

    def resized(self, event):
        if not hasattr(self, 'rewrap_timer'):
            self.rewrap_timer = wx.Timer()
            self.rewrap_timer.Bind(wx.EVT_TIMER, self.rewrap)

        # If we try to rewrap every time we get EVT_SIZE then a resize is
        # extremely slow.
        self.rewrap_timer.Start(50, oneShot=True)
        event.Skip()

    def rewrap(self, event=None):
        self.description.SetLabel(self.description_text)
        self.description.Wrap(self.GetSize().x - 20)
        self.description_container.Layout()
        if event:
            event.Skip()

    def __set_properties(self):
        # begin wxGlade: SatinPane.__set_properties
        # end wxGlade
        pass

    def __do_layout(self):
        # just to add space around the settings
        box = wx.BoxSizer(wx.VERTICAL)

        summary_box = wx.StaticBox(self, wx.ID_ANY, label=_("Inkscape objects"))
        sizer = wx.StaticBoxSizer(summary_box, wx.HORIZONTAL)
#        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.description = wx.StaticText(self)
        self.update_description()
        self.description.SetLabel(self.description_text)
        self.description_container = box
        self.Bind(wx.EVT_SIZE, self.resized)
        sizer.Add(self.description, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
        box.Add(sizer, proportion=0, flag=wx.ALL, border=5)

        if self.toggle:
            toggle_sizer = wx.BoxSizer(wx.HORIZONTAL)
            toggle_sizer.Add(self.create_change_indicator(self.toggle.name), proportion = 0, flag=wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=5)
            toggle_sizer.Add(self.toggle_checkbox, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
            box.Add(toggle_sizer, proportion=0, flag=wx.BOTTOM, border=10)

        for param in self.params:
            self.settings_grid.Add(self.create_change_indicator(param.name), proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)

            description = wx.StaticText(self, label=param.description)
            description.SetToolTip(param.tooltip)
            self.settings_grid.Add(description, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=5)

            if param.type == 'boolean':

                if len(param.values) > 1:
                    input = wx.CheckBox(self, style=wx.CHK_3STATE)
                    input.Set3StateValue(wx.CHK_UNDETERMINED)
                else:
                    input = wx.CheckBox(self)
                    if param.values:
                        input.SetValue(param.values[0])

                input.Bind(wx.EVT_CHECKBOX, self.changed)
            elif len(param.values) > 1:
                input = wx.ComboBox(self, wx.ID_ANY, choices=sorted(str(value) for value in param.values), style=wx.CB_DROPDOWN)
                input.Bind(wx.EVT_COMBOBOX, self.changed)
                input.Bind(wx.EVT_TEXT, self.changed)
            else:
                value = param.values[0] if param.values else ""
                input = wx.TextCtrl(self, wx.ID_ANY, value=str(value))
                input.Bind(wx.EVT_TEXT, self.changed)

            self.param_inputs[param.name] = input

            self.settings_grid.Add(input, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.LEFT, border=40)
            self.settings_grid.Add(wx.StaticText(self, label=param.unit or ""), proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)

        self.inputs_to_params = {v: k for k, v in self.param_inputs.iteritems()}

        box.Add(self.settings_grid, proportion=1, flag=wx.ALL, border=10)
        self.SetSizer(box)

        self.Layout()

    def create_change_indicator(self, param):
        indicator = wx.Button(self, style=wx.BORDER_NONE | wx.BU_NOTEXT, size=(28, 28))
        indicator.SetToolTip(_('Click to force this parameter to be saved when you click "Apply and Quit"'))
        indicator.Bind(wx.EVT_BUTTON, lambda event: self.enable_change_indicator(param))

        self.param_change_indicators[param] = indicator
        return indicator

    def enable_change_indicator(self, param):
        self.param_change_indicators[param].SetBitmapLabel(self.pencil_icon)
        self.param_change_indicators[param].SetToolTip(_('This parameter will be saved when you click "Apply and Quit"'))

        self.changed_inputs.add(self.param_inputs[param])

        if self.on_change_hook():
            self.on_change_hook(self)

# end of class SatinPane

class SettingsFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        # begin wxGlade: MyFrame.__init__
        self.tabs_factory = kwargs.pop('tabs_factory', [])
        self.cancel_hook = kwargs.pop('on_cancel', None)
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          _("Embroidery Params")
                          )
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.tabs = self.tabs_factory(self.notebook)

        for tab in self.tabs:
            tab.on_change(self.update_simulator)

        self.simulate_window = None
        self.simulate_thread = None
        self.simulate_refresh_needed = Event()

        # used when closing to avoid having the window reopen at the last second
        self.disable_simulate_window = False

        wx.CallLater(1000, self.update_simulator)

        self.presets_box = wx.StaticBox(self, wx.ID_ANY, label=_("Presets"))

        self.preset_chooser = wx.ComboBox(self, wx.ID_ANY)
        self.update_preset_list()

        self.load_preset_button = wx.Button(self, wx.ID_ANY, _("Load"))
        self.load_preset_button.Bind(wx.EVT_BUTTON, self.load_preset)

        self.add_preset_button = wx.Button(self, wx.ID_ANY, _("Add"))
        self.add_preset_button.Bind(wx.EVT_BUTTON, self.add_preset)

        self.overwrite_preset_button = wx.Button(self, wx.ID_ANY, _("Overwrite"))
        self.overwrite_preset_button.Bind(wx.EVT_BUTTON, self.overwrite_preset)

        self.delete_preset_button = wx.Button(self, wx.ID_ANY, _("Delete"))
        self.delete_preset_button.Bind(wx.EVT_BUTTON, self.delete_preset)

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.use_last_button = wx.Button(self, wx.ID_ANY, _("Use Last Settings"))
        self.use_last_button.Bind(wx.EVT_BUTTON, self.use_last)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def update_simulator(self, tab=None):
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
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.load(stitch_plan=stitch_plan)
        else:
            params_rect = self.GetScreenRect()
            simulator_pos = params_rect.GetTopRight()
            simulator_pos.x += 5

            current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
            display = wx.Display(current_screen)
            screen_rect = display.GetClientArea()

            max_width = screen_rect.GetWidth() - params_rect.GetWidth()
            max_height = screen_rect.GetHeight()

            try:
                self.simulate_window = EmbroiderySimulator(None, -1, _("Preview"),
                                                           simulator_pos,
                                                           size=(300, 300),
                                                           x_position=simulator_pos.x,
                                                           stitch_plan=stitch_plan,
                                                           on_close=self.simulate_window_closed,
                                                           target_duration=5,
                                                           max_width=max_width,
                                                           max_height=max_height)
            except:
                error = traceback.format_exc()

                try:
                    # a window may have been created, so we need to destroy it
                    # or the app will never exit
                    wx.Window.FindWindowByName("Preview").Destroy()
                except:
                    pass

                info_dialog(self, error, _("Internal Error"))

            self.simulate_window.Show()
            wx.CallLater(10, self.Raise)

        wx.CallAfter(self.simulate_window.go)

    def simulate_window_closed(self):
        self.simulate_window = None

    def generate_patches(self):
        patches = []
        nodes = []

        for tab in self.tabs:
            tab.apply()

            if tab.enabled() and not tab.is_dependent_tab():
                nodes.extend(tab.nodes)

        # sort nodes into the proper stacking order
        nodes.sort(key=lambda node: node.order)

        try:
            for node in nodes:
                if self.simulate_refresh_needed.is_set():
                    # cancel; params were updated and we need to start over
                    return []

                # Making a copy of the embroidery element is an easy
                # way to drop the cache in the @cache decorators used
                # for many params in embroider.py.

                patches.extend(copy(node).embroider(None))
        except SystemExit:
            raise
        except:
            # Ignore errors.  This can be things like incorrect paths for
            # satins or division by zero caused by incorrect param values.
            pass

        return patches

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

    def _apply(self):
        for tab in self.tabs:
            tab.apply()

    def apply(self, event):
        self._apply()
        save_preset("__LAST__", self.get_preset_data())
        self.close()

    def use_last(self, event):
        self.disable_simulate_window = True
        self._load_preset("__LAST__")
        self.apply(event)

    def close(self):
        if self.simulate_window:
            self.simulate_window.stop()
            self.simulate_window.Close()

        self.Destroy()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()

        self.close()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.notebook.SetMinSize((800, 600))
        self.preset_chooser.SetSelection(-1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        #self.sizer_3_staticbox.Lower()
        sizer_2 = wx.StaticBoxSizer(self.presets_box, wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        for tab in self.tabs:
            self.notebook.AddPage(tab, tab.name)
        sizer_1.Add(self.notebook, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 10)
        sizer_2.Add(self.preset_chooser, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer_2.Add(self.load_preset_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer_2.Add(self.add_preset_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer_2.Add(self.overwrite_preset_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer_2.Add(self.delete_preset_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer_1.Add(sizer_2, 0, flag=wx.EXPAND|wx.ALL, border=10)
        sizer_3.Add(self.cancel_button, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        sizer_3.Add(self.use_last_button, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)
        sizer_3.Add(self.apply_button, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)
        sizer_1.Add(sizer_3, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

class NoValidObjects(Exception):
    pass

class Params(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        self.cancelled = False
        InkstitchExtension.__init__(self, *args, **kwargs)

    def embroidery_classes(self, node):
        element = EmbroideryElement(node)
        classes = []

        if element.get_style("fill"):
            classes.append(AutoFill)
            classes.append(Fill)

        if element.get_style("stroke") and not is_command(node):
            classes.append(Stroke)

            if element.get_style("stroke-dasharray") is None:
                classes.append(SatinColumn)

        return classes

    def get_nodes_by_class(self):
        nodes = self.get_nodes()
        nodes_by_class = defaultdict(list)

        for z, node in enumerate(nodes):
            for cls in self.embroidery_classes(node):
                element = cls(node)
                element.order = z
                nodes_by_class[cls].append(element)

        return sorted(nodes_by_class.items(), key=lambda (cls, nodes): cls.__name__)

    def get_values(self, param, nodes):
        getter = 'get_param'

        if param.type in ('toggle', 'boolean'):
            getter = 'get_boolean_param'
        else:
            getter = 'get_param'

        values = filter(lambda item: item is not None,
                        (getattr(node, getter)(param.name, param.default) for node in nodes))

        return values

    def group_params(self, params):
        def by_group_and_sort_index(param):
            return param.group, param.sort_index

        def by_group(param):
            return param.group

        return groupby(sorted(params, key=by_group_and_sort_index), by_group)

    def create_tabs(self, parent):
        tabs = []
        nodes_by_class = self.get_nodes_by_class()

        if not nodes_by_class:
            raise NoValidObjects()

        for cls, nodes in self.get_nodes_by_class():
            params = cls.get_params()

            for param in params:
                param.values = list(set(self.get_values(param, nodes)))

            parent_tab = None
            new_tabs = []
            for group, params in self.group_params(params):
                tab = ParamsTab(parent, id=wx.ID_ANY, name=group or cls.element_name, params=list(params), nodes=nodes)
                new_tabs.append(tab)

                if group is None:
                    parent_tab = tab

            for tab in new_tabs:
                if tab != parent_tab:
                    parent_tab.add_dependent_tab(tab)
                    tab.set_parent_tab(parent_tab)

            tabs.extend(new_tabs)

        for tab in tabs:
            if tab.toggle and tab.toggle.inverse:
                for other_tab in tabs:
                    if other_tab != tab and other_tab.toggle.name == tab.toggle.name:
                        tab.pair(other_tab)
                        other_tab.pair(tab)

        def tab_sort_key(tab):
            parent = tab.parent_tab or tab

            sort_key = (
                        # For Stroke and SatinColumn, place the one that's
                        # enabled first.  Place dependent tabs first too.
                        parent.toggle and parent.toggle_checkbox.IsChecked(),

                        # If multiple tabs are enabled, make sure dependent
                        # tabs are grouped with the parent.
                        parent,

                        # Within parent/dependents, put the parent first.
                        tab == parent
                       )

            return sort_key

        tabs.sort(key=tab_sort_key, reverse=True)

        return tabs


    def cancel(self):
        self.cancelled = True

    def effect(self):
        try:
            app = wx.App()
            frame = SettingsFrame(tabs_factory=self.create_tabs, on_cancel=self.cancel)

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
        except NoValidObjects:
            self.no_elements_error()
