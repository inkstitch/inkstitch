# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx

import sys
from ..stitch_plan import Stitch
from shapely.geometry import Polygon, MultiPoint, Point
from shapely import prepare
from shapely.affinity import translate
from shapely.ops import nearest_points
from ..utils.threading import check_stop_flag


class CrossGeometry(object):
    '''Holds data for cross stitch geometry:

        crosses: a list containing cross data
                 each cross is defined by five nodes
                 1. the center point
                 2. the four corners
    '''
    def __init__(self, fill, shape, cross_stitch_method):
        """Initialize cross stitch geometry generation for the given shape.

        Arguments:
            fill:                   the FillStitch instance
            shape:                  shape as shapely geometry
            cross_stitch_method:    cross stitch method as string
        """
        self.cross_stitch_method = cross_stitch_method
        self.fill = fill

        box_x, box_y = self.fill.pattern_size
        offset_x, offset_y = self.get_offset_values(shape)
        square = Polygon([(0, 0), (box_x, 0), (box_x, box_y), (0, box_y)])
        self.full_square_area = square.area

        # upright polygon
        center = list(square.centroid.coords)[0]
        upright_square = Polygon([(0, center[1]), (center[0], 0), (box_x, center[1]), (center[0], box_y)])

        # start and end have to be a multiple of the stitch length
        # we also add the initial offset
        minx, miny, maxx, maxy = shape.bounds
        adapted_minx = minx - minx % box_x - offset_x
        adapted_miny = miny - miny % box_y + offset_y
        adapted_maxx = maxx + box_x - maxx % box_x
        adapted_maxy = maxy + box_y - maxy % box_y

        prepare(shape)
        self.crosses = []

        y = adapted_miny
        while y <= adapted_maxy:
            x = adapted_minx
            while x <= adapted_maxx:
                # translate box to cross position
                box = translate(square, x, y)
                upright_box = translate(upright_square, x, y)
                if shape.contains(box):
                    self.add_cross(box, upright_box)
                elif shape.intersects(box):
                    intersection = box.intersection(shape)
                    if intersection.area / self.full_square_area * 100 + 0.0001 >= self.fill.fill_coverage:
                        self.add_cross(box, upright_box)
                x += box_x
            y += box_y
            check_stop_flag()

    def get_offset_values(self, shape):
        offset_x, offset_y = self.fill.cross_offset
        if not self.fill.canvas_grid_origin:
            box_x, box_y = self.fill.pattern_size
            bounds = shape.bounds
            offset_x -= bounds[0] % box_x
            offset_y -= bounds[1] % box_y
        return offset_x, offset_y

    def add_cross(self, box, upright_box):
        cross = {'center_point': [], 'corners': []}
        if "upright" in self.cross_stitch_method:
            box = upright_box
        coords = list(box.exterior.coords)
        cross['center_point'] = list(box.centroid.coords)[0]
        cross['corners'] = [coords[0], coords[1], coords[2], coords[3]]
        coords = list(upright_box.exterior.coords)
        cross['middles'] = [coords[0], coords[1], coords[2], coords[3]]

        self.crosses.append(cross)


def top_left(cross):
    return cross['corners'][3]


def top_right(cross):
    return cross['corners'][2]


def bottom_right(cross):
    return cross['corners'][1]


def bottom_left(cross):
    return cross['corners'][0]


def center_point(cross):
    return cross['center_point']


def middle_left(cross):
    return cross['middles'][0]


def middle_right(cross):
    return cross['middles'][2]


def middle_top(cross):
    return cross['middles'][1]


def middle_bottom(cross):
    return cross['middles'][3]


def even_cross_stitch(fill, shape, starting_point, threads_number):
    nb_repeats = (threads_number // 2) - 1
    method = fill.cross_stitch_method
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    subgraphs = _build_connect_subgraphs(cross_geoms)
    if method != "double_cross":
        eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, cross_geoms, nb_repeats)

        if "flipped" in cross_geoms.cross_stitch_method:
            for i in range(len(eulerian_cycles)):
                eulerian_cycles[i] = eulerian_cycles[i][::-1]
    else:
        eulerian_cycles = _build_eulerian_cycles(subgraphs, starting_point, cross_geoms, nb_repeats, True)

    stitches = _cycles_to_stitches(eulerian_cycles)
    return [stitches]


def get_starting_corner(starting_point, subcrosses):
    '''Snap starting and ending point on existing corners on our cross stitch pattern
    starting_point is not None when called
    '''
    snap_points = MultiPoint([corner for cross in subcrosses for corner in cross['corners']])
    start_point = nearest_points(snap_points, Point(starting_point))[0]
    starting_corner = (start_point.x, start_point.y)
    return starting_corner


def _build_connect_subgraphs(cross_geoms):
    """  first build the graph
    add first the nodes: each node is either a center point or a corner of a cross
    edges are between center point and corners, and between opposite corners
    each node carries the list of crosses it belongs to
    then add the edges
    finally extract the connected components as subgraphs """

    G = nx.Graph()

    for cross in cross_geoms.crosses:
        center = cross['center_point']
        G.add_node(center, crosses=[cross])
        corners = cross['corners']
        for corner in corners:
            if corner in G.nodes:
                G.nodes[corner]['crosses'].append(cross)
            else:
                G.add_node(corner, crosses=[cross])

        for corner in cross['corners']:
            G.add_edge(center, corner)
        G.add_edge(corners[0], corners[2])
        G.add_edge(corners[1], corners[3])

    return [G.subgraph(c).copy() for c in nx.connected_components(G)]


def _build_eulerian_cycles(subgraphs, starting_point, cross_geoms, nb_repeats, double=False):
    """ We need to construct an eulerian cycle for each subgraph, but we need to make sure
    that no cross is flipped
    So we construct partial cycles (tours) that cover rows of crosses without flipping any cross
    and we insert those partial cycles into the eulerian cycle until all crosses are covered

    We use a slightly different row tour, depending whether the starting point is above or below
    the center of the first cross

    diagonals will be added as many times as needed, depending on the number of threads,
    in a bean stitch fashion """

    eulerian_cycles = []
    centers = [cross['center_point'] for cross in cross_geoms.crosses]
    # if there is a starting point, make sure it is relevant to the  first subgraph
    if cross_geoms.crosses != [] and starting_point:
        first_subgraph = find_index_first_subgraph(subgraphs, cross_geoms.crosses, starting_point)
        subgraphs[0], subgraphs[first_subgraph] = subgraphs[first_subgraph], subgraphs[0]

    for subgraph in subgraphs:
        subcrosses = find_available_crosses(subgraph, cross_geoms.crosses)
        if subcrosses == []:
            continue

        if starting_point:
            starting_corner = get_starting_corner(starting_point, subcrosses)
        else:
            # any corner will do
            index = 0
            while list(subgraph.nodes)[index] in centers:
                index += 1
            starting_corner = list(subgraph.nodes)[index]

        if not double:
            cycle = _build_row_tour_above(subcrosses, starting_corner, nb_repeats)
            if cycle == []:
                cycle = _build_row_tour_below(subcrosses, starting_corner, nb_repeats)

            while subcrosses != []:
                for node in cycle:
                    for cross in subcrosses:
                        if node in cross['corners']:
                            cycle_to_insert = _build_row_tour_above(subcrosses, node, nb_repeats)
                            if cycle_to_insert == []:
                                cycle_to_insert = _build_row_tour_below(subcrosses, node, nb_repeats)
                            cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)
        else:
            # constructing  double crosses
            cycle = _build_double_row_tour_above(subcrosses, starting_corner, nb_repeats)

            if cycle == []:
                cycle = _build_double_row_tour_below(subcrosses, starting_corner, nb_repeats)

            while subcrosses != []:
                for node in cycle:
                    for cross in subcrosses:
                        if node in cross['corners']:
                            cycle_to_insert = _build_double_row_tour_above(subcrosses, node, nb_repeats)
                            if cycle_to_insert == []:
                                cycle_to_insert = _build_double_row_tour_below(subcrosses, node, nb_repeats)
                            cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)

        eulerian_cycles.append(cycle)
        # other connected components have no starting_point command
        starting_point = None

    return eulerian_cycles


def find_index_first_subgraph(subgraphs, crosses, starting_point):
    starting_corner = get_starting_corner(starting_point, crosses)
    index = 0
    while starting_corner not in list(subgraphs[index].nodes):
        index += 1
    return index


def is_cross_in_subgraph(cross, subgraph):

    if cross['center_point'] not in list(subgraph.nodes()):
        return False
    for corner in cross['corners']:
        if corner not in list(subgraph.nodes):
            return False
    return True


def find_available_crosses(subgraph, crosses):
    return [cross for cross in crosses if is_cross_in_subgraph(cross, subgraph)]


def cross_above_to_the_left(crosses, node):
    # looking for a cross where node is at bottom right
    left_cross = None
    for cross in crosses:
        if node == bottom_right(cross):
            return cross
    return left_cross


def cross_above_to_the_right(crosses, node):
    # looking for a cross where node is at bottom left
    right_cross = None
    for cross in crosses:
        if node == bottom_left(cross):
            return cross
    return right_cross


def cross_below_to_the_left(crosses, node):
    # looking for a cross where node is at top right
    left_cross = None
    for cross in crosses:
        if node == top_right(cross):
            return cross
    return left_cross


def cross_below_to_the_right(crosses, node):
    # looking for a cross where node is at top left
    right_cross = None
    for cross in crosses:
        if node == top_left(cross):
            return cross
    return right_cross


def _build_double_row_tour_below(subcrosses, starting_corner, nb_repeats):
    tour = []
    tour += construct_left_side_below(subcrosses, starting_corner, nb_repeats)
    tour += construct_right_side_below(subcrosses, starting_corner, nb_repeats)
    return tour


def construct_left_side_below(subcrosses, starting_corner, nb_repeats):
    tour = [starting_corner]
    covered_crosses = []
    current_node = starting_corner
    while cross_below_to_the_left(subcrosses, current_node):
        # reach top leftmost corner
        cross = cross_below_to_the_left(subcrosses, current_node)
        # first diagonal
        tour.append(bottom_left(cross))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(bottom_left(cross))
        tour.append(center_point(cross))
        tour.append(bottom_right(cross))
        # second diagonal
        tour.append(top_left(cross))
        for i in range(nb_repeats):
            tour.append(bottom_right(cross))
            tour.append(top_left(cross))
        current_node = top_left(cross)
    while current_node != starting_corner:
        # go back to starting_corner  finishing the double crosses
        cross = cross_below_to_the_right(subcrosses, current_node)
        tour.append(center_point(cross))
        tour.append(middle_left(cross))
        # horizontal
        tour.append(middle_right(cross))
        for i in range(nb_repeats):
            tour.append(middle_left(cross))
            tour.append(middle_right(cross))
        tour.append(center_point(cross))
        tour.append(middle_top(cross))
        # vertical
        tour.append(middle_bottom(cross))
        for i in range(nb_repeats):
            tour.append(middle_top(cross))
            tour.append(middle_bottom(cross))
        tour.append(center_point(cross))
        tour.append(top_right(cross))
        current_node = top_right(cross)
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

    while cross_below_to_the_right(subcrosses, current_node):
        cross = cross_below_to_the_right(subcrosses, current_node)
        # first diagonal
        tour.append(bottom_right(cross))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(bottom_right(cross))
        tour.append(center_point(cross))
        tour.append(bottom_left(cross))
        # second diagonal
        tour.append(top_right(cross))
        for i in range(nb_repeats):
            tour.append(bottom_left(cross))
            tour.append(top_right(cross))
        current_node = top_right(cross)

    while current_node != starting_corner:
        cross = cross_below_to_the_left(subcrosses, current_node)
        tour.append(center_point(cross))
        tour.append(middle_left(cross))
        # horizontal
        tour.append(middle_right(cross))
        for i in range(nb_repeats):
            tour.append(middle_left(cross))
            tour.append(middle_right(cross))
        tour.append(center_point(cross))
        tour.append(middle_top(cross))
        # vertical
        tour.append(middle_bottom(cross))
        for i in range(nb_repeats):
            tour.append(middle_top(cross))
            tour.append(middle_bottom(cross))
        tour.append(center_point(cross))
        tour.append(top_left(cross))
        current_node = top_left(cross)
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

    while cross_above_to_the_left(subcrosses, current_node):
        cross = cross_above_to_the_left(subcrosses, current_node)
        # first diagonal
        tour.append(top_left(cross))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(top_left(cross))
        tour.append(center_point(cross))
        tour.append(top_right(cross))
        # second diagonal
        tour.append(bottom_left(cross))
        for i in range(nb_repeats):
            tour.append(top_right(cross))
            tour.append(bottom_left(cross))
        current_node = bottom_left(cross)

    while current_node != starting_corner:
        cross = cross_above_to_the_right(subcrosses, current_node)
        tour.append(center_point(cross))
        tour.append(middle_left(cross))
        # horizontal
        tour.append(middle_right(cross))
        for i in range(nb_repeats):
            tour.append(middle_left(cross))
            tour.append(middle_right(cross))
        tour.append(center_point(cross))
        tour.append(middle_top(cross))
        # vertical
        tour.append(middle_bottom(cross))
        for i in range(nb_repeats):
            tour.append(middle_top(cross))
            tour.append(middle_bottom(cross))
        tour.append(center_point(cross))
        tour.append(bottom_right(cross))
        current_node = bottom_right(cross)
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

    while cross_above_to_the_right(subcrosses, current_node):
        cross = cross_above_to_the_right(subcrosses, current_node)
        # first diagonal
        tour.append(top_right(cross))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(top_right(cross))
        tour.append(center_point(cross))
        tour.append(top_left(cross))
        # second diagonal
        tour.append(bottom_right(cross))
        for i in range(nb_repeats):
            tour.append(top_left(cross))
            tour.append(bottom_right(cross))
        current_node = bottom_right(cross)

    while current_node != starting_corner:
        cross = cross_above_to_the_left(subcrosses, current_node)
        tour.append(center_point(cross))
        tour.append(middle_left(cross))
        # horizontal
        tour.append(middle_right(cross))
        for i in range(nb_repeats):
            tour.append(middle_left(cross))
            tour.append(middle_right(cross))
        tour.append(center_point(cross))
        tour.append(middle_top(cross))
        # vertical
        tour.append(middle_bottom(cross))
        for i in range(nb_repeats):
            tour.append(middle_top(cross))
            tour.append(middle_bottom(cross))
        tour.append(center_point(cross))
        tour.append(bottom_left(cross))
        current_node = bottom_left(cross)
        covered_crosses.append(cross)

    if len(tour) > 1:
        remove_crosses(subcrosses, covered_crosses)
        return tour
    else:
        return []


def _build_row_tour_above(crosses, node, nb_repeats):
    """  build a tour  of the row of crosses (among param crosses) above the given node
    ensuring that no cross is flipped,
    adding diagonals as needed depending on the number of threads
    """
    tour = [node]
    covered_crosses = []
    current_node = node
    while cross_above_to_the_left(crosses, current_node):
        tour.append(center_point(cross_above_to_the_left(crosses, current_node)))
        tour.append(bottom_left(cross_above_to_the_left(crosses, current_node)))
        current_node = bottom_left(cross_above_to_the_left(crosses, current_node))
    while cross_above_to_the_right(crosses, current_node):
        # add first diagonal of a cross
        tour.append(top_right(cross_above_to_the_right(crosses, current_node)))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(top_right(cross_above_to_the_right(crosses, current_node)))
        tour.append(center_point(cross_above_to_the_right(crosses, current_node)))
        tour.append(top_left(cross_above_to_the_right(crosses, current_node)))
        # add second diagonal of the same  cross
        tour.append(bottom_right(cross_above_to_the_right(crosses, current_node)))
        for i in range(nb_repeats):
            tour.append(top_left(cross_above_to_the_right(crosses, current_node)))
            tour.append(bottom_right(cross_above_to_the_right(crosses, current_node)))
        covered_crosses.append(cross_above_to_the_right(crosses, current_node))
        current_node = bottom_right(cross_above_to_the_right(crosses, current_node))
    while current_node != node:
        tour.append(center_point(cross_above_to_the_left(crosses, current_node)))
        tour.append(bottom_left(cross_above_to_the_left(crosses, current_node)))
        current_node = bottom_left(cross_above_to_the_left(crosses, current_node))

    if len(tour) > 1:
        remove_crosses(crosses, covered_crosses)
        return tour
    else:
        return []


def remove_crosses(crosses, covered_crosses):
    for cross in covered_crosses:
        crosses.remove(cross)


def _build_row_tour_below(crosses, node, nb_repeats):
    """ build a tour that of the row of crosses below the given node
    ensuring that no cross is flipped
    adding diagonals as needed depending on the number of threads
    remove the covered crosses from the crosses
    return empty list if no cross below """

    tour = [node]
    covered_crosses = []
    current_node = node

    while cross_below_to_the_right(crosses, current_node):
        tour.append(center_point(cross_below_to_the_right(crosses, current_node)))
        tour.append(top_right(cross_below_to_the_right(crosses, current_node)))
        current_node = top_right(cross_below_to_the_right(crosses, current_node))

    while cross_below_to_the_left(crosses, current_node):
        # add first diagonal of a cross
        tour.append(bottom_left(cross_below_to_the_left(crosses, current_node)))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(bottom_left(cross_below_to_the_left(crosses, current_node)))
        tour.append(center_point(cross_below_to_the_left(crosses, current_node)))
        tour.append(bottom_right(cross_below_to_the_left(crosses, current_node)))
        tour.append(top_left(cross_below_to_the_left(crosses, current_node)))
        # add second diagonal of the same  cross
        covered_crosses.append(cross_below_to_the_left(crosses, current_node))
        for i in range(nb_repeats):
            tour.append(bottom_right(cross_below_to_the_left(crosses, current_node)))
            tour.append(top_left(cross_below_to_the_left(crosses, current_node)))
        current_node = top_left(cross_below_to_the_left(crosses, current_node))

    while current_node != node:
        tour.append(center_point(cross_below_to_the_right(crosses, current_node)))
        tour.append(top_right(cross_below_to_the_right(crosses, current_node)))
        current_node = top_right(cross_below_to_the_right(crosses, current_node))

    if len(tour) > 1:
        remove_crosses(crosses, covered_crosses)
        return tour
    else:
        return []


def insert_cycle_at_node(cycle_to_increase, cycle_to_insert, node):
    if node in cycle_to_increase:
        index = cycle_to_increase.index(node)
        new_cycle = cycle_to_increase[:index] + cycle_to_insert + cycle_to_increase[index+1:]
        return new_cycle


def _cycles_to_stitches(eulerian_cycles):
    stitches = []
    for cycle in eulerian_cycles:
        if cycle is not None:
            for point in cycle:
                stitches.append(Stitch(*point))
    return stitches
