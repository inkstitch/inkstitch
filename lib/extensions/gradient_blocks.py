# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees

from inkex import DirectedLineSegment, PathElement, errormsg
from shapely.geometry import Point
from shapely.ops import nearest_points

from ..commands import add_commands
from ..elements import FillStitch
from ..elements.gradient_fill import gradient_shapes_and_attributes
from ..i18n import _
from ..svg import get_correction_transform
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

            previous_color = None
            previous_element = None
            for i, shape in enumerate(fill_shapes):
                color = attributes[i]['color']
                style['fill'] = color
                end_row_spacing = attributes[i]['end_row_spacing'] or None
                angle = degrees(attributes[i]['angle'])
                d = "M " + " ".join([f'{x}, {y}' for x, y in list(shape.exterior.coords)]) + " Z"
                block = PathElement(attrib={
                    "id": self.uniqueId("path"),
                    "style": str(style),
                    "transform": correction_transform,
                    "d": d,
                    INKSTITCH_ATTRIBS['angle']: f'{angle: .2f}'
                })
                # apply parameters from original element
                params = get_inkstitch_attributes(element.node)
                for attrib in params:
                    block.attrib[attrib] = str(element.node.attrib[attrib])
                # set end_row_spacing
                if end_row_spacing:
                    if self.options.end_row_spacing != 0:
                        end_row_spacing = self.options.end_row_spacing
                    block.set('inkstitch:end_row_spacing_mm', f'{end_row_spacing: .2f}')
                else:
                    block.pop('inkstitch:end_row_spacing_mm')
                # disable underlay and underpath
                block.set('inkstitch:fill_underlay', False)
                block.set('inkstitch:underpath', False)
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


if __name__ == '__main__':
    e = GradientBlocks()
    e.effect()
