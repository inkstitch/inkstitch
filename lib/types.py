from typing import List
import shapely

"""The datatype representing a 2D shape in the plane."""
Shape = shapely.geometry.MultiPolygon

GratingSegments = List[List[shapely.coords.CoordinateSequence]]
