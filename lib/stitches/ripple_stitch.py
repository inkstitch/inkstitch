from collections import defaultdict

from shapely.geometry import LineString, Point
from shapely.ops import substring

from ..utils.geometry import line_string_to_point_list
from .running_stitch import running_stitch


def ripple_stitch(lines, target, line_count, points, max_stitch_length, repeats, flip, skip_start, skip_end, render_grid, exponent, guide_line):
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

    # ignore skip_start and skip_end if both toghether are greater or equal to line_count
    if skip_start + skip_end >= line_count:
        skip_start = skip_end = 0

    if is_closed(outline):
        rippled_line = do_circular_ripple(outline, target, line_count, repeats, flip, max_stitch_length, skip_start, skip_end, exponent, guide_line)
    else:
        rippled_line = do_linear_ripple(lines, points, target, line_count - 1, repeats, flip, max_stitch_length,
                                        skip_start, skip_end, render_grid, exponent, guide_line)

    return running_stitch(line_string_to_point_list(rippled_line), max_stitch_length)


def do_circular_ripple(outline, target, line_count, repeats, flip, max_stitch_length, skip_start, skip_end, exponent, guide_line):
    if guide_line:
        # for each point generate a line going along and pointing to the guide line
        lines = guided_helper_lines(outline, flip, max_stitch_length, guide_line.geoms[0])
    else:
        # for each point generate a line going to the target point
        lines = target_point_lines_normalized_distances(outline, target, flip, max_stitch_length)

    # create a list of points for each line
    points = get_interpolation_points(lines, line_count, exponent, "circular")

    # connect the lines to a spiral towards the target
    coords = []
    for i in range(skip_start, line_count - skip_end):
        for j in range(len(lines)):
            coords.append(Point(points[j][i].x, points[j][i].y))

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def do_linear_ripple(lines, points, target, line_count, repeats, flip, max_stitch_length, skip_start, skip_end, render_grid, exponent, guide_line):
    if len(lines) == 1:
        if guide_line:
            helper_lines = guided_helper_lines(lines[0], flip, max_stitch_length, guide_line.geoms[0])
        else:
            helper_lines = target_point_lines(lines[0], target, flip)
    else:
        helper_lines = []
        for start, end in zip(points[0], points[1]):
            if flip:
                helper_lines.append(LineString([end, start]))
            else:
                helper_lines.append(LineString([start, end]))

    # get linear points along the lines
    points = get_interpolation_points(helper_lines, line_count, exponent)

    # go back and forth along the lines - flip direction of every second line
    coords = []
    for i in range(skip_start, len(points[0]) - skip_end):
        for j in range(len(helper_lines)):
            k = j
            if i % 2 != 0:
                k = len(helper_lines) - j - 1
            coords.append(Point(points[k][i].x, points[k][i].y))

    # add helper lines as a grid
    # for now only add this to satin type ripples, otherwise it could become to dense at the target point
    if len(lines) > 1 and render_grid:
        coords.extend(do_grid(helper_lines, line_count - skip_end))

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def do_grid(lines, num_lines):
    coords = []
    if num_lines % 2 == 0:
        lines = reversed(lines)
    for i, line in enumerate(lines):
        line_coords = list(line.coords)
        if (i % 2 == 0 and num_lines % 2 == 0) or (i % 2 != 0 and num_lines % 2 != 0):
            coords.extend(reversed(line_coords))
        else:
            coords.extend(line_coords)
    return coords


def line_length(line):
    return line.length


def is_closed(line):
    coords = line.coords
    return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05


def target_point_lines(outline, target, flip):
    lines = []
    for point in outline.coords:
        if flip:
            lines.append(LineString([point, target]))
        else:
            lines.append(LineString([target, point]))
    return lines


def target_point_lines_normalized_distances(outline, target, flip, max_stitch_length):
    lines = []
    outline = running_stitch(line_string_to_point_list(outline), max_stitch_length)
    for point in outline:
        if flip:
            lines.append(LineString([target, point]))
        else:
            lines.append(LineString([point, target]))
    return lines


def guided_helper_lines(outline, flip, max_stitch_length, guide_line):
    # generates lines along the guide line tapering off towards to top
    line_point_dict = defaultdict(list)
    outline = running_stitch(line_string_to_point_list(outline), max_stitch_length)
    guide_line = running_stitch(line_string_to_point_list(guide_line), max_stitch_length)
    guide_length = len(guide_line)
    for j, outline_point in enumerate(outline):
        points = []
        for i, guide_point in enumerate(guide_line):
            if i == 0:
                steps = list(reversed(get_steps(guide_length - 1, 1)))
            else:
                if steps[i] == 0:
                    point = guide_point
                else:
                    transform = guide_line[0] - guide_point
                    transformed_point = outline_point - transform
                    transformed_line = LineString([guide_point, Point(transformed_point)])
                    distance = transformed_line.length * steps[i]
                    point = substring(transformed_line, 0, distance).coords[1]
                points.append(Point(point))
        line_point_dict[j] = points

    lines = []
    for i in range(len(outline)):
        lines.append(LineString(line_point_dict[i]))
    return lines


def get_interpolation_points(lines, line_count, exponent, method="linear"):
    new_points = defaultdict(list)
    count = len(lines) - 1
    for i, line in enumerate(lines):
        steps = get_steps(line_count, exponent)
        points = []
        for j in range(line_count):
            length = line.length * steps[j]
            if method == "circular":
                distance = length + (((line.length * steps[j+1]) - length) * (i / count))
            else:
                distance = line.length * steps[j]
            points.append(line.interpolate(distance))
        if method == "linear":
            points.append(Point(*line.coords[-1]))
        new_points[i] = points
    return new_points


def get_steps(total_lines, exponent):
    # get_steps is scribbled from the inkscape interpolate extension
    # (https://gitlab.com/inkscape/extensions/-/blob/master/interp.py)
    steps = [
        ((i + 1) / (total_lines)) ** exponent
        for i in range(total_lines - 1)
    ]
    return [0] + steps + [1]


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
