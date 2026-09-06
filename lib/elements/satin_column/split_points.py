from typing import TYPE_CHECKING

from shapely import geometry as shgeo

from ...stitches import running_stitch

if TYPE_CHECKING:
    from .satin_column import SatinColumn


def get_split_points(satin: 'SatinColumn', a, b, a_short, b_short, length, count=None, length_sigma=0.0,
                     random_phase=False, min_split_length=None, seed=None, row_num=0, from_end=False):
    if satin.split_method == "default":
        return _get_split_points_default(satin,
            a, b, a_short, b_short, length, count, length_sigma,
            random_phase, min_split_length, seed)
    elif satin.split_method == "simple":
        return _get_split_points_simple(satin, a, b, a_short, b_short, length, row_num, from_end), None
    elif satin.split_method == "staggered":
        return _get_split_points_staggered(satin, a, b, a_short, b_short, length, row_num, from_end), None
    raise ValueError(f'Unexpected split method: {satin.split_method}')


def _get_split_points_default(satin: 'SatinColumn', a, b, a_short, b_short, length, count=None, length_sigma=0.0, random_phase=False,
                              min_split_length=None,
                              seed=None):
    if not length:
        return ([], None)
    if min_split_length is None:
        min_split_length = length
    distance = a.distance(b)
    if distance <= min_split_length:
        return ([], 1)
    if random_phase:
        points = running_stitch.split_segment_random_phase(a_short, b_short, length, length_sigma, seed)
        # avoid hard stitches: do not insert split stitches near the end points
        if len(points) > 1 and points[0].distance(shgeo.Point(a)) <= satin.min_stitch_len:
            del points[0]
        if len(points) > 1 and points[-1].distance(shgeo.Point(b)) <= satin.min_stitch_len:
            del points[-1]
        return (points, None)
    elif count is not None:
        points = running_stitch.split_segment_even_n(a, b, count, length_sigma, seed)
        return (points, count)
    else:
        points = running_stitch.split_segment_even_dist(a, b, length, length_sigma, seed)
        return (points, len(points) + 1)


def _get_split_points_simple(satin: 'SatinColumn', a, b, a_short, b_short, length, row_num=0, from_end=False):
    return _get_split_points_staggered(satin, a, b, a_short, b_short, length, row_num, from_end, 1)


def _get_split_points_staggered(satin: 'SatinColumn', a, b, a_short, b_short, length, row_num=0, from_end=False, staggers=None):
    if not length or a.distance(b) <= length:
        return []

    if staggers is None:
        # This is only here to allow _get_split_points_simple to override
        staggers = satin.split_staggers

    if from_end:
        a, b = b, a
        a_short, b_short = b_short, a_short

    line = shgeo.LineString((a, b))
    a_short_projection = line.project(shgeo.Point(a_short))
    b_short_projection = line.project(shgeo.Point(b_short))
    split_points = running_stitch.split_segment_stagger_phase(
        a, b, length,
        staggers, row_num,
        min_val=a_short_projection,
        max_val=b_short_projection)

    if from_end:
        split_points = list(reversed(split_points))

    return split_points
