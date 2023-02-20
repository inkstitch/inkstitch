# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely import geometry as shgeo

from .marker import get_marker_elements
from .stitch_plan import Stitch
from .utils import Point


def get_patterns_cache_key_data(node):
    patterns = get_marker_elements(node, "pattern")
    data = []
    data.extend([fill.wkt for fill in patterns['fill']])
    data.extend([stroke.wkt for stroke in patterns['stroke']])

    return data


def apply_patterns(stitch_groups, node):
    patterns = get_marker_elements(node, "pattern")
    _apply_fill_patterns(patterns['fill'], stitch_groups)
    _apply_stroke_patterns(patterns['stroke'], stitch_groups)


def _apply_stroke_patterns(patterns, stitch_groups):
    for pattern in patterns:
        for stitch_group in stitch_groups:
            stitch_group_points = []
            for i, stitch in enumerate(stitch_group.stitches):
                stitch_group_points.append(stitch)
                if i == len(stitch_group.stitches) - 1:
                    continue
                intersection_points = _get_pattern_points(stitch, stitch_group.stitches[i + 1], pattern)
                for point in intersection_points:
                    stitch_group_points.append(Stitch(point, tags=('pattern_point',)))
            stitch_group.stitches = stitch_group_points


def _apply_fill_patterns(patterns, stitch_groups):
    for pattern in patterns:
        for stitch_group in stitch_groups:
            stitch_group_points = []
            for i, stitch in enumerate(stitch_group.stitches):
                if not shgeo.Point(stitch).within(pattern):
                    # keep points outside the fill pattern
                    stitch_group_points.append(stitch)
                elif i - 1 < 0 or i >= len(stitch_group.stitches) - 1:
                    # keep start and end points
                    stitch_group_points.append(stitch)
                elif stitch.has_tag('fill_row_start') or stitch.has_tag('fill_row_end'):
                    # keep points if they are the start or end of a fill stitch row
                    stitch_group_points.append(stitch)
                elif stitch.has_tag('auto_fill') and not stitch.has_tag('auto_fill_top'):
                    # keep auto-fill underlay
                    stitch_group_points.append(stitch)
                elif stitch.has_tag('auto_fill_travel'):
                    # keep travel stitches (underpath or travel around the border)
                    stitch_group_points.append(stitch)
                elif stitch.has_tag('satin_column') and not stitch.has_tag('satin_split_stitch'):
                    # keep satin column stitches unless they are split stitches
                    stitch_group_points.append(stitch)
            stitch_group.stitches = stitch_group_points


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
