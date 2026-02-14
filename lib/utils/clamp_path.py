from shapely.errors import GEOSException
from shapely.geometry import LineString, MultiPolygon
from shapely.geometry import Point as ShapelyPoint
from shapely.ops import nearest_points
from shapely.prepared import prep

from .geometry import (Point, ensure_geometry_collection,
                       ensure_multi_line_string)


def path_to_segments(path):
    """Convert a path of Points into a list of segments as LineStrings"""
    for start, end in zip(path[:-1], path[1:]):
        yield LineString((start, end))


def segments_to_path(segments):
    """Convert a list of contiguous LineStrings into a list of Points."""
    if not segments:
        return []

    coords = [segments[0].coords[0]]

    for segment in segments:
        coords.extend(segment.coords[1:])

    return [Point(x, y) for x, y in coords]


def fix_starting_point(border_pieces):
    """Reconnect the starting point of a polygon border's pieces.

    When splitting a polygon border with two lines, we want to get two
    pieces.  However, that's not quite how Shapely works.  The outline
    of the polygon is a LinearRing that starts and ends at the same place,
    but Shapely still knows where that starting point is and splits there
    too.

    We don't want that third piece, so we'll reconnect the segments that
    touch the starting point.
    """

    if len(border_pieces) == 3:
        # Fortunately, Shapely keeps the starting point of the LinearRing
        # as the starting point of the first segment.  That means it's also
        # the ending point of the last segment.  Reconnecting is super simple:
        return [border_pieces[1],
                LineString(border_pieces[2].coords[:] + border_pieces[0].coords[1:])]
    else:
        # We probably cut exactly at the starting point.
        return border_pieces


def adjust_line_end(line, end):
    """Reverse line if necessary to ensure that it ends near end."""

    line_start = ShapelyPoint(*line.coords[0])
    line_end = ShapelyPoint(*line.coords[-1])

    if line_end.distance(end) < line_start.distance(end):
        return line
    else:
        return LineString(line.coords[::-1])


def find_border(polygon, point):
    """Finds subpath of polygon which intersects with the point.
       Ignores small border fragments"""
    for border in polygon.interiors:
        if border.length > 0.1 and border.intersects(point):
            return border
    else:
        return polygon.exterior


def clamp_fully_external_path(path, polygon):
    """Clamp a path that lies entirely outside a polygon."""

    start = ShapelyPoint(path[0])
    end = ShapelyPoint(path[-1])

    start_on_outline = nearest_points(start, polygon.exterior)[1].buffer(0.01, quad_segs=1)
    end_on_outline = nearest_points(end, polygon.exterior)[1].buffer(0.01, quad_segs=1)

    border_pieces = ensure_multi_line_string(polygon.exterior.difference(MultiPolygon((start_on_outline, end_on_outline)))).geoms
    border_pieces = fix_starting_point(border_pieces)
    shorter = min(border_pieces, key=lambda piece: piece.length)

    return adjust_line_end(shorter, start)


def clamp_path_to_polygon(path, polygon, check_distance=True):
    """Constrain a path to a Polygon.

    The path is expected to have at least some part inside the Polygon.

    Description: https://gis.stackexchange.com/questions/428848/clamp-linestring-to-polygon
    """

    start = path[0]
    end = path[-1]

    # This splits the path at the points where it intersects with the polygon
    # border and returns the pieces in the same order as the original path.
    try:
        split_path = ensure_geometry_collection(LineString(path).difference(polygon.boundary))
    except FloatingPointError:
        return path

    # contains() checks can fail without the buffer.
    try:
        buffered_polygon = prep(polygon.buffer(1e-9))
    except GEOSException:
        # Buffering seems to fail when coordinate values are very high (shape is way off from the canvas)
        # However, the output results seem to be better, when we do not try to continue clamping
        # For an example fle see issue https://github.com/inkstitch/inkstitch/issues/4219
        return path

    if len(split_path.geoms) == 1 and buffered_polygon.contains(split_path.geoms[0]):
        # The path never intersects with the polygon, so it's entirely inside.
        return path

    # Add the start and end points to avoid losing part of the path if the
    # start or end coincides with the polygon boundary
    split_path = [ShapelyPoint(start), *split_path.geoms, ShapelyPoint(end)]

    clamped_path = _clamp_path(split_path, buffered_polygon, polygon, check_distance)

    if not clamped_path:
        return clamp_fully_external_path(path, polygon)

    return segments_to_path(clamped_path)


def _clamp_path(split_path, buffered_polygon, polygon, check_distance):
    last_point_inside = None
    was_inside = False
    result = []

    for segment in split_path:
        if buffered_polygon.contains(segment):
            start = ShapelyPoint(segment.coords[0])

            # The first part of this or condition checks whether we traveled
            # outside the shape for a while.
            #
            # The second part of this or condition checks whether part of the
            # path was removed by difference() above, because it coincided
            # with part of the shape border.
            if last_point_inside is not None and (
                not was_inside or
                (check_distance and last_point_inside.distance(start) > 0.01)
            ):
                # We traveled outside or on the border of the shape for
                # a while.  In either case, we need to add a path along the
                # border between the exiting and entering points.

                # First, find the two points.  Buffer them just a bit to
                # ensure intersection with the border.
                exit_point = last_point_inside.buffer(0.01, quad_segs=1)
                entry_point = ShapelyPoint(segment.coords[0]).buffer(0.01, quad_segs=1)

                if not exit_point.intersects(entry_point):
                    # Now break the border into pieces using those points.
                    border = find_border(polygon, exit_point)
                    border_pieces = ensure_multi_line_string(border.difference(MultiPolygon((entry_point, exit_point)))).geoms
                    border_pieces = fix_starting_point(border_pieces)

                    # Pick the shortest way to get from the exiting to the
                    # entering point along the border.
                    shorter = min(border_pieces, key=lambda piece: piece.length)

                    # We don't know which direction the polygon border
                    # piece should be.  adjust_line_end() will figure
                    # that out.
                    result.append(adjust_line_end(shorter, entry_point))

            result.append(segment)
            was_inside = True
            last_point_inside = ShapelyPoint(segment.coords[-1])
        else:
            was_inside = False

    return result
