# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx

import sys
from ..stitch_plan import Stitch
from shapely.geometry import Polygon
from shapely import prepare
from shapely.affinity import translate
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




def even_cross_stitch(fill, shape, starting_point, threads_number):
    nb_repeats = (threads_number // 2) -1
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    #print(cross_geoms.crosses, file=sys.stderr)
    cross = cross_geoms.crosses[0]
    # sys.stderr.write(f"First cross at center {cross['center_point']} with corners {cross['corners']}.\n")
    # sys.stderr.write(f"left top corner: {top_left(cross)}\n")
    # sys.stderr.write(f"right top corner: {top_right(cross)}\n")
    # sys.stderr.write(f"right bottom corner: {bottom_right(cross)}\n")
    # sys.stderr.write(f"left bottom corner: {bottom_left(cross)}\n") 

    
 
    subgraphs = _build_connect_subgraph(cross_geoms)
    # sys.stderr.write(f"Built {len(subgraphs)} connected subgraphs for cross stitch pattern.\n")
    # for node in subgraphs[0].nodes:
    #     node_crosses = subgraphs[0].nodes[node]['crosses']
    #     sys.stderr.write(f"Node: {node} belongs to  {len(node_crosses)} crosses :{node_crosses}\n")

    eulerian_cycles = _build_eulerian_cycles(subgraphs,nb_repeats)
    # sys.stderr.write(f"Built {len(eulerian_cycles)} eulerian cycles for cross stitch pattern.\n")
    # for cycle in eulerian_cycles:
    #     sys.stderr.write(f"Built eulerian cycle with {len(cycle)} edges.\n")
    #     sys.stderr.write(str(cycle))
    #     sys.stderr.write("\n")
    
    stitches = _cycles_to_stitches(eulerian_cycles)
    return [stitches]


def _build_connect_subgraph(cross_geoms):

    G = nx.Graph()

    for cross in cross_geoms.crosses:
        center = cross['center_point']
        G.add_node(center,crosses = [cross])
        corners = cross['corners']
        for corner in corners:
            if corner in G.nodes:
                G.nodes[corner]['crosses'].append(cross)
            else:
                G.add_node(corner, crosses = [cross])
            

        for corner in cross['corners']:
            G.add_edge(center, corner)
    
        G.add_edge(corners[0], corners[2])
        G.add_edge(corners[1], corners[3])
    # sys.stderr.write(f"Built graph with {len(G.nodes(data=True))} nodes and {len(G.edges())} edges for cross stitch pattern.\n")
    # sys.stderr.write(f"Built graph with {G.nodes(data=True)} nodes and {G.edges()} edges for cross stitch pattern.\n")

    return [G.subgraph(c).copy() for c in nx.connected_components(G)]


def _build_eulerian_cycles(subgraphs,nb_repeats):
    eulerian_cycles = []
    for subgraph in subgraphs:
       # cycle = list(nx.eulerian_circuit(subgraph))
      
       
        # sys.stderr.write(f"starting at node   {i} going above{list(subgraph.nodes)[i]}.\n")
        # cycle = _build_row_tour_above(subgraph, list(subgraph.nodes)[i])
        # if cycle != []:
        #     eulerian_cycles.append(cycle)
        # sys.stderr.write(f"starting at node   {i} going below{list(subgraph.nodes)[i]}.\n")
        # cycle = _build_row_tour_below(subgraph, list(subgraph.nodes)[i])
        # if cycle != []:
        #     eulerian_cycles.append(cycle)

        
        # cycle_to_increase = _build_row_tour_above(subgraph, list(subgraph.nodes)[1])
        # cycle_to_insert= _build_row_tour_below(subgraph, list(subgraph.nodes)[3])
        # increased_cycle = insert_cycle_at_node(cycle_to_increase, cycle_to_insert, list(subgraph.nodes)[3])
        # if increased_cycle != []:
        #     eulerian_cycles.append(increased_cycle)
        
        ## we don't want to start from a center
        
        cycle = _build_row_tour_above(subgraph, list(subgraph.nodes)[1], nb_repeats)
        if cycle == []:
            cycle = _build_row_tour_below(subgraph, list(subgraph.nodes)[1], nb_repeats)

        while not is_covert(subgraph):

            for node in cycle:
                if len(subgraph.nodes[node]['crosses']) != 0:
                    cycle_to_insert = _build_row_tour_above(subgraph, node, nb_repeats)
                    if cycle_to_insert == []:
                        cycle_to_insert = _build_row_tour_below(subgraph, node, nb_repeats)
               
                    cycle = insert_cycle_at_node(cycle, cycle_to_insert, node)
        eulerian_cycles.append(cycle)

    return eulerian_cycles

def is_covert(subgraph):
    for node in subgraph.nodes:
        if len(subgraph.nodes[node]['crosses']) > 0:
            return False
    return True

def cross_above_to_the_left(subgraph,node):
    ## looking for a cross where node is at bottom right
    left_cross = None
    for cross in subgraph.nodes[node]['crosses']:
        if node == bottom_right(cross):
            left_cross = cross
            return left_cross
    return left_cross

def cross_above_to_the_right(subgraph,node):
    ## looking for a cross where node is at bottom left
    right_cross = None
    for cross in subgraph.nodes[node]['crosses']:
        if node == bottom_left(cross):
            right_cross = cross
            return right_cross
    return right_cross  

def cross_below_to_the_left(subgraph,node):
    ## looking for a cross where node is at top right
    left_cross = None
    for cross in subgraph.nodes[node]['crosses']:
        if node == top_right(cross):
            left_cross = cross
            return left_cross
    return left_cross

def cross_below_to_the_right(subgraph,node):
    ## looking for a cross where node is at top left
    right_cross = None
    for cross in subgraph.nodes[node]['crosses']:
        if node == top_left(cross):
            right_cross = cross
            return right_cross
    return right_cross

def _build_row_tour_above(subgraph,node,nb_repeats):
    tour = [node]
    covered_crosses = []
    current_node = node

    while cross_above_to_the_left(subgraph,current_node):

        tour.append(center_point(cross_above_to_the_left(subgraph,current_node)))
        tour.append(bottom_left(cross_above_to_the_left(subgraph,current_node)))
        current_node = bottom_left(cross_above_to_the_left(subgraph,current_node))

    while cross_above_to_the_right(subgraph,current_node):
        ## add first diagonal of a cross
        
        tour.append(top_right(cross_above_to_the_right(subgraph,current_node)))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(top_right(cross_above_to_the_right(subgraph,current_node)))
        tour.append(center_point(cross_above_to_the_right(subgraph,current_node)))
        tour.append(top_left(cross_above_to_the_right(subgraph,current_node)))
        ## add second diagonal of the same  cross
        tour.append(bottom_right(cross_above_to_the_right(subgraph,current_node)))
        for i in range(nb_repeats):
            tour.append(top_left(cross_above_to_the_right(subgraph,current_node)))
            tour.append(bottom_right(cross_above_to_the_right(subgraph,current_node)))
        covered_crosses.append(cross_above_to_the_right(subgraph,current_node))
        current_node = bottom_right(cross_above_to_the_right(subgraph,current_node))
        
    while current_node != node:
        tour.append(center_point(cross_above_to_the_left(subgraph,current_node)))
        tour.append(bottom_left(cross_above_to_the_left(subgraph,current_node)))
        current_node = bottom_left(cross_above_to_the_left(subgraph,current_node))
  
    if len(tour) > 1:
        # sys.stderr.write(f"Completed row tour above: {tour}.\n")
        remove_crosses(subgraph, covered_crosses)
        # sys.stderr.write(f"Removed covered crosses from subgraph {subgraph.nodes(data=True)}.\n")
        return tour
    else:
        return []
    
def remove_crosses(subgraph, covered_crosses):
    for node in subgraph.nodes:
        node_crosses = subgraph.nodes[node]['crosses']
        for cross in covered_crosses:
            if cross in node_crosses:
               subgraph.nodes[node]['crosses'].remove(cross)
        
    
def _build_row_tour_below(subgraph,node,nb_repeats):
    tour = [node]
    covered_crosses = []
    current_node = node

    while cross_below_to_the_right(subgraph,current_node):
        tour.append(center_point(cross_below_to_the_right(subgraph,current_node)))
        tour.append(top_right(cross_below_to_the_right(subgraph,current_node)))
        current_node = top_right(cross_below_to_the_right(subgraph,current_node))

    while cross_below_to_the_left(subgraph,current_node):
        ## add first diagonal of a cross
        tour.append(bottom_left(cross_below_to_the_left(subgraph,current_node)))
        for i in range(nb_repeats):
            tour.append(current_node)
            tour.append(bottom_left(cross_below_to_the_left(subgraph,current_node)))
        tour.append(center_point(cross_below_to_the_left(subgraph,current_node)))
        tour.append(bottom_right(cross_below_to_the_left(subgraph,current_node)))
        tour.append(top_left(cross_below_to_the_left(subgraph,current_node)))
        ## add second diagonal of the same  cross
        covered_crosses.append(cross_below_to_the_left(subgraph,current_node))
        for i in range(nb_repeats):
            tour.append(bottom_right(cross_below_to_the_left(subgraph,current_node)))
            tour.append(top_left(cross_below_to_the_left(subgraph,current_node)))
        current_node = top_left(cross_below_to_the_left(subgraph,current_node))

    while current_node != node:
        tour.append(center_point(cross_below_to_the_right(subgraph,current_node)))
        tour.append(top_right(cross_below_to_the_right(subgraph,current_node)))
        current_node = top_right(cross_below_to_the_right(subgraph,current_node))
    
    if len(tour) > 1:
        # sys.stderr.write(f"Completed row tour below: {tour}.\n")
        remove_crosses(subgraph, covered_crosses)
        # sys.stderr.write(f"Removed covered crosses from subgraph {subgraph.nodes(data=True)}.\n")
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
   # stitches.append(Stitch(*eulerian_cycles[0][0][0]))
    for cycle in eulerian_cycles:
        # for edge in cycle:
        #     stitches.append(Stitch(*edge[1]))
        if cycle is not None:
            for point in cycle:
                stitches.append(Stitch(*point))
    return stitches

