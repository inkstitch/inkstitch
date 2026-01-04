# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import LineString, Polygon
from shapely.affinity import translate, scale
from shapely import prepare
from ...utils.threading import check_stop_flag


class CrossGeometry(object):
    '''Holds data for cross stitch geometry:

       boxes:                   a list of box shaped polygons. The outlines for each cross.
                                To get the final outline for our cross stitch pattern,
                                we will combine all available boxes to a (hopefully) single shape.

       scaled_boxes:            same as boxes, except that the boxes are scaled p slightly.
                                Used to reconnect shapes which would be disconnected otherwise.
                                A good example for this are crosses which are touching each other at only one corner.

        diagonals1, diagonals2: A list of Linestrings with the actual cross stitch geometry

        travel_edges:           a list of Linestings with every possible edge in a cross stitch box:
                                the box outlines as well as lines from the box cornes to the center

        snap_points:            a list containing two lists with points.
                                1. the center points for each box
                                2. the four corners of each box
    '''
    def __init__(self, fill, shape, original_shape, cross_stitch_method):
        """Initialize cross stitch geometry generation for the given shape.

        Arguments:
            fill:                   the FillStitch instance
            shape:                  shape as shapely geometry
            cross_stitch_method:    cross stitch method as string
            original_shape:         we may have broken the shape apart.
                                    the offset however, should align to the complete shape geometry
        """
        self.cross_stitch_method = cross_stitch_method
        self.fill = fill

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
        self.scaled_boxes = []

        self.cross_diagonals1 = []
        self.cross_diagonals2 = []

        self.travel_edges = []
        self.snap_points = [[], []]

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

        if "flipped" in cross_stitch_method:
            self.cross_diagonals2, self.cross_diagonals1 = self.cross_diagonals1, self.cross_diagonals2

    def get_offset_values(self, shape, original_shape):
        offset_x, offset_y = self.fill.cross_offset
        if not self.fill.canvas_grid_origin:
            box_x, box_y = self.fill.pattern_size
            if original_shape:
                bounds = original_shape.bounds
            else:
                bounds = shape.bounds
            offset_x -= bounds[0] % box_x
            offset_y -= bounds[1] % box_y
        return offset_x, offset_y

    def add_cross(self, box, upright_box):
        if "upright" in self.cross_stitch_method:
            box = upright_box

        coords = list(box.exterior.coords)
        center = list(box.centroid.coords)[0]

        self.boxes.append(box)
        self.scaled_boxes.append(scale(box, xfact=1.0000000000001, yfact=1.0000000000001))

        self.cross_diagonals1.append(LineString([coords[0], coords[2]]))
        self.cross_diagonals2.append(LineString([coords[1], coords[3]]))

        self.travel_edges.append(LineString([coords[0], center]))
        self.travel_edges.append(LineString([coords[1], center]))
        self.travel_edges.append(LineString([coords[2], center]))
        self.travel_edges.append(LineString([coords[3], center]))
        self.travel_edges.append(LineString([coords[0], coords[1]]))
        self.travel_edges.append(LineString([coords[1], coords[2]]))
        self.travel_edges.append(LineString([coords[2], coords[3]]))
        self.travel_edges.append(LineString([coords[3], coords[0]]))

        self.snap_points[0].append(center)
        self.snap_points[1].append(coords[0])
        self.snap_points[1].append(coords[1])
        self.snap_points[1].append(coords[2])
        self.snap_points[1].append(coords[3])
