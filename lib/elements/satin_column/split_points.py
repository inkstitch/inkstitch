from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shapely import geometry as shgeo

from ...stitches import running_stitch
from ...utils import Point

if TYPE_CHECKING:
    from .satin_column import SatinColumn


@dataclass
class SplitPointParams:
    satin: SatinColumn
    a: Point
    b: Point
    a_short: Point
    b_short: Point
    length: float | None = None
    count: int | None = None
    length_sigma: float = 0.0
    random_phase: bool = False
    min_split_length: float | None = None
    seed: str | None = None
    row_num: int = 0
    from_end: bool = False


def get_split_points(satin: 'SatinColumn',
                     a: Point,
                     b: Point,
                     a_short: Point,
                     b_short: Point,
                     length: float | None,
                     count: int | None = None,
                     length_sigma: float = 0.0,
                     random_phase: bool = False,
                     min_split_length: float | None = None,
                     seed: str | None = None,
                     row_num: int = 0,
                     from_end: bool = False) -> tuple[list[Point], int | None]:
    # todo: have callers pass this instead of constructing here
    params = SplitPointParams(
        satin,
        a,
        b,
        a_short,
        b_short,
        length,
        count,
        length_sigma,
        random_phase,
        min_split_length,
        seed,
        row_num,
        from_end
    )
    if satin.split_method == "default":
        return _get_split_points_default(params)
    elif satin.split_method == "simple":
        return _get_split_points_simple(params), None
    elif satin.split_method == "staggered":
        return _get_split_points_staggered(params), None
    raise ValueError(f'Unexpected split method: {satin.split_method}')


def _get_split_points_default(params: SplitPointParams) -> tuple[list[Point], int | None]:
    if not params.length:
        return ([], None)
    if params.min_split_length is None:
        params.min_split_length = params.length
    distance = params.a.distance(params.b)
    if distance <= params.min_split_length:
        return ([], 1)
    if params.random_phase:
        points = running_stitch.split_segment_random_phase(params.a_short, params.b_short, params.length, params.length_sigma, params.seed)
        # avoid hard stitches: do not insert split stitches near the end points
        if len(points) > 1 and points[0].distance(params.a) <= params.satin.min_stitch_len:
            del points[0]
        if len(points) > 1 and points[-1].distance(params.b) <= params.satin.min_stitch_len:
            del points[-1]
        return (points, None)
    elif params.count is not None:
        points = running_stitch.split_segment_even_n(params.a, params.b, params.count, params.length_sigma, params.seed)
        return (points, params.count)
    else:
        points = running_stitch.split_segment_even_dist(params.a, params.b, params.length, params.length_sigma, params.seed)
        return (points, len(points) + 1)


def _get_split_points_simple(params: SplitPointParams) -> list[Point]:
    return _get_split_points_staggered(params, staggers=1)


def _get_split_points_staggered(params: SplitPointParams, staggers: int | None = None) -> list[Point]:
    if not params.length or params.a.distance(params.b) <= params.length:
        return []

    if staggers is None:
        # This is only here to allow _get_split_points_simple to override
        staggers = params.satin.split_staggers

    if params.from_end:
        params.a, params.b = params.b, params.a
        params.a_short, params.b_short = params.b_short, params.a_short

    line = shgeo.LineString((params.a, params.b))
    a_short_projection = line.project(shgeo.Point(params.a_short))
    b_short_projection = line.project(shgeo.Point(params.b_short))
    split_points = running_stitch.split_segment_stagger_phase(
        params.a, params.b, params.length,
        staggers, params.row_num,
        min_val=a_short_projection,
        max_val=b_short_projection)

    if params.from_end:
        split_points = list(reversed(split_points))

    return split_points
