# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..elements import FillStitch, SatinColumn, Stroke
from ..gui.test_swatches import GenerateSwatchesApp
from ..i18n import _
from ..utils.param import ParamOption
from .base import InkstitchExtension


class TestSwatches(InkstitchExtension):
    '''
    This generates swatches from selection by altering one param each time.
    '''

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            errormsg(_("Please select one or more elements."))
            return

        choices = []

        fill_added = False
        stroke_added = False
        satin_added = False

        for element in self.elements:
            if not fill_added and isinstance(element, FillStitch):
                choices.extend(fill_choices)
                fill_added = True
            elif not satin_added and isinstance(element, SatinColumn):
                choices.extend(satin_choices)
                satin_added = True
            elif not stroke_added and isinstance(element, Stroke):
                choices.extend(stroke_choices)
                stroke_added = True

        app = GenerateSwatchesApp(self, choices)
        app.MainLoop()


stroke_choices = [
    ParamOption("running_stitch_tolerance_mm", "Running Stitch Tolerance mm"),
    ParamOption("repeats", "Repeats"),
    ParamOption("running_stitch_length_mm", "Running Stitch Length mm"),
    ParamOption("bean_stitch_repeats", "Bean Stitch Repeats (Bean Stitch)"),
    ParamOption("exponent", "Exponent (Ripple)"),
    ParamOption("grid_size_mm", "Grid Size mm (Ripple)"),
    ParamOption("line_count", "Line Count (Ripple)"),
    ParamOption("min_line_dist_mm", "Minimum Line Distanse mm (Ripple)"),
    ParamOption("scale_end", "Scale End (Ripple)"),
    ParamOption("scale_start", "Scale Start (Ripple)"),
    ParamOption("skip_end", "Skip End (Ripple)"),
    ParamOption("skip_start", "Skip Start (Ripple)"),
    ParamOption("max_stitch_length_mm", "Maximum Stitch Length mm (Manual Stitch)"),
    ParamOption("pull_compensation_mm", "Pull Compensation mm (ZigZag)"),
    ParamOption("zigzag_spacing_mm", "Zigzag Spacing mm (Satin, Zigzag)")
]

fill_choices = [
    ParamOption("running_stitch_length_mm", "Running Stitch Length mm"),
    ParamOption("running_stitch_tolerance_mm", "Running Stitch Tolerance mm"),
    ParamOption("max_stitch_length_mm", "Maximum Stitch Length mm (Auto Fill, Contour Fill, Guided Fill"),
    ParamOption("angle", "Angle (Auto Fill)"),
    ParamOption("row_spacing_mm", "Row Spacing mm"),
    ParamOption("end_row_spacing_mm", "End Row Spacing mm"),
    ParamOption("expand_mm", "Expand mm"),
    ParamOption("repeats", "Repeats (Circular Fill, Meander Fill)"),
    ParamOption("bean_stitch_repeats", "Bean Stitch Repeats (Circular Fill, Meander Fill)"),
    ParamOption("meander_angle", "Meander Pattern: Angle (Meander Fill)"),
    ParamOption("meander_scale_percent", "Meander Pattern: Scale Percent (Meander Fill)"),
    ParamOption("smoothness_mm", "Smoothness mm (Contour Fill, Meander Fill)"),
    ParamOption("staggers", "Staggers (Auto Fill, Fuided Fill"),
    ParamOption("fill_underlay_angle", "Fill Underlay: Angle"),
    ParamOption("fill_underlay_inset_mm", "Fill Underlay: Inset mm"),
    ParamOption("fill_underlay_max_stitch_length_mm", "Fill Underlay: Maximum Stitch Length mm"),
    ParamOption("fill_underlay_row_spacing_mm", "Fill Underlay: Row Spacing mm")
]

satin_choices = [
    ParamOption("zigzag_spacing_mm", "Zigzag Spacing mm"),
    ParamOption("random_zigzag_spacing_percent", "Random Zigzag Spacing percent"),
    ParamOption("pull_compensation_mm", "Pull Compensation mm"),
    ParamOption("pull_compensation_percent", "Pull Compensation percent"),
    ParamOption("random_width_decrease_percent", "Random Width Decrease percent"),
    ParamOption("random_width_increase_percent", "Random width Increase percent"),
    ParamOption("short_stitch_inset", "Short Stitch: Inset"),
    ParamOption("max_stitch_length_mm", "Maximum Stitch Length mm"),
    ParamOption("split_staggers", "Split Staggers"),
    ParamOption("short_stitch_distance_mm", "Short Stitch: Distance mm"),
    ParamOption("min_random_split_length_mm", "Minimum Random Split Length mm"),
    ParamOption("random_split_jitter_percent", "Random Split Jitter percent"),
    ParamOption("center_walk_underlay_position", "Center Walk Underlay: Position"),
    ParamOption("center_walk_underlay_repeats", "Center Walk Underlay: Repeats"),
    ParamOption("center_walk_underlay_stitch_length_mm", "center Walk Underlay: Stitch Length mm"),
    ParamOption("contour_underlay_inset_mm", "Contour Underlay: Inset mm"),
    ParamOption("contour_underlay_inset_percent", "Contour Underlay: Inset percent"),
    ParamOption("contour_underlay_stitch_length_mm", "Contour Underlay: Stitch Length mm"),
    ParamOption("zigzag_underlay_inset_mm", "Zigzag Underlay: Inset_mm"),
    ParamOption("zigzag_underlay_inset_percent", "Zigzag Underlay: Inset percent"),
    ParamOption("zigzag_underlay_max_stitch_length_mm", "ZigZag Underlay: Maximum Stitch Length mm"),
    ParamOption("zigzag_underlay_spacing_mm", "Zigzag Underlay: Spacing mm")
]
