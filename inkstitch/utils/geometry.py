from .. import Point as InkstitchPoint
from shapely.geometry import LineString, Point as ShapelyPoint

def cut(line, distance):
    """ Cuts a LineString in two at a distance from its starting point.

    This is an example in the Shapely documentation.
    """
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
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

    return [InkstitchPoint(*point) for point in subpath.coords]

