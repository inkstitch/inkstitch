from shapely.geometry.polygon import LinearRing, LineString
from shapely.geometry import Polygon, MultiLineString
from shapely.ops import  polygonize
from shapely.geometry import MultiPolygon
from anytree import AnyNode, PreOrderIter
from shapely.geometry.polygon import orient
from depq import DEPQ
from enum import IntEnum
from ..stitches import ConnectAndSamplePattern
from ..stitches import constants



# Problem: When shapely offsets a LinearRing the start/end point might be handled wrongly since they are only treated as LineString.
# (See e.g. https://i.stack.imgur.com/vVh56.png as a problematic example)
# This method checks first whether the start/end point form a problematic edge with respect to the offset side. If it is not a problematic
# edge we can use the normal offset_routine. Otherwise we need to perform two offsets:
# -offset the ring
# -offset the start/end point + its two neighbors left and right
# Finally both offsets are merged together to get the correct offset of a LinearRing
def offset_linear_ring(ring, offset, side, resolution, join_style, mitre_limit):
    coords = ring.coords[:]
    # check whether edge at index 0 is concave or convex. Only for concave edges we need to spend additional effort
    dx_seg1 = dy_seg1 = 0
    if coords[0] != coords[-1]:
        dx_seg1 = coords[0][0]-coords[-1][0]
        dy_seg1 = coords[0][1]-coords[-1][1]
    else:
        dx_seg1 = coords[0][0]-coords[-2][0]
        dy_seg1 = coords[0][1]-coords[-2][1]
    dx_seg2 = coords[1][0]-coords[0][0]
    dy_seg2 = coords[1][1]-coords[0][1]
    # use cross product:
    crossvalue = dx_seg1*dy_seg2-dy_seg1*dx_seg2
    sidesign = 1
    if side == 'left':
        sidesign = -1

    # We do not need to take care of the joint n-0 since we offset along a concave edge:
    if sidesign*offset*crossvalue <= 0:
        return ring.parallel_offset(offset, side, resolution, join_style, mitre_limit)

    # We offset along a convex edge so we offset the joint n-0 separately:
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    offset_ring1 = ring.parallel_offset(
        offset, side, resolution, join_style, mitre_limit)
    offset_ring2 = LineString((coords[-2], coords[0], coords[1])).parallel_offset(
        offset, side, resolution, join_style, mitre_limit)

    # Next we need to merge the results:
    if offset_ring1.geom_type == 'LineString':
        return LinearRing(offset_ring2.coords[:]+offset_ring1.coords[1:-1])
    else:
        # We have more than one resulting LineString for offset of the geometry (ring) = offset_ring1.
        # Hence we need to find the LineString which belongs to the offset of element 0 in coords =offset_ring2
        # in order to add offset_ring2 geometry to it:
        result_list = []
        thresh = constants.offset_factor_for_adjacent_geometry*abs(offset)
        for offsets in offset_ring1:
            if(abs(offsets.coords[0][0]-coords[0][0]) < thresh and abs(offsets.coords[0][1]-coords[0][1]) < thresh):
                result_list.append(LinearRing(
                    offset_ring2.coords[:]+offsets.coords[1:-1]))
            else:
                result_list.append(LinearRing(offsets))
        return MultiLineString(result_list)


# Removes all geometries which do not form a "valid" LinearRing (meaning a ring which does not form a straight line)
def take_only_valid_linear_rings(rings):
    if(rings.geom_type == 'MultiLineString'):
        new_list = []
        for ring in rings:
            if len(ring.coords) > 3 or (len(ring.coords) == 3 and ring.coords[0] != ring.coords[-1]):
                new_list.append(ring)
        if len(new_list) == 1:
            return LinearRing(new_list[0])
        else:
            return MultiLineString(new_list)
    else:
        if len(rings.coords) <= 2:
            return LinearRing()
        elif len(rings.coords) == 3 and rings.coords[0] == rings.coords[-1]:
            return LinearRing()
        else:
            return rings


#Since naturally holes have the opposite point ordering than non-holes we make 
#all lines within the tree "root" uniform (having all the same ordering direction)
def make_tree_uniform_ccw(root):
    for node in PreOrderIter(root):
        if(node.id == 'hole'):
            node.val.coords = list(node.val.coords)[::-1]


#Used to define which stitching strategy shall be used
class StitchingStrategy(IntEnum):
    CLOSEST_POINT = 0
    INNER_TO_OUTER = 1

# Takes a polygon (which can have holes) as input and creates offsetted versions until the polygon is filled with these smaller offsets.
# These created geometries are afterwards connected to each other and resampled with a maximum stitch_distance.
# The return value is a LineString which should cover the full polygon.
#Input:
#-poly: The shapely polygon which can have holes
#-offset: The used offset for the curves
#-join_style: Join style for the offset - can be round, mitered or bevel (https://shapely.readthedocs.io/en/stable/manual.html#shapely.geometry.JOIN_STYLE)
#For examples look at https://shapely.readthedocs.io/en/stable/_images/parallel_offset.png
#-stitch_distance maximum allowed stitch distance between two points
#-offset_by_half: True if the points shall be interlaced
#-strategy: According to StitchingStrategy you can select between different strategies for the connection between parent and childs
#Output:
#-List of point coordinate tuples
#-Tag (origin) of each point to analyze why a point was placed at this position
def offset_poly(poly, offset, join_style, stitch_distance, offset_by_half, strategy, starting_point):
    ordered_poly = orient(poly, -1)
    ordered_poly = ordered_poly.simplify(
        constants.simplification_threshold, False)
    root = AnyNode(id="node", val=ordered_poly.exterior, already_rastered=False, transferred_point_priority_deque=DEPQ(
        iterable=None, maxlen=None))
    active_polys = [root]
    active_holes = [[]]

    for holes in ordered_poly.interiors:
        #print("hole: - is ccw: ", LinearRing(holes).is_ccw)
        active_holes[0].append(
            AnyNode(id="hole", val=holes, already_rastered=False, transferred_point_priority_deque=DEPQ(
                iterable=None, maxlen=None)))

    # counter = 0
    while len(active_polys) > 0:  # and counter < 20:
        # counter += 1
        # print("New iter")
        current_poly = active_polys.pop()
        current_holes = active_holes.pop()
        poly_inners = []

        # outer = current_poly.val.parallel_offset(offset,'left', 5, join_style, 10)
        outer = offset_linear_ring(current_poly.val, offset, 'left', 5, join_style, 10)
        outer = outer.simplify(constants.simplification_threshold, False)
        outer = take_only_valid_linear_rings(outer)

        for j in range(len(current_holes)):
            # inner = closeLinearRing(current_holes[j].val,offset/2.0).parallel_offset(offset,'left', 5, join_style, 10)
            inner = offset_linear_ring(
                current_holes[j].val, offset, 'left', 5, join_style, 10)
            inner = inner.simplify(constants.simplification_threshold, False)
            inner = take_only_valid_linear_rings(inner)
            if not inner.is_empty:
                poly_inners.append(Polygon(inner))
        if not outer.is_empty:
            if len(poly_inners) == 0:
                if outer.geom_type == 'LineString':
                    result = Polygon(outer)
                else:
                    result = MultiPolygon(polygonize(outer))
            else:
                if outer.geom_type == 'LineString':
                    result = Polygon(outer).difference(
                        MultiPolygon(poly_inners))
                else:
                    result = MultiPolygon(outer).difference(
                        MultiPolygon(poly_inners))

            if not result.is_empty and result.area > offset*offset/10:
                result_list = []
                if result.geom_type == 'Polygon':
                    result_list = [result]
                else:
                    result_list = list(result)
                # print("New result_list: ", len(result_list))
                for polygon in result_list:
                    polygon = orient(polygon, -1)

                    if polygon.area < offset*offset/10:
                        continue

                    polygon = polygon.simplify(constants.simplification_threshold, False)
                    poly_coords = polygon.exterior
                    # if polygon.exterior.is_ccw:
                    #   hole.coords = list(hole.coords)[::-1]
                    #poly_coords = polygon.exterior.simplify(constants.simplification_threshold, False)
                    poly_coords = take_only_valid_linear_rings(poly_coords)
                    if poly_coords.is_empty:
                        continue
                    #print("node: - is ccw: ", LinearRing(poly_coords).is_ccw)
                    # if(LinearRing(poly_coords).is_ccw):
                    #    print("Fehler!")
                    node = AnyNode(id="node", parent=current_poly,
                                   val=poly_coords, already_rastered=False, transferred_point_priority_deque=DEPQ(
                                       iterable=None, maxlen=None))
                    active_polys.append(node)
                    hole_node_list = []
                    for hole in polygon.interiors:
                        hole_node = AnyNode(
                            id="hole", val=hole, already_rastered=False, transferred_point_priority_deque=DEPQ(
                                iterable=None, maxlen=None))
                        for previous_hole in current_holes:
                            if Polygon(hole).contains(Polygon(previous_hole.val)):
                                previous_hole.parent = hole_node
                        hole_node_list.append(hole_node)
                    active_holes.append(hole_node_list)
        for previous_hole in current_holes:  # if the previous holes are not contained in the new holes they have been merged with the outer polygon
            if previous_hole.parent == None:
                previous_hole.parent = current_poly


    #DebuggingMethods.drawPoly(root, 'r-')

    make_tree_uniform_ccw(root)
    # print(RenderTree(root))
    if strategy == StitchingStrategy.CLOSEST_POINT:
        connected_line, connected_line_origin = ConnectAndSamplePattern.connect_raster_tree_nearest_neighbor(
                root, offset, stitch_distance, starting_point, offset_by_half)
    elif strategy == StitchingStrategy.INNER_TO_OUTER:
        connected_line, connected_line_origin = ConnectAndSamplePattern.connect_raster_tree_from_inner_to_outer(
            root, offset, stitch_distance, starting_point, offset_by_half)
    else:
        print("Invalid strategy!")
        assert(0)

    return connected_line, connected_line_origin
