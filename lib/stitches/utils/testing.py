from typing import List, Tuple

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
