import networkx


from ..elements import SatinColumn


def auto_satin(satins, starting_point=None, ending_point=None):
    """Find an optimal order to stitch a list of SatinColumns.

    Add running stitch and jump stitches as necessary to construct a stitch
    order.  Cut satins as necessary to minimize jump stitch length.

    For example, consider three satins making up the letters "PO":

        * one vertical satin for the "P"
        * the loop of the "P"
        * the "O"

    A good stitch path would be:

      1. up the leg
      2. down through half of the loop
      3. running stitch to the bottom of the loop
      4. satin stitch back up to the middle of the loop
      5. jump to the closest point on the O
      6. satin stitch around the O

    If passed, stitching will start from starting_point and end at
    ending_point.  It is expected that the starting and ending points will
    fall on satin columns in the list.  If they don't, the nearest
    point on a satin column in the list will be used.

    Returns: a list of SatinColumn and Stroke objects making up the selected
      stitch order.  Jumps between objects are implied if they are not right
      next to each other.
    """

    graph = build_graph(satins, starting_point, ending_point)
    add_intersection_points(graph)
    add_starting_and_ending_points(graph, starting_point, ending_point)
    augment_graph(graph)
    graph = networkx.eulerize(graph)
    path = find_path(graph)

    return path_to_elements(path, graph)
