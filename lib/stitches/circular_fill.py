from networkx import is_empty
from shapely import geometry as shgeo
from shapely.ops import substring

from lib.utils import prng

from ..stitch_plan import Stitch
from ..utils.geometry import Point, reverse_line_string
from .auto_fill import (build_fill_stitch_graph, build_travel_graph,
                        collapse_sequential_outline_edges, fallback,
                        find_stitch_path, graph_make_valid, travel)
from .contour_fill import _make_fermat_spiral
from .running_stitch import bean_stitch, even_running_stitch, running_stitch


def circular_fill(shape,
                  angle,
                  row_spacing,
                  end_row_spacing,
                  num_staggers,
                  running_stitch_length,
                  running_stitch_tolerance,
                  bean_stitch_repeats,
                  repeats,
                  skip_last,
                  starting_point,
                  ending_point,
                  underpath,
                  target,
                  enable_random_stitch_length,
                  running_stitch_length_jitter,
                  random_seed,
                  ):

    # get furthest distance of the target point to a shape border
    # so we know how many circles we will need
    distance = shape.hausdorff_distance(target)
    radius = row_spacing
    center = shgeo.Point(target)

    if radius > distance:
        # if the shape is smaller than row_spacing, return a simple circle in the size of row_spacing
        stitches = even_running_stitch([Stitch(*point) for point in center.buffer(radius).exterior.coords],
                                       running_stitch_length, running_stitch_tolerance)
        return _apply_bean_stitch_and_repeats(stitches, repeats, bean_stitch_repeats)

    circles = []
    # add a small inner circle to make sure that the spiral ends close to the center
    circles.append(shgeo.LineString(center.buffer(0.1).exterior.coords))
    # add twice the size of the (end_)row_spacing to make sure we go big enough
    stopp_at_distance = distance + (end_row_spacing or row_spacing) * 2
    while radius < stopp_at_distance:
        circles.append(shgeo.LineString(center.buffer(radius).exterior.coords))
        if end_row_spacing:
            radius += row_spacing + (end_row_spacing - row_spacing) * (radius / distance)
        else:
            radius += row_spacing
    circles.reverse()

    # Use double spiral from contour fill (we don't want to get stuck in the middle of the spiral)
    double_spiral = _make_fermat_spiral(circles, running_stitch_length, circles[0].coords[0])
    double_spiral = shgeo.LineString(list(double_spiral))
    intersection = double_spiral.intersection(shape)

    if isinstance(intersection, shgeo.LineString):
        # if we get a single linestrig (original shape is a circle), apply start and end commands and return path
        path = list(intersection.coords)
        path = _apply_start_end_commands(shape, path, starting_point, ending_point)
        stitches = running_stitch([Stitch(*point) for point in path],
                                  running_stitch_length,
                                  running_stitch_tolerance,
                                  enable_random_stitch_length,
                                  running_stitch_length_jitter,
                                  random_seed)
        return _apply_bean_stitch_and_repeats(stitches, repeats, bean_stitch_repeats)

    segments = []
    for n, line in enumerate(intersection.geoms):
        if isinstance(line, shgeo.LineString):
            # use running stitch here to adjust the stitch length
            coords = running_stitch([Point(*point) for point in line.coords],
                                    [running_stitch_length],
                                    running_stitch_tolerance,
                                    enable_random_stitch_length,
                                    running_stitch_length_jitter,
                                    prng.join_args(random_seed, n))
            segments.append([(point.x, point.y) for point in coords])

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if is_empty(fill_stitch_graph):
        return fallback(shape, running_stitch_length, running_stitch_tolerance)
    graph_make_valid(fill_stitch_graph)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point, underpath)
    result = path_to_stitches(shape, path, travel_graph, fill_stitch_graph, running_stitch_length, running_stitch_tolerance, skip_last, underpath)
    result = _apply_bean_stitch_and_repeats(result, repeats, bean_stitch_repeats)
    return result


def _apply_bean_stitch_and_repeats(stitches, repeats, bean_stitch_repeats):
    if any(bean_stitch_repeats):
        # add bean stitches, but ignore travel stitches
        stitches = bean_stitch(stitches, bean_stitch_repeats, ['auto_fill_travel'])

    if repeats:
        for i in range(1, repeats):
            if i % 2 == 1:
                # reverse every other pass
                stitches.extend(stitches[::-1])
            else:
                stitches.extend(stitches)

    return stitches


def _apply_start_end_commands(shape, path, starting_point, ending_point):
    if starting_point or ending_point:
        outline = shape.boundary
        if isinstance(outline, shgeo.MultiLineString):
            outline = outline.geoms[0]
        if starting_point:
            start = _get_start_end_sequence(outline, shgeo.Point(*starting_point), shgeo.Point(*path[0]))
            path = list(start.coords) + path
        if ending_point:
            end = _get_start_end_sequence(outline, shgeo.Point(*path[-1]), shgeo.Point(*ending_point))
            path.extend(list(end.coords))
    return path


def _get_start_end_sequence(outline, start, end):
    start_dist = outline.project(start)
    end_dist = outline.project(end)
    return substring(outline, start_dist, end_dist)


def path_to_stitches(shape, path, travel_graph, fill_stitch_graph, running_stitch_length, running_stitch_tolerance, skip_last, underpath):
    path = collapse_sequential_outline_edges(path, fill_stitch_graph)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0], tags={'auto_fill_travel'}))

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
            stitches.extend(travel(shape, travel_graph, edge, [running_stitch_length], running_stitch_tolerance, skip_last, underpath))

    return stitches
