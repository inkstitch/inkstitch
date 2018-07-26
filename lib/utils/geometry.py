from shapely.geometry import LineString, Point as ShapelyPoint
import math


def cut(line, distance):
    """ Cuts a LineString in two at a distance from its starting point.

    This is an example in the Shapely documentation.
    """
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line), None]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        # TODO: I think this doesn't work if the path doubles back on itself
        pd = line.project(ShapelyPoint(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]


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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def mul(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __mul__(self, other):
        if isinstance(other, Point):
            # dot product
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        else:
            raise ValueError("cannot multiply Point by %s" % type(other))

    def __neg__(self):
        return self * -1

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        else:
            raise ValueError("cannot multiply Point by %s" % type(other))

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return self * (1.0 / other)
        else:
            raise ValueErorr("cannot divide Point by %s" % type(other))

    def __repr__(self):
        return "Point(%s,%s)" % (self.x, self.y)

    def length(self):
        return math.sqrt(math.pow(self.x, 2.0) + math.pow(self.y, 2.0))

    def unit(self):
        return self.mul(1.0 / self.length())

    def rotate_left(self):
        return Point(-self.y, self.x)

    def rotate(self, angle):
        return Point(self.x * math.cos(angle) - self.y * math.sin(angle), self.y * math.cos(angle) + self.x * math.sin(angle))

    def as_int(self):
        return Point(int(round(self.x)), int(round(self.y)))

    def as_tuple(self):
        return (self.x, self.y)

    def __cmp__(self, other):
        return cmp(self.as_tuple(), other.as_tuple())

    def __getitem__(self, item):
        return self.as_tuple()[item]

    def __len__(self):
        return 2
