import numpy as np
from shapely import geometry as shgeo
from shapely.ops import linemerge, unary_union

from .auto_fill import (build_fill_stitch_graph,
                        build_travel_graph, collapse_sequential_outline_edges, fallback,
                        find_stitch_path, graph_is_valid, travel)
from ..i18n import _
from ..stitch_plan import Stitch
from ..utils.geometry import Point as InkstitchPoint, ensure_geometry_collection, ensure_multi_line_string, reverse_line_string


def guided_fill(shape,
                guideline,
                angle,
                row_spacing,
                num_staggers,
                max_stitch_length,
                running_stitch_length,
                skip_last,
                starting_point,
                ending_point=None,
                underpath=True):
    try:
        segments = intersect_region_with_grating_guideline(shape, guideline, row_spacing, num_staggers, max_stitch_length)
        fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    except ValueError:
        # Small shapes will cause the graph to fail - min() arg is an empty sequence through insert node
        return fallback(shape, running_stitch_length)

    if not graph_is_valid(fill_stitch_graph, shape, max_stitch_length):
        return fallback(shape, running_stitch_length)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(path, travel_graph, fill_stitch_graph, max_stitch_length, running_stitch_length, skip_last)

    return result


def path_to_stitches(path, travel_graph, fill_stitch_graph, stitch_length, running_stitch_length, skip_last):
    path = collapse_sequential_outline_edges(path)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for edge in path:
        if edge.is_segment():
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']

            if edge[0] != path_geometry.coords[0]:
                path_geometry = reverse_line_string(path_geometry)

            new_stitches = [Stitch(*point) for point in path_geometry.coords]

            # need to tag stitches

            if skip_last:
                del new_stitches[-1]

            stitches.extend(new_stitches)

            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(travel_graph, edge[0], edge[1], running_stitch_length, skip_last))

    return stitches


def extend_line(line, shape):
    (minx, miny, maxx, maxy) = shape.bounds

    line = line.simplify(0.01, False)

    upper_left = InkstitchPoint(minx, miny)
    lower_right = InkstitchPoint(maxx, maxy)
    length = (upper_left - lower_right).length()

    point1 = InkstitchPoint(*line.coords[0])
    point2 = InkstitchPoint(*line.coords[1])
    new_starting_point = point1 - (point2 - point1).unit() * length

    point3 = InkstitchPoint(*line.coords[-2])
    point4 = InkstitchPoint(*line.coords[-1])
    new_ending_point = point4 + (point4 - point3).unit() * length

    return shgeo.LineString([new_starting_point.as_tuple()] +
                            line.coords[1:-1] + [new_ending_point.as_tuple()])


def repair_multiple_parallel_offset_curves(multi_line):
    lines = ensure_multi_line_string(linemerge(multi_line))
    longest_line = max(lines.geoms, key=lambda line: line.length)

    # need simplify to avoid doubled points caused by linemerge
    return longest_line.simplify(0.01, False)


def repair_non_simple_line(line):
    repaired = unary_union(line)
    counter = 0
    # Do several iterations since we might have several concatenated selfcrossings
    while repaired.geom_type != 'LineString' and counter < 4:
        line_segments = []
        for line_seg in repaired.geoms:
            if not line_seg.is_ring:
                line_segments.append(line_seg)

        repaired = unary_union(linemerge(line_segments))
        counter += 1
    if repaired.geom_type != 'LineString':
        raise ValueError(
            _("Guide line (or offset copy) is self crossing!"))
    else:
        return repaired


def take_only_line_strings(thing):
    things = ensure_geometry_collection(thing)
    line_strings = [line for line in things.geoms if isinstance(line, shgeo.LineString)]

    return shgeo.MultiLineString(line_strings)


def apply_stitches(line, max_stitch_length, num_staggers, row_spacing, row_num):
    threshold = row_spacing / 2.0
    simplified_line = line.simplify(row_spacing / 2.0, False)
    simplified_points = [shgeo.Point(x, y) for x, y in simplified_line.coords]
    start = (float(row_num % num_staggers) / num_staggers) * max_stitch_length
    distances = np.arange(start, line.length, max_stitch_length)
    stitched_line = shgeo.LineString([line.interpolate(distance) for distance in distances])

    # stitched_line may round corners, which will look terrible.  This finds them and adds
    # them in.
    extra_points = [line.project(point) for point in simplified_points if point.distance(stitched_line) > threshold]
    distances = np.sort(np.concatenate([distances, extra_points]))

    return shgeo.LineString([line.interpolate(distance) for distance in distances])


def intersect_region_with_grating_guideline(shape, line, row_spacing, num_staggers, max_stitch_length):
    if line.geom_type != 'LineString' or not line.is_simple:
        line = repair_non_simple_line(line)

    # extend the line towards the ends to increase probability that all offsetted curves cross the shape
    line = extend_line(line, shape)

    row = 0
    direction = 1
    while True:
        offset_line = line.parallel_offset(row * row_spacing * direction, 'left', join_style=shgeo.JOIN_STYLE.bevel)
        offset_line = take_only_line_strings(offset_line)

        if isinstance(offset_line, shgeo.MultiLineString):
            offset_line = repair_multiple_parallel_offset_curves(offset_line)

        if not offset_line.is_simple:
            offset_line = repair_non_simple_line(offset_line)

        if direction == -1:
            offset_line = reverse_line_string(offset_line)

        stitched_line = apply_stitches(offset_line, max_stitch_length, num_staggers, row_spacing, row * direction)
        intersection = shape.intersection(stitched_line)

        if intersection.is_empty:
            if direction == 1:
                direction = -1
                row = 1
            else:
                break
        else:
            for segment in take_only_line_strings(intersection).geoms:
                yield segment.coords[:]
            row += 1
