# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

# Lightweight stub -- heavy wx / GUI imports are deferred to params_gui.py
# and only loaded when effect() actually runs.

import sys
from collections import defaultdict
from itertools import groupby

from .base import InkstitchExtension


class Params(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        self.cancelled = False
        InkstitchExtension.__init__(self, *args, **kwargs)

    def embroidery_classes(self, node):
        from ..commands import is_command, is_command_symbol
        from ..elements import Clone, EmbroideryElement, FillStitch, SatinColumn, Stroke
        from ..elements.clone import is_clone
        from ..svg.tags import EMBROIDERABLE_TAGS

        element = EmbroideryElement(node)
        classes = []

        if not is_command(node) and not is_command_symbol(node):
            if is_clone(node):
                classes.append(Clone)
            elif node.tag in EMBROIDERABLE_TAGS and not node.get_path():
                pass
            else:
                if element.fill_color is not None and not element.get_style("fill-opacity", 1) == "0":
                    classes.append(FillStitch)
                if element.stroke_color is not None:
                    if len(element.path) > 1 or element.stroke_width >= element.satin_threshold:
                        classes.append(SatinColumn)
                    classes.append(Stroke)
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
        if param.type in ('toggle', 'boolean'):
            getter = 'get_boolean_param'
            values = [item for item in (getattr(node, getter)(
                param.name, param.default) for node in nodes) if item is not None]
        else:
            getter = 'get_param'
            values = [item if item is not None else "" for item in (getattr(node, getter)(
                param.name, param.default) for node in nodes)]

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
                parent.toggle and parent.toggle_checkbox.IsChecked(),
                parent and parent.name,
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
        import wx
        from .params_gui import NoValidObjects, ParamsTab

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
                tab = ParamsTab(parent, id=wx.ID_ANY, name=tab_name,
                                params=list(params), nodes=nodes)
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
        import wx
        from ..gui.simulator import SplitSimulatorWindow
        from ..i18n import _
        from ..utils.svg_data import get_pagecolor
        from .params_gui import NoValidObjects, SettingsPanel

        nodes = self.get_nodes()
        try:
            app = wx.App()
            wx.DisableAsserts()
            metadata = self.get_inkstitch_metadata()
            background_color = get_pagecolor(self.svg.namedview)
            frame = SplitSimulatorWindow(
                title=_("Embroidery Params"),
                panel_class=SettingsPanel,
                nodes=nodes,
                tabs_factory=self.create_tabs,
                on_cancel=self.cancel,
                metadata=metadata,
                background_color=background_color,
                target_duration=5,
            )

            frame.Show()
            app.MainLoop()

            if self.cancelled:
                sys.exit(0)
        except NoValidObjects:
            self.no_elements_error()
