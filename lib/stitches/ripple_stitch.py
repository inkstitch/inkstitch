from collections import defaultdict
from math import atan2, ceil

import numpy as np
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, Point
from shapely.ops import substring

from ..elements import SatinColumn
from ..utils import Point as InkstitchPoint
from ..utils import prng
from ..utils.geometry import line_string_to_point_list
from ..utils.threading import check_stop_flag
from .guided_fill import apply_stitches
from .running_stitch import even_running_stitch, running_stitch


def ripple_stitch(stroke):
    '''
    Ripple stitch is allowed to cross itself and doesn't care about an equal distance of lines
    It is meant to be used with light (not dense) stitching
    It will ignore holes in a closed shape. Closed shapes will be filled with a spiral
    Open shapes will be stitched back and forth.
    If there is only one (open) line or a closed shape the target point will be used.
    If more sublines are present interpolation will take place between the first two.
    '''

    if stroke.as_multi_line_string().length < 0.1:
        return []

    is_linear, helper_lines = _get_helper_lines(stroke)
    if not helper_lines:
        return []

    num_lines = len(helper_lines[0])
    skip_start = _adjust_skip(stroke, num_lines, stroke.skip_start)
    skip_end = _adjust_skip(stroke, num_lines, stroke.skip_end)

    lines = _get_ripple_lines(helper_lines, is_linear, skip_start, skip_end)
    stitches = _get_stitches(stroke, is_linear, lines, skip_start)

    if stroke.reverse:
        stitches.reverse()

    if stitches and stroke.grid_size != 0:
        stitches.extend(_do_grid(stroke, helper_lines, skip_start, skip_end, is_linear, stitches[-1]))
        if stroke.grid_first:
            stitches = stitches[::-1]

    return _repeat_coords(stitches, stroke.repeats)


def _get_stitches(stroke, is_linear, lines, skip_start):
    if stroke.manual_pattern_placement:
        stitches = []
        for i, line in enumerate(lines):
            if i % 2 == 0 and stroke.flip_copies:
                line = line[::-1]
            if stitches:
                # even though this is manual stitch placement, we do not want the
                # connector lines to exceed the running stitch length value
                # so let's add some points
                points = LineString([stitches[-1], line[0]]).segmentize(stroke.running_stitch_length).coords
                if len(points) > 2:
                    stitches.extend([InkstitchPoint(coord[0], coord[1]) for coord in points[1:-1]])
            stitches.extend(line)
        return stitches
    if is_linear and stroke.flip_copies:
        return _get_staggered_stitches(stroke, lines, skip_start)
    else:
        points = [point for line in lines for point in line]
        return running_stitch(points,
                              stroke.running_stitch_length,
                              stroke.running_stitch_tolerance,
                              stroke.enable_random_stitch_length,
                              stroke.random_stitch_length_jitter,
                              stroke.random_seed)


def _get_staggered_stitches(stroke, lines, skip_start):
    stitches = []
    stitch_length = stroke.running_stitch_length
    tolerance = stroke.running_stitch_tolerance
    is_random = stroke.enable_random_stitch_length
    length_sigma = stroke.random_stitch_length_jitter
    random_seed = stroke.random_seed
    last_point = None
    for i, line in enumerate(lines):
        connector = []
        if i != 0 and stroke.join_style == 0:
            if i % 2 == 0 or not stroke.flip_copies:
                first_point = line[0]
            else:
                first_point = line[-1]
            connector = even_running_stitch([last_point, first_point],
                                            stitch_length, tolerance)[1:-1]
        if stroke.join_style == 0:
            should_reverse = i % 2 == 1
        elif stroke.join_style == 1:
            should_reverse = (i + skip_start) % 2 == 1

        if stroke.staggers == 0:
            if should_reverse and stroke.flip_copies:
                line.reverse()
            stitched_line = running_stitch(line, stitch_length, tolerance, is_random, length_sigma, prng.join_args(random_seed, i))
        else:
            if len(stitch_length) > 1:
                points = list(
                    apply_stagger(line, stitch_length, stroke.staggers, i, tolerance, is_random, length_sigma, prng.join_args(random_seed, i)).coords
                )
            else:
                # uses the guided fill alforithm to stagger rows of stitches
                points = list(apply_stitches(LineString(line), stitch_length, stroke.staggers, 0.5, i, tolerance).coords)

            # simplifying the path in apply_stitches could have removed the start or end point
            # we can simply add it again, the minimum stitch length value will take care to remove possible duplicates
            points = [line[0]] + points + [line[-1]]

            stitched_line = [InkstitchPoint(*point) for point in points]
            if should_reverse and stroke.flip_copies:
                stitched_line.reverse()

        stitched_line = connector + stitched_line

        last_point = stitched_line[-1]
        stitches.extend(stitched_line)
    return stitches


def apply_stagger(line, stitch_length, num_staggers, row_num, tolerance, is_random, stitch_length_sigma, random_seed):
    if num_staggers == 0:
        num_staggers = 1  # sanity check to avoid division by zero.
    start = ((row_num / num_staggers) % 1) * sum(stitch_length)
    first_segment = LineString(line[:2])
    segment_length = first_segment.length
    target_length = segment_length + 2 * start
    scale_factor = target_length / segment_length
    extended_line = scale(first_segment, scale_factor, scale_factor)

    line = [InkstitchPoint(*extended_line.coords[0])] + line
    stitched_line = LineString(running_stitch(line, stitch_length, tolerance, is_random, stitch_length_sigma, random_seed))

    points.append(line.coords[-1])
    stitched_line = LineString(points)

    return substring(stitched_line, start, stitched_line.length)


def _adjust_skip(stroke, num_lines, skip):
    if stroke.skip_start + stroke.skip_end >= num_lines:
        return 0
    return skip


def _get_ripple_lines(helper_lines, is_linear, skip_start, skip_end):
    lines = []
    for point_num in range(skip_start, len(helper_lines[0]) - skip_end):
        row = []
        for line_num in range(len(helper_lines)):
            row.append(helper_lines[line_num][point_num])
        lines.append(row)
    return lines


def _get_satin_line_count(stroke, pairs):
    if not stroke.min_line_dist:
        num_lines = stroke.line_count
    else:
        shortest_line_len = 0
        for point0, point1 in pairs:
            length = LineString([point0, point1]).length
            if shortest_line_len == 0 or length < shortest_line_len:
                shortest_line_len = length
        num_lines = ceil(shortest_line_len / stroke.min_line_dist)
    return _line_count_adjust(stroke, num_lines)


def _get_target_line_count(stroke, target, outline):
    return _get_satin_line_count(stroke, zip(outline, [target]*len(outline)))


def _get_guided_line_count(stroke, guide_line):
    if not stroke.min_line_dist:
        num_lines = stroke.line_count
    else:
        num_lines = ceil(guide_line.length / stroke.min_line_dist)
    return _line_count_adjust(stroke, num_lines)


def _line_count_adjust(stroke, num_lines):
    if stroke.min_line_dist and stroke.line_count % 2 != num_lines % 2:
        # We want the line count always to be either even or odd - depending on the line count value.
        # So that the end point stays the same even if the design is resized. This is necessary to enable
        # the user to carefully plan the output and and connect the end point to the following object
        num_lines -= 1
    # ensure minimum line count
    num_lines = max(1, num_lines)
    if stroke.is_closed or stroke.join_style == 1:
        # for flat join styles we need to add an other line
        num_lines += 1
    return num_lines


def _get_helper_lines(stroke):
    lines = stroke.as_multi_line_string().geoms
    if len(lines) > 1:
        return True, _get_satin_ripple_helper_lines(stroke)
    else:
        if stroke.manual_pattern_placement:
            path = stroke.parse_path()
            path = [stroke.strip_control_points(subpath) for subpath in path][0]
            outline = LineString(path)
        else:
            outline = LineString(even_running_stitch(
                line_string_to_point_list(lines[0]),
                stroke.grid_size or stroke.running_stitch_length,
                stroke.running_stitch_tolerance)
            )

        if stroke.is_closed:
            return False, _get_circular_ripple_helper_lines(stroke, outline)
        elif stroke.join_style == 1:
            return True, _get_point_style_linear_helper_lines(stroke, outline)
        else:
            return True, _get_linear_ripple_helper_lines(stroke, outline)


def _get_satin_ripple_helper_lines(stroke):
    # if grid_size has a number use this, otherwise use running_stitch_length
    length = stroke.grid_size or min(stroke.running_stitch_length)

    # use satin column points for satin like build ripple stitches
    rail_pairs = SatinColumn(stroke.node).plot_points_on_rails(length)
    count = _get_satin_line_count(stroke, rail_pairs)

    steps = _get_steps(count, exponent=stroke.exponent, flip=stroke.flip_exponent)

    helper_lines = []
    for point0, point1 in rail_pairs:
        check_stop_flag()

        helper_lines.append([])
        helper_line = LineString((point0, point1))
        for step in steps:
            helper_lines[-1].append(InkstitchPoint.from_shapely_point(helper_line.interpolate(step, normalized=True)))

    if stroke.join_style == 1 or not stroke.flip_copies:
        helper_lines = _converge_helper_line_points(helper_lines, True, stroke.flip_copies)

    return helper_lines


def _converge_helper_line_points(helper_lines, point_edge=False, flip_copies=True):
    num_lines = len(helper_lines)
    steps = _get_steps(num_lines)
    for i, line in enumerate(helper_lines):
        check_stop_flag()

        points = []
        for j in range(len(line) - 1):
            if point_edge and j % 2 == 1 and flip_copies:
                k = num_lines - 1 - i
                points.append(line[j] * (1 - steps[k]) + line[j + 1] * steps[k])
            else:
                points.append(line[j] * (1 - steps[i]) + line[j + 1] * steps[i])
        helper_lines[i] = points

    return helper_lines


def _get_circular_ripple_helper_lines(stroke, outline):
    helper_lines = _get_linear_ripple_helper_lines(stroke, outline)
    # Now we want to adjust the helper lines to make a spiral.
    return _converge_helper_line_points(helper_lines)


def _get_point_style_linear_helper_lines(stroke, outline):
    helper_lines = _get_linear_ripple_helper_lines(stroke, outline)
    return _converge_helper_line_points(helper_lines, True)


def _get_linear_ripple_helper_lines(stroke, outline):
    guide_line = stroke.get_guide_line()
    max_dist = stroke.grid_size or stroke.running_stitch_length

    if guide_line:
        return _get_guided_helper_lines(stroke, outline, max_dist)
    else:
        return _target_point_helper_lines(stroke, outline)


def _target_point_helper_lines(stroke, outline):
    helper_lines = [[] for i in range(len(outline.coords))]
    target = stroke.get_ripple_target()
    count = _get_target_line_count(stroke, target, outline.coords)
    steps = _get_steps(count, exponent=stroke.exponent, flip=stroke.flip_exponent)
    for i, point in enumerate(outline.coords):
        check_stop_flag()

        line = LineString([point, target])

        for step in steps:
            helper_lines[i].append(InkstitchPoint.from_shapely_point(line.interpolate(step, normalized=True)))

    return helper_lines


def _adjust_helper_lines_for_grid(grid, last_stitch):
    # check which end of the grid is nearest to the last stitch
    # and adjust grid accordingly
    last_stitch = Point(last_stitch)
    distances = [
        Point(grid[0][0]).distance(last_stitch),
        Point(grid[0][-1]).distance(last_stitch),
        Point(grid[-1][0]).distance(last_stitch),
        Point(grid[-1][-1]).distance(last_stitch)
    ]
    nearest = distances.index(min(distances))
    if nearest in [1, 3]:
        adjusted_grid = []
        for line in grid:
            adjusted_grid.append(line[::-1])
        grid = adjusted_grid
    if nearest in [2, 3]:
        grid.reverse()
    return grid


def _do_grid(stroke, helper_lines, skip_start, skip_end, is_linear, last_stitch):
    grid = []
    for i, helper in enumerate(helper_lines):
        end = len(helper) - skip_end
        points = helper[skip_start:end]
        if i % 2 != 0 and is_linear and not stroke.flip_copies and stroke.join_style == 0:
            points.reverse()
        grid.append(points)
    grid = _adjust_helper_lines_for_grid(grid, last_stitch)
    grid = _get_staggered_stitches(stroke, grid, 0)
    return grid


def _get_guided_helper_lines(stroke, outline, max_distance):
    # for each point generate a line going along and pointing to the guide line
    guide_line = stroke.get_guide_line()
    if isinstance(guide_line, SatinColumn):
        # satin type guide line
        return generate_satin_guide_helper_lines(stroke, outline, guide_line)
    else:
        # simple guide line
        return _generate_guided_helper_lines(stroke, outline, max_distance, guide_line.geoms[0])


def _generate_guided_helper_lines(stroke, outline, max_distance, guide_line):
    # helper lines are generated by making copies of the outline along the guide line
    line_point_dict = defaultdict(list)
    if not stroke.manual_pattern_placement:
        outline = LineString(even_running_stitch(
            line_string_to_point_list(outline),
            max_distance,
            stroke.running_stitch_tolerance
        ))

    center = outline.centroid
    center = InkstitchPoint(center.x, center.y)

    if stroke.satin_guide_pattern_position == "render_at_rungs":
        count = len(guide_line.coords)
    else:
        count = _get_guided_line_count(stroke, guide_line)
        outline_steps = _get_steps(count, exponent=stroke.exponent, flip=stroke.flip_exponent)

    scale_steps = _get_steps(count, start=stroke.scale_start / 100.0, end=stroke.scale_end / 100.0)

    start_point = InkstitchPoint(*(guide_line.coords[0]))
    start_rotation = _get_start_rotation(guide_line)

    previous_guide_point = None
    for i in range(count):
        check_stop_flag()

        if stroke.satin_guide_pattern_position == "render_at_rungs":
            # Requires the guide line to be defined as manual stitch
            guide_point = InkstitchPoint(*guide_line.coords[i])
        else:
            guide_point = InkstitchPoint.from_shapely_point(guide_line.interpolate(outline_steps[i], normalized=True))
        translation = guide_point - start_point
        scaling = scale_steps[i]
        if stroke.rotate_ripples and previous_guide_point:
            rotation = atan2(guide_point.y - previous_guide_point.y, guide_point.x - previous_guide_point.x)
            rotation = rotation - start_rotation
        else:
            rotation = 0
        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(guide_point), stroke.scale_axis)

        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(InkstitchPoint(point[0], point[1]))

        previous_guide_point = guide_point

    return _point_dict_to_helper_lines(len(outline.coords), line_point_dict)


def _get_start_rotation(line):
    point0 = line.interpolate(0)
    point1 = line.interpolate(0.1)

    return atan2(point1.y - point0.y, point1.x - point0.x)


def generate_satin_guide_helper_lines(stroke, outline, guide_line):
    anchor_line = stroke.get_anchor_line()
    if anchor_line:
        # position, rotation and scale defined by anchor line
        outline0 = InkstitchPoint(*anchor_line.coords[0])
        outline1 = InkstitchPoint(*anchor_line.coords[-1])
    else:
        # position rotation and scale defined by line end points
        outline_coords = outline.coords
        outline0 = InkstitchPoint(*outline_coords[0])
        outline1 = InkstitchPoint(*outline_coords[-1])
        if outline0 == outline1:
            return _generate_simple_satin_guide_helper_lines(stroke, outline, guide_line)

    outline_width = (outline1 - outline0).length()
    outline_rotation = atan2(outline1.y - outline0.y, outline1.x - outline0.x)

    if stroke.satin_guide_pattern_position == "adaptive":
        return _generate_satin_guide_helper_lines_with_varying_pattern_distance(
            stroke, guide_line, outline, outline0, outline_width, outline_rotation
        )
    else:
        return _generate_satin_guide_helper_lines_with_constant_pattern_distance(
            stroke, guide_line, outline, outline0, outline_width, outline_rotation
        )


def _generate_simple_satin_guide_helper_lines(stroke, outline, guide_line):
    count = _get_guided_line_count(stroke, guide_line.center_line)

    spacing = guide_line.center_line.length / max(1, count - 1)
    if stroke.satin_guide_pattern_position == "render_at_rungs":
        sections = guide_line.flattened_sections
        pairs = []
        for (rail0, rail1) in sections:
            pairs.append((rail0[-1], rail1[-1]))
        pairs = pairs[:-1]
    else:
        pairs = guide_line.plot_points_on_rails(spacing)

    point0 = pairs[0][0]
    point1 = pairs[0][1]

    start_rotation = atan2(point1.y - point0.y, point1.x - point0.x)
    start_scale = (point1 - point0).length()
    outline_center = InkstitchPoint.from_shapely_point(outline.centroid)

    line_point_dict = defaultdict(list)

    # add scaled and rotated outlines along the satin column guide line
    for i, (point0, point1) in enumerate(pairs):
        check_stop_flag()

        guide_center = (point0 + point1) / 2
        translation = guide_center - outline_center
        if stroke.rotate_ripples:
            rotation = atan2(point1.y - point0.y, point1.x - point0.x)
            rotation = rotation - start_rotation
        else:
            rotation = 0
        scaling = (point1 - point0).length() / start_scale

        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(guide_center), stroke.scale_axis)

        # outline to helper line points
        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(InkstitchPoint(point[0], point[1]))

    return _point_dict_to_helper_lines(len(outline.coords), line_point_dict)


def _generate_satin_guide_helper_lines_with_constant_pattern_distance(stroke, guide_line, outline, outline0, outline_width, outline_rotation):
    # add scaled and rotated outlines along the satin column guide line
    if stroke.satin_guide_pattern_position == "render_at_rungs":
        sections = guide_line.flattened_sections
        pairs = []
        for (rail0, rail1) in sections:
            pairs.append((rail0[-1], rail1[-1]))
    else:
        count = _get_guided_line_count(stroke, guide_line.center_line)
        spacing = guide_line.center_line.length / max(1, count - 1)
        pairs = guide_line.plot_points_on_rails(spacing)

    if pairs[0] == pairs[-1]:
        pairs = pairs[:-1]

    line_point_dict = defaultdict(list)
    for i, (point0, point1) in enumerate(pairs):
        check_stop_flag()

        # move to point0, rotate and scale so the other point hits point1
        scaling = (point1 - point0).length() / outline_width
        rotation = atan2(point1.y - point0.y, point1.x - point0.x)
        rotation = rotation - outline_rotation
        translation = point0 - outline0
        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(point0), 0)

        # outline to helper line points
        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(InkstitchPoint(point[0], point[1]))

    return _point_dict_to_helper_lines(len(outline.coords), line_point_dict)


def _generate_satin_guide_helper_lines_with_varying_pattern_distance(stroke, guide_line, outline, outline0, outline_width, outline_rotation):
    # rotate pattern and get the pattern width
    transformed_outline = _transform_outline(Point([0, 0]), outline_rotation, 1, outline, Point(outline0), 0)
    minx, miny, maxx, maxy = transformed_outline.bounds
    pattern_height = maxy - miny

    distance = 0
    min_distance = stroke.min_line_dist or 0
    line_point_dict = defaultdict(list)
    while True:
        if distance > guide_line.center_line.length:
            break
        check_stop_flag()
        point0, point1 = get_cut_points(guide_line, distance)

        # move to point0, rotate and scale so the other point hits point1
        scaling = (point1 - point0).length() / outline_width
        rotation = atan2(point1.y - point0.y, point1.x - point0.x)
        rotation = rotation - outline_rotation
        translation = point0 - outline0
        transformed_outline = _transform_outline(translation, rotation, scaling, outline, Point(point0), 0)

        distance += max(0.01, (pattern_height * scaling) + min_distance)

        # outline to helper line points
        for j, point in enumerate(transformed_outline.coords):
            line_point_dict[j].append(InkstitchPoint(point[0], point[1]))

    return _point_dict_to_helper_lines(len(outline.coords), line_point_dict)


def get_cut_points(guide_line, distance):
    cut_point = guide_line.center_line.interpolate(distance)
    return guide_line.find_cut_points(*cut_point.coords)


def _transform_outline(translation, rotation, scaling, outline, origin, scale_axis):
    # transform
    transformed_outline = translate(outline, translation.x, translation.y)
    # rotate
    if rotation != 0:
        transformed_outline = rotate(transformed_outline, rotation, use_radians=True, origin=origin)
    # scale | scale_axis => 0: xy, 1: x, 2: y, 3: none
    scale_x = scale_y = scaling
    if scale_axis in [2, 3]:
        scale_x = 1
    if scale_axis in [1, 3]:
        scale_y = 1
    transformed_outline = scale(transformed_outline, scale_x, scale_y, origin=origin)
    return transformed_outline


def _point_dict_to_helper_lines(line_count, point_dict):
    lines = []
    for i in range(line_count):
        points = point_dict[i]
        lines.append(points)
    return lines


def _get_steps(num_steps, start=0.0, end=1.0, exponent=1, flip=False):
    steps = np.linspace(start, end, num_steps)
    steps = steps ** exponent

    if flip:
        steps = 1.0 - np.flip(steps)

    return list(steps)


def _repeat_coords(coords, repeats):
    if not coords:
        return coords
    final_coords = []
    for i in range(repeats):
        if i % 2 == 1:
            # reverse every other pass
            this_coords = coords[::-1]
        else:
            this_coords = coords[:]

        final_coords.extend(this_coords)
    return final_coords
