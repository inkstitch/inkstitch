from shapely import geometry as shgeo

from lib.stitches import fill
from lib.stitches.utils import testing
from lib.utils.geometry import Point


def test_intersect_region_with_grating_convex():
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
        [(Point(20, 11), Point(10, 11))],
        [(Point(20, 12), Point(10, 12))],
        [(Point(20, 13), Point(10, 13))],
        [(Point(20, 14), Point(10, 14))],
        [(Point(20, 15), Point(10, 15))],
        [(Point(20, 16), Point(10, 16))],
        [(Point(20, 17), Point(10, 17))],
        [(Point(20, 18), Point(10, 18))],
        [(Point(20, 19), Point(10, 19))],
        [(Point(20, 20), Point(10, 20))],
    ]

    assert len(actual) == len(expected)
    testing.assert_close(expected, actual)


def test_intersect_region_with_grating_H_shape():
    # an H shape with side length 10 and lower-left corner at (10, 10)
    left_side = shgeo.box(10, 10, 12, 20, ccw=True)
    right_side = shgeo.box(18, 10, 20, 20, ccw=True)
    belt = shgeo.box(10, 14, 20, 16, ccw=True)
    shape = left_side.union(right_side).union(belt)
    angle = 0
    row_spacing = 1

    actual = fill.intersect_region_with_grating(
        shape=shape,
        angle=angle,
        row_spacing=row_spacing,
    )
    actual = testing.as_point_list(actual)

    expected = [
        [(Point(12, 11), Point(10, 11)), (Point(20, 11), Point(18, 11))],
        [(Point(12, 12), Point(10, 12)), (Point(20, 12), Point(18, 12))],
        [(Point(12, 13), Point(10, 13)), (Point(20, 13), Point(18, 13))],
        [(Point(12, 14), Point(10, 14)), (Point(20, 14), Point(18, 14))],
        # these two rows are in the "belt", and so their intersection with
        # the region is a single connected segment.
        [(Point(20, 15), Point(10, 15))],
        [(Point(20, 16), Point(10, 16))],
        [(Point(12, 17), Point(10, 17)), (Point(20, 17), Point(18, 17))],
        [(Point(12, 18), Point(10, 18)), (Point(20, 18), Point(18, 18))],
        [(Point(12, 19), Point(10, 19)), (Point(20, 19), Point(18, 19))],
        [(Point(12, 20), Point(10, 20)), (Point(20, 20), Point(18, 20))],
    ]

    assert len(actual) == len(expected)
    testing.assert_close(expected, actual)
