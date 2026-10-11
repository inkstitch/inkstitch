# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import sqrt
from typing import Literal

from inkex import BaseElement, Boolean, Path, PathElement
from shapely import minimum_bounding_circle, union_all
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

from ..elements import (Clone, EmbroideryElement, FillStitch, SatinColumn,
                        Stroke)
from ..stitches.ripple_stitch import ripple_stitch
from ..stitches.utils.cross_stitch import CrossGeometries
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
        self.arg_parser.add_argument("-j", "--join-style", type=str, default="round", dest="join_style")
        self.arg_parser.add_argument("-m", "--mitre-limit", type=float, default=5.0, dest="mitre_limit")

        self.arg_parser.add_argument("-s", "--shape", type=str, default='', dest="shape")
        self.arg_parser.add_argument("-a", "--simple-shape", type=Boolean, default=False, dest="simple_shape")
        self.arg_parser.add_argument("-f", "--shape-offset", type=float, default=0, dest="shape_offset")
        # TODO: Layer options: underlay, row spacing, angle

    def effect(self) -> None:
        if not self.get_elements():
            return

        polygons = []

        for element in self.elements:
            polygons.extend(self.element_outlines(element))
        combined_shape = union_all(polygons)

        offset_shape = combined_shape
        if not self.options.simple_shape:
            # When users choose to only insert the surrounding embossed shape, we do not want to apply the offset to the original elements
            # otherwise users would have to explicitly set the offset value to 0 in the options tab or
            # calculate their value for the embossing tab, which can be confusing
            offset_shape = self._apply_offset(combined_shape, self.options.offset, self.options.join_style)
            offset_shape = offset_shape.simplify(0.3)

        offset_shape = ensure_multi_polygon(offset_shape)

        self.insert_knockdown_elements(offset_shape)

    def element_outlines(self, element: EmbroideryElement) -> list[BaseGeometry]:
        polygons: list[BaseGeometry] = []
        if isinstance(element, FillStitch):
            polygons.extend(self._fill_polygons(element))
        elif isinstance(element, SatinColumn):
            # plot points on rails, so we get the actual satin size (including pull compensation)
            rail_pairs = zip(*element.plot_points_on_rails(
                0.3,
                element.pull_compensation_px,
                element.pull_compensation_percent / 100)
            )
            rails = []
            for rail in rail_pairs:
                rails.append(LineString(rail))
            polygon = Polygon(list(rails[0].coords) + list(rails[1].reverse().coords)).buffer(0).simplify(0.1)
            polygons.append(polygon)
        elif isinstance(element, Stroke):
            if element.stroke_method == 'ripple_stitch':
                # for ripples this is going to be a bit complicated, so let's follow the stitch plan
                polygons.extend(self._ripple_knockdown(element))
            elif element.stroke_method == 'zigzag_stitch':
                # zigzag stitch depends on the width of the stroke and pull compensation settings
                polygons.append(element.as_multi_line_string().buffer((element.stroke_width + element.pull_compensation) / 2, cap_style='flat'))
            else:
                polygons.append(element.as_multi_line_string().buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
        elif isinstance(element, Clone):
            with element.clone_elements() as elements:
                for clone_child in elements:
                    polygons.extend(self.element_outlines(clone_child))
        return polygons

    def _apply_offset(self, shape: BaseGeometry, offset_mm: float, join_style: Literal['round', 'mitre', 'bevel']) -> BaseGeometry:
        offset = offset_mm * PIXELS_PER_MM
        mitre_limit = float(max(self.options.mitre_limit * PIXELS_PER_MM, 0.1))

        return shape.buffer(distance=offset, join_style=join_style, mitre_limit=mitre_limit, )

    def _fill_polygons(self, element: FillStitch) -> list[BaseGeometry]:
        polygons: list[BaseGeometry] = []
        if element.fill_method == 'cross_stitch':
            # For cross stitch, we want the outline of the grid
            geoms = CrossGeometries(
                element.shape, element.pattern_size, element.fill_coverage, element.cross_stitch_method,
                element.cross_offset, element.canvas_grid_origin, 2
            )
            for box in geoms.boxes:
                # add a small buffer to each box, so adjacing edges connect
                # even when the user hasn't chosen to use an offset
                # (which is likely with cross stitches as they may want to add a running stitch outline)
                polygons.append(box.buffer(0.00001).simplify(0.1))
        else:
            # take expand value into account
            shape = element.shrink_or_grow_shape(element.shape, element.expand)
            # MultiPolygon
            for polygon in shape.geoms:
                polygons.append(polygon)
        return polygons

    def _ripple_knockdown(self, element: Stroke) -> list[BaseGeometry]:
        polygons: list[BaseGeometry] = []
        stitch_groups = ripple_stitch(element)
        for stitches in stitch_groups:
            linestring = LineString(stitches)
            polygons.append(linestring.buffer(0.15 * PIXELS_PER_MM, cap_style='flat'))
        return polygons

    def insert_knockdown_elements(self, combined_shape: MultiPolygon) -> None:
        first = self.elements[0].node
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

    def _insert_embossed_path(self, combined_shape: MultiPolygon, transform: str, parent: BaseElement, index: int) -> None:
        if self.options.shape == 'rect':
            rect = combined_shape.envelope
            offset_shape = self._apply_offset(rect, self.options.shape_offset, "mitre")
        else:
            circle = minimum_bounding_circle(combined_shape)
            offset_shape = self._apply_offset(circle, self.options.shape_offset, "round")

        if isinstance(offset_shape, Polygon):
            # this is always a polygon (buffered circle), but we need to ensure that mypy understands it too
            emboss: Polygon = offset_shape.reverse()
            d = str(Path(emboss.exterior.coords))

            if not self.options.simple_shape:
                for polygon in combined_shape.geoms:
                    d += str(Path(polygon.exterior.coords))
                    d += self._get_hole_paths(polygon)

            self.insert_path(d, transform, parent, index)

    def _insert_knockdown_path(self, combined_shape: MultiPolygon, transform: str, parent: BaseElement, index: int) -> None:
        for polygon in combined_shape.geoms:
            d = str(Path(polygon.exterior.coords))
            d += self._get_hole_paths(polygon)
            self.insert_path(d, transform, parent, index)

    def _get_hole_paths(self, polygon: Polygon) -> str:
        d = ''
        if not self.options.keep_holes:
            return d
        for interior in polygon.interiors:
            d += str(Path(interior.coords))
        return d

    def insert_path(self, d: str, transform: str, parent: BaseElement, index: int) -> None:
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
