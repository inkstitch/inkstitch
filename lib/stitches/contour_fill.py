from collections import namedtuple
from itertools import chain

import networkx as nx
import numpy as np
import trimesh
from shapely import offset_curve
from shapely.geometry import (GeometryCollection, LineString, MultiPolygon,
                              Point, Polygon)
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points, polygonize
from shapely.validation import make_valid

from ..stitch_plan import Stitch
from ..utils import DotDict
from ..utils.clamp_path import clamp_path_to_polygon
from ..utils.geometry import (cut, ensure_geometry_collection,
                              ensure_multi_line_string, reverse_line_string,
                              roll_linear_ring)
from ..utils.smoothing import smooth_path
from ..utils.threading import check_stop_flag
from .running_stitch import running_stitch


class Tree(nx.DiGraph):
    # This lets us do tree.nodes['somenode'].parent instead of the default
    # tree.nodes['somenode']['parent'].
    node_attr_dict_factory = DotDict

    def __init__(self, *args, **kwargs):
        self.__node_num = 0
        super().__init__(**kwargs)

    def generate_node_name(self):
        node = self.__node_num
        self.__node_num += 1

        return node


nearest_neighbor_tuple = namedtuple(
    "nearest_neighbor_tuple",
    [
        "nearest_point_parent",
        "nearest_point_child",
        "proj_distance_parent",
        "child_node",
    ],
)


def _offset_linear_ring(ring, offset, resolution, join_style, mitre_limit):
    ring = Polygon(ring)
    result = offset_curve(ring, -offset, resolution, join_style=join_style, mitre_limit=mitre_limit)
    result = ensure_multi_line_string(result)
    rings = result.simplify(0.01, False)

    return _take_only_valid_linear_rings(rings)


def _take_only_valid_linear_rings(rings):
    """
    Removes all geometries which do not form a "valid" LinearRing.

    A "valid" ring is one that does not form a straight line.
    """

    valid_rings = []

    for ring in ensure_geometry_collection(rings).geoms:
        if len(ring.coords) > 3 or (len(ring.coords) == 3 and ring.coords[0] != ring.coords[-1]):
            valid_rings.append(ring)

    return GeometryCollection(valid_rings)


def _orient_linear_ring(ring, clockwise=True):
    # Unfortunately for us, Inkscape SVGs have an inverted Y coordinate.
    # Normally we don't have to care about that, but in this very specific
    # case, the meaning of is_ccw is flipped.  It actually tests whether
    # a ring is clockwise.  That makes this logic super-confusing.
    if ring.is_ccw != clockwise:
        return reverse_line_string(ring)
    else:
        return ring


def _orient_tree(tree, clockwise=True):
    """
    Orient all linear rings in the tree.

    Since naturally holes have the opposite point ordering than non-holes we
    make all lines within the tree uniform (having all the same ordering
    direction)
    """

    for node in tree.nodes.values():
        node.val = _orient_linear_ring(node.val, clockwise)


def offset_polygon(polygon, offset, join_style, clockwise):
    """
    Convert a polygon to a tree of isocontours.

    An isocontour is an offset version of the polygon's boundary.  For example,
    the isocontours of a circle are a set of concentric circles inside the
    circle.

    This function takes a polygon (which may have holes) as input and creates
    isocontours until the polygon is filled completely.  The isocontours are
    returned as a Tree, with a parent-child relationship indicating that the
    parent isocontour contains the child isocontour.

    Arguments:
        polygon - The shapely Polygon which may have holes
        offset - The spacing between isocontours
        join_style - Join style used when offsetting the Polygon border to create
                     isocontours.  Can be round, mitered or bevel, as defined by
                     shapely:
                       https://shapely.readthedocs.io/en/stable/manual.html#shapely.geometry.JOIN_STYLE
        clockwise - If True, isocontour points are in clockwise order; if False, counter-clockwise.

    Return Value:
        Tree - see above
    """

    ordered_polygon = orient(polygon, -1)
    tree = Tree()
    tree.add_node('root', type='node', parent=None, val=ordered_polygon.exterior)
    active_polygons = ['root']
    active_holes = [[]]

    for hole in ordered_polygon.interiors:
        hole_node = tree.generate_node_name()
        tree.add_node(hole_node, type="hole", val=hole)
        active_holes[0].append(hole_node)

    while len(active_polygons) > 0:
        check_stop_flag()

        current_poly = active_polygons.pop()
        current_holes = active_holes.pop()

        outer, inners = _offset_polygon_and_holes(tree, current_poly, current_holes, offset, join_style)

        polygons = _match_polygons_and_holes(outer, inners)

        for polygon in polygons.geoms:
            new_polygon, new_holes = _convert_polygon_to_nodes(tree, polygon, parent_polygon=current_poly, child_holes=current_holes)

            if new_polygon is not None:
                active_polygons.append(new_polygon)
                active_holes.append(new_holes)

        for previous_hole in current_holes:
            # If the previous holes are not
            # contained in the new holes they
            # have been merged with the
            # outer polygon
            if not tree.nodes[previous_hole].parent:
                tree.nodes[previous_hole].parent = current_poly
                tree.add_edge(current_poly, previous_hole)

    _orient_tree(tree, clockwise)
    return tree


def _offset_polygon_and_holes(tree, poly, holes, offset, join_style):
    outer = _offset_linear_ring(
        tree.nodes[poly].val,
        offset,
        resolution=5,
        join_style=join_style,
        mitre_limit=10,
    )

    inners = []
    for hole in holes:
        inner = _offset_linear_ring(
            tree.nodes[hole].val,
            -offset,  # take negative offset for holes
            resolution=5,
            join_style=join_style,
            mitre_limit=10,
        )
        if not inner.is_empty:
            inners.append(Polygon(inner.geoms[0]))

    return outer, inners


def _match_polygons_and_holes(outer, inners):
    result = MultiPolygon(polygonize(outer.geoms))
    if len(inners) > 0:
        inners = MultiPolygon(inners)
        if not inners.is_valid:
            inners = make_valid(MultiPolygon(inners))
        result = ensure_geometry_collection(result.difference(inners))

    return result


def _convert_polygon_to_nodes(tree, polygon, parent_polygon, child_holes):
    if polygon.area < 0.1:
        return None, None

    polygon = orient(polygon, -1)

    valid_rings = _take_only_valid_linear_rings(polygon.exterior)

    try:
        exterior = valid_rings.geoms[0]
    except IndexError:
        return None, None

    node = tree.generate_node_name()
    tree.add_node(node, type='node', parent=parent_polygon, val=exterior)
    tree.add_edge(parent_polygon, node)

    hole_nodes = []
    for hole in polygon.interiors:
        hole_node = tree.generate_node_name()
        tree.add_node(hole_node, type="hole", val=hole)
        for previous_hole in child_holes:
            if Polygon(hole).contains(Polygon(tree.nodes[previous_hole].val)):
                tree.nodes[previous_hole].parent = hole_node
                tree.add_edge(hole_node, previous_hole)
        hole_nodes.append(hole_node)

    return node, hole_nodes


def _get_nearest_points_closer_than_thresh(travel_line, next_line, threshold):
    """
    Find the first point along travel_line that is within threshold of next_line.

    Input:
        travel_line - The "parent" line for which the distance should
                      be minimized to enter next_line
        next_line - contains the next_line which need to be entered
        threshold - The distance between travel_line and next_line needs
                    to below threshold to be a valid point for entering

    Return value:
        tuple or None
            - the tuple structure is:
              (point in travel_line, point in next_line)
            - None is returned if there is no point that satisfies the threshold.
    """

    # We'll buffer next_line and find the intersection with travel_line.
    # Then we'll return the very first point in the intersection,
    # matched with a corresponding point on next_line.  Fortunately for
    # us, intersection of a Polygon with a LineString yields pieces of
    # the LineString in the same order as the input LineString.
    threshold_area = next_line.buffer(threshold)
    portion_within_threshold = travel_line.intersection(threshold_area)

    if portion_within_threshold.is_empty:
        return None
    else:
        # Projecting with 0 lets us avoid distinguishing between LineString and
        # MultiLineString.
        parent_point = Point(portion_within_threshold.interpolate(0))
        return nearest_points(parent_point, next_line)


def _create_nearest_points_list(travel_line, tree, children, threshold, threshold_hard):
    """Determine the best place to enter each of parent's children

    Arguments:
        travel_line - The "parent" line for which the distance should
                      be minimized to enter each child
        children - children of travel_line that need to be entered
        threshold - The distance between travel_line and a child should
                    to be below threshold to be a valid point for entering
        threshold_hard - As a last resort, we can accept an entry point
                         that is this far way

    Return value:
        list of nearest_neighbor_tuple - indicating where to enter each
                                         respective child
    """

    children_nearest_points = []

    for child in children:
        result = _get_nearest_points_closer_than_thresh(travel_line, tree.nodes[child].val, threshold)
        if result is None:
            # where holes meet outer borders a distance
            # up to 2 * used offset can arise
            result = _get_nearest_points_closer_than_thresh(travel_line, tree.nodes[child].val, threshold_hard)

        # if we still didn't get a result, ignore this child
        # this may lead to oddities, but at least it doesn't fail
        if result is None:
            continue

        proj = travel_line.project(result[0])
        children_nearest_points.append(
            nearest_neighbor_tuple(
                nearest_point_parent=result[0],
                nearest_point_child=result[1],
                proj_distance_parent=proj,
                child_node=child,
            )
        )

    return children_nearest_points


def _find_path_inner_to_outer(tree, node, offset, starting_point, avoid_self_crossing, forward=True):
    """Find a stitch path for this ring and its children.

    Strategy: A connection from parent to child is made as fast as possible to
    reach the innermost child as fast as possible in order to stitch afterwards
    from inner to outer.

    This function calls itself recursively to find a stitch path for each child
    (and its children).

    Arguments:
        tree - a Tree of isocontours (as returned by offset_polygon)
        offset - offset that was passed to offset_polygon
        starting_point - starting point for stitching
        avoid_self_crossing - if True, tries to generate a path that does not
                              cross itself.
        forward - if True, this ring will be stitched in its natural direction
                  (used internally by avoid_self_crossing)

    Return value:
        LineString -- the stitching path
    """
    check_stop_flag()

    current_node = tree.nodes[node]
    current_ring = current_node.val

    if not forward and avoid_self_crossing:
        current_ring = reverse_line_string(current_ring)

    # reorder the coordinates of this ring so that it starts with
    # a point nearest the starting_point
    start_distance = current_ring.project(starting_point)
    current_ring = roll_linear_ring(current_ring, start_distance)
    current_node.val = current_ring

    # Find where along this ring to connect to each child.
    nearest_points_list = _create_nearest_points_list(
        current_ring,
        tree,
        tree[node],
        threshold=1.5 * offset,
        threshold_hard=2.05 * offset
    )
    nearest_points_list.sort(key=lambda tup: tup.proj_distance_parent)

    result_coords = []
    if not nearest_points_list:
        # We have no children, so we're at the center of a spiral.  Reversing
        # the innermost ring gives a nicer visual appearance.
        if not avoid_self_crossing:
            current_ring = reverse_line_string(current_ring)
    else:
        # This is a recursive algorithm.  We'll stitch along this ring, pausing
        # to jump to each child ring in turn and sew it before continuing on
        # this ring.  We'll end back where we started.

        result_coords.append(current_ring.coords[0])
        distance_so_far = 0
        for child_connection in nearest_points_list:
            # Cut this ring into pieces before and after where this child will connect.
            before, after = cut(current_ring, child_connection.proj_distance_parent - distance_so_far)
            distance_so_far = child_connection.proj_distance_parent

            # Stitch the part leading up to this child.
            if before is not None:
                result_coords.extend(before.coords)

            # Stitch this child.  The child will start and end in the same
            # place, which should be close to our current location.
            child_path = _find_path_inner_to_outer(
                tree,
                child_connection.child_node,
                offset,
                child_connection.nearest_point_child,
                avoid_self_crossing,
                not forward
            )
            result_coords.extend(child_path.coords)

            # Skip ahead a little bit on this ring before resuming.  This
            # gives a nice spiral pattern, where we spiral out from the
            # innermost child.
            if after is not None:
                skip, after = cut(after, offset)
                distance_so_far += offset

            current_ring = after

    if current_ring is not None:
        # skip a little at the end so we don't end exactly where we started.
        remaining_length = current_ring.length
        if remaining_length > offset:
            current_ring, skip = cut(current_ring, current_ring.length - offset)

        result_coords.extend(current_ring.coords)

    return LineString(result_coords)


def inner_to_outer(tree, polygon, offset,
                   stitch_length, tolerance, smoothness,
                   starting_point, avoid_self_crossing,
                   enable_random_stitch_length, random_sigma, random_seed):
    """Fill a shape with spirals, from innermost to outermost."""

    stitch_path = _find_path_inner_to_outer(tree, 'root', offset, starting_point, avoid_self_crossing)
    points = [Stitch(*point) for point in stitch_path.coords]

    if smoothness > 0:
        smoothed = smooth_path(points, smoothness)
        points = clamp_path_to_polygon(smoothed, polygon)

    stitches = running_stitch(points, [stitch_length], tolerance, enable_random_stitch_length, random_sigma, random_seed)

    return stitches


def _reorder_linear_ring(ring, start):
    distances = ring - start
    start_index = np.argmin(np.linalg.norm(distances, axis=1))
    return np.roll(ring, -start_index, axis=0)


def _interpolate_linear_rings(ring1, ring2, max_stitch_length, start=None):
    """
    Interpolate between two LinearRings

    Creates a path from start_point on ring1 and around the rings, ending at a
    nearby point on ring2.  The path will smoothly transition from ring1 to
    ring2 as it travels around the rings.

    Inspired by interpolate() from https://github.com/mikedh/pocketing/blob/master/pocketing/polygons.py

    Arguments:
        ring1 -- LinearRing start point will lie on
        ring2 -- LinearRing end point will lie on
        max_stitch_length -- maximum stitch length (used to calculate resampling accuracy)
        start -- Point on ring1 to start at, as a tuple

    Return value: Path interpolated between two LinearRings, as a LineString.
    """

    # Resample the two LinearRings so that they are the same number of points
    # long.  Then take the corresponding points in each ring and interpolate
    # between them, gradually going more toward ring2.
    #
    # This is a little less accurate than the method in interpolate(), but several
    # orders of magnitude faster because we're not building and querying a KDTree.

    num_points = int(20 * ring1.length / max_stitch_length)
    ring1_resampled = trimesh.path.traversal.resample_path(np.array(ring1.coords), count=num_points)
    ring2_resampled = trimesh.path.traversal.resample_path(np.array(ring2.coords), count=num_points)

    if start is not None:
        ring1_resampled = _reorder_linear_ring(ring1_resampled, start)
        ring2_resampled = _reorder_linear_ring(ring2_resampled, start)

    weights = np.linspace(0.0, 1.0, num_points).reshape((-1, 1))
    points = (ring1_resampled * (1.0 - weights)) + (ring2_resampled * weights)
    result = LineString(points)

    return result.simplify(0.1, False)


def _check_and_prepare_tree_for_valid_spiral(tree):
    """Check whether spiral fill is possible, and tweak if necessary.

    Takes a tree consisting of isocontours. If a parent has more than one child
    we cannot create a spiral. However, to make the routine more robust, we
    allow more than one child if only one of the children has own children. The
    other children are removed in this routine then. If the routine returns true,
    the tree will have been cleaned up from unwanted children.

    If even with these weaker constraints, a spiral is not possible, False is
    returned.
    """

    def process_node(node):
        check_stop_flag()

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


def single_spiral(tree, stitch_length, tolerance, starting_point, enable_random_stitch_length, random_sigma, random_seed):
    """Fill a shape with a single spiral going from outside to center."""
    return _spiral_fill(tree, stitch_length, tolerance, starting_point, enable_random_stitch_length, random_sigma, random_seed, _make_spiral)


def double_spiral(tree, stitch_length, tolerance, starting_point, enable_random_stitch_length, random_sigma, random_seed):
    """Fill a shape with a double spiral going from outside to center and back to outside. """
    return _spiral_fill(tree, stitch_length, tolerance, starting_point, enable_random_stitch_length, random_sigma, random_seed, _make_fermat_spiral)


def _spiral_fill(tree, stitch_length, tolerance, close_point, enable_random_stitch_length, random_sigma, random_seed, spiral_maker):
    starting_point = close_point.coords[0]

    rings = _get_spiral_rings(tree)
    path = spiral_maker(rings, stitch_length, starting_point)
    path = [Stitch(*stitch) for stitch in path]

    return running_stitch(path, [stitch_length], tolerance, enable_random_stitch_length, random_sigma, random_seed)


def _get_spiral_rings(tree):
    rings = []

    node = 'root'
    while True:
        check_stop_flag()

        rings.append(tree.nodes[node].val)

        children = tree[node]
        if len(children) == 0:
            break
        elif len(children) == 1:
            node = list(children)[0]
        else:
            # We can only really fill a shape with a single spiral if each
            # parent has only one child.  We'll do our best though, because
            # that is probably more helpful to the user than just refusing
            # entirely.  We'll pick the child that's closest to the center.
            parent_center = rings[-1].centroid
            node = min(children, key=lambda child: parent_center.distance(tree.nodes[child].val.centroid))

    return rings


def _make_fermat_spiral(rings, stitch_length, starting_point):
    forward = _make_spiral(rings[::2], stitch_length, starting_point)
    back = _make_spiral(rings[1::2], stitch_length, starting_point)
    back.reverse()

    return chain(forward, back)


def _make_spiral(rings, stitch_length, starting_point):
    path = []
    spiral_part = None

    for ring1, ring2 in zip(rings[:-1], rings[1:]):
        check_stop_flag()

        spiral_part = _interpolate_linear_rings(ring1, ring2, stitch_length, starting_point)
        # skip last to avoid duplicated points
        path.extend(spiral_part.coords[:-1])

    if spiral_part:
        # at the end add last point
        path.append(spiral_part.coords[-1])

    return path
