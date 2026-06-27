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
from ...svg.tags import INKSCAPE_LABEL, INKSTITCH_SATIN_MULTICOLOR
import json
from ...utils import DotDict


class MultiColorSatinPanel(wx.Panel):

    def __init__(self, parent, simulator, elements, metadata=None, background_color='white'):
        self.parent = parent
        self.elements = elements

        self.simulator = simulator
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

        self.is_reedit = self.load_settings()
        self.satin_elements = []
        if not len(self.settings.colors):
            self.settings.colors.append(
                DotDict({
                    "value": self.elements[0].color,
                    "width": 100,
                    "margin": 0
                }))

        self.apply_settings()

        self.SetSizerAndFit(self.notebook_sizer)

        self.Layout()

    def create_group(self):
        group = inkex.Group(attrib={
            INKSCAPE_LABEL: _("Ink/Stitch Multicolor Satin"),
        })
        return group

    def load_settings(self):
        """Load the settings saved into the SVG group element"""
        self.settings = DotDict({
            "equidistance": True,
            "monochrome_width": 100,
            "colors": [],
            "overflow_left": 0,
            "overflow_right": 0,
            "pull_compensation": 0,
            "seed": "",
            "adjust_underlay_per_color": False
        })
        self.reedit_group = None
        self.reedit_layer = None
        self.reedit_index = None
        self.reedit_template_node = None

        # TODO improve by verifying if multiple parents exist with satin config and if so throw error - we can only reedit one at a time
        parent = self.elements[0].node.getparent()
        if parent and INKSTITCH_SATIN_MULTICOLOR in parent.attrib:
            try:
                json_config = json.loads(
                    parent.get(INKSTITCH_SATIN_MULTICOLOR))
                self.settings.update(json_config)

                self.settings.colors = []

                for color_json in json_config["colors"]:
                    self.settings.colors.append(DotDict(color_json))

                self.reedit_group = parent
                self.reedit_layer = parent.getparent()
                if self.reedit_layer is not None:
                    self.reedit_index = self.reedit_layer.index(parent)
                self.reedit_template_node = copy(self.elements[0].node)
                self.elements = [self.elements[0]]
                return True
            except (TypeError, ValueError):
                return False
        return False

    def apply_settings(self):
        self.colorize_panel.equististance.SetValue(self.settings.equidistance)
        self.colorize_panel.monochrome_width.SetValue(self.settings.monochrome_width)
        self.colorize_panel.overflow_left.SetValue(self.settings.overflow_left)
        self.colorize_panel.overflow_right.SetValue(self.settings.overflow_right)
        self.colorize_panel.pull_compensation.SetValue(self.settings.pull_compensation)
        self.colorize_panel.adjust_underlay_per_color.SetValue(self.settings.adjust_underlay_per_color)
        if self.settings.seed:
            self.colorize_panel.seed.SetValue(self.settings.seed)
        for color in self.settings.colors:
            self.colorize_panel.add_color(color.value, color.width, color.margin_right)

    def save_settings(self):
        """Save the settings into the SVG group element."""

        self.settings.equidistance = self.colorize_panel.equististance.GetValue()
        self.settings.monochrome_width = self.colorize_panel.monochrome_width.GetValue()
        self.settings.overflow_left = self.colorize_panel.overflow_left.GetValue()
        self.settings.overflow_right = self.colorize_panel.overflow_right.GetValue()
        self.settings.pull_compensation = self.colorize_panel.pull_compensation.GetValue()
        self.settings.adjust_underlay_per_color = self.colorize_panel.adjust_underlay_per_color.GetValue()
        self.settings.seed = self.colorize_panel.seed.GetValue()

        colors = [
            DotDict({
                "value": c.GetWindow().colorpicker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
                "width": c.GetWindow().color_width.GetValue(),
                "margin_right": c.GetWindow().color_margin_right.GetValue()
            })
            for c in self.colorize_panel.color_sizer.GetChildren()]

        self.settings.colors = colors

        for group in self.output_groups:
            group.set(INKSTITCH_SATIN_MULTICOLOR, json.dumps(self.settings))

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
        if not self.is_reedit and not self.colorize_panel.keep_original.GetValue():
            for element in self.elements:
                element.node.delete()

        self.save_settings()
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

    def _update_satin_column(self, new_satin, color, pull_compensation, seed, element, i, margin, previous_margin, current_position, width):
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
        return current_position

    def update_satin_elements(self):
        for out_group in self.output_groups:
            if self.is_reedit and out_group is self.reedit_group:
                for child in list(out_group):
                    out_group.remove(child)
            else:
                out_group.delete()

        self.output_groups = []
        self.satin_elements = []

        overflow_left = self.colorize_panel.overflow_left.GetValue()
        overflow_right = self.colorize_panel.overflow_right.GetValue()
        pull_compensation = self.colorize_panel.pull_compensation.GetValue()
        seed = self.colorize_panel.seed.GetValue()

        color_sizer = self.colorize_panel.color_sizer.GetChildren()
        num_colors = len(color_sizer)
        for element in self.elements:
            if self.is_reedit:
                group = self.reedit_group
                layer = self.reedit_layer
                index = self.reedit_index
                template_node = self.reedit_template_node
            else:
                group = self.create_group()
                layer = element.node.getparent()
                index = layer.index(element.node)
                template_node = element.node

            check_stop_flag()
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

                new_satin = copy(template_node)
                current_position = self._update_satin_column(
                    new_satin, color, pull_compensation, seed, element, i, margin, previous_margin, current_position, width)
                previous_margin = margin

                group.add(new_satin)
                self.satin_elements.append(new_satin)

            if not self.is_reedit and layer is not group:
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

    def on_change(self, attribute, event):
        value = event.GetEventObject().GetValue()
        self.settings[attribute] = value
