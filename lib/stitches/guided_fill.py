from shapely import geometry as shgeo
from shapely.ops import linemerge, unary_union

from .auto_fill import (build_fill_stitch_graph,
                        build_travel_graph, collapse_sequential_outline_edges, fallback,
                        find_stitch_path, graph_is_valid, travel)
from .running_stitch import running_stitch
from ..i18n import _
from ..stitch_plan import Stitch
from ..utils.geometry import Point as InkstitchPoint, reverse_line_string


def guided_fill(shape,
                guideline,
                angle,
                row_spacing,
                max_stitch_length,
                running_stitch_length,
                skip_last,
                starting_point,
                ending_point=None,
                underpath=True):
    try:
        segments = intersect_region_with_grating_guideline(shape, guideline, row_spacing)
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

            point_list = [Stitch(*point) for point in path_geometry.coords]
            new_stitches = running_stitch(point_list, stitch_length)

            # need to tag stitches

            if skip_last:
                del new_stitches[-1]

            stitches.extend(new_stitches)

            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(travel_graph, edge[0], edge[1], running_stitch_length, skip_last))

    return stitches


def extend_line(line, minx, maxx, miny, maxy):
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
    lines = linemerge(multi_line)
    lines = list(lines.geoms)
    max_length = -1
    max_length_idx = -1
    for idx, subline in enumerate(lines):
        if subline.length > max_length:
            max_length = subline.length
            max_length_idx = idx
    # need simplify to avoid doubled points caused by linemerge
    return lines[max_length_idx].simplify(0.01, False)


def repair_non_simple_lines(line):
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


def intersect_region_with_grating_guideline(shape, line, row_spacing, flip=False):  # noqa: C901

    row_spacing = abs(row_spacing)
    (minx, miny, maxx, maxy) = shape.bounds
    upper_left = InkstitchPoint(minx, miny)
    rows = []

    if line.geom_type != 'LineString' or not line.is_simple:
        line = repair_non_simple_lines(line)
    # extend the line towards the ends to increase probability that all offsetted curves cross the shape
    line = extend_line(line, minx, maxx, miny, maxy)

    line_offsetted = line
    res = line_offsetted.intersection(shape)
    while isinstance(res, (shgeo.GeometryCollection, shgeo.MultiLineString)) or (not res.is_empty and len(res.coords) > 1):
        if isinstance(res, (shgeo.GeometryCollection, shgeo.MultiLineString)):
            runs = [line_string.coords for line_string in res.geoms if (
                    not line_string.is_empty and len(line_string.coords) > 1)]
        else:
            runs = [res.coords]

        runs.sort(key=lambda seg: (
                InkstitchPoint(*seg[0]) - upper_left).length())
        if flip:
            runs.reverse()
            runs = [tuple(reversed(run)) for run in runs]

        if row_spacing > 0:
            rows.append(runs)
        else:
            rows.insert(0, runs)

        line_offsetted = line_offsetted.parallel_offset(row_spacing, 'left', 5)
        if line_offsetted.geom_type == 'MultiLineString':  # if we got multiple lines take the longest
            line_offsetted = repair_multiple_parallel_offset_curves(line_offsetted)
        if not line_offsetted.is_simple:
            line_offsetted = repair_non_simple_lines(line_offsetted)

        if row_spacing < 0:
            line_offsetted = reverse_line_string(line_offsetted)
        line_offsetted = line_offsetted.simplify(0.01, False)
        res = line_offsetted.intersection(shape)
        if row_spacing > 0 and not isinstance(res, (shgeo.GeometryCollection, shgeo.MultiLineString)):
            if (res.is_empty or len(res.coords) == 1):
                row_spacing = -row_spacing

                line_offsetted = line.parallel_offset(row_spacing, 'left', 5)
                if line_offsetted.geom_type == 'MultiLineString':  # if we got multiple lines take the longest
                    line_offsetted = repair_multiple_parallel_offset_curves(
                        line_offsetted)
                if not line_offsetted.is_simple:
                    line_offsetted = repair_non_simple_lines(line_offsetted)
                # using negative row spacing leads as a side effect to reversed offsetted lines - here we undo this
                line_offsetted = reverse_line_string(line_offsetted)
                line_offsetted = line_offsetted.simplify(0.01, False)
                res = line_offsetted.intersection(shape)

    for row in rows:
        yield from row
