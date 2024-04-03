# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..commands import add_layer_commands
from ..i18n import _
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL
from .base import InkstitchExtension


class DisplayStackingOrder(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-s", "--font_size", type=int, default=4, dest="font_size")

    def effect(self):
        layer = self.create_layer()

        nodes = self.get_nodes()
        for i, node in enumerate(nodes):
            if node.style['fill'] != 'none':
                position = node.bounding_box(node.composed_transform()).minimum
                self.insert_stacking_num(layer, i + 1, position)
            else:
                path = node.get_path().transform(node.composed_transform())
                position = next(path.end_points)
                self.insert_stacking_num(layer, i + 1, position)

        add_layer_commands(layer, ["ignore_layer"])

        # remove layer if empty
        if len(layer) == 0:
            self.svg.remove(layer)

    def insert_stacking_num(self, layer, num, position):
        text = inkex.TextElement(attrib={
            'x': str(position[0]),
            'y': str(position[1])
        })
        text.style = inkex.Style(f"text-anchor: middle;text-align: center;dominant-baseline: middle;font-size: { self.options.font_size }")
        tspan = inkex.Tspan()
        tspan.text = str(num)
        text.add(tspan)
        layer.add(text)

    def create_layer(self):
        layer = self.svg.find(".//*[@id='__inkstitch_stacking_order__']")

        # Remove the existing layer
        if layer is not None:
            layer.getparent().remove(layer)

        layer = inkex.Group(attrib={
            'id': '__inkstitch_stacking_order__',
            INKSCAPE_LABEL: _('Stacking Order'),
            INKSCAPE_GROUPMODE: 'layer',
        })
        self.svg.append(layer)

        return layer
