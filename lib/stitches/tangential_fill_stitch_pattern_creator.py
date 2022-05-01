import math
from collections import namedtuple
import networkx as nx
import numpy as np
import trimesh
from shapely.geometry import Point, LineString, LinearRing, MultiLineString
from shapely.ops import nearest_points

from .running_stitch import running_stitch

from ..debug import debug
from ..stitches import constants
from ..stitches import sample_linestring
from ..stitch_plan import Stitch
from ..utils.geometry import cut, roll_linear_ring, reverse_line_string

nearest_neighbor_tuple = namedtuple(
    "nearest_neighbor_tuple",
    [
        "nearest_point_parent",
        "nearest_point_child",
        "proj_distance_parent",
        "child_node",
    ],
)


@debug.time
def get_nearest_points_closer_than_thresh(travel_line, next_line, threshold):
    """
    Find the first point along travel_line that is within threshold of next_line.

    Input:
    -travel_line: The "parent" line for which the distance should
     be minimized to enter next_line
    -next_line: contains the next_line which need to be entered
    -threshold: The distance between travel_line and next_line needs
     to below threshold to be a valid point for entering

    Output:
    -tuple or None
      - the tuple structure is:
        (nearest point in travel_line, nearest point in next_line)
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
        if isinstance(portion_within_threshold, MultiLineString):
            portion_within_threshold = portion_within_threshold.geoms[0]

        parent_point = Point(portion_within_threshold.coords[0])
        return nearest_points(parent_point, next_line)


def create_nearest_points_list(
        travel_line, tree, children_list, threshold, threshold_hard):
    """
    Takes a line and calculates the nearest distance along this line to
    enter the childs in children_list
    The method calculates the distances along the line and along the
    reversed line to find the best direction which minimizes the overall
    distance for all childs.
    Input:
    -travel_line: The "parent" line for which the distance should
     be minimized to enter the childs
    -children_list: contains the childs of travel_line which need to be entered
    -threshold: The distance between travel_line and a child needs to be
     below threshold to be a valid point for entering
    -preferred_direction: Put a bias on the desired travel direction along
     travel_line. If equals zero no bias is applied.
     preferred_direction=1 means we prefer the direction of travel_line;
     preferred_direction=-1 means we prefer the opposite direction.
    Output:
    -stitching direction for travel_line
    -list of tuples (one tuple per child). The tuple structure is:
     ((nearest point in travel_line, nearest point in child),
       distance along travel_line, belonging child)
    """

    children_nearest_points = []

    for child in children_list:
        result = get_nearest_points_closer_than_thresh(travel_line, tree.nodes[child].val, threshold)
        if result is None:
            # where holes meet outer borders a distance
            # up to 2 * used offset can arise
            result = get_nearest_points_closer_than_thresh(travel_line, tree.nodes[child].val, threshold_hard)

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


def calculate_replacing_middle_point(line_segment, abs_offset, max_stitch_distance):
    """
    Takes a line segment (consisting of 3 points!)
    and calculates a new middle point if the line_segment is
    straight enough to be resampled by points max_stitch_distance apart FROM THE END OF line_segment.
    Returns None if the middle point is not needed.
    """
    angles = sample_linestring.calculate_line_angles(line_segment)
    if angles[1] < abs_offset * constants.limiting_angle_straight:
        if line_segment.length < max_stitch_distance:
            return None
        else:
            return line_segment.interpolate(line_segment.length - max_stitch_distance).coords[0]
    else:
        return line_segment.coords[1]


@debug.time
def connect_raster_tree_from_inner_to_outer(tree, node, offset, stitch_distance, min_stitch_distance, starting_point,
                                            offset_by_half):  # noqa: C901
    """
    Takes the offset curves organized as a tree, connects and samples them.
    Strategy: A connection from parent to child is made as fast as possible to
    reach the innermost child as fast as possible in order to stitch afterwards
    from inner to outer.
    Input:
    -tree: contains the offsetted curves in a hierachical organized
     data structure.
    -used_offset: used offset when the offsetted curves were generated
    -stitch_distance: maximum allowed distance between two points
     after sampling
    -min_stitch_distance stitches within a row shall be at least min_stitch_distance apart. Stitches connecting
     offsetted paths might be shorter.
    -close_point: defines the beginning point for stitching
     (stitching starts always from the undisplaced curve)
    -offset_by_half: If true the resulting points are interlaced otherwise not.
    Returnvalues:
    -All offsetted curves connected to one line and sampled with points obeying
     stitch_distance and offset_by_half
    -Tag (origin) of each point to analyze why a point was placed
     at this position
    """

    current_node = tree.nodes[node]
    current_ring = current_node.val

    # reorder the coordinates of this ring so that it starts with
    # a point nearest the starting_point
    start_distance = current_ring.project(starting_point)
    current_ring = roll_linear_ring(current_ring, start_distance)
    current_node.val = current_ring

    # Find where along this ring to connect to each child.
    nearest_points_list = create_nearest_points_list(
        current_ring,
        tree,
        tree[node],
        constants.offset_factor_for_adjacent_geometry * offset,
        2.05 * offset
    )
    nearest_points_list.sort(key=lambda tup: tup.proj_distance_parent)

    result_coords = []
    if not nearest_points_list:
        # We have no children, so we're at the center of a spiral.  Reversing
        # the ring gives a nicer visual appearance.
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
            distance_so_far += child_connection.proj_distance_parent

            # Stitch the part leading up to this child.
            if before is not None:
                result_coords.extend(before.coords)

            # Stitch this child.  The child will start and end in the same
            # place, which should be close to our current location.
            child_path = connect_raster_tree_from_inner_to_outer(
                tree,
                child_connection.child_node,
                offset,
                stitch_distance,
                min_stitch_distance,
                child_connection.nearest_point_child,
                offset_by_half,
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


def orient_linear_ring(ring):
    if not ring.is_ccw:
        return LinearRing(reversed(ring.coords))
    else:
        return ring


def reorder_linear_ring(ring, start):
    # TODO: actually use start?
    start_index = np.argmin(np.linalg.norm(ring, axis=1))
    return np.roll(ring, -start_index, axis=0)


def interpolate_linear_rings(ring1, ring2, max_stitch_length, start=None):
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

    ring1 = orient_linear_ring(ring1)
    ring2 = orient_linear_ring(ring2)

    # Resample the two LinearRings so that they are the same number of points
    # long.  Then take the corresponding points in each ring and interpolate
    # between them, gradually going more toward ring2.
    #
    # This is a little less accurate than the method in interpolate(), but several
    # orders of magnitude faster because we're not building and querying a KDTree.

    num_points = int(20 * ring1.length / max_stitch_length)
    ring1_resampled = trimesh.path.traversal.resample_path(ring1, count=num_points)
    ring2_resampled = trimesh.path.traversal.resample_path(ring2, count=num_points)

    if start is not None:
        ring1_resampled = reorder_linear_ring(ring1_resampled, start)
        ring2_resampled = reorder_linear_ring(ring2_resampled, start)

    weights = np.linspace(0.0, 1.0, num_points).reshape((-1, 1))
    points = (ring1_resampled * (1.0 - weights)) + (ring2_resampled * weights)
    result = LineString(points)

    # TODO: remove when rastering is cheaper
    return result.simplify(constants.simplification_threshold, False)


def connect_raster_tree_spiral(tree, used_offset, stitch_distance, min_stitch_distance, close_point, offset_by_half):  # noqa: C901
    """
    Takes the offsetted curves organized as tree, connects and samples them as a spiral.
    It expects that each node in the tree has max. one child
    Input:
    -tree: contains the offsetted curves in a hierarchical organized
     data structure.
    -used_offset: used offset when the offsetted curves were generated
    -stitch_distance: maximum allowed distance between two points
     after sampling
    -min_stitch_distance stitches within a row shall be at least min_stitch_distance apart. Stitches connecting
     offsetted paths might be shorter.
    -close_point: defines the beginning point for stitching
     (stitching starts always from the undisplaced curve)
    -offset_by_half: If true the resulting points are interlaced otherwise not.
    Return values:
    -All offsetted curves connected to one spiral and sampled with
     points obeying stitch_distance and offset_by_half
    -Tag (origin) of each point to analyze why a point was
     placed at this position
    """

    if not tree['root']:  # if node has no children
        stitches = [Stitch(*point) for point in tree.nodes['root'].val.coords]
        return running_stitch(stitches, stitch_distance)

    starting_point = close_point.coords[0]
    path = []
    for node in nx.dfs_preorder_nodes(tree, 'root'):
        if tree[node]:
            ring1 = tree.nodes[node].val
            child = list(tree.successors(node))[0]
            ring2 = tree.nodes[child].val

            spiral_part = interpolate_linear_rings(ring1, ring2, stitch_distance, starting_point)
            path.extend(spiral_part.coords)

    path = [Stitch(*stitch) for stitch in path]

    return running_stitch(path, stitch_distance), None
