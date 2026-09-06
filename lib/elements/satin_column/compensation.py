from typing import Sequence

from shapely import affinity as shaffinity
from shapely import geometry as shgeo
from shapely.ops import substring

from ...utils import Point


def _extend_line(linestring: shgeo.LineString, value: float, at_end: bool = False) -> shgeo.LineString:
    """Extends either the first or the last segment of the given line by given value.
    """
    if at_end:
        linestring = linestring.reverse()
    coords = list(linestring.coords)
    start_segment = shgeo.LineString([coords[0], coords[1]])
    line_length = start_segment.length
    target_length = line_length - value
    scale_factor = target_length / line_length
    extended_segment = shaffinity.scale(start_segment, xfact=scale_factor, yfact=scale_factor,
                                        origin=shgeo.Point(coords[1]))
    first = list(extended_segment.coords)[0]
    extended_line = shgeo.LineString([first] + coords)
    if at_end:
        extended_line = extended_line.reverse()
    return extended_line

def get_compensated_line_string_rails(line_string_rails: Sequence[shgeo.LineString], start: float, end: float) -> list[shgeo.Point | shgeo.LineString]:
    """Apply push compensation on rails"""
    return [apply_push_comp(rail, start, end) for rail in line_string_rails]


def apply_push_comp_on_point_list(rail: list[Point], start: float, end: float):
    line = shgeo.LineString(rail)
    return [Point(*point) for point in apply_push_comp(line, start, end).coords]


def apply_push_comp(linestring: shgeo.LineString, start: float, end: float) -> shgeo.Point | shgeo.LineString:
    if start < 0:
        linestring = _extend_line(linestring, start)
        start = 0
    if end < 0:
        linestring = _extend_line(linestring, end, True)
        end = 0
    if not start and not end:
        return linestring
    if end == 0:
        end = 0.00000001
    if start + end >= linestring.length - 0.5:
        return linestring
    return substring(linestring, start, -end)
