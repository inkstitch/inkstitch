# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import numpy as np
from shapely.geometry import LineString, Point


def apply_stitches(
        line: LineString,
        max_stitch_length: list[float],
        num_staggers: int,
        row_spacing: float,
        row_num: int,
        threshold: float | None = None) -> LineString:
    stitch_length = max_stitch_length[0]
    if num_staggers == 0:
        num_staggers = 1  # sanity check to avoid division by zero.
    start = ((row_num / num_staggers) % 1) * stitch_length
    projections = [0] + np.arange(start, line.length, stitch_length)
    points = np.array([line.interpolate(projection).coords[0] for projection in projections])

    if len(points) < 2:
        coords = line.coords
        points = np.array([coords[0], coords[-1]])

    stitched_line = LineString(points)

    # stitched_line may round corners, which will look terrible.  This finds the
    # corners.
    if not threshold:
        threshold = row_spacing / 2.0
    simplified_line = line.simplify(threshold, preserve_topology=False)
    simplified_points = [Point(x, y) for x, y in simplified_line.coords]

    extra_points = []
    extra_point_projections = []
    for point in simplified_points:
        if point.distance(stitched_line) > threshold:
            extra_points.append(point.coords[0])
            extra_point_projections.append(line.project(point))

    # Now we need to insert the new points into their correct spots in the line.
    indices = np.searchsorted(projections, extra_point_projections)
    if len(indices) > 0:
        points = np.insert(points, indices, extra_points, axis=0)

    return LineString(points)
