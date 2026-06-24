from math import atan2, copysign, cos, sin
from random import random

from networkx import connected_components, is_empty
from shapely import get_coordinates, get_point, set_precision
from shapely.affinity import translate
from shapely.geometry import (LinearRing, LineString, MultiLineString,
                              MultiPoint, Point, Polygon)
from shapely.ops import linemerge, nearest_points, substring, unary_union
from shapely.prepared import prep

from lib.utils import prng

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..svg import PIXELS_PER_MM
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_geometry_collection,
                              ensure_multi_line_string, ensure_multi_point,
                              reverse_line_string, roll_linear_ring)
from ..utils.smoothing import smooth_path
from ..utils.threading import check_stop_flag
from .running_stitch import bean_stitch, running_stitch
from .tatami_fill import (build_fill_stitch_graph, build_travel_graph,
                          collapse_sequential_outline_edges, find_stitch_path,
                          graph_make_valid, tatami_fill, travel)
from .utils.connect_geometries import connect_offset_lines
from .utils.stitches import filter_small_stitches


def guided_fill(fill, shape, guideline, anchor_line, starting_point, ending_point):
    guide_line = prepare_guide_line(guideline, shape, fill.guided_fill_strategy)

    segments = intersect_region_with_grating_guideline(fill, shape, guide_line)

    if fill.guided_fill_strategy > 0 and segments:
        segments = connect_offset_lines(shape, segments, fill.row_spacing, fill.skip_last, fill.max_stitch_length)

    segments = _stagger_and_cut_segments(fill, shape, segments, guide_line, anchor_line)

    if not segments:
        return fallback(fill, shape, guideline, starting_point, ending_point)

    debug.add_layer("Segments")
    debug.log_line_strings([LineString(segment) for segment in segments])

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if is_empty(fill_stitch_graph):
        return fallback(fill, shape, guideline, ending_point)

    # in case we end up with disconnected shapes for whatever reason, let's render them independently (with a jump in between)
    connected_graphs = [fill_stitch_graph.subgraph(c).copy() for c in connected_components(fill_stitch_graph)]
    result = []
    for guided_graph in connected_graphs:
        check_stop_flag()
        graph_make_valid(guided_graph)

        travel_graph = build_travel_graph(guided_graph, shape, fill.guided_fill_angle or 0, fill.underpath)

        path = find_stitch_path(guided_graph, travel_graph, starting_point, ending_point, fill.underpath)
        stitches = path_to_stitches(fill, shape, path, travel_graph, guided_graph)

        if any(fill.bean_stitch_repeats):
            # remove small stitches before applying any bean stitches
            # otherwise the back stitch may not end up at the correct position
            metadata = fill.get_inkstitch_metadata()
            min_stitch_length = fill.min_stitch_length or metadata.get('min_stitch_len_mm') * PIXELS_PER_MM
            stitches = filter_small_stitches(stitches, min_stitch_length)

            # add bean stitches, but ignore travel stitches
            stitches = bean_stitch(stitches, fill.bean_stitch_repeats, ['travel', 'fill_row_start'])
        result.append(stitches)
    return result


def fallback(fill, shape, guideline, starting_point, ending_point,):
    # fall back to normal auto-fill with an angle that matches the guideline (sorta)
    guideline = guideline.geoms[0]
    guide_start, guide_end = [guideline.coords[0], guideline.coords[-1]]
    angle = atan2(guide_end[1] - guide_start[1], guide_end[0] - guide_start[0]) * -1
    return [tatami_fill(
        shape, angle, fill.row_spacing, None, fill.max_stitch_length, fill.running_stitch_length, fill.running_stitch_tolerance,
        fill.staggers, fill.skip_last, starting_point, ending_point, fill.underpath
    )]


def _stagger_and_cut_segments(fill, shape, segments, guide_line, anchor_line) -> list[list[tuple[float, ...]]]:

    # sort segments so that they are well prepared for staggering
    segments = _sort_segments(shape, segments, fill.guided_fill_strategy, guide_line)

    # apply stagger and smoothness
    new_segments = []
    i = 0
    debug.add_layer("stagger")
    for segment in segments:
        check_stop_flag()
        linestring = segment
        rolled = False

        if fill.smoothness:
            points = smooth_path([InkstitchPoint(*coord) for coord in linestring.coords], fill.smoothness)
            linestring = LineString(points)

        if linestring.is_ring and (get_point(linestring, 0).within(shape) or anchor_line):
            # users have the option to use an anchor line to help defining the start and end of the linestrings
            # for the stitch positioning task
            if anchor_line is not None:
                linestring, rolled = _get_anchored_stitch_line(fill, linestring, guide_line, anchor_line, i)
            if not rolled:
                # we assume that all lines which possibly ends within the shape are actually rings (even when not recognized as such)
                # take exterior of the shape, ignoring the holes. we connected everything to the exterior, so this should work
                # and if we are lucky, we can even expect a better stitch positioning (which is in general not ideal for the buffer method)
                diff = linestring.difference(Polygon(shape.exterior))
                if not diff.is_empty:
                    outside_point = take_only_line_strings(diff).geoms[0].interpolate(0.5, True)
                    linestring = _apply_stagger(fill, LineString(roll_linear_ring(linestring, linestring.project(outside_point))), guide_line, i)
        else:
            linestring = _apply_stagger(fill, linestring, guide_line, i)

        debug.log_line_string(linestring, "row", "blue")

        # when they used an anchor line, we still need to make sure, that the actual start point is outside of the shape
        if rolled or get_point(linestring, 0).within(shape):
            diff = linestring.difference(Polygon(shape.exterior))
            if not diff.is_empty:
                outside_point = take_only_line_strings(diff).geoms[0].interpolate(0.5, True)
                linestring = LineString(roll_linear_ring(linestring, linestring.project(outside_point)))

        # restrict segments to shape
        new_segments.extend(_linestring_to_segments(shape, linestring))
        i += 1

    return new_segments


def _get_anchored_stitch_line(fill, linestring, guide_line, anchor_line, i) -> tuple[LineString, bool]:
    rolled = False

    # get intersection points
    intersection = ensure_multi_point(linestring.intersection(anchor_line))
    if intersection.is_empty:
        # no intersection, return as is
        return linestring, rolled

    # roll start point to the first intersection point with the anchor
    projection = linestring.project(Point(intersection.geoms[0]))
    linestring = LineString(roll_linear_ring(linestring, projection))
    rolled = True

    if len(intersection.geoms) == 1:
        # there is only one intersection, we can simply apply stitches
        linestring = _apply_stagger(fill, linestring, guide_line, i)
    else:
        # more than one intersection
        # split the segment into multiple paths and apply stitches individually
        projections = [0, linestring.length]
        for point in list(intersection.geoms)[1:]:
            projections.append(linestring.project(point))
        projections.sort()
        linestring_coords: list[Point] = []
        for start, end in zip(projections[:-1], projections[1:]):
            line = substring(linestring, start, end)
            stitched_line = _apply_stagger(fill, line, guide_line, i)
            linestring_coords.extend(get_coordinates(stitched_line).tolist())
        linestring = LineString(linestring_coords)
    return linestring, rolled


def _apply_stagger(fill, linestring, guide_line, i) -> LineString:
    # we stagger by using a substring of the original line
    # then we reappend the first point (just in case we actually need it)
    num_staggers = fill.staggers
    if num_staggers == 0:
        num_staggers = 1  # sanity check to avoid division by zero.

    if fill.guided_fill_strategy != 2:
        start = ((i / fill.staggers) % 1) * fill.max_stitch_length
    else:
        # stitch positions for the buffer method
        # it'd be better if we applied stitch positions earlier, but this would alter distance values between the rings and may also change
        # recognition wether a shape contains an other, which in turn would make it difficult to connect the inner rings to the exterior of the
        # shape. Additionally: we already changed our starting points to somwhere outside of the shape
        # this helps to hide start and end point and enables us to do the routing, but it also means, that we already are way off when it
        # comes to stitch positions
        pos = round(linestring.distance(guide_line) / fill.row_spacing)
        start = ((pos / num_staggers) % 1) * fill.max_stitch_length

    first_point = get_point(linestring, 0)
    points = [InkstitchPoint(*coord) for coord in substring(linestring, start, linestring.length).coords]

    return LineString(
        [first_point] +
        running_stitch(
            points,
            [fill.max_stitch_length],
            fill.running_stitch_tolerance,
            fill.enable_random_stitch_length,
            fill.random_stitch_length_jitter,
            prng.join_args(fill.random_seed, i),
            False)
    )


def _sort_segments(shape, segments, strategy, guide_line) -> list[LineString]:
    # sort segments
    if strategy == 2:
        # we will check for the distance of the guide line in order to set the stagger
        return segments
    if strategy != 2:
        # construct a line going through all the segments
        points = MultiPoint([get_point(line, 0) for line in segments])
        # necessary for macOS
        points = set_precision(points, 0.0001)
        rect = points.minimum_rotated_rectangle
        projection_line = LineString()
        if isinstance(rect, LineString):
            projection_line = rect
        elif isinstance(rect, Polygon):
            minx, miny, maxx, maxy = rect.bounds
            projection_line = LineString([(minx, miny), (maxx, maxy)])
        else:
            return segments
    segments.sort(key=lambda line: projection_line.project(get_point(line, 0)))
    debug.add_layer("sorted")
    debug.log_line_strings(segments, 'sorted lines', 'red')
    return segments


def _linestring_to_segments(shape, linestring) -> list[list[tuple[float, ...]]]:
    # We could restrict the lines to the shape with linestring.intersection(shape), but this sadly would destroy
    # lines with self-intersections - and this may very well be the case with some of our lines
    # (ring connections, smoothing, running stitch tolerance). So let's put some more effort into this
    segments: list[list[tuple[float, ...]]] = []
    # Find where the line enters/exits the polygon
    boundary_intersections = ensure_multi_point(linestring.intersection(shape.boundary))
    # Get the distances along the line
    projections = sorted(linestring.project(point, True) for point in boundary_intersections.geoms)
    if projections:
        projections = [0] + projections + [1]
    elif get_point(linestring, 0).within(shape):
        # line is fully within the shape
        return [linestring.coords[:]]
    # Collect inside segments
    segments = []
    for d0, d1 in zip(projections[:-1], projections[1:]):
        seg = substring(linestring, d0, d1, True)
        if isinstance(seg, Point):
            continue
        if shape.contains(substring(seg, 0.4, -0.4, True)):
            segments.append(seg.coords[:])
    return segments


def path_to_stitches(fill, shape, path, travel_graph, fill_stitch_graph):
    path = collapse_sequential_outline_edges(path, fill_stitch_graph)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for edge in path:
        check_stop_flag()

        if edge.is_segment():
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']

            if edge[0] != path_geometry.coords[0]:
                path_geometry = reverse_line_string(path_geometry)

            new_stitches = [Stitch(*point, tags=['guided_fill', 'fill_row']) for point in path_geometry.coords]

            if fill.skip_last:
                del new_stitches[-1]

            if new_stitches:
                new_stitches[0].add_tag('fill_row_start')
                new_stitches[-1].add_tag('fill_row_end')

            stitches.extend(new_stitches)

            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(
                shape, travel_graph, edge, [fill.running_stitch_length], fill.running_stitch_tolerance, fill.skip_last, fill.underpath)
            )

    return stitches


def extend_line(line, shape) -> LineString:
    start_point = InkstitchPoint.from_tuple(line.coords[0])
    end_point = InkstitchPoint.from_tuple(line.coords[-1])
    direction = (end_point - start_point).unit()

    length = max(
        Point(start_point).hausdorff_distance(shape.envelope),
        Point(end_point).hausdorff_distance(shape.envelope)
    )

    new_start_point = start_point - direction * length
    new_end_point = end_point + direction * length

    # without this, we seem especially likely to run into this libgeos bug:
    #   https://github.com/shapely/shapely/issues/820
    new_start_point += InkstitchPoint(random() * 0.01, random() * 0.01)
    new_end_point += InkstitchPoint(random() * 0.01, random() * 0.01)

    return LineString((new_start_point, *line.coords, new_end_point))


def repair_non_simple_line(line) -> LineString:
    repaired = ensure_multi_line_string(unary_union(line))
    counter = 0
    # Do several iterations since we might have several concatenated selfcrossings
    while len(repaired.geoms) != 1 and counter < 4:
        line_segments = []
        for line_seg in repaired.geoms:
            if not line_seg.is_ring:
                line_segments.append(line_seg)

        repaired = ensure_multi_line_string(unary_union(linemerge(line_segments)))
        counter += 1
    if len(repaired.geoms) > 1:
        # They gave us a line with complicated self-intersections.  Use a fallback.
        return LineString((line.coords[0], line.coords[-1]))
    else:
        return repaired.geoms[0]


def take_only_line_strings(thing) -> MultiLineString:
    things = ensure_geometry_collection(thing)
    line_strings = linemerge([line for line in things.geoms if isinstance(line, (LineString, LinearRing))])
    return ensure_multi_line_string(line_strings)


def prepare_copy_guide(line, shape) -> LineString:
    line = line.geoms[0]
    if line.geom_type != 'LineString' or not line.is_simple:
        line = repair_non_simple_line(line)

    if line.is_ring:
        # If they pass us a ring, break it to avoid dividing by zero when
        # calculating a unit vector from start to end.
        line = LineString(line.coords[:-2])

    # extend the end points away from each other
    line = extend_line(line, shape)
    return line


def prepare_offset_guide(line, shape) -> LineString | LinearRing:
    line = line.geoms[0]
    if not line.is_ring:
        # extend the end points away from each other
        line = extend_line(line, shape)

    if line.geom_type != 'LineString' or not line.is_simple:
        line = repair_non_simple_line(line)

    if line.is_ring:
        line = LinearRing(line)

    return line


def prepare_guide_line(line, shape, strategy) -> LinearRing | LineString | MultiLineString:
    if strategy == 0:
        return prepare_copy_guide(line, shape)
    elif strategy == 2:
        return line.simplify(0.0001).normalize()
    return prepare_offset_guide(line, shape)


def _get_direction_and_start_row(shape, guide_line, strategy, angle, row_spacing):
    if strategy == 1 or (strategy == 0 and angle is None):
        translate_direction = InkstitchPoint(*guide_line.coords[-1]) - InkstitchPoint(*guide_line.coords[0])
        translate_direction = translate_direction.unit().rotate_left()
        start_row = _get_start_row(guide_line, shape, row_spacing, translate_direction)
    elif strategy == 0:
        translate_direction = InkstitchPoint(cos(angle), sin(angle)).unit()
        start_row = _get_start_row(guide_line, shape, row_spacing, translate_direction)
    else:
        translate_direction = None
        start_row = int(guide_line.distance(shape) / row_spacing)
    return translate_direction, start_row


def _get_start_row(line, shape, row_spacing, line_direction) -> int:
    if line.intersects(shape):
        return 0

    point1, point2 = nearest_points(line, shape.centroid)
    distance = point1.distance(point2)
    row = int(distance / row_spacing)

    # This flips the sign of the starting row if the shape is on the other side
    # of the guide line
    shape_direction = InkstitchPoint.from_shapely_point(point2) - InkstitchPoint.from_shapely_point(point1)
    return int(copysign(row, shape_direction * line_direction))


def intersect_region_with_grating_guideline(fill, shape, guide_line) -> list[LineString]:  # noqa: C901
    shape_envelope = prep(shape.envelope)
    strategy = fill.guided_fill_strategy
    translate_direction, start_row = _get_direction_and_start_row(
        shape, guide_line, strategy, fill.guided_fill_angle, fill.row_spacing
    )

    row = start_row
    direction = 1
    offset_line = None
    rows = []
    i = 0

    while True:
        # used for the copy method with random stitch length
        i += 1
        check_stop_flag()

        if strategy > 0:
            # parallel_offset
            offset = row * fill.row_spacing
            if offset == 0:
                # this is needed for macOS builds
                offset = 0.0001
            if strategy == 1:
                segment = guide_line.offset_curve(offset, quad_segs=16)
                if not isinstance(segment, (LineString, LinearRing)):
                    # sometimes for an odd reason parallel_offset will split up a part of the offset line
                    # we can put it back together with the line_merge method and still keepthe disjoint parts
                    segment = list(ensure_multi_line_string(segment).geoms)
                    segment = linemerge(segment)
            elif strategy == 2:
                # buffer reaches out to both sides at once, when we reach the end of the first direction
                # we have enough lines to work with
                if direction == -1:
                    break
                segment = guide_line.buffer(offset + fill.row_spacing / 2).boundary
        else:
            # Copy
            translate_amount = translate_direction * row * fill.row_spacing
            offset_line = translate(guide_line, xoff=translate_amount.x, yoff=translate_amount.y)
            if fill.smoothness:
                offset_line = LineString(smooth_path(offset_line.coords, fill.smoothness))
            segment = offset_line

        if shape_envelope.intersects(segment):
            for segment in take_only_line_strings(segment).geoms:
                if segment.intersects(shape):
                    rows.append(segment)
            row += direction
        else:
            if direction == 1:
                direction = -1
                row = start_row - 1
            else:
                break

    # Add some debug infos
    debug.log_line_strings(ensure_multi_line_string(guide_line), 'guide line')
    debug.log_line_strings(ensure_multi_line_string(shape.boundary), "guided fill shape")
    debug.add_layer("Grating rows")
    debug.log_line_strings(rows)

    return rows
