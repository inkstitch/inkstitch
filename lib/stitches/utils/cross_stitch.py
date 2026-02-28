# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict

from shapely import prepare
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Polygon

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
    def __init__(self, fill, shape, cross_stitch_method, original_shape=None):
        """Initialize cross stitch geometry generation for the given shape.

        Arguments:
            fill:                       the FillStitch instance
            shape:                      shape as shapely geometry
            cross_stitch_method:        cross stitch method as string
            original_shape (optional):  used for alignment, when shape had to be split up
        """
        if "flip" in cross_stitch_method:
            shape = rotate(shape, 90, origin=(0, 0))

        self.fill = fill
        self.cross_stitch_method = cross_stitch_method
        self._shape = shape
        self._original_shape = original_shape
        self.boxes = []
        self.crosses = set()
        self.center_points = []
        self.diagonals = []
        self.crosses_by_good_point = defaultdict(list)
        self.crosses_by_bad_point = defaultdict(list)

        prepare(shape)
        self._setup_geometry()
        self._setup_crosses()
        self._classify_points()

    def _setup_geometry(self):
        self._box_x, self._box_y = self.fill.pattern_size
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

    def _setup_crosses(self):
        self._grid = dict()
        grid_x = grid_y = 0
        y = self._adapted_miny
        while y <= self._adapted_maxy:
            x = self._adapted_minx
            grid_x = 0
            while x <= self._adapted_maxx:
                # translate box to cross position
                box = translate(self._square, x, y)
                self._upright_box = translate(self._upright_square, x, y)
                if self._shape.contains(box):
                    self._grid[(grid_x, grid_y)] = self.add_cross(box, self._upright_box)
                elif self._shape.intersects(box):
                    intersection = box.intersection(self._shape)
                    if intersection.area / self.full_square_area * 100 + 0.0001 >= self.fill.fill_coverage:
                        self._grid[(grid_x, grid_y)] = self.add_cross(box, self._upright_box)
                x += self._box_x
                grid_x += 1
            y += self._box_y
            grid_y += 1
            check_stop_flag()

        self._grid_x_max = grid_x
        self._grid_y_max = grid_y

    def _classify_points(self):
        for cross in self.crosses:
            for point in cross.good_points:
                self.crosses_by_good_point[point].append(cross)
            for point in cross.bad_points:
                self.crosses_by_bad_point[point].append(cross)

    def _get_offset_values(self, shape, original_shape):
        self._offset_x, self._offset_y = self.fill.cross_offset
        if not self.fill.canvas_grid_origin:
            box_x, box_y = self.fill.pattern_size
            bounds = shape.bounds
            if original_shape:
                bounds = original_shape.bounds
            self._offset_x -= bounds[0] % box_x
            self._offset_y -= bounds[1] % box_y

    def add_cross(self, box, upright_box):
        center_point = list(box.centroid.coords)[0]

        if "upright" in self.cross_stitch_method:
            box = upright_box
        corners = list(box.exterior.coords)[:4]
        middle_points = list(upright_box.exterior.coords)[:4]

        cross = Cross(center_point, corners, middle_points)
        self.crosses.add(cross)

        # diagnonals for half crosses
        if "flipped" in self.cross_stitch_method:
            diagonal = LineString([cross.bottom_left, cross.top_right])
        else:
            diagonal = LineString([cross.top_left, cross.bottom_right])

        self.center_points.append(cross.center_point)
        self.diagonals.append(diagonal)
        self.boxes.append(box)

        return cross

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

    def __init__(self, center_point, corners, middle_points):
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

        self.good_points = (self.top_right, self.bottom_left)
        self.bad_points = (self.top_left, self.bottom_right)

    def get(self, attribute):
        """Temporary compatibility method"""
        return getattr(self, attribute)

    def cycle_from_point(self, starting_point, nb_repeats):
        if starting_point == self.top_left:
            return self.cycle_from_top_left(nb_repeats)
        elif starting_point == self.top_right:
            return self.cycle_from_top_right(nb_repeats)
        elif starting_point == self.bottom_left:
            return self.cycle_from_bottom_left(nb_repeats)
        elif starting_point == self.bottom_right:
            return self.cycle_from_bottom_right(nb_repeats)

    def cycle_from_top_left(self, nb_repeats):
        return (
            [self.bottom_right, self.top_left] * nb_repeats +
            [self.bottom_right, self.center_point] +
            [self.top_right, self.bottom_left] * (nb_repeats + 1) +

            # this is bad travel
            [self.center_point, self.top_left]
        )

    def cycle_from_bottom_right(self, nb_repeats):
        return (
            [self.top_left, self.bottom_right] * nb_repeats +
            [self.top_left, self.center_point] +
            [self.top_right, self.bottom_left] * (nb_repeats + 1) +

            # this is bad travel
            [self.center_point, self.bottom_right]
        )

    def cycle_from_top_right(self, nb_repeats):
        return (
            [self.center_point, self.top_left] +
            [self.bottom_right, self.top_left] * nb_repeats +
            [self.bottom_right, self.center_point] +
            [self.bottom_left, self.top_right] * (nb_repeats + 1)
        )

    def cycle_from_bottom_left(self, nb_repeats):
        return (
            [self.center_point, self.bottom_right] +
            [self.top_left, self.bottom_right] * nb_repeats +
            [self.top_left, self.center_point] +
            [self.top_right, self.bottom_left] * (nb_repeats + 1)
        )
