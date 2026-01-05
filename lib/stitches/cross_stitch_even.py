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


def even_cross_stitch(fill, shape, starting_point):
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    #print(cross_geoms.crosses, file=sys.stderr)
 
    subgraphs = _build_connect_subgraph(cross_geoms)
    eulerian_cycles = _build_eulerian_cycles(subgraphs)
    # sys.stderr.write(f"Built {len(eulerian_cycles)} eulerian cycles for cross stitch pattern.\n")
    # for cycle in eulerian_cycles:
    #     sys.stderr.write(f"Built eulerian cycle with {len(cycle)} edges.\n")
    #     sys.stderr.write(str(cycle))
    #     sys.stderr.write("\n")

   # stitches = _cycles_to_stitches(eulerian_cycles)
    stitches = []
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
    sys.stderr.write(f"Built graph with {len(G.nodes(data=True))} nodes and {len(G.edges())} edges for cross stitch pattern.\n")
    sys.stderr.write(f"Built graph with {G.nodes(data=True)} nodes and {G.edges()} edges for cross stitch pattern.\n")

    return [G.subgraph(c).copy() for c in nx.connected_components(G)]


def _build_eulerian_cycles(subgraphs):
    eulerian_cycles = []
    for subgraph in subgraphs:
        cycle = list(nx.eulerian_circuit(subgraph))

        eulerian_cycles.append(cycle)
    return eulerian_cycles


def _cycles_to_stitches(eulerian_cycles):
    stitches = []
    stitches.append(Stitch(*eulerian_cycles[0][0][0]))
    for cycle in eulerian_cycles:
        for edge in cycle:
            stitches.append(Stitch(*edge[1]))
    return stitches
