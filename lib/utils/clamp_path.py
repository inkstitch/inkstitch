from shapely.geometry import LineString, Point as ShapelyPoint, MultiPolygon
from shapely.prepared import prep
from .geometry import Point, ensure_multi_line_string


def path_to_segments(path):
    """Convert a path of Points into a list of segments as LineStrings"""
    for start, end in zip(path[:-1], path[1:]):
        yield LineString((start, end))


def segments_to_path(segments):
    """Convert a list of contiguous LineStrings into a list of Points."""
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
    for border in polygon.interiors:
        if border.intersects(point):
            return border
    else:
        return polygon.exterior


def clamp_path_to_polygon(path, polygon):
    """Constrain a path to a Polygon.

    Description: https://gis.stackexchange.com/questions/428848/clamp-linestring-to-polygon
    """

    path = LineString(path)

    # This splits the path at the points where it intersects with the polygon
    # border and returns the pieces in the same order as the original path.
    split_path = ensure_multi_line_string(path.difference(polygon.boundary))

    # contains() checks can fail without this.
    buffered_polygon = prep(polygon.buffer(1e-9))

    last_segment_inside = None
    was_inside = False
    result = []

    for segment in split_path.geoms:
        if buffered_polygon.contains(segment):
            if not was_inside:
                if last_segment_inside is not None:
                    # The path crossed out of the polygon, and now it's crossed
                    # back in.  We need to add a path along the border between
                    # the exiting and entering points.

                    # First, find the two points.  Buffer them just a bit to
                    # ensure intersection with the border.
                    x, y = last_segment_inside.coords[-1]
                    exit_point = ShapelyPoint(x, y).buffer(0.01, resolution=1)
                    x, y = segment.coords[0]
                    entry_point = ShapelyPoint(x, y).buffer(0.01, resolution=1)

                    if not exit_point.intersects(entry_point):
                        # Now break the border into pieces using those points.
                        border = find_border(polygon, exit_point)
                        border_pieces = border.difference(MultiPolygon((entry_point, exit_point)))
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
            last_segment_inside = segment
        else:
            was_inside = False

    return segments_to_path(result)
