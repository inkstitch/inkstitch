from enum import IntEnum

import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import substring

from ..stitches import constants, point_transfer


class PointSource(IntEnum):
    """
    Used to tag the origin of a rastered point
    """
    # MUST_USE = 0  # Legacy
    REGULAR_SPACING = 1  # introduced to not exceed maximal stichting distance
    # INITIAL_RASTERING = 2  #Legacy
    # point which must be stitched to avoid to large deviations to the desired path
    EDGE_NEEDED = 3
    # NOT_NEEDED = 4 #Legacy
    # ALREADY_TRANSFERRED = 5 #Legacy
    # ADDITIONAL_TRACKING_POINT_NOT_NEEDED = 6 #Legacy
    # EDGE_RASTERING_ALLOWED = 7 #Legacy
    # EDGE_PREVIOUSLY_SHIFTED = 8  #Legacy
    ENTER_LEAVING_POINT = 9  # Whether this point is used to enter or leave a child
    # If the angle at a point is <= constants.limiting_angle this point is marked as SOFT_EDGE
    SOFT_EDGE_INTERNAL = 10
    # If the angle at a point is > constants.limiting_angle this point is marked as HARD_EDGE (HARD_EDGES will always be stitched)
    HARD_EDGE_INTERNAL = 11
    # If the point was created by a projection (transferred point) of a neighbor it is marked as PROJECTED_POINT
    PROJECTED_POINT = 12
    REGULAR_SPACING_INTERNAL = 13  # introduced to not exceed maximal stichting distance
    # FORBIDDEN_POINT_INTERNAL=14  #Legacy
    SOFT_EDGE = 15  # If the angle at a point is <= constants.limiting_angle this point is marked as SOFT_EDGE
    # If the angle at a point is > constants.limiting_angle this point is marked as HARD_EDGE (HARD_EDGES will always be stitched)
    HARD_EDGE = 16
    FORBIDDEN_POINT = 17  # Only relevant for desired interlacing - non-shifted point positions at the next neighbor are marked as forbidden
    # If one decides to avoid forbidden points new points to the left and to the right as replacement are created
    REPLACED_FORBIDDEN_POINT = 18
    DIRECT = 19  # Calculated by next neighbor projection
    OVERNEXT = 20  # Calculated by overnext neighbor projection


def calculate_line_angles(line):
    """
    Calculates the angles between adjacent edges at each interior point
    Note that the first and last values in the return array are zero since for the boundary points no
    angle calculations were possible
    """
    angles = np.zeros(len(line.coords))

    # approach from https://stackoverflow.com/a/50772253/4249120
    vectors = np.diff(line.coords, axis=0)
    v1 = vectors[:-1]
    v2 = vectors[1:]
    dot = np.einsum('ij,ij->i', v1, v2)
    mag1 = np.linalg.norm(v1, axis=1)
    mag2 = np.linalg.norm(v2, axis=1)
    cosines = dot / (mag1 * mag2)
    angles[1:-1] = np.arccos(np.clip(cosines, -1, 1))

    return angles


def raster_line_string_with_priority_points(line,  # noqa: C901
                                            start_distance,
                                            end_distance,
                                            maxstitch_distance,
                                            minstitch_distance,
                                            must_use_points_deque,
                                            abs_offset,
                                            offset_by_half,
                                            replace_forbidden_points):
    """
    Rasters a line between start_distance and end_distance.
    Input:
    -line: The line to be rastered
    -start_distance: The distance along the line from which the rastering should start
    -end_distance: The distance along the line until which the rastering should be done
    -maxstitch_distance: The maximum allowed stitch distance
    -minstitch_distance: The minimum allowed stitch distance
    -Note that start_distance > end_distance for stitching_direction = -1
    -must_use_points_deque: deque with projected points on line from its neighbors. An item of the deque
     is setup as follows: ((projected point on line, LineStringSampling.PointSource), priority=distance along line)
     index of point_origin is the index of the point in the neighboring line
    -abs_offset: used offset between to offsetted curves
    -offset_by_half: Whether the points of neighboring lines shall be interlaced or not
    -replace_forbidden_points: Whether points marked as forbidden in must_use_points_deque shall be replaced by adjacend points
    Output:
    -List of tuples with the rastered point coordinates
    -List which defines the point origin for each point according to the PointSource enum.
    """

    if (abs(end_distance-start_distance) < max(minstitch_distance, constants.line_lengh_seen_as_one_point)):
        return [line.interpolate(start_distance).coords[0]], [PointSource.HARD_EDGE]

    deque_points = list(must_use_points_deque)

    linecoords = line.coords

    if start_distance > end_distance:
        start_distance, end_distance = line.length - \
                                       start_distance, line.length - end_distance
        linecoords = linecoords[::-1]
        for i in range(len(deque_points)):
            deque_points[i] = (deque_points[i][0],
                               line.length - deque_points[i][1])
    else:
        # Since points with highest priority (=distance along line) are first (descending sorted)
        deque_points = deque_points[::-1]

    # Remove all points from the deque which do not fall in the segment [start_distance; end_distance]
    while (len(deque_points) > 0 and
           deque_points[0][1] <= start_distance + min(maxstitch_distance / 20, minstitch_distance, constants.point_spacing_to_be_considered_equal)):
        deque_points.pop(0)
    while (len(deque_points) > 0 and
           deque_points[-1][1] >= end_distance - min(maxstitch_distance / 20, minstitch_distance, constants.point_spacing_to_be_considered_equal)):
        deque_points.pop()

    # Ordering in priority queue:
    #   (point, LineStringSampling.PointSource), priority)
    # might be different from line for stitching_direction=-1
    aligned_line = LineString(linecoords)
    path_coords = substring(aligned_line,
                            start_distance, end_distance)

    # aligned line is a line without doubled points.
    # I had the strange situation in which the offset "start_distance" from the line beginning
    # resulted in a starting point which was already present in aligned_line causing a doubled point.
    # A double point is not allowed in the following calculations so we need to remove it:
    if (abs(path_coords.coords[0][0] - path_coords.coords[1][0]) < constants.eps and
            abs(path_coords.coords[0][1] - path_coords.coords[1][1]) < constants.eps):
        path_coords.coords = path_coords.coords[1:]
    if (abs(path_coords.coords[-1][0] - path_coords.coords[-2][0]) < constants.eps and
            abs(path_coords.coords[-1][1] - path_coords.coords[-2][1]) < constants.eps):
        path_coords.coords = path_coords.coords[:-1]

    angles = calculate_line_angles(path_coords)
    # For the first and last point we cannot calculate an angle. Set it to above the limit to make it a hard edge
    angles[0] = 1.1 * constants.limiting_angle
    angles[-1] = 1.1 * constants.limiting_angle

    current_distance = 0
    last_point = Point(path_coords.coords[0])
    # Next we merge the line points and the projected (deque) points into one list
    merged_point_list = []
    dq_iter = 0
    for point, angle in zip(path_coords.coords, angles):
        current_distance += last_point.distance(Point(point))
        last_point = Point(point)
        while dq_iter < len(deque_points) and deque_points[dq_iter][1] < current_distance+start_distance:
            # We want to avoid setting points at soft edges close to forbidden points
            if deque_points[dq_iter][0].point_source == PointSource.FORBIDDEN_POINT:
                # Check whether a previous added point is a soft edge close to the forbidden point
                if (merged_point_list[-1][0].point_source == PointSource.SOFT_EDGE_INTERNAL and
                   abs(merged_point_list[-1][1]-deque_points[dq_iter][1]+start_distance < abs_offset*constants.factor_offset_forbidden_point)):
                    item = merged_point_list.pop()
                    merged_point_list.append((point_transfer.projected_point_tuple(
                        point=item[0].point, point_source=PointSource.FORBIDDEN_POINT), item[1]-start_distance))
            else:
                merged_point_list.append(
                    (deque_points[dq_iter][0], deque_points[dq_iter][1]-start_distance))
                # merged_point_list.append(deque_points[dq_iter])
            dq_iter += 1
        # Check whether the current point is close to a forbidden point
        if (dq_iter < len(deque_points) and
            deque_points[dq_iter-1][0].point_source == PointSource.FORBIDDEN_POINT and
            angle < constants.limiting_angle and
                abs(deque_points[dq_iter-1][1]-current_distance-start_distance) < abs_offset*constants.factor_offset_forbidden_point):
            point_source = PointSource.FORBIDDEN_POINT
        else:
            if angle < constants.limiting_angle:
                point_source = PointSource.SOFT_EDGE_INTERNAL
            else:
                point_source = PointSource.HARD_EDGE_INTERNAL
        merged_point_list.append((point_transfer.projected_point_tuple(
            point=Point(point), point_source=point_source), current_distance))

    result_list = [merged_point_list[0]]

    # General idea: Take one point of merged_point_list after another into the current segment until this segment is not simplified
    # to a straight line by shapelys simplify method.
    # Then, look at the points within this segment and choose the best fitting one
    # (HARD_EDGE > OVERNEXT projected point > DIRECT projected point) as termination of this segment
    # and start point for the next segment (so we do not always take the maximum possible length for a segment)
    segment_start_index = 0
    segment_end_index = 1
    forbidden_point_list = []
    while segment_end_index < len(merged_point_list):
        # Collection of points for the current segment
        current_point_list = [merged_point_list[segment_start_index][0].point]

        while segment_end_index < len(merged_point_list):
            segment_length = merged_point_list[segment_end_index][1] - \
                merged_point_list[segment_start_index][1]
            if segment_length < minstitch_distance:
                segment_end_index += 1
                continue
            if segment_length > maxstitch_distance+constants.point_spacing_to_be_considered_equal:
                new_distance = merged_point_list[segment_start_index][1] + \
                    maxstitch_distance
                merged_point_list.insert(segment_end_index, (point_transfer.projected_point_tuple(
                    point=aligned_line.interpolate(new_distance), point_source=PointSource.REGULAR_SPACING_INTERNAL), new_distance))
                segment_end_index += 1
                break

            current_point_list.append(
                merged_point_list[segment_end_index][0].point)
            simplified_len = len(LineString(current_point_list).simplify(
                constants.factor_offset_remove_dense_points*abs_offset, preserve_topology=False).coords)
            if simplified_len > 2:  # not all points have been simplified - so we need to add it
                break

            if merged_point_list[segment_end_index][0].point_source == PointSource.HARD_EDGE_INTERNAL:
                segment_end_index += 1
                break
            segment_end_index += 1

        segment_end_index -= 1

        # Now we choose the best fitting point within this segment
        index_overnext = -1
        index_direct = -1
        index_hard_edge = -1

        iter = segment_start_index+1
        while (iter <= segment_end_index):
            segment_length = merged_point_list[iter][1] - \
                merged_point_list[segment_start_index][1]
            if segment_length < minstitch_distance and merged_point_list[iter][0].point_source != PointSource.HARD_EDGE_INTERNAL:
                # We need to create this hard edge exception - otherwise there are some too large deviations posible
                iter += 1
                continue

            if merged_point_list[iter][0].point_source == PointSource.OVERNEXT:
                index_overnext = iter
            elif merged_point_list[iter][0].point_source == PointSource.DIRECT:
                index_direct = iter
            elif merged_point_list[iter][0].point_source == PointSource.HARD_EDGE_INTERNAL:
                index_hard_edge = iter
            iter += 1
        if index_hard_edge != -1:
            segment_end_index = index_hard_edge
        else:
            if offset_by_half:
                index_preferred = index_overnext
                index_less_preferred = index_direct
            else:
                index_preferred = index_direct
                index_less_preferred = index_overnext

            if index_preferred != -1:
                if (index_less_preferred != -1 and index_less_preferred > index_preferred and
                        (merged_point_list[index_less_preferred][1]-merged_point_list[index_preferred][1]) >=
                        constants.factor_segment_length_direct_preferred_over_overnext *
                        (merged_point_list[index_preferred][1]-merged_point_list[segment_start_index][1])):
                    # We allow to take the direct projected point instead of the overnext projected point if it would result in a
                    # significant longer segment length
                    segment_end_index = index_less_preferred
                else:
                    segment_end_index = index_preferred
            elif index_less_preferred != -1:
                segment_end_index = index_less_preferred

        # Usually OVERNEXT and DIRECT points are close to each other and in some cases both were selected as segment edges
        # If they are too close (<abs_offset) we remove one of it
        if (((merged_point_list[segment_start_index][0].point_source == PointSource.OVERNEXT and
            merged_point_list[segment_end_index][0].point_source == PointSource.DIRECT) or
            (merged_point_list[segment_start_index][0].point_source == PointSource.DIRECT and
            merged_point_list[segment_end_index][0].point_source == PointSource.OVERNEXT)) and
                abs(merged_point_list[segment_end_index][1] - merged_point_list[segment_start_index][1]) < abs_offset):
            result_list.pop()

        result_list.append(merged_point_list[segment_end_index])
        # To have a chance to replace all forbidden points afterwards
        if merged_point_list[segment_end_index][0].point_source == PointSource.FORBIDDEN_POINT:
            forbidden_point_list.append(len(result_list)-1)

        segment_start_index = segment_end_index
        segment_end_index += 1

    return_point_list = []  # [result_list[0][0].point.coords[0]]
    return_point_source_list = []  # [result_list[0][0].point_source]

    # Note: replacement of forbidden points sometimes not satisfying
    if replace_forbidden_points:
        result_list = _replace_forbidden_points(
            aligned_line, result_list, forbidden_point_list, abs_offset)

    # Finally we create the final return_point_list and return_point_source_list
    for i in range(len(result_list)):
        return_point_list.append(result_list[i][0].point.coords[0])
        if result_list[i][0].point_source == PointSource.HARD_EDGE_INTERNAL:
            point_source = PointSource.HARD_EDGE
        elif result_list[i][0].point_source == PointSource.SOFT_EDGE_INTERNAL:
            point_source = PointSource.SOFT_EDGE
        elif result_list[i][0].point_source == PointSource.REGULAR_SPACING_INTERNAL:
            point_source = PointSource.REGULAR_SPACING
        elif result_list[i][0].point_source == PointSource.FORBIDDEN_POINT:
            point_source = PointSource.FORBIDDEN_POINT
        else:
            point_source = PointSource.PROJECTED_POINT

        return_point_source_list.append(point_source)

    assert(len(return_point_list) == len(return_point_source_list))

    # return remove_dense_points(returnpointlist, returnpointsourcelist, maxstitch_distance,abs_offset)
    return return_point_list, return_point_source_list


def _replace_forbidden_points(line, result_list, forbidden_point_list_indices, abs_offset):
    # since we add and remove points in the result_list, we need to adjust the indices stored in forbidden_point_list_indices
    current_index_shift = 0
    for index in forbidden_point_list_indices:
        index += current_index_shift
        distance_left = result_list[index][0].point.distance(
            result_list[index-1][0].point)/2.0
        distance_right = result_list[index][0].point.distance(
            result_list[(index+1) % len(result_list)][0].point)/2.0
        while distance_left > constants.point_spacing_to_be_considered_equal and distance_right > constants.point_spacing_to_be_considered_equal:
            new_point_left_proj = result_list[index][1]-distance_left
            if new_point_left_proj < 0:
                new_point_left_proj += line.length
            new_point_right_proj = result_list[index][1]+distance_right
            if new_point_right_proj > line.length:
                new_point_right_proj -= line.length
            point_left = line.interpolate(new_point_left_proj)
            point_right = line.interpolate(new_point_right_proj)
            forbidden_point_distance = result_list[index][0].point.distance(
                LineString([point_left, point_right]))
            if forbidden_point_distance < constants.factor_offset_remove_dense_points*abs_offset:
                del result_list[index]
                result_list.insert(index, (point_transfer.projected_point_tuple(
                    point=point_right, point_source=PointSource.REPLACED_FORBIDDEN_POINT), new_point_right_proj))
                result_list.insert(index, (point_transfer.projected_point_tuple(
                    point=point_left, point_source=PointSource.REPLACED_FORBIDDEN_POINT), new_point_left_proj))
                current_index_shift += 1
                break
            else:
                distance_left /= 2.0
                distance_right /= 2.0
    return result_list
