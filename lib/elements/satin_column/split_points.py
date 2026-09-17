from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from shapely import geometry as shgeo

from ...stitches import running_stitch
from ...utils import Point

if TYPE_CHECKING:
    from .satin_column import SatinColumn


@dataclass(frozen=True)
class SplitPointsOptions:
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
    options = SplitPointsOptions(
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
        return _get_split_points_default(options)
    elif satin.split_method == "simple":
        return _get_split_points_simple(options), None
    elif satin.split_method == "staggered":
        return _get_split_points_staggered(options), None
    raise ValueError(f'Unexpected split method: {satin.split_method}')


def _get_split_points_default(options: SplitPointsOptions) -> tuple[list[Point], int | None]:
    if not options.length:
        return ([], None)

    if options.min_split_length is None:
        options = replace(options, min_split_length=options.length)

    distance = options.a.distance(options.b)

    if distance <= options.min_split_length:
        return ([], 1)

    if options.random_phase:
        points = running_stitch.split_segment_random_phase(options.a_short, options.b_short, options.length, options.length_sigma, options.seed)
        # avoid hard stitches: do not insert split stitches near the end points
        if len(points) > 1 and points[0].distance(options.a) <= options.satin.min_stitch_len:
            del points[0]
        if len(points) > 1 and points[-1].distance(options.b) <= options.satin.min_stitch_len:
            del points[-1]
        return (points, None)
    elif options.count is not None:
        points = running_stitch.split_segment_even_n(options.a, options.b, options.count, options.length_sigma, options.seed)
        return (points, options.count)
    else:
        points = running_stitch.split_segment_even_dist(options.a, options.b, options.length, options.length_sigma, options.seed)
        return (points, len(points) + 1)


def _get_split_points_simple(options: SplitPointsOptions) -> list[Point]:
    return _get_split_points_staggered(options, staggers=1)


def _get_split_points_staggered(options: SplitPointsOptions, staggers: int | None = None) -> list[Point]:
    if not options.length or options.a.distance(options.b) <= options.length:
        return []

    if staggers is None:
        # This is only here to allow _get_split_points_simple to override
        staggers = options.satin.split_staggers

    if options.from_end:
        options = replace(options,
                         a=options.b,
                         b=options.a,
                         a_short=options.b_short,
                         b_short=options.a_short)

    line = shgeo.LineString((options.a, options.b))
    a_short_projection = line.project(shgeo.Point(options.a_short))
    b_short_projection = line.project(shgeo.Point(options.b_short))
    split_points = running_stitch.split_segment_stagger_phase(
        options.a, options.b, options.length,
        staggers, options.row_num,
        min_val=a_short_projection,
        max_val=b_short_projection)

    if options.from_end:
        split_points = list(reversed(split_points))

    return split_points
