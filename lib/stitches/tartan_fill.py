# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# This file needs some more love before it'll pass type checking.
# mypy: ignore-errors=true

from collections import defaultdict
from itertools import chain
from math import cos, radians, sin
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from networkx import is_empty
from shapely import get_point, line_merge, minimum_bounding_radius, segmentize
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, MultiLineString, Point, Polygon
from shapely.ops import nearest_points

from ..stitch_plan import Stitch, StitchGroup
from ..svg import PIXELS_PER_MM
from ..tartan.utils import (get_palette_width, get_tartan_settings,
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

if TYPE_CHECKING:
    from ..elements import FillStitch


def tartan_fill(fill: 'FillStitch', outline: Polygon, starting_point: Union[tuple, Stitch, None], ending_point: Union[tuple, Stitch, None]):
    """
    Main method to fill the tartan element with tartan fill stitches

    :param fill: FillStitch element
    :param outline: the outline of the fill
    :param starting_point: the starting point (or None)
    :param ending_point: the ending point (or None)
    :returns: stitch_groups forming the tartan pattern
    """
    tartan_settings = get_tartan_settings(fill.node)
    warp, weft = get_tartan_stripes(tartan_settings)
    warp_width = get_palette_width(tartan_settings)
    weft_width = get_palette_width(tartan_settings, 1)

    offset = (abs(tartan_settings['offset_x']), abs(tartan_settings['offset_y']))
    rotation = tartan_settings['rotate']
    dimensions = _get_dimensions(fill, outline, offset, warp_width, weft_width)
    rotation_center = _get_rotation_center(outline)

    warp_shapes = stripes_to_shapes(
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

    weft_shapes = stripes_to_shapes(
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
        lines = _generate_herringbone_lines(outline, fill, dimensions, rotation)
        warp_lines, weft_lines = _split_herringbone_warp_weft(lines, fill.rows_per_thread, fill.running_stitch_length)
        warp_color_lines = _get_herringbone_color_segments(warp_lines, warp_shapes, outline, rotation, fill.running_stitch_length)
        weft_color_lines = _get_herringbone_color_segments(weft_lines, weft_shapes, outline, rotation, fill.running_stitch_length, True)
    else:
        lines = _generate_tartan_lines(outline, fill, dimensions, rotation)
        warp_lines, weft_lines = _split_warp_weft(lines, fill.rows_per_thread)
        warp_color_lines = _get_tartan_color_segments(warp_lines, warp_shapes, outline, rotation, fill.running_stitch_length)
        weft_color_lines = _get_tartan_color_segments(weft_lines, weft_shapes, outline, rotation, fill.running_stitch_length, True)
    if not lines:
        return []

    warp_color_runs = _get_color_runs(warp_shapes, fill.running_stitch_length)
    weft_color_runs = _get_color_runs(weft_shapes, fill.max_stitch_length)

    color_lines = defaultdict(list)
    for color, lines in chain(warp_color_lines.items(), weft_color_lines.items()):
        color_lines[color].extend(lines)

    color_runs = defaultdict(list)
    for color, lines in chain(warp_color_runs.items(), weft_color_runs.items()):
        color_runs[color].extend(lines)

    color_lines, color_runs = sort_fills_and_strokes(color_lines, color_runs)

    stitch_groups = _get_fill_stitch_groups(fill, outline, color_lines, starting_point, ending_point)
    if stitch_groups and not fill.stop_at_ending_point:
        starting_point = stitch_groups[-1].stitches[-1]
    stitch_groups += _get_run_stitch_groups(fill, outline, color_runs, starting_point, ending_point)
    return stitch_groups


def _generate_herringbone_lines(
    outline: Polygon,
    fill: 'FillStitch',
    dimensions: Tuple[float, float, float, float],
    rotation: float,
) -> List[List[List[LineString]]]:
    """
    Generates herringbone lines with staggered stitch positions

    :param outline: the outline to fill with the herringbone lines
    :param fill: the tartan fill element
    :param dimensions: minx, miny, maxx, maxy
    :param rotation: the rotation value
    :returns: a tuple of two list with herringbone stripes [0] up segments / [1] down segments \
    """
    rotation_center = _get_rotation_center(outline)
    minx, miny, maxx, maxy = dimensions

    herringbone_lines: list = [[], []]
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
            linestring = LineString(line)
            staggered_line = apply_stitches(linestring, [fill.max_stitch_length], fill.staggers, fill.row_spacing, i)
            # make sure we do not ommit the very first or very last point (it would confuse our sorting algorithm)
            staggered_line = LineString([linestring.coords[0]] + list(staggered_line.coords) + [linestring.coords[-1]])
            staggered_lines.append(staggered_line)

        if odd:
            herringbone_lines[0].append(list(rotate(MultiLineString(staggered_lines), rotation, rotation_center).geoms))
        else:
            herringbone_lines[1].append(list(rotate(MultiLineString(staggered_lines), rotation, rotation_center).geoms))

        # add some little space extra to make things easier with line_merge later on
        # (avoid spots with 4 line points)
        minx += fill.herringbone_width + 0.005

    return herringbone_lines


def _generate_tartan_lines(
    outline: Polygon,
    fill: 'FillStitch',
    dimensions: Tuple[float, float, float, float],
    rotation: float,
) -> List[LineString]:
    """
    Generates tartan lines with staggered stitch positions

    :param outline: the outline to fill with the herringbone lines
    :param fill: the tartan fill element
    :param dimensions: minx, miny, maxx, maxy
    :param rotation: the rotation value
    :returns: a list with the tartan lines
    """
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
        linestring = LineString(line)
        staggered_line = apply_stitches(linestring, [fill.max_stitch_length], fill.staggers, fill.row_spacing, i)
        # make sure we do not ommit the very first or very last point (it would confuse our sorting algorithm)
        staggered_line = LineString([linestring.coords[0]] + list(staggered_line.coords) + [linestring.coords[-1]])
        staggered_lines.append(staggered_line)
    return staggered_lines


def _split_herringbone_warp_weft(
    lines: List[List[List[LineString]]],
    rows_per_thread: int,
    stitch_length: float
) -> tuple:
    """
    Split the herringbone lines into warp lines and weft lines as defined by rows rows_per_thread
    Merge weft lines for each block.

    :param lines: lines to divide
    :param rows_per_thread: length of line blocks
    :param stitch_length: maximum stitch length for weft connector lines
    :returns: [0] warp and [1] weft list of MultiLineString objects
    """
    warp_lines: List[LineString] = []
    weft_lines: List[LineString] = []
    for i, line_blocks in enumerate(lines):
        for line_block in line_blocks:
            if i == 0:
                warp, weft = _split_warp_weft(line_block, rows_per_thread)
            else:
                weft, warp = _split_warp_weft(line_block, rows_per_thread)
            warp_lines.append(warp)
            weft_lines.append(weft)

    connected_weft = []
    line2 = None
    for multilinestring in weft_lines:
        connected_line_block = []
        geoms = list(multilinestring.geoms)
        for line1, line2 in zip(geoms[:-1], geoms[1:]):
            connected_line_block.append(line1)
            connector_line = LineString([get_point(line1, -1), get_point(line2, 0)])
            connector_line = segmentize(connector_line, max_segment_length=stitch_length)
            connected_line_block.append(connector_line)
        if line2:
            connected_line_block.append(line2)
        connected_weft.append(ensure_multi_line_string(line_merge(MultiLineString(connected_line_block))))
    return warp_lines, connected_weft


def _split_warp_weft(lines: List[LineString], rows_per_thread: int) -> Tuple[List[LineString], List[LineString]]:
    """
    Divide given lines in warp and weft, sort afterwards

    :param lines: a list of LineString shapes
    :param rows_per_thread: length of line blocks
    :returns: tuple with sorted [0] warp and [1] weft LineString shapes
    """
    warp_lines = []
    weft_lines = []
    for i in range(rows_per_thread):
        warp_lines.extend(lines[i::rows_per_thread*2])
        weft_lines.extend(lines[i+rows_per_thread::rows_per_thread*2])
    return _sort_lines(warp_lines), _sort_lines(weft_lines)


def _sort_lines(lines: List[LineString]):
    """
    Sort given list of LineString shapes by first coordinate
    and reverse every second line

    :param lines: a list of LineString shapes
    :returns: sorted list of LineString shapes with alternating directions
    """
    # sort lines
    lines.sort(key=lambda line: line.coords[0])
    # reverse every second line
    lines = [line if i % 2 == 0 else line.reverse() for i, line in enumerate(lines)]
    return MultiLineString(lines)


@cache
def _get_rotation_center(outline: Polygon) -> Point:
    """
    Returns the rotation center used for any tartan pattern rotation

    :param outline: the polygon shape to be filled with the pattern
    :returns: the center point of the shape
    """
    # somehow outline.centroid doesn't deliver the point we need
    bounds = outline.bounds
    return LineString([(bounds[0], bounds[1]), (bounds[2], bounds[3])]).centroid


@cache
def _get_dimensions(
    fill: 'FillStitch',
    outline: Polygon,
    offset: Tuple[float, float],
    warp_width: float,
    weft_width: float
) -> Tuple[float, float, float, float]:
    """
    Calculates the dimensions for the tartan pattern.
    Make sure it is big enough for pattern rotations, etc.

    :param fill: the FillStitch element
    :param outline: the shape to be filled with a tartan pattern
    :param offset: mm offset for x, y
    :param warp_width: mm warp width
    :param weft_width: mm weft width
    :returns: a tuple with boundaries (minx, miny, maxx, maxy)
    """
    # add space to allow rotation and herringbone patterns to cover the shape
    centroid = _get_rotation_center(outline)
    min_radius = minimum_bounding_radius(outline)
    minx = centroid.x - min_radius
    miny = centroid.y - min_radius
    maxx = centroid.x + min_radius
    maxy = centroid.y + min_radius

    # add some extra space
    extra_space = max(
        warp_width * PIXELS_PER_MM,
        weft_width * PIXELS_PER_MM,
        2 * fill.row_spacing * fill.rows_per_thread
    )
    minx -= extra_space
    maxx += extra_space
    miny -= extra_space
    maxy += extra_space

    minx -= (offset[0] * PIXELS_PER_MM)
    miny -= (offset[1] * PIXELS_PER_MM)

    return minx, miny, maxx, maxy


def _get_herringbone_color_segments(
    lines: List[MultiLineString],
    polygons: defaultdict,
    outline: Polygon,
    rotation: float,
    stitch_length: float,
    weft: bool = False
) -> defaultdict:
    """
    Generate herringbone line segments in given tartan direction grouped by color

    :param lines: the line segments forming the pattern
    :param polygons: color grouped polygon stripes
    :param outline: the outline to be filled with the herringbone pattern
    :param rotation: degrees used for rotation
    :param stitch_length: maximum stitch length for weft connector lines
    :param weft: wether to render as warp or weft
    :returns: defaultdict with color grouped herringbone segments
    """
    line_segments: defaultdict = defaultdict(list)

    if not polygons:
        return line_segments

    lines = line_merge(lines)
    for line_blocks in lines:
        segments = _get_tartan_color_segments(line_blocks, polygons, outline, rotation, stitch_length, weft, True)
        for color, segment in segments.items():
            if weft:
                line_segments[color].append(MultiLineString(segment))
            else:
                line_segments[color].extend(segment)

    if not weft:
        return line_segments

    return _get_weft_herringbone_color_segments(outline, line_segments, polygons, stitch_length)


def _get_weft_herringbone_color_segments(
    outline: Polygon,
    line_segments: defaultdict,
    polygons: defaultdict,
    stitch_length: float,
) -> defaultdict:
    """
    Makes sure weft herringbone lines connect correctly

    Herringbone weft lines need to connect in horizontal direction (or whatever the current rotation is)
    which is opposed to the herringbone stripe blocks \\\\ //// \\\\ //// \\\\ ////

    :param outline: the outline to be filled with the herringbone pattern
    :param line_segments: the line segments forming the pattern
    :param polygons: color grouped polygon stripes
    :param stitch_length: maximum stitch length
    :returns: defaultdict with color grouped weft lines
    """
    weft_lines = defaultdict(list)
    for color, lines in line_segments.items():
        color_lines: List[LineString] = []
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
                connectors = _get_weft_herringbone_connectors(polygon_lines, polygon_top, polygon_bottom, stitch_length)
                if connectors:
                    color_lines.extend(connectors)

            check_stop_flag()

        # Users are likely to type in a herringbone width which is a multiple (or fraction) of the stripe width.
        # They may end up unconnected after line_merge, so we need to shift the weft for a random small number
        multi_lines = translate(ensure_multi_line_string(line_merge(MultiLineString(color_lines))), 0.00123, 0.00123)
        multi_lines = ensure_multi_line_string(multi_lines.intersection(outline))

        weft_lines[color].extend(list(multi_lines.geoms))

    return weft_lines


def _get_weft_herringbone_connectors(
    polygon_lines: List[LineString],
    polygon_top: LineString,
    polygon_bottom: LineString,
    stitch_length: float
) -> List[LineString]:
    """
    Generates lines to connect lines

    :param polygon_lines: lines to connect
    :param polygon_top: top line of the polygon
    :param polygon_bottom: bottom line of the polygon
    :param stitch_length: stitch length
    :returns: a list of LineString connectors
    """
    connectors: List[LineString] = []
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


def _get_tartan_color_segments(
    lines: List[LineString],
    polygons: defaultdict,
    outline: Polygon,
    rotation: float,
    stitch_length: float,
    weft: bool = False,
    herringbone: bool = False
) -> defaultdict:
    """
    Generate tartan line segments in given tartan direction grouped by color

    :param lines: the lines to form the tartan pattern with
    :param polygons: color grouped polygon stripes
    :param outline: the outline to fill with the tartan pattern
    :param rotation: rotation in degrees
    :param stitch_length: maximum stitch length for weft connector lines
    :param weft: wether to render as warp or weft
    :param herringbone: wether herringbone or normal tartan patterns are rendered
    :returns: a dictionary with color grouped line segments
    """
    line_segments: defaultdict = defaultdict(list)
    if not polygons:
        return line_segments
    for color, shapes in polygons.items():
        polygons = shapes[0]
        for polygon in polygons:
            segments = _get_segment_lines(polygon, lines, outline, stitch_length, rotation, weft, herringbone)
            if segments:
                line_segments[color].extend(segments)
        check_stop_flag()
    return line_segments


def _get_color_runs(lines: defaultdict, stitch_length: float) -> defaultdict:
    """
    Segmentize running stitch segments and return in a separate color grouped dictionary

    :param lines: tartan shapes grouped by color
    :param stitch_length: stitch length used to segmentize the lines
    :returns: defaultdict with segmentized running stitches grouped by color
    """
    runs: defaultdict = defaultdict(list)
    if not lines:
        return runs
    for color, shapes in lines.items():
        for run in shapes[1]:
            runs[color].append(segmentize(run, max_segment_length=stitch_length))
    return runs


def _get_segment_lines(
    polygon: Polygon,
    lines: MultiLineString,
    outline: Polygon,
    stitch_length: float,
    rotation: float,
    weft: bool,
    herringbone: bool
) -> List[LineString]:
    """
    Fill the given polygon with lines
    Each line should start and end at the outline border

    :param polygon: the polygon stripe to fill
    :param lines: the lines that form the pattern
    :param outline: the outline to fill with the tartan pattern
    :param stitch_length: maximum stitch length for weft connector lines
    :param rotation: rotation in degrees
    :param weft: wether to render as warp or weft
    :param herringbone: wether herringbone or normal tartan patterns are rendered
    :returns: a list of LineString objects
    """
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


def _get_connector(
    point1: Point,
    point2: Point,
    boundary: Union[MultiLineString, LineString],
    stitch_length: float
) -> Optional[LineString]:
    """
    Constructs a line between the two points when they are not near the boundary

    :param point1: first point
    :param point2: last point
    :param boundary: the outline of the shape (including holes)
    :param stitch_length: maximum stitch length to segmentize new line
    :returns: a LineString between point1 and point1, None if one of them touches the boundary
    """
    connector = None
    if point1.distance(boundary) > 0.005 and point2.distance(boundary) > 0.005:
        connector = segmentize(LineString([point1, point2]), max_segment_length=stitch_length)
    return connector


def _connect_lines_to_outline(
    lines: Union[MultiLineString, LineString],
    outline: Polygon,
    rotation: float,
    stitch_length: float,
    weft: bool
) -> Union[MultiLineString, LineString]:
    """
    Connects end points within the shape with the outline
    This should only be necessary if the tartan angle is nearly 0 or 90 degrees

    :param lines: lines to connect to the outline (if necessary)
    :param outline: the shape to be filled with a tartan pattern
    :param rotation: the rotation value
    :param stitch_length: maximum stitch length to segmentize new line
    :param weft: wether to render as warp or weft
    :returns: merged line(s) connected to the outline
    """
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


def _connect_point_to_outline(
    point: Point,
    outline: Polygon,
    rotation: float,
    stitch_length: float,
    weft: bool
) -> Union[LineString, list]:
    """
    Connect given point to the outline

    :param outline: the shape to be filled with a tartan pattern
    :param rotation: the rotation value
    :param stitch_length: maximum stitch length to segmentize new line
    :param weft: wether to render as warp or weft
    :returns: a Linestring with the correct angle for the given tartan direction (between outline and point)
    """
    scale_factor = point.hausdorff_distance(outline) * 2
    directional_vector = _get_angled_line_from_point(point, rotation, scale_factor, weft)
    directional_vector = outline.boundary.intersection(directional_vector)
    if directional_vector.is_empty:
        return []
    return segmentize(LineString([point, nearest_points(directional_vector, point)[0]]), max_segment_length=stitch_length)


def _get_angled_line_from_point(point: Point, rotation: float, scale_factor: float, weft: bool) -> LineString:
    """
    Generates an angled line for the given tartan direction

    :param point: the starting point for the new line
    :param rotation: the rotation value
    :param scale_factor: defines the length of the line
    :param weft: wether to render as warp or weft
    :returns: a LineString
    """
    if not weft:
        rotation += 90
    rotation = radians(rotation)
    x = point.coords[0][0] + cos(rotation)
    y = point.coords[0][1] + sin(rotation)
    return scale(LineString([point, (x, y)]), scale_factor, scale_factor)


def _get_fill_stitch_groups(
    fill: 'FillStitch',
    shape: Polygon,
    color_lines: defaultdict,
    starting_point: Union[tuple, Stitch, None],
    ending_point: Union[tuple, Stitch, None]
) -> List[StitchGroup]:
    """
    Route fill stitches

    :param fill: the FillStitch element
    :param shape: the shape to be filled
    :param color_lines: lines grouped by color
    :param starting_point: the starting_point
    :paramt ending_point: the ending_point
    :returns: a list with StitchGroup objects
    """
    stitch_groups: List[StitchGroup] = []
    i = 0
    for color, lines in color_lines.items():
        if not fill.stop_at_ending_point:
            i += 1
            if stitch_groups:
                starting_point = stitch_groups[-1].stitches[-1]
        if starting_point is None:
            starting_point = ensure_multi_line_string(shape.boundary).geoms[0].coords[1]
        if ending_point is None:
            ending_point = ensure_multi_line_string(shape.boundary).geoms[0].coords[1]

        segments = [list(line.coords) for line in lines if len(line.coords) > 1]
        if len(segments) == 0:
            continue
        stitch_group = _segments_to_stitch_group(fill, shape, segments, i, color, starting_point, ending_point)
        if stitch_group is not None:
            stitch_groups.append(stitch_group)
        check_stop_flag()
    return stitch_groups


def _get_run_stitch_groups(
    fill: 'FillStitch',
    shape: Polygon,
    color_lines: defaultdict,
    starting_point: Optional[Union[tuple, Stitch]],
    ending_point: Optional[Union[tuple, Stitch]]
) -> List[StitchGroup]:
    """
    Route running stitches

    :param fill: the FillStitch element
    :param shape: the shape to be filled
    :param color_lines: lines grouped by color
    :param starting_point: the starting point
    :param ending_point: the ending point
    :returns: a list with StitchGroup objects
    """
    stitch_groups: List[StitchGroup] = []
    for color, lines in color_lines.items():
        if not fill.stop_at_ending_point and stitch_groups:
            starting_point = stitch_groups[-1].stitches[-1]
        # get segments and ignore lines smaller than 0.5 mm
        segments = [list(line.coords) for line in lines if line.length > 0.5 * PIXELS_PER_MM]
        if len(segments) == 0:
            continue
        stitch_group = _segments_to_stitch_group(fill, shape, segments, 0, color, starting_point, ending_point, True)
        if stitch_group is not None:
            stitch_groups.append(stitch_group)
        check_stop_flag()
    return stitch_groups


def _segments_to_stitch_group(
    fill: 'FillStitch',
    shape: Polygon,
    segments: List[List[Tuple[float, float]]],
    iteration: int,
    color: str,
    starting_point: Optional[Union[tuple, Stitch]],
    ending_point: Optional[Union[tuple, Stitch]],
    runs: bool = False
) -> Optional[StitchGroup]:
    """
    Route segments and turn them into a stitch group

    :param fill: the FillStitch element
    :param shape: the shape to be filled
    :param segments: a list with coordinate tuples
    :param iteration: wether to remove start and end travel stitches from the stitch group
    :param color: color information
    :param starting_point: the starting point
    :param ending_point: the ending point
    :param runs: wether running_stitch options should be applied or not
    :returns: a StitchGroup
    """
    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    if is_empty(fill_stitch_graph):
        return None
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
