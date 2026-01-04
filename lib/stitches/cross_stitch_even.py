# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from .utils.cross_stitch import CrossGeometry

import sys


def even_cross_stitch(fill, shape, starting_point):
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    if not cross_geoms.cross_diagonals1:
        return []
    
    subgraphs = _build_connect_subgraph(cross_geoms)
    eulerian_cycles = _build_eulerian_cycles(subgraphs)
    sys.stderr.write(f"Built {len(eulerian_cycles)} eulerian cycles for cross stitch pattern.\n")
    for cycle in eulerian_cycles:
        sys.stderr.write(f"Built eulerian cycle with {len(cycle)} edges.\n")
        sys.stderr.write(str(cycle))
        sys.stderr.write("\n")

    stitches = _cycles_to_stitches(eulerian_cycles)
    
    return []

    

def _build_connect_subgraph(cross_geoms):

    G = nx.Graph()
    for line in cross_geoms.travel_edges:
        G.add_edge(line.coords[0], line.coords[-1], path=line)

    for line in cross_geoms.cross_diagonals1:
        G.add_edge(line.coords[0], line.coords[-1], path=line)

    for line in cross_geoms.cross_diagonals2:
        G.add_edge(line.coords[0], line.coords[-1], path=line)    
    
    return  [G.subgraph(c).copy() for c in nx.connected_components(G)]

def _build_eulerian_cycles(subgraphs):
   
    eulerian_cycles = []
    for subgraph in subgraphs:
        cycle = list(nx.eulerian_circuit(subgraph))

        eulerian_cycles.append(cycle)
    return eulerian_cycles

def _cycles_to_stitches(eulerian_cycles):
    ## what is the easiest way to convert cycles to stitches?
    stitches = []
    
    return stitches