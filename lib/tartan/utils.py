# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from collections import defaultdict
from copy import copy

from shapely import LineString, Polygon, unary_union
from shapely.affinity import rotate

from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSTITCH_TARTAN
from ..utils import ensure_multi_line_string, ensure_multi_polygon
from .pallet import Pallet


def stripes_to_shapes(stripes, dimensions, outline, rotation, rotation_center, symmetry, scale, min_stripe_width, weft=False, intersect_outline=True):
    ''' Converts tartan stripes to polygons and linestrings (depending on stripe width) sorted by color '''

    minx, miny, maxx, maxy = dimensions
    shapes = defaultdict(list)

    original_stripes = stripes
    if len(original_stripes) == 0:
        return []

    left = minx
    top = miny
    i = -1
    while True:
        i += 1
        stripes = original_stripes

        segments = stripes
        if symmetry and i % 2 != 0 and len(stripes) > 1:
            segments = reversed(stripes[1:-1])
        for stripe in segments:
            width = stripe['width'] * PIXELS_PER_MM * (scale / 100)
            right = left + width
            bottom = top + width

            if (top > maxy and weft) or (left > maxx and not weft):
                return _merge_polygons(shapes, outline, intersect_outline)

            if not stripe['render']:
                left = right
                top = bottom
                continue

            dimensions = (top, bottom, left, right, minx, miny, maxx, maxy)
            if width <= min_stripe_width * PIXELS_PER_MM:
                linestrings = _get_linestrings(outline, dimensions, rotation, rotation_center, weft)
                shapes[stripe['color']].extend(linestrings)
                continue

            polygon = _get_polygon(dimensions, rotation, rotation_center, weft)
            shapes[stripe['color']].append(polygon)
            left = right
            top = bottom


def _merge_polygons(shapes, outline, intersect_outline=True):
    shapes_copy = copy(shapes)
    for color, shape_group in shapes_copy.items():
        polygons = []
        lines = []
        for shape in shape_group:
            if not shape.intersects(outline):
                continue
            if shape.geom_type == "Polygon":
                polygons.append(shape)
            else:
                lines.append(shape)
        polygons = unary_union(polygons)
        polygons = polygons.simplify(0.01)
        if intersect_outline:
            polygons = polygons.intersection(outline)
        polygons = ensure_multi_polygon(polygons)
        shapes[color] = [list(polygons.geoms), lines]
    return shapes


def _get_polygon(dimensions, rotation, rotation_center, weft):
    top, bottom, left, right, minx, miny, maxx, maxy = dimensions
    if not weft:
        polygon = Polygon([(left, miny), (right, miny), (right, maxy), (left, maxy)])
    else:
        polygon = Polygon([(minx, top), (maxx, top), (maxx, bottom), (minx, bottom)])
    if rotation != 0:
        polygon = rotate(polygon, rotation, rotation_center)
    return polygon


def _get_linestrings(outline, dimensions, rotation, rotation_center, weft):
    top, bottom, left, right, minx, miny, maxx, maxy = dimensions
    linestrings = []
    if weft:
        linestring = LineString([(minx, top), (maxx, top)])
    else:
        linestring = LineString([(left, miny), (left, maxy)])
    if rotation != 0:
        linestring = rotate(linestring, rotation, rotation_center)
    intersection = linestring.intersection(outline)
    if not intersection.is_empty:
        linestrings.extend(ensure_multi_line_string(intersection).geoms)
    return linestrings


def sort_fills_and_strokes(fills, strokes):
    # Lines should be stitched out last, so they won't be covered by following fill elements.
    # However, if we find lines of the same color as one of the polygon groups, we can make
    # sure that they stitch next to each other to reduce color changes by at least one
    color_to_connect = filter(lambda color: color in fills, strokes)
    color_to_connect = next(color_to_connect, None)
    if color_to_connect is not None:
        last = fills[color_to_connect]
        fills.pop(color_to_connect)
        fills[color_to_connect] = last

        sorted_strokes = defaultdict(list)
        sorted_strokes[color_to_connect] = strokes[color_to_connect]
        strokes.pop(color_to_connect)
        sorted_strokes.update(strokes)
        strokes = sorted_strokes

    return fills, strokes


def get_tartan_settings(node):
    settings = node.get(INKSTITCH_TARTAN, None)
    if settings is None:
        settings = {
            'pallet': '(#101010)/5.0 (#FFFFFF)/?5.0',
            'rotate': 0,
            'offset_x': 0,
            'offset_y': 0,
            'symmetry': True,
            'scale': 100,
            'min_stripe_width': 1
        }
        return settings
    return json.loads(settings)


def get_pallet_width(settings, direction=0):
    pallet_code = settings['pallet']
    pallet = Pallet()
    pallet.update_from_code(pallet_code)
    return pallet.get_pallet_width(settings['scale'], settings['min_stripe_width'], direction)


def get_tartan_stripes(settings):
    # get stripes, return empty lists if total width is 0
    pallet_code = settings['pallet']
    pallet = Pallet()
    pallet.update_from_code(pallet_code)
    warp, weft = pallet.pallet_stripes

    if pallet.get_pallet_width(settings['scale'], settings['min_stripe_width']) == 0:
        warp = []
    if pallet.get_pallet_width(settings['scale'], settings['min_stripe_width'], 1) == 0:
        weft = []
    if len([stripe for stripe in warp if stripe['render'] is True]) == 0:
        warp = []
    if len([stripe for stripe in weft if stripe['render'] is True]) == 0:
        weft = []

    if pallet.equal_warp_weft:
        weft = warp
    return warp, weft
