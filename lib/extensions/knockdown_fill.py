# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import sqrt

from inkex import Boolean, Path, PathElement
from shapely import minimum_bounding_circle, union_all
from shapely.geometry import LineString, Polygon

from ..stitches.ripple_stitch import ripple_stitch
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..utils.geometry import ensure_multi_polygon
from .base import InkstitchExtension


class KnockdownFill(InkstitchExtension):
    '''
    This extension generates a shape around all selected shapes and inserts it into the document
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-l", "--stitch-length", type=float, default=3, dest="stitch_length")
        self.arg_parser.add_argument("-k", "--keep-holes", type=Boolean, default=True, dest="keep_holes")
        self.arg_parser.add_argument("-o", "--offset", type=float, default=0, dest="offset")
        self.arg_parser.add_argument("-j", "--join-style", type=str, default="1", dest="join_style")
        self.arg_parser.add_argument("-m", "--mitre-limit", type=float, default=5.0, dest="mitre_limit")

        self.arg_parser.add_argument("-s", "--shape", type=str, default='', dest="shape")
        self.arg_parser.add_argument("-f", "--shape-offset", type=float, default=0, dest="shape_offset")
        self.arg_parser.add_argument("-p", "--shape-join-style", type=str, default="1", dest="shape_join_style")
        # TODO: Layer options: underlay, row spacing, angle

    def effect(self):
        if not self.get_elements():
            return

        polygons = []
        for element in self.elements:
            polygons.extend(self.element_outlines(element))
        combined_shape = union_all(polygons)

        offset_shape = self._apply_offset(combined_shape, self.options.offset, self.options.join_style)
        offset_shape = offset_shape.simplify(0.3)
        offset_shape = ensure_multi_polygon(offset_shape)

        self.insert_knockdown_elements(offset_shape)

    def element_outlines(self, element):
        polygons = []
        if element.name == "FillStitch":
            # take expand value into account
            shape = element.shrink_or_grow_shape(element.shape, element.expand)
            # MultiPolygon
            for polygon in shape.geoms:
                polygons.append(polygon)
        elif element.name == "SatinColumn":
            # plot points on rails, so we get the actual satin size (including pull compensation)
            rail_pairs = zip(*element.plot_points_on_rails(
                0.3,
                element.pull_compensation_px,
                element.pull_compensation_percent / 100)
            )
            rails = []
            for rail in rail_pairs:
                rails.append(LineString(rail))
            polygon = Polygon(list(rails[0].coords) + list(rails[1].reverse().coords)).buffer(0)
            polygons.append(polygon)
        elif element.name == "Stroke":
            if element.stroke_method == 'ripple_stitch':
                # for ripples this is going to be a bit complicated, so let's follow the stitch plan
                polygons.extend(self._ripple_knockdown(element))
            elif element.stroke_method == 'zigzag_stitch':
                # zigzag stitch depends on the width of the stroke and pull compensation settings
                polygons.append(element.as_multi_line_string().buffer((element.stroke_width + element.pull_compensation) / 2, cap_style='flat'))
            else:
                polygons.append(element.as_multi_line_string().buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
        elif element.name == "Clone":
            with element.clone_elements() as elements:
                for clone_child in elements:
                    polygons.extend(self.element_outlines(clone_child))
        return polygons

    def _apply_offset(self, shape, offset_mm, join_style):
        return shape.buffer(
            offset_mm * PIXELS_PER_MM,
            cap_style=int(join_style),
            join_style=int(join_style),
            mitre_limit=float(max(self.options.mitre_limit, 0.1))
        )

    def _ripple_knockdown(self, element):
        polygons = []
        stitch_groups = ripple_stitch(element)
        for stitches in stitch_groups:
            linestring = LineString(stitches)
            polygons.append(linestring.buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
        return polygons

    def insert_knockdown_elements(self, combined_shape):
        first = self.svg.selection.rendering_order()[0]
        try:
            parent = first.getparent()
            index = parent.index(first)
        except AttributeError:
            parent = self.svg
            index = 0
        transform = get_correction_transform(first)

        if self.options.shape:
            self._insert_embossed_path(combined_shape, transform, parent, index)
        else:
            self._insert_knockdown_path(combined_shape, transform, parent, index)

    def _insert_embossed_path(self, combined_shape, transform, parent, index):
        if self.options.shape == 'rect':
            rect = combined_shape.envelope
            offset_shape = self._apply_offset(rect, self.options.shape_offset, self.options.shape_join_style)
        else:
            circle = minimum_bounding_circle(combined_shape)
            offset_shape = self._apply_offset(circle, self.options.shape_offset, self.options.shape_join_style)

        offset_shape = offset_shape.reverse()
        d = str(Path(offset_shape.exterior.coords))

        for polygon in combined_shape.geoms:
            d += str(Path(polygon.exterior.coords))
            d += self._get_hole_paths(polygon)

        self.insert_path(d, transform, parent, index)

    def _insert_knockdown_path(self, combined_shape, transform, parent, index):
        for polygon in combined_shape.geoms:
            d = str(Path(polygon.exterior.coords))
            d += self._get_hole_paths(polygon)
            self.insert_path(d, transform, parent, index)

    def _get_hole_paths(self, polygon):
        d = ''
        if not self.options.keep_holes:
            return d
        for interior in polygon.interiors:
            d += str(Path(interior.coords))
        return d

    def insert_path(self, d, transform, parent, index):
        stitch_length = self.options.stitch_length
        row_spacing = (sqrt(3) * stitch_length) / 2

        path = PathElement()
        path.set('d', d)
        path.label = self.svg.get_unique_id('Knockdown ')
        path.set('transform', transform)

        path.set('inkstitch:max_stitch_length_mm', stitch_length)
        path.set('inkstitch:row_spacing_mm', '{0:.4f}'.format(row_spacing))
        path.set('inkstitch:fill_underlay_angle', '60 -60')
        path.set('inkstitch:fill_underlay_max_stitch_length_mm', stitch_length)
        path.set('inkstitch:fill_underlay_row_spacing_mm', '{0:.4f}'.format(row_spacing))
        path.set('inkstitch:underlay_underpath', 'False')
        path.set('inkstitch:underpath', 'False')
        path.set('inkstitch:staggers', '2')
        path.set('style', 'fill:black;')

        parent.insert(index, path)
