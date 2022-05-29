from collections import defaultdict
from math import atan2, pi

from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import substring

from ..utils import Point as InkstitchPoint
from ..utils.geometry import line_string_to_point_list
from .running_stitch import running_stitch


def ripple_stitch(lines, target, line_count, points, max_stitch_length, repeats, reverse, skip_start, skip_end,
                  render_grid, exponent, flip_exponent, scale_axis, rotate_ripples, guide_line):
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

    if _is_closed(outline):
        rippled_line = _do_circular_ripple(outline, target, line_count, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                                           exponent, flip_exponent, scale_axis, rotate_ripples, guide_line)
    else:
        rippled_line = _do_linear_ripple(lines, points, target, line_count - 1, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                                         exponent, flip_exponent, scale_axis, rotate_ripples, guide_line)

    if reverse != flip_exponent:
        rippled_line = LineString(list(reversed(rippled_line.coords)))

    return running_stitch(line_string_to_point_list(rippled_line), max_stitch_length)


def _do_circular_ripple(outline, target, line_count, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                        exponent, flip_exponent, scale_axis, rotate_ripples, guide_line):
    max_dist = render_grid or max_stitch_length
    if guide_line:
        lines = _get_guided_helper_lines(outline, max_dist, flip_exponent, scale_axis, rotate_ripples, guide_line)
    else:
        # for each point generate a line going to the target point
        lines = _target_point_lines_normalized_distances(outline, target, flip_exponent, max_dist)

    # create a list of points for each line
    points = _get_interpolation_points(lines, line_count, exponent, "circular")

    # connect the lines to a spiral towards the target
    coords = []
    for i in range(skip_start, line_count - skip_end):
        for j in range(len(lines)):
            coords.append(Point(points[j][i].x, points[j][i].y))

    if render_grid:
        coords.extend(_do_grid(lines, points, line_count, skip_start, skip_end, flip_exponent))

    coords = _repeat_coords(coords, repeats)

    return LineString(coords)


def _do_linear_ripple(lines, points, target, line_count, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                      exponent, flip_exponent, scale_axis, rotate_ripples, guide_line):

    if len(lines) == 1:
        if guide_line:
            helper_lines = _get_guided_helper_lines(lines[0], max_stitch_length, flip_exponent, scale_axis, rotate_ripples, guide_line)
        else:
            helper_lines = _target_point_lines(lines[0], target, flip_exponent)
    else:
        helper_lines = []
        for start, end in zip(points[0], points[1]):
            if flip_exponent:
                end, start = [start, end]
            helper_lines.append(LineString([start, end]))

    # get linear points along the lines
    points = _get_interpolation_points(helper_lines, line_count, exponent)

    # go back and forth along the lines - flip direction of every second line
    coords = []
    for i in range(skip_start, len(points[0]) - skip_end):
        for j in range(len(helper_lines)):
            k = j
            if i % 2 != 0:
                k = len(helper_lines) - j - 1
            coords.append(Point(points[k][i].x, points[k][i].y))

    # add helper lines as a grid
    if render_grid:
        coords.extend(_do_grid(helper_lines, points, line_count, skip_start, skip_end, flip_exponent))

    coords = _repeat_coords(coords, repeats)

    return LineString(coords)


def _do_grid(lines, point_dict, line_count, skip_start, skip_end, flip_exponent):
    num_lines = line_count - skip_end
    coords = []

    start = 0
    end = len(lines) - 1
    steps = 1
    if num_lines % 2 == 0:
        start, end = [end, start]
        steps = -1
    for i in range(start, end, steps):
        line = lines[i]
        if skip_start or skip_end:
            # get the substring of helper lines if start or end has been skipped
            seg_start = line.project(point_dict[i][skip_start])
            seg_end = line.project(point_dict[i][len(point_dict[0]) - skip_end - 1])
            seg = substring(line, seg_start, seg_end)
            line_coords = list(seg.coords)
        else:
            line_coords = list(line.coords)

        if (i % 2 != 0 and num_lines % 2 == 0) or (i % 2 == 0 and num_lines % 2 != 0):
            coords.extend(reversed(line_coords))
        else:
            coords.extend(line_coords)

    return coords


def _is_closed(line):
    coords = line.coords
    return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05


def _target_point_lines(outline, target, flip_exponent):
    lines = []
    for point in outline.coords:
        if flip_exponent:
            lines.append(LineString([point, target]))
        else:
            lines.append(LineString([target, point]))
    return lines


def _target_point_lines_normalized_distances(outline, target, flip_exponent, max_stitch_length):
    lines = []
    outline = running_stitch(line_string_to_point_list(outline), max_stitch_length)
    for point in outline:
        if flip_exponent:
            lines.append(LineString([target, point]))
        else:
            lines.append(LineString([point, target]))
    return lines


def _get_guided_helper_lines(lines, max_stitch_length, flip_exponent, scale_axis, rotate_ripples, guide_line):
    # for each point generate a line going along and pointing to the guide line
    if isinstance(guide_line, MultiLineString):
        # simple guide line
        lines = _generate_guided_helper_lines(lines, max_stitch_length, flip_exponent, scale_axis, rotate_ripples, guide_line.geoms[0])
    else:
        # satin type guide line
        rail_points = guide_line.plot_points_on_rails(max_stitch_length, 0)
        lines = _generate_satin_guide_helper_lines(lines, max_stitch_length, flip_exponent, scale_axis, rotate_ripples, rail_points)
    return lines


def _generate_guided_helper_lines(outline, max_stitch_length, flip_exponent, scale_axis, rotate_ripples, guide_line):
    # generates lines along the guide line tapering off towards to top
    line_point_dict = defaultdict(list)
    outline = LineString(running_stitch(line_string_to_point_list(outline), max_stitch_length))

    center = outline.centroid
    center = InkstitchPoint(center.x, center.y)

    guide_line = line_string_to_point_list(guide_line)
    # add center point of the outline as the starting point to the guide line
    guide_line = [center] + guide_line
    guide_line = running_stitch(guide_line, max_stitch_length)
    guide_length = len(guide_line)

    steps = list(reversed(_get_steps(guide_length - 1, 1)))

    minx, miny, maxx, maxy = outline.bounds
    minx = _get_most_distant_x_point(minx, outline.coords)
    outline_rotation = atan2(center.y - minx.y, center.x - minx.x)

    for i, guide_point in enumerate(guide_line):
        translation = guide_point - center
        scaling = steps[i]
        if rotate_ripples and not i == 0:
            rotation = atan2(guide_point.y - minx.y, guide_point.x - minx.x)
            rotation = abs((rotation - outline_rotation) * 360 / (2 * pi))
        else:
            rotation = 0
        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(guide_point), scale_axis, rotate_ripples)

        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(point)

    return _point_dict_to_linestring(len(outline.coords), line_point_dict, flip_exponent)


def _generate_satin_guide_helper_lines(outline, max_stitch_length, flip_exponent, scale_axis, rotate_ripples, rail_points):
    first, last = [Point(i) for i in outline.coords[::len(outline.coords)-1]]
    if _is_closed(outline):
        minx, miny, maxx, maxy = outline.bounds
        first = _get_most_distant_x_point(minx, outline.coords)
        last = _get_most_distant_x_point(maxx, outline.coords)

    outline_width = last.x - first.x

    # flip rails if they are the wrong way around
    rail_start_width = rail_points[0][0].x - rail_points[1][0].x
    if (outline_width * rail_start_width > 0):
        rail_points = list(reversed(rail_points))

    outline_width = abs(outline_width)
    outline = LineString(running_stitch(line_string_to_point_list(outline), max_stitch_length))
    outline_center = InkstitchPoint((last.x + first.x) / 2, (last.y + first.y) / 2)

    outline_rotation = atan2(first.y - last.y, first.x - last.x)

    line_point_dict = defaultdict(list)
    # add original line
    for j, point in enumerate(outline.coords):
        line_point_dict[j].append(point)

    # add scaled and rotated outlines along the satin column guide line
    for i, (point1, point2) in enumerate(zip(*rail_points)):
        guide_center = InkstitchPoint((point2.x + point1.x) / 2, (point2.y + point1.y) / 2)
        translation = guide_center - outline_center
        if rotate_ripples:
            rotation = atan2(point1.y - point2.y, point1.x - point2.x)
            rotation = (rotation - outline_rotation) * 360 / (2 * pi)
        else:
            rotation = 0
        scaling = abs((point2 - point1).length() / outline_width)

        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(guide_center), scale_axis, rotate_ripples)
        # outline to helper line points
        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(point)

    return _point_dict_to_linestring(len(outline.coords), line_point_dict, flip_exponent)


def _transform_outline(translation, rotation, scaling, outline, origin, scale_axis, rotate_ripples):
    # transform
    transformed_outline = translate(outline, translation.x, translation.y)
    # rotate
    if rotate_ripples:
        transformed_outline = rotate(transformed_outline, rotation, origin=origin)
    # scale | scale_axis => 0: xy, 1: x, 2: y, 3: none
    scale_x = scale_y = scaling
    if scale_axis in [2, 3]:
        scale_x = 1
    if scale_axis in [1, 3]:
        scale_y = 1
    transformed_outline = scale(transformed_outline, scale_x, scale_y, origin=origin)
    return transformed_outline


def _get_most_distant_x_point(x, coords):
    point = [point for point in coords if point[0] == x]
    if len(point) > 1:
        point = LineString(point).centroid
    if not isinstance(point, Point):
        point = Point(point)
    return point


def _point_dict_to_linestring(line_count, point_dict, flip_exponent):
    lines = []
    for i in range(line_count):
        points = point_dict[i]
        if flip_exponent:
            points = list(reversed(points))
        lines.append(LineString(points))
    return lines


def _get_interpolation_points(lines, line_count, exponent, method="linear"):
    new_points = defaultdict(list)
    count = len(lines) - 1
    for i, line in enumerate(lines):
        steps = _get_steps(line_count, exponent)
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


def _get_steps(total_lines, exponent):
    # get_steps is scribbled from the inkscape interpolate extension
    # (https://gitlab.com/inkscape/extensions/-/blob/master/interp.py)
    steps = [
        ((i + 1) / (total_lines)) ** exponent
        for i in range(total_lines - 1)
    ]
    return [0] + steps + [1]


def _repeat_coords(coords, repeats):
    final_coords = []
    for i in range(repeats):
        if i % 2 == 1:
            # reverse every other pass
            this_coords = coords[::-1]
        else:
            this_coords = coords[:]

        final_coords.extend(this_coords)
    return final_coords
