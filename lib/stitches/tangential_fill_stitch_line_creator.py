from enum import IntEnum

import networkx as nx
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely.geometry.polygon import orient
from shapely.ops import polygonize

from .running_stitch import running_stitch
from ..stitch_plan import Stitch
from ..stitches import constants
from ..stitches import tangential_fill_stitch_pattern_creator
from ..utils import DotDict
from ..utils.geometry import reverse_line_string, ensure_geometry_collection, ensure_multi_polygon


class Tree(nx.DiGraph):
    # This lets us do tree.nodes['somenode'].parent instead of the default
    # tree.nodes['somenode']['parent'].
    node_attr_dict_factory = DotDict


def offset_linear_ring(ring, offset, resolution, join_style, mitre_limit):
    result = Polygon(ring).buffer(-offset, resolution, cap_style=2, join_style=join_style, mitre_limit=mitre_limit, single_sided=True)
    result = ensure_multi_polygon(result)

    rings = GeometryCollection([poly.exterior for poly in result.geoms])
    rings = rings.simplify(constants.simplification_threshold, False)

    return take_only_valid_linear_rings(rings)


def take_only_valid_linear_rings(rings):
    """
    Removes all geometries which do not form a "valid" LinearRing
    (meaning a ring which does not form a straight line)
    """

    valid_rings = []

    for ring in ensure_geometry_collection(rings).geoms:
        if len(ring.coords) > 3 or (len(ring.coords) == 3 and ring.coords[0] != ring.coords[-1]):
            valid_rings.append(ring)

    return GeometryCollection(valid_rings)


def orient_linear_ring(ring, clockwise=True):
    # Unfortunately for us, Inkscape SVGs have an inverted Y coordinate.
    # Normally we don't have to care about that, but in this very specific
    # case, the meaning of is_ccw is flipped.  It actually tests whether
    # a ring is clockwise.  That makes this logic super-confusing.
    if ring.is_ccw != clockwise:
        return reverse_line_string(ring)
    else:
        return ring


def make_tree_uniform(tree, clockwise=True):
    """
    Since naturally holes have the opposite point ordering than non-holes we
    make all lines within the tree "root" uniform (having all the same
    ordering direction)
    """

    for node in tree.nodes.values():
        node.val = orient_linear_ring(node.val, clockwise)


# Used to define which stitching strategy shall be used
class StitchingStrategy(IntEnum):
    INNER_TO_OUTER = 0
    SINGLE_SPIRAL = 1
    DOUBLE_SPIRAL = 2


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


def offset_poly(poly, offset, join_style, clockwise):
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
    -avoid_self_crossing: don't let the path cross itself when using the Inner to Outer strategy
    Output:
    -List of point coordinate tuples
    -Tag (origin) of each point to analyze why a point was placed
     at this position
    """

    ordered_poly = orient(poly, -1)
    tree = Tree()
    tree.add_node('root', type='node', parent=None, val=ordered_poly.exterior)
    active_polys = ['root']
    active_holes = [[]]

    # We don't care about the names of the nodes, we just need them to be unique.
    node_num = 0

    for hole in ordered_poly.interiors:
        tree.add_node(node_num, type="hole", val=hole)
        active_holes[0].append(node_num)
        node_num += 1

    while len(active_polys) > 0:
        current_poly = active_polys.pop()
        current_holes = active_holes.pop()
        outer, inners = offset_polygon_and_holes(tree, current_poly, current_holes, offset, join_style)

        if not outer.is_empty:
            polygons = match_polygons_and_holes(outer, inners)

            if not polygons.is_empty:
                for polygon in polygons.geoms:
                    new_polygon, new_holes = convert_polygon_to_nodes(tree, polygon, parent_polygon=current_poly, child_holes=current_holes)

                    if new_polygon:
                        active_polys.append(new_polygon)
                        active_holes.append(new_holes)

        for previous_hole in current_holes:
            # If the previous holes are not
            # contained in the new holes they
            # have been merged with the
            # outer polygon
            if not tree.nodes[previous_hole].parent:
                tree.nodes[previous_hole].parent = current_poly
                tree.add_edge(current_poly, previous_hole)

    make_tree_uniform(tree, clockwise)

    return tree


def offset_polygon_and_holes(tree, poly, holes, offset, join_style):
    outer = offset_linear_ring(
        tree.nodes[poly].val,
        offset,
        resolution=5,
        join_style=join_style,
        mitre_limit=10,
    )

    inners = []
    for hole in holes:
        inner = offset_linear_ring(
            tree.nodes[hole].val,
            -offset,  # take negative offset for holes
            resolution=5,
            join_style=join_style,
            mitre_limit=10,
        )
        if not inner.is_empty:
            inners.append(Polygon(inner.geoms[0]))

    return outer, inners


def match_polygons_and_holes(outer, inners):
    result = MultiPolygon(polygonize(outer))
    if len(inners) > 0:
        result = ensure_geometry_collection(result.difference(MultiPolygon(inners)))

    return result


def convert_polygon_to_nodes(tree, polygon, parent_polygon, child_holes):
    polygon = orient(polygon, -1)

    if polygon.area < 0.1:
        return None, None

    polygon = polygon.simplify(constants.simplification_threshold, False)
    valid_rings = take_only_valid_linear_rings(polygon.exterior)

    try:
        exterior = valid_rings.geoms[0]
    except IndexError:
        return None, None

    node = id(polygon)  # just needs to be unique

    tree.add_node(node, type='node', parent=parent_polygon, val=exterior)
    tree.add_edge(parent_polygon, node)

    hole_node_list = []
    for hole in polygon.interiors:
        hole_node = id(hole)
        tree.add_node(hole_node, type="hole", val=hole)
        for previous_hole in child_holes:
            if Polygon(hole).contains(Polygon(tree.nodes[previous_hole].val)):
                tree.nodes[previous_hole].parent = hole_node
                tree.add_edge(hole_node, previous_hole)
        hole_node_list.append(hole_node)

    return node, hole_node_list


def tangential_fill(poly, strategy, offset, stitch_distance, join_style, clockwise, starting_point, avoid_self_crossing):
    if strategy in (StitchingStrategy.SINGLE_SPIRAL, StitchingStrategy.DOUBLE_SPIRAL) and len(poly.interiors) > 1:
        raise ValueError(
            "Single spiral geometry must not have more than one hole!")

    tree = offset_poly(poly, offset, join_style, clockwise)

    if strategy == StitchingStrategy.INNER_TO_OUTER:
        connected_line = tangential_fill_stitch_pattern_creator.connect_raster_tree_from_inner_to_outer(
            tree, 'root', offset, stitch_distance, starting_point, avoid_self_crossing)
        path = [Stitch(*point) for point in connected_line.coords]
        return running_stitch(path, stitch_distance)
    elif strategy == StitchingStrategy.SINGLE_SPIRAL:
        if not check_and_prepare_tree_for_valid_spiral(tree):
            raise ValueError("Geometry cannot be filled with one spiral!")
        connected_line = tangential_fill_stitch_pattern_creator.connect_raster_tree_single_spiral(
            tree, offset, stitch_distance, starting_point)
    elif strategy == StitchingStrategy.DOUBLE_SPIRAL:
        if not check_and_prepare_tree_for_valid_spiral(tree):
            raise ValueError("Geometry cannot be filled with a double spiral!")
        connected_line = tangential_fill_stitch_pattern_creator.connect_raster_tree_double_spiral(
            tree, offset, stitch_distance, starting_point)
    else:
        raise ValueError("Invalid stitching stratety!")

    return connected_line
