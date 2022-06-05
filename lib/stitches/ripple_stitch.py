from collections import defaultdict
from math import atan2

import numpy as np
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, Point

from .running_stitch import running_stitch
from ..elements import SatinColumn
from ..utils import Point as InkstitchPoint
from ..utils.geometry import line_string_to_point_list


def ripple_stitch(stroke):
    '''
    Ripple stitch is allowed to cross itself and doesn't care about an equal distance of lines
    It is meant to be used with light (not dense) stitching
    It will ignore holes in a closed shape. Closed shapes will be filled with a spiral
    Open shapes will be stitched back and forth.
    If there is only one (open) line or a closed shape the target point will be used.
    If more sublines are present interpolation will take place between the first two.
    '''

    is_linear, helper_lines = _get_helper_lines(stroke)
    ripple_points = _do_ripple(stroke, helper_lines, is_linear)

    if stroke.reverse:
        ripple_points.reverse()

    if stroke.grid_size != 0:
        ripple_points.extend(_do_grid(stroke, helper_lines))

    return running_stitch(ripple_points, stroke.running_stitch_length)


def _do_ripple(stroke, helper_lines, is_linear):
    points = []

    for point_num in range(stroke.get_skip_start(), len(helper_lines[0]) - stroke.get_skip_end()):
        row = []
        for line_num in range(len(helper_lines)):
            row.append(helper_lines[line_num][point_num])

        if is_linear and point_num % 2 == 1:
            # reverse every other row in linear ripple
            row.reverse()

        points.extend(row)

    return points


def _get_helper_lines(stroke):
    lines = stroke.as_multi_line_string().geoms
    if len(lines) > 1:
        return True, _get_satin_ripple_helper_lines(stroke)
    else:
        outline = max(lines, key=lambda line: line.length)
        outline = LineString(running_stitch(line_string_to_point_list(outline), stroke.grid_size or stroke.running_stitch_length))

        if _is_closed(outline):
            return False, _get_circular_ripple_helper_lines(stroke, outline)
        else:
            return True, _get_linear_ripple_helper_lines(stroke, outline)


def _get_satin_ripple_helper_lines(stroke):
    # if grid_size has a number use this, otherwise use running_stitch_length
    length = stroke.grid_size or stroke.running_stitch_length

    # use satin column points for satin like build ripple stitches
    rail_points = SatinColumn(stroke.node).plot_points_on_rails(length, 0)

    steps = _get_steps(stroke.line_count, exponent=stroke.exponent, flip=stroke.flip_exponent)

    helper_lines = []
    for point0, point1 in zip(*rail_points):
        helper_lines.append([])
        helper_line = LineString((point0, point1))
        for step in steps:
            helper_lines[-1].append(InkstitchPoint.from_shapely_point(helper_line.interpolate(step, normalized=True)))

    return helper_lines


def _get_circular_ripple_helper_lines(stroke, outline):
    helper_lines = _get_linear_ripple_helper_lines(stroke, outline)

    # Now we want to adjust the helper lines to make a spiral.
    num_lines = len(helper_lines)
    steps = _get_steps(num_lines)
    for i, line in enumerate(helper_lines):
        points = []
        for j in range(len(line) - 1):
            points.append(line[j] * (1 - steps[i]) + line[j + 1] * steps[i])
        helper_lines[i] = points

    return helper_lines


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
    steps = _get_steps(stroke.line_count, exponent=stroke.exponent, flip=stroke.flip_exponent)
    for i, point in enumerate(outline.coords):
        line = LineString([point, target])

        for step in steps:
            helper_lines[i].append(InkstitchPoint.from_shapely_point(line.interpolate(step, normalized=True)))

    return helper_lines


def _do_grid(stroke, helper_lines):
    for i, helper in enumerate(helper_lines):
        start = stroke.get_skip_start()
        end = len(helper) - stroke.get_skip_end()
        points = helper[start:end]
        if i % 2 == 0:
            points.reverse()
        yield from points


def _is_closed(line):
    coords = line.coords
    return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05


def _get_guided_helper_lines(stroke, outline, max_distance):
    # for each point generate a line going along and pointing to the guide line
    guide_line = stroke.get_guide_line()
    if isinstance(guide_line, SatinColumn):
        # satin type guide line
        return _generate_satin_guide_helper_lines(stroke, outline, guide_line)
    else:
        # simple guide line
        return _generate_guided_helper_lines(stroke, outline, max_distance, guide_line.geoms[0])


def _generate_guided_helper_lines(stroke, outline, max_distance, guide_line):
    # helper lines are generated by making copies of the outline alog the guide line
    line_point_dict = defaultdict(list)
    outline = LineString(running_stitch(line_string_to_point_list(outline), max_distance))

    center = outline.centroid
    center = InkstitchPoint(center.x, center.y)

    outline_steps = _get_steps(stroke.line_count, exponent=stroke.exponent, flip=stroke.flip_exponent)
    scale_steps = _get_steps(stroke.line_count, start=stroke.scale_start / 100.0, end=stroke.scale_end / 100.0)

    start_point = InkstitchPoint(*(guide_line.coords[0]))
    start_rotation = _get_start_rotation(guide_line)

    previous_guide_point = None
    for i in range(stroke.line_count):
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


def _generate_satin_guide_helper_lines(stroke, outline, guide_line):
    spacing = guide_line.center_line.length / (stroke.line_count - 1)
    rail_points = guide_line.plot_points_on_rails(spacing, 0)

    point0 = rail_points[0][0]
    point1 = rail_points[1][0]
    start_rotation = atan2(point1.y - point0.y, point1.x - point0.x)
    start_scale = (point1 - point0).length()
    outline_center = InkstitchPoint.from_shapely_point(outline.centroid)

    line_point_dict = defaultdict(list)

    # add scaled and rotated outlines along the satin column guide line
    for i, (point0, point1) in enumerate(zip(*rail_points)):
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
    final_coords = []
    for i in range(repeats):
        if i % 2 == 1:
            # reverse every other pass
            this_coords = coords[::-1]
        else:
            this_coords = coords[:]

        final_coords.extend(this_coords)
    return final_coords
