# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil, floor, sqrt

import numpy as np
from inkex import Color, ColorError, DirectedLineSegment, Transform
from networkx import is_empty
from shapely import segmentize
from shapely.affinity import rotate
from shapely.geometry import LineString, MultiLineString, Point, Polygon

from lib.utils import prng

from ..stitch_plan import StitchGroup
from ..svg import get_node_transform
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import ensure_multi_line_string
from ..utils.threading import check_stop_flag
from .auto_fill import (build_fill_stitch_graph, build_travel_graph,
                        find_stitch_path, graph_make_valid)
from .circular_fill import path_to_stitches
from .guided_fill import apply_stitches
from .running_stitch import random_running_stitch


def linear_gradient_fill(fill, shape, starting_point, ending_point):
    lines, colors, stop_color_line_indices = _get_lines_and_colors(shape, fill)
    color_lines, colors = _get_color_lines(lines, colors, stop_color_line_indices)
    stitch_groups = _get_stitch_groups(fill, shape, colors, color_lines, starting_point, ending_point)
    return stitch_groups


def _get_lines_and_colors(shape, fill):
    '''
    Returns lines and color gradient information
    lines:  a list of lines which cover the whole shape in a 90° angle to the gradient line
    colors: a list of color values
    stop_color_line_indices: line indices indicating where color changes are positioned at
    '''
    orig_bbox = shape.bounds

    # get angle, colors, as well as start and stop position of the gradient
    angle, colors, offsets, gradient_start, gradient_end = _get_gradient_info(fill, orig_bbox)

    # get lines
    lines, bottom_line = _get_lines(fill, shape, orig_bbox, angle)

    gradient_start_line_index = round(bottom_line.project(gradient_start) / fill.row_spacing)
    if gradient_start_line_index == 0:
        gradient_start_line_index = -round(LineString([gradient_start, gradient_end]).project(Point(bottom_line.coords[0])) / fill.row_spacing)
    stop_color_line_indices = []
    gradient_line = LineString([gradient_start, gradient_end])
    for offset in offsets:
        stop_color_line_indices.append(round((gradient_line.length * offset) / fill.row_spacing) + gradient_start_line_index)

    return lines, colors, stop_color_line_indices


def _get_gradient_info(fill, bbox):
    if fill.gradient is None:
        # there is no linear gradient, let's simply space out one single color instead
        angle = fill.angle
        offsets = [0, 1]
        colors = [fill.color, 'none']
        gradient_start = (bbox[0], bbox[1])
        gradient_end = (bbox[2], bbox[3])
    else:
        fill.gradient.apply_transform()
        offsets = fill.gradient.stop_offsets
        # get stop colors
        # it would be easier if we just used fill.gradient.stop_styles to collect them
        # but inkex/tinycss fails on stop color styles when it is not in the style attribute, but in it's own stop-color attribute
        colors = []
        for i, stop in enumerate(fill.gradient.stops):
            try:
                color = stop.get_computed_style('stop-color')
            except ColorError:
                color = Color('black')
            opacity = stop.get_computed_style('stop-opacity')
            if float(opacity) == 0:
                color = 'none'
            colors.append(color)
        gradient_start, gradient_end = gradient_start_end(fill.node, fill.gradient)
        angle = gradient_angle(fill.node, fill.gradient)
    return angle, colors, offsets, Point(list(gradient_start)), Point(list(gradient_end))


def _get_lines(fill, shape, bounding_box, angle):
    '''
    To generate the lines we rotate the bounding box to bring the angle in vertical position.
    From bounds we create a Polygon which we then rotate back, so we receive a rotated bounding box
    which aligns well to the stitch angle. Combining the points of the subdivided top and bottom line
    will finally deliver to our stitch rows
    '''

    # get the rotated bounding box for the shape
    rotated_shape = rotate(shape, -angle, origin=(bounding_box[0], bounding_box[3]), use_radians=True)
    bounds = rotated_shape.bounds

    # Generate a Polygon from the rotated bounding box which we then rotate back into original position
    # extend bounding box for lines just a little to make sure we cover the whole area with lines
    # this avoids rounding errors due to the rotation later on
    rot_bbox = Polygon([
        (bounds[0] - fill.max_stitch_length, bounds[1] - fill.row_spacing),
        (bounds[2] + fill.max_stitch_length, bounds[1] - fill.row_spacing),
        (bounds[2] + fill.max_stitch_length, bounds[3] + fill.row_spacing),
        (bounds[0] - fill.max_stitch_length, bounds[3] + fill.row_spacing)
    ])
    # and rotate it back into original position
    rot_bbox = list(rotate(rot_bbox, angle, origin=(bounding_box[0], bounding_box[3]), use_radians=True).exterior.coords)

    # segmentize top and bottom line to finally be ableto generate the stitch lines
    top_line = LineString([rot_bbox[0], rot_bbox[1]])
    top = segmentize(top_line, max_segment_length=fill.row_spacing)

    bottom_line = LineString([rot_bbox[3], rot_bbox[2]])
    bottom = segmentize(bottom_line, max_segment_length=fill.row_spacing)

    lines = list(zip(top.coords, bottom.coords))

    # stagger stitched lines according to user settings
    staggered_lines = []
    for i, line in enumerate(lines):
        if fill.enable_random_stitch_length:
            points = [InkstitchPoint(*x) for x in line]
            staggered_line = LineString(random_running_stitch(
                points,
                [fill.max_stitch_length], fill.running_stitch_tolerance, fill.random_stitch_length_jitter, prng.join_args(fill.random_seed, i))
            )
        else:
            staggered_line = apply_stitches(LineString(line), [fill.max_stitch_length], fill.staggers, fill.row_spacing, i)
        staggered_lines.append(staggered_line)
    return staggered_lines, bottom_line


def _get_color_lines(lines, colors, stop_color_line_indices):
    '''
    To define which line will be stitched in which color, we will loop through the color sections
    defined by the stop positions of the gradient (stop_color_line_indices).
    Each section will then be subdivided into smaller sections using the square root of the total line number
    of the whole section. Lines left over from this operation will be added step by step to the smaller sub-sections.
    Since we do this symmetrically we may end one line short, which we an add at the end.

    Now we define the line colors of the first half of our color section, we will later mirror this on the second half.
    Therefor we use one additional line of color2 in each sub-section and position them as evenly as possible between the color1 lines.
    Doing this we take care, that the number of consecutive lines of color1 is always decreasing.

    For example let's take a 12 lines sub-section, with 5 lines of color2.
    12 / 5 = 2.4
    12 % 5 = 2
    This results into the following pattern:
    xx|xx|x|x|x| (while x = color1 and | = color2).
    Note that the first two parts have an additional line (as defined by the modulo operation)

    Method returns
    color_lines: A dictionary with lines grouped by color
    colors:      An updated list of color values.
                 Colors which are positioned outside the shape will be removed.
    '''

    # create dictionary with a key for each color
    color_lines = {}
    for color in colors:
        color_lines[color] = []

    prev_color = colors[0]
    prev = None
    for line_index, color in zip(stop_color_line_indices, colors):
        if prev is None:
            if line_index > 0:
                color_lines[color].extend(lines[0:line_index + 1])
            prev = line_index
            prev_color = color
            continue
        if prev < 0 and line_index < 0:
            prev = line_index
            prev_color = color
            continue

        prev += 1
        line_index += 1
        total_lines = line_index - prev
        sections = floor(sqrt(max(total_lines, 0)))

        color1 = []
        color2 = []

        c2_count = 0
        c1_count = 0
        max_count = 1000
        current_line = 0

        line_count_diff = floor((total_lines - sections**2) / 2)

        stop = False
        for i in range(sections):
            if stop:
                break

            c2_count += 1
            c1_count = sections - c2_count
            rest = c1_count % c2_count
            c1_count = ceil(c1_count / c2_count)

            current_line, line_count_diff, color1, color2, max_count, stop = _add_lines(
                current_line,
                total_lines,
                line_count_diff,
                color1,
                color2,
                stop,
                rest,
                c1_count,
                c2_count,
                max_count
            )

        if not color1 or not color2:
            continue

        # mirror the first half of the color section to receive the full section
        second_half = color2[-1] * 2 + 1

        color1 = np.array(color1)
        color2 = np.array(color2)

        c1 = np.append(color1, second_half - color2)
        color2 = np.append(color2, second_half - color1)
        color1 = c1

        # until now we only cared about the length of the section
        # now we need to move it to the correct position
        color1 += prev
        color2 += prev

        # add lines to their color key in the dictionary
        # as sections can start before or after the actual shape we need to make sure,
        # that we only try to add existing lines
        color_lines[prev_color].extend([lines[x] for x in color1 if 0 < x < len(lines)])
        color_lines[color].extend([lines[x] for x in color2 if 0 < x < len(lines)])

        prev = np.max(color2)
        prev_color = color

        check_stop_flag()

    # add left over lines to last color
    color_lines[color].extend(lines[prev+1:])

    # remove transparent colors (we just want a gap)
    color_lines.pop('none', None)

    # remove empty line lists and update colors
    color_lines = {color: lines for color, lines in color_lines.items() if lines}
    colors = list(color_lines.keys())

    return color_lines, colors


def _add_lines(current_line, total_lines, line_count_diff, color1, color2, stop, rest, c1_count, c2_count, max_count):
    for j in range(c2_count):
        if stop:
            break

        if rest == 0 or j < rest:
            count = c1_count
        else:
            count = c1_count - 1
        if line_count_diff > 0:
            count += 1
            line_count_diff -= 1
        count = min(count, max_count)

        for k in range(count):
            color1.append(current_line)
            current_line += 1
            if total_lines / 2 <= current_line + 1:
                stop = True
                break
        color2.append(current_line)
        current_line += 1
    max_count = count
    return current_line, line_count_diff, color1, color2, max_count, stop


def _get_stitch_groups(fill, shape, colors, color_lines, starting_point, ending_point):
    stitch_groups = []
    for i, color in enumerate(colors):
        lines = color_lines[color]

        multiline = ensure_multi_line_string(MultiLineString(lines).intersection(shape))
        if multiline.is_empty:
            continue

        segments = [list(line.coords) for line in multiline.geoms if len(line.coords) > 1]
        fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

        if is_empty(fill_stitch_graph):
            continue
        graph_make_valid(fill_stitch_graph)

        travel_graph = build_travel_graph(fill_stitch_graph, shape, fill.angle, False)
        path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, False)
        stitches = path_to_stitches(
            shape,
            path,
            travel_graph,
            fill_stitch_graph,
            fill.running_stitch_length,
            fill.running_stitch_tolerance,
            fill.skip_last,
            False  # no underpath
        )

        stitches = remove_start_end_travel(fill, stitches, colors, i)

        stitch_groups.append(StitchGroup(
            color=color,
            tags=("linear_gradient_fill", "auto_fill_top"),
            stitches=stitches,
            force_lock_stitches=fill.force_lock_stitches,
            lock_stitches=fill.lock_stitches,
            trim_after=fill.has_command("trim") or fill.trim_after
        ))

    return stitch_groups


def remove_start_end_travel(fill, stitches, colors, color_section):
    # We can savely remove travel stitches at start since we are changing color all the time
    # but we do care for the first starting point, it is important when they use an underlay of the same color
    remove_before = 0
    if color_section > 0 or not fill.fill_underlay:
        for stitch in range(len(stitches)-1):
            if 'auto_fill_travel' not in stitches[stitch].tags:
                remove_before = stitch
                break
        stitches = stitches[remove_before:]
    remove_after = len(stitches) - 1
    # We also remove travel stitches at the end. It is optional to the user if the last color block travels
    # to the defined ending point
    if color_section < len(colors) - 2 or not fill.stop_at_ending_point:
        for stitch in range(remove_after, 0, -1):
            if 'auto_fill_travel' not in stitches[stitch].tags:
                remove_after = stitch + 1
                break
        stitches = stitches[:remove_after]
    return stitches


def gradient_start_end(node, gradient):
    transform = Transform(get_node_transform(node))
    gradient_start = transform.apply_to_point((float(gradient.x1()), float(gradient.y1())))
    gradient_end = transform.apply_to_point((float(gradient.x2()), float(gradient.y2())))
    return gradient_start, gradient_end


def gradient_angle(node, gradient):
    if gradient is None:
        return
    gradient_start, gradient_end = gradient_start_end(node, gradient)
    gradient_line = DirectedLineSegment(gradient_start, gradient_end)
    return gradient_line.angle
