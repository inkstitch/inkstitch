from ..stitches import constants
from ..stitches import LineStringSampling
from shapely.geometry import  Point, MultiPoint
from shapely.geometry.polygon import LineString, LinearRing
from shapely.ops import nearest_points
import math

#Takes the current tree item and its rastered points (treenode.val and its origin treenode.pointsourcelist) and transfers it to parent and siblings.
# To do so it calculates the current normal and determines its intersection with the neighbors which gives the transferred points.
#Input:
#-treenode: Tree node whose coordinates stored in the attribute "val" shall be transferred to its parent and siblings.
#-used_offset: The used offset when the curves where offsetted
#-offset_by_half: True if the transferred points shall be interlaced with respect to the points in treenode.val
#-max_stitching_distance: The maximum allowed stitch distance between two points
#-transfer_to_siblings_childs: If a point is transferred to a sibling - shall the points also recursively be transferred to the siblings childs?
#-transfer_to_parent: Shall the points also be transferred to the parent (=True) or only to the siblings (=False)
#Output:
#-Fills the attribute "transferred_point_priority_deque" of the siblings and parent in the tree datastructure.  An item of the deque
#is setup as follows: (projected point on line, index of point_origin, id(treenode origin), LineStringSampling.PointSource), priority=distance along line)
#index of point_origin is the index of the point in the neighboring line
def transfer_inner_points_to_surrounding2(treenode, used_offset, offset_by_half, max_stitching_distance, transfer_to_siblings_childs=True, transfer_to_parent=True):
    # if(treenode.id == 'hole' and not LinearRing(treenode.val).is_ccw):
    #    print("Error in transfer!")
    # print("Hier in Transfer!")
    # checkTree(treenode)

    # Get a list of all possible adjacent nodes which will be considered for transferring the points of treenode:
    siblings_tuple = treenode.siblings
    # Take only siblings which have not rastered before
    neighbor_list = []
    siblings_list = []
    for sibling in siblings_tuple:
        if sibling.already_rastered == False:
            # sibling.to_transfer = []
            neighbor_list.append(sibling)
            siblings_list.append(sibling)

    # to_transfer_points_per_sibling = [[] for i in range(len(siblings_list))]
    to_transfer_points_per_sibling = {
        id(sibling): [] for sibling in siblings_list}

    # Take also the parend into account:
    if treenode.parent != None and transfer_to_parent:
        neighbor_list.append(treenode.parent)

    if not neighbor_list:
        return

    # if treenode.id == 'hole' and treenode.parent.id == 'node':
    #    print("HIER IB")

    # Go through all rastered points of treenode and check where they should be transferred to its neighbar
    # The source of each point is stored in treenode.pointsourcelist
    point_list = list(MultiPoint(treenode.val.coords))
    point_source_list = treenode.pointsourcelist.copy()
    assert(len(point_list) == len(point_source_list))

    # For a linear ring the last point is the same as the starting point which we delete
    # since we do not want to transfer the starting and end point twice
    closedLine = treenode.val
    if point_list[0].distance(point_list[-1]) < constants.point_spacing_to_be_considered_equal:
        point_list.pop()
        point_source_list.pop()
    else:
        # closed line is needed if we offset by half since we need to determine the line
        # length including the closing segment
        closedLine = LinearRing(treenode.val)

    bisectorline_length = abs(used_offset) * \
        constants.transfer_point_distance_factor
    linesign = treenode.stitching_direction
   # print(RenderTree(treenode))
   # if treenode.id == 'hole':
   #     linesign *= -1

    i = 0
    currentDistance = 0
    while i < len(point_list):
        #if abs(point_list[i].coords[0][0]-28.1) < 0.5 and abs(point_list[i].coords[0][1]-94.9) < 0.5:
        #    print("HIER gefunden!")
        #need_additional_nearest_neighbor = False

        point_source =  point_source_list[i] #LineStringSampling.PointSource.MUST_USE

        # We do not transfer points which were only characteristic ("fix") to the geometry of the source
        #if(offset_by_half and point_source_list[i] == LineStringSampling.PointSource.EDGE_NEEDED and
        #        point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.EDGE_NEEDED):
        #    point_source = LineStringSampling.PointSource.EDGE_RASTERING_ALLOWED
        
        if(offset_by_half and point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.EDGE_PREVIOUSLY_SHIFTED):
            point_source = LineStringSampling.PointSource.EDGE_PREVIOUSLY_SHIFTED
        #elif(point_source_list[i] == LineStringSampling.PointSource.EDGE_NEEDED):
        #    point_source = LineStringSampling.PointSource.NOT_NEEDED
        elif(point_source_list[i] == LineStringSampling.PointSource.ALREADY_TRANSFERRED):# or
             #point_source_list[i] == LineStringSampling.PointSource.NOT_NEEDED or
             #point_source_list[i] == LineStringSampling.PointSource.ADDITIONAL_TRACKING_POINT_NOT_NEEDED):
            currentDistance += point_list[i].distance(
                point_list[(i+1) % len(point_list)])
            i += 1
            continue

        # if(abs(point_list[i].coords[0][0]-134) < 0.5 and abs(point_list[i].coords[0][1]-75.5) < 0.5):
        #    print("HIERRR point")

        # We create a bisecting line through the current point
        normalized_vector_prev_x = (
            point_list[i].coords[0][0]-point_list[i-1].coords[0][0])  # makes use of closed shape
        normalized_vector_prev_y = (
            point_list[i].coords[0][1]-point_list[i-1].coords[0][1])
        prev_spacing = math.sqrt(normalized_vector_prev_x*normalized_vector_prev_x +
                                 normalized_vector_prev_y*normalized_vector_prev_y)
        normalized_vector_prev_x /= prev_spacing
        normalized_vector_prev_y /= prev_spacing

        normalized_vector_next_x = normalized_vector_next_y = 0
        next_spacing = 0
        while True:
            normalized_vector_next_x = (
                point_list[i].coords[0][0]-point_list[(i+1) % len(point_list)].coords[0][0])
            normalized_vector_next_y = (
                point_list[i].coords[0][1]-point_list[(i+1) % len(point_list)].coords[0][1])
            next_spacing = math.sqrt(normalized_vector_next_x*normalized_vector_next_x +
                                     normalized_vector_next_y*normalized_vector_next_y)
            if next_spacing < constants.line_lengh_seen_as_one_point:
                point_list.pop(i)
                point_source_list.pop(i)
                currentDistance += next_spacing
                continue
            normalized_vector_next_x /= next_spacing
            normalized_vector_next_y /= next_spacing
            break

        # We do not transfer points which were only characteristic ("fix") to the geometry of the source
        # Since offset_by_half depends also on the following point, we need to check this point, too
        #if((offset_by_half and point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.EDGE_NEEDED) and
        #        point_source_list[i] != LineStringSampling.PointSource.EDGE_NEEDED):
        #    point_source = LineStringSampling.PointSource.NOT_NEEDED
        if(offset_by_half and point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.ALREADY_TRANSFERRED):# or
             #offset_by_half and point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.NOT_NEEDED or
             #offset_by_half and point_source_list[(i+1) % len(point_list)] == LineStringSampling.PointSource.ADDITIONAL_TRACKING_POINT_NOT_NEEDED):
            i += 1
            currentDistance += next_spacing
            continue

        vecx = (normalized_vector_next_x+normalized_vector_prev_x)
        vecy = (normalized_vector_next_y+normalized_vector_prev_y)
        vec_length = math.sqrt(vecx*vecx+vecy*vecy)

        # The two sides are (anti)parallel - construct normal vector (bisector) manually:
        # If we offset by half we are offseting normal to the next segment
        if(vec_length < 1E-2 or offset_by_half):
            vecx = linesign*bisectorline_length*normalized_vector_next_y
            vecy = -linesign*bisectorline_length*normalized_vector_next_x
            #need_additional_nearest_neighbor = offset_by_half
        else:
            vecx *= bisectorline_length/vec_length
            vecy *= bisectorline_length/vec_length
            if (vecx*normalized_vector_next_y-vecy * normalized_vector_next_x)*linesign < 0:
                vecx = -vecx
                vecy = -vecy
            #need_additional_nearest_neighbor = True

        assert((vecx*normalized_vector_next_y-vecy *
               normalized_vector_next_x)*linesign >= 0)

        originPoint = point_list[i]
        if(offset_by_half):
            off = currentDistance+next_spacing/2
            # negative priority values start from end
            # if off < 0:
            #    off += treenode.val.length
            if off > closedLine.length:
                off -= closedLine.length
            originPoint = closedLine.interpolate(off)

        bisectorline = LineString([(originPoint.coords[0][0],
                                  originPoint.coords[0][1]),
                                   (originPoint.coords[0][0]+vecx,
                                  originPoint.coords[0][1]+vecy)])

        for neighbor in neighbor_list:
            result = bisectorline.intersection(neighbor.val)
            if not result.is_empty:
                desired_point = Point()
                if result.geom_type == 'Point':
                    desired_point = result
                else:
                    resultlist = list(result)
                    desired_point = resultlist[0]
                    if len(resultlist) > 1:
                        desired_point = nearest_points(
                            result, point_list[i])[0]

                priority = neighbor.val.project(desired_point)
                point = desired_point

                # if abs(point.coords[0][0]-9.4) < 0.2 and abs(point.coords[0][1]-13.3) < 0.2:
                #    print("HIIIIIIIIIIIERRR")

                # if abs(point.coords[0][0]-58) < 0.5 and abs(point.coords[0][1]-132) < 0.5:
                #    print("HIER gefunden!")
                # its a sibling - the transferred point to this sibling needs to be transferred to the siblings childs afterwards
                if transfer_to_siblings_childs and neighbor.parent == treenode.parent and point_source != LineStringSampling.PointSource.NOT_NEEDED:
                    to_transfer_points_per_sibling[id(neighbor)].append(point)
                    # neighbor.to_transfer.append(point)
                neighbor.transferred_point_priority_deque.insert(
                    (point, i, id(treenode), point_source), priority)  # We add also i as well as the source id as information which is helpful later to detect interrupted transferred points to the parent (e.g. because another sibling was closer)

            #if need_additional_nearest_neighbor:
                # if abs(point_list[i].coords[0][0]-10.4) < 0.2 and abs(point_list[i].coords[0][1]-14) < 0.2:
                #    print("HIIIIIIIIIIIERRR")
                #add_point = nearest_points(neighbor.val, point_list[i])[0]

                # if abs(add_point.coords[0][0]-9.4) < 0.2 and abs(add_point.coords[0][1]-13.3) < 0.2:
                #    print("HIIIIIIIIIIIERRR")

                #if add_point.distance(point_list[i]) < constants.offset_factor_for_adjacent_geometry*abs(used_offset):
                #    priority = neighbor.val.project(add_point)
                #    neighbor.transferred_point_priority_deque.insert(
                #        (add_point, i, id(treenode), LineStringSampling.PointSource.ADDITIONAL_TRACKING_POINT_NOT_NEEDED), priority)

        i += 1
        currentDistance += next_spacing

    assert(len(point_list) == len(point_source_list))

    if transfer_to_siblings_childs:
        # Transfer the points transferred to the siblings also to their childs
        for sibling in siblings_list:
            transfer_transferred_points_also_to_childs(
                sibling, used_offset, offset_by_half, max_stitching_distance, to_transfer_points_per_sibling[id(sibling)][::linesign])


#Takes the current tree item and its rastered points (to_transfer_points) and transfers these points to its childs
# To do so it calculates the current normal and determines its intersection with the childs which gives the transferred points.
#Input:
#-treenode: Tree node whose points stored in "to_transfer_points" shall be transferred to its childs.
#-used_offset: The used offset when the curves where offsetted
#-offset_by_half: True if the transferred points shall be interlaced with respect to the points in treenode.val
#-max_stitching_distance: The maximum allowed stitch distance between two points
#-to_transfer_points: List of points belonging to treenode which shall be transferred
#-recursive: Shall the points also recursively be transferred to the child childs?
#-to_transfer_points_origin: The origin tag of each point in to_transfer_points
#Output:
#-Fills the attribute "transferred_point_priority_deque" of the siblings and parent in the tree datastructure. An item of the deque
#is setup as follows: (projected point on line, index of point_origin, id(treenode origin), LineStringSampling.PointSource), priority=distance along line)
#index of point_origin is the index of the point in the neighboring line
def transfer_transferred_points_also_to_childs(treenode, used_offset, offset_by_half, max_stitching_distance, to_transfer_points, recursive=True, to_transfer_points_origin=[]):
   # checkTree(treenode)

    assert(len(to_transfer_points)==len(to_transfer_points_origin) or len(to_transfer_points_origin) == 0)

    if len(to_transfer_points) == 0:
        return

    # Get a list of all possible adjacent nodes which will be considered for transferring the points of treenode:
    childs_tuple = treenode.children
    # Take only siblings which have not rastered before
    child_list = []
    for child in childs_tuple:
        if child.already_rastered == False:
            # child.to_transfer = []
            child_list.append(child)

    to_transfer_points_per_child = [[] for i in range(len(child_list))]

    # Go through all rastered points of treenode and check where they should be transferred to its neighbar
    # The source of each point is stored in treenode.pointsourcelist
    point_list = list(MultiPoint(to_transfer_points))

    # For a linear ring the last point is the same as the starting point which we delete
    # since we do not want to transfer the starting and end point twice
    closedLine = treenode.val
    if point_list[0].distance(point_list[-1]) < constants.point_spacing_to_be_considered_equal:
        point_list.pop()
        if(to_transfer_points_origin):
            to_transfer_points_origin.pop()
        if len(point_list) == 0:
            return
    else:
        # closed line is needed if we offset by half since we need to determine the line
        # length including the closing segment
        closedLine = LinearRing(treenode.val)

    bisectorline_length = abs(used_offset) * \
        constants.transfer_point_distance_factor
   # if hasattr(treenode, 'stitching_direction'):
   #     linesign = -treenode.stitching_direction
  #  else:
    linesign = math.copysign(1, used_offset)
   # print(RenderTree(treenode))
   # if treenode.id == 'hole':
   #     linesign *= -1

    i = 0
    while i < len(point_list):
        currentDistance = closedLine.project(point_list[i])

#        if abs(point_list[i].coords[0][0]-28.1) < 0.2 and abs(point_list[i].coords[0][1]-94.9) < 0.2:
#            print("HIIIIIIIIIIIERRR")

#        if abs(point_list[i].coords[0][0]-24) < 0.2 and abs(point_list[i].coords[0][1]-97.1) < 0.2:
#            print("HIIIIIIIIIIIERRR")

#        if abs(point_list[i].coords[0][0]-20) < 0.2 and abs(point_list[i].coords[0][1]-99.8) < 0.2:
#            print("HIIIIIIIIIIIERRR")

        # We create a bisecting line through the current point
        normalized_vector_prev_x = (
            point_list[i].coords[0][0]-point_list[i-1].coords[0][0])  # makes use of closed shape
        normalized_vector_prev_y = (
            point_list[i].coords[0][1]-point_list[i-1].coords[0][1])
        prev_spacing = math.sqrt(normalized_vector_prev_x*normalized_vector_prev_x +
                                 normalized_vector_prev_y*normalized_vector_prev_y)

        # If spacing is too large we interpolate for a better bisecting line
        if(prev_spacing-constants.line_lengh_seen_as_one_point > max_stitching_distance):
            prev_spacing = min(max_stitching_distance, closedLine.length/10.0)
            prev_point_distance = currentDistance-prev_spacing
            if currentDistance < prev_spacing:
                prev_point_distance += closedLine.length  # makes use of closed shape
            prev_point = closedLine.interpolate(prev_point_distance)

            normalized_vector_prev_x = (
                point_list[i].coords[0][0]-prev_point.coords[0][0])
            normalized_vector_prev_y = (
                point_list[i].coords[0][1]-prev_point.coords[0][1])

        normalized_vector_prev_x /= prev_spacing
        normalized_vector_prev_y /= prev_spacing

        normalized_vector_next_x = normalized_vector_next_y = 0
        next_spacing = 0
        while True:
            normalized_vector_next_x = (
                point_list[i].coords[0][0]-point_list[(i+1) % len(point_list)].coords[0][0])
            normalized_vector_next_y = (
                point_list[i].coords[0][1]-point_list[(i+1) % len(point_list)].coords[0][1])
            next_spacing = math.sqrt(normalized_vector_next_x*normalized_vector_next_x +
                                     normalized_vector_next_y*normalized_vector_next_y)
            if next_spacing < constants.line_lengh_seen_as_one_point:
                point_list.pop(i)
                if(to_transfer_points_origin):
                    to_transfer_points_origin.pop(i)
                continue

            # If spacing is too large we interpolate for a better bisecting line
            if(next_spacing-constants.line_lengh_seen_as_one_point > max_stitching_distance):
                next_spacing = min(max_stitching_distance,
                                   closedLine.length/10.0)
                next_point_distance = currentDistance+next_spacing
                if next_point_distance > closedLine.length:
                    next_point_distance -= closedLine.length  # makes use of closed shape
                next_point = closedLine.interpolate(next_point_distance)

                normalized_vector_next_x = (
                    point_list[i].coords[0][0]-next_point.coords[0][0])
                normalized_vector_next_y = (
                    point_list[i].coords[0][1]-next_point.coords[0][1])

            normalized_vector_next_x /= next_spacing
            normalized_vector_next_y /= next_spacing
            break

        vecx = (normalized_vector_next_x+normalized_vector_prev_x)
        vecy = (normalized_vector_next_y+normalized_vector_prev_y)
        vec_length = math.sqrt(vecx*vecx+vecy*vecy)

        # The two sides are (anti)parallel - construct normal vector (bisector) manually:
        # If we offset by half we are offseting normal to the next segment
        if(vec_length < constants.line_lengh_seen_as_one_point or offset_by_half):
            vecx = linesign*bisectorline_length*normalized_vector_next_y
            vecy = -linesign*bisectorline_length*normalized_vector_next_x
        else:
            vecx *= bisectorline_length/vec_length
            vecy *= bisectorline_length/vec_length
            if (vecx*normalized_vector_next_y-vecy * normalized_vector_next_x)*linesign < 0:
                vecx = -vecx
                vecy = -vecy

        assert((vecx*normalized_vector_next_y-vecy *
               normalized_vector_next_x)*linesign >= 0)

        originPoint = point_list[i]
        if(offset_by_half):
            off = currentDistance+next_spacing/2
            # negative priority values start from end
            # if off < 0:
            #    off += treenode.val.length
            if off > closedLine.length:
                off -= closedLine.length
            originPoint = closedLine.interpolate(off)

        bisectorline = LineString([(originPoint.coords[0][0],
                                  originPoint.coords[0][1]),
                                   (originPoint.coords[0][0]+vecx,
                                  originPoint.coords[0][1]+vecy)])

        for child, transfer_point_list_child in zip(child_list, to_transfer_points_per_child):
            result = bisectorline.intersection(child.val)
            if result.is_empty:
                continue
            desired_point = Point()
            if result.geom_type == 'Point':
                desired_point = result
            elif result.geom_type == 'LineString':
                desired_point = Point(result.coords[0])
            else:
                resultlist = list(result)
                desired_point = resultlist[0]
                if len(resultlist) > 1:
                    desired_point = nearest_points(result, point_list[i])[0]

            priority = child.val.project(desired_point)
            point = desired_point


            #if abs(point.coords[0][0]-55.70833790329981) < 0.5 and abs(point.coords[0][1]-42.41749061817239) < 0.5:
            #    print("HIER gefunden!")
            if(recursive):
                transfer_point_list_child.append(point)
            if(to_transfer_points_origin):
                if offset_by_half and to_transfer_points_origin[(i+1)%len(to_transfer_points_origin)] == LineStringSampling.PointSource.EDGE_PREVIOUSLY_SHIFTED:
                    child.transferred_point_priority_deque.insert(
                        (point, i, id(treenode),  LineStringSampling.PointSource.EDGE_PREVIOUSLY_SHIFTED), priority)  # We add also i as well as the source id as information which is helpful later to detect interrupted transferred points to the parent (e.g. because another sibling was closer)
                else:
                   child.transferred_point_priority_deque.insert(
                        (point, i, id(treenode), to_transfer_points_origin[i]), priority)  # We add also i as well as the source id as information which is helpful later to detect interrupted transferred points to the parent (e.g. because another sibling was closer) 
            else:
                child.transferred_point_priority_deque.insert(
                    (point, i, id(treenode), LineStringSampling.PointSource.ALREADY_TRANSFERRED), priority)  # We add also i as well as the source id as information which is helpful later to detect interrupted transferred points to the parent (e.g. because another sibling was closer)
                
        i += 1

    if(recursive):
        for child, transfer_point_list_child in zip(child_list, to_transfer_points_per_child):
            transfer_transferred_points_also_to_childs(
                child, used_offset, offset_by_half, max_stitching_distance, transfer_point_list_child)

    assert(len(point_list)==len(to_transfer_points_origin) or len(to_transfer_points_origin) == 0)
