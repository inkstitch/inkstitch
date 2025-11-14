# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean

from ..elements import FillStitch
from ..i18n import _
from .base import InkstitchExtension


class DimensionalEffect(InkstitchExtension):
    """Apply 3D/dimensional effects to fill stitches.

    This extension modifies fill patterns to create raised, textured effects
    by adjusting stitch density and adding wave patterns.
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--height_percent", type=float, default=150.0,
                                     help="Height of 3D effect (50-200%)")
        self.arg_parser.add_argument("--wave_frequency", type=float, default=3.0,
                                     help="Wave frequency for texture")

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            self.no_elements_error()
            return

        fill_elements = [elem for elem in self.elements if isinstance(elem, FillStitch)]

        if not fill_elements:
            self.errormsg(_("Please select at least one fill object to apply dimensional effect."))
            return

        for fill_element in fill_elements:
            self._apply_dimensional_effect(fill_element)

        self.msg(_(f"Applied dimensional effect to {len(fill_elements)} fill(s)"))

    def _apply_dimensional_effect(self, fill_element):
        """Apply dimensional effect to a fill element."""
        node = fill_element.node

        # Adjust parameters for dimensional effect
        # Increase row spacing for raised appearance
        current_spacing = fill_element.get_float_param('row_spacing_mm', 0.4)
        new_spacing = current_spacing * (self.options.height_percent / 100.0)

        # Set ripple effect parameters
        node.set('inkstitch:row_spacing_mm', str(new_spacing))

        # Add underlay for dimension
        node.set('inkstitch:auto_fill_underlay', 'true')
        node.set('inkstitch:auto_fill_underlay_angle', str(90))  # Perpendicular underlay

        # Adjust max stitch length for texture
        node.set('inkstitch:max_stitch_length_mm', str(3.0 / (self.options.wave_frequency / 3.0)))

        # Add note to node label
        current_label = node.get('inkscape:label', '')
        if '(3D)' not in current_label:
            node.set('inkscape:label', f"{current_label} (3D)".strip())
