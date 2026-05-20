from math import atan2, copysign
from random import random

import numpy as np
from networkx import connected_components, is_empty
from shapely import get_point
from shapely.affinity import scale, translate
from shapely.geometry import (LinearRing, LineString, MultiLineString, Point,
                              Polygon)
from shapely.ops import linemerge, nearest_points, substring, unary_union
from shapely.prepared import prep

from lib.utils import prng

from ..debug.debug import debug
from ..stitch_plan import Stitch
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_geometry_collection,
                              ensure_multi_line_string, ensure_multi_point,
                              reverse_line_string, roll_linear_ring)
from ..utils.smoothing import smooth_path
from ..utils.threading import check_stop_flag
from .auto_fill import (auto_fill, build_fill_stitch_graph, build_travel_graph,
                        collapse_sequential_outline_edges, find_stitch_path,
                        graph_make_valid, travel)
from .running_stitch import bean_stitch, random_running_stitch


def guided_fill(shape,
                guideline,
                angle,
                row_spacing,
                num_staggers,
                bean_stitch_repeats,
                max_stitch_length,
                running_stitch_length,
                running_stitch_tolerance,
                smoothness,
                skip_last,
                starting_point,
                ending_point,
                underpath,
                strategy,
                enable_random_stitch_length,
                random_sigma,
                random_seed,
                ):
    segments = intersect_region_with_grating_guideline(
        shape, guideline, row_spacing, num_staggers, max_stitch_length, strategy, running_stitch_tolerance, smoothness,
        enable_random_stitch_length, random_sigma, random_seed
    )

    if strategy > 0 and segments:
        segments = _connect_parallel_offset_segments(shape, segments, row_spacing, skip_last, max_stitch_length)

        segments = _stagger_and_cut_segments(
            shape, segments, max_stitch_length, row_spacing, num_staggers, strategy,
            enable_random_stitch_length, random_sigma, random_seed, running_stitch_tolerance, smoothness
        )
    else:
        segments = [line.coords for line in segments]

    if not segments:
        return fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                        num_staggers, skip_last, starting_point, ending_point, underpath)

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    if is_empty(fill_stitch_graph):
        return fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                        num_staggers, skip_last, starting_point, ending_point, underpath)

    # if the shape has holes, we may run into a problem with disconnected components
    # TODO: we may want to solve this in a different way in some future day,
    # but for now, let's render those components independently (which will result in jumps)
    connected_graphs = [fill_stitch_graph.subgraph(c).copy() for c in connected_components(fill_stitch_graph)]
    result = []
    for guided_graph in connected_graphs:
        check_stop_flag()
        graph_make_valid(guided_graph)

        travel_graph = build_travel_graph(guided_graph, shape, angle, underpath)

        path = find_stitch_path(guided_graph, travel_graph, starting_point, ending_point, underpath)
        stitches = path_to_stitches(
            shape, path, travel_graph, guided_graph, max_stitch_length, running_stitch_length, running_stitch_tolerance,
            skip_last, underpath
        )

        if any(bean_stitch_repeats):
            # add bean stitches, but ignore travel stitches
            stitches = bean_stitch(stitches, bean_stitch_repeats, ['auto_fill_travel', 'fill_row_start'])
        result.append(stitches)
    return result


def _stagger_and_cut_segments(
        shape, segments, max_stitch_length, row_spacing, num_staggers, strategy,
        enable_random_stitch_length, random_sigma, random_seed, tolerance, smoothness) -> list[list[tuple[float, ...]]]:

    # sort segments so that they are well prepared for staggering
    if num_staggers:
        _sort_segments(shape, segments)

    # apply stagger and smoothness
    new_segments = []
    i = 0
    for segment in segments:
        check_stop_flag()
        linestring = segment

        if linestring.is_ring or get_point(linestring, 0).within(shape):
            # we assume that all lines which possibly ends within the shape are actually rings (even when not recognized as such)
            diff = linestring.difference(shape)
            if not diff.is_empty:
                outside_point = take_only_line_strings(diff).geoms[0].interpolate(0.5, True)
                linestring = LineString(roll_linear_ring(linestring, linestring.project(outside_point)))
                stagger = 1
            i -= 1
        else:
            stagger = num_staggers

        if smoothness:
            points = smooth_path([InkstitchPoint(*coord) for coord in linestring.coords], smoothness)
            linestring = LineString(points)

        if enable_random_stitch_length:
            start = ((i / (stagger)) % 1) * max_stitch_length
            first_segment = substring(linestring, 0, 1)
            segment_length = max(first_segment.length, 0.1)
            target_length = segment_length + 2 * start
            scale_factor = target_length / segment_length
            extended_line = scale(first_segment, scale_factor, scale_factor, origin='centroid')
            points = [InkstitchPoint(*extended_line.coords[0])] + [InkstitchPoint(*coord) for coord in linestring.coords]
            linestring = LineString(random_running_stitch(points, [max_stitch_length], tolerance, random_sigma, prng.join_args(random_seed, i)))
        else:
            linestring = apply_stitches(linestring, [max_stitch_length], stagger, row_spacing, i, tolerance)
            # we may have distoreted the line, cut it (by staggereing) or did something else bad to it
            first = get_point(linestring, 0)
            last = get_point(linestring, -1)
            if max_stitch_length >= first.distance(shape.boundary) > 0.001 and first.within(shape):
                linestring = _connect_line_to_boundary(shape.boundary, linestring, 0)
            elif max_stitch_length > last.distance(shape.boundary) > 0.001 and last.within(shape):
                linestring = _connect_line_to_boundary(shape.boundary, linestring, -1)

        # restrict segments to shape
        new_segments.extend(_linestring_to_segments(shape, linestring))
        i += 1

    return new_segments


def _sort_segments(shape, segments) -> None:
    # sort segments
    # construct a line going through all the segments
    envelope = shape.envelope.boundary
    if envelope.is_empty:
        return
    segments.sort(key=lambda line: envelope.project(get_point(line, 0)))


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


def _connect_line_to_boundary(boundary, line, position) -> LineString:
    point = nearest_points(get_point(line, position), boundary)[1]
    if position == 0:
        new_line = LineString([point] + list(line.coords))
    else:
        new_line = LineString(list(line.coords) + [point])
    return new_line


def _connect_parallel_offset_segments(shape, segments, row_spacing, skip_last, max_stitch_length):
    outline_segments, segments_within = _split_segment_types(shape, segments, row_spacing)
    if not segments_within:
        return segments
    if not outline_segments:
        outline_segments = list(ensure_multi_line_string(shape.boundary).geoms)

    # sort inside segments from small to big
    segments_within.sort(key=lambda pg: pg.area)

    # now that we found out which segments need to be connected
    # let's see how they are related to each other
    connected_segments = _get_segment_relations(segments_within)

    # the polygons were helpful to figure out the geometric relationsship between the shapes
    # up from now we prefer to work with LinearRings, the index positions will stay the same
    linearrings_within = [LinearRing(seg.exterior.coords) for seg in segments_within]

    # now let's loop through the connected_segments dictionary and connect the shapes as good as possible
    _connect_within(connected_segments, linearrings_within, row_spacing, skip_last, max_stitch_length)

    # now we cleaned up the inner circles
    # we only need to connect them to the outside
    _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing)

    debug.add_layer('connected offset segments')
    debug.log_line_strings(outline_segments)

    return outline_segments


def _connect_within(connected_segments, linearrings_within, row_spacing, skip_last, max_stitch_length):
    # while we are connecting the shapes, we will update the shape at the outer_index position to contain the connected shape
    # therefore we will need to collect the indices of the inner shapes that are now duplicated
    # this way we can remove them from the list in the end
    segments_to_remove = []
    for inner_index, outer_index in connected_segments.items():
        if outer_index is None:
            continue

        if row_spacing == 0:
            row_spacing = 0.001

        # First we are more restrict in order to find a good spot
        d_tolerance = row_spacing * 1.5
        shapes_are_connected = _connect_linearrings(
            linearrings_within, segments_to_remove, inner_index, outer_index, row_spacing, skip_last, max_stitch_length, d_tolerance
        )
        if not shapes_are_connected:
            # we couldn't find an ok spot, so let's skip this element
            segments_to_remove.append(inner_index)

    # remove the duplicated inner segments
    segments_to_remove.sort(reverse=True)
    for segment_index in segments_to_remove:
        try:
            linearrings_within.pop(segment_index)
        except IndexError:
            pass


def _connect_linearrings(
        linearrings_within, segments_to_remove, inner_index, outer_index, row_spacing, skip_last, max_stitch_length, d_tolerance):
    # ensure consistent direction
    inner = ensure_ccw(linearrings_within[inner_index])
    outer = ensure_ccw(linearrings_within[outer_index])
    # We could speed things up by predefining a good spot,
    # but we get nicer connections for smoothing if we don't (speed vs stitch path...)
    # nearest = nearest_points(inner, outer)
    # inner = roll_linear_ring(inner, inner.project(nearest[0]))
    offset = 0
    # move around the inner ring and check combining conditions in sections of row_spacing width
    while offset + row_spacing < inner.length:
        check_stop_flag()
        p1_inner, p2_inner, p1_outer, p2_outer, d1, d2 = _get_possible_connector_points(inner, outer, offset, row_spacing)
        # check if distances are within tolerance
        if d1 < row_spacing + d_tolerance and d2 < row_spacing + d_tolerance:
            proj1 = inner.project(p2_inner)
            proj2 = outer.project(p2_outer)
            rolled_inner = LineString(roll_linear_ring(inner, proj1))
            rolled_outer = LineString(roll_linear_ring(outer, proj2))
            rolled_inner = substring(rolled_inner, 0, -row_spacing)
            rolled_outer = substring(rolled_outer, 0, -row_spacing)
            if skip_last:
                # TODO: this could be improved, maybe with a substring,
                # but I'm goig to leave it like this for now, because taking simply the substring would not be correct neither
                connected_line = LinearRing(rolled_outer.coords[:] + rolled_inner.segmentize(max_stitch_length).reverse().coords[1:-1])
            else:
                connected_line = LinearRing(rolled_outer.coords[:] + rolled_inner.reverse().coords[:])
            linearrings_within[outer_index] = connected_line
            segments_to_remove.append(inner_index)
            return True
        offset += 1
    return False


def _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing, iteration=0) -> None:
    remove: list[int] = []
    add: list[LineString] = []
    unconnected: list[LineString] = []
    for ring in linearrings_within:
        _connect_ring(ring, shape, outline_segments, linearrings_within, row_spacing, unconnected, remove, add)
    # remove the duplicated inner segments
    for segment_index in sorted(remove, reverse=True):
        try:
            outline_segments.pop(segment_index)
        except IndexError:
            pass
    outline_segments.extend(add)
    if unconnected and iteration < 5:
        # give it an other try, we may have made helping connections in the last iteration
        linearrings_within = unconnected
        iteration += 1
        _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing, iteration)


def _connect_ring(ring, shape, outline_segments, linearrings_within, row_spacing, unconnected, remove, add) -> None:
    original_ring = ring
    connected = None
    for i in range(len(outline_segments)):
        if i in remove:
            continue
        line = outline_segments[i]
        if original_ring.distance(line) <= row_spacing + 0.001:
            if connected is None:
                new_segment = _connect_linearring_with_linestring(ring, line, row_spacing)
                if new_segment is not None:
                    outline_segments[i] = new_segment
                    ring = new_segment
                    connected = i
                    if line.intersects(shape.exterior):
                        return
            else:
                if get_point(line, 0).within(shape):
                    seg1 = _connect_linearring_with_linestring(ring, line, row_spacing)
                    if seg1 is None:
                        continue
                else:
                    seg1, seg2 = _connect_linestrings(ring, line, row_spacing)
                    add.append(seg2)
                outline_segments[connected] = seg1
                remove.append(i)
                # let's not try any harder
                return
    unconnected.append(ring)


def _get_segment_relations(segments_within) -> dict[int, int | None]:
    # this creates a dictionary with the index positions of the inner shapes
    # and the value represents the index postion of the outer shape
    connected_segments: dict[int, int | None] = {}
    for i, inner in enumerate(segments_within):
        segment_connected = False
        for j, outer in enumerate(segments_within):
            if j <= i:
                continue
            if outer.covers(inner):
                segment_connected = True
                connected_segments[i] = j
                break
        if not segment_connected:
            connected_segments[i] = None
    return connected_segments


def _connect_linestrings(line1, line2, row_spacing):
    # connect two linestrings
    p1, p3 = nearest_points(line1, line2)
    p2 = line1.interpolate(line1.project(p1) + row_spacing)
    p4 = line2.interpolate(line2.project(p3) + row_spacing)
    if _needs_reverse(p1, p2, p3, p4):
        p4 = line2.interpolate(line2.project(p3) - row_spacing)
        line2 = line2.reverse()
    segment1 = substring(line1, 0, line1.project(p1))
    segment2 = substring(line2, 0, line2.project(p3)).reverse()
    segment3 = substring(line1, line1.project(p2), line1.length).reverse()
    segment4 = substring(line2, line2.project(p4), line2.length)
    connected = LineString(list(segment1.coords) + list(segment2.coords)), LineString(list(segment3.coords) + list(segment4.coords))
    return connected


def _needs_reverse(p1, p2, p3, p4):
    p1p3 = LineString([p1, p3])
    p2p4 = LineString([p2, p4])
    if p1p3.intersects(p2p4):
        return True
    return False


def _connect_linearring_with_linestring(ring, line, row_spacing, threshold=0.01):
    offset = 0
    while ring.length >= row_spacing + offset:
        check_stop_flag()
        p1, p2, p3, p4, d1, d2 = _get_possible_connector_points(ring, line, offset, row_spacing)
        if d1 < row_spacing * 1.5 and d2 < row_spacing * 1.5:
            # line start
            proj1 = line.project(p3)
            proj2 = line.project(p4)
            if proj1 > proj2:
                proj1, proj2 = proj2, proj1
            if abs(proj1 - proj2) > row_spacing + threshold:
                proj2 = proj1 + row_spacing
            o1 = substring(line, 0, proj1)
            o2 = substring(line, proj1 + row_spacing, line.length)
            # open the ring
            proj1 = ring.project(p1)
            rolled_ring = LineString(roll_linear_ring(ring, proj1))
            rolled_ring = substring(rolled_ring, row_spacing, rolled_ring.length)
            # connect the parts
            connected = LineString(o1.coords[:] + rolled_ring.coords[:] + o2.coords[:])
            if not connected.is_simple:
                connected = LineString(o1.coords[:] + rolled_ring.coords[::-1] + o2.coords[:])
            return connected
        offset += 1
    return None


def _split_segment_types(shape, segments, row_spacing) -> tuple[list[LineString], list[Polygon]]:
    # we have two different kinds of segments:
    # the ones that are touching the outline
    # and the ones, that are entirely within the shape (those are the ones we need to connect)

    prepared_shape = prep(shape)
    prepared_boundary = prep(shape.boundary)

    outline_segments = []
    segments_within = []
    for line in segments:
        if not prepared_shape.intersects(line):
            continue
        if not prepared_boundary.intersects(line):
            # ensure the line has at least 4 points, which is necessary for both, polygon or linearring
            if len(line.coords) < 4:
                length = line.length
                line = line.segmentize(max_segment_length=length/3).coords[:]
            segments_within.append(Polygon(line))
        else:
            # if this segment has the same starting and ending point (linearring),
            # we need to ensure, that this point lies outside of the shape
            if line.coords[0] == line.coords[-1] and get_point(line, 0).within(shape):
                outside_point = take_only_line_strings(line.difference(shape)).geoms[0].interpolate(0.5, True)
                line = LineString(roll_linear_ring(line, line.project(outside_point)))
            outline_segments.append(line)
    return outline_segments, segments_within


def _get_possible_connector_points(inner, outer, offset, row_spacing) -> tuple[Point, Point, Point, Point, float, float]:
    # define two points on the inner ring according to offset and row_spacing
    p1 = inner.interpolate(offset)
    p2 = inner.interpolate(offset + row_spacing)
    # get nearest points on the outer ring
    p1_outer = nearest_points(outer, p1)[0]
    p2_outer = nearest_points(outer, p2)[0]
    # get the distances between the corresponding points
    d1 = p1.distance(p1_outer)
    d2 = p2.distance(p2_outer)
    return p1, p2, p1_outer, p2_outer, d1, d2


def ensure_ccw(ring) -> LinearRing:
    # True if counter-clockwise
    if ring.is_ccw:
        return ring
    else:
        return ring.reverse()


def fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
             num_staggers, skip_last, starting_point, ending_point, underpath):
    # fall back to normal auto-fill with an angle that matches the guideline (sorta)
    guideline = guideline.geoms[0]
    guide_start, guide_end = [guideline.coords[0], guideline.coords[-1]]
    angle = atan2(guide_end[1] - guide_start[1], guide_end[0] - guide_start[0]) * -1
    return [auto_fill(shape, angle, row_spacing, None, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                      num_staggers, skip_last, starting_point, ending_point, underpath)]


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph,
                     stitch_length, running_stitch_length, running_stitch_tolerance, skip_last,
                     underpath):
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

            if skip_last:
                del new_stitches[-1]

            if new_stitches:
                new_stitches[0].add_tag('fill_row_start')
                new_stitches[-1].add_tag('fill_row_end')

            stitches.extend(new_stitches)

            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(shape, travel_graph, edge, [running_stitch_length], running_stitch_tolerance, skip_last, underpath))

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


def apply_stitches(line, max_stitch_length, num_staggers, row_spacing, row_num, threshold=None) -> LineString:
    max_stitch_length = max_stitch_length[0]
    if num_staggers == 0:
        num_staggers = 1  # sanity check to avoid division by zero.
    start = ((row_num / num_staggers) % 1) * max_stitch_length
    projections = np.arange(start, line.length, max_stitch_length)
    points = np.array([line.interpolate(projection).coords[0] for projection in projections])

    if len(points) < 2:
        coords = line.coords
        points = np.array([coords[0], coords[-1]])

    stitched_line = LineString(points)

    # stitched_line may round corners, which will look terrible.  This finds the
    # corners.
    if not threshold:
        threshold = row_spacing / 2.0
    simplified_line = line.simplify(threshold, preserve_topology=False)
    simplified_points = [Point(x, y) for x, y in simplified_line.coords]

    extra_points = []
    extra_point_projections = []
    for point in simplified_points:
        if point.distance(stitched_line) > threshold:
            extra_points.append(point.coords[0])
            extra_point_projections.append(line.project(point))

    # Now we need to insert the new points into their correct spots in the line.
    indices = np.searchsorted(projections, extra_point_projections)
    if len(indices) > 0:
        points = np.insert(points, indices, extra_points, axis=0)

    return LineString(points)


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
        return line.normalize()
    return prepare_offset_guide(line, shape)


def _get_start_row(line, shape, row_spacing, line_direction):
    if line.intersects(shape):
        return 0

    point1, point2 = nearest_points(line, shape.centroid)
    distance = point1.distance(point2)
    row = int(distance / row_spacing)

    # This flips the sign of the starting row if the shape is on the other side
    # of the guide line
    shape_direction = InkstitchPoint.from_shapely_point(point2) - InkstitchPoint.from_shapely_point(point1)
    return copysign(row, shape_direction * line_direction)


def intersect_region_with_grating_guideline(shape, line, row_spacing, num_staggers, max_stitch_length, strategy, tolerance, smoothness,  # noqa: C901
                                            enable_random_stitch_length, random_sigma, random_seed) -> list[LineString]:
    line = prepare_guide_line(line, shape, strategy)

    shape_envelope = prep(shape.convex_hull)

    if num_staggers == 0:
        num_staggers = 1  # sanity check to avoid division by zero.

    if strategy != 2:
        translate_direction = InkstitchPoint(*line.coords[-1]) - InkstitchPoint(*line.coords[0])
        translate_direction = translate_direction.unit().rotate_left()

        start_row = _get_start_row(line, shape, row_spacing, translate_direction)
    else:
        start_row = int(line.distance(shape) / row_spacing)

    row = start_row
    direction = 1
    offset_line = None
    rows = []
    buffer_offset = 0

    while True:
        check_stop_flag()

        if strategy > 0:
            # parallel_offset
            offset = row * row_spacing
            if offset == 0:
                # this is needed for macOS builds
                offset = 0.0001
            if strategy == 1:
                stitched_line = line.offset_curve(offset, quad_segs=16)
                if not isinstance(stitched_line, (LineString, LinearRing)):
                    # sometimes for an odd reason parallel_offset will split up a part of the offset line
                    # we can put it back together with the line_merge method and still keepthe disjoint parts
                    stitched_line = list(ensure_multi_line_string(stitched_line).geoms)
                    stitched_line = linemerge(stitched_line)
            elif strategy == 2:
                # buffer
                # buffer reaches out to both sides at once, when we reach the end of the first direction
                # we have enough lines to work with
                if direction == -1:
                    break

                # the first line can be used as a simple line in case all parts start and end outside of the shape
                # or we received a closed shape
                # when it ends within the shape, we still want to apply a small buffer as there is no way to connect
                # the endpoint properly otherwise
                if offset < row_spacing:
                    lines = ensure_multi_line_string(line)
                    end_points_within = []
                    for buffered_geoms in lines.geoms:
                        end_points_within.extend([
                            Point(buffered_geoms.coords[0]).within(shape),
                            Point(buffered_geoms.coords[-1]).within(shape)
                        ])
                    if line.is_simple and (line.is_ring or not any(end_points_within)):
                        # we would like to avoid avoid doubling up the first line with a small buffer value
                        # but we can only do that, when the line is intersecting with the outline or isa linear ring
                        # otherwise it will be difficult to connect it properly
                        stitched_line = line
                    else:
                        # set an inital offset to avoid a doubled line at the center
                        buffer_offset = row_spacing / 2
                        stitched_line = line.buffer(offset + buffer_offset).boundary
                else:
                    stitched_line = line.buffer(offset + buffer_offset).boundary
        else:
            # Copy
            translate_amount = translate_direction * row * row_spacing
            offset_line = translate(line, xoff=translate_amount.x, yoff=translate_amount.y)
            if smoothness:
                offset_line = LineString(smooth_path(offset_line.coords, smoothness))
            stitched_line = apply_stitches(offset_line, [max_stitch_length], num_staggers, row_spacing, row, tolerance)

        intersection = shape.intersection(stitched_line)
        if shape_envelope.intersects(stitched_line):
            if not intersection.is_empty:
                if strategy == 1:
                    # cut later in order to sort them for stagger
                    for segment in take_only_line_strings(stitched_line).geoms:
                        rows.append(segment)
                elif strategy == 2:
                    # apply stitches reduces the line length, so when we cut our lines here, we'll need to add at least the stitch length to it
                    intersection = stitched_line.intersection(shape.envelope.buffer(max_stitch_length + 0.2))
                    for segment in take_only_line_strings(intersection).geoms:
                        if segment.intersects(shape):
                            rows.append(segment)
                else:
                    for segment in take_only_line_strings(intersection).geoms:
                        rows.append(segment)
            row += direction
        else:
            if direction == 1:
                direction = -1
                row = start_row - 1
            else:
                break

    # Add some debug infos
    debug.log_line_strings(ensure_multi_line_string(line), 'guide line')
    debug.log_line_strings(ensure_multi_line_string(shape.boundary), "guided fill shape")
    debug.add_layer("Grating rows")
    debug.log_line_strings([LineString(row) for row in rows])

    return rows
