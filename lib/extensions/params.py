# -*- coding: UTF-8 -*-

import os
import sys
from collections import defaultdict
from copy import copy
from itertools import groupby

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ..commands import is_command
from ..elements import (AutoFill, Clone, EmbroideryElement, Fill, Polyline,
                        SatinColumn, Stroke)
from ..elements.clone import is_clone
from ..gui import PresetsPanel, SimulatorPreview
from ..i18n import _
from ..svg.tags import SVG_POLYLINE_TAG
from ..utils import get_resource_dir
from .base import InkstitchExtension


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

        self.pencil_icon = wx.Image(os.path.join(get_resource_dir("icons"), "pencil_20x20.png")).ConvertToBitmap()

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
            if self.toggle_checkbox in self.changed_inputs:
                if self.toggle.inverse:
                    values[self.toggle.name] = not checked
                else:
                    values[self.toggle.name] = checked

            if not checked:
                # Ignore params on this tab if the toggle is unchecked,
                # because they're grayed out anyway.
                return values

        for name, input in self.param_inputs.items():
            if input in self.changed_inputs and input != self.toggle_checkbox:
                values[name] = input.GetValue()

        return values

    def apply(self):
        values = self.get_values()
        for node in self.nodes:
            # print >> sys.stderr, "apply: ", self.name, node.id, values
            for name, value in values.items():
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

        for name, value in preset_data.items():
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
        self.description = wx.StaticText(self)
        self.update_description()
        self.description.SetLabel(self.description_text)
        self.description_container = box
        self.Bind(wx.EVT_SIZE, self.resized)
        sizer.Add(self.description, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        box.Add(sizer, proportion=0, flag=wx.ALL, border=5)

        if self.toggle:
            toggle_sizer = wx.BoxSizer(wx.HORIZONTAL)
            toggle_sizer.Add(self.create_change_indicator(self.toggle.name), proportion=0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
            toggle_sizer.Add(self.toggle_checkbox, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
            box.Add(toggle_sizer, proportion=0, flag=wx.BOTTOM, border=10)

        for param in self.params:
            self.settings_grid.Add(self.create_change_indicator(param.name), proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)

            description = wx.StaticText(self, label=param.description)
            description.SetToolTip(param.tooltip)
            self.settings_grid.Add(description, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP, border=5)

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

            self.settings_grid.Add(input, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT, border=40)
            self.settings_grid.Add(wx.StaticText(self, label=param.unit or ""), proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)

        self.inputs_to_params = {v: k for k, v in self.param_inputs.items()}

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

        if self.on_change_hook:
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
            tab.on_change(self.update_preview)

        self.preview = SimulatorPreview(self)
        self.presets_panel = PresetsPanel(self)

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.use_last_button = wx.Button(self, wx.ID_ANY, _("Use Last Settings"))
        self.use_last_button.Bind(wx.EVT_BUTTON, self.use_last)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.notebook.SetMinSize((800, 600))

        self.__do_layout()
        # end wxGlade

    def update_preview(self, tab):
        self.preview.update()

    def generate_patches(self, abort_early):
        # called by self.preview

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
                if abort_early.is_set():
                    # cancel; params were updated and we need to start over
                    return []

                # Making a copy of the embroidery element is an easy
                # way to drop the cache in the @cache decorators used
                # for many params in embroider.py.

                patches.extend(copy(node).embroider(None))
        except SystemExit:
            raise
        except Exception:
            # Ignore errors.  This can be things like incorrect paths for
            # satins or division by zero caused by incorrect param values.
            pass

        return patches

    def get_preset_data(self):
        # called by self.presets_panel

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

    def apply_preset_data(self, preset_data):
        # called by self.presets_panel

        for tab in self.tabs:
            tab.load_preset(preset_data)

        self.preview.update()

    def _apply(self):
        for tab in self.tabs:
            tab.apply()

    def apply(self, event):
        self._apply()
        self.presets_panel.store_preset("__LAST__", self.get_preset_data())
        self.close()

    def use_last(self, event):
        self.preview.disable()
        self.presets_panel.load_preset("__LAST__")
        self.apply(event)

    def close(self):
        self.preview.close()
        self.Destroy()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()

        self.close()

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        # self.sizer_3_staticbox.Lower()
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        for tab in self.tabs:
            self.notebook.AddPage(tab, tab.name)
        sizer_1.Add(self.notebook, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        sizer_1.Add(self.presets_panel, 0, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_3.Add(self.cancel_button, 0, wx.RIGHT, 5)
        sizer_3.Add(self.use_last_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        sizer_3.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 5)
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

        if not is_command(node):
            if node.tag == SVG_POLYLINE_TAG:
                classes.append(Polyline)
            elif is_clone(node):
                classes.append(Clone)
            else:
                if element.get_style("fill", 'black') and not element.get_style("fill-opacity", 1) == "0":
                    classes.append(AutoFill)
                    classes.append(Fill)
                if element.get_style("stroke") is not None:
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

        return sorted(list(nodes_by_class.items()), key=lambda cls_nodes: cls_nodes[0].__name__)

    def get_values(self, param, nodes):
        getter = 'get_param'

        if param.type in ('toggle', 'boolean'):
            getter = 'get_boolean_param'
        else:
            getter = 'get_param'

        values = [item for item in (getattr(node, getter)(param.name, param.default) for node in nodes) if item is not None]

        return values

    def group_params(self, params):
        def by_group_and_sort_index(param):
            return param.group or "", param.sort_index

        def by_group(param):
            return param.group or ""

        return groupby(sorted(params, key=by_group_and_sort_index), by_group)

    def sort_tabs(self, tabs):
        def tab_sort_key(tab):
            parent = tab.parent_tab or tab

            sort_key = (
                # For Stroke and SatinColumn, place the one that's
                # enabled first.  Place dependent tabs first too.
                parent.toggle and parent.toggle_checkbox.IsChecked(),

                # If multiple tabs are enabled, make sure dependent
                # tabs are grouped with the parent.
                parent and parent.name,

                # Within parent/dependents, put the parent first.
                tab == parent
            )

            return sort_key

        tabs.sort(key=tab_sort_key, reverse=True)

    def pair_tabs(self, tabs):
        for tab in tabs:
            if tab.toggle and tab.toggle.inverse:
                for other_tab in tabs:
                    if other_tab != tab and other_tab.toggle.name == tab.toggle.name:
                        tab.pair(other_tab)
                        other_tab.pair(tab)

    def assign_parents(self, tabs, parent_tab):
        for tab in tabs:
            if tab != parent_tab:
                parent_tab.add_dependent_tab(tab)
                tab.set_parent_tab(parent_tab)

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
                tab_name = group or cls.element_name
                tab = ParamsTab(parent, id=wx.ID_ANY, name=tab_name, params=list(params), nodes=nodes)
                new_tabs.append(tab)

                if group == "":
                    parent_tab = tab

            self.assign_parents(new_tabs, parent_tab)
            tabs.extend(new_tabs)

        self.pair_tabs(tabs)
        self.sort_tabs(tabs)

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
            frame.SetPosition((int(display_size[0]), int(display_size[3]/2 - frame_size[1]/2)))

            frame.Show()
            app.MainLoop()

            if self.cancelled:
                # This prevents the superclass from outputting the SVG, because we
                # may have modified the DOM.
                sys.exit(0)
        except NoValidObjects:
            self.no_elements_error()
