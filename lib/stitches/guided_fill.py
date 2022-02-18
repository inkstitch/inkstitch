import networkx
from depq import DEPQ
from shapely.geometry import GeometryCollection, LineString, MultiLineString
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

from ..debug import debug
from ..i18n import _
from ..stitch_plan import Stitch
from ..svg import PIXELS_PER_MM
from ..utils.geometry import Point as InkstitchPoint
from .auto_fill import (add_edges_between_outline_nodes, build_travel_graph,
                        collapse_sequential_outline_edges, fallback,
                        find_stitch_path, graph_is_valid, insert_node,
                        tag_nodes_with_outline_and_projection, travel,
                        weight_edges_by_length)
from .point_transfer import transfer_points_to_surrounding_graph
from .sample_linestring import raster_line_string_with_priority_points


@debug.time
def guided_fill(shape,
                guideline,
                angle,
                row_spacing,
                max_stitch_length,
                running_stitch_length,
                skip_last,
                starting_point,
                ending_point=None,
                underpath=True,
                offset_by_half=True):

    fill_stitch_graph = []
    try:
        fill_stitch_graph = build_guided_fill_stitch_graph(
            shape, guideline, row_spacing, starting_point, ending_point)
    except ValueError:
        # Small shapes will cause the graph to fail - min() arg is an empty sequence through insert node
        return fallback(shape, running_stitch_length)

    if not graph_is_valid(fill_stitch_graph, shape, max_stitch_length):
        return fallback(shape, running_stitch_length)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(path, travel_graph, fill_stitch_graph, angle, row_spacing,
                              max_stitch_length, running_stitch_length, skip_last, offset_by_half)

    return result


@debug.time
def build_guided_fill_stitch_graph(shape, guideline, row_spacing, starting_point=None, ending_point=None):
    """build a graph representation of the grating segments

    This function builds a specialized graph (as in graph theory) that will
    help us determine a stitching path.  The idea comes from this paper:

    http://www.sciencedirect.com/science/article/pii/S0925772100000158

    The goal is to build a graph that we know must have an Eulerian Path.
    An Eulerian Path is a path from edge to edge in the graph that visits
    every edge exactly once and ends at the node it started at.  Algorithms
    exist to build such a path, and we'll use Hierholzer's algorithm.

    A graph must have an Eulerian Path if every node in the graph has an
    even number of edges touching it.  Our goal here is to build a graph
    that will have this property.

    Based on the paper linked above, we'll build the graph as follows:

        * nodes are the endpoints of the grating segments, where they meet
        with the outer outline of the region the outlines of the interior
        holes in the region.
        * edges are:
        * each section of the outer and inner outlines of the region,
            between nodes
        * double every other edge in the outer and inner hole outlines

    Doubling up on some of the edges seems as if it will just mean we have
    to stitch those spots twice.  This may be true, but it also ensures
    that every node has 4 edges touching it, ensuring that a valid stitch
    path must exist.
    """

    debug.add_layer("auto-fill fill stitch")

    rows_of_segments = intersect_region_with_grating_guideline(shape, guideline, row_spacing)

    # segments = [segment for row in rows_of_segments for segment in row]

    graph = networkx.MultiGraph()

    for i in range(len(rows_of_segments)):
        for segment in rows_of_segments[i]:
            # First, add the grating segments as edges.  We'll use the coordinates
            # of the endpoints as nodes, which networkx will add automatically.

            # networkx allows us to label nodes with arbitrary data.  We'll
            # mark this one as a grating segment.
            # graph.add_edge(*segment, key="segment", underpath_edges=[])
            previous_neighbors = [(seg[0], seg[-1])
                                  for seg in rows_of_segments[i-1] if i > 0]
            next_neighbors = [(seg[0], seg[-1]) for seg in rows_of_segments[(i+1) %
                              len(rows_of_segments)] if i < len(rows_of_segments)-1]

            graph.add_edge(segment[0], segment[-1], key="segment", underpath_edges=[],
                           geometry=LineString(segment), previous_neighbors=previous_neighbors, next_neighbors=next_neighbors,
                           projected_points=DEPQ(iterable=None, maxlen=None), already_rastered=False)

    tag_nodes_with_outline_and_projection(graph, shape, graph.nodes())
    add_edges_between_outline_nodes(graph, duplicate_every_other=True)

    if starting_point:
        insert_node(graph, shape, starting_point)

    if ending_point:
        insert_node(graph, shape, ending_point)

    debug.log_graph(graph, "graph")

    return graph


def get_segments(graph):
    segments = []
    for start, end, key, data in graph.edges(keys=True, data=True):
        if key == 'segment':
            segments.append(data["geometry"])

    return segments


def process_travel_edges(graph, fill_stitch_graph, shape, travel_edges):
    """Weight the interior edges and pre-calculate intersection with fill stitch rows."""

    # Set the weight equal to 5x the edge length, to encourage travel()
    # to avoid them.
    weight_edges_by_length(graph, 5)

    segments = get_segments(fill_stitch_graph)

    # The shapely documentation is pretty unclear on this.  An STRtree
    # allows for building a set of shapes and then efficiently testing
    # the set for intersection.  This allows us to do blazing-fast
    # queries of which line segments overlap each underpath edge.
    strtree = STRtree(segments)

    # This makes the distance calculations below a bit faster.  We're
    # not looking for high precision anyway.
    outline = shape.boundary.simplify(0.5 * PIXELS_PER_MM, preserve_topology=False)

    for ls in travel_edges:
        # In most cases, ls will be a simple line segment.  If we're
        # unlucky, in rare cases we can get a tiny little extra squiggle
        # at the end that can be ignored.
        points = [InkstitchPoint(*coord) for coord in ls.coords]
        p1, p2 = points[0], points[-1]

        edge = (p1.as_tuple(), p2.as_tuple(), 'travel')

        for segment in strtree.query(ls):
            # It seems like the STRTree only gives an approximate answer of
            # segments that _might_ intersect ls.  Refining the result is
            # necessary but the STRTree still saves us a ton of time.
            if segment.crosses(ls):
                start = segment.coords[0]
                end = segment.coords[-1]
                fill_stitch_graph[start][end]['segment']['underpath_edges'].append(
                    edge)

        # The weight of a travel edge is the length of the line segment.
        weight = p1.distance(p2)

        # Give a bonus to edges that are far from the outline of the shape.
        # This includes the outer outline and the outlines of the holes.
        # The result is that travel stitching will tend to hug the center
        # of the shape.
        weight /= ls.distance(outline) + 0.1

        graph.add_edge(*edge, weight=weight)

    # without this, we sometimes get exceptions like this:
    # Exception AttributeError: "'NoneType' object has no attribute 'GEOSSTRtree_destroy'" in
    #   <bound method STRtree.__del__ of <shapely.strtree.STRtree instance at 0x0D2BFD50>> ignored
    del strtree


def stitch_line(stitches, stitching_direction, geometry, projected_points, max_stitch_length, row_spacing, skip_last, offset_by_half):
    if stitching_direction == 1:
        stitched_line, _ = raster_line_string_with_priority_points(
            geometry, 0.0, geometry.length, max_stitch_length, projected_points, abs(row_spacing), offset_by_half, True)
    else:
        stitched_line, _ = raster_line_string_with_priority_points(
            geometry, geometry.length, 0.0, max_stitch_length, projected_points, abs(row_spacing), offset_by_half, True)

    stitches.append(Stitch(*stitched_line[0], tags=('fill_row_start',)))
    for i in range(1, len(stitched_line)-1):
        stitches.append(Stitch(*stitched_line[i], tags=('fill_row')))

    if not skip_last:
        if stitching_direction == 1:
            stitches.append(
                Stitch(*geometry.coords[-1], tags=('fill_row_end',)))
        else:
            stitches.append(
                Stitch(*geometry.coords[0], tags=('fill_row_end',)))


@debug.time
def path_to_stitches(path, travel_graph, fill_stitch_graph, angle, row_spacing, max_stitch_length,
                     running_stitch_length, skip_last, offset_by_half):
    path = collapse_sequential_outline_edges(path)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for edge in path:
        if edge.is_segment():
            new_stitches = []
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']
            projected_points = current_edge['projected_points']
            stitching_direction = 1
            if (abs(edge[0][0]-path_geometry.coords[0][0])+abs(edge[0][1]-path_geometry.coords[0][1]) >
                    abs(edge[0][0]-path_geometry.coords[-1][0])+abs(edge[0][1]-path_geometry.coords[-1][1])):
                stitching_direction = -1
            stitch_line(new_stitches, stitching_direction, path_geometry, projected_points,
                        max_stitch_length, row_spacing, skip_last, offset_by_half)
            current_edge['already_rastered'] = True
            transfer_points_to_surrounding_graph(
                fill_stitch_graph, current_edge, row_spacing, False, new_stitches, overnext_neighbor=True)
            transfer_points_to_surrounding_graph(fill_stitch_graph, current_edge, row_spacing, offset_by_half,
                                                 new_stitches, overnext_neighbor=False, transfer_forbidden_points=offset_by_half)

            stitches.extend(new_stitches)
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
    new_starting_point = point1-(point2-point1).unit()*length

    point3 = InkstitchPoint(*line.coords[-2])
    point4 = InkstitchPoint(*line.coords[-1])
    new_ending_point = point4+(point4-point3).unit()*length

    return LineString([new_starting_point.as_tuple()] +
                      line.coords[1:-1]+[new_ending_point.as_tuple()])


def repair_multiple_parallel_offset_curves(multi_line):
    # TODO: linemerge is overritten by the very next line?!?
    lines = linemerge(multi_line)
    lines = list(multi_line.geoms)
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
            _("Guide line (or offsetted instance) is self crossing!"))
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
    while isinstance(res, (GeometryCollection, MultiLineString)) or (not res.is_empty and len(res.coords) > 1):
        if isinstance(res, (GeometryCollection, MultiLineString)):
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
            line_offsetted.coords = line_offsetted.coords[::-1]
        line_offsetted = line_offsetted.simplify(0.01, False)
        res = line_offsetted.intersection(shape)
        if row_spacing > 0 and not isinstance(res, (GeometryCollection, MultiLineString)):
            if (res.is_empty or len(res.coords) == 1):
                row_spacing = -row_spacing

                line_offsetted = line.parallel_offset(row_spacing, 'left', 5)
                if line_offsetted.geom_type == 'MultiLineString':  # if we got multiple lines take the longest
                    line_offsetted = repair_multiple_parallel_offset_curves(
                        line_offsetted)
                if not line_offsetted.is_simple:
                    line_offsetted = repair_non_simple_lines(line_offsetted)
                # using negative row spacing leads as a side effect to reversed offsetted lines - here we undo this
                line_offsetted.coords = line_offsetted.coords[::-1]
                line_offsetted = line_offsetted.simplify(0.01, False)
                res = line_offsetted.intersection(shape)
    return rows
