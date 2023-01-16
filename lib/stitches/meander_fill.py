from shapely.geometry import MultiPoint, Point
from shapely.ops import nearest_points
import networkx as nx

from .. import tiles
from ..debug import debug
from ..utils.list import poprandom


def meander_fill(fill, shape, starting_point, ending_point):
    tile = get_tile(fill.meander_pattern)
    if not tile:
        return []

    graph = tile.to_graph(shape)
    start, end = find_starting_and_ending_nodes(graph, starting_point, ending_point)

    return generate_meander_path(graph, start, end)


def get_tile(tile_name):
    all_tiles = {tile.name: tile for tile in tiles.all_tiles()}

    try:
        return all_tiles.get(tile_name, all_tiles.popitem()[1])
    except KeyError:
        return None


def find_starting_and_ending_nodes(graph, starting_point, ending_point):
    all_points = MultiPoint(list(graph))

    starting_node = nearest_points(starting_point, all_points)[1].coords[0]
    ending_node = nearest_points(ending_point, all_points)[1].coords[0]

    if starting_node == ending_node:
        # We need a path to start with, so pick a new ending node
        all_points = all_points.difference(Point(starting_node))
        ending_node = nearest_points(ending_point, all_points)[1].coords[0]

    return starting_node, ending_node


def find_initial_path(graph, start, end):
    # We need some path to start with.  We could use
    # nx.all_simple_paths(graph, start, end) and choose the first one.
    # However, that tends to pick a really "orderly" path.  Shortest
    # path looks more random.
    return nx.shortest_path(graph, start, end)


def generate_meander_path(graph, start, end):
    path = find_initial_path(graph, start, end)
    path_edges = list(zip(path[:-1], path[1:]))
    graph.remove_edges_from(path_edges)
    graph_nodes = set(graph) - set(path)

    edges_to_consider = list(path_edges)
    meander_path = path_edges
    while edges_to_consider:
        while edges_to_consider:
            edge = poprandom(edges_to_consider)
            edges_to_consider.extend(replace_edge(meander_path, edge, graph, graph_nodes))

        edge_pairs = list(zip(path[:-1], path[1:]))
        while edge_pairs:
            edge1, edge2 = poprandom(edge_pairs)
            edges_to_consider.extend(replace_edge_pair(meander_path, edge1, edge2, graph, graph_nodes))

    return meander_path


def replace_edge(path, edge, graph, graph_nodes):
    subgraph = graph.subgraph(graph_nodes | set(edge))
    new_path = None
    for new_path in nx.all_simple_edge_paths(subgraph, edge[0], edge[1], 7):
        if len(new_path) > 1:
            break
    if new_path is None or len(new_path) == 1:
        return []
    i = path.index(edge)
    path[i:i + 1] = new_path
    graph.remove_edges_from(new_path)
    graph_nodes.difference_update(start for start, end in new_path)
    debug.log(f"found new path of length {len(new_path)} at position {i}")

    return new_path


def replace_edge_pair(path, edge1, edge2, graph, graph_nodes):
    subgraph = graph.subgraph(graph_nodes | {edge1[0], edge2[1]})
    new_path = None
    for new_path in nx.all_simple_edge_paths(subgraph, edge1[0], edge2[1], 10):
        if len(new_path) > 2:
            break
    if new_path is None or len(new_path) <= 2:
        return []
    i = path.index(edge1)
    path[i:i + 2] = new_path
    graph.remove_edges_from(new_path)
    graph_nodes.difference_update(start for start, end in new_path)
    debug.log(f"found new pair path of length {len(new_path)} at position {i}")

    return new_path
