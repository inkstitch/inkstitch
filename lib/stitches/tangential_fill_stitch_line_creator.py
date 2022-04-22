from enum import IntEnum

import networkx as nx
from depq import DEPQ
from shapely.geometry import MultiLineString, Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry.polygon import LinearRing
from shapely.geometry.polygon import orient
from shapely.ops import polygonize

from ..stitches import constants
from ..stitches import tangential_fill_stitch_pattern_creator
from ..utils import DotDict


class Tree(nx.DiGraph):
    # This lets us do tree.nodes['somenode'].parent instead of the default
    # tree.nodes['somenode']['parent'].
    node_attr_dict_factory = DotDict


def offset_linear_ring(ring, offset, resolution, join_style, mitre_limit):
    result = Polygon(ring).buffer(offset, resolution, cap_style=2, join_style=join_style, mitre_limit=mitre_limit, single_sided=True)

    if result.geom_type == 'Polygon':
        return result.exterior
    else:
        result_list = []
        for poly in result:
            result_list.append(poly.exterior)
        return MultiLineString(result_list)

    # """
    #     Solves following problem: When shapely offsets a LinearRing the
    #     start/end point might be handled wrongly since they
    #     are only treated as LineString.
    #     (See e.g. https://i.stack.imgur.com/vVh56.png as a problematic example)
    #     This method checks first whether the start/end point form a problematic
    #     edge with respect to the offset side. If it is not a problematic
    #     edge we can use the normal offset_routine. Otherwise we need to
    #     perform two offsets:
    #     -offset the ring
    #     -offset the start/end point + its two neighbors left and right
    #     Finally both offsets are merged together to get the correct
    #     offset of a LinearRing
    #     """

    # PROBLEM: Did not work in rare cases since it expects the point order be maintained after offsetting the curve
    # (e.g. the first point in the offsetted curve shall belong to the first point in the original curve). However, this
    # assumption seems to be not always true that is why this code was replaced by the buffer routine.

    #     coords = ring.coords[:]
    #     # check whether edge at index 0 is concave or convex. Only for
    #     # concave edges we need to spend additional effort
    #     dx_seg1 = dy_seg1 = 0
    #     if coords[0] != coords[-1]:
    #         dx_seg1 = coords[0][0] - coords[-1][0]
    #         dy_seg1 = coords[0][1] - coords[-1][1]
    #     else:
    #         dx_seg1 = coords[0][0] - coords[-2][0]
    #         dy_seg1 = coords[0][1] - coords[-2][1]
    #     dx_seg2 = coords[1][0] - coords[0][0]
    #     dy_seg2 = coords[1][1] - coords[0][1]
    #     # use cross product:
    #     crossvalue = dx_seg1 * dy_seg2 - dy_seg1 * dx_seg2
    #     sidesign = 1
    #     if side == "left":
    #         sidesign = -1

    #     # We do not need to take care of the joint n-0 since we
    #     # offset along a concave edge:
    #     if sidesign * offset * crossvalue <= 0:
    #         return ring.parallel_offset(offset, side, resolution, join_style, mitre_limit)

    #     # We offset along a convex edge so we offset the joint n-0 separately:
    #     if coords[0] != coords[-1]:
    #         coords.append(coords[0])
    #     offset_ring1 = ring.parallel_offset(
    #         offset, side, resolution, join_style, mitre_limit
    #     )
    #     offset_ring2 = LineString((coords[-2], coords[0], coords[1])).parallel_offset(
    #         offset, side, resolution, join_style, mitre_limit
    #     )

    #     # Next we need to merge the results:
    #     if offset_ring1.geom_type == "LineString":
    #         return LinearRing(offset_ring2.coords[:] + offset_ring1.coords[1:-1])
    #     else:
    #         # We have more than one resulting LineString for offset of
    #         # the geometry (ring) = offset_ring1.
    #         # Hence we need to find the LineString which belongs to the
    #         # offset of element 0 in coords =offset_ring2
    #         # in order to add offset_ring2 geometry to it:
    #         result_list = []
    #         thresh = constants.offset_factor_for_adjacent_geometry * abs(offset)
    #         for offsets in offset_ring1:
    #             if (
    #                 abs(offsets.coords[0][0] - coords[0][0]) < thresh
    #                 and abs(offsets.coords[0][1] - coords[0][1]) < thresh
    #             ):
    #                 result_list.append(
    #                     LinearRing(offset_ring2.coords[:] + offsets.coords[1:-1])
    #                 )
    #             else:
    #                 result_list.append(LinearRing(offsets))
    #         return MultiLineString(result_list)


def take_only_valid_linear_rings(rings):
    """
    Removes all geometries which do not form a "valid" LinearRing
    (meaning a ring which does not form a straight line)
    """
    if rings.geom_type == "MultiLineString":
        new_list = []
        for ring in rings:
            if len(ring.coords) > 3 or (
                len(ring.coords) == 3 and ring.coords[0] != ring.coords[-1]
            ):
                new_list.append(ring)
        if len(new_list) == 1:
            return LinearRing(new_list[0])
        else:
            return MultiLineString(new_list)
    elif rings.geom_type == "LineString" or rings.geom_type == "LinearRing":
        if len(rings.coords) <= 2:
            return LinearRing()
        elif len(rings.coords) == 3 and rings.coords[0] == rings.coords[-1]:
            return LinearRing()
        else:
            return rings
    else:
        return LinearRing()


def make_tree_uniform_ccw(tree):
    """
    Since naturally holes have the opposite point ordering than non-holes we
    make all lines within the tree "root" uniform (having all the same
    ordering direction)
    """
    for node in nx.dfs_preorder_nodes(tree, 'root'):
        if tree.nodes[node].type == "hole":
            tree.nodes[node].val = LinearRing(reversed(tree.nodes[node].val.coords))


# Used to define which stitching strategy shall be used
class StitchingStrategy(IntEnum):
    CLOSEST_POINT = 0
    INNER_TO_OUTER = 1
    SPIRAL = 2


def check_and_prepare_tree_for_valid_spiral(tree):
    """
    Takes a tree consisting of offsetted curves. If a parent has more than one child we
    cannot create a spiral. However, to make the routine more robust, we allow more than
    one child if only one of the childs has own childs. The other childs are removed in this
    routine then. If the routine returns true, the tree will have been cleaned up from unwanted
    childs. If the routine returns false even under the mentioned weaker conditions the
    tree cannot be connected by one spiral.
    """

    def process_node(node):
        children = set(tree[node])

        if len(children) == 0:
            return True
        elif len(children) == 1:
            child = children.pop()
            return process_node(child)
        else:
            children_with_children = {child for child in children if tree[child]}
            if len(children_with_children) > 1:
                # Node has multiple children with children, so a perfect spiral is not possible.
                # This False value will be returned all the way up the stack.
                return False
            elif len(children_with_children) == 1:
                children_without_children = children - children_with_children
                child = children_with_children.pop()
                tree.remove_nodes_from(children_without_children)
                return process_node(child)
            else:
                # None of the children has its own children, so we'll just take the longest.
                longest = max(children, key=lambda child: tree[child]['val'].length)
                shorter_children = children - {longest}
                tree.remove_nodes_from(shorter_children)
                return process_node(longest)

    return process_node('root')


def offset_poly(poly, offset, join_style, stitch_distance, min_stitch_distance, offset_by_half, strategy, starting_point):  # noqa: C901
    """
    Takes a polygon (which can have holes) as input and creates offsetted
    versions until the polygon is filled with these smaller offsets.
    These created geometries are afterwards connected to each other and
    resampled with a maximum stitch_distance.
    The return value is a LineString which should cover the full polygon.
    Input:
    -poly: The shapely polygon which can have holes
    -offset: The used offset for the curves
    -join_style: Join style for the offset - can be round, mitered or bevel
     (https://shapely.readthedocs.io/en/stable/manual.html#shapely.geometry.JOIN_STYLE)
     For examples look at
     https://shapely.readthedocs.io/en/stable/_images/parallel_offset.png
    -stitch_distance maximum allowed stitch distance between two points
    -min_stitch_distance stitches within a row shall be at least min_stitch_distance apart. Stitches connecting
     offsetted paths might be shorter.
    -offset_by_half: True if the points shall be interlaced
    -strategy: According to StitchingStrategy enum class you can select between
     different strategies for the connection between parent and childs. In
     addition it offers the option "SPIRAL" which creates a real spiral towards inner.
     In contrast to the other two options, "SPIRAL" does not end at the starting point
     but at the innermost point
    -starting_point: Defines the starting point for the stitching
    Output:
    -List of point coordinate tuples
    -Tag (origin) of each point to analyze why a point was placed
     at this position
    """

    if strategy == StitchingStrategy.SPIRAL and len(poly.interiors) > 1:
        raise ValueError(
            "Single spiral geometry must not have more than one hole!")

    ordered_poly = orient(poly, -1)
    ordered_poly = ordered_poly.simplify(
        constants.simplification_threshold, False)
    tree = Tree()
    tree.add_node('root',
                  type='node',
                  parent=None,
                  val=ordered_poly.exterior,
                  already_rastered=False,
                  transferred_point_priority_deque=DEPQ(iterable=None, maxlen=None),
                  )
    active_polys = ['root']
    active_holes = [[]]

    # We don't care about the names of the nodes, we just need them to be unique.
    node_num = 0

    for hole in ordered_poly.interiors:
        tree.add_node(node_num,
                      type="hole",
                      val=hole,
                      already_rastered=False,
                      transferred_point_priority_deque=DEPQ(iterable=None, maxlen=None),
                      )
        active_holes[0].append(node_num)
        node_num += 1

    while len(active_polys) > 0:
        current_poly = active_polys.pop()
        current_holes = active_holes.pop()
        poly_inners = []

        outer = offset_linear_ring(
            tree.nodes[current_poly].val,
            offset,
            resolution=5,
            join_style=join_style,
            mitre_limit=10,
        )
        outer = outer.simplify(constants.simplification_threshold, False)
        outer = take_only_valid_linear_rings(outer)

        for hole in current_holes:
            inner = offset_linear_ring(
                tree.nodes[hole].val,
                -offset,  # take negative offset for holes
                resolution=5,
                join_style=join_style,
                mitre_limit=10,
            )
            inner = inner.simplify(constants.simplification_threshold, False)
            inner = take_only_valid_linear_rings(inner)
            if not inner.is_empty:
                poly_inners.append(Polygon(inner))
        if not outer.is_empty:
            if len(poly_inners) == 0:
                if outer.geom_type == "LineString" or outer.geom_type == "LinearRing":
                    result = Polygon(outer)
                else:
                    result = MultiPolygon(polygonize(outer))
            else:
                if outer.geom_type == "LineString" or outer.geom_type == "LinearRing":
                    result = Polygon(outer).difference(
                        MultiPolygon(poly_inners))
                else:
                    result = MultiPolygon(outer).difference(
                        MultiPolygon(poly_inners))

            if not result.is_empty and result.area > offset * offset / 10:
                if result.geom_type == "Polygon":
                    result_list = [result]
                else:
                    result_list = list(result.geoms)

                for polygon in result_list:
                    polygon = orient(polygon, -1)

                    if polygon.area < offset * offset / 10:
                        continue

                    polygon = polygon.simplify(
                        constants.simplification_threshold, False
                    )
                    poly_coords = polygon.exterior
                    poly_coords = take_only_valid_linear_rings(poly_coords)
                    if poly_coords.is_empty:
                        continue

                    node = node_num
                    node_num += 1
                    tree.add_node(node,
                                  type='node',
                                  parent=current_poly,
                                  val=poly_coords,
                                  already_rastered=False,
                                  transferred_point_priority_deque=DEPQ(iterable=None, maxlen=None),
                                  )
                    tree.add_edge(current_poly, node)
                    active_polys.append(node)
                    hole_node_list = []
                    for hole in polygon.interiors:
                        hole_node = node_num
                        node_num += 1
                        tree.add_node(hole_node,
                                      type="hole",
                                      val=hole,
                                      already_rastered=False,
                                      transferred_point_priority_deque=DEPQ(iterable=None, maxlen=None),
                                      )
                        for previous_hole in current_holes:
                            if Polygon(hole).contains(Polygon(tree.nodes[previous_hole].val)):
                                tree.nodes[previous_hole].parent = hole_node
                                tree.add_edge(hole_node, previous_hole)
                        hole_node_list.append(hole_node)
                    active_holes.append(hole_node_list)
        for previous_hole in current_holes:
            # If the previous holes are not
            # contained in the new holes they
            # have been merged with the
            # outer polygon
            if tree.nodes[previous_hole].parent is None:
                tree.nodes[previous_hole].parent = current_poly
                tree.add_edge(current_poly, previous_hole)

    make_tree_uniform_ccw(tree)

    if strategy == StitchingStrategy.CLOSEST_POINT:
        (connected_line, connected_line_origin) = tangential_fill_stitch_pattern_creator.connect_raster_tree_nearest_neighbor(
            tree, 'root', offset, stitch_distance, min_stitch_distance, starting_point, offset_by_half)
    elif strategy == StitchingStrategy.INNER_TO_OUTER:
        (connected_line, connected_line_origin) = tangential_fill_stitch_pattern_creator.connect_raster_tree_from_inner_to_outer(
            tree, 'root', offset, stitch_distance, min_stitch_distance, starting_point, offset_by_half)
    elif strategy == StitchingStrategy.SPIRAL:
        if not check_and_prepare_tree_for_valid_spiral(tree):
            raise ValueError("Geometry cannot be filled with one spiral!")
        (connected_line, connected_line_origin) = tangential_fill_stitch_pattern_creator.connect_raster_tree_spiral(
            tree, offset, stitch_distance, min_stitch_distance, starting_point, offset_by_half)
    else:
        raise ValueError("Invalid stitching stratety!")

    return connected_line, connected_line_origin
