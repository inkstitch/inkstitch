# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx
from ...stitch_plan import StitchPlan

from ...i18n import _


class DesignInfoDialog(wx.Dialog):
    """A dialog to show design info
    """

    def __init__(self, parent: wx.Window, stitch_plan: StitchPlan | None) -> None:
        super(DesignInfoDialog, self).__init__(parent, title=_('Design Info'))
        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        info_sizer = wx.FlexGridSizer(6, 2, 5, 5)

        dimensions_label = wx.StaticText(self, label=_("Design dimensions (mm)"))
        self.dimensions = wx.StaticText(self)

        num_stitches_label = wx.StaticText(self, label=_('# Stitches'))
        self.num_stitches = wx.StaticText(self)

        num_color_changes_label = wx.StaticText(self, label=_("# Color Changes"))
        self.num_color_changes = wx.StaticText(self)

        num_jumps_label = wx.StaticText(self, label=_("# Jumps"))
        self.num_jumps = wx.StaticText(self)

        num_trims_label = wx.StaticText(self, label=_("# Trims"))
        self.num_trims = wx.StaticText(self)

        num_stops_label = wx.StaticText(self, label=_("# Stops"))
        self.num_stops = wx.StaticText(self)

        info_sizer.Add(dimensions_label, 0, wx.ALL, 10)
        info_sizer.Add(self.dimensions, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(num_stitches_label, 0, wx.ALL, 10)
        info_sizer.Add(self.num_stitches, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(num_color_changes_label, 0, wx.ALL, 10)
        info_sizer.Add(self.num_color_changes, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(num_jumps_label, 0, wx.ALL, 10)
        info_sizer.Add(self.num_jumps, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(num_trims_label, 0, wx.ALL, 10)
        info_sizer.Add(self.num_trims, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(num_stops_label, 0, wx.ALL, 10)
        info_sizer.Add(self.num_stops, 0, wx.EXPAND | wx.ALL, 10)

        sizer.Add(info_sizer, 1, wx.ALL, 10)
        self.SetSizerAndFit(sizer)
        self.load(stitch_plan)

    def load(self, stitch_plan: StitchPlan | None) -> None:
        if stitch_plan is None:
            for label in [self.dimensions, self.num_stitches, self.num_color_changes, self.num_jumps, self.num_trims, self.num_stops]:
                label.SetLabel("")
            return

        self.dimensions.SetLabel("{:.2f} x {:.2f}".format(*stitch_plan.dimensions_mm))
        self.num_stitches.SetLabel(f"{stitch_plan.num_stitches}")
        self.num_color_changes.SetLabel(f"{stitch_plan.num_color_blocks-1}")
        self.num_jumps.SetLabel(f"{stitch_plan.num_jumps-1}")
        self.num_trims.SetLabel(f"{stitch_plan.num_trims}")
        self.num_stops.SetLabel(f"{stitch_plan.num_stops}")
        self.Fit()
