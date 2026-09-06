from typing import Optional, TYPE_CHECKING

from shapely import LineString
from shapely import geometry as shgeo

from ...stitch_plan import Stitch, StitchGroup
from ...stitches import running_stitch
from ...utils import Point
from .compensation import apply_push_comp, apply_push_comp_on_point_list
from .rails import plot_points_on_rails

if TYPE_CHECKING:
    from .satin_column import SatinColumn

def do_underlay_stitch_groups(satin: 'SatinColumn', top_layer: StitchGroup, end_point: Optional[Point]) -> list[StitchGroup]:
    stitch_groups: list[StitchGroup] = []
    if satin.center_walk_underlay:
        stitch_groups.extend(_do_center_walk(satin, end_point))

    if satin.contour_underlay:
        stitch_groups.extend(_do_contour_underlay(satin, top_layer, end_point))

    if satin.zigzag_underlay:
        stitch_groups.extend(_do_zigzag_underlay(satin, end_point))

    return stitch_groups

def _to_stitch_group(satin: 'SatinColumn', linestring: LineString, tags, reverse: bool = False) -> StitchGroup:
    if reverse:
        linestring = linestring.reverse()
    return StitchGroup(
        color=satin.color,
        tags=tags,
        stitches=[Stitch.from_coordinates(coord) for coord in linestring.coords]
    )

def _do_contour_underlay(satin: 'SatinColumn', top_layer: StitchGroup, end_point: Optional[Point]):
    # "contour walk" underlay: do stitches up one side and down the
    # other. if the two sides are far away, adding a running stitch to travel
    # in between avoids a long jump or a trim.

    pairs = plot_points_on_rails(
        satin,
        satin.contour_underlay_stitch_tolerance,
        -satin.contour_underlay_inset_px, -satin.contour_underlay_inset_percent/100)

    if not pairs:
        return []

    first_side = running_stitch.even_running_stitch(
        [points[0] for points in pairs],
        [satin.contour_underlay_stitch_length],
        satin.contour_underlay_stitch_tolerance
    )
    second_side = running_stitch.even_running_stitch(
        [points[1] for points in pairs],
        [satin.contour_underlay_stitch_length],
        satin.contour_underlay_stitch_tolerance
    )
    if satin.satin_method == 'zigzag':
        top_layer_stitches = top_layer.stitches

        end_first = _get_peak(top_layer_stitches[::-1], "peak_a")
        first_side = _shorten_contour_underlay_for_zigzag(first_side, end_first, cut_end=True)

        end_second = _get_peak(top_layer_stitches[::-1], "peak_b")
        second_side = _shorten_contour_underlay_for_zigzag(second_side, end_second, cut_end=True)

        start_second = _get_peak(top_layer_stitches, "peak_b")
        second_side = _shorten_contour_underlay_for_zigzag(second_side, start_second)

    first_side = apply_push_comp_on_point_list(first_side, satin.contour_underlay_inset_px[0], satin.contour_underlay_inset_px[1])
    second_side = apply_push_comp_on_point_list(second_side, satin.contour_underlay_inset_px[0], satin.contour_underlay_inset_px[1])

    if satin.center_walk_is_odd():
        first_side.reverse()
    else:
        second_side.reverse()

    if end_point:
        stitch_groups: list[StitchGroup] = []
        tags = ("satin_column", "satin_column_underlay", "satin_contour_underlay")
        first_linestring = shgeo.LineString(first_side)
        first_start, first_end = satin.split_linestring_at_end_point(first_linestring, end_point)
        second_linestring = shgeo.LineString(second_side)
        second_end, second_start = satin.split_linestring_at_end_point(second_linestring, end_point)
        stitch_groups.append(_to_stitch_group(satin, first_start, tags))
        stitch_groups.append(_to_stitch_group(satin, second_end, tags))
        stitch_groups.append(_to_stitch_group(satin, second_start, tags))
        stitch_groups.append(_to_stitch_group(satin, first_end, tags))
        return stitch_groups

    stitch_group = StitchGroup(
        color=satin.color,
        tags=("satin_column", "satin_column_underlay", "satin_contour_underlay"),
        stitches=first_side
    )

    satin.add_running_stitches(first_side[-1], second_side[0], stitch_group)
    stitch_group.stitches += second_side
    return [stitch_group]

def _get_peak(stitches: list[Stitch], peak: str) -> Stitch | None:
    for stitch in stitches:
        if peak in stitch.tags:
            return stitch
    return None

def _shorten_contour_underlay_for_zigzag(rail: list[Point], end_point: Optional[Point], cut_end: bool = False) -> list[Point]:
    if not end_point:
        return rail
    line = shgeo.LineString(rail)
    if cut_end:
        end = line.reverse().project(shgeo.Point(end_point))
        shortened_line = apply_push_comp(line, 0, end)
    else:
        start = line.project(shgeo.Point(end_point))
        shortened_line = apply_push_comp(line, start, 0)
    return [Point(*point) for point in shortened_line.coords]

def _do_center_walk(satin: 'SatinColumn', end_point: Optional[Point]):
    # Center walk underlay is just a running stitch down and back on the
    # center line between the bezier curves.
    repeats = satin.center_walk_underlay_repeats

    stitch_groups = []
    stitches = satin.get_center_line_stitches(satin.center_walk_underlay_position, satin.center_walk_underlay_stitch_length)
    if end_point:
        tags = ("satin_column", "satin_column_underlay", "satin_center_walk")
        stitches = shgeo.LineString(stitches)
        start, end = satin.split_linestring_at_end_point(stitches, end_point)
        if satin.center_walk_is_odd():
            end, start = start, end
        stitch_groups.append(_to_stitch_group(satin, start, tags))
        stitch_groups.append(_to_stitch_group(satin, end, tags, True))
    else:
        stitch_group = StitchGroup(
            color=satin.color,
            tags=("satin_column", "satin_column_underlay", "satin_center_walk"),
            stitches=stitches
        )
        stitch_groups.append(stitch_group)

    for stitch_group in stitch_groups:
        stitch_count = len(stitch_group.stitches)
        for i in range(repeats - 1):
            if i % 2 == 0:
                stitch_group.stitches += reversed(stitch_group.stitches[:stitch_count])
            else:
                stitch_group.stitches += stitch_group.stitches[:stitch_count]
    return stitch_groups

def _do_zigzag_underlay(satin: 'SatinColumn', end_point: Optional[Point]):
    # zigzag underlay, usually done at a much lower density than the
    # satin itself.  It looks like this:
    #
    # \/\/\/\/\/\/\/\/\/\/|
    # /\/\/\/\/\/\/\/\/\/\|
    #
    # In combination with the "contour walk" underlay, this is the
    # "German underlay" described here:
    #   http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/

    stitch_groups = []

    pairs = plot_points_on_rails(
        satin,
        satin.zigzag_underlay_spacing / 2.0,
        -satin.zigzag_underlay_inset_px,
        -satin.zigzag_underlay_inset_percent/100)

    if satin.center_walk_is_odd():
        pairs = list(reversed(pairs))

    # This organizes the points in each side in the order that they'll be visited.
    # take a point, from each side in turn, then go backed over the other points
    point_groups: tuple[list[Point], list[Point]] = [pair[i % 2] for i, pair in enumerate(pairs)], list(reversed([pair[i % 2] for i, pair in enumerate(pairs, 1)]))

    start_groups = []
    end_groups = []
    for points in point_groups:
        if not end_point:
            stitch_groups.append(_generate_zigzag_stitch_group(satin, points))
            continue
        if len(points) == 1:
            points.append(points[0])
        zigzag_line = shgeo.LineString(points)
        start, end = satin.split_linestring_at_end_point(zigzag_line, end_point)
        start_groups.append(_generate_zigzag_stitch_group(satin, [Stitch(*point) for point in start.coords]))
        end_groups.append(_generate_zigzag_stitch_group(satin, [Stitch(*point) for point in end.coords]))
    if start_groups:
        stitch_groups.append(satin.connect_and_add(start_groups[0], end_groups[-1]))
        stitch_groups.append(satin.connect_and_add(start_groups[-1], end_groups[0]))

    return stitch_groups

def _generate_zigzag_stitch_group(satin: 'SatinColumn', points: list[Point] | list[Stitch]) -> StitchGroup:
    max_len = satin.zigzag_underlay_max_stitch_length
    last_point = None
    stitch_group = StitchGroup(color=satin.color)
    for point in points:
        if last_point and max_len:
            if last_point.distance(point) > max_len:
                split_points = running_stitch.split_segment_even_dist(last_point, point, max_len)
                for p in split_points:
                    stitch_group.add_stitch(p, ("split_stitch",))
        last_point = point
        stitch_group.add_stitch(point, ("edge",))
    stitch_group.add_tags(("satin_column", "satin_column_underlay", "satin_zigzag_underlay"))
    return stitch_group
