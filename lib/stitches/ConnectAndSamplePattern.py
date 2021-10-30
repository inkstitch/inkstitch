from shapely.geometry.polygon import LineString, LinearRing
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from collections import namedtuple
from depq import DEPQ
import math
from ..stitches import LineStringSampling
from ..stitches import PointTransfer
from ..stitches import constants

nearest_neighbor_tuple = namedtuple(
    "nearest_neighbor_tuple",
    [
        "nearest_point_parent",
        "nearest_point_child",
        "proj_distance_parent",
        "child_node",
    ],
)


def cut(line, distance):
    """
    Cuts a closed line so that the new closed line starts at the
    point with "distance" to the beginning of the old line.
    """
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        if i > 0 and p == coords[0]:
            pd = line.length
        else:
            pd = line.project(Point(p))
        if pd == distance:
            if coords[0] == coords[-1]:
                return LineString(coords[i:] + coords[1: i + 1])
            else:
                return LineString(coords[i:] + coords[:i])
        if pd > distance:
            cp = line.interpolate(distance)
            if coords[0] == coords[-1]:
                return LineString(
                    [(cp.x, cp.y)] + coords[i:] + coords[1:i] + [(cp.x, cp.y)]
                )
            else:
                return LineString([(cp.x, cp.y)] + coords[i:] + coords[:i])


def connect_raster_tree_nearest_neighbor(
    tree, used_offset, stitch_distance, close_point, offset_by_half
):
    """
    Takes the offsetted curves organized as tree, connects and samples them.
    Strategy: A connection from parent to child is made where both curves
    come closest together.
    Input:
    -tree: contains the offsetted curves in a hierachical organized
     data structure.
    -used_offset: used offset when the offsetted curves were generated
    -stitch_distance: maximum allowed distance between two points
     after sampling
    -close_point: defines the beginning point for stitching
     (stitching starts always from the undisplaced curve)
    -offset_by_half: If true the resulting points are interlaced otherwise not.
    Returnvalues:
    -All offsetted curves connected to one line and sampled with
     points obeying stitch_distance and offset_by_half
    -Tag (origin) of each point to analyze why a point was
     placed at this position
    """

    current_coords = tree.val
    abs_offset = abs(used_offset)
    result_coords = []
    result_coords_origin = []

    # We cut the current item so that its index 0 is closest to close_point
    start_distance = tree.val.project(close_point)
    if start_distance > 0:
        current_coords = cut(current_coords, start_distance)
        tree.val = current_coords

        if not tree.transferred_point_priority_deque.is_empty():
            new_DEPQ = DEPQ(iterable=None, maxlen=None)
            for item, priority in tree.transferred_point_priority_deque:
                new_DEPQ.insert(
                    item,
                    math.fmod(
                        priority - start_distance + current_coords.length,
                        current_coords.length,
                    ),
                )
            tree.transferred_point_priority_deque = new_DEPQ

    stitching_direction = 1
    # This list should contain a tuple of nearest points between
    # the current geometry and the subgeometry, the projected
    # distance along the current geometry, and the belonging subtree node
    nearest_points_list = []

    for subnode in tree.children:
        point_parent, point_child = nearest_points(current_coords, subnode.val)
        proj_distance = current_coords.project(point_parent)
        nearest_points_list.append(
            nearest_neighbor_tuple(
                nearest_point_parent=point_parent,
                nearest_point_child=point_child,
                proj_distance_parent=proj_distance,
                child_node=subnode,
            )
        )
    nearest_points_list.sort(
        reverse=False, key=lambda tup: tup.proj_distance_parent)

    if nearest_points_list:
        start_distance = min(
            abs_offset * constants.factor_offset_starting_points,
            nearest_points_list[0].proj_distance_parent,
        )
        end_distance = max(
            current_coords.length
            - abs_offset * constants.factor_offset_starting_points,
            nearest_points_list[-1].proj_distance_parent,
        )
    else:
        start_distance = abs_offset * constants.factor_offset_starting_points
        end_distance = (
            current_coords.length - abs_offset * constants.factor_offset_starting_points
        )

    (
        own_coords,
        own_coords_origin,
    ) = LineStringSampling.raster_line_string_with_priority_points(
        current_coords,
        start_distance,  # We add/subtract an offset to not sample
        # the same point again (avoid double
        # points for start and end)
        end_distance,
        stitch_distance,
        tree.transferred_point_priority_deque,
        abs_offset,
        offset_by_half,
        False
    )
    assert len(own_coords) == len(own_coords_origin)
    own_coords_origin[0] = LineStringSampling.PointSource.ENTER_LEAVING_POINT
    own_coords_origin[-1] = LineStringSampling.PointSource.ENTER_LEAVING_POINT
    tree.stitching_direction = stitching_direction
    tree.already_rastered = True

    # Next we need to transfer our rastered points to siblings and childs
    to_transfer_point_list = []
    to_transfer_point_list_origin = []
    for k in range(1, len(own_coords) - 1):
        # Do not take the first and the last since they are ENTER_LEAVING_POINT
        # points for sure

        if (
            not offset_by_half
            and own_coords_origin[k] == LineStringSampling.PointSource.EDGE_NEEDED
        ):
            continue
        if (
            own_coords_origin[k] == LineStringSampling.PointSource.ENTER_LEAVING_POINT
            or own_coords_origin[k] == LineStringSampling.PointSource.FORBIDDEN_POINT
        ):
            continue
        to_transfer_point_list.append(Point(own_coords[k]))
        point_origin = own_coords_origin[k]
        to_transfer_point_list_origin.append(point_origin)

    # Since the projection is only in ccw direction towards inner we need
    # to use "-used_offset" for stitching_direction==-1
    PointTransfer.transfer_points_to_surrounding(
        tree,
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
        PointTransfer.transfer_points_to_surrounding(
            tree,
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
        # If there is no child (inner geometry) we can simply take
        # our own rastered coords as result
        result_coords = own_coords
        result_coords_origin = own_coords_origin
    else:
        # There are childs so we need to merge their coordinates +
        # with our own rastered coords

        # To create a closed ring
        own_coords.append(own_coords[0])
        own_coords_origin.append(own_coords_origin[0])

        # own_coords does not start with current_coords but has an offset
        # (see call of raster_line_string_with_priority_points)
        total_distance = start_distance
        cur_item = 0
        result_coords = [own_coords[0]]
        result_coords_origin = [
            LineStringSampling.PointSource.ENTER_LEAVING_POINT]
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

                item = nearest_points_list[cur_item]
                (
                    child_coords,
                    child_coords_origin,
                ) = connect_raster_tree_nearest_neighbor(
                    item.child_node,
                    used_offset,
                    stitch_distance,
                    item.nearest_point_child,
                    offset_by_half,
                )

                d = item.nearest_point_parent.distance(
                    Point(own_coords[i - 1]))
                if d > abs_offset * constants.factor_offset_starting_points:
                    result_coords.append(item.nearest_point_parent.coords[0])
                    result_coords_origin.append(
                        LineStringSampling.PointSource.ENTER_LEAVING_POINT
                    )
                # reversing avoids crossing when entering and
                # leaving the child segment
                result_coords.extend(child_coords[::-1])
                result_coords_origin.extend(child_coords_origin[::-1])

                # And here we calculate the point for the leaving
                d = item.nearest_point_parent.distance(Point(own_coords[i]))
                if cur_item < len(nearest_points_list) - 1:
                    d = min(
                        d,
                        abs(
                            nearest_points_list[cur_item +
                                                1].proj_distance_parent
                            - item.proj_distance_parent
                        ),
                    )

                if d > abs_offset * constants.factor_offset_starting_points:
                    result_coords.append(
                        current_coords.interpolate(
                            item.proj_distance_parent
                            + abs_offset * constants.factor_offset_starting_points
                        ).coords[0]
                    )
                    result_coords_origin.append(
                        LineStringSampling.PointSource.ENTER_LEAVING_POINT
                    )

                cur_item += 1
            if i < len(own_coords) - 1:
                if (
                    Point(result_coords[-1]).distance(Point(own_coords[i]))
                    > abs_offset * constants.factor_offset_remove_points
                ):
                    result_coords.append(own_coords[i])
                    result_coords_origin.append(own_coords_origin[i])

            # Since current_coords and temp are rastered differently
            # there accumulate errors regarding the current distance.
            # Since a projection of each point in temp would be very time
            # consuming we project only every n-th point which resets
            # the accumulated error every n-th point.
            if i % 20 == 0:
                total_distance = current_coords.project(Point(own_coords[i]))
            else:
                total_distance += next_distance

    assert len(result_coords) == len(result_coords_origin)
    return result_coords, result_coords_origin


def get_nearest_points_closer_than_thresh(travel_line, next_line, thresh):
    """
    Takes a line and calculates the nearest distance along this
    line to enter the next_line
    Input:
    -travel_line: The "parent" line for which the distance should
     be minimized to enter next_line
    -next_line: contains the next_line which need to be entered
    -thresh: The distance between travel_line and next_line needs
     to below thresh to be a valid point for entering
    Output:
    -tuple - the tuple structure is:
     (nearest point in travel_line, nearest point in next_line)
    """
    point_list = list(MultiPoint(travel_line.coords))

    if point_list[0].distance(next_line) < thresh:
        return nearest_points(point_list[0], next_line)

    for i in range(len(point_list) - 1):
        line_segment = LineString([point_list[i], point_list[i + 1]])
        result = nearest_points(line_segment, next_line)

        if result[0].distance(result[1]) < thresh:
            return result
    line_segment = LineString([point_list[-1], point_list[0]])
    result = nearest_points(line_segment, next_line)

    if result[0].distance(result[1]) < thresh:
        return result
    else:
        return None


def create_nearest_points_list(
    travel_line, children_list, threshold, threshold_hard, preferred_direction=0
):
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

    result_list_in_order = []
    result_list_reversed_order = []

    travel_line_reversed = LinearRing(travel_line.coords[::-1])

    weight_in_order = 0
    weight_reversed_order = 0
    for child in children_list:
        result = get_nearest_points_closer_than_thresh(
            travel_line, child.val, threshold
        )
        if result is None:
            # where holes meet outer borders a distance
            # up to 2*used offset can arise
            result = get_nearest_points_closer_than_thresh(
                travel_line, child.val, threshold_hard
            )
            assert result is not None
        proj = travel_line.project(result[0])
        weight_in_order += proj
        result_list_in_order.append(
            nearest_neighbor_tuple(
                nearest_point_parent=result[0],
                nearest_point_child=result[1],
                proj_distance_parent=proj,
                child_node=child,
            )
        )

        result = get_nearest_points_closer_than_thresh(
            travel_line_reversed, child.val, threshold
        )
        if result is None:
            # where holes meet outer borders a distance
            # up to 2*used offset can arise
            result = get_nearest_points_closer_than_thresh(
                travel_line_reversed, child.val, threshold_hard
            )
            assert result is not None
        proj = travel_line_reversed.project(result[0])
        weight_reversed_order += proj
        result_list_reversed_order.append(
            nearest_neighbor_tuple(
                nearest_point_parent=result[0],
                nearest_point_child=result[1],
                proj_distance_parent=proj,
                child_node=child,
            )
        )

    if preferred_direction == 1:
        # Reduce weight_in_order to make in order stitching more preferred
        weight_in_order = min(
            weight_in_order / 2, max(0, weight_in_order - 10 * threshold)
        )
        if weight_in_order == weight_reversed_order:
            return (1, result_list_in_order)
    elif preferred_direction == -1:
        # Reduce weight_reversed_order to make reversed
        # stitching more preferred
        weight_reversed_order = min(
            weight_reversed_order /
            2, max(0, weight_reversed_order - 10 * threshold)
        )
        if weight_in_order == weight_reversed_order:
            return (-1, result_list_reversed_order)

    if weight_in_order < weight_reversed_order:
        return (1, result_list_in_order)
    else:
        return (-1, result_list_reversed_order)


def calculate_replacing_middle_point(line_segment, abs_offset, max_stitch_distance):
    """
    Takes a line segment (consisting of 3 points!)
    and calculates a new middle point if the line_segment is
    straight enough to be resampled by points max_stitch_distance apart.
    Returns None if the middle point is not needed.
    """
    angles = LineStringSampling.calculate_line_angles(line_segment)
    if angles[1] < abs_offset * constants.limiting_angle_straight:
        if line_segment.length < max_stitch_distance:
            return None
        else:
            return line_segment.interpolate(
                line_segment.length - max_stitch_distance
            ).coords[0]
    else:
        return line_segment.coords[1]


def connect_raster_tree_from_inner_to_outer(
    tree, used_offset, stitch_distance, close_point, offset_by_half
):
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
    -close_point: defines the beginning point for stitching
     (stitching starts always from the undisplaced curve)
    -offset_by_half: If true the resulting points are interlaced otherwise not.
    Returnvalues:
    -All offsetted curves connected to one line and sampled with points obeying
     stitch_distance and offset_by_half
    -Tag (origin) of each point to analyze why a point was placed
     at this position
    """

    current_coords = tree.val
    abs_offset = abs(used_offset)
    result_coords = []
    result_coords_origin = []

    start_distance = tree.val.project(close_point)
    # We cut the current path so that its index 0 is closest to close_point
    if start_distance > 0:
        current_coords = cut(current_coords, start_distance)
        tree.val = current_coords

        if not tree.transferred_point_priority_deque.is_empty():
            new_DEPQ = DEPQ(iterable=None, maxlen=None)
            for item, priority in tree.transferred_point_priority_deque:
                new_DEPQ.insert(
                    item,
                    math.fmod(
                        priority - start_distance + current_coords.length,
                        current_coords.length,
                    ),
                )
            tree.transferred_point_priority_deque = new_DEPQ

    # We try to use always the opposite stitching direction with respect to the
    # parent to avoid crossings when entering and leaving the child
    parent_stitching_direction = -1
    if tree.parent is not None:
        parent_stitching_direction = tree.parent.stitching_direction

    # Find the nearest point in current_coords and its children and
    # sort it along the stitching direction
    stitching_direction, nearest_points_list = create_nearest_points_list(
        current_coords,
        tree.children,
        1.5 * abs_offset,
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
        end_offset = (
            current_coords.length - abs_offset * constants.factor_offset_starting_points
        )

    if stitching_direction == 1:
        (
            own_coords,
            own_coords_origin,
        ) = LineStringSampling.raster_line_string_with_priority_points(
            current_coords,
            start_offset,  # We add start_offset to not sample the same
            # point again (avoid double points for start
            # and end)
            end_offset,
            stitch_distance,
            tree.transferred_point_priority_deque,
            abs_offset,
            offset_by_half,
            False
        )
    else:
        (
            own_coords,
            own_coords_origin,
        ) = LineStringSampling.raster_line_string_with_priority_points(
            current_coords,
            current_coords.length - start_offset,  # We subtract
            # start_offset to not
            # sample the same point
            # again (avoid double
            # points for start
            # and end)
            current_coords.length - end_offset,
            stitch_distance,
            tree.transferred_point_priority_deque,
            abs_offset,
            offset_by_half,
            False
        )
        current_coords.coords = current_coords.coords[::-1]

    assert len(own_coords) == len(own_coords_origin)

    tree.stitching_direction = stitching_direction
    tree.already_rastered = True

    to_transfer_point_list = []
    to_transfer_point_list_origin = []
    for k in range(0, len(own_coords)):
        # TODO: maybe do not take the first and the last
        # since they are ENTER_LEAVING_POINT points for sure
        if (
            not offset_by_half
            and own_coords_origin[k] == LineStringSampling.PointSource.EDGE_NEEDED
            or own_coords_origin[k] == LineStringSampling.PointSource.FORBIDDEN_POINT
        ):
            continue
        if own_coords_origin[k] == LineStringSampling.PointSource.ENTER_LEAVING_POINT:
            continue
        to_transfer_point_list.append(Point(own_coords[k]))
        to_transfer_point_list_origin.append(own_coords_origin[k])

    assert len(to_transfer_point_list) == len(to_transfer_point_list_origin)

    # Next we need to transfer our rastered points to siblings and childs
    # Since the projection is only in ccw direction towards inner we
    # need to use "-used_offset" for stitching_direction==-1
    PointTransfer.transfer_points_to_surrounding(
        tree,
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
        PointTransfer.transfer_points_to_surrounding(
            tree,
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
                (
                    child_coords,
                    child_coords_origin,
                ) = connect_raster_tree_from_inner_to_outer(
                    item.child_node,
                    used_offset,
                    stitch_distance,
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
                if (
                    Point(result_coords[-1]
                          ).distance(item.nearest_point_parent)
                    > constants.factor_offset_starting_points * abs_offset
                ):
                    result_coords.append(item.nearest_point_parent.coords[0])
                    result_coords_origin.append(
                        LineStringSampling.PointSource.ENTER_LEAVING_POINT
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
                        abs(
                            nearest_points_list[cur_item +
                                                1].proj_distance_parent
                            - item.proj_distance_parent
                        ),
                    )

                if d > constants.factor_offset_starting_points * abs_offset:
                    result_coords.append(
                        current_coords.interpolate(
                            item.proj_distance_parent
                            + 2 * constants.factor_offset_starting_points * abs_offset
                        ).coords[0]
                    )
                    result_coords_origin.append(
                        LineStringSampling.PointSource.ENTER_LEAVING_POINT
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
                if (
                    Point(result_coords[-1]).distance(Point(own_coords[i]))
                    > abs_offset * constants.factor_offset_remove_points
                ):
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
