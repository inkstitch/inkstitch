# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# -*- coding: UTF-8 -*-

import networkx as nx
from shapely.geometry import MultiPoint, Point, LineString
from shapely.ops import nearest_points

from ..stitch_plan import Stitch
from ..utils.threading import check_stop_flag
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
    cross_geoms = CrossGeometries(fill, shape, method)
    subgraphs = _build_connect_subgraphs(cross_geoms)
    if method != "double_cross":
        eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms, nb_repeats, _build_row_tour, flipped=False)

        if "flipped" in method:
            eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms, nb_repeats, _build_row_tour, flipped=True)
            for i in range(len(eulerian_cycles)):
                eulerian_cycles[i] = eulerian_cycles[i][::-1]
    else:
        # flipped is not useful here but _build_eulerian_cycles requires it
        eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, ending_point,
                                                 cross_geoms, nb_repeats, _build_double_row_tour, flipped=False)

    stitches = _cycles_to_stitches(eulerian_cycles, fill.max_cross_stitch_length)
    return [stitches]


def get_corner(point, subcrosses):
    '''Snap point on existing corners on our cross stitch pattern
    starting_point is not None when called
    '''
    snap_points = MultiPoint([corner for cross in subcrosses for corner in cross.corners])
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


def _build_eulerian_cycles(subgraphs, starting_point, ending_point, cross_geoms, nb_repeats, row_tour, flipped):
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
    centers = cross_geoms.center_points
    travel, starting_point, ending_point = organize(subgraphs, cross_geoms, starting_point, ending_point)

    for i, subgraph in enumerate(subgraphs):
        subcrosses = find_available_crosses(subgraph, cross_geoms.crosses)
        if not subcrosses:
            continue

        if i == 0 and starting_point:
            starting_corner = get_corner(starting_point, subcrosses)
        elif i == len(subgraphs) and ending_point:
            starting_corner = get_corner(ending_point, subcrosses)
        else:
            # any corner will do
            index = 0
            while list(subgraph.nodes)[index] in centers:
                index += 1
            starting_corner = list(subgraph.nodes)[index]

        position, cycle = row_tour(subcrosses, starting_corner, nb_repeats, True)
        crosses = cross_geoms.crosses

        if row_tour == _build_row_tour:
            cycle = _build_simple_cycles(crosses, subcrosses, cycle, nb_repeats, flipped)
        else:
            cycle = _build_double_cycle(subcrosses, cycle, nb_repeats)

        cycle = travel + cycle
        travel = []

        eulerian_cycles.append(cycle)

    return eulerian_cycles


def _build_simple_cycles(crosses, subcrosses, cycle, nb_repeats, flipped):
    while subcrosses:
        # find a corner on the cycle that needs more crosses, so that we can enlarge the cycle
        potential_node = None
        for cross in subcrosses:
            for node in cross.corners:
                if node in cycle:
                    potential_node = node
                    break
            if potential_node:
                break
        if potential_node is None:
            break

        # here we try to minimize "bad traveling"

        # check if the insertion will be above or below
        position, cycle_to_insert = _build_row_tour(subcrosses, potential_node, nb_repeats, remove=False)
        # avoid bad traveling as much as possible
        if position == "below" and not flipped or position == "above" and flipped:
            node = insertion_node(crosses, potential_node, cycle, cycle_to_insert, position, True)
        else:
            node = insertion_node(crosses, potential_node, cycle, cycle_to_insert, position, False)

        position, cycle_to_insert = _build_row_tour(subcrosses, node, nb_repeats, remove=True)
        cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)

    return cycle


def _build_double_cycle(subcrosses, cycle, nb_repeats):
    while subcrosses:
        corners = [node for cross in subcrosses for node in cross.corners]
        for node in cycle:
            if node in corners:
                break
        _, cycle_to_insert = _build_double_row_tour(subcrosses, node, nb_repeats, remove=False)
        cycle = insert_cycle_at_node(cycle, cycle_to_insert, node,last_occurence=False)
    return cycle


def insertion_node(crosses, node, cycle, cycle_to_insert, position, favor_left):
    if position == "below":
        previous_node = insert_node_at_position(crosses, node, cycle, cycle_to_insert, favor_left, "bottom_right", "bottom_left")
    else:
        previous_node = insert_node_at_position(crosses, node, cycle, cycle_to_insert, favor_left, "top_right", "top_left")

    return previous_node


def insert_node_at_position(crosses, node, cycle, cycle_to_insert, favor_left, first_position, second_position):
    current_node = node
    next_node = None
    previous_node = current_node

    if favor_left:
        cross = cross_at_position(crosses, current_node, first_position)
        if cross:
            next_node = cross.get(second_position)
    else:
        cross = cross_at_position(crosses, current_node, second_position)
        if cross:
            next_node = cross.get(first_position)
    while cross and next_node in cycle and next_node in cycle_to_insert:
        previous_node = current_node
        current_node = next_node
        if favor_left:
            cross = cross_at_position(crosses, current_node, first_position)
            if cross:
                next_node = cross.get(second_position)
        else:
            cross = cross_at_position(crosses, current_node, second_position)
            if cross:
                next_node = cross.get(first_position)

    return previous_node


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


def _build_row_tour(subcrosses, starting_corner, nb_repeats, remove):
    position = None
    cross_order = ("top_right", "top_left", "bottom_right", "bottom_left")
    cycle = _build_side_row_tour(subcrosses, starting_corner, nb_repeats, remove, cross_order)
    if cycle:
        position = "above"
    if not cycle:
        cross_order = ("bottom_left", "bottom_right", "top_left", "top_right")
        cycle = _build_side_row_tour(subcrosses, starting_corner, nb_repeats, remove, cross_order)
        if cycle:
            position = "below"
    return position, cycle


def _build_double_row_tour(subcrosses, starting_corner, nb_repeats, remove=True):
    # position is not going to used , but we need same signature as for
    position = None
    cycle = _build_double_row_tour_above(subcrosses, starting_corner, nb_repeats)
    if cycle:
        position = "above"
    if not cycle:
        cycle = _build_double_row_tour_below(subcrosses, starting_corner, nb_repeats)
        if cycle:
            position = "below"
    return position, cycle


def find_index_subgraph(subgraphs, crosses, point):
    corner = get_corner(point, crosses)
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


def find_available_crosses(subgraph, crosses):
    return [cross for cross in crosses if is_cross_in_subgraph(cross, subgraph)]


def cross_at_position(crosses, node, position):
    for cross in crosses:
        if node == cross.get(position):
            return cross
    return None


def _build_double_row_tour_below(subcrosses, starting_corner, nb_repeats):
    tour = []

    cross_order = ("bottom_right", "top_left", "top_right", "bottom_left")
    tour += construct_side(subcrosses, starting_corner, nb_repeats, cross_order)

    cross_order = ("bottom_left", "top_right", "top_left", "bottom_right")
    tour += construct_side(subcrosses, starting_corner, nb_repeats, cross_order)

    return tour


def _build_double_row_tour_above(subcrosses, starting_corner, nb_repeats):
    tour = []
    cross_order = ("top_right", "bottom_left", "bottom_right", "top_left")
    tour += construct_side(subcrosses, starting_corner, nb_repeats, cross_order)

    cross_order = ("top_left", "bottom_right", "bottom_left", "top_right")
    tour += construct_side(subcrosses, starting_corner, nb_repeats, cross_order)
    return tour


def construct_side(subcrosses, starting_corner, nb_repeats, cross_order):
    pos1, pos2, pos3, pos4 = cross_order

    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner
    while cross_at_position(subcrosses, current_node, pos1):
        cross = cross_at_position(subcrosses, current_node, pos1)
        # first diagonal
        tour.append(cross.get(pos2))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross.get(pos2))
        tour.append(cross.center_point)
        tour.append(cross.get(pos3))
        # second diagonal
        tour.append(cross.get(pos4))
        for i in range(nb_repeats):
            tour.append(cross.get(pos3))
            tour.append(cross.get(pos4))
        current_node = cross.get(pos4)
    while current_node != starting_corner:
        # go back to starting_corner finishing the double crosses
        cross = cross_at_position(subcrosses, current_node, pos4)
        tour.append(cross.center_point)
        tour.append(cross.middle_left)
        # horizontal
        tour.append(cross.middle_right)
        for i in range(nb_repeats):
            tour.append(cross.middle_left)
            tour.append(cross.middle_right)
        tour.append(cross.center_point)
        tour.append(cross.middle_top)
        # vertical
        tour.append(cross.middle_bottom)
        for i in range(nb_repeats):
            tour.append(cross.middle_top)
            tour.append(cross.middle_bottom)
        tour.append(cross.center_point)
        tour.append(cross.get(pos1))
        current_node = cross.get(pos1)
        covered_crosses.append(cross)
    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def _build_side_row_tour(crosses, node, nb_repeats, remove, cross_order):
    pos1, pos2, pos3, pos4 = cross_order

    """build a tour of the row of crosses (among param crosses) above or below the given node
       ensuring that no cross is flipped,
       adding diagonals as needed depending on the number of threads
       remove the covered crosses from the crosses
       return empty list if no cross below
    """
    tour = [node]
    covered_crosses = []
    current_node = node
    while cross_at_position(crosses, current_node, pos1):
        tour.append(cross_at_position(crosses, current_node, pos1).center_point)
        tour.append(cross_at_position(crosses, current_node, pos1).get(pos2))
        current_node = cross_at_position(crosses, current_node, pos1).get(pos2)
        check_stop_flag()
    while cross_at_position(crosses, current_node, pos2):
        # add first diagonal of a cross
        tour.append(cross_at_position(crosses, current_node, pos2).get(pos3))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross_at_position(crosses, current_node, pos2).get(pos3))
        tour.append(cross_at_position(crosses, current_node, pos2).center_point)
        tour.append(cross_at_position(crosses, current_node, pos2).get(pos4))
        # add second diagonal of the same cross
        tour.append(cross_at_position(crosses, current_node, pos2).get(pos1))
        for i in range(nb_repeats):
            tour.append(cross_at_position(crosses, current_node, pos2).get(pos4))
            tour.append(cross_at_position(crosses, current_node, pos2).get(pos1))
        covered_crosses.append(cross_at_position(crosses, current_node, pos2))
        current_node = cross_at_position(crosses, current_node, pos2).get(pos1)
        check_stop_flag()
    while current_node != node:
        # This part of the tour is "bad traveling", going through center of crosses
        # after stitching last diagonal
        tour.append(cross_at_position(crosses, current_node, pos1).center_point)
        tour.append(cross_at_position(crosses, current_node, pos1).get(pos2))
        current_node = cross_at_position(crosses, current_node, pos1).get(pos2)
        check_stop_flag()
    if len(tour) > 1 and remove:
        remove_crosses(crosses, covered_crosses)
    if len(tour) > 1:
        return tour
    else:
        return []


def remove_crosses(crosses, covered_crosses):
    for cross in covered_crosses:
        crosses.remove(cross)


def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1


def insert_cycle_at_node(cycle_to_increase, cycle_to_insert, node,last_occurence=True):
    if node in cycle_to_increase:
        if last_occurence:
            index = rindex(cycle_to_increase, node)
        else:
            index = cycle_to_increase.index(node)
        new_cycle = cycle_to_increase[:index] + cycle_to_insert + cycle_to_increase[index+1:]
        return new_cycle


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
