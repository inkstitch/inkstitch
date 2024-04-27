# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import copy

import inkex
import wx
import wx.adv

from ...elements import SatinColumn
from ...exceptions import InkstitchException, format_uncaught_exception
from ...i18n import _
from ...stitch_plan import stitch_groups_to_stitch_plan
from ...utils.threading import ExitThread, check_stop_flag
from .. import PreviewRenderer, WarningPanel
from .colorize import ColorizePanel
from .help_panel import HelpPanel


class MultiColorSatinPanel(wx.Panel):

    def __init__(self, parent, simulator, elements, on_cancel=None, metadata=None, output_groups=[]):
        self.parent = parent
        self.simulator = simulator
        self.elements = elements
        self.cancel_hook = on_cancel
        self.metadata = metadata or dict()
        self.output_groups = []

        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        # preview
        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)
        # warnings
        self.warning_panel = WarningPanel(self)
        self.warning_panel.Hide()
        # notebook
        self.notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.notebook_sizer.Add(self.warning_panel, 0, wx.EXPAND | wx.ALL, 10)
        self.notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)
        # customize
        self.colorize_panel = ColorizePanel(self.notebook, self)
        self.notebook.AddPage(self.colorize_panel, _('Colorize'))
        self.colorize_panel.SetupScrolling()
        # help
        help_panel = HelpPanel(self.notebook)
        self.notebook.AddPage(help_panel, _("Help"))
        # apply and cancel buttons
        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 5)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        self.notebook_sizer.Add(apply_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(self.notebook_sizer)

        self.colorize_panel.add_color(self.elements[0].color)

        self.Layout()
        self.SetMinSize(self.notebook_sizer.CalcMin())

    def _hide_warning(self):
        self.warning_panel.clear()
        self.warning_panel.Hide()
        self.Layout()

    def _show_warning(self, warning_text):
        self.warning_panel.set_warning_text(warning_text)
        self.warning_panel.Show()
        self.Layout()

    def update_preview(self, event=None):
        self.preview_renderer.update()

    def close(self):
        self.GetTopLevelParent().Close()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()
        self.close()

    def apply(self, event):
        self.update_satin_elements()
        self.close()

    def render_stitch_plan(self):
        self.update_satin_elements()
        stitch_groups = self._get_stitch_groups()

        if stitch_groups:
            stitch_plan = stitch_groups_to_stitch_plan(
                stitch_groups,
                collapse_len=self.metadata['collapse_len_mm'],
                min_stitch_len=self.metadata['min_stitch_len_mm']
            )
            return stitch_plan

    def _get_stitch_groups(self):
        stitch_groups = []
        for element in self.satin_elements:
            try:
                # copy the embroidery element to drop the cache
                stitch_group = copy(SatinColumn(element)).embroider(None)
                stitch_groups.extend(stitch_group)
            except (SystemExit, ExitThread):
                raise
            except InkstitchException as exc:
                wx.CallAfter(self._show_warning, str(exc))
            except Exception:
                wx.CallAfter(self._show_warning, format_uncaught_exception())
        return stitch_groups

    def update_satin_elements(self):
        # empty old groups
        for group in self.output_groups:
            group.getparent().remove(group)
        self.output_groups = []

        overflow_left = self.colorize_panel.overflow_left.GetValue()
        overflow_right = self.colorize_panel.overflow_right.GetValue()
        seed = self.colorize_panel.seed.GetValue()

        self.satin_elements = []
        color_sizer = self.colorize_panel.color_sizer.GetChildren()
        num_colors = len(color_sizer)
        for element in self.elements:
            check_stop_flag()
            layer = element.node.getparent()
            index = layer.index(element.node)
            group = inkex.Group()
            current_position = 0
            previous_margin = overflow_left
            for i, segment_sizer in enumerate(color_sizer):
                segment = segment_sizer.GetSizer().GetChildren()
                color = segment[1].GetWindow().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                if i == num_colors - 1:
                    margin = overflow_right
                else:
                    margin = segment[2].GetWindow().GetValue()
                width = segment[3].GetWindow().GetValue()

                new_satin = copy(element.node)
                new_satin.style['stroke'] = color
                new_satin.set('inkstitch:random_seed', seed)

                if i % 2 == 0:
                    new_satin.set('inkstitch:swap_satin_rails', False)
                    new_satin.set('inkstitch:random_width_increase_percent', f'{ margin } 0')
                    new_satin.set('inkstitch:random_width_decrease_percent', f'0 { -previous_margin }')
                    new_satin.set('inkstitch:pull_compensation_percent', f'{  current_position + width - 100} { -current_position }')
                else:
                    new_satin.set('inkstitch:swap_satin_rails', True)
                    new_satin.set('inkstitch:random_width_increase_percent', f'0 { margin }')
                    new_satin.set('inkstitch:random_width_decrease_percent', f'{ -previous_margin } 0')
                    new_satin.set('inkstitch:pull_compensation_percent', f'{ -current_position } { current_position + width - 100}')

                previous_margin = margin
                current_position += width + margin

                group.add(new_satin)
                self.satin_elements.append(new_satin)

            layer.insert(index + 1, group)
            self.output_groups.append(group)

    def on_stitch_plan_rendered(self, stitch_plan):
        self.simulator.stop()
        self.simulator.load(stitch_plan)
        self.simulator.go()
