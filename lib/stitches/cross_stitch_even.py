# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import networkx as nx
from .utils.cross_stitch import CrossGeometry


def even_cross_stitch(fill, shape, starting_point):
    cross_geoms = CrossGeometry(fill, shape, fill.cross_stitch_method)
    if not cross_geoms.cross_diagonals1:
        return []
    
    subgraphs = _build_connect_subgraph(cross_geoms)
    eulerian_cycles = _build_eulerian_cycles(subgraphs)
    import sys
    print(f"Even cross stitch will create {len(eulerian_cycles)} separate paths", file=sys.stderr)
    return []


def _build_connect_subgraph(cross_geoms):

    G = nx.Graph()
    for line in cross_geoms.travel_edges:
        G.add_edge(str(line.coords[0]), str(line.coords[-1]), path=line)

    for line in cross_geoms.cross_diagonals1:
        G.add_edge(str(line.coords[0]), str(line.coords[-1]), path=line)

    for line in cross_geoms.cross_diagonals2:
        G.add_edge(str(line.coords[0]), str(line.coords[-1]), path=line)    
    
    return  [G.subgraph(c).copy() for c in nx.connected_components(G)]

def _build_eulerian_cycles(subgraphs):
   
    eulerian_cycles = []
    for subgraph in subgraphs:
        cycle = list(nx.eulerian_circuit(subgraph))

        eulerian_cycles.append(cycle)
    return eulerian_cycles