# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
import typing

import numpy
from shapely.geometry import (GeometryCollection, LinearRing, LineString,
                              MultiLineString, MultiPoint, MultiPolygon)
from shapely.geometry import Point as ShapelyPoint


def cut(line, distance, normalized=False):
    """ Cuts a LineString in two at a distance from its starting point.

    This is an example in the Shapely documentation.
    """
    if normalized:
        distance *= line.length

    if distance <= 0.0:
        return [None, line]
    elif distance >= line.length:
        return [line, None]

    coords = list(ShapelyPoint(p) for p in line.coords)
    traveled = 0
    last_point = coords[0]
    for i, p in enumerate(coords[1:], 1):
        traveled += p.distance(last_point)
        last_point = p
        if traveled == distance:
            return [
                LineString(coords[:i + 1]),
                LineString(coords[i:])]
        if traveled > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]


def cut_multiple(line, distances, normalized=False):
    """Cut a LineString at multiple distances along that line.

    Always returns a list of N + 1 members, where N is the number of distances
    provided.  Some members of the list may be None, indicating an empty
    segment.  This can happen if one of the distances is at the start or end
    of the line, or if duplicate distances are provided.

    Returns:
        a list of LineStrings or None values"""

    distances = list(sorted(distances))

    segments = [line]
    distance_so_far = 0
    nones = []

    for distance in distances:
        segment = segments.pop()
        before, after = cut(segment, distance - distance_so_far, normalized)

        segments.append(before)

        if after is None:
            nones.append(after)
        else:
            if before is not None:
                distance_so_far += before.length
            segments.append(after)

    segments.extend(nones)
    return segments


def roll_linear_ring(ring, distance, normalized=False):
    """Make a linear ring start at a different point.

    Example: A B C D E F G A -> D E F G A B C

    Same linear ring, different ordering of the coordinates.
    """

    if not isinstance(ring, LinearRing):
        # In case they handed us a LineString
        ring = LinearRing(ring)

    pieces = cut(LinearRing(ring), distance, normalized=False)

    if None in pieces:
        # We cut exactly at the start or end.
        return ring

    # The first and last point in a linear ring are duplicated, so we omit one
    # copy
    return LinearRing(pieces[1].coords[:] + pieces[0].coords[1:])


def reverse_line_string(line_string):
    return LineString(line_string.coords[::-1])


def ensure_multi_line_string(thing, min_size=0):
    """Given a shapely geometry, return a MultiLineString"""
    multi_line_string = MultiLineString()
    if thing.is_empty:
        return multi_line_string
    if thing.geom_type == "MultiLineString":
        multi_line_string = thing
    elif thing.geom_type == "LineString":
        multi_line_string = MultiLineString([thing])
    elif thing.geom_type == "GeometryCollection":
        multilinestring = []
        for shape in thing.geoms:
            if shape.geom_type == "MultiLineString":
                multilinestring.extend(shape.geoms)
            elif shape.geom_type == "LineString":
                multilinestring.append(shape)
        multi_line_string = MultiLineString(multilinestring)
    if min_size > 0:
        multi_line_string = MultiLineString([line for line in multi_line_string.geoms if line.length > min_size])
    return multi_line_string


def ensure_geometry_collection(thing):
    """Given a shapely geometry, return a GeometryCollection"""
    if thing.is_empty:
        return GeometryCollection()
    if thing.geom_type == "GeometryCollection":
        return thing
    if thing.geom_type in ["MultiLineString", "MultiPolygon", "MultiPoint"]:
        return GeometryCollection(thing.geoms)
    # LineString, Polygon, Point
    return GeometryCollection([thing])


def ensure_multi_polygon(thing, min_size=0):
    """Given a shapely geometry, return a MultiPolygon"""
    multi_polygon = MultiPolygon()
    if thing.is_empty:
        return multi_polygon
    if thing.geom_type == "MultiPolygon":
        multi_polygon = thing
    elif thing.geom_type == "Polygon":
        multi_polygon = MultiPolygon([thing])
    elif thing.geom_type == "GeometryCollection":
        multipolygon = []
        for shape in thing.geoms:
            if shape.geom_type == "MultiPolygon":
                multipolygon.extend(shape.geoms)
            elif shape.geom_type == "Polygon":
                multipolygon.append(shape)
        multi_polygon = MultiPolygon(multipolygon)
    if min_size > 0:
        multi_polygon = MultiPolygon([polygon for polygon in multi_polygon.geoms if polygon.area > min_size])
    return multi_polygon


def ensure_multi_point(thing):
    """Given a shapely geometry, return a MultiPoint"""
    multi_point = MultiPoint()
    if thing.is_empty:
        return multi_point
    if thing.geom_type == "MultiPoint":
        return thing
    elif thing.geom_type == "Point":
        return MultiPoint([thing])
    elif thing.geom_type == "GeometryCollection":
        points = []
        for shape in thing.geoms:
            if shape.geom_type == "Point":
                points.append(shape)
            elif shape.geom_type == "MultiPoint":
                points.extend(shape.geoms)
        return MultiPoint(points)
    return multi_point


def cut_path(points, length):
    """Return a subsection of at the start of the path that is length units long.

    Given a path denoted by a set of points, walk along it until we've travelled
    the specified length and return a new path up to that point.

    If the original path isn't that long, just return it as is.
    """

    if len(points) < 2:
        return points

    path = LineString(points)
    subpath, rest = cut(path, length)

    return [Point(*point) for point in subpath.coords]


class Point:
    def __init__(self, x: typing.Union[float, numpy.float64], y: typing.Union[float, numpy.float64]):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_shapely_point(cls, point):
        return cls(point.x, point.y)

    @classmethod
    def from_tuple(cls, point):
        return cls(point[0], point[1])

    def __json__(self):
        return vars(self)

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def mul(self, scalar):
        return self.__class__(self.x * scalar, self.y * scalar)

    def __mul__(self, other):
        if isinstance(other, Point):
            # dot product
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return self.__class__(self.x * other, self.y * other)
        else:
            raise ValueError("cannot multiply %s by %s" % (type(self), type(other)))

    def __neg__(self):
        return self * -1

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        else:
            raise ValueError("cannot multiply %s by %s" % (type(self), type(other)))

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self * (1.0 / other)
        else:
            raise ValueError("cannot divide %s by %s" % (type(self), type(other)))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "%s(%s,%s)" % (type(self), self.x, self.y)

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def distance(self, other):
        return (other - self).length()

    def unit(self):
        length = self.length()
        return self.__class__(self.x / length, self.y / length)

    def angle(self):
        return math.atan2(self.y, self.x)

    def rotate_left(self):
        return self.__class__(-self.y, self.x)

    def rotate(self, angle):
        return self.__class__(self.x * math.cos(angle) - self.y * math.sin(angle), self.y * math.cos(angle) + self.x * math.sin(angle))

    def scale(self, x_scale, y_scale):
        return self.__class__(self.x * x_scale, self.y * y_scale)

    def as_int(self):
        return self.__class__(int(round(self.x)), int(round(self.y)))

    def as_tuple(self):
        return (self.x, self.y)

    def __getitem__(self, item):
        return self.as_tuple()[item]

    def __len__(self):
        return 2

    def __str__(self):
        return "({0:.3f}, {1:.3f})".format(self.x, self.y)


def line_string_to_point_list(line_string):
    return [Point(*point) for point in line_string.coords]


def coordinate_list_to_point_list(coordinate_list):
    return [Point.from_tuple(coords) for coords in coordinate_list]
