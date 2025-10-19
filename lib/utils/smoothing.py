import numpy as np

from ..stitches.running_stitch import stitch_curve_evenly
from .geometry import Point, coordinate_list_to_point_list


def _remove_duplicate_coordinates(coords_array):
    """Remove consecutive duplicate points from an array.

    Arguments:
        coords_array -- numpy.array

    Returns:
        a numpy.array of coordinates, minus consecutive duplicates
    """

    differences = np.diff(coords_array, axis=0)
    zero_differences = np.isclose(differences, 0)
    keepers = np.r_[True, np.any(zero_differences == False, axis=1)]  # noqa: E712

    return coords_array[keepers]


def smooth_path(path, smoothness=1.0, iterations=5):
    """Smooth a path of coordinates.

    Arguments:
        path -- an iterable of coordinate tuples or Points
        smoothness -- float, how much smoothing to apply.  Bigger numbers
            smooth more.

    Returns:
        A list of Points.
    """
    points = coordinate_list_to_point_list(path)
    if smoothness == 0:
        return points

    # Smoothing seems to look nicer if the line segments in the path are mostly
    # similar in length.  If we have some especially long segments, then the
    # smoothed path sometimes diverges more from the original path as the
    # spline curve struggles to fit the path.  This can be especially bad at
    # the start and end.
    #
    # Fortunately, we can convert the path to segments that are mostly the same
    # length by using the running stitch algorithm.
    points, _ = stitch_curve_evenly(points, [smoothness * 5], smoothness * 2)
    points = np.array(points)
    for _ in range(iterations):
        ll = points.repeat(2, axis=0)
        r = np.empty_like(ll)
        if len(r) == 0:
            continue
        r[0] = ll[0]
        r[2::2] = ll[1:-1:2]
        r[1:-1:2] = ll[2::2]
        r[-1] = ll[-1]
        points = ll * 0.75 + r * 0.25

    # we want to keep the old start and end points
    start = [Point(* path[0])]
    end = [Point(* path[-1])]

    return start + [Point(*coord) for coord in points] + end
