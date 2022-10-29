from typing import List, Tuple

from lib.types import GratingSegments
from lib.utils.geometry import Point


def as_point_list(grating_segments: GratingSegments) -> List[Tuple[Point, Point]]:
    point_list: List[Tuple[Point, Point]] = []

    for grating_segment in grating_segments:
        # for some reason the segment is a list with one entry?
        grating_segment = grating_segment[0]
        start, end = grating_segment
        point_list.append((Point.from_tuple(start), Point.from_tuple(end)))

    return point_list
