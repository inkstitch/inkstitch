# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil, floor, sqrt

import numpy as np
from inkex import DirectedLineSegment, Transform
from shapely import segmentize
from shapely.affinity import rotate
from shapely.geometry import LineString, MultiLineString, Point, Polygon

from ..stitch_plan import StitchGroup
from ..svg import get_node_transform
from ..utils.threading import check_stop_flag
from .auto_fill import (build_fill_stitch_graph, build_travel_graph,
                        find_stitch_path, graph_is_valid)
from .circular_fill import path_to_stitches
from .guided_fill import apply_stitches


def linear_gradient_fill(fill, shape, starting_point, ending_point):
    colors, lines, line_nums = _get_lines_nums_and_colors(shape, fill)
    color_lines, colors = _get_color_lines(colors, line_nums, lines)
    if fill.gradient is None:
        colors.pop()
    stitch_groups = _get_stitch_groups(fill, shape, colors, color_lines, starting_point, ending_point)
    return stitch_groups


def _get_lines_nums_and_colors(shape, fill):
    # min x, min y, max x, max y
    orig_bbox = shape.bounds

    if fill.gradient is None:
        # there is no linear gradient, let's simply space out one single color instead
        angle = 0
        offsets = [0, 1]
        colors = [fill.color, 'none']
        point1 = (orig_bbox[0], orig_bbox[1])
        point2 = (orig_bbox[2], orig_bbox[3])
    else:
        node = fill.node
        fill.gradient.apply_transform()
        offsets = fill.gradient.stop_offsets
        colors = [style['stop-color'] for style in fill.gradient.stop_styles]
        transform = Transform(get_node_transform(node))
        point1 = transform.apply_to_point((float(fill.gradient.x1()), float(fill.gradient.y1())))
        point2 = transform.apply_to_point((float(fill.gradient.x2()), float(fill.gradient.y2())))

        gradient_line = DirectedLineSegment(point1, point2)
        angle = gradient_line.angle

    rotated_shape = rotate(shape, -angle, origin=(orig_bbox[0], orig_bbox[3]), use_radians=True)
    bounds = rotated_shape.bounds

    # extend bounding box for lines just a little to make sure we cover the whole area with lines
    rot_bbox = Polygon([
        (bounds[0] - fill.max_stitch_length, bounds[1] - fill.row_spacing),
        (bounds[2] + fill.max_stitch_length, bounds[1] - fill.row_spacing),
        (bounds[2] + fill.max_stitch_length, bounds[3] + fill.row_spacing),
        (bounds[0] - fill.max_stitch_length, bounds[3] + fill.row_spacing)
    ])
    rot_bbox = list(rotate(rot_bbox, angle, origin=(orig_bbox[0], orig_bbox[3]), use_radians=True).exterior.coords)

    top_line = LineString([rot_bbox[0], rot_bbox[1]])
    top = segmentize(top_line, max_segment_length=fill.row_spacing)

    bottom_line = LineString([rot_bbox[3], rot_bbox[2]])
    bottom = segmentize(bottom_line, max_segment_length=fill.row_spacing)

    lines = list(zip(top.coords, bottom.coords))
    staggered_lines = []
    for i, line in enumerate(lines):
        staggered_line = apply_stitches(LineString(line), fill.max_stitch_length, fill.staggers, fill.row_spacing, i)
        staggered_lines.append(staggered_line)

    lines = staggered_lines

    gradient_start = round(bottom_line.project(Point(point1)) / fill.row_spacing)
    if gradient_start == 0:
        gradient_start = -round(LineString([point1, point2]).project(Point(rot_bbox[0])) / fill.row_spacing)

    line_nums = [gradient_start]
    gradient_line = LineString([point1, point2])
    for offset in offsets[1:]:
        line_nums.append(round((gradient_line.length * offset) / fill.row_spacing) + gradient_start)

    return colors, lines, line_nums


def _get_color_lines(colors, line_nums, lines):  # noqa: C901
    color_lines = {}
    for color in colors:
        color_lines[color] = []

    prev_color = colors[0]
    prev = None
    for line_num, color in zip(line_nums, colors):
        if prev is None:
            if line_num > 0:
                color_lines[color].extend(lines[0:line_num + 1])
            prev = line_num
            prev_color = color
            continue
        if prev < 0 and line_num < 0:
            prev = line_num
            prev_color = color
            continue

        prev += 1
        line_num += 1
        total_lines = line_num - prev
        sections = floor(sqrt(total_lines))

        color1 = []
        color2 = []

        c2_count = 0
        c1_count = 0
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
                for k in range(count):
                    color1.append(current_line)
                    current_line += 1
                    if total_lines / 2 <= current_line + 1:
                        stop = True
                        break
                color2.append(current_line)
                current_line += 1

        block2_end = color2[-1] * 2 + 1

        color1 = np.array(color1)
        color2 = np.array(color2)

        c1 = np.append(color1, block2_end - color2)
        color2 = np.append(color2, block2_end - color1)
        color1 = c1

        color1 += prev
        color2 += prev

        color_lines[prev_color].extend([lines[x] for x in color1 if 0 < x < len(lines)])
        color_lines[color].extend([lines[x] for x in color2 if 0 < x < len(lines)])

        prev = np.max(color2)
        prev_color = color

        check_stop_flag()

    color_lines[color].extend(lines[prev+1:])

    # remove empty line lists and update colors
    color_lines = {color: lines for color, lines in color_lines.items() if lines}
    colors = list(color_lines.keys())

    return color_lines, colors


def _get_stitch_groups(fill, shape, colors, color_lines, starting_point, ending_point):
    stitch_groups = []
    for i, color in enumerate(colors):
        lines = color_lines[color]

        multiline = MultiLineString(lines).intersection(shape)
        if not isinstance(multiline, MultiLineString):
            continue
        segments = [list(line.coords) for line in multiline.geoms if len(line.coords) > 1]

        fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
        if not graph_is_valid(fill_stitch_graph):
            continue

        travel_graph = build_travel_graph(fill_stitch_graph, shape, fill.angle, False)
        path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
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

        stitches = _remove_start_end_travel(fill, stitches, colors, i)

        stitch_groups.append(StitchGroup(
            color=color,
            tags=("linear_gradient_fill", "auto_fill_top"),
            stitches=stitches,
            force_lock_stitches=fill.force_lock_stitches,
            lock_stitches=fill.lock_stitches,
            trim_after=fill.has_command("trim") or fill.trim_after
        ))

    return stitch_groups


def _remove_start_end_travel(fill, stitches, colors, color_section):
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
