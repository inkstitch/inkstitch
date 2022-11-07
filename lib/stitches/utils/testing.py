from typing import List, Tuple, Any
from collections.abc import Iterable

from lib.types import RowSegments
from lib.utils.geometry import Point


def as_point_list(rows: List[RowSegments]) -> List[List[Tuple[Point, Point]]]:
    point_list: List[List[Tuple[Point, Point]]] = []

    for row_segments in rows:
        converted_segments: List[Tuple[Point, Point]] = []
        for segment in row_segments:
            start, end = segment
            converted_segments.append((Point.from_tuple(start), Point.from_tuple(end)))
        point_list.append(converted_segments)

    return point_list


def assert_close(expected: Any, actual: Any) -> None:
    """
    Assert two arbitrarily-nested Iterables of Points are identical in
    structure and close in value.
    """
    if isinstance(expected, Iterable):
        assert isinstance(actual, Iterable)
        expected_list = list(iter(expected))
        actual_list = list(iter(actual))
        assert len(expected_list) == len(actual_list)
        for (expected_value, actual_value) in zip(expected_list, actual_list):
            assert_close(expected_value, actual_value)
    elif isinstance(expected, Point):
        assert isinstance(actual, Point)
        assert expected.isclose(actual)
    else:
        assert False, f"Arguments had unknown types {type(expected)}, {type(actual)}"
