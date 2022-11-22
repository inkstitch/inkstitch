# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees

from inkex import PathElement, errormsg

from ..elements import FillStitch
from ..elements.gradient_fill import gradient_shapes_and_attributes
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import INKSTITCH_ATTRIBS
from .base import InkstitchExtension


class GradientBlocks(InkstitchExtension):
    '''
    This will break apart fill objects with a gradient fill into solid color blocks with end_row_spacing.
    '''

    def effect(self):
        if not self.svg.selection:
            errormsg(_("Please select at least one object with a gradient fill."))
            return

        if not self.get_elements():
            return

        elements = [element for element in self.elements if (isinstance(element, FillStitch) and element.has_gradient_color())]
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
            for i, shape in enumerate(fill_shapes):
                style['fill'] = attributes[i]['color']
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
                if end_row_spacing:
                    block.set('inkstitch:end_row_spacing_mm', f'{end_row_spacing: .2f}')
                    block.set('inkstitch:underpath', False)
                parent.insert(index, block)
            parent.remove(element.node)


if __name__ == '__main__':
    e = GradientBlocks()
    e.effect()
