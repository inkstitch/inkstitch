import numpy as np
from scipy.interpolate import splprep, splev

from .geometry import Point, coordinate_list_to_point_list
from ..stitches.running_stitch import running_stitch


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


def smooth_path(path, smoothness=1.0):
    """Smooth a path of coordinates.

    Arguments:
        path -- an iterable of coordinate tuples or Points
        smoothness -- float, how much smoothing to apply.  Bigger numbers
            smooth more.

    Returns:
        A list of Points.
    """
    from ..debug import debug

    if smoothness == 0:
        # s of exactly zero seems to indicate a default level of smoothing
        # in splprep, so we'll just exit instead.
        return path

    # Smoothing seems to look nicer if the line segments in the path are mostly
    # similar in length.  If we have some especially long segments, then the
    # smoothed path sometimes diverges more from the original path as the
    # spline curve struggles to fit the path.  This can be especially bad at
    # the start and end.
    #
    # Fortunately, we can convert the path to segments that are mostly the same
    # length by using the running stitch algorithm.
    path = running_stitch(coordinate_list_to_point_list(path), 5 * smoothness, smoothness / 2)

    # splprep blows up on duplicated consecutive points with "Invalid inputs"
    coords = _remove_duplicate_coordinates(np.array(path))
    num_points = len(coords)

    if num_points <= 3:
        # splprep throws an error unless num_points > k
        return path

    # s is explained in this issue: https://github.com/scipy/scipy/issues/11916
    # the smoothness parameter limits how much the smoothed path can deviate
    # from the original path.  The standard deviation of the distance between
    # the smoothed path and the original path is equal to the smoothness.
    # In practical terms, if smoothness is 1mm, then the smoothed path can be
    # up to 1mm away from the original path.
    s = num_points * (smoothness ** 2)

    # .T transposes the array (for some reason splprep expects
    # [[x1, x2, ...], [y1, y2, ...]]
    tck, fp, ier, msg = splprep(coords.T, s=s, k=3, nest=-1, full_output=1)
    if ier > 0:
        debug.log(f"error {ier} smoothing path: {msg}")
        return path

    # Evaluate the spline curve at many points along its length to produce the
    # smoothed point list.  2 * num_points seems to be a good number, but it
    # does produce a lot of points.
    smoothed_x_values, smoothed_y_values = splev(np.linspace(0, 1, int(num_points * 2)), tck[0])
    coords = np.array([smoothed_x_values, smoothed_y_values]).T

    return [Point(x, y) for x, y in coords]
