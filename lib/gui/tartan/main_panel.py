# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from copy import copy

import inkex
import wx
import wx.adv

from ...elements import FillStitch, nodes_to_elements
from ...exceptions import InkstitchException, format_uncaught_exception
from ...i18n import _
from ...stitch_plan import stitch_groups_to_stitch_plan
from ...svg.tags import INKSTITCH_TARTAN
from ...tartan.fill_element import prepare_tartan_fill_element
from ...tartan.pallet import Pallet
from ...tartan.svg import TartanSvgGroup
from ...utils import DotDict
from ...utils.threading import ExitThread, check_stop_flag
from .. import PresetsPanel, PreviewRenderer, WarningPanel
from . import CodePanel, CustomizePanel, EmbroideryPanel, HelpPanel


class TartanMainPanel(wx.Panel):

    def __init__(self, parent, simulator, elements, on_cancel=None, metadata=None, output_groups=inkex.Group()):
        self.parent = parent
        self.simulator = simulator
        self.elements = elements
        self.cancel_hook = on_cancel
        self.pallet = Pallet()
        self.metadata = metadata or dict()
        self.output_groups = output_groups

        super().__init__(parent, wx.ID_ANY)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        # preview
        self.preview_renderer = PreviewRenderer(self.render_stitch_plan, self.on_stitch_plan_rendered)
        self.presets_panel = PresetsPanel(self)
        # warnings
        self.warning_panel = WarningPanel(self)
        self.warning_panel.Hide()
        # notebook
        self.notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.notebook_sizer.Add(self.warning_panel, 0, wx.EXPAND | wx.ALL, 10)
        self.notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)
        # customize
        self.customize_panel = CustomizePanel(self.notebook, self)
        self.notebook.AddPage(self.customize_panel, _('Customize'))
        self.customize_panel.SetupScrolling()  # scroll_x=False)
        # code
        self.code_panel = CodePanel(self.notebook, self)
        self.notebook.AddPage(self.code_panel, _("Pallet Code"))
        # embroidery settings
        self.embroidery_panel = EmbroideryPanel(self.notebook, self)
        self.notebook.AddPage(self.embroidery_panel, _("Embroidery Settings"))
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

        self.notebook_sizer.Add(self.presets_panel, 0, wx.EXPAND | wx.ALL, 10)
        self.notebook_sizer.Add(apply_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(self.notebook_sizer)

        self.load_settings()
        self.apply_settings()

        self.Layout()
        self.SetMinSize(self.notebook_sizer.CalcMin())

    def update_from_code(self):
        self.pallet.update_from_code(self.code_panel.threadcount_text.GetValue())
        self.customize_panel.symmetry_checkbox.SetValue(self.pallet.symmetry)
        self.customize_panel.warp_weft_checkbox.SetValue(self.pallet.equal_warp_weft)
        self.code_panel.threadcount_text.SetValue(self.pallet.pallet_code)
        self.customize_panel.update_stripes(self.pallet.pallet_stripes)
        self.customize_panel.update_symmetry()
        self.customize_panel.update_warp_weft()
        self.customize_panel.FitInside()
        self.update_preview()

    def update_from_stripes(self):
        sizers = [self.customize_panel.warp_sizer]
        if not self.customize_panel.warp_weft_checkbox.GetValue():
            sizers.append(self.customize_panel.weft_sizer)
        self.pallet.update_from_stripe_sizer(
            sizers,
            self.customize_panel.symmetry_checkbox.GetValue(),
            self.customize_panel.warp_weft_checkbox.GetValue()
        )
        self.update_code_text()
        self.update_preview()

    def update_code_text(self):
        self.code_panel.threadcount_text.SetValue(self.pallet.pallet_code)
        self.settings['pallet'] = self.pallet.pallet_code

    def load_settings(self):
        """Load the settings saved into the SVG element"""
        self.settings = DotDict({
            "symmetry": True,
            "equal_warp_weft": True,
            "rotate": 0.0,
            "scale": 100,
            "offset_x": 0.0,
            "offset_y": 0.0,
            "pallet": "K/10 W/?10",
            "output": "embroidery",
            "stitch_type": "legacy_fill",
            "row_spacing": 1.0,
            "angle_warp": 0.0,
            "angle_weft": 90.0,
            "min_stripe_width": 1.0,
            "bean_stitch_repeats": 0
        })

        try:
            self.settings.update(json.loads(self.elements[0].get(INKSTITCH_TARTAN)))
        except (TypeError, ValueError, IndexError):
            pass

    def apply_settings(self):
        """Make the settings in self.settings visible in the UI."""
        self.customize_panel.rotate.SetValue(self.settings.rotate)
        self.customize_panel.scale.SetValue(int(self.settings.scale))
        self.customize_panel.offset_x.SetValue(self.settings.offset_x)
        self.customize_panel.offset_y.SetValue(self.settings.offset_y)
        self.code_panel.threadcount_text.SetValue(self.settings.pallet)
        self.embroidery_panel.set_output(self.settings.output)
        self.embroidery_panel.set_stitch_type(self.settings.stitch_type)
        self.embroidery_panel.svg_row_spacing.SetValue(self.settings.row_spacing)
        self.embroidery_panel.angle_warp.SetValue(self.settings.angle_warp)
        self.embroidery_panel.angle_weft.SetValue(self.settings.angle_weft)
        self.embroidery_panel.min_stripe_width.SetValue(self.settings.min_stripe_width)
        self.embroidery_panel.svg_bean_stitch_repeats.SetValue(self.settings.bean_stitch_repeats)
        self.embroidery_panel.stitch_angle.SetValue(self.elements[0].get('inkstitch:tartan_angle', -45))
        self.embroidery_panel.rows_per_thread.SetValue(self.elements[0].get('inkstitch:rows_per_thread', 2))
        self.embroidery_panel.row_spacing.SetValue(self.elements[0].get('inkstitch:row_spacing_mm', 0.25))
        underlay = self.elements[0].get('inkstitch:fill_underlay', "True").lower() in ('yes', 'y', 'true', 't', '1')
        self.embroidery_panel.underlay.SetValue(underlay)
        self.embroidery_panel.herringbone.SetValue(self.elements[0].get('inkstitch:herringbone_width_mm', 0))
        self.embroidery_panel.bean_stitch_repeats.SetValue(self.elements[0].get('inkstitch:bean_stitch_repeats', '0'))

        self.update_from_code()

        self.customize_panel.symmetry_checkbox.SetValue(bool(self.settings.symmetry))
        self.pallet.update_symmetry(self.settings.symmetry)
        self.customize_panel.warp_weft_checkbox.SetValue(bool(self.settings.equal_warp_weft))
        self.customize_panel.update_warp_weft()

    def save_settings(self):
        """Save the settings into the SVG elements."""
        for element in self.elements:
            element.set(INKSTITCH_TARTAN, json.dumps(self.settings))

    def get_preset_data(self):
        # called by self.presets_panel
        settings = dict(self.settings)
        return settings

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

    def apply_preset_data(self, preset_data):
        settings = DotDict(preset_data)
        self.settings = settings
        self.apply_settings()

    def get_preset_suite_name(self):
        # called by self.presets_panel
        return "tartan"

    def close(self):
        self.GetTopLevelParent().Close()

    def cancel(self, event):
        if self.cancel_hook:
            self.cancel_hook()
        self.close()

    def apply(self, event):
        self.update_tartan()
        self.save_settings()
        self.close()

    def render_stitch_plan(self):
        if self.settings['output'] == 'svg':
            self.update_tartan()
            stitch_groups = self._get_svg_stitch_groups()
        else:
            self.save_settings()
            stitch_groups = []
            previous_stitch_group = None
            for element in self.elements:
                try:
                    # copy the embroidery element to drop the cache
                    stitch_groups.extend(copy(FillStitch(element)).embroider(previous_stitch_group))
                    if stitch_groups:
                        previous_stitch_group = stitch_groups[-1]
                except (SystemExit, ExitThread):
                    raise
                except InkstitchException as exc:
                    wx.CallAfter(self._show_warning, str(exc))
                except Exception:
                    wx.CallAfter(self._show_warning, format_uncaught_exception())

        if stitch_groups:
            return stitch_groups_to_stitch_plan(
                stitch_groups,
                collapse_len=self.metadata['collapse_len_mm'],
                min_stitch_len=self.metadata['min_stitch_len_mm']
            )

    def _get_svg_stitch_groups(self):
        stitch_groups = []
        previous_stitch_group = None
        for element in self.elements:
            parent = element.getparent()
            embroidery_elements = nodes_to_elements(parent.iterdescendants())
            for embroidery_element in embroidery_elements:
                check_stop_flag()
                if embroidery_element.node == element:
                    continue
                try:
                    # copy the embroidery element to drop the cache
                    stitch_groups.extend(copy(embroidery_element).embroider(previous_stitch_group))
                    if stitch_groups:
                        previous_stitch_group = stitch_groups[-1]
                except InkstitchException:
                    pass
                except Exception:
                    pass
        return stitch_groups

    def update_tartan(self):
        for element in self.elements:
            check_stop_flag()
            if self.settings['output'] == 'svg':
                TartanSvgGroup(self.settings).generate(element)
            else:
                prepare_tartan_fill_element(element)

    def on_stitch_plan_rendered(self, stitch_plan):
        self.simulator.stop()
        self.simulator.load(stitch_plan)
        self.simulator.go()
