# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ...i18n import _


class DesignInfoDialog(wx.Dialog):
    """A dialog to show design info
    """

    def __init__(self, *args, **kwargs):
        super(DesignInfoDialog, self).__init__(*args, **kwargs)
        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.view_panel = self.GetParent()
        self.drawing_panel = self.view_panel.drawing_panel

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
        self.update()

    def update(self):
        if not self.drawing_panel.loaded:
            return
        self.dimensions.SetLabel("{:.2f} x {:.2f}".format(self.drawing_panel.dimensions_mm[0], self.drawing_panel.dimensions_mm[1]))
        self.num_stitches.SetLabel(f"{self.drawing_panel.num_stitches}")
        self.num_color_changes.SetLabel(f"{self.drawing_panel.num_color_changes}")
        self.num_jumps.SetLabel(f"{self.drawing_panel.num_jumps}")
        self.num_trims.SetLabel(f"{self.drawing_panel.num_trims}")
        self.num_stops.SetLabel(f"{self.drawing_panel.num_stops}")
        self.Fit()
