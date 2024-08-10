# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

import sys
from copy import copy

import wx
from wx.lib.agw import ultimatelistctrl as ulc
from wx.lib.splitter import MultiSplitterWindow

from .base import InkstitchExtension
from ..debug.debug import debug
from ..exceptions import InkstitchException, format_uncaught_exception
from ..gui import PreviewRenderer, WarningPanel
from ..gui.simulator import SplitSimulatorWindow
from ..i18n import _
from ..sew_stack import SewStack
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..utils.svg_data import get_pagecolor
from ..utils.threading import ExitThread, check_stop_flag


class SewStackPanel(wx.Panel):
    def __init__(self, parent, sew_stacks=None, metadata=None, background_color='white', simulator=None):
        super().__init__(parent, wx.ID_ANY)

        self.sew_stacks = sew_stacks
        self.metadata = metadata
        self.background_color = background_color
        self.simulator = simulator
        self.parent = parent
        self.layers = self.sew_stacks[0].layers

        self.splitter = MultiSplitterWindow(self, wx.ID_ANY, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetOrientation(wx.VERTICAL)

        self.layer_list = ulc.UltimateListCtrl(
            parent=self.splitter,
            size=(300, 200),
            agwStyle=ulc.ULC_REPORT | ulc.ULC_SINGLE_SEL | ulc.ULC_VRULES | ulc.ULC_HAS_VARIABLE_ROW_HEIGHT
        )
        self.update_layer_list()
        self.splitter.AppendWindow(self.layer_list, 300)
        self.layer_config_panel = None
        self.splitter.SizeWindows()

        self._dragging_row = None
        self._editing_row = None
        self._name_editor = None

        self.layer_list.Bind(ulc.EVT_LIST_BEGIN_DRAG, self.on_begin_drag)
        self.layer_list.Bind(ulc.EVT_LIST_END_DRAG, self.on_end_drag)
        self.layer_list.Bind(ulc.EVT_LIST_ITEM_ACTIVATED, self.on_double_click)
        self.layer_list.Bind(ulc.EVT_LIST_ITEM_SELECTED, self.on_layer_selection_changed)
        # self.layer_list.Bind(ulc.EVT_LIST_ITEM_DESELECTED, self.on_layer_selection_changed)

        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)

        self.warning_panel = WarningPanel(self)
        self.warning_panel.Hide()

        self.cancel_button = wx.Button(self, wx.ID_ANY, _("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.Bind(wx.EVT_CLOSE, self.cancel)

        self.apply_button = wx.Button(self, wx.ID_ANY, _("Apply and Quit"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)

        self.__do_layout()
        self.update_preview()

    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.warning_panel, 0, flag=wx.ALL, border=10)
        main_sizer.Add(self.splitter, 1, wx.LEFT | wx.TOP | wx.RIGHT, 10)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.cancel_button, 0, wx.RIGHT, 5)
        buttons_sizer.Add(self.apply_button, 0, wx.BOTTOM, 5)
        main_sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def update_layer_list(self):
        self.layer_list.Freeze()

        if self.layer_list.GetColumnCount() == 3:
            # Save and restore column widths to work around an UltimateListCtrl bug.
            # If we don't do this, ULC_AUTOSIZE_FILL stops working and the layer name
            # column shrinks.
            column_sizes = [self.layer_list.GetColumn(i).GetWidth() for i in range(self.layer_list.GetColumnCount())]
        else:
            column_sizes = (24, wx.LIST_AUTOSIZE, ulc.ULC_AUTOSIZE_FILL)

        self.layer_list.ClearAll()

        self.layer_list.InsertColumn(0, "", format=ulc.ULC_FORMAT_RIGHT)
        self.layer_list.InsertColumn(1, _("Type"), format=ulc.ULC_FORMAT_CENTER)
        self.layer_list.InsertColumn(2, _("Name"))

        for i, layer in enumerate(self.layers):
            item = ulc.UltimateListItem()
            item.SetMask(ulc.ULC_MASK_KIND | ulc.ULC_MASK_CHECK | ulc.ULC_MASK_FORMAT | ulc.ULC_MASK_ENABLE)
            item.SetKind(1)  # 1 is "a checkbox-like item"
            item.SetAlign(ulc.ULC_FORMAT_RIGHT)
            item.Check(layer.enabled)
            item.Enable(layer.enabled)
            item.SetId(i)
            item.SetColumn(0)
            self.layer_list.InsertItem(item)

            self.layer_list.SetStringItem(i, 1, layer.type_name)
            self.layer_list.SetStringItem(i, 2, layer.name)

        # insert one more row so that the UltimateListCtrl allows dragging items to the very
        # end of the list
        self.layer_list.InsertStringItem(len(self.layers), "")
        self.layer_list.EnableItem(len(self.layers), enable=False)

        for i, size in enumerate(column_sizes):
            self.layer_list.SetColumnWidth(i, size)

        self.layer_list.Thaw()

    def on_begin_drag(self, event):
        self.stop_editing()
        self._dragging_row = event.Index

    def on_end_drag(self, event):
        self.stop_editing()
        if self._dragging_row is not None:
            row = self.layers.pop(self._dragging_row)
            destination = event.Index
            if destination > self._dragging_row:
                destination -= 1
            self.layers.insert(destination, row)
            self.update_layer_list()
            self._dragging_row = None

    def on_double_click(self, event):
        debug.log(f"double-click {event.Index}")

        if event.GetColumn() != 2:
            event.Veto()
            return

        self.stop_editing()

        self._editing_row = event.Index
        self._name_editor = wx.TextCtrl(self.layer_list, wx.ID_ANY, value=self.layers[event.Index].name,
                                        style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_LEFT)
        self._name_editor.Bind(wx.EVT_TEXT_ENTER, self.on_name_editor_end)
        self._name_editor.Bind(wx.EVT_KEY_UP, self.on_name_editor_key_up)
        self.layer_list.SetItemWindow(event.Index, 2, self._name_editor, expand=True)

    def on_name_editor_key_up(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.stop_editing(cancel=True)
        else:
            event.Skip()

    def on_name_editor_end(self, event):
        self.stop_editing()

    def on_layer_selection_changed(self, event):
        self.stop_editing()
        debug.log(f"layer selection changed: {event.Index} {self.layer_list.GetFirstSelected()}")
        if -1 < event.Index < len(self.layers):
            selected_layer = self.layers[event.Index]
            new_layer_config_panel = selected_layer.get_property_grid_panel(parent=self.splitter)

            if self.layer_config_panel is not None:
                self.layer_config_panel.Hide()
                self.splitter.ReplaceWindow(self.layer_config_panel, new_layer_config_panel)
            else:
                self.splitter.AppendWindow(new_layer_config_panel)
            self.layer_config_panel = new_layer_config_panel
            self.splitter.SizeWindows()

            self.Layout()

    def stop_editing(self, cancel=False):
        if self._name_editor is None or self._editing_row is None:
            return

        if not cancel:
            new_name = self._name_editor.GetValue()
            self.layers[self._editing_row].name = new_name
            self.layer_list.DeleteItemWindow(self._editing_row, 2)
            item = self.layer_list.GetItem(self._editing_row, 2)
            item.SetMask(ulc.ULC_MASK_TEXT)
            item.SetText(new_name)
            self.layer_list.SetItem(item)

        self._name_editor.Hide()
        self._name_editor.Destroy()
        self._name_editor = None
        self._editing_row = None

    def update_preview(self):
        self.simulator.stop()
        self.simulator.clear()
        self.preview_renderer.update()

    def render_stitch_plan(self):
        return
        stitch_groups = []
        nodes = []
        # move the stroke tab to the end of the list
        tabs = self.get_stroke_last_tabs()
        for tab in tabs:
            tab.apply()
            if tab.enabled() and not tab.is_dependent_tab():
                nodes.extend(tab.nodes)

            check_stop_flag()

        # sort nodes into the proper stacking order
        nodes.sort(key=lambda node: node.order)

        try:
            wx.CallAfter(self._hide_warning)
            last_stitch_group = None
            for node in nodes:
                # Making a copy of the embroidery element is an easy
                # way to drop the cache in the @cache decorators used
                # for many params in embroider.py.

                stitch_groups.extend(copy(node).embroider(last_stitch_group))
                if stitch_groups:
                    last_stitch_group = stitch_groups[-1]

                check_stop_flag()

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
        try:
            self.simulator.stop()
            self.simulator.load(stitch_plan)
            self.simulator.go()
        except RuntimeError:
            # this can happen when they close the window at a bad time
            pass

    def _hide_warning(self):
        self.warning_panel.clear()
        self.warning_panel.Hide()
        self.Layout()

    def _show_warning(self, warning_text):
        self.warning_panel.set_warning_text(warning_text)
        self.warning_panel.Show()
        self.Layout()

    def _apply(self):
        pass

    def apply(self, event):
        self._apply()
        self.close()

    def use_last(self, event):
        self.presets_panel.load_preset("__LAST__")
        self.apply(event)

    def close(self):
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().close)

    def cancel(self, event):
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().cancel)


class SewStackEditor(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        self.cancelled = False
        InkstitchExtension.__init__(self, *args, **kwargs)

    def cancel(self):
        self.cancelled = True

    def get_sew_stacks(self):
        nodes = self.get_nodes()
        if nodes:
            return [SewStack(node) for node in nodes]
        else:
            self.no_elements_error()

    def effect(self):
        app = wx.App()
        metadata = self.get_inkstitch_metadata()
        background_color = get_pagecolor(self.svg.namedview)
        frame = SplitSimulatorWindow(
            title=_("Embroidery Params"),
            panel_class=SewStackPanel,
            sew_stacks=self.get_sew_stacks(),
            on_cancel=self.cancel,
            metadata=metadata,
            background_color=background_color,
            target_duration=5
        )

        frame.Show()
        app.MainLoop()

        if self.cancelled:
            # This prevents the superclass from outputting the SVG, because we
            # may have modified the DOM.
            sys.exit(0)
