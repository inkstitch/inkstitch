import math
from collections import namedtuple
import networkx as nx
import numpy as np
import trimesh
from depq import DEPQ
from shapely.geometry import Point, LineString, LinearRing, MultiLineString
from shapely.ops import nearest_points

from .running_stitch import running_stitch

from ..debug import debug
from ..stitches import constants
from ..stitches import point_transfer
from ..stitches import sample_linestring
from ..stitch_plan import Stitch
from ..utils.geometry import roll_linear_ring

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
        travel_line, tree, children_list, threshold, threshold_hard, preferred_direction=0):
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

    return (1, children_nearest_points)


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


def connect_raster_tree_from_inner_to_outer(tree, node, used_offset, stitch_distance, min_stitch_distance, close_point,
                                            offset_by_half):  # noqa: C901
    """
    Takes the offsetted curves organized as tree, connects and samples them.
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
    current_coords = current_node.val
    abs_offset = abs(used_offset)
    result_coords = []
    result_coords_origin = []

    start_distance = current_coords.project(close_point)
    # We cut the current path so that its index 0 is closest to close_point
    if start_distance > 0:
        current_coords = roll_linear_ring(current_coords, start_distance)
        current_node.val = current_coords

        if not current_node.transferred_point_priority_deque.is_empty():
            new_DEPQ = DEPQ(iterable=None, maxlen=None)
            for item, priority in current_node.transferred_point_priority_deque:
                new_DEPQ.insert(
                    item,
                    math.fmod(
                        priority - start_distance + current_coords.length,
                        current_coords.length,
                    ),
                )
            current_node.transferred_point_priority_deque = new_DEPQ

    # We try to use always the opposite stitching direction with respect to the
    # parent to avoid crossings when entering and leaving the child
    # LEX: this seems like a lie ^^
    parent_stitching_direction = -1
    if current_node.parent is not None:
        parent_stitching_direction = tree.nodes[current_node.parent].stitching_direction

    # Find the nearest point in current_coords and its children and
    # sort it along the stitching direction
    stitching_direction, nearest_points_list = create_nearest_points_list(
        current_coords,
        tree,
        tree[node],
        constants.offset_factor_for_adjacent_geometry * abs_offset,
        2.05 * abs_offset,
        parent_stitching_direction,
    )
    nearest_points_list.sort(
        reverse=False, key=lambda tup: tup.proj_distance_parent)

    # Have a small offset for the starting and ending to avoid double points
    # at start and end point (since the paths are closed rings)
    if nearest_points_list:
        start_offset = min(
            abs_offset * constants.factor_offset_starting_points,
            nearest_points_list[0].proj_distance_parent,
        )
        end_offset = max(
            current_coords.length
            - abs_offset * constants.factor_offset_starting_points,
            nearest_points_list[-1].proj_distance_parent,
        )
    else:
        start_offset = abs_offset * constants.factor_offset_starting_points
        end_offset = (current_coords.length - abs_offset * constants.factor_offset_starting_points)

    if stitching_direction == 1:
        (own_coords, own_coords_origin) = sample_linestring.raster_line_string_with_priority_points(
            current_coords,
            start_offset,  # We add start_offset to not sample the initial/end
            # point twice (avoid double points for start
            # and end)
            end_offset,
            stitch_distance,
            min_stitch_distance,
            current_node.transferred_point_priority_deque,
            abs_offset,
            offset_by_half,
            False
        )
    else:
        (own_coords, own_coords_origin) = sample_linestring.raster_line_string_with_priority_points(
            current_coords,
            current_coords.length - start_offset,  # We subtract
            # start_offset to not
            # sample the initial/end point
            # twice (avoid double
            # points for start
            # and end)
            current_coords.length - end_offset,
            stitch_distance,
            min_stitch_distance,
            current_node.transferred_point_priority_deque,
            abs_offset,
            offset_by_half,
            False
        )
        current_coords.coords = current_coords.coords[::-1]

    assert len(own_coords) == len(own_coords_origin)

    current_node.stitching_direction = stitching_direction
    current_node.already_rastered = True

    to_transfer_point_list = []
    to_transfer_point_list_origin = []
    for k in range(0, len(own_coords)):
        # TODO: maybe do not take the first and the last
        # since they are ENTER_LEAVING_POINT points for sure
        if (
                not offset_by_half
                and own_coords_origin[k] == sample_linestring.PointSource.EDGE_NEEDED
                or own_coords_origin[k] == sample_linestring.PointSource.FORBIDDEN_POINT):
            continue
        if own_coords_origin[k] == sample_linestring.PointSource.ENTER_LEAVING_POINT:
            continue
        to_transfer_point_list.append(Point(own_coords[k]))
        to_transfer_point_list_origin.append(own_coords_origin[k])

    assert len(to_transfer_point_list) == len(to_transfer_point_list_origin)

    # Next we need to transfer our rastered points to siblings and childs
    # Since the projection is only in ccw direction towards inner we
    # need to use "-used_offset" for stitching_direction==-1
    point_transfer.transfer_points_to_surrounding(
        tree,
        node,
        stitching_direction * used_offset,
        offset_by_half,
        to_transfer_point_list,
        to_transfer_point_list_origin,
        overnext_neighbor=False,
        transfer_forbidden_points=False,
        transfer_to_parent=False,
        transfer_to_sibling=True,
        transfer_to_child=True,
    )

    # We transfer also to the overnext child to get a more straight
    # arrangement of points perpendicular to the stitching lines
    if offset_by_half:
        point_transfer.transfer_points_to_surrounding(
            tree,
            node,
            stitching_direction * used_offset,
            False,
            to_transfer_point_list,
            to_transfer_point_list_origin,
            overnext_neighbor=True,
            transfer_forbidden_points=False,
            transfer_to_parent=False,
            transfer_to_sibling=True,
            transfer_to_child=True,
        )

    if not nearest_points_list:
        # If there is no child (inner geometry) we can simply
        # take our own rastered coords as result
        result_coords = own_coords
        result_coords_origin = own_coords_origin
    else:
        # There are childs so we need to merge their coordinates
        # with our own rastered coords

        # Create a closed ring for the following code
        own_coords.append(own_coords[0])
        own_coords_origin.append(own_coords_origin[0])

        # own_coords does not start with current_coords but has an offset
        # (see call of raster_line_string_with_priority_points)
        total_distance = start_offset

        cur_item = 0
        result_coords = [own_coords[0]]
        result_coords_origin = [own_coords_origin[0]]

        for i in range(1, len(own_coords)):
            next_distance = math.sqrt(
                (own_coords[i][0] - own_coords[i - 1][0]) ** 2
                + (own_coords[i][1] - own_coords[i - 1][1]) ** 2
            )
            while (
                cur_item < len(nearest_points_list)
                and total_distance + next_distance + constants.eps
                > nearest_points_list[cur_item].proj_distance_parent
            ):
                # The current and the next point in own_coords enclose the
                # nearest point tuple between this geometry and child
                # geometry. Hence we need to insert the child geometry points
                # here before the next point of own_coords.
                item = nearest_points_list[cur_item]
                (child_coords, child_coords_origin) = connect_raster_tree_from_inner_to_outer(
                    tree,
                    item.child_node,
                    used_offset,
                    stitch_distance,
                    min_stitch_distance,
                    item.nearest_point_child,
                    offset_by_half,
                )

                # Imagine the nearest point of the child is within a long
                # segment of the parent. Without additonal points
                # on the parent side this would cause noticeable deviations.
                # Hence we add here points shortly before and after
                # the entering of the child to have only minor deviations to
                # the desired shape.
                # Here is the point for the entering:
                if (Point(result_coords[-1]).distance(item.nearest_point_parent) > constants.factor_offset_starting_points * abs_offset):
                    result_coords.append(item.nearest_point_parent.coords[0])
                    result_coords_origin.append(
                        sample_linestring.PointSource.ENTER_LEAVING_POINT
                    )

                # Check whether the number of points of the connecting lines
                # from child to child can be reduced
                if len(child_coords) > 1:
                    point = calculate_replacing_middle_point(
                        LineString(
                            [result_coords[-1], child_coords[0], child_coords[1]]
                        ),
                        abs_offset,
                        stitch_distance,
                    )

                    if point is not None:
                        result_coords.append(point)
                        result_coords_origin.append(child_coords_origin[0])

                    result_coords.extend(child_coords[1:])
                    result_coords_origin.extend(child_coords_origin[1:])
                else:
                    result_coords.extend(child_coords)
                    result_coords_origin.extend(child_coords_origin)

                # And here is the point for the leaving of the child
                # (distance to the own following point should not be too large)
                d = item.nearest_point_parent.distance(Point(own_coords[i]))
                if cur_item < len(nearest_points_list) - 1:
                    d = min(
                        d,
                        abs(nearest_points_list[cur_item + 1].proj_distance_parent - item.proj_distance_parent),
                    )

                if d > constants.factor_offset_starting_points * abs_offset:
                    result_coords.append(
                        current_coords.interpolate(item.proj_distance_parent + 2 * constants.factor_offset_starting_points * abs_offset).coords[0]
                    )
                    result_coords_origin.append(
                        sample_linestring.PointSource.ENTER_LEAVING_POINT
                    )
                    # Check whether this additional point makes the last point
                    # of the child unnecessary
                    point = calculate_replacing_middle_point(
                        LineString(
                            [result_coords[-3], result_coords[-2], result_coords[-1]]
                        ),
                        abs_offset,
                        stitch_distance,
                    )
                    if point is None:
                        result_coords.pop(-2)
                        result_coords_origin.pop(-2)

                cur_item += 1
            if i < len(own_coords) - 1:
                if (Point(result_coords[-1]).distance(Point(own_coords[i])) > abs_offset * constants.factor_offset_remove_points):
                    result_coords.append(own_coords[i])
                    result_coords_origin.append(own_coords_origin[i])

            # Since current_coords and own_coords are rastered differently
            # there accumulate errors regarding the current distance.
            # Since a projection of each point in own_coords would be very
            # time consuming we project only every n-th point which resets
            # the accumulated error every n-th point.
            if i % 20 == 0:
                total_distance = current_coords.project(Point(own_coords[i]))
            else:
                total_distance += next_distance

    assert len(result_coords) == len(result_coords_origin)
    return result_coords, result_coords_origin


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
