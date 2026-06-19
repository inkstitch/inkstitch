from shapely import get_point
from shapely.geometry import LinearRing, LineString, Point, Polygon
from shapely.ops import nearest_points, substring
from shapely.prepared import prep

from ...debug.debug import debug
from ...utils.geometry import ensure_multi_line_string, roll_linear_ring
from ...utils.threading import check_stop_flag


def connect_offset_lines(shape, segments, row_spacing, skip_last, max_stitch_length) -> list[LineString]:
    ''' Used by guided fill parallel offset and buffer methods
        This first splits the segments into two groups:
        - lines within the shape
        - lines intersecting the shape exterior border
        1. Shapes within: rings which are fully covered by an other ring in row spacing distance will be connected with the outer ring
        2. Connect shapes within to the second group (intersecting lines)
    '''
    outline_segments, segments_within = _split_segment_types(shape, segments, row_spacing)
    if not segments_within:
        return segments
    if not outline_segments:
        outline_segments = list(ensure_multi_line_string(shape.boundary).geoms)

    # sort inside segments from small to big
    segments_within.sort(key=lambda pg: pg.area)

    # now that we found out which segments need to be connected
    # let's see how they are related to each other
    connected_segments = _get_segment_relations(segments_within)

    # the polygons were helpful to figure out the geometric relationsship between the shapes
    # up from now we prefer to work with LinearRings, the index positions will stay the same
    linearrings_within = [LinearRing(seg.exterior.coords) for seg in segments_within]

    # now let's loop through the connected_segments dictionary and connect the shapes as good as possible
    _connect_within(connected_segments, linearrings_within, row_spacing, skip_last, max_stitch_length)

    debug.add_layer('rings within')
    debug.log_line_strings(linearrings_within)

    # now we cleaned up the inner circles
    # we only need to connect them to the outside
    _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing)

    debug.add_layer('connected offset segments')
    debug.log_line_strings(outline_segments)

    return outline_segments


def _split_segment_types(shape, segments, row_spacing) -> tuple[list[LineString], list[Polygon]]:
    ''' Splits segments into lines within the shape and lines intersecting the shapes exterior
    '''
    # we have two different kinds of segments:
    # the ones that are touching the outline
    # and the ones, that are entirely within the shape (those are the ones we need to connect)

    prepared_shape = prep(shape)
    # strategy 2 (everything is a ring), ensure that grating lines intersecting holes are still connected to the outside
    prepared_boundary = prep(shape.exterior)
    # strategy 1: prepared_boundary = prep(shape.boundary)

    outline_segments = []
    segments_within = []
    for line in segments:
        if not prepared_shape.intersects(line):
            continue
        if not prepared_boundary.intersects(line):
            # ensure the line has at least 4 points, which is necessary for both, polygon or linearring
            if len(line.coords) < 4:
                length = line.length
                line = line.segmentize(max_segment_length=length/3).coords[:]
            segments_within.append(Polygon(line))
        else:
            # if this segment has the same starting and ending point (linearring),
            # we need to ensure, that this point lies outside of the shape
            if line.coords[0] == line.coords[-1] and get_point(line, 0).within(shape):
                outside_point = ensure_multi_line_string(line.difference(shape)).geoms[0].interpolate(0.5, True)
                line = LineString(roll_linear_ring(line, line.project(outside_point)))
            outline_segments.append(line)
    return outline_segments, segments_within


def _get_segment_relations(segments_within) -> dict[int, int | None]:
    ''' Generates a dictionary with the information on which element is covered by an other
        connected_segments:
        - key: inner segment (index)
        - value: outer segment (index)
    '''
    connected_segments: dict[int, int | None] = {}
    for i, inner in enumerate(segments_within):
        segment_connected = False
        for j, outer in enumerate(segments_within):
            if j <= i:
                continue
            if outer.covers(inner):
                segment_connected = True
                connected_segments[i] = j
                break
        if not segment_connected:
            connected_segments[i] = None
    return connected_segments


def _connect_within(connected_segments, linearrings_within, row_spacing, skip_last, max_stitch_length) -> None:
    ''' Connects inner lines with their outer lines'''
    # while we are connecting the shapes, we will update the shape at the outer_index position to contain the connected shape
    # therefore we will need to collect the indices of the inner shapes that are now duplicated
    # this way we can remove them from the list in the end
    segments_to_remove: list[int] = []
    for inner_index, outer_index in connected_segments.items():
        if outer_index is None:
            continue

        if row_spacing == 0:
            row_spacing = 0.001

        # First we are more restrict in order to find a good spot
        d_tolerance = row_spacing * 1.5
        shapes_are_connected = _connect_linearrings(
            linearrings_within, segments_to_remove, inner_index, outer_index, row_spacing, skip_last, max_stitch_length, d_tolerance
        )
        if not shapes_are_connected:
            # we couldn't find an ok spot, so let's skip this element
            segments_to_remove.append(inner_index)

    # remove the duplicated inner segments
    segments_to_remove.sort(reverse=True)
    for segment_index in segments_to_remove:
        try:
            linearrings_within.pop(segment_index)
        except IndexError:
            pass


def _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing, iteration=0) -> None:
    ''' Try to connect each ring to an outline segment (a segment intersecting with the shapes exterior.
        Some rings may need adjacing rings to be connected first until they can find their match,
        So we run this in multiple iterations.
    '''
    remove: list[int] = []
    add: list[LineString] = []
    unconnected: list[LineString] = []
    for ring in linearrings_within:
        _connect_ring(ring, shape, outline_segments, linearrings_within, row_spacing, unconnected, remove, add)
    # remove the duplicated inner segments
    for segment_index in sorted(remove, reverse=True):
        try:
            outline_segments.pop(segment_index)
        except IndexError:
            pass
    outline_segments.extend(add)
    if unconnected and iteration < 5:
        # give it an other try, we may have made helping connections in the last iteration
        linearrings_within = unconnected
        iteration += 1
        _connect_rings_to_regular_lines(shape, outline_segments, linearrings_within, row_spacing, iteration)


def _connect_linearrings(
        linearrings_within, segments_to_remove, inner_index, outer_index, row_spacing, skip_last, max_stitch_length, d_tolerance) -> bool:
    '''Try to connect two linearrings
       Returns True on success and False if the rings couldn't be connected
    '''
    # ensure consistent direction
    inner = ensure_ccw(linearrings_within[inner_index])
    outer = ensure_ccw(linearrings_within[outer_index])
    # We could speed things up by predefining a good spot,
    # but we get nicer connections for smoothing if we don't (speed vs stitch path...)
    # nearest = nearest_points(inner, outer)
    # inner = roll_linear_ring(inner, inner.project(nearest[0]))
    offset = 0
    # move around the inner ring and check combining conditions in sections of row_spacing width
    while offset + row_spacing < inner.length:
        check_stop_flag()
        p1_inner, p2_inner, p1_outer, p2_outer, d1, d2 = _get_possible_connector_points(inner, outer, offset, row_spacing)
        # check if distances are within tolerance
        if d1 < row_spacing + d_tolerance and d2 < row_spacing + d_tolerance:
            proj1 = inner.project(p2_inner)
            proj2 = outer.project(p2_outer)
            rolled_inner = LineString(roll_linear_ring(inner, proj1))
            rolled_outer = LineString(roll_linear_ring(outer, proj2))
            # row_spacing is not 0, we know we'll end up with a LineString, but mypy needs to know, so let's ensure
            rolled_inner = ensure_multi_line_string(substring(rolled_inner, 0, -row_spacing)).geoms[0]
            rolled_outer = ensure_multi_line_string(substring(rolled_outer, 0, -row_spacing)).geoms[0]
            if skip_last:
                connected_line = LinearRing(rolled_outer.coords[:] + rolled_inner.segmentize(max_stitch_length).reverse().coords[1:-1])
            else:
                connected_line = LinearRing(rolled_outer.coords[:] + rolled_inner.reverse().coords[:])
            linearrings_within[outer_index] = connected_line
            segments_to_remove.append(inner_index)
            return True
        offset += 1
    return False


def _connect_ring(ring, shape, outline_segments, linearrings_within, row_spacing, unconnected, remove, add) -> None:
    ''' Try to connect a ring to one of the outline_segments
    '''
    original_ring = ring
    connected = None
    for i in range(len(outline_segments)):
        if i in remove:
            continue
        line = outline_segments[i]
        if original_ring.distance(line) <= row_spacing + 0.001:
            if connected is None:
                new_segment = _connect_linearring_with_linestring(shape, ring, line, row_spacing)
                if new_segment is not None:
                    outline_segments[i] = new_segment
                    ring = new_segment
                    connected = i
                    if line.intersects(shape.exterior):
                        return
            else:
                if get_point(line, 0).within(shape):
                    seg1 = _connect_linearring_with_linestring(shape, ring, line, row_spacing)
                    if seg1 is None:
                        continue
                else:
                    seg1, seg2 = _connect_linestrings(ring, line, row_spacing)
                    add.append(seg2)
                outline_segments[connected] = seg1
                remove.append(i)
                # let's not try any harder
                return
    unconnected.append(ring)


def _connect_linestrings(line1, line2, row_spacing):
    ''' combines two linestrings '''
    # connect two linestrings
    p1, p3 = nearest_points(line1, line2)
    p2 = line1.interpolate(line1.project(p1) + row_spacing)
    p4 = line2.interpolate(line2.project(p3) + row_spacing)
    if _needs_reverse(p1, p2, p3, p4):
        p4 = line2.interpolate(line2.project(p3) - row_spacing)
        line2 = line2.reverse()
    segment1 = substring(line1, 0, line1.project(p1))
    segment2 = substring(line2, 0, line2.project(p3)).reverse()
    segment3 = substring(line1, line1.project(p2), line1.length).reverse()
    segment4 = substring(line2, line2.project(p4), line2.length)
    connected = LineString(list(segment1.coords) + list(segment2.coords)), LineString(list(segment3.coords) + list(segment4.coords))
    return connected


def _needs_reverse(p1, p2, p3, p4):
    ''' check if the two connector lines are crossing each other '''
    p1p3 = LineString([p1, p3])
    p2p4 = LineString([p2, p4])
    if p1p3.intersects(p2p4):
        return True
    return False


def _connect_linearring_with_linestring(shape, ring, line, row_spacing, threshold=0.01):
    ''' connect the inner rings with the lines which are interesecting the outline
    '''
    offset = 0
    while ring.length >= row_spacing + offset:
        check_stop_flag()
        line_fraction = line.intersection(shape)
        if line_fraction.is_empty:
            return None
        p1, p2, p3, p4, d1, d2 = _get_possible_connector_points(ring, line_fraction, offset, row_spacing)
        if d1 < row_spacing * 1.5 and d2 < row_spacing * 1.5:
            # line start
            proj1 = line.project(p3)
            proj2 = line.project(p4)
            if proj1 > proj2:
                proj1, proj2 = proj2, proj1
            if abs(proj1 - proj2) > row_spacing + threshold:
                proj2 = proj1 + row_spacing
            o1 = substring(line, 0, proj1)
            o2 = substring(line, proj1 + row_spacing, line.length)
            # open the ring
            proj1 = ring.project(p1)
            rolled_ring = LineString(roll_linear_ring(ring, proj1))
            rolled_ring = substring(rolled_ring, row_spacing, rolled_ring.length)
            # connect the parts
            connected = LineString(o1.coords[:] + rolled_ring.coords[:] + o2.coords[:])
            if not connected.is_simple:
                connected = LineString(o1.coords[:] + rolled_ring.coords[::-1] + o2.coords[:])
            return connected
        offset += 1
    return None


def _get_possible_connector_points(inner, outer, offset, row_spacing) -> tuple[Point, Point, Point, Point, float, float]:
    ''' Gather information about possible connector positions '''
    # define two points on the inner ring according to offset and row_spacing
    p1 = inner.interpolate(offset)
    p2 = inner.interpolate(offset + row_spacing)
    # get nearest points on the outer ring
    p1_outer = nearest_points(outer, p1)[0]
    p2_outer = nearest_points(outer, p2)[0]
    # get the distances between the corresponding points
    d1 = p1.distance(p1_outer)
    d2 = p2.distance(p2_outer)
    return p1, p2, p1_outer, p2_outer, d1, d2


def ensure_ccw(ring) -> LinearRing:
    ''' Ensure that a linear ring runs counter clockwise '''
    if ring.is_ccw:
        return ring
    else:
        return ring.reverse()
