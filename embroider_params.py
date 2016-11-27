#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import traceback
from cStringIO import StringIO
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from collections import defaultdict
import inkex
from embroider import Param, EmbroideryElement, Fill, AutoFill,SergFill, Stroke, SatinColumn, descendants
from functools import partial
from itertools import groupby


def presets_path():
    try:
        import appdirs
        config_path = appdirs.user_config_dir('inkscape-embroidery')
    except ImportError:
        config_path = os.path.expanduser('~/.inkscape-embroidery')

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


def confirm_dialog(parent, question, caption = 'inkscape-embroidery'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def info_dialog(parent, message, caption = 'inkscape-embroidery'):
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

        self.settings_grid = wx.FlexGridSizer(rows=0, cols=3, hgap=10, vgap=10)
        self.settings_grid.AddGrowableCol(0, 1)
        self.settings_grid.SetFlexibleDirection(wx.HORIZONTAL)

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

    def update_toggle_state(self, event=None, notify_pair=True):
        enable = self.toggle_checkbox.IsChecked()
        # print self.name, "update_toggle_state", enable
        for child in self.settings_grid.GetChildren():
            widget = child.GetWindow()
            if widget:
                child.GetWindow().Enable(enable)

        if notify_pair and self.paired_tab:
            self.paired_tab.pair_changed(self.toggle_checkbox.IsChecked())

        for tab in self.dependent_tabs:
            tab.dependent_enable(enable)

        if event:
            event.Skip()

    def pair_changed(self, value):
        # print self.name, "pair_changed", value
        new_value = not value

        if self.toggle_checkbox.IsChecked() != new_value:
            self.set_toggle_state(not value)
            self.toggle_checkbox.changed = True
            self.update_toggle_state(notify_pair=False)

    def dependent_enable(self, enable):
        if enable:
            self.toggle_checkbox.Enable()
        else:
            self.set_toggle_state(False)
            self.toggle_checkbox.Disable()
            self.toggle_checkbox.changed = True
            self.update_toggle_state()

    def set_toggle_state(self, value):
        self.toggle_checkbox.SetValue(value)

    def get_values(self):
        values = {}

        if self.toggle:
            checked = self.toggle_checkbox.IsChecked()
            if self.toggle_checkbox in self.changed_inputs and not self.toggle.inverse:
                values[self.toggle.name] = checked

            if not checked:
                # Ignore params on this tab if the toggle is unchecked,
                # because they're grayed out anyway.
                return values

        for name, input in self.param_inputs.iteritems():
            if input in self.changed_inputs:
                values[name] = input.GetValue()

        return values

    def apply(self):
        values = self.get_values()
        for node in self.nodes:
            #print >> sys.stderr, node.id, values
            for name, value in values.iteritems():
                node.set_param(name, value)

    def changed(self, event):
        self.changed_inputs.add(event.GetEventObject())
        event.Skip()

    def load_preset(self, preset):
        preset_data = preset.get(self.name, {})

        for name, value in preset_data.iteritems():
            if name in self.param_inputs:
                self.param_inputs[name].SetValue(value)
                self.changed_inputs.add(self.param_inputs[name])

        self.update_toggle_state()

    def save_preset(self, storage):
        preset = storage[self.name] = {}
        for name, input in self.param_inputs.iteritems():
            preset[name] = input.GetValue()

    def update_description(self):
        description = "These settings will be applied to %d object%s." % \
            (len(self.nodes), "s" if len(self.nodes) != 1 else "")

        if any(len(param.values) > 1 for param in self.params):
            description += "\n • Some settings had different values across objects.  Select a value from the dropdown or enter a new one."

        if self.dependent_tabs:
            description += "\n • Disabling this tab will disable the following %d tabs." % len(self.dependent_tabs)

        if self.paired_tab:
            description += "\n • Enabling this tab will disable %s and vice-versa." % self.paired_tab.name

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

        summary_box = wx.StaticBox(self, wx.ID_ANY, label="Inkscape objects")
        sizer = wx.StaticBoxSizer(summary_box, wx.HORIZONTAL)
#        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.description = wx.StaticText(self, style=wx.TE_WORDWRAP)
        self.update_description()
        self.description.SetLabel(self.description_text)
        self.description_container = box
        self.Bind(wx.EVT_SIZE, self.resized)
        sizer.Add(self.description, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
        box.Add(sizer, proportion=0, flag=wx.ALL, border=5)

        if self.toggle:
            box.Add(self.toggle_checkbox, proportion=0, flag=wx.BOTTOM, border=10)

        for param in self.params:
            self.settings_grid.Add(wx.StaticText(self, label=param.description), proportion=1, flag=wx.EXPAND|wx.RIGHT, border=40)

            if param.type == 'boolean':

                values = list(set(param.values))
                if len(values) > 1:
                    input = wx.CheckBox(self, style=wx.CHK_3STATE)
                    input.Set3StateValue(wx.CHK_UNDETERMINED)
                else:
                    input = wx.CheckBox(self)
                    if values:
                        input.SetValue(values[0])

                input.Bind(wx.EVT_CHECKBOX, self.changed)
            elif len(param.values) > 1:
                input = wx.ComboBox(self, wx.ID_ANY, choices=param.values, style=wx.CB_DROPDOWN | wx.CB_SORT)
                input.Bind(wx.EVT_COMBOBOX, self.changed)
                input.Bind(wx.EVT_TEXT, self.changed)
            else:
                value = param.values[0] if param.values else ""
                input = wx.TextCtrl(self, wx.ID_ANY, value=value)
                input.Bind(wx.EVT_TEXT, self.changed)

            self.param_inputs[param.name] = input

            self.settings_grid.Add(input, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.settings_grid.Add(wx.StaticText(self, label=param.unit or ""), proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)

        box.Add(self.settings_grid, proportion=1, flag=wx.ALL, border=10)
        self.SetSizer(box)

        self.Layout()

# end of class SatinPane

class SettingsFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        # begin wxGlade: MyFrame.__init__
        self.tabs_factory = kwargs.pop('tabs_factory', [])
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "Embroidery Params"
                          )
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.tabs = self.tabs_factory(self.notebook)

        self.presets_box = wx.StaticBox(self, wx.ID_ANY, label="Presets")

        self.preset_chooser = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_SORT)
        self.update_preset_list()

        self.load_preset_button = wx.Button(self, wx.ID_ANY, "Load")
        self.load_preset_button.Bind(wx.EVT_BUTTON, self.load_preset)

        self.add_preset_button = wx.Button(self, wx.ID_ANY, "Add")
        self.add_preset_button.Bind(wx.EVT_BUTTON, self.add_preset)

        self.overwrite_preset_button = wx.Button(self, wx.ID_ANY, "Overwrite")
        self.overwrite_preset_button.Bind(wx.EVT_BUTTON, self.overwrite_preset)

        self.delete_preset_button = wx.Button(self, wx.ID_ANY, "Delete")
        self.delete_preset_button.Bind(wx.EVT_BUTTON, self.delete_preset)

        self.cancel_button = wx.Button(self, wx.ID_ANY, "Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.close)

        self.apply_button = wx.Button(self, wx.ID_ANY, "Apply and Quit")
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def update_preset_list(self):
        self.preset_chooser.SetItems(load_presets().keys())

    def get_preset_name(self):
        preset_name = self.preset_chooser.GetValue().strip()
        if preset_name:
            return preset_name
        else:
            info_dialog(self, "Please enter or select a preset name first.", caption='Preset')
            return

    def check_and_load_preset(self, preset_name):
        preset = load_preset(preset_name)
        if not preset:
            info_dialog(self, 'Preset "%s" not found.' % preset_name, caption='Preset')

        return preset

    def get_preset_data(self):
        preset = {}

        current_tab = self.tabs[self.notebook.GetSelection()]
        while current_tab.parent_tab:
            current_tab = current_tab.parent_tab

        tabs = [current_tab]
        if current_tab.paired_tab:
            tabs.append(current_tab.paired_tab)
        tabs.extend(current_tab.dependent_tabs)

        for tab in tabs:
            tab.save_preset(preset)

        return preset

    def add_preset(self, event, overwrite=False):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        if not overwrite and load_preset(preset_name):
            info_dialog(self, 'Preset "%s" already exists.  Please use another name or press "Overwrite"' % preset_name, caption='Preset')

        save_preset(preset_name, self.get_preset_data())
        self.update_preset_list()

        event.Skip()

    def overwrite_preset(self, event):
        self.add_preset(event, overwrite=True)

    def load_preset(self, event):
        preset_name = self.get_preset_name()
        if not preset_name:
            return

        preset = self.check_and_load_preset(preset_name)         
        if not preset:
            return
        
        for tab in self.tabs:
            tab.load_preset(preset)

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
        for tab in self.tabs:
            tab.apply()

        self.Close()

    def close(self, event):
        self.Close()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Embroidery Params")
        self.notebook.SetMinSize((800, 400))
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
        sizer_3.Add(self.apply_button, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)
        sizer_1.Add(sizer_3, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

class EmbroiderParams(inkex.Effect):
    def get_nodes(self):
        if self.selected:
            nodes = []
            for node in self.document.getroot().iter():
                if node.get("id") in self.selected:
                    nodes.extend(descendants(node))
        else:
            nodes = descendants(self.document.getroot())

        return nodes

    def embroidery_classes(self, node):
        element = EmbroideryElement(node)
        classes = []

        if element.get_style("fill"):
            classes.append(AutoFill)
            classes.append(Fill)
            classes.append(SergFill)
        if element.get_style("stroke"):
            classes.append(Stroke)

            if element.get_style("stroke-dasharray") is None:
                classes.append(SatinColumn)

        return classes

    def get_nodes_by_class(self):
        nodes = self.get_nodes()
        nodes_by_class = defaultdict(list)

        for node in self.get_nodes():
            for cls in self.embroidery_classes(node):
                nodes_by_class[cls].append(node)

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
        def by_group(param):
            return param.group

        return groupby(sorted(params, key=by_group), by_group)

    def create_tabs(self, parent):
        tabs = []
        for cls, nodes in self.get_nodes_by_class():
            nodes = [cls(node) for node in nodes]
            params = cls.get_params()

            for param in params:
                param.values = self.get_values(param, nodes)

            parent_tab = None
            new_tabs = []
            for group, params in self.group_params(params):
                tab = ParamsTab(parent, id=wx.ID_ANY, name=group or cls.__name__, params=list(params), nodes=nodes)
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


    def effect(self):
        app = wx.App()
        frame = SettingsFrame(tabs_factory=self.create_tabs)
        frame.Show()
        app.MainLoop()


def save_stderr():
    # GTK likes to spam stderr, which inkscape will show in a dialog.
    null = open('/dev/null', 'w')
    sys.stderr_dup = os.dup(sys.stderr.fileno())
    os.dup2(null.fileno(), 2)
    sys.stderr_backup = sys.stderr
    sys.stderr = StringIO()


def restore_stderr():
    os.dup2(sys.stderr_dup, 2)
    sys.stderr_backup.write(sys.stderr.getvalue())
    sys.sys.stderr = stderr_backup


# end of class MyFrame
if __name__ == "__main__":
    save_stderr()

    try:
        e = EmbroiderParams()
        e.affect()
    except:
        traceback.print_exc()

    restore_stderr()
