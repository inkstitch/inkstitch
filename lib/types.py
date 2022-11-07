from typing import List, Iterable

try:
    from typing import TypeAlias  # type: ignore
except ImportError:
    # for Python < 3.10
    from typing_extensions import TypeAlias  # type: ignore

import shapely

"""The datatype representing a connected 2D shape in the plane."""
Shape = shapely.geometry.Polygon

"""A segment is a sequence of two coordinates representing the start and end of
the segment."""
Segment: TypeAlias = shapely.coords.CoordinateSequence

"""A list of possibly disconnected segments on the same row."""
RowSegments = List[Segment]

"""A type that is like a point."""
PointLike = Iterable[int]
