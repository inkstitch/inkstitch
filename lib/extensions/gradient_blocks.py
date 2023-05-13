# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees, pi

from inkex import DirectedLineSegment, PathElement, Transform, errormsg
from shapely import geometry as shgeo
from shapely.affinity import affine_transform, rotate
from shapely.geometry import Point
from shapely.ops import nearest_points, split

from ..commands import add_commands
from ..elements import FillStitch
from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..svg.tags import INKSTITCH_ATTRIBS
from .commands import CommandsExtension
from .duplicate_params import get_inkstitch_attributes


class GradientBlocks(CommandsExtension):
    '''
    This will break apart fill objects with a gradient fill into solid color blocks with end_row_spacing.
    '''

    COMMANDS = ['fill_start', 'fill_end']

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)
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

        elements = [element for element in self.elements if (isinstance(element, FillStitch) and self.has_gradient_color(element))]
        if not elements:
            errormsg(_("Please select at least one object with a gradient fill."))
            return

        for element in elements:
            parent = element.node.getparent()
            correction_transform = get_correction_transform(element.node)
            style = element.node.style
            index = parent.index(element.node)
            fill_shapes, attributes = gradient_shapes_and_attributes(element, element.shape)
            # reverse order so we can always insert with the same index number
            fill_shapes.reverse()
            attributes.reverse()

            if self.options.end_row_spacing != 0:
                end_row_spacing = self.options.end_row_spacing
            else:
                end_row_spacing = element.row_spacing / PIXELS_PER_MM * 2
            end_row_spacing = f'{end_row_spacing: .2f}'

            previous_color = None
            previous_element = None
            for i, shape in enumerate(fill_shapes):
                color = attributes[i]['color']
                style['fill'] = color
                is_gradient = attributes[i]['is_gradient']
                angle = degrees(attributes[i]['angle'])
                angle = f'{angle: .2f}'
                d = "M " + " ".join([f'{x}, {y}' for x, y in list(shape.exterior.coords)]) + " Z"
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

                parent.insert(index, block)

                if previous_color == color:
                    current = FillStitch(block)
                    previous = FillStitch(previous_element)
                    nearest = nearest_points(current.shape, previous.shape)
                    pos_current = self._get_command_postion(current, nearest[0])
                    pos_previous = self._get_command_postion(previous, nearest[1])
                    add_commands(current, ['fill_end'], pos_current)
                    add_commands(previous, ['fill_start'], pos_previous)
                previous_color = color
                previous_element = block
            parent.remove(element.node)

    def has_gradient_color(self, element):
        return element.color.startswith('url') and "linearGradient" in element.color

    def _get_command_postion(self, fill, point):
        center = fill.shape.centroid
        line = DirectedLineSegment((center.x, center.y), (point.x, point.y))
        pos = line.point_at_length(line.length + 20)
        return Point(pos)


def gradient_shapes_and_attributes(element, shape):
    # e.g. url(#linearGradient872) -> linearGradient872
    color = element.color[5:-1]
    xpath = f'.//svg:defs/svg:linearGradient[@id="{color}"]'
    gradient = element.node.getroottree().getroot().findone(xpath)
    gradient.apply_transform()
    point1 = (float(gradient.get('x1')), float(gradient.get('y1')))
    point2 = (float(gradient.get('x2')), float(gradient.get('y2')))
    # get 90° angle to calculate the splitting angle
    line = DirectedLineSegment(point1, point2)
    angle = line.angle - (pi / 2)
    # Ink/Stitch somehow turns the stitch angle
    stitch_angle = angle * -1
    # create bbox polygon to calculate the length necessary to make sure that
    # the gradient splitter lines will cut the entire design
    bbox = element.node.bounding_box()
    bbox_polygon = shgeo.Polygon([(bbox.left, bbox.top), (bbox.right, bbox.top),
                                  (bbox.right, bbox.bottom), (bbox.left, bbox.bottom)])
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
        length = split_point.hausdorff_distance(bbox_polygon)
        split_line = shgeo.LineString([(split_point.x - length - 2, split_point.y),
                                       (split_point.x + length + 2, split_point.y)])
        split_line = rotate(split_line, angle, origin=split_point, use_radians=True)
        transform = -Transform(get_correction_transform(element.node))
        transform = list(transform.to_hexad())
        split_line = affine_transform(split_line, transform)
        offset_line = split_line.parallel_offset(1, 'right')
        polygon = split(shape, split_line)
        color = stop_styles[i]['stop-color']
        # does this gradient line split the shape
        offset_outside_shape = len(polygon.geoms) == 1
        for poly in polygon.geoms:
            if isinstance(poly, shgeo.Polygon) and element.shape_is_valid(poly):
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


if __name__ == '__main__':
    e = GradientBlocks()
    e.effect()
