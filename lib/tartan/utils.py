# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from collections import defaultdict
from copy import copy
from typing import List, Optional, Tuple, Union

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

    full_sett = _stripes_to_sett(stripes, symmetry, scale, min_stripe_width)

    minx, miny, maxx, maxy = dimensions
    shapes: defaultdict = defaultdict(list)

    if len(full_sett) == 0:
        return shapes

    left = minx
    top = miny
    i = -1
    while True:
        i += 1
        for stripe in full_sett:
            width = stripe['width']
            right = left + width
            bottom = top + width

            if (top > maxy and weft) or (left > maxx and not weft):
                return _merge_polygons(shapes, outline, intersect_outline)

            if stripe['color'] is None or not stripe['render']:
                left = right
                top = bottom
                continue

            shape_dimensions = [top, bottom, left, right, minx, miny, maxx, maxy]
            if stripe['is_stroke']:
                linestrings = _get_linestrings(outline, shape_dimensions, rotation, rotation_center, weft)
                shapes[stripe['color']].extend(linestrings)
            else:
                polygon = _get_polygon(shape_dimensions, rotation, rotation_center, weft)
                shapes[stripe['color']].append(polygon)
                left = right
                top = bottom


def _stripes_to_sett(
    stripes: List[dict],
    symmetry: bool,
    scale: int,
    min_stripe_width: float,
) -> List[dict]:
    """
    Builds a full sett for easier conversion into elements

    :param stripes: a list of dictionaries with stripe information
    :param symmetry: reflective sett (True) / repeating sett (False)
    :param scale: the scale value (percent) for the pattern
    :param min_stripe_width: min stripe width before it is rendered as running stitch
    :returns: a list of dictionaries with stripe information (color, width, is_stroke, render)
    """

    last_fill_color: Optional[str] = _get_last_fill_color(stripes, scale, min_stripe_width, symmetry)
    first_was_stroke = False
    last_was_stroke = False
    add_width = 0
    sett = []
    for stripe in stripes:
        width = stripe['width'] * PIXELS_PER_MM * (scale / 100)
        is_stroke = width <= min_stripe_width * PIXELS_PER_MM
        render = stripe['render']

        if render == 0:
            sett.append({'color': None, 'width': width + add_width, 'is_stroke': False, 'render': False})
            last_fill_color = None
            add_width = 0
            last_was_stroke = False
            continue

        if render == 2:
            sett.append({'color': last_fill_color, 'width': width + add_width, 'is_stroke': False, 'render': True})
            add_width = 0
            last_was_stroke = False
            continue

        if is_stroke:
            if len(sett) == 0:
                first_was_stroke = True
            width /= 2
            sett.append({'color': last_fill_color, 'width': width + add_width, 'is_stroke': False, 'render': True})
            sett.append({'color': stripe['color'], 'width': 0, 'is_stroke': True, 'render': True})
            add_width = width
            last_was_stroke = True
        else:
            sett.append({'color': stripe['color'], 'width':  width + add_width, 'is_stroke': False, 'render': True})
            last_fill_color = stripe['color']
            last_was_stroke = False

    if add_width > 0:
        sett.append({'color': last_fill_color, 'width':  add_width, 'is_stroke': False, 'render': True})

    # For symmetric setts we want to mirror the sett and append to receive a full sett
    # We do not repeat at pivot points, which means we exclude the first and the last list item from the mirror
    if symmetry:
        reversed_sett = list(reversed(sett[1:-1]))
        if first_was_stroke:
            reversed_sett = reversed_sett[:-1]
        if last_was_stroke:
            reversed_sett = reversed_sett[1:]
        sett.extend(reversed_sett)

    return sett


def _get_last_fill_color(stripes: List[dict], scale: int, min_stripe_width: float, symmetry: bool,) -> Optional[str]:
    '''
    Returns the first fill color of a pattern to substitute spaces if the pattern starts with strokes or
    stripes with render mode 2

    :param stripes: a list of dictionaries with stripe information
    :param scale: the scale value (percent) for the pattern
    :param min_stripe_width: min stripe width before it is rendered as running stitch
    :param symmetry: reflective sett (True) / repeating sett (False)
    :returns: a list with fill colors or a list with one None item if there are no fills
    '''
    fill_colors: list[Optional[str]] = []
    for stripe in stripes:
        if stripe['render'] == 0:
            fill_colors.append(None)
        elif stripe['render'] == 2:
            continue
        elif stripe['width'] * (scale / 100) > min_stripe_width:
            fill_colors.append(stripe['color'])
    if len(fill_colors) == 0:
        fill_colors = [None]

    if symmetry:
        return fill_colors[0]
    else:
        return fill_colors[-1]


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
) -> List[LineString]:
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
    if len([stripe for stripe in warp if stripe['render'] == 1]) == 0:
        warp = []
    if len([stripe for stripe in weft if stripe['render'] == 1]) == 0:
        weft = []

    if palette.equal_warp_weft:
        weft = warp
    return warp, weft
