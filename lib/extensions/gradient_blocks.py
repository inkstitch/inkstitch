# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees, pi

from inkex import (Color, ColorError, DirectedLineSegment, Group,
                   LinearGradient, Path, PathElement, Transform, errormsg)
from shapely import geometry as shgeo
from shapely.affinity import rotate
from shapely.ops import split

from ..elements import FillStitch
from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..svg.tags import INKSTITCH_ATTRIBS
from .base import InkstitchExtension
from .duplicate_params import get_inkstitch_attributes


class GradientBlocks(InkstitchExtension):
    '''
    This will break apart fill objects with a gradient fill into solid color blocks with end_row_spacing.
    '''

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook", type=str, default=0.0)
        self.arg_parser.add_argument("--options", type=str, default=0.0)
        self.arg_parser.add_argument("--info", type=str, default=0.0)
        self.arg_parser.add_argument("-e", "--end-row-spacing", type=float, default=0.0, dest="end_row_spacing")

    def effect(self):
        if not self.svg.selection:
            errormsg(_("Please select at least one object with a gradient fill."))
            return

        if not self.get_elements():
            return

        elements = [element for element in self.elements if isinstance(element, FillStitch) and isinstance(element.gradient, LinearGradient)]
        if not elements:
            errormsg(_("Please select at least one object with a gradient fill."))
            return

        for element in elements:
            parent = element.node.getparent()
            correction_transform = get_correction_transform(element.node)
            style = element.node.style
            index = parent.index(element.node)
            fill_shapes, attributes = gradient_shapes_and_attributes(element, element.shape, self.svg.viewport_to_unit(1))
            # reverse order so we can always insert with the same index number
            fill_shapes.reverse()
            attributes.reverse()

            if self.options.end_row_spacing != 0:
                end_row_spacing = self.options.end_row_spacing
            else:
                end_row_spacing = element.row_spacing / PIXELS_PER_MM * 2
            end_row_spacing = f'{end_row_spacing: .2f}'

            color_block_group = Group()
            color_block_group.label = _("Color Gradient Blocks")
            parent.insert(index, color_block_group)

            for i, shape in enumerate(fill_shapes):
                if shape.area < 15:
                    continue
                color = verify_color(attributes[i]['color'])
                style['fill'] = color
                is_gradient = attributes[i]['is_gradient']
                angle = degrees(attributes[i]['angle'])
                angle = f'{angle: .2f}'
                d = self._element_to_path(shape)
                block = PathElement(attrib={
                    "id": self.uniqueId("path"),
                    "style": str(style),
                    "transform": correction_transform,
                    "d": d,
                    INKSTITCH_ATTRIBS['angle']: angle
                })
                # apply parameters from original element
                params = get_inkstitch_attributes(element.node)
                for attrib in params:
                    block.attrib[attrib] = str(element.node.attrib[attrib])
                # disable underlay and underpath
                block.set('inkstitch:fill_underlay', False)
                block.set('inkstitch:underpath', False)
                # set end_row_spacing
                if is_gradient:
                    block.set('inkstitch:end_row_spacing_mm', end_row_spacing)
                else:
                    block.pop('inkstitch:end_row_spacing_mm')
                    # use underlay to compensate for higher density in the gradient parts
                    block.set('inkstitch:fill_underlay', True)
                    block.set('inkstitch:fill_underlay_angle', angle)
                    block.set('inkstitch:fill_underlay_row_spacing_mm', end_row_spacing)

                color_block_group.append(block)
            element.node.delete()

    def _element_to_path(self, shape):
        coords = list(shape.exterior.coords)
        for interior in shape.interiors:
            coords.extend(interior.coords)
        path = Path(coords)
        path.close()
        return str(path)


def gradient_shapes_and_attributes(element, shape, unit_multiplier):
    # e.g. url(#linearGradient872) -> linearGradient872
    gradient = element.gradient
    gradient.apply_transform()
    # Note: when x and y are given in percentage within the svg file (which can happen in inkscape-non-native-files),
    # gradient returns (0, 0) for both positions and will not render correctly.
    # When the object is moved just once in inkscape, values are updated and this will work again.
    point1 = (gradient.x1(), gradient.y1())
    point2 = (gradient.x2(), gradient.y2())
    # get 90° angle to calculate the splitting angle
    transform = -Transform(get_correction_transform(element.node, child=True))
    line = DirectedLineSegment(transform.apply_to_point(point1), transform.apply_to_point(point2))
    angle = line.angle - (pi / 2)
    # Ink/Stitch somehow turns the stitch angle
    stitch_angle = angle * -1

    # create bbox polygon to calculate the length necessary to make sure that
    # the gradient splitter lines will cut the entire design
    # bounding_box returns the value in viewport units, we need to convert the length later to px
    minx, miny, maxx, maxy = shape.bounds
    bbox_polygon = shgeo.Polygon([(minx, miny), (maxx, miny),
                                  (maxx, maxy), (minx, maxy)])
    # gradient stops
    offsets = gradient.stop_offsets
    stop_styles = gradient.stop_styles
    # now split the shape according to the gradient stops
    polygons = []
    colors = []
    attributes = []
    previous_color = None
    is_gradient = False
    for i, offset in enumerate(offsets):
        shape_rest = []
        split_point = shgeo.Point(line.point_at_ratio(float(offset)))
        import sys
        print(bbox_polygon, split_point, file=sys.stderr)
        length = split_point.hausdorff_distance(bbox_polygon) / unit_multiplier
        split_line = shgeo.LineString([(split_point.x - length - 2, split_point.y),
                                       (split_point.x + length + 2, split_point.y)])
        split_line = rotate(split_line, angle, origin=split_point, use_radians=True)
        offset_line = split_line.parallel_offset(1, 'right')
        polygon = split(shape, split_line)
        color = _get_and_verify_color(stop_styles, gradient, i)
        # does this gradient line split the shape
        offset_outside_shape = len(polygon.geoms) == 1
        for poly in polygon.geoms:
            if isinstance(poly, shgeo.Polygon) and poly.is_valid:
                if poly.intersects(offset_line):
                    if previous_color:
                        polygons.append(poly)
                        colors.append(previous_color)
                        attributes.append({'color': previous_color, 'angle': stitch_angle, 'is_gradient': is_gradient})
                    polygons.append(poly)
                    attributes.append({'color': color, 'angle': stitch_angle + pi, 'is_gradient': is_gradient})
                else:
                    shape_rest.append(poly)
        shape = shgeo.MultiPolygon(shape_rest)
        previous_color = color
        is_gradient = True
    # add left over shape(s)
    if shape:
        if offset_outside_shape:
            for s in shape.geoms:
                polygons.append(s)
                attributes.append({'color': stop_styles[-2]['stop-color'], 'angle': stitch_angle, 'is_gradient': is_gradient})
            stitch_angle += pi
        else:
            is_gradient = False
        for s in shape.geoms:
            polygons.append(s)
            attributes.append({'color': stop_styles[-1]['stop-color'], 'angle': stitch_angle, 'is_gradient': is_gradient})
    return polygons, attributes


def _get_and_verify_color(stop_styles, gradient, iterator):
    try:
        color = verify_color(stop_styles[iterator]['stop-color'])
    except KeyError:
        color = gradient.stops[iterator].get_computed_style('stop-color')
        stop_styles[iterator]['stop-color'] = color
    return color


def verify_color(color):
    try:
        Color(color)
    except ColorError:
        return "black"
    return color


if __name__ == '__main__':
    e = GradientBlocks()
    e.run()
