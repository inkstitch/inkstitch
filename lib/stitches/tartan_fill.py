# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict
from itertools import chain
from math import cos, radians, sin

from networkx import is_empty
from shapely import get_point, line_merge, minimum_bounding_radius, segmentize
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, MultiLineString

from ..stitch_plan import StitchGroup
from ..svg import PIXELS_PER_MM
from ..tartan.utils import (get_pallet_width, get_tartan_settings,
                            get_tartan_stripes, sort_fills_and_strokes,
                            stripes_to_shapes)
from ..utils import cache, ensure_multi_line_string
from ..utils.threading import check_stop_flag
from .auto_fill import (build_fill_stitch_graph, build_travel_graph,
                        find_stitch_path, graph_make_valid)
from .circular_fill import path_to_stitches
from .guided_fill import apply_stitches
from .linear_gradient_fill import remove_start_end_travel
from .running_stitch import bean_stitch


def tartan_fill(fill, outline, starting_point, ending_point):
    tartan_settings = get_tartan_settings(fill.node)
    warp, weft = get_tartan_stripes(tartan_settings)
    warp_width = get_pallet_width(tartan_settings)
    weft_width = get_pallet_width(tartan_settings, 1)

    offset = (abs(tartan_settings['offset_x']), abs(tartan_settings['offset_y']))
    rotation = tartan_settings['rotate']
    dimensions = _get_dimensions(fill, outline, rotation, offset, warp_width, weft_width)
    rotation_center = _get_rotation_center(outline)

    warp = stripes_to_shapes(
        warp,
        dimensions,
        outline,
        rotation,
        rotation_center,
        tartan_settings['symmetry'],
        tartan_settings['scale'],
        tartan_settings['min_stripe_width'],
        False,  # weft
        False  # do not cut polygons just yet
    )

    weft = stripes_to_shapes(
        weft,
        dimensions,
        outline,
        rotation,
        rotation_center,
        tartan_settings['symmetry'],
        tartan_settings['scale'],
        tartan_settings['min_stripe_width'],
        True,  # weft
        False  # do not cut polygons just yet
    )

    if fill.herringbone_width > 0:
        lines = _generate_herringbone_lines(outline, fill, dimensions, rotation, offset)
        warp_lines, weft_lines = _split_herringbone_warp_weft(lines, fill.rows_per_thread)
        warp_color_lines = _get_herringbone_color_segments(warp_lines, warp, outline, rotation, rotation_center, fill.running_stitch_length)
        weft_color_lines = _get_herringbone_color_segments(weft_lines, weft, outline, rotation, rotation_center, fill.running_stitch_length, True)
    else:
        lines = _generate_tartan_lines(outline, fill, dimensions, rotation, offset)
        warp_lines, weft_lines = _split_warp_weft(lines, fill.rows_per_thread)
        warp_color_lines = _get_tartan_color_segments(warp_lines, warp, outline, rotation, rotation_center, fill.running_stitch_length)
        weft_color_lines = _get_tartan_color_segments(weft_lines, weft, outline, rotation, rotation_center, fill.running_stitch_length, True)
    if not lines:
        return []

    warp_color_runs = _get_color_runs(warp, fill.running_stitch_length)
    weft_color_runs = _get_color_runs(weft, fill.max_stitch_length)

    color_lines = defaultdict(list)
    for color, lines in chain(warp_color_lines.items(), weft_color_lines.items()):
        color_lines[color].extend(lines)

    color_runs = defaultdict(list)
    for color, lines in chain(warp_color_runs.items(), weft_color_runs.items()):
        color_runs[color].extend(lines)

    color_lines, color_runs = sort_fills_and_strokes(color_lines, color_runs)

    stitch_groups = _get_fill_stitch_groups(fill, outline, color_lines, starting_point, ending_point)
    if stitch_groups:
        starting_point = stitch_groups[-1].stitches[-1]
    stitch_groups += _get_run_stitch_groups(fill, outline, color_runs, starting_point, ending_point)
    return stitch_groups


def _generate_herringbone_lines(outline, fill, dimensions, rotation, offset):
    rotation_center = _get_rotation_center(outline)
    minx, miny, maxx, maxy = dimensions

    herringbone_lines = [[], []]
    odd = True
    while minx < maxx:
        odd = not odd
        right = minx + fill.herringbone_width
        if odd:
            left_line = LineString([(minx, miny), (minx, maxy + fill.herringbone_width)])
        else:
            left_line = LineString([(minx, miny - fill.herringbone_width), (minx, maxy)])

        if odd:
            right_line = LineString([(right, miny - fill.herringbone_width), (right, maxy)])
        else:
            right_line = LineString([(right, miny), (right, maxy + fill.herringbone_width)])

        left_line = segmentize(left_line, max_segment_length=fill.row_spacing)
        right_line = segmentize(right_line, max_segment_length=fill.row_spacing)

        lines = list(zip(left_line.coords, right_line.coords))

        staggered_lines = []
        for i, line in enumerate(lines):
            line = LineString(line)
            staggered_line = apply_stitches(line, fill.max_stitch_length, fill.staggers, fill.row_spacing, i)
            # make sure we do not ommit the very first or very last point (it would confuse our sorting algorithm)
            staggered_line = LineString([line.coords[0]] + list(staggered_line.coords) + [line.coords[-1]])
            staggered_lines.append(staggered_line)

        if odd:
            herringbone_lines[0].append(list(rotate(MultiLineString(staggered_lines), rotation, rotation_center).geoms))
        else:
            herringbone_lines[1].append(list(rotate(MultiLineString(staggered_lines), rotation, rotation_center).geoms))

        # add some little space extra to make things easier with line_merge later on
        # (avoid spots with 4 line points)
        minx += fill.herringbone_width + 0.005

    return herringbone_lines


def _generate_tartan_lines(outline, fill, dimensions, rotation, offset):
    rotation_center = _get_rotation_center(outline)
    # default angle is 45°
    rotation += fill.tartan_angle
    minx, miny, maxx, maxy = dimensions

    left_line = LineString([(minx, miny), (minx, maxy)])
    left_line = rotate(left_line, rotation, rotation_center)
    left_line = segmentize(left_line, max_segment_length=fill.row_spacing)

    right_line = LineString([(maxx, miny), (maxx, maxy)])
    right_line = rotate(right_line, rotation, rotation_center)
    right_line = segmentize(right_line, max_segment_length=fill.row_spacing)

    lines = list(zip(left_line.coords, right_line.coords))

    staggered_lines = []
    for i, line in enumerate(lines):
        line = LineString(line)
        staggered_line = apply_stitches(line, fill.max_stitch_length, fill.staggers, fill.row_spacing, i)
        # make sure we do not ommit the very first or very last point (it would confuse our sorting algorithm)
        staggered_line = LineString([line.coords[0]] + list(staggered_line.coords) + [line.coords[-1]])
        staggered_lines.append(staggered_line)
    return staggered_lines


def _split_herringbone_warp_weft(lines, rows_per_thread):
    warp_lines = []
    weft_lines = []
    for i, line_blocks in enumerate(lines):
        for line_block in line_blocks:
            if i == 0:
                warp, weft = _split_warp_weft(line_block, rows_per_thread)
            else:
                weft, warp = _split_warp_weft(line_block, rows_per_thread)
            warp_lines.append(warp)
            weft_lines.append(weft)

    connected_weft = []
    for multilinestring in weft_lines:
        connected_line_block = []
        geoms = list(multilinestring.geoms)
        for line1, line2 in zip(geoms[:-1], geoms[1:]):
            connected_line_block.append(line1)
            connected_line_block.append(LineString([get_point(line1, -1), get_point(line2, 0)]))
        connected_line_block.append(line2)
        connected_weft.append(ensure_multi_line_string(line_merge(MultiLineString(connected_line_block))))
    return warp_lines, connected_weft


def _split_warp_weft(lines, rows_per_thread):
    warp_lines = []
    weft_lines = []
    for i in range(rows_per_thread):
        warp_lines.extend(lines[i::rows_per_thread*2])
        weft_lines.extend(lines[i+rows_per_thread::rows_per_thread*2])
    return _sort_lines(warp_lines), _sort_lines(weft_lines)


def _sort_lines(lines):
    # sort lines and reverse every second line
    lines.sort(key=lambda line: line.coords[0])
    # projection_line = scale(rotate(lines[0], 90), 2, 2)
    # lines.sort(key=lambda line: projection_line.project(line.intersection(projection_line)))
    lines = [line if i % 2 == 0 else line.reverse() for i, line in enumerate(lines)]
    return MultiLineString(lines)


@cache
def _get_rotation_center(outline):
    # somehow outline.centroid doesn't deliver the point we need
    bounds = outline.bounds
    return LineString([(bounds[0], bounds[1]), (bounds[2], bounds[3])]).centroid


@cache
def _get_dimensions(fill, outline, rotation, offset, warp_width, weft_width):
    # add space to allow rotation and herringbone patterns to cover the shape
    centroid = _get_rotation_center(outline)
    min_radius = minimum_bounding_radius(outline)
    minx = centroid.x - min_radius
    miny = centroid.y - min_radius
    maxx = centroid.x + min_radius
    maxy = centroid.y + min_radius

    # add some extra space
    extra_space = max(warp_width, weft_width, 2 * fill.row_spacing * fill.rows_per_thread)
    minx -= extra_space
    maxx += extra_space
    miny -= extra_space
    maxy += extra_space

    minx -= (offset[0] * PIXELS_PER_MM)
    miny -= (offset[1] * PIXELS_PER_MM)

    return minx, miny, maxx, maxy


def _get_herringbone_color_segments(lines, polygons, outline, rotation, rotation_center, stitch_length, weft=False):
    line_segments = defaultdict(list)
    # if not weft:
    #    return line_segments

    if not polygons:
        return line_segments
    lines = line_merge(lines)
    for line_blocks in lines:
        segments = _get_tartan_color_segments(line_blocks, polygons, outline, rotation, rotation_center, stitch_length, weft, True)
        for color, segment in segments.items():
            if weft:
                line_segments[color].append(MultiLineString(segment))
            else:
                line_segments[color].extend(segment)

    if not weft:
        return line_segments

    return _get_weft_herringbone_color_segments(outline, line_segments, polygons, stitch_length, rotation)


def _get_weft_herringbone_color_segments(outline, line_segments, polygons, stitch_length, rotation):
    weft_lines = defaultdict(list)
    for color, lines in line_segments.items():
        color_lines = []
        for polygon in polygons[color][0]:
            polygon = polygon.normalize()
            polygon_coords = list(polygon.exterior.coords)
            polygon_top = LineString(polygon_coords[0:2])
            polygon_bottom = LineString(polygon_coords[2:4]).reverse()
            if not any([polygon_top.intersects(outline), polygon_bottom.intersects(outline)]):
                polygon_top = LineString(polygon_coords[1:3])
                polygon_bottom = LineString(polygon_coords[3:5]).reverse()

            polygon_multi_lines = lines
            polygon_multi_lines.sort(key=lambda line: polygon_bottom.project(line.centroid))
            polygon_lines = []
            for multiline in polygon_multi_lines:
                polygon_lines.extend(multiline.geoms)
            polygon_lines = [line for line in polygon_lines if line.intersects(polygon)]
            if not polygon_lines:
                continue
            color_lines.extend(polygon_lines)

            if polygon_top.intersects(outline) or polygon_bottom.intersects(outline):
                connectors = _get_weft_herringbone_connectors(polygon_lines, polygon, polygon_top, polygon_bottom, stitch_length)
                if connectors:
                    color_lines.extend(connectors)

            check_stop_flag()

        # Users are likely to type in a herringbone width which is a multiple (or fraction)
        # of the stripe width, avoid a collision by shifting the weft for a random small number
        color_lines = translate(ensure_multi_line_string(line_merge(MultiLineString(color_lines))), 0.00123, 0.00123)
        color_lines = ensure_multi_line_string(color_lines.intersection(outline))

        weft_lines[color].extend(list(color_lines.geoms))

    return weft_lines


def _get_weft_herringbone_connectors(polygon_lines, polygon, polygon_top, polygon_bottom, stitch_length):
    connectors = []
    previous_end = None
    for line in reversed(polygon_lines):
        start = get_point(line, 0)
        end = get_point(line, -1)
        if previous_end is None:
            # adjust direction of polygon lines if necessary
            if polygon_top.project(start, True) > 0.5:
                polygon_top = polygon_top.reverse()
                polygon_bottom = polygon_bottom.reverse()
            start_distance = polygon_top.project(start)
            end_distance = polygon_top.project(end)
            if start_distance > end_distance:
                start, end = end, start
            previous_end = end
            continue

        # adjust line direction and add connectors
        prev_polygon_line = min([polygon_top, polygon_bottom], key=lambda polygon_line: previous_end.distance(polygon_line))
        current_polygon_line = min([polygon_top, polygon_bottom], key=lambda polygon_line: start.distance(polygon_line))
        if prev_polygon_line != current_polygon_line:
            start, end = end, start
        if not previous_end == start:
            connector = LineString([previous_end, start])
            if prev_polygon_line == polygon_top:
                connector = connector.offset_curve(-0.0001)
            else:
                connector = connector.offset_curve(0.0001)
            connectors.append(LineString([previous_end, get_point(connector, 0)]))
            connectors.append(segmentize(connector, max_segment_length=stitch_length))
            connectors.append(LineString([get_point(connector, -1), start]))
        previous_end = end
    return connectors


def _get_tartan_color_segments(lines, polygons, outline, rotation, rotation_center, stitch_length, weft=False, herringbone=False):
    line_segments = defaultdict(list)
    if not polygons:
        return line_segments
    for color, shapes in polygons.items():
        segments = []
        polygons = shapes[0]
        for polygon in polygons:
            segments = _get_segment_lines(polygon, lines, outline, stitch_length, rotation, weft, herringbone)
            if segments:
                line_segments[color].extend(segments)
        check_stop_flag()
    return line_segments


def _get_connector_line(connectors):
    # let's take the shortest line and duplicate it
    connectors.sort(key=lambda connector: connector.length)
    # translate line just a little bit, so that the fill algorithm will not swallow it
    connector = translate(connectors[0], 0.01).reverse()
    return connector


def _get_color_runs(lines, stitch_length):
    runs = defaultdict(list)
    if not lines:
        return runs
    for color, shapes in lines.items():
        for run in shapes[1]:
            runs[color].append(segmentize(run, max_segment_length=stitch_length))
    return runs


def _get_segment_lines(polygon, lines, outline, stitch_length, rotation, weft, herringbone):
    boundary = outline.boundary
    segments = []
    if not lines.intersects(polygon):
        return []
    segment_lines = list(ensure_multi_line_string(lines.intersection(polygon), 0.5).geoms)
    if not segment_lines:
        return []
    previous_line = None
    for line in segment_lines:
        segments.append(line)
        if not previous_line:
            previous_line = line
            continue
        point1 = get_point(previous_line, -1)
        point2 = get_point(line, 0)
        if point1.equals(point2):
            previous_line = line
            continue
        # add connector from point1 to point2 if none of them touches the outline
        connector = _get_connector(point1, point2, boundary, stitch_length)
        if connector:
            segments.append(connector)
        previous_line = line

    if not segments:
        return []
    lines = line_merge(MultiLineString(segments))

    if not (herringbone and weft):
        lines = lines.intersection(outline)

    if not herringbone:
        lines = _connect_lines_to_outline(lines, outline, rotation, stitch_length, weft)

    return list(ensure_multi_line_string(lines).geoms)


def _connect_lines_to_outline(lines, outline, rotation, stitch_length, weft):
    ''' connects end points within the shape with the outline (should only be necessary if the tartan
        angle is nearly 0 or 90 degrees'''
    boundary = outline.boundary
    lines = list(ensure_multi_line_string(lines).geoms)
    outline_connectors = []
    for line in lines:
        start = get_point(line, 0)
        end = get_point(line, -1)
        if start.intersects(outline) and start.distance(boundary) > 0.05:
            outline_connectors.append(_connect_point_to_outline(start, outline, rotation, stitch_length, weft))
        if end.intersects(outline) and end.distance(boundary) > 0.05:
            outline_connectors.append(_connect_point_to_outline(end, outline, rotation, stitch_length, weft))
    lines.extend(outline_connectors)
    lines = line_merge(MultiLineString(lines))
    return lines


def _connect_point_to_outline(point, outline, rotation, stitch_length, weft):
    from shapely.ops import nearest_points
    scale_factor = point.hausdorff_distance(outline) * 2
    directional_vector = _get_angled_line_from_point(point, rotation, scale_factor, weft)
    directional_vector = outline.boundary.intersection(directional_vector)
    if directional_vector.is_empty:
        return []
    return segmentize(LineString([point, nearest_points(directional_vector, point)[0]]), max_segment_length=stitch_length)


def _get_angled_line_from_point(point, rotation, scale_factor, weft):
    if not weft:
        rotation += 90
    rotation = radians(rotation)
    x = point.coords[0][0] + cos(rotation)
    y = point.coords[0][1] + sin(rotation)
    return scale(LineString([point, (x, y)]), scale_factor, scale_factor)


def _get_connector(point1, point2, boundary, stitch_length):
    connector = None
    if (point1.distance(boundary) > 0.005 and point2.distance(boundary) > 0.005):
        connector = segmentize(LineString([point1, point2]), max_segment_length=stitch_length)
    return connector


def _get_fill_stitch_groups(fill, shape, color_lines, starting_point, ending_point):
    stitch_groups = []
    i = 0
    for color, lines in color_lines.items():
        i += 1
        if stitch_groups:
            starting_point = stitch_groups[-1].stitches[-1]
        else:
            starting_point = ensure_multi_line_string(shape.boundary).geoms[0].coords[0]
        ending_point = ensure_multi_line_string(shape.boundary).geoms[0].coords[0]
        segments = [list(line.coords) for line in lines if len(line.coords) > 1]
        stitch_groups.append(_segments_to_stitch_group(fill, shape, segments, i, color, starting_point, ending_point))
        check_stop_flag()
    return stitch_groups


def _get_run_stitch_groups(fill, shape, color_lines, starting_point, ending_point):
    stitch_groups = []
    for color, lines in color_lines.items():
        segments = [list(line.coords) for line in lines if len(line.coords) > 1]
        stitch_groups.append(_segments_to_stitch_group(fill, shape, segments, None, color, starting_point, ending_point, True))
        check_stop_flag()
    return stitch_groups


def _segments_to_stitch_group(fill, shape, segments, iteration, color, starting_point, ending_point, runs=False):
    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    if is_empty(fill_stitch_graph):
        return []
    graph_make_valid(fill_stitch_graph)
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

    if iteration:
        stitches = remove_start_end_travel(fill, stitches, color, iteration)

    if runs:
        stitches = bean_stitch(stitches, fill.bean_stitch_repeats, ['auto_fill_travel'])

    stitch_group = StitchGroup(
        color=color,
        tags=("tartan_fill", "auto_fill_top"),
        stitches=stitches,
        force_lock_stitches=fill.force_lock_stitches,
        lock_stitches=fill.lock_stitches,
        trim_after=fill.has_command("trim") or fill.trim_after
    )

    if runs:
        stitch_group.add_tag("tartan_run")

    return stitch_group
