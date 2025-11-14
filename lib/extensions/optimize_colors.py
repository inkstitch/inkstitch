# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean

from ..elements import nodes_to_elements
from ..i18n import _
from ..stitch_plan import stitch_groups_to_stitch_plan
from .base import InkstitchExtension


class OptimizeColors(InkstitchExtension):
    """Intelligently reorder stitch groups to minimize thread changes.

    This extension analyzes the design and reorders elements to group
    same-color stitches together, reducing the number of thread changes
    needed during embroidery.
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--strategy", type=str, default="greedy",
                                     help="Optimization strategy: greedy or spatial")
        self.arg_parser.add_argument("--max_jump_mm", type=float, default=50.0,
                                     help="Maximum jump stitch length (mm)")

    def effect(self):
        if not self.get_elements():
            return

        # Get stitch groups from elements
        stitch_groups = self.elements_to_stitch_groups(self.elements)

        if not stitch_groups:
            self.errormsg(_("No stitchable elements found"))
            return

        # Optimize color order
        if self.options.strategy == "greedy":
            optimized_groups = self._greedy_optimize(stitch_groups)
        else:
            optimized_groups = self._spatial_optimize(stitch_groups, self.options.max_jump_mm)

        # Calculate improvement
        original_changes = self._count_color_changes(stitch_groups)
        optimized_changes = self._count_color_changes(optimized_groups)

        # Reorder elements in SVG
        self._reorder_elements(optimized_groups)

        # Show results
        self.msg(_(f"Color optimization complete!\n"
                   f"Original thread changes: {original_changes}\n"
                   f"Optimized thread changes: {optimized_changes}\n"
                   f"Improvement: {original_changes - optimized_changes} fewer changes"))

    def _greedy_optimize(self, stitch_groups):
        """Greedy algorithm: group consecutive same-color stitches."""
        # Group by color while maintaining relative order when possible
        color_groups = {}
        for group in stitch_groups:
            color = group.color
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(group)

        # Rebuild stitch groups by color
        optimized = []
        for color in color_groups:
            optimized.extend(color_groups[color])

        return optimized

    def _spatial_optimize(self, stitch_groups, max_jump_mm):
        """Spatial optimization: minimize both color changes and jump stitches."""
        from ..svg import PIXELS_PER_MM

        max_jump = max_jump_mm * PIXELS_PER_MM

        # Group by color
        by_color = {}
        for group in stitch_groups:
            color = group.color
            if color not in by_color:
                by_color[color] = []
            by_color[color].append(group)

        # Start with the first group
        optimized = []
        remaining = list(stitch_groups)
        current = remaining.pop(0)
        optimized.append(current)

        while remaining:
            # Find best next group (prefer same color, then closest)
            best_group = None
            best_score = float('inf')

            current_end = current.stitches[-1] if current.stitches else None

            for group in remaining:
                # Score based on color change (0 if same, 1 if different)
                color_penalty = 0 if group.color == current.color else 1000

                # Score based on distance
                if current_end and group.stitches:
                    distance = (group.stitches[0] - current_end).length()
                    distance_penalty = min(distance, max_jump)
                else:
                    distance_penalty = 0

                score = color_penalty + distance_penalty

                if score < best_score:
                    best_score = score
                    best_group = group

            if best_group:
                optimized.append(best_group)
                remaining.remove(best_group)
                current = best_group

        return optimized

    def _count_color_changes(self, stitch_groups):
        """Count the number of thread color changes."""
        if not stitch_groups:
            return 0

        changes = 0
        prev_color = None

        for group in stitch_groups:
            if prev_color is not None and group.color != prev_color:
                changes += 1
            prev_color = group.color

        return changes

    def _reorder_elements(self, optimized_groups):
        """Reorder SVG elements to match optimized stitch group order."""
        # Create mapping from stitch group to element
        group_to_element = {}
        for element in self.elements:
            element_groups = element.embroider(None, None)
            for group in element_groups:
                group_to_element[id(group)] = element

        # Get parent layer
        if not self.elements:
            return

        parent = self.elements[0].node.getparent()

        # Reorder nodes
        seen_elements = set()
        for group in optimized_groups:
            element = group_to_element.get(id(group))
            if element and element.node not in seen_elements:
                # Move element to end (maintains order)
                parent.append(element.node)
                seen_elements.add(element.node)
