# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

from shapely import prepare
from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, Point, MultiPoint
from shapely.ops import nearest_points

from ...utils.threading import check_stop_flag


class CrossGeometries(object):
    '''Holds data for cross stitch geometry:
        crosses:        a list containing cross data
                        each cross is defined by five nodes
                        1. the center point
                        2. the four corners
        center_points:  a list with all center points
        boxes:          a list of box outlines as Polygons
        diagonals:      a list with cross diagonals as LineStrings
    '''
    def __init__(self, shape, pattern_size, coverage, cross_stitch_method, cross_offset, canvas_grid_origin, thread_count, original_shape=None):
        """Initialize cross stitch geometry generation for the given shape.
        Arguments:
            shape:                      shape as shapely geometry
            pattern_size:               grid size in px tuple(x, y)
            coverate:                   fill coverage in %
            cross_stitch_method:        cross stitch method as string
            cross_offset:               offset to original alignment in px tuple(x, y)
            original_shape (optional):  used for alignment, when shape had to be split up
        """
        self.pattern_size = pattern_size
        self.coverage = coverage
        self.cross_offset = cross_offset
        self.canvas_grid_origin = canvas_grid_origin
        self.cross_stitch_method = cross_stitch_method
        self.thread_count = thread_count
        self._shape = shape
        self._original_shape = original_shape
        self.boxes = []
        self.crosses = set()
        self.center_points = []
        self.diagonals = []
        self.crosses_by_good_point = defaultdict(list)
        self.crosses_by_bad_point = defaultdict(list)

        self.nb_repeats = (thread_count ) // 2

        prepare(shape)
        self._choose_cross_class()
        self._setup_geometry()
        self._setup_crosses()
        if "dense" in self.cross_stitch_method:
            self._setup_crosses(offset=True)
        self._classify_points()

    def _choose_cross_class(self):
        if "upright" in self.cross_stitch_method:
            self.cross_class = UprightCross
        elif "double" in self.cross_stitch_method:
            self.cross_class = DoubleCross
        elif "smyrna" in self.cross_stitch_method:
            self.cross_class = SmyrnaCross
        else:
            self.cross_class = Cross

    def _setup_geometry(self):
        self._box_x, self._box_y = self.pattern_size
        self._get_offset_values(self._shape, self._original_shape)
        self._square = Polygon([(0, 0), (self._box_x, 0), (self._box_x, self._box_y), (0, self._box_y)])
        self.full_square_area = self._square.area

        # upright polygon
        center = list(self._square.centroid.coords)[0]
        self._upright_square = Polygon([(0, center[1]), (center[0], 0), (self._box_x, center[1]), (center[0], self._box_y)])

        # start and end have to be a multiple of the stitch length
        # we also add the initial offset
        minx, miny, maxx, maxy = self._shape.bounds
        self._adapted_minx = minx - minx % self._box_x - self._offset_x
        self._adapted_miny = miny - miny % self._box_y + self._offset_y
        self._adapted_maxx = maxx + self._box_x - maxx % self._box_x
        self._adapted_maxy = maxy + self._box_y - maxy % self._box_y

    def _potential_middle_points(self, offset=False):
        potential_middle_points = []
        y = self._adapted_miny - self._box_y
        while y <= self._adapted_maxy + self._box_y:
            x = self._adapted_minx - self._box_x
            while x <= self._adapted_maxx + self._box_x:
                potential_middle_points.append((x + (self._box_x / 2), y))
                potential_middle_points.append((x, y + (self._box_y / 2)))
                x += self._box_x
            y += self._box_y

        return potential_middle_points

    def _snapped_box(self, box, points):
        snap_points = MultiPoint(points)
        snapped_coords = []
        for point in list(box.exterior.coords)[:4]:
            snapped_point = nearest_points(snap_points, Point(point))[0]
            snapped_coords.append((snapped_point.x, snapped_point.y))
        return Polygon(snapped_coords)

    def _setup_crosses(self, offset=False):
        snap_points = MultiPoint(self._potential_middle_points())
        center = list(self._square.centroid.coords)[0]
        if offset:
            delta_x = center[0]
            delta_y = center[1]
        else:
            delta_x = 0
            delta_y = 0
        y = self._adapted_miny - delta_y
        while y <= self._adapted_maxy:
            x = self._adapted_minx - delta_x
            while x <= self._adapted_maxx:
                # translate box to cross position
                box = translate(self._square, x, y)
                self._upright_box = translate(self._upright_square, x, y)
                if "dense" in self.cross_stitch_method:
                    self._upright_box = self._snapped_box(self._upright_box, snap_points)
                if self._shape.contains(box):
                    self.add_cross(box, self._upright_box)
                elif self._shape.intersects(box):
                    intersection = box.intersection(self._shape)
                    if intersection.area / self.full_square_area * 100 + 0.0001 >= self.coverage:
                        self.add_cross(box, self._upright_box)
                x += self._box_x
            y += self._box_y
            check_stop_flag()

    def _classify_points(self):
        for cross in self.crosses:
            for point in cross.good_points:
                self.crosses_by_good_point[point].append(cross)
            for point in cross.bad_points:
                self.crosses_by_bad_point[point].append(cross)

    def _get_offset_values(self, shape, original_shape):
        self._offset_x, self._offset_y = self.cross_offset
        if not self.canvas_grid_origin:
            box_x, box_y = self.pattern_size
            bounds = shape.bounds
            if original_shape:
                bounds = original_shape.bounds
            self._offset_x -= bounds[0] % box_x
            self._offset_y += bounds[1] % box_y

    def add_cross(self, box, upright_box):
        center_point = list(box.centroid.coords)[0]
        corners = list(box.exterior.coords)[:4]
        middle_points = list(upright_box.exterior.coords)[:4]

        cross = self.cross_class(center_point, corners, middle_points, self.nb_repeats)
        self.crosses.add(cross)

        # diagnonals for half crosses
        if "flipped" in self.cross_stitch_method:
            diagonal = LineString([cross.bottom_left, cross.top_right])
        else:
            diagonal = LineString([cross.top_left, cross.bottom_right])

        self.center_points.append(cross.center_point)
        self.diagonals.append(diagonal)
        self.boxes.append(box)

    def remove_cross(self, cross):
        for point in cross.good_points:
            self.crosses_by_good_point[point].remove(cross)
        for point in cross.bad_points:
            self.crosses_by_bad_point[point].remove(cross)
        self.crosses.remove(cross)


class Cross:
    """A single cross in a cross stitch fill

    Has attributes for corners, middle points, and center point.  Also has
    good_points and bad_points, which cover good and bad points from which to
    start stitching this cross.
    """

    def __init__(self, center_point, corners, middle_points, nb_repeats):
        self.center_point = center_point

        self.corners = corners
        self.top_left = corners[0]
        self.top_right = corners[1]
        self.bottom_right = corners[2]
        self.bottom_left = corners[3]

        self.middle_points = middle_points
        self.middle_left = middle_points[0]
        self.middle_top = middle_points[1]
        self.middle_right = middle_points[2]
        self.middle_bottom = middle_points[3]

        self.nb_repeats = nb_repeats

        self.good_points = (self.top_right, self.bottom_left)
        self.bad_points = (self.top_left, self.bottom_right)
        self.all_connection_points = self.corners
        self.stitches = (self.good_points, self.bad_points)

    def get(self, attribute):
        """Temporary compatibility method"""
        return getattr(self, attribute)

    def cycle_from_point(self, starting_point):
        if starting_point == self.top_left:
            return self.cycle_from_top_left()
        elif starting_point == self.top_right:
            return self.cycle_from_top_right()
        elif starting_point == self.bottom_left:
            return self.cycle_from_bottom_left()
        elif starting_point == self.bottom_right:
            return self.cycle_from_bottom_right()

    def cycle_from_top_left(self):
        return (
            [self.bottom_right, self.top_left] * (self.nb_repeats - 1) +
            [self.bottom_right, self.center_point] +
            [self.top_right, self.bottom_left] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.top_left]
        )

    def cycle_from_bottom_right(self):
        return (
            [self.top_left, self.bottom_right] * (self.nb_repeats - 1) +
            [self.top_left, self.center_point] +
            [self.top_right, self.bottom_left] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.bottom_right]
        )

    def cycle_from_top_right(self):
        return (
            [self.center_point] +
            [self.top_left, self.bottom_right] * self.nb_repeats +
            [self.center_point] +
            [self.bottom_left, self.top_right] * self.nb_repeats
        )

    def cycle_from_bottom_left(self):
        return (
            [self.center_point] +
            [self.bottom_right, self.top_left] * self.nb_repeats +
            [self.center_point] +
            [self.top_right, self.bottom_left] * self.nb_repeats
        )


class UprightCross(Cross):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.good_points = [self.middle_top, self.middle_bottom]
        self.bad_points = [self.middle_left, self.middle_right]
        self.all_connection_points = self.good_points + self.bad_points
        self.stitches = (self.good_points, self.bad_points)

    def cycle_from_point(self, starting_point):
        if starting_point == self.middle_top:
            return self.cycle_from_middle_top()
        elif starting_point == self.middle_bottom:
            return self.cycle_from_middle_bottom()
        elif starting_point == self.middle_left:
            return self.cycle_from_middle_left()
        elif starting_point == self.middle_right:
            return self.cycle_from_middle_right()

    def cycle_from_middle_top(self):
        return (
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_bottom, self.middle_top] * self.nb_repeats
        )

    def cycle_from_middle_bottom(self):
        return (
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats
        )

    def cycle_from_middle_left(self):
        return (
            [self.middle_right, self.middle_left] * (self.nb_repeats - 1) +
            [self.middle_right, self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.middle_left]
        )

    def cycle_from_middle_right(self):
        return (
            [self.middle_left, self.middle_right] * (self.nb_repeats - 1) +
            [self.middle_left, self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.middle_right]
        )


class DoubleCross(Cross):
    # Top Cross is the normal cross
    # Double Cross has the same corners and diagonals as normal Cross, so no
    # need to override __init__()

    def cycle_from_top_left(self):
        return (
            [self.bottom_right, self.top_left] * (self.nb_repeats - 1) +
            [self.bottom_right, self.center_point] +

            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            [self.center_point] +

            [self.top_right, self.bottom_left] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.top_left]
        )

    def cycle_from_bottom_right(self):
        return (
            [self.top_left, self.bottom_right] * (self.nb_repeats - 1) +
            [self.top_left, self.center_point] +

            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            [self.center_point] +

            [self.top_right, self.bottom_left] * self.nb_repeats +

            # this is bad travel
            [self.center_point, self.bottom_right]
        )

    def cycle_from_top_right(self):
        return (
            [self.center_point] +
            [self.top_left, self.bottom_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            [self.center_point] +
            [self.bottom_left, self.top_right] * self.nb_repeats
        )

    def cycle_from_bottom_left(self):
        return (
            [self.center_point] +
            [self.bottom_right, self.top_left] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            [self.center_point] +
            [self.top_right, self.bottom_left] * self.nb_repeats
        )


class SmyrnaCross(Cross):
    # Top cross is the upright cross, this is the usual handstitch order for double crosses.
    # To avoid bad traveling, we favor connecting the cycles through the top middle points,
    # and bottom middle points, any other connecting  point creates bad traveling.
    # We will need to connect via diagonal point when the crosses are joined only at diagonal
    # We do not use connection via middle left and middle right point as when they exist,
    # the connection via diagonal is also possible.
    # As end result, there will be exactly one bad traveled cross on each connected column of Smyrna crosses.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.good_points = [self.middle_top, self.middle_bottom]
        self.bad_points = [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
        self.all_connection_points = self.good_points + self.bad_points

    def cycle_from_point(self, starting_point):
        if starting_point == self.middle_top:
            return self.cycle_from_middle_top()
        elif starting_point == self.middle_bottom:
            return self.cycle_from_middle_bottom()
        elif starting_point == self.top_left:
            return self.cycle_from_top_left()
        elif starting_point == self.top_right:
            return self.cycle_from_top_right()
        elif starting_point == self.bottom_left:
            return self.cycle_from_bottom_left()
        elif starting_point == self.bottom_right:
            return self.cycle_from_bottom_right()

    def cycle_from_middle_top(self):
        return (
            [self.center_point] +
            [self.top_left, self.bottom_right] * self.nb_repeats +
            [self.center_point] +
            [self.bottom_left, self.top_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_bottom, self.middle_top] * self.nb_repeats
        )

    def cycle_from_middle_bottom(self):
        return (
            [self.center_point] +
            [self.top_left, self.bottom_right] * self.nb_repeats +
            [self.center_point] +
            [self.bottom_left, self.top_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats
        )

    def cycle_from_top_left(self):
        return (
            [self.bottom_right, self.top_left] * (self.nb_repeats - 1) +
            [self.bottom_right, self.center_point] +
            [self.bottom_left, self.top_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_bottom, self.middle_top] * self.nb_repeats +
            # this is bad travel
            [self.center_point, self.top_left]
        )

    def cycle_from_bottom_right(self):
        return (
            [self.top_left, self.bottom_right] * (self.nb_repeats - 1) +
            [self.top_left, self.center_point] +
            [self.top_right, self.bottom_left] * self.nb_repeats +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            # this is bad travel
            [self.center_point, self.bottom_right]
        )

    def cycle_from_top_right(self):
        return (
            [self.center_point] +
            [self.top_left, self.bottom_right] * self.nb_repeats +
            [self.center_point, self.bottom_left] +
            [self.top_right, self.bottom_left] * (self.nb_repeats - 1) +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            # this is bad travel
            [self.center_point, self.top_right]
        )

    def cycle_from_bottom_left(self):
        return (
            [self.center_point] +
            [self.bottom_right, self.top_left] * self.nb_repeats +
            [self.center_point, self.top_right] +
            [self.bottom_left, self.top_right] * (self.nb_repeats - 1) +
            [self.center_point] +
            [self.middle_left, self.middle_right] * self.nb_repeats +
            [self.center_point] +
            [self.middle_top, self.middle_bottom] * self.nb_repeats +
            # this is bad travel
            [self.center_point, self.bottom_left]
        )
