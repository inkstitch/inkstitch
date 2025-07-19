# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import copy

import inkex
import wx
import wx.adv

from ...elements import nodes_to_elements
from ...exceptions import InkstitchException, format_uncaught_exception
from ...i18n import _
from ...stitch_plan import stitch_groups_to_stitch_plan
from ...utils.threading import ExitThread, check_stop_flag
from .. import PreviewRenderer, WarningPanel
from . import ColorizePanel, HelpPanel


class MultiColorSatinPanel(wx.Panel):

    def __init__(self, parent, simulator, elements, metadata=None, background_color='white'):
        self.parent = parent
        self.simulator = simulator
        self.elements = elements
        self.metadata = metadata or dict()
        self.background_color = background_color
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

        self.colorize_panel.add_color(self.elements[0].color)

        self.SetSizerAndFit(self.notebook_sizer)

        self.Layout()

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
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().close)

    def cancel(self, event):
        self.simulator.stop()
        wx.CallAfter(self.GetTopLevelParent().cancel)

    def apply(self, event):
        self.update_satin_elements()
        if not self.colorize_panel.keep_original.GetValue():
            for element in self.elements:
                element.node.delete()
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
        elements = nodes_to_elements(self.satin_elements)

        stitch_groups = []
        last_stitch_group = None
        next_elements = [None]
        if len(elements) > 1:
            next_elements = elements[1:] + next_elements
        for element, next_element in zip(elements, next_elements):
            try:
                stitch_group = element.embroider(last_stitch_group, next_element)
                stitch_groups.extend(stitch_group)

                if stitch_groups:
                    last_stitch_group = stitch_groups[-1]
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
            group.delete()
        self.output_groups = []

        overflow_left = self.colorize_panel.overflow_left.GetValue()
        overflow_right = self.colorize_panel.overflow_right.GetValue()
        pull_compensation = self.colorize_panel.pull_compensation.GetValue()
        seed = self.colorize_panel.seed.GetValue()

        self.satin_elements = []
        color_sizer = self.colorize_panel.color_sizer.GetChildren()
        num_colors = len(color_sizer)
        for element in self.elements:
            check_stop_flag()
            layer = element.node.getparent()
            index = layer.index(element.node)
            group = inkex.Group()
            group.label = _("Multicolor Satin Group")
            current_position = 0
            previous_margin = overflow_left
            for i, color_panel in enumerate(color_sizer):
                panel = color_panel.GetWindow()
                color = panel.colorpicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                if i == num_colors - 1:
                    margin = overflow_right
                else:
                    margin = panel.color_margin_right.GetValue()
                width = panel.color_width.GetValue()

                new_satin = copy(element.node)
                new_satin.style['stroke'] = color
                new_satin.set('inkstitch:pull_compensation_mm', pull_compensation)
                new_satin.set('inkstitch:random_seed', seed)

                reverse_rails = self._get_new_reverse_rails_param(element, i)
                if reverse_rails is not None:
                    new_satin.set('inkstitch:reverse_rails', reverse_rails)

                if i % 2 == 0:
                    new_satin.set('inkstitch:swap_satin_rails', False)
                    new_satin.set('inkstitch:random_width_increase_percent', f'{ margin } 0')
                    new_satin.set('inkstitch:random_width_decrease_percent', f'0 { -previous_margin }')
                    new_satin.set('inkstitch:pull_compensation_percent', f'{ current_position + width - 100} { -current_position }')
                    new_satin.set('inkstitch:running_stitch_position', f'{100 - current_position - width / 2}')
                else:
                    new_satin.set('inkstitch:swap_satin_rails', True)
                    new_satin.set('inkstitch:random_width_increase_percent', f'0 { margin }')
                    new_satin.set('inkstitch:random_width_decrease_percent', f'{ -previous_margin } 0')
                    new_satin.set('inkstitch:pull_compensation_percent', f'{ -current_position } { current_position + width - 100}')
                    new_satin.set('inkstitch:running_stitch_position', f'{current_position + width / 2}')

                # underlay
                if self.colorize_panel.adjust_underlay_per_color.GetValue():
                    if i % 2 == 0:
                        new_satin.set('inkstitch:center_walk_underlay_position', f'{ 100 - current_position - width / 2 }')
                        new_satin.set('inkstitch:contour_underlay_inset_percent', f'{ 100 - current_position - width } { current_position }')
                        new_satin.set('inkstitch:zigzag_underlay_inset_percent', f'{ 100 - current_position - width} { current_position }')
                    else:
                        new_satin.set('inkstitch:center_walk_underlay_position', f'{ current_position + width / 2 }')
                        new_satin.set('inkstitch:contour_underlay_inset_percent', f'{ current_position } { 100 - current_position - width }')
                        new_satin.set('inkstitch:zigzag_underlay_inset_percent', f'{ current_position } { 100 - current_position - width }')
                elif i > 0:
                    new_satin.set('inkstitch:center_walk_underlay', False)
                    new_satin.set('inkstitch:contour_underlay', False)
                    new_satin.set('inkstitch:zigzag_underlay', False)

                previous_margin = margin
                current_position += width + margin

                group.add(new_satin)
                self.satin_elements.append(new_satin)

            layer.insert(index + 1, group)
            self.output_groups.append(group)

    def _get_new_reverse_rails_param(self, element, i):
        reverse_rails = element._get_rails_to_reverse()
        if any(reverse_rails) and element.reverse_rails == 'automatic':
            if (reverse_rails[0] and i % 2 == 0) or (reverse_rails[1] and i % 2 != 0):
                return 'first'
            else:
                return 'second'
        return None

    def on_stitch_plan_rendered(self, stitch_plan):
        self.simulator.stop()
        self.simulator.load(stitch_plan)
        self.simulator.go()
