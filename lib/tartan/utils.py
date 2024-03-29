# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from collections import defaultdict
from copy import copy
from typing import List, Tuple, Union

from inkex import BaseElement
from shapely import LineString, MultiPolygon, Point, Polygon, unary_union
from shapely.affinity import rotate

from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSTITCH_TARTAN
from ..utils import ensure_multi_line_string, ensure_multi_polygon
from .palette import Palette


def stripes_to_shapes(
    stripes: List[dict],
    dimensions: Tuple[float, float, float, float],
    outline: Union[MultiPolygon, Polygon],
    rotation: float,
    rotation_center: Point,
    symmetry: bool,
    scale: int,
    min_stripe_width: float,
    weft: bool = False,
    intersect_outline: bool = True
) -> defaultdict:
    """
    Convert tartan stripes to polygons and linestrings (depending on stripe width) sorted by color

    :param stripes: a list of dictionaries with stripe information
    :param dimensions: the dimension to fill with the tartan pattern (minx, miny, maxx, maxy)
    :param outline: the shape to fill with the tartan pattern
    :param rotation: the angle to rotate the pattern
    :param rotation_center: the center point for rotation
    :param symmetry: reflective sett (True) / repeating sett (False)
    :param scale: the scale value (percent) for the pattern
    :param min_stripe_width: min stripe width before it is rendered as running stitch
    :param weft: wether to render warp or weft oriented stripes
    :param intersect_outline: wether or not cut the shapes to fit into the outline
    :returns: a dictionary with shapes grouped by color
    """

    minx, miny, maxx, maxy = dimensions
    shapes: defaultdict = defaultdict(list)

    original_stripes = stripes
    if len(original_stripes) == 0:
        return shapes

    left = minx
    top = miny
    i = -1
    while True:
        i += 1
        stripes = original_stripes

        segments = stripes
        if symmetry and i % 2 != 0 and len(stripes) > 1:
            segments = list(reversed(stripes[1:-1]))
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

            shape_dimensions = [top, bottom, left, right, minx, miny, maxx, maxy]
            if width <= min_stripe_width * PIXELS_PER_MM:
                linestrings = _get_linestrings(outline, shape_dimensions, rotation, rotation_center, weft)
                shapes[stripe['color']].extend(linestrings)
                continue

            polygon = _get_polygon(shape_dimensions, rotation, rotation_center, weft)
            shapes[stripe['color']].append(polygon)
            left = right
            top = bottom


def _merge_polygons(
    shapes: defaultdict,
    outline: Union[MultiPolygon, Polygon],
    intersect_outline: bool = True
) -> defaultdict:
    """
    Merge polygons which are bordering each other (they most probably used a running stitch in between)

    :param shapes: shapes grouped by color
    :param outline: the shape to be filled with a tartan pattern
    :intersect_outline: wether to return an intersection of the shapes with the outline or not
    :returns: the shapes with merged polygons
    """
    shapes_copy = copy(shapes)
    for color, shape_group in shapes_copy.items():
        polygons: List[Polygon] = []
        lines: List[LineString] = []
        for shape in shape_group:
            if not shape.intersects(outline):
                continue
            if shape.geom_type == "Polygon":
                polygons.append(shape)
            else:
                lines.append(shape)
        merged_polygons = unary_union(polygons)
        merged_polygons = merged_polygons.simplify(0.01)
        if intersect_outline:
            merged_polygons = merged_polygons.intersection(outline)
        merged_polygons = ensure_multi_polygon(merged_polygons)
        shapes[color] = [list(merged_polygons.geoms), lines]
    return shapes


def _get_polygon(dimensions: List[float], rotation: float, rotation_center: Point, weft: bool) -> Polygon:
    """
    Generates a rotated polygon with the given dimensions

    :param dimensions: top, bottom, left, right, minx, miny, maxx, maxy
    :param rotation: the angle to rotate the pattern
    :param rotation_center: the center point for rotation
    :param weft: wether to render warp or weft oriented stripes
    :returns: the generated Polygon
    """
    top, bottom, left, right, minx, miny, maxx, maxy = dimensions
    if not weft:
        polygon = Polygon([(left, miny), (right, miny), (right, maxy), (left, maxy)])
    else:
        polygon = Polygon([(minx, top), (maxx, top), (maxx, bottom), (minx, bottom)])
    if rotation != 0:
        polygon = rotate(polygon, rotation, rotation_center)
    return polygon


def _get_linestrings(
    outline: Union[MultiPolygon, Polygon],
    dimensions: List[float],
    rotation: float,
    rotation_center: Point, weft: bool
) -> list:
    """
    Generates a rotated linestrings with the given dimension (outline intersection)

    :param outline: the outline to be filled with the tartan pattern
    :param dimensions: top, bottom, left, right, minx, miny, maxx, maxy
    :param rotation: the angle to rotate the pattern
    :param rotation_center: the center point for rotation
    :param weft: wether to render warp or weft oriented stripes
    :returns: a list of the generated linestrings
    """
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


def sort_fills_and_strokes(fills: defaultdict, strokes: defaultdict) -> Tuple[defaultdict, defaultdict]:
    """
    Lines should be stitched out last, so they won't be covered by following fill elements.
    However, if we find lines of the same color as one of the polygon groups, we can make
    sure that they stitch next to each other to reduce color changes by at least one.

    :param fills: fills grouped by color
    :param strokes: strokes grouped by color
    :returns: the sorted fills and strokes
    """
    colors_to_connect = [color for color in fills.keys() if color in strokes]
    if colors_to_connect:
        color_to_connect = colors_to_connect[-1]

        last = fills[color_to_connect]
        fills.pop(color_to_connect)
        fills[color_to_connect] = last

        sorted_strokes = defaultdict(list)
        sorted_strokes[color_to_connect] = strokes[color_to_connect]
        strokes.pop(color_to_connect)
        sorted_strokes.update(strokes)
        strokes = sorted_strokes

    return fills, strokes


def get_tartan_settings(node: BaseElement) -> dict:
    """
    Parse tartan settings from node inkstich:tartan attribute

    :param node: the tartan svg element
    :returns: the tartan settings in a dictionary
    """
    settings = node.get(INKSTITCH_TARTAN, None)
    if settings is None:
        settings = {
            'palette': '(#101010)/5.0 (#FFFFFF)/?5.0',
            'rotate': 0.0,
            'offset_x': 0.0,
            'offset_y': 0.0,
            'symmetry': True,
            'scale': 100,
            'min_stripe_width': 1.0
        }
        return settings
    return json.loads(settings)


def get_palette_width(settings: dict, direction: int = 0) -> float:
    """
    Calculate the width of all stripes (with a minimum width) in given direction

    :param settings: tartan settings
    :param direction: [0] warp [1] weft
    :returns: the calculated palette width
    """
    palette_code = settings['palette']
    palette = Palette()
    palette.update_from_code(palette_code)
    return palette.get_palette_width(settings['scale'], settings['min_stripe_width'], direction)


def get_tartan_stripes(settings: dict) -> Tuple[list, list]:
    """
    Get tartan stripes

    :param settings: tartan settings
    :returns: a list with warp stripe dictionaries and a list with weft stripe dictionaries
        Lists are empty if total width is 0 (for example if there are only strokes)
    """
    # get stripes, return empty lists if total width is 0
    palette_code = settings['palette']
    palette = Palette()
    palette.update_from_code(palette_code)
    warp, weft = palette.palette_stripes

    if palette.get_palette_width(settings['scale'], settings['min_stripe_width']) == 0:
        warp = []
    if palette.get_palette_width(settings['scale'], settings['min_stripe_width'], 1) == 0:
        weft = []
    if len([stripe for stripe in warp if stripe['render'] is True]) == 0:
        warp = []
    if len([stripe for stripe in weft if stripe['render'] is True]) == 0:
        weft = []

    if palette.equal_warp_weft:
        weft = warp
    return warp, weft
