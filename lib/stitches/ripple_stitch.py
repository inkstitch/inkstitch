from collections import defaultdict

from shapely.geometry import LineString, Point

from ..utils.geometry import line_string_to_point_list
from .running_stitch import running_stitch


def ripple_stitch(lines, target, line_count, points, max_stitch_length, repeats):
    '''
    Ripple stitch is allowed to cross itself and doesn't care about an equal distance of lines
    It is meant to be used with light (not dense) stitching
    It will ignore holes in a closed shape. Closed shapes will be filled with a spiral
    Open shapes will be stitched back and forth.
    If there is only one (open) line or a closed shape the target point will be used.
    If more sublines are present interpolation will take place between the first two.
    '''

    # sort geoms by size
    lines = sorted(lines.geoms, key=lambda linestring: linestring.length, reverse=True)
    outline = lines[0]

    if is_closed(outline):
        rippled_line = do_circular_ripple(outline, target, line_count, repeats)
    else:
        rippled_line = do_linear_ripple(lines, points, target, line_count - 1, repeats)

    return running_stitch(line_string_to_point_list(rippled_line), max_stitch_length)


def do_circular_ripple(outline, target, line_count, repeats):
    # for each point generate a line going to the target point
    lines = target_point_lines(outline, target)

    # create a list of points for each line
    points = get_interpolation_points(lines, line_count, "circular")

    # connect the lines to a spiral towards the target
    coords = []
    for i in range(line_count):
        for j in range(len(points)):
            coords.append(Point(points[j][i].x, points[j][i].y))

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def do_linear_ripple(lines, points, target, line_count, repeats):
    if len(lines) == 1:
        lines = target_point_lines(lines[0], target)
    else:
        lines = []
        for start, end in zip(points[0], points[1]):
            lines.append(LineString([start, end]))

    # get linear points along the lines
    points = get_interpolation_points(lines, line_count)

    # go back and forth along the lines - flip direction of every second line
    coords = []
    for i in range(line_count):
        for j in range(len(lines)):
            k = j
            if i % 2 != 0:
                k = len(lines) - j - 1
            coords.append(Point(points[k][i].x, points[k][i].y))

    # add last line
    if line_count % 2 != 0:
        lines = reversed(lines)
    for line in lines:
        coords.append(line.coords[-1])

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def line_length(line):
    return line.length


def is_closed(line):
    coords = line.coords
    return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05


def target_point_lines(outline, target):
    lines = []
    for point in outline.coords:
        lines.append(LineString([point, target]))
    return lines


def get_interpolation_points(lines, line_count, method="linear"):
    new_points = defaultdict(list)
    count = len(lines)
    for i, line in enumerate(lines):
        segment_length = line.length / line_count
        distance = 0
        points = []
        for j in range(line_count):
            if distance == 0 and method == "circular":
                # the first line makes sure, it is going to be a spiral
                distance = segment_length - (segment_length * ((count - i) / count))
                if distance == 0:
                    distance = 0.0001
            elif distance == 0:
                # first line along the outline
                distance = 0.0001
            else:
                distance += segment_length
            points.append(line.interpolate(distance))
        new_points[i] = points
    return new_points


def repeat_coords(coords, repeats):
    final_coords = []
    for i in range(repeats):
        if i % 2 == 1:
            # reverse every other pass
            this_coords = coords[::-1]
        else:
            this_coords = coords[:]

        final_coords.extend(this_coords)
    return final_coords
