# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from shapely import geometry as shgeo

from .svg import apply_transforms
from .svg.tags import EMBROIDERABLE_TAGS
from .utils import Point


def is_pattern(node):
    if node.tag not in EMBROIDERABLE_TAGS:
        return False
    return "marker-start:url(#inkstitch-pattern-marker)" in node.get('style', '')


def apply_patterns(patches, node):
    patterns = _get_patterns(node)
    if not patterns:
        return patches

    patch_points = []
    for patch in patches:
        for i, stitch in enumerate(patch.stitches):
            patch_points.append(stitch)
            if i == len(patch.stitches) - 1:
                continue
            intersection_points = _get_pattern_points(stitch, patch.stitches[i+1], patterns)
            for point in intersection_points:
                patch_points.append(point)
    patch.stitches = patch_points


def _get_patterns(node):
    xpath = "./parent::svg:g/*[contains(@style, 'marker-start:url(#inkstitch-pattern-marker)')]"
    patterns = node.xpath(xpath, namespaces=inkex.NSS)
    line_strings = []
    for pattern in patterns:
        if pattern.tag not in EMBROIDERABLE_TAGS:
            continue
        d = pattern.get_path()
        path = inkex.paths.Path(d).to_superpath()
        path = apply_transforms(path, pattern)
        inkex.bezier.cspsubdiv(path, 0.1)
        path = [[point for control_before, point, control_after in subpath] for subpath in path]
        lines = [shgeo.LineString(p) for p in path]
        for line in lines:
            line_strings.append(line)
    return shgeo.MultiLineString(line_strings)


def _get_pattern_points(first, second, patterns):
    points = []
    for pattern in patterns:
        intersection = shgeo.LineString([first, second]).intersection(pattern)
        if isinstance(intersection, shgeo.Point):
            points.append(Point(intersection.x, intersection.y))
        if isinstance(intersection, shgeo.MultiPoint):
            for point in intersection:
                points.append(Point(point.x, point.y))
    # sort points after their distance to left
    points.sort(key=lambda point: point.distance(first))
    return points
