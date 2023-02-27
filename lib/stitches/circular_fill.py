from shapely import geometry as shgeo

from ..stitch_plan import Stitch
from ..utils.geometry import reverse_line_string
from .auto_fill import (build_fill_stitch_graph, build_travel_graph,
                        collapse_sequential_outline_edges, fallback,
                        find_stitch_path, graph_is_valid, travel)
from .contour_fill import _make_fermat_spiral
from .running_stitch import running_stitch


def circular_fill(shape,
                  angle,
                  row_spacing,
                  num_staggers,
                  running_stitch_length,
                  running_stitch_tolerance,
                  skip_last,
                  starting_point,
                  ending_point,
                  underpath,
                  target
                  ):

    # get furthest distance of the target point to a shape border
    # so we know how many circles we will need
    distance = shape.hausdorff_distance(target) + 1
    radius = row_spacing
    center = shgeo.Point(target)

    circles = []
    # add a small inner circle to make sure that the spiral ends close to the center
    circles.append(shgeo.LineString(center.buffer(0.1).exterior.coords))
    while distance > radius:
        circles.append(shgeo.LineString(center.buffer(radius).exterior.coords))
        radius += row_spacing
    circles.reverse()

    # Use double spiral from contour fill (we don't want to get stuck in the middle of the spiral)
    double_spiral = _make_fermat_spiral(circles, running_stitch_length, circles[0].coords[0])
    double_spiral = shgeo.LineString(list(double_spiral))
    intersection = double_spiral.intersection(shape)

    segments = []
    for line in intersection.geoms:
        if isinstance(line, shgeo.LineString):
            segments.append(line.coords[:])

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)
    if not graph_is_valid(fill_stitch_graph, shape, running_stitch_length):
        return fallback(shape, running_stitch_length, running_stitch_tolerance)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(path, travel_graph, fill_stitch_graph, running_stitch_length, running_stitch_tolerance, skip_last)

    # use running stitch to adjust the stitch length
    result = running_stitch(result,
                            running_stitch_length,
                            running_stitch_tolerance)

    return result


def path_to_stitches(path, travel_graph, fill_stitch_graph, running_stitch_length, running_stitch_tolerance, skip_last):
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
            stitches.extend(travel(travel_graph, edge[0], edge[1], running_stitch_length, running_stitch_tolerance, skip_last))

    return stitches
