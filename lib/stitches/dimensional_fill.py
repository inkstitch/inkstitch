# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""3D/Dimensional fill stitch creates raised, textured effects."""

import math

from shapely.geometry import LineString, Point

from ..utils import Point as InkstitchPoint
from ..utils.geometry import ensure_multi_line_string


def dimensional_fill(shape, angle, row_spacing, max_stitch_length, starting_point=None,
                     ending_point=None, underpath=None, height_percent=100):
    """Create dimensional fill with raised effect.

    Args:
        shape: Shapely MultiPolygon to fill
        angle: Angle of fill rows in degrees
        row_spacing: Distance between rows in pixels
        max_stitch_length: Maximum length of a single stitch
        starting_point: Optional starting point
        ending_point: Optional ending point
        underpath: Optional underpath
        height_percent: Height of the 3D effect (50-200%)

    Returns:
        List of InkstitchPoint objects representing the stitches
    """

    # Convert height percent to multiplier
    height_multiplier = height_percent / 100.0

    stitches = []

    # Get bounding box
    minx, miny, maxx, maxy = shape.bounds

    # Calculate the angle in radians
    angle_rad = math.radians(angle)

    # Calculate row spacing
    row_spacing_actual = row_spacing

    # Start from one side and work across
    current_offset = 0
    row = 0

    # Direction perpendicular to rows
    perp_angle = angle_rad + math.pi / 2

    while True:
        # Calculate the line for this row
        # Start point far to the left
        start_x = minx - (maxx - minx)
        start_y = miny + current_offset

        # Rotate around center
        center_x = (minx + maxx) / 2
        center_y = (miny + maxy) / 2

        # Create row line
        line_length = math.hypot(maxx - minx, maxy - miny) * 2

        p1_x = center_x + math.cos(angle_rad) * line_length
        p1_y = center_y + math.sin(angle_rad) * line_length + current_offset

        p2_x = center_x - math.cos(angle_rad) * line_length
        p2_y = center_y - math.sin(angle_rad) * line_length + current_offset

        row_line = LineString([(p1_x, p1_y), (p2_x, p2_y)])

        # Intersect with shape
        try:
            intersection = shape.intersection(row_line)
        except Exception:
            current_offset += row_spacing_actual
            if current_offset > (maxy - miny) + row_spacing_actual * 2:
                break
            row += 1
            continue

        if intersection.is_empty:
            current_offset += row_spacing_actual
            if current_offset > (maxy - miny) + row_spacing_actual * 2:
                break
            row += 1
            continue

        # Convert intersection to line strings
        line_strings = ensure_multi_line_string(intersection)

        # Add stitches along each line segment
        for line in line_strings.geoms:
            coords = list(line.coords)
            if not coords:
                continue

            # Alternate direction for 3D effect
            if row % 2 == 1:
                coords = list(reversed(coords))

            # Add intermediate stitches for 3D effect
            for i in range(len(coords) - 1):
                x1, y1 = coords[i]
                x2, y2 = coords[i + 1]

                # Calculate segment length
                seg_length = math.hypot(x2 - x1, y2 - y1)
                num_stitches = max(2, int(seg_length / max_stitch_length) + 1)

                for j in range(num_stitches):
                    t = j / (num_stitches - 1)

                    # Linear interpolation
                    x = x1 + (x2 - x1) * t
                    y = y1 + (y2 - y1) * t

                    # Add wave effect for dimension
                    wave_offset = math.sin(t * math.pi) * row_spacing_actual * 0.3 * height_multiplier

                    # Apply offset perpendicular to stitch direction
                    x += math.cos(perp_angle) * wave_offset
                    y += math.sin(perp_angle) * wave_offset

                    stitches.append(InkstitchPoint(x, y))

        current_offset += row_spacing_actual
        row += 1

        if current_offset > (maxy - miny) + row_spacing_actual * 2:
            break

    return stitches
