from shapely import geometry as shgeo

from lib.stitches import fill
from lib.stitches.utils import testing
from lib.utils.geometry import Point


TOL = 1e-08


def test_intserect_region_with_grating():
    # a box with side length 10 and lower-left corner at (10, 10)
    shape = shgeo.box(10, 10, 20, 20, ccw=True)
    angle = 0
    row_spacing = 1

    actual = fill.intersect_region_with_grating(
        shape=shape,
        angle=angle,
        row_spacing=row_spacing,
    )
    actual = testing.as_point_list(actual)

    # The grating segments produced as output start from the
    # bottom of the box, and are oriented from right to left.
    # The very bottom edge is not included as a stitch.
    expected = [
        (Point(20, 11), Point(10, 11)),
        (Point(20, 12), Point(10, 12)),
        (Point(20, 13), Point(10, 13)),
        (Point(20, 14), Point(10, 14)),
        (Point(20, 15), Point(10, 15)),
        (Point(20, 16), Point(10, 16)),
        (Point(20, 17), Point(10, 17)),
        (Point(20, 18), Point(10, 18)),
        (Point(20, 19), Point(10, 19)),
        (Point(20, 20), Point(10, 20)),
    ]

    assert len(actual) == len(expected)
    for (expected_seg, actual_seg) in zip(expected, actual):
        assert len(actual_seg) == 2
        expected_start, expected_end = expected_seg
        actual_start, actual_end = actual_seg
        assert expected_start.isclose(actual_start, rel_tol=TOL)
        assert expected_end.isclose(actual_end, rel_tol=TOL)
