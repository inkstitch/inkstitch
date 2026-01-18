# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import LineString, Polygon
from shapely.affinity import translate
from shapely import prepare
from ...utils.threading import check_stop_flag
from ...utils import DotDict


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
        self.fill = fill
        self.cross_stitch_method = cross_stitch_method

        box_x, box_y = self.fill.pattern_size
        offset_x, offset_y = self.get_offset_values(shape, original_shape)
        square = Polygon([(0, 0), (box_x, 0), (box_x, box_y), (0, box_y)])
        self.full_square_area = square.area

        # upright polygon
        center = list(square.centroid.coords)[0]
        upright_square = Polygon([(0, center[1]), (center[0], 0), (box_x, center[1]), (center[0], box_y)])

        # start and end have to be a multiple of the stitch length
        # we also add the initial offset
        minx, miny, maxx, maxy = shape.bounds
        adapted_minx = minx - minx % box_x - offset_x
        adapted_miny = miny - miny % box_y + offset_y
        adapted_maxx = maxx + box_x - maxx % box_x
        adapted_maxy = maxy + box_y - maxy % box_y

        prepare(shape)

        self.boxes = []
        self.crosses = []
        self.center_points = []
        self.diagonals = []

        y = adapted_miny
        while y <= adapted_maxy:
            x = adapted_minx
            while x <= adapted_maxx:
                # translate box to cross position
                box = translate(square, x, y)
                upright_box = translate(upright_square, x, y)
                if shape.contains(box):
                    self.add_cross(box, upright_box)
                elif shape.intersects(box):
                    intersection = box.intersection(shape)
                    if intersection.area / self.full_square_area * 100 + 0.0001 >= self.fill.fill_coverage:
                        self.add_cross(box, upright_box)
                x += box_x
            y += box_y
            check_stop_flag()

    def get_offset_values(self, shape, original_shape):
        offset_x, offset_y = self.fill.cross_offset
        if not self.fill.canvas_grid_origin:
            box_x, box_y = self.fill.pattern_size
            bounds = shape.bounds
            if original_shape:
                bounds = original_shape.bounds
            offset_x -= bounds[0] % box_x
            offset_y -= bounds[1] % box_y
        return offset_x, offset_y

    def add_cross(self, box, upright_box):
        cross = DotDict()

        # center point
        cross.center_point = list(box.centroid.coords)[0]

        if "upright" in self.cross_stitch_method:
            box = upright_box

        # box corners
        coords = list(box.exterior.coords)
        cross.corners = [coords[0], coords[1], coords[2], coords[3]]
        cross.bottom_left = coords[3]
        cross.bottom_right = coords[2]
        cross.top_right = coords[1]
        cross.top_left = coords[0]

        # middle points for the four sides of the box
        coords = list(upright_box.exterior.coords)
        cross.middle_left = [coords[0], coords[1], coords[2], coords[3]]
        cross.middle_bottom = coords[3]
        cross.middle_right = coords[2]
        cross.middle_top = coords[1]
        cross.middle_left = coords[0]

        # diagnonals for half crosses
        if "flipped" in self.cross_stitch_method:
            diagonal = LineString([cross.bottom_left, cross.top_right])
        else:
            diagonal = LineString([cross.top_left, cross.bottom_right])

        self.crosses.append(cross)
        self.center_points.append(cross.center_point)
        self.diagonals.append(diagonal)
        self.boxes.append(box)
