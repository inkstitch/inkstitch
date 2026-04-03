# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

from collections import deque

import networkx as nx
from shapely.affinity import rotate
from shapely.geometry import LineString, MultiPoint, Point
from shapely.ops import nearest_points

from ..stitch_plan import Stitch
from ..utils.threading import check_stop_flag
from .cross_stitch_half import half_cross_stitch
from .utils.cross_stitch import CrossGeometries


def cross_stitch(fill, shape, starting_point, ending_point):
    ''' Cross stitch fill

        Cross stitches are organized in a pixelated pattern. Each "cross pixel" has two diagonals.
        Traditionally cross stitches are strictly organized and each cross follows the same pattern.
        Meaning the layering of the diagonals can't be switched during the stitch out.
        For example all crosses start with '\' as a bottom layer and end with '/' as the top layer.

        In machine embroidery we do not have the freedom a hand embroiderer has.
        In order to jump from one stitch to an other, we will need to stitch at the crosses centers,
        but we try to hide those center stitches whenever possible.

        In Ink/Stitch cross stitches come in four flavours.
        - simple cross (two diagonals) and it's reverse (flipped) variant
        - upright cross (horizontal, vertical) and it's reverse (flipped) variant
        - half stitches (only one diagonal) and it's reverse (flipped) variant)
        - double crosses (combined simple and upright cross)
    '''
    # thread count is strictly positive
    thread_count = abs(fill.cross_thread_count)
    rotation_center, shape = _grid_rotate(fill, shape)
    if fill.cross_stitch_method.startswith('half'):
        # half stitches only differ from auto-fill in
        # - their pixelated outline
        # - thread count option (bean stitch repeats)
        #   bean stitch repeats will always return an odd thread count, opposed to the other cross stitch methods
        thread_count = thread_count // 2
        stitches = half_cross_stitch(fill, shape, starting_point, ending_point, thread_count)
        stitches = _grid_unrotate(stitches, fill.cross_rotation, rotation_center)
        return [stitches]
    # cross stitch method only takes even thread counts
    # it starts and ends at the same position
    if starting_point is None:
        starting_point = ending_point
        ending_point = None
    if thread_count % 2 != 0:
        thread_count -= 1
    stitches = even_cross_stitch(fill, shape, starting_point, ending_point, thread_count)
    if fill.cross_rotation != 0:
        rotated_stitches = []
        for stitch_group in stitches:
            rotated_stitches.append(_grid_unrotate(stitch_group, fill.cross_rotation, rotation_center))
        stitches = rotated_stitches
    return stitches


def _grid_rotate(fill, shape):
    # When we rotate a cross stitch shape (for example with lettering along path)
    # we want to preserve the cross stitch positions of the unrotated shape
    # It is way easier to rotate the shape and rotate it back, than trying to apply the rotations on each cross stitch area
    # The rotation center is taken from inkscapes transform center values, so that users can actually manipulate the effect
    if fill.cross_rotation == 0:
        return (0, 0), shape

    minx, miny, maxx, maxy = shape.bounds
    rotation_center_x = fill.node.get('inkscape:transform-center-x', None)
    rotation_center_y = fill.node.get('inkscape:transform-center-y', None)
    if not fill.canvas_grid_origin and rotation_center_x and rotation_center_y:
        center = list(LineString([(minx, miny), (maxx, maxy)]).centroid.coords[0])
        rotation_center_x_px = fill.node.unit_to_viewport(rotation_center_x)
        rotation_center_y_px = fill.node.unit_to_viewport(rotation_center_y)
        x = center[0] + rotation_center_x_px
        y = center[1] - rotation_center_y_px
        rotation_center = (x, y)
    elif not fill.canvas_grid_origin:
        rotation_center = (minx, maxy)
    else:
        rotation_center = fill.cross_offset
    rotated_shape = rotate(shape, -fill.cross_rotation, origin=rotation_center)
    return rotation_center, rotated_shape


def _grid_unrotate(stitches, angle, origin):
    if angle == 0:
        return stitches
    # Reverse the rotation we have applied to the cross stitch shape (fill.cross_rotation)
    rotated_stitches = []
    for stitch_list in stitches:
        rotated_stitches.append([stitch.rotate(angle, origin) for stitch in stitch_list])
    return rotated_stitches


def even_cross_stitch(fill, shape, starting_point, ending_point, thread_count):
    """ Cross stitch algorithm for all cross stitch types except for half crosses and their reverse version

        Steps:
        - Determine cross geometries from the given fill shape
        - Get connected subgraphs (cross geometries may split the shape in narrow areas)
        - Construct an eulerian cycle for each subgraph, by ensuring that no cross is flipped

        fill:                   the fill element
        shape:                  shape as MultiPolygon
        starting_point:         defines where to start
        ending_point:           defines where to end
        thread_number:          defines the thread count (even number, otherwise rounded to the previous even integer, exception: 1 = 2)
    """
    method = fill.cross_stitch_method

    flipped = "flip" in method

    if flipped:
        # "Flip" means to swap the order that the cross stitches are sewn in.
        # We handle that by rotating the shape and running the algorithm as
        # usual, then rotating the resulting stitches.  That way we don't have
        # to consider flipping in our stitch generation.

        if starting_point:
            starting_point = _rotate_coords(Point(starting_point).x, Point(starting_point).y)

        if ending_point:
            ending_point = _rotate_coords(Point(ending_point).x, Point(ending_point).y)
        shape = rotate(shape, 90, origin=(0, 0))

    cross_geoms = CrossGeometries(shape, fill.pattern_size, fill.fill_coverage, method, fill.cross_offset, fill.canvas_grid_origin, thread_count)

    subgraphs = _build_connect_subgraphs(cross_geoms)

    eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms)

    stitches = _cycles_to_stitches(eulerian_cycles, fill.max_cross_stitch_length, flipped)
    if stitches:
        return [stitches]
    else:
        return []


def get_corner(point, subcrosses):
    '''Snap point on existing corners on our cross stitch pattern
    starting_point is not None when called
    '''
    snap_points = MultiPoint([corner for cross in subcrosses for corner in cross.all_connection_points])
    start_point = nearest_points(snap_points, Point(point))[0]
    corner = (start_point.x, start_point.y)
    return corner


def _build_connect_subgraphs(cross_geoms):
    """  first build the graph
    add first the nodes: each node is either a center point or a corner of a cross
    edges are between center point and corners,
    the other edges are not inserted as they are not useful to find the
    connected components
    each node carries the list of crosses it belongs to
    then add the edges
    finally extract the connected components as subgraphs """

    G = nx.Graph()

    for cross in cross_geoms.crosses:
        center = cross.center_point
        G.add_node(center, crosses=[cross])
        connection_points = cross.all_connection_points
        for point in connection_points:
            if point in G.nodes:
                G.nodes[point]['crosses'].append(cross)
            else:
                G.add_node(point, crosses=[cross])

        for point in cross.all_connection_points:
            G.add_edge(center, point)

    return [G.subgraph(c).copy() for c in nx.connected_components(G)]


def _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms):
    """ We need to construct an eulerian cycle for each subgraph,
        but we need to make sure that no cross is flipped
        So we construct partial cycles (tours) that cover rows of crosses without flipping any cross
        and we insert those partial cycles into the eulerian cycle until all crosses are covered

        We use a slightly different row tour, depending whether the starting point is above or below
        the center of the first cross

        diagonals will be added as many times as needed, depending on the number of threads,
        in a bean stitch fashion
    """

    eulerian_cycles = []
    travel, starting_point, ending_point = organize(subgraphs, cross_geoms, starting_point, ending_point)

    for i, subgraph in enumerate(subgraphs):
        subcrosses = set(find_available_crosses(subgraph, cross_geoms.crosses))
        if not subcrosses:
            continue

        if i == 0 and starting_point:
            starting_corner = get_corner(starting_point, subcrosses)
        elif i == len(subgraphs)-1 and ending_point:
            starting_corner = get_corner(ending_point, subcrosses)
        else:
            # chose a good corner belonging to only one cross to avoid starting inside the shape
            for cross in subcrosses:
                starting_corner = cross.good_points[0]
                if len(cross_geoms.crosses_by_good_point[starting_corner]) + len(cross_geoms.crosses_by_bad_point[starting_corner]) == 1:
                    break
                starting_corner = cross.good_points[1]
                if len(cross_geoms.crosses_by_good_point[starting_corner]) + len(cross_geoms.crosses_by_bad_point[starting_corner]) == 1:
                    break

        cycle = travel + _build_simple_cycles(subcrosses, cross_geoms, starting_corner)
        travel = []

        eulerian_cycles.append(cycle)

    return eulerian_cycles


def _build_simple_cycles(subcrosses, cross_geoms, starting_point):
    possible_crosses = cross_geoms.crosses_by_good_point[starting_point] + cross_geoms.crosses_by_bad_point[starting_point]
    cross = possible_crosses[0]
    path = deque(cross.cycle_from_point(starting_point))
    cross_geoms.remove_cross(cross)
    subcrosses.remove(cross)

    # possible optimization: once we've checked a section of the path for both
    # good and bad points, we never need to check that section again

    while subcrosses:
        new_path = deque()
        while path:
            check_stop_flag()

            current_point = path.popleft()
            new_path.append(current_point)
            for cross in list(cross_geoms.crosses_by_good_point[current_point]):
                # must reverse because deque.extendleft() reverses the sequence
                # when extending on the left
                path.extendleft(reversed(cross.cycle_from_point(current_point)))
                cross_geoms.remove_cross(cross)
                subcrosses.remove(cross)
        path = new_path

        check_stop_flag()

        if subcrosses:
            new_path = deque()
            while path:
                current_point = path.popleft()
                new_path.append(current_point)
                if cross_geoms.crosses_by_bad_point.get(current_point):
                    cross = cross_geoms.crosses_by_bad_point[current_point][0]
                    new_path.extend(cross.cycle_from_point(current_point))
                    new_path.extend(path)
                    cross_geoms.remove_cross(cross)
                    subcrosses.remove(cross)
                    break
            path = new_path

    path.appendleft(starting_point)
    return list(path)


def organize(subgraphs, cross_geoms, starting_point, ending_point):
    # Make the subgraph containing the starting_point the first one
    # And make the one containing the ending_point the last one
    # If both starting  and ending point are both in the now first subgraph
    # travel will be a shortest path from starting to ending point and
    # ending  point becomes  the starting point of the eulerian tour

    if cross_geoms.crosses and starting_point:
        starting_corner, first_subgraph = find_index_subgraph(subgraphs, cross_geoms.crosses, starting_point)
        subgraphs[0], subgraphs[first_subgraph] = subgraphs[first_subgraph], subgraphs[0]

    if cross_geoms.crosses and starting_point and ending_point:
        ending_corner, last_subgraph = find_index_subgraph(subgraphs, cross_geoms.crosses, ending_point)
        subgraphs[-1], subgraphs[last_subgraph] = subgraphs[last_subgraph], subgraphs[-1]

    travel = []
    if cross_geoms.crosses and starting_point and ending_point and last_subgraph == 0:
        try:
            travel = nx.shortest_path(subgraphs[0], source=starting_corner, target=ending_corner)
        except nx.NodeNotFound:
            pass
        starting_point = ending_point

    return travel, starting_point, ending_point


def find_index_subgraph(subgraphs, crosses, point):
    corner = get_corner(point, crosses)
    index = 0
    while corner not in list(subgraphs[index].nodes):
        index += 1
    return corner, index


def is_cross_in_subgraph(cross, subgraph):

    if cross.center_point not in list(subgraph.nodes()):
        return False
    for corner in cross.all_connection_points:
        if corner not in list(subgraph.nodes):
            return False
    return True


def find_available_crosses(subgraph, crosses):
    return [cross for cross in crosses if is_cross_in_subgraph(cross, subgraph)]


def _rotate_coords(x, y):
    return -y, x


def _unrotate_coords(x, y):
    return y, -x


def _cycles_to_stitches(eulerian_cycles, max_stitch_length, flip):
    stitches = []
    for cycle in eulerian_cycles:
        cycle_stitches = []
        if cycle is not None:
            last_point = cycle[0]
            if flip:
                last_point = _unrotate_coords(*last_point)
            cycle_stitches.append(Stitch(*last_point, tags=["cross_stitch"]))
            for point in cycle[1:]:
                if flip:
                    point = _unrotate_coords(*point)
                if point == last_point:
                    continue
                line = LineString([last_point, point]).segmentize(max_stitch_length)
                for coord in line.coords:
                    cycle_stitches.append(Stitch(*coord, tags=["cross_stitch"]))
                last_point = point
        stitches.append(cycle_stitches)
    return stitches
