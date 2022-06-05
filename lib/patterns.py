# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely import geometry as shgeo

from .marker import get_marker_elements
from .stitch_plan import Stitch
from .utils import Point


def apply_patterns(patches, node):
    patterns = get_marker_elements(node, "pattern")
    _apply_fill_patterns(patterns['fill'], patches)
    _apply_stroke_patterns(patterns['stroke'], patches)


def _apply_stroke_patterns(patterns, patches):
    for pattern in patterns:
        for patch in patches:
            patch_points = []
            for i, stitch in enumerate(patch.stitches):
                patch_points.append(stitch)
                if i == len(patch.stitches) - 1:
                    continue
                intersection_points = _get_pattern_points(stitch, patch.stitches[i+1], pattern)
                for point in intersection_points:
                    patch_points.append(Stitch(point, tags=('pattern_point',)))
            patch.stitches = patch_points


def _apply_fill_patterns(patterns, patches):
    for pattern in patterns:
        for patch in patches:
            patch_points = []
            for i, stitch in enumerate(patch.stitches):
                if not shgeo.Point(stitch).within(pattern):
                    # keep points outside the fill pattern
                    patch_points.append(stitch)
                elif i - 1 < 0 or i >= len(patch.stitches) - 1:
                    # keep start and end points
                    patch_points.append(stitch)
                elif stitch.has_tag('fill_row_start') or stitch.has_tag('fill_row_end'):
                    # keep points if they are the start or end of a fill stitch row
                    patch_points.append(stitch)
                elif stitch.has_tag('auto_fill') and not stitch.has_tag('auto_fill_top'):
                    # keep auto-fill underlay
                    patch_points.append(stitch)
                elif stitch.has_tag('auto_fill_travel'):
                    # keep travel stitches (underpath or travel around the border)
                    patch_points.append(stitch)
                elif stitch.has_tag('satin_column') and not stitch.has_tag('satin_split_stitch'):
                    # keep satin column stitches unless they are split stitches
                    patch_points.append(stitch)
            patch.stitches = patch_points


def _get_pattern_points(first, second, pattern):
    points = []
    intersection = shgeo.LineString([first, second]).intersection(pattern)
    if isinstance(intersection, shgeo.Point):
        points.append(Point(intersection.x, intersection.y))
    if isinstance(intersection, shgeo.MultiPoint):
        for point in intersection.geoms:
            points.append(Point(point.x, point.y))
    # sort points after their distance to first
    points.sort(key=lambda point: point.distance(first))
    return points
