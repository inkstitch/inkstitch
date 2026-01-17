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
from math import floor
from .cross_stitch_half import half_cross_stitch


def cross_stitch(fill, shape, starting_point, ending_point):
    # thread count is strictly positive
    thread_count = abs(fill.cross_thread_count)
    if fill.cross_stitch_method in ['half_cross', 'half_cross_flipped']:
        # half stitches are more like a auto-fill stitch type, except for their blockish look
        thread_count = floor(thread_count / 2)
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
    """ We need to construct an eulerian cycle for each subgraph, but we need to make sure
    that no cross is flipped
    So we construct partial cycles (tours) that cover rows of crosses without flipping any cross
    and we insert those partial cycles into the eulerian cycle until all crosses are covered

    We use a slightly different row tour, depending whether the starting point is above or below
    the center of the first cross

    diagonals will be added as many times as needed, depending on the number of threads,
    in a bean stitch fashion """

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
            while subcrosses:

                for node in cycle:
                    cycle_to_insert = []
                    for cross in subcrosses:

                        if node in cross.corners:
                            position, cycle_to_insert = row_tour(subcrosses, node, nb_repeats, remove=False)
                            # here we try to minimize "bad traveling"
                            if cycle_to_insert:
                                if position == "below" and not flipped or position == "above" and flipped:
                                    node = insertion_node(crosses, node, cycle, cycle_to_insert, position, True)
                                else:
                                    node = insertion_node(crosses, node, cycle, cycle_to_insert, position, False)
                                position, cycle_to_insert = row_tour(subcrosses, node, nb_repeats, remove=True)
                                cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)
                                break

                    if cycle_to_insert:
                        break
        else:
            # for double crosses we can't reduce amount of bad travelinng
            while subcrosses:
                for node in cycle:
                    cycle_to_insert = []
                    for cross in subcrosses:
                        if node in cross.corners:
                            position, cycle_to_insert = row_tour(subcrosses, node, nb_repeats, remove=False)
                            cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)
                    if cycle_to_insert:
                        break

        cycle = travel + cycle
        travel = []

        eulerian_cycles.append(cycle)

    return eulerian_cycles


def insertion_node(crosses, node, cycle, cycle_to_insert, position, favor_left):

    current_node = node
    next_node = None
    previous_node = current_node

    if position == "below":
        if favor_left:
            cross = cross_at_position(crosses, current_node, "bottom_right")
            if cross:
                next_node = cross.bottom_left
        else:
            cross = cross_at_position(crosses, current_node, "bottom_left")
            if cross:
                next_node = cross.bottom_right
        while cross and next_node in cycle and next_node in cycle_to_insert:
            previous_node = current_node
            current_node = next_node
            if favor_left:
                cross = cross_at_position(crosses, current_node, "bottom_right")
                if cross:
                    next_node = cross.bottom_left
            else:
                cross = cross_at_position(crosses, current_node, "bottom_left")
                if cross:
                    next_node = cross.bottom_right

    elif position == "above":
        if favor_left:
            cross = cross_at_position(crosses, current_node, "top_right")
            if cross:
                next_node = cross.top_left
        else:
            cross = cross_at_position(crosses, current_node, "top_left")
            if cross:
                next_node = cross.top_right
        while cross and next_node in cycle and next_node in cycle_to_insert:
            previous_node = current_node
            current_node = next_node
            if favor_left:
                cross = cross_at_position(crosses, current_node, "top_right")
                if cross:
                    next_node = cross.top_left
            else:
                cross = cross_at_position(crosses, current_node, "top_left")
                if cross:
                    next_node = cross.top_right
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
    position = "no"
    cycle = _build_row_tour_above(subcrosses, starting_corner, nb_repeats, remove)
    if cycle:
        position = "above"
    if not cycle:
        cycle = _build_row_tour_below(subcrosses, starting_corner, nb_repeats, remove)
        if cycle:
            position = "below"
    return position, cycle


def _build_double_row_tour(subcrosses, starting_corner, nb_repeats, remove=True):
    # position is not going to used , but we need same signature as for
    position = "no"
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
    tour += construct_left_side_below(subcrosses, starting_corner, nb_repeats)
    tour += construct_right_side_below(subcrosses, starting_corner, nb_repeats)
    return tour


def construct_left_side_below(subcrosses, starting_corner, nb_repeats):
    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner
    while cross_at_position(subcrosses, current_node, "bottom_right"):
        # reach top leftmost corner
        cross = cross_at_position(subcrosses, current_node, "bottom_right")
        # first diagonal
        tour.append(cross.top_left)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross.top_left)
        tour.append(cross.center_point)
        tour.append(cross.top_right)
        # second diagonal
        tour.append(cross.bottom_left)
        for i in range(nb_repeats):
            tour.append(cross.top_right)
            tour.append(cross.bottom_left)
        current_node = cross.bottom_left
    while current_node != starting_corner:
        # go back to starting_corner  finishing the double crosses
        cross = cross_at_position(subcrosses, current_node, "bottom_left")
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
        tour.append(cross.bottom_right)
        current_node = cross.bottom_right
        covered_crosses.append(cross)
    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def construct_right_side_below(subcrosses, starting_corner, nb_repeats):
    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner

    while cross_at_position(subcrosses, current_node, "bottom_left"):
        cross = cross_at_position(subcrosses, current_node, "bottom_left")
        # first diagonal
        tour.append(cross.top_right)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross.top_right)
        tour.append(cross.center_point)
        tour.append(cross.top_left)
        # second diagonal
        tour.append(cross.bottom_right)
        for i in range(nb_repeats):
            tour.append(cross.top_left)
            tour.append(cross.bottom_right)
        current_node = cross.bottom_right

    while current_node != starting_corner:
        cross = cross_at_position(subcrosses, current_node, "bottom_right")
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
        tour.append(cross.bottom_left)
        current_node = cross.bottom_left
        covered_crosses.append(cross)
    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def _build_double_row_tour_above(subcrosses, starting_corner, nb_repeats):
    tour = []
    tour += construct_left_side_above(subcrosses, starting_corner, nb_repeats)
    tour += construct_right_side_above(subcrosses, starting_corner, nb_repeats)
    return tour


def construct_left_side_above(subcrosses, starting_corner, nb_repeats):
    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner

    while cross_at_position(subcrosses, current_node, "top_right"):
        cross = cross_at_position(subcrosses, current_node, "top_right")
        # first diagonal
        tour.append(cross.bottom_left)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross.bottom_left)
        tour.append(cross.center_point)
        tour.append(cross.bottom_right)
        # second diagonal
        tour.append(cross.top_left)
        for i in range(nb_repeats):
            tour.append(cross.bottom_right)
            tour.append(cross.top_left)
        current_node = cross.top_left

    while current_node != starting_corner:
        cross = cross_at_position(subcrosses, current_node, "top_left")
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
        tour.append(cross.top_right)
        current_node = cross.top_right
        covered_crosses.append(cross)

    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def construct_right_side_above(subcrosses, starting_corner, nb_repeats):
    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner

    while cross_at_position(subcrosses, current_node, "top_left"):
        cross = cross_at_position(subcrosses, current_node, "top_left")
        # first diagonal
        tour.append(cross.bottom_right)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross.bottom_right)
        tour.append(cross.center_point)
        tour.append(cross.bottom_left)
        # second diagonal
        tour.append(cross.top_right)
        for i in range(nb_repeats):
            tour.append(cross.bottom_left)
            tour.append(cross.top_right)
        current_node = cross.top_right

    while current_node != starting_corner:
        cross = cross_at_position(subcrosses, current_node, "top_right")
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
        tour.append(cross.top_left)
        current_node = cross.top_left
        covered_crosses.append(cross)

    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def _build_row_tour_above(crosses, node, nb_repeats, remove):
    """  build a tour  of the row of crosses (among param crosses) above the given node
    ensuring that no cross is flipped,
    adding diagonals as needed depending on the number of threads
    """
    tour = [node]
    covered_crosses = []
    current_node = node
    while cross_at_position(crosses, current_node, "top_right"):
        tour.append(cross_at_position(crosses, current_node, "top_right").center_point)
        tour.append(cross_at_position(crosses, current_node, "top_right").top_left)
        current_node = cross_at_position(crosses, current_node, "top_right").top_left
        check_stop_flag()
    while cross_at_position(crosses, current_node, "top_left"):
        # add first diagonal of a cross
        tour.append(cross_at_position(crosses, current_node, "top_left").bottom_right)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross_at_position(crosses, current_node, "top_left").bottom_right)
        tour.append(cross_at_position(crosses, current_node, "top_left").center_point)
        tour.append(cross_at_position(crosses, current_node, "top_left").bottom_left)
        # add second diagonal of the same  cross
        tour.append(cross_at_position(crosses, current_node, "top_left").top_right)
        for i in range(nb_repeats):
            tour.append(cross_at_position(crosses, current_node, "top_left").bottom_left)
            tour.append(cross_at_position(crosses, current_node, "top_left").top_right)
        covered_crosses.append(cross_at_position(crosses, current_node, "top_left"))
        current_node = cross_at_position(crosses, current_node, "top_left").top_right
        check_stop_flag()
    while current_node != node:
        # This part of the tour is "bad traveling", going through center of crosses
        # after stitching last diagonal
        tour.append(cross_at_position(crosses, current_node, "top_right").center_point)
        tour.append(cross_at_position(crosses, current_node, "top_right").top_left)
        current_node = cross_at_position(crosses, current_node, "top_right").top_left
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


def _build_row_tour_below(crosses, node, nb_repeats, remove):
    """ build a tour that of the row of crosses below the given node
    ensuring that no cross is flipped
    adding diagonals as needed depending on the number of threads
    remove the covered crosses from the crosses
    return empty list if no cross below """

    tour = [node]
    covered_crosses = []
    current_node = node

    while cross_at_position(crosses, current_node, "bottom_left"):
        tour.append(cross_at_position(crosses, current_node, "bottom_left").center_point)
        tour.append(cross_at_position(crosses, current_node, "bottom_left").bottom_right)
        current_node = cross_at_position(crosses, current_node, "bottom_left").bottom_right
        check_stop_flag()

    while cross_at_position(crosses, current_node, "bottom_right"):
        # add first diagonal of a cross
        tour.append(cross_at_position(crosses, current_node, "bottom_right").top_left)
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(cross_at_position(crosses, current_node, "bottom_right").top_left)
        tour.append(cross_at_position(crosses, current_node, "bottom_right").center_point)
        tour.append(cross_at_position(crosses, current_node, "bottom_right").top_right)
        tour.append(cross_at_position(crosses, current_node, "bottom_right").bottom_left)
        # add second diagonal of the same  cross
        covered_crosses.append(cross_at_position(crosses, current_node, "bottom_right"))
        for i in range(nb_repeats):
            tour.append(cross_at_position(crosses, current_node, "bottom_right").top_right)
            tour.append(cross_at_position(crosses, current_node, "bottom_right").bottom_left)
        current_node = cross_at_position(crosses, current_node, "bottom_right").bottom_left
        check_stop_flag()

    while current_node != node:
        tour.append(cross_at_position(crosses, current_node, "bottom_left").center_point)
        tour.append(cross_at_position(crosses, current_node, "bottom_left").bottom_right)
        current_node = cross_at_position(crosses, current_node, "bottom_left").bottom_right
        check_stop_flag()

    if len(tour) > 1 and remove:
        remove_crosses(crosses, covered_crosses)
    if len(tour) > 1:
        return tour
    else:
        return []


def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1


def insert_cycle_at_node(cycle_to_increase, cycle_to_insert, node):
    if node in cycle_to_increase:
        index = rindex(cycle_to_increase, node)
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
