# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

import networkx as nx
from shapely.geometry import MultiPoint, Point, LineString
from shapely.ops import nearest_points

from ..stitch_plan import Stitch
from .utils.cross_stitch import CrossGeometries
from .cross_stitch_half import half_cross_stitch


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
    if fill.cross_stitch_method.startswith('half'):
        # half stitches only differ from auto-fill in
        # - their pixelated outline
        # - thread count option (bean stitch repeats)
        #   bean stitch repeats will always return an odd thread count, opposed to the other cross stitch methods
        thread_count = thread_count // 2
        return half_cross_stitch(fill, shape, starting_point, ending_point, thread_count)
    # cross stitch method only takes even thread counts
    # it starts and ends at the same position
    if starting_point is None:
        starting_point = ending_point
        ending_point = None
    if thread_count % 2 != 0:
        thread_count -= 1
    return even_cross_stitch(fill, shape, starting_point, ending_point, thread_count)


def even_cross_stitch(fill, shape, starting_point, ending_point, threads_number):
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
    nb_repeats = (threads_number // 2) - 1
    method = fill.cross_stitch_method

    cross_geoms = CrossGeometries(shape, fill.pattern_size, fill.fill_coverage, method, fill.cross_offset, fill.canvas_grid_origin)
    subgraphs = _build_connect_subgraphs(cross_geoms)
    eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms, nb_repeats, method)
    stitches = _cycles_to_stitches(eulerian_cycles, fill.max_cross_stitch_length)
    return [stitches]


def get_good_corner(point, subcrosses, starting_positions):
    # starting_positions are the two positions in the cross from where we can tour
    # a cross while respecting diagonal order and hiding center stitches
    # under last diagonal.

    '''Snap point on existing  good corners on our cross stitch pattern
    starting_point is not None when called
    '''
    snap_points = MultiPoint([cross.get(starting_positions[0]) for cross in subcrosses]
                             +
                             [cross.get(starting_positions[1]) for cross in subcrosses])
    start_point = nearest_points(snap_points, Point(point))[0]
    corner = (start_point.x, start_point.y)
    return corner


def _build_connect_subgraphs(cross_geoms):
    """  first build the graph
    add first the nodes: each node is either a center point or a corner of a cross
    edges are between center point and corners, and between opposite corners
    each node carries the list of crosses it belongs to
    then add the edges
    finally extract the connected components as subgraphs """

    G = nx.Graph()

    for cross in cross_geoms.crosses:
        center = cross.center_point
        G.add_node(center, crosses=[cross])
        corners = cross.corners
        for corner in corners:
            if corner in G.nodes:
                G.nodes[corner]['crosses'].append(cross)
            else:
                G.add_node(corner, crosses=[cross])

        for corner in cross.corners:
            G.add_edge(center, corner)
        G.add_edge(corners[0], corners[2])
        G.add_edge(corners[1], corners[3])

    return [G.subgraph(c).copy() for c in nx.connected_components(G)]


def _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms, nb_repeats, method):
    """ We need to construct an eulerian cycle for each subgraph,
        but we need to make sure that no cross is flipped
        we construct suitble cycle on each cross, and then we join them at suitable position
    """

    eulerian_cycles = []
    cross_order = ("top_right", "top_left", "bottom_right", "bottom_left")
    joining_positions = ["bottom_right", "top_left"]
    starting_positions = ["top_right", "bottom_left"]

    if "flipped" in method:
        # exchange  left and right
        cross_order = ("top_left", "top_right", "bottom_left", "bottom_right")
        joining_positions, starting_positions = starting_positions, joining_positions

    if method == "double_cross":
        cross_order = ("top_right", "middle_top", "middle_bottom", "middle_left", "middle_right", "top_left", "bottom_right", "bottom_left")

    travel, starting_good_corner, ending_good_corner = organize(subgraphs, cross_geoms, starting_point, ending_point, starting_positions)

    for i, subgraph in enumerate(subgraphs):
        # as much as we can we will use crosses in available_good_crosses, the stitching of such
        # a cross will respect diagonal order and no center stitch will show.
        # when  no such cross  is available, we will use a cross where diagonal order is still respected
        # but a center stitche will show.
        available_good_crosses = find_available_crosses(subgraph, cross_geoms.crosses, starting_positions)
        available_bad_crosses = find_available_crosses(subgraph, cross_geoms.crosses, joining_positions)
        if len(available_good_crosses) == 0 and len(available_bad_crosses) == 0:
            continue

        if i == 0 and starting_good_corner:
            # starting_good_corner exists, and therefore belongs to subgrpahs[O]
            if not ending_good_corner or travel == []:
                first_cross = list(available_good_crosses.get(starting_good_corner))[0]
            else:  # ending_good_corner exists and belongs to subgraphs[0]
                first_cross = list(available_good_crosses.get(ending_good_corner))[0]
        elif i == len(subgraphs) - 1 and ending_good_corner and travel != []:
            # both starting and ending good_corner exists but they are in different subgraphs
            # ending_good_corner is in the last subbgraph
            first_cross = list(available_good_crosses.get(ending_good_corner))[0]
        else:
            # for all other cases
            #  any good corner will do
            starting_corner = list(available_good_crosses.keys())[0]
            first_cross = list(available_good_crosses.get(starting_corner))[0]

        if method == "double_cross":
            cycle = double_cross_cycle(first_cross, nb_repeats, cross_order)
        else:
            cycle = cross_cycle(first_cross, nb_repeats, cross_order)

        available_good_crosses = remove_cross(first_cross, available_good_crosses, starting_positions)
        available_bad_crosses = remove_cross(first_cross, available_bad_crosses, joining_positions)

        cycle = _build_simple_cycles(available_good_crosses, available_bad_crosses, cycle, nb_repeats, cross_order)

        cycle = travel + cycle
        travel = []

        eulerian_cycles.append(cycle)

    return eulerian_cycles


def remove_cross(cross, available_crosses, positions):
    for pos in list(positions):
        node = cross.get(pos)
        if available_crosses.get(node) and cross in available_crosses.get(node):
            available_crosses.get(node).remove(cross)
            if available_crosses.get(node) == []:
                del (available_crosses[node])

    return available_crosses


def double_cross_cycle(cross, nb_repeats, cross_order):
    pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8 = cross_order

    top_left = cross.get(pos1)
    center = cross.get('center_point')
    middle_top = cross.get(pos2)
    middle_bottom = cross.get(pos3)
    middle_left = cross.get(pos4)
    middle_right = cross.get(pos5)
    top_right = cross.get(pos6)
    bottom_left = cross.get(pos7)
    bottom_right = cross.get(pos8)

    double_cycle = [top_left, center, middle_top, middle_bottom]
    for i in range(nb_repeats):
        double_cycle.append(middle_top)
        double_cycle.append(middle_bottom)
    double_cycle += [center, middle_left, middle_right]
    for i in range(nb_repeats):
        double_cycle.append(middle_left)
        double_cycle.append(middle_right)
    double_cycle += [center, top_right, bottom_left]
    for i in range(nb_repeats):
        double_cycle.append(top_right)
        double_cycle.append(bottom_left)
    double_cycle += [center, bottom_right, top_left]
    for i in range(nb_repeats):
        double_cycle.append(bottom_right)
        double_cycle.append(top_left)

    return double_cycle


def cross_cycle(cross, nb_repeats, cross_order):
    pos1, pos2, pos3, pos4 = cross_order
    cycle = [cross.get(pos1)]
    cycle.append(cross.center_point)
    cycle.append(cross.get(pos2))
    cycle.append(cross.get(pos3))
    for i in range(nb_repeats):
        cycle.append(cross.get(pos2))
        cycle.append(cross.get(pos3))
    cycle.append(cross.center_point)
    cycle.append(cross.get(pos4))
    cycle.append(cross.get(pos1))
    for i in range(nb_repeats):
        cycle.append(cross.get(pos4))
        cycle.append(cross.get(pos1))
    return cycle


def _build_simple_cycles(available_good_crosses, available_bad_crosses, cycle, nb_repeats, cross_order):
    # we want to insert as many good_crosses as we can into the cycle
    # when we can't anymore, we insert a bad cross (meaning that there will be a visible center point stitch)

    i = 0  # no good cycle can be inserted into cycle[:i]
    j = 0  # no good and no bad cycle can be inserted into cycle [j:]

    if len(cross_order) == 4:
        # not using double_cross method
        construct_cycle = cross_cycle
        # when using a bad sinple cycle we will shift it by 2 position to start at its first  good corner
        shift_by = 2
    else:
        # using double_cross method
        construct_cycle = double_cross_cycle
        # when using a bad sinple cycle we will shift it by this number of  positions to start at its first  good corner
        shift_by = 7 + (4 * nb_repeats)

    while len(available_good_crosses) != 0 and len(available_bad_crosses) != 0:
        # we want to use good_crosses as much as possible
        while i < len(cycle) and not available_good_crosses.get(cycle[i]):
            i += 1
        if i < len(cycle):
            new_cross = available_good_crosses.get(cycle[i])[0]
            new_cross_cycle = construct_cycle(new_cross, nb_repeats, cross_order)
            if new_cross_cycle[0] != cycle[i]:
                new_cross_cycle = construct_cycle(new_cross, nb_repeats, reverse_order(cross_order))
            cycle = cycle[:i] + new_cross_cycle + cycle[i:]
            available_good_crosses = remove_cross(new_cross, available_good_crosses, cross_order)
            available_bad_crosses = remove_cross(new_cross, available_bad_crosses, cross_order)
        else:   # no more good cycle, let us pick a bad one
            while j < len(cycle) and not available_bad_crosses.get(cycle[j]):
                j += 1
            new_cross = available_bad_crosses.get(cycle[j])[0]
            new_cross_cycle = construct_cycle(new_cross, nb_repeats, cross_order)
            if new_cross_cycle[shift_by] != cycle[j]:
                new_cross_cycle = construct_cycle(new_cross, nb_repeats, reverse_order(cross_order))

            cycle = cycle[:j] + new_cross_cycle[shift_by:] + new_cross_cycle[:shift_by]+cycle[j:]
            i = j
            available_good_crosses = remove_cross(new_cross, available_good_crosses, cross_order)
            available_bad_crosses = remove_cross(new_cross, available_bad_crosses, cross_order)

    return cycle


def reverse_order(cross_order):
    if len(cross_order) == 4:
        return cross_order[::-1]
    else:
        pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8 = cross_order
        return (pos8, pos2, pos3, pos4, pos5, pos6, pos7, pos1)


def organize(subgraphs, cross_geoms, starting_point, ending_point, starting_positions):
    # Make the subgraph containing the starting_point the first one
    # And make the one containing the ending_point the last one
    # If both starting  and ending point are both in the now first subgraph
    # travel will be a shortest path from starting to ending point and
    # ending  point becomes  the starting point of the eulerian tour

    starting_good_corner = starting_point
    ending_good_corner = ending_point
    start_and_end_in_same_subgraph = False

    if cross_geoms.crosses and starting_point:
        starting_good_corner, first_subgraph = find_index_subgraph(subgraphs, cross_geoms.crosses, starting_point, starting_positions)
        subgraphs[0], subgraphs[first_subgraph] = subgraphs[first_subgraph], subgraphs[0]

    if cross_geoms.crosses and starting_point and ending_point:
        ending_good_corner, last_subgraph = find_index_subgraph(subgraphs, cross_geoms.crosses, ending_point, starting_positions)
        if last_subgraph != 0:
            subgraphs[-1], subgraphs[last_subgraph] = subgraphs[last_subgraph], subgraphs[-1]
        if last_subgraph == 0:
            start_and_end_in_same_subgraph = True

    travel = []
    # if both starting_point and ending_point are defined and are in the same subgraph
    # then they both belong to subgraphs[0]
    # in that case, in subgraphs[0] we first travel from starting_point to ending_point then use the eulerian_cycle in sub
    # if they are both defined but not in the same subgraph

    if cross_geoms.crosses and starting_point and ending_point and start_and_end_in_same_subgraph:
        try:
            travel = nx.shortest_path(subgraphs[0], source=starting_good_corner, target=ending_good_corner)
        except nx.NodeNotFound:
            pass

    return travel, starting_good_corner, ending_good_corner


def find_index_subgraph(subgraphs, crosses, point, starting_positions):
    # point is not None when this function is called
    # return the closest good corner from point, and the index of the subgraph that contains it
    corner = get_good_corner(point, crosses, starting_positions)
    index = 0
    while corner not in list(subgraphs[index].nodes):
        index += 1
    return corner, index


def is_cross_in_subgraph(cross, subgraph):

    if cross.center_point not in list(subgraph.nodes()):
        return False
    for corner in cross.corners:
        if corner not in list(subgraph.nodes):
            return False
    return True


def find_available_crosses(subgraph, crosses, positions):
    # construct a dictionary,with nodes as key and value is a list of crosses of the subbgraph
    # where node is at one of the positions
    # list may have length 0, 1 or 2
    crosses = [cross for cross in crosses if is_cross_in_subgraph(cross, subgraph)]
    available_crosses = {}
    centers = [cross.center_point for cross in crosses]
    for node in list(subgraph.nodes):
        if node not in centers:
            available_crosses.setdefault(node, [])
    for cross in crosses:
        for position in list(positions):
            node = cross.get(position)
            available_crosses.get(node).append(cross)
    for node in list(subgraph.nodes):
        if available_crosses.get(node) == []:
            del (available_crosses[node])
    return available_crosses


def _cycles_to_stitches(eulerian_cycles, max_stitch_length):
    stitches = []
    for cycle in eulerian_cycles:
        if cycle is not None:
            last_point = cycle[0]
            stitches.append(Stitch(*last_point, tags=["cross_stitch"]))
            for point in cycle[1:]:
                if point == last_point:
                    continue
                line = LineString([last_point, point]).segmentize(max_stitch_length)
                for coord in line.coords:
                    stitches.append(Stitch(*coord, tags=["cross_stitch"]))
                last_point = point
    return stitches
