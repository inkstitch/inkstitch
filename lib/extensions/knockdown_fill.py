# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, Path, PathElement
from shapely import union_all
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
        self.arg_parser.add_argument("-k", "--keep-holes", type=Boolean, default=True, dest="keep_holes")
        self.arg_parser.add_argument("-o", "--offset", type=float, default=0, dest="offset")
        self.arg_parser.add_argument("-j", "--join-style", type=str, default="1", dest="join_style")
        self.arg_parser.add_argument("-m", "--mitre-limit", type=float, default=5.0, dest="mitre_limit")
        # TODO: Layer options: underlay, row spacing, angle

    def effect(self):
        if not self.get_elements():
            return

        polygons = []
        for element in self.elements:
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
                    stitches = ripple_stitch(element)
                    linestring = LineString(stitches)
                    polygons.append(linestring.buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
                elif element.stroke_method == 'zigzag_stitch':
                    # zigzag stitch depends on the width of the stroke and pull compensation settings
                    polygons.append(element.as_multi_line_string().buffer((element.stroke_width + element.pull_compensation) / 2, cap_style='flat'))
                else:
                    polygons.append(element.as_multi_line_string().buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
        combined_shape = union_all(polygons)
        combined_shape = combined_shape.buffer(
            self.options.offset * PIXELS_PER_MM,
            cap_style=int(self.options.join_style),
            join_style=int(self.options.join_style),
            mitre_limit=float(max(self.options.mitre_limit, 0.1))
        )
        combined_shape = combined_shape.simplify(0.3)
        combined_shape = ensure_multi_polygon(combined_shape)

        self.insert_knockdown_elements(combined_shape)

    def insert_knockdown_elements(self, combined_shape):
        first = self.svg.selection.rendering_order()[0]
        try:
            parent = first.getparent()
            index = parent.index(first)
        except AttributeError:
            parent = self.svg
            index = 0
        transform = get_correction_transform(first)

        for polygon in combined_shape.geoms:
            d = str(Path(polygon.exterior.coords))
            if self.options.keep_holes:
                for interior in polygon.interiors:
                    d += str(Path(interior.coords))

            path = PathElement()
            path.set('d', d)
            path.label = self.svg.get_unique_id('Knockdown ')
            path.set('transform', transform)

            path.set('inkstitch:row_spacing_mm', '2.6')
            path.set('inkstitch:fill_underlay_angle', '60 -60')
            path.set('inkstitch:fill_underlay_max_stitch_length_mm', '3')
            path.set('inkstitch:fill_underlay_row_spacing_mm', '2.6')
            path.set('inkstitch:underlay_underpath', 'False')
            path.set('inkstitch:underpath', 'False')
            path.set('inkstitch:staggers', '2')
            path.set('style', 'fill:black;')

            parent.insert(index, path)
