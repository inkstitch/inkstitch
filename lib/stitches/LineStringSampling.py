#from sys import path
#from typing import NoReturn
#import matplotlib.pyplot as plt
from shapely.geometry.polygon import LineString
from shapely.geometry import Point
from shapely.ops import substring
import math
import numpy as np
from depq import DEPQ
from enum import IntEnum
from ..stitches import constants

#Used to tag the origin of a rastered point
class PointSource(IntEnum):
    #MUST_USE = 0  # Legacy
    REGULAR_SPACING = 1  # introduced to not exceed maximal stichting distance
    INITIAL_RASTERING = 2  # No transferred points for this segment were available
    EDGE_NEEDED = 3 # point which must be stitched to avoid to large deviations to the desired path (relevant for interlaced mode)
    #NOT_NEEDED = 4 #Legacy
    ALREADY_TRANSFERRED = 5 #The point transfer can be done recursively down to all sub-childs. 
    #These points are tagged as ALREADY_TRANSFERRED to avoid that they are transferred again to all sub-childs if the next child in the order is rastered.
    
    #ADDITIONAL_TRACKING_POINT_NOT_NEEDED = 6 #Legacy
    #EDGE_RASTERING_ALLOWED = 7 #Legacy
    EDGE_PREVIOUSLY_SHIFTED=8 #If an edge_needed was previously shifted the next edge (childs edge) should not be shifted in interlaced mode

# Calculates the angles between adjacent edges at each interior point
#Note that the resulting list has a lenght = len(line)-2 since for the boundary points no angle calculations were possible
def calculate_line_angles(line):
    Angles = np.zeros(len(line.coords))
    for i in range(1, len(line.coords)-1):
        vec1 = np.array(line.coords[i])-np.array(line.coords[i-1])
        vec2 = np.array(line.coords[i])-np.array(line.coords[i+1])
        vec1length = np.linalg.norm(vec1)
        vec2length = np.linalg.norm(vec2)
        Angles[i] = math.acos(np.dot(vec1, vec2)/(vec1length*vec2length))
    return Angles


#Takes all points within "line" and adds additional points if the spacing between two points in line exceeds maxstitchdistance
#Output:
#-List of tuples with the rastered point coordinates
#-List which defines the point origin for each point according to the PointSource enum.
def rasterLineString2(line, maxstitchdistance):
    if line.length < constants.line_lengh_seen_as_one_point:
        return [line.coords[0]], [PointSource.EDGE_NEEDED]
   
    returnpointlist = []
    returnpointsourcelist = []
    overall_distance = 0
    skipped_segment_length = 0
    skipped_segment_start_index = -1

    for i in range(len(line.coords)-1):
        startindex = i
        segmentlength = math.sqrt(pow(
            line.coords[startindex][0]-line.coords[startindex+1][0], 2)+pow(line.coords[startindex][1]-line.coords[startindex+1][1], 2))

        if segmentlength < constants.line_lengh_seen_as_one_point:
            overall_distance += segmentlength
            if skipped_segment_length == 0:
                skipped_segment_start_index = i
                skipped_segment_length = segmentlength
                continue
            else:
                skipped_segment_length += segmentlength
                if skipped_segment_length < constants.line_lengh_seen_as_one_point:
                    continue
                else:
                    startindex = skipped_segment_start_index
                    segmentlength = skipped_segment_length
                    skipped_segment_length = 0
        else:
            skipped_segment_length = 0
            # we subtract "eps=constants.line_lengh_seen_as_one_point" to account for numerical inaccuracies -
            # e.g. segment_length = 2*maxstitchdistance would otherwise sometimes cause 1 and sometimes cause 2 subpoints
        numberofsubpoints = math.ceil(
            (segmentlength-constants.line_lengh_seen_as_one_point)/maxstitchdistance)-1
        subsegmentlength = segmentlength/(numberofsubpoints+1)
        returnpointlist.append((line.coords[startindex]))
        returnpointsourcelist.append(PointSource.INITIAL_RASTERING)
        #if abs(returnpointlist[-1][0]-29)< 0.2 and abs(returnpointlist[-1][1]-11)<0.2:
        #    print("Initial Rastering gefunden!")
        for j in range(1, numberofsubpoints+1):
            returnpointlist.append(
                (line.interpolate(overall_distance+j*subsegmentlength).coords[0]))
            #if abs(returnpointlist[-1][0]-29)< 0.2 and abs(returnpointlist[-1][1]-11)<0.2:
            #    print("Initial Rastering gefunden!")
            returnpointsourcelist.append(PointSource.INITIAL_RASTERING)
        overall_distance = overall_distance+segmentlength
    return returnpointlist, returnpointsourcelist


#Checks whether an edge (unshifted point) can be replaced by shifted_point without have too strong deviations of unshifted_point to the resulting line segment.
#line contains both points (unshifted_point and shifted_point)
#The threshold whether the shift is allowed is a comparison of the resulting distance and a factor times absoffset
#To create a line segment to which unshifted_point is compared we need one point left (e.g. shifted_point) and one point right to unshifted point on the line "line"-
#This second point to the right is calculated by traveling the same spacing between unshifted_point and shifted_point in the opposite direction. This traveling distance is cropped by "maxdelta_next_point"
#Output:
#-True or false whether the shift of the edge is allowed (not a too large deviation)
def check_edge_needed_shift_allowed(line, unshifted_point, shifted_point, absoffset, maxdelta_next_point):
    #assert(abs(line.coords[0][0]-line.coords[-1][0])<constants.eps and abs(line.coords[0][1]-line.coords[-1][1])<constants.eps)
    proj1 = line.project(unshifted_point)
    proj2 = line.project(shifted_point)
    delta = proj2-proj1
    if maxdelta_next_point != -1:
        delta = math.copysign(min(abs(delta), maxdelta_next_point),delta)
    newproj = proj1-delta
    if newproj < 0:
        #newproj+=line.length
        return False
    if newproj > line.length:
        #newproj-=line.length
        return False
    thirdPoint = line.interpolate(newproj)
    bisection = LineString([shifted_point, thirdPoint])
    distance = bisection.distance(unshifted_point)

    return (distance<=constants.fac_offset_edge_shift*absoffset)

#Rasters a line between start_distance and end_distance.
#Input:
#-line: The line to be rastered
#-start_distance: The distance along the line from which the rastering should start
#-end_distance: The distance along the line until which the rastering should be done
#-maxstitchdistance: The maximum allowed stitch distance
#-stitching_direction: =1 is stitched along line direction, =-1 if stitched in reversed order. Note that
# start_distance > end_distance for stitching_direction = -1
#-must_use_points_deque: deque with projected points on line from its neighbors. An item of the deque
#is setup as follows: (projected point on line, index of point_origin, id(treenode origin), LineStringSampling.PointSource), priority=distance along line)
#index of point_origin is the index of the point in the neighboring line
#-absoffset: used offset between to offsetted curves
#Output:
#-List of tuples with the rastered point coordinates
#-List which defines the point origin for each point according to the PointSource enum.
def rasterLineString2_Priority2(line, start_distance, end_distance, maxstitchdistance, stitching_direction, must_use_points_deque, absoffset):
    if (abs(end_distance-start_distance) < constants.line_lengh_seen_as_one_point):
        return [line.interpolate(start_distance).coords[0]], [PointSource.EDGE_NEEDED]

    assert (stitching_direction == -1 and start_distance >= end_distance) or (
        stitching_direction == 1 and start_distance <= end_distance)
   
    deque_points = list(must_use_points_deque)

    if len(deque_points) == 0:
        return rasterLineString2(substring(line, start_distance, end_distance), maxstitchdistance)

    linecoords = line.coords
    # for item in linecoords:
    #    if abs(item[0]-135) < 0.5 and abs(item[1]-16) < 0.5:
    #        print("GEFUNDEN!")

    if start_distance > end_distance:
        start_distance, end_distance = line.length - \
            start_distance, line.length-end_distance
        linecoords = linecoords[::-1]
        for i in range(len(deque_points)):
            deque_points[i] = (deque_points[i][0],
                               line.length-deque_points[i][1])
    else:
        deque_points = deque_points[::-1]

    # Remove all points from the "must use point list" which do not fall in the segment [start_distance; end_distance]
    while (len(deque_points) > 0 and deque_points[0][1] <= start_distance+min(maxstitchdistance/20, constants.point_spacing_to_be_considered_equal)):
        deque_points.pop(0)
    while (len(deque_points) > 0 and deque_points[-1][1] >= end_distance-min(maxstitchdistance/20, constants.point_spacing_to_be_considered_equal)):
        deque_points.pop()

    if len(deque_points) == 0:
        return rasterLineString2(substring(line, start_distance, end_distance), maxstitchdistance)

# Ordering in priority queue:
#   (point, i, id(treenode), LineStringSampling.PointSource), priority)

    returnpointlist = []
    returnpointsourcelist = []

    path_coords = substring(LineString(linecoords),
                            start_distance, end_distance)
    Angles = calculate_line_angles(path_coords)

    limiting_angle = math.pi*177.5/180.0

    j = 0
    i = 1
    k1 = 0
    k2 = 0
    startpoint_proj = 0

    startpoint = path_coords.coords[j]
    startpoint_source = PointSource.EDGE_NEEDED

    returnpointsourcelist.append(startpoint_source)
    returnpointlist.append(startpoint)
    #if (abs(returnpointlist[-1][0]-13.2)< 0.2 and abs(returnpointlist[-1][1]-141.4)<0.2):
    #            print("HIIER FOUNDED1")  

    last_shifted_edge_points = [None, None]

    while i < len(Angles):
        while i < len(Angles)-1 and Angles[i] >= limiting_angle:
            i += 1
        while k1 < len(deque_points) and deque_points[k1][1]-start_distance < startpoint_proj:
            k1 += 1

        #Get final index:
        k2 = k1
        end_point_proj = path_coords.project(Point(path_coords.coords[i]))
        while k2 < len(deque_points) and deque_points[k2][1]-start_distance < end_point_proj:
            k2 += 1    
        k3 = k2-1

        if (abs(path_coords.coords[i][0]-38.6)< 0.2 and abs(path_coords.coords[i][1]-131.0)<0.2):
            print("HIIER FOUNDED1")  

        found_EDGE_Needed_and_not_edge_shifted = False
        found_index = -1
        
        if not(k2 < len(deque_points) and deque_points[k2][1]-start_distance <= end_point_proj+absoffset and deque_points[k2][0][3] == PointSource.EDGE_PREVIOUSLY_SHIFTED):
            while k3 > 0 and deque_points[k3][1]-start_distance >= max(startpoint_proj,end_point_proj- maxstitchdistance/2.0)  and k2-k3 < 4: #look max 3 points ahead
                if deque_points[k3][0][3] == PointSource.EDGE_PREVIOUSLY_SHIFTED:
                    found_EDGE_Needed_and_not_edge_shifted = False
                    break
                elif not found_EDGE_Needed_and_not_edge_shifted and (deque_points[k3][0][3] == PointSource.EDGE_NEEDED or deque_points[k3][0][3] == PointSource.INITIAL_RASTERING):
                    found_index = k3
                    found_EDGE_Needed_and_not_edge_shifted = True
                k3 -= 1

        endpoint = path_coords.coords[i]
        endpoint_source = PointSource.EDGE_NEEDED

        if  found_EDGE_Needed_and_not_edge_shifted:
            if i < len(path_coords.coords)-1:
                found_EDGE_Needed_and_not_edge_shifted = check_edge_needed_shift_allowed(path_coords,Point(endpoint), Point(deque_points[found_index][0][0].coords[0]),absoffset, Point(endpoint).distance(Point(path_coords.coords[i+1])))
            else:
                found_EDGE_Needed_and_not_edge_shifted = check_edge_needed_shift_allowed(path_coords,Point(endpoint), Point(deque_points[found_index][0][0].coords[0]),absoffset, -1)
            if found_EDGE_Needed_and_not_edge_shifted:
                #if (abs( deque_points[found_index][0][0].coords[0][0]-90.0)< 0.2 and abs( deque_points[found_index][0][0].coords[0][1]-174.5)<0.2):
                #    print("HIIER FOUNDED1")
                #if(deque_points[found_index][0][0].distance(Point(startpoint)) > constants.fact_offset_edge_shift_remaining_line_length*absoffset):
                last_shifted_edge_points.pop(0)
                last_shifted_edge_points.append(Point(endpoint))      
                endpoint =  deque_points[found_index][0][0].coords[0]
                end_point_proj = path_coords.project(Point(endpoint))
                endpoint_source = PointSource.EDGE_PREVIOUSLY_SHIFTED

       
        proj_list = []
        while k1 < len(deque_points) and deque_points[k1][1]-start_distance < end_point_proj:
            # TODO maybe take not all points (e.g. EDGE NEEDED)
            if deque_points[k1][0][3] != PointSource.EDGE_PREVIOUSLY_SHIFTED:
                proj_list.append(
                    deque_points[k1][1]-startpoint_proj-start_distance)
            k1 += 1



        distributed_proj_list = distribute_points_proj2(
            Point(startpoint), Point(endpoint), proj_list, maxstitchdistance)

        if returnpointsourcelist[-1] == PointSource.EDGE_PREVIOUSLY_SHIFTED and distributed_proj_list:
            last_shifted_edge_point = last_shifted_edge_points[0] #assumed endpoint_source == PointSource.EDGE_PREVIOUSLY_SHIFTED, so last_shifted_edge_points[1] contains the end-edge_point of this segment
            if endpoint_source != PointSource.EDGE_PREVIOUSLY_SHIFTED:
                last_shifted_edge_point = last_shifted_edge_points[1]
            next_point = path_coords.interpolate(distributed_proj_list[0]+startpoint_proj)
            bisectorline = LineString([next_point, Point(returnpointlist[-1])])
            distance = bisectorline.distance(last_shifted_edge_point)
            if distance > constants.fac_offset_edge_shift*absoffset:
                if len(returnpointlist) > 1 and last_shifted_edge_point.distance(Point(returnpointlist[-2])) > maxstitchdistance :
                    returnpointlist.append(last_shifted_edge_point.coords[0])
                    returnpointsourcelist.append(PointSource.EDGE_NEEDED)
                else:
                    returnpointlist.pop()
                    returnpointsourcelist.pop()
                    returnpointlist.append(last_shifted_edge_point.coords[0])
                    returnpointsourcelist.append(PointSource.EDGE_NEEDED)
                
        for item in distributed_proj_list:
            returnpointlist.append(path_coords.interpolate(
                item+startpoint_proj).coords[0])
            #if (abs(returnpointlist[-1][0]-34)< 0.2 and abs(returnpointlist[-1][1]-165.6)<0.2):
            #    print("HIIER FOUNDED1")    
            returnpointsourcelist.append(PointSource.REGULAR_SPACING)
        
        if (Point(endpoint).distance(Point(returnpointlist[-1])) > absoffset*constants.factor_offset_remove_points 
                    or endpoint_source == PointSource.EDGE_PREVIOUSLY_SHIFTED): #The "or endpoint_source == PointSource.EDGE_PREVIOUSLY_SHIFTED" is necessary since shifting can bring points very close together 
                                                                                #and if we do not add it here we do not know that the previous point was shifted in the next round
            returnpointlist.append(endpoint)
            returnpointsourcelist.append(endpoint_source)
        startpoint_proj = end_point_proj
        startpoint = endpoint
        j = i
        i += 1
        #if (abs(returnpointlist[-1][0]-10)< 0.2 and abs(returnpointlist[-1][1]-143.8)<0.2):
        #    print("HIIER FOUNDED1")  


    # TODO: Check whether the angle splitting was too lax so that we might need to add further EDGE_NEEDED afterwards to minimize the deviation to the original path

    assert(len(returnpointlist) == len(returnpointsourcelist))

    return returnpointlist, returnpointsourcelist


#Returns the index in arr whose value is closest to target
def get_closest_value_index(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # edge case - last or above all
    if target >= arr[n - 1]:
        return arr[n - 1], n-1
    # edge case - first or below all
    if target <= arr[0]:
        return arr[0], 0
    # BSearch solution: Time & Space: Log(N)

    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid], mid

    if target < arr[mid]:
        if target - arr[mid-1] >= arr[mid] - target:
            return arr[mid], mid
        else:
            return arr[mid-1], mid-1
        # return find_closest(arr[mid - 1], arr[mid], target)
    else:
        if target - arr[mid] >= arr[mid+1] - target:
            return arr[mid+1], mid+1
        else:
            return arr[mid], mid
        # return find_closest(arr[mid], arr[mid + 1], target)



# findClosest
# We find the closest by taking the difference
# between the target and both values. It assumes
# that val2 is greater than val1 and target lies
# between these two.
def find_closest(val1, val2, target):
    return val2 if target - val1 >= val2 - target else val1


#Tries to optimally distribute the points between start_point and end_point 
# - thereby considering projected points on this linesegment (transferPointList_proj) and
# - the maximum allowed stitch distance (maxStitchdistance)
#Output:
#-List of the distance of the calculated, distributed points with respect to the start_point (projection on the linesegment)
def distribute_points_proj2(start_point, end_point, transferPointList_proj, maxStitchdistance):

   # if abs(end_point.coords[0][0]-58.4) < 0.2 and abs(end_point.coords[0][1]-45.5)< 0.2:
   #     print("GEFUNDEN")

    L = start_point.distance(end_point)

    min_number_of_points_in_between = math.floor(L/maxStitchdistance)

    #We remove transfer points which are very close at the boundary since they sometimes are projection artifacts and 
    #should not influence the decisions below with len(transferPointList_proj) == 0, 1 or 2
    limit3_fac = 0.1
    while len(transferPointList_proj) > 0 and transferPointList_proj[0] <= limit3_fac*min(L,maxStitchdistance):
        transferPointList_proj.pop(0)

    while len(transferPointList_proj) > 0 and L-transferPointList_proj[-1] <= limit3_fac*min(L,maxStitchdistance):
        transferPointList_proj.pop()

    if len(transferPointList_proj) == 0:
        resultlist = []
        delta_step = L/(min_number_of_points_in_between+1)
        for j in range(1, min_number_of_points_in_between+1):
            resultlist.append(delta_step*j)
        return resultlist

    limit1 = 0.5*maxStitchdistance
    limit2_fac = 0.25

    if L <= limit1:
        return []

    limit_assymetric_fac = 0.25

    if len(transferPointList_proj) == 1 and min_number_of_points_in_between <= 1:
        if L <= maxStitchdistance and abs((L/2)-transferPointList_proj[0]) > limit_assymetric_fac*L:
            return []
        else:
            return transferPointList_proj

    if len(transferPointList_proj) == 2 and L <= maxStitchdistance:
        return []

    # if min_number_of_points_in_between == 0 and len(transferPointList_proj) != 1:
    #    return []
    # elif min_number_of_points_in_between == 0:
    #    return transferPointList_proj

    val, index = get_closest_value_index(transferPointList_proj, L/2)
    #point = LineString([start_point, end_point]).interpolate(val)

    delta = 0
    if index == len(transferPointList_proj)-1:
        delta = val-transferPointList_proj[index-1]
    elif index == 0:
        delta = transferPointList_proj[index+1]-val
    else:
        delta = max(
            val-transferPointList_proj[index-1],  transferPointList_proj[index+1]-val)

    if delta < constants.point_spacing_to_be_considered_equal:
        delta = maxStitchdistance

    number_of_points_with_delta = 1+math.floor((val-limit2_fac*delta)/delta)+math.floor((L-val-limit2_fac*delta)/delta)

    if number_of_points_with_delta %2 != 0:#len(transferPointList_proj) % 2 != 0:
        if delta < limit1:
            i = 2
            while(delta*i < limit1):
                i += 1
            delta *= i

        if delta > maxStitchdistance:
            i = 2
            while(delta/i > maxStitchdistance):
                i += 1
            delta /= i

    #residuum_left = val % delta
    #residuum_right = (L-val) % delta
    #NLeft = math.floor(val/delta)
    #NRight = math.floor((L-val)/delta)

    delta_left = delta_right = delta
    #delta_new_left = delta_new_right = delta
    #if residuum_left <= delta/2.0 and NLeft != 0:
    #        delta_new_left = min(maxStitchdistance, val/NLeft)
    #elif residuum_left > delta/2.0:
    #        delta_new_left = min(maxStitchdistance, val/(NLeft+1))

    #if residuum_right <= delta/2.0 and NRight != 0:
    #        delta_new_right = min(maxStitchdistance,(L-val)/NRight)
    #elif residuum_right > delta/2.0:
    #        delta_new_right = min(maxStitchdistance,(L-val)/(NRight+1))

    #mixing_factor_left = 1.0-math.exp(-30*(residuum_left-delta/2.0)**2/delta**2)
    #mixing_factor_right = 1.0-math.exp(-30*(residuum_right-delta/2.0)**2/delta**2)
            
    #delta_left = mixing_factor_left*delta_new_left+(1.0-mixing_factor_left)*delta
    #delta_right = mixing_factor_right*delta_new_right+(1.0-mixing_factor_right)*delta   

    returnlist = [val]

    current_val = val-delta_left
    while current_val > 0:
        if current_val < limit2_fac*delta_left and (delta_left+current_val) <= maxStitchdistance:
            break
        returnlist.insert(0, current_val)
        current_val -= delta_left

    current_val = val+delta_right
    while current_val < L:
        if (L-current_val) < limit2_fac*delta_right and (delta_right+L-current_val) <= maxStitchdistance:
            break
        returnlist.append(current_val)
        current_val += delta_right

    return returnlist
