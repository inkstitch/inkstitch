# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import sqrt

from inkex import Boolean, Color, Grid
from inkex.units import convert_unit

from .base import InkstitchExtension


class CrossStitchGrid(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-x", "--box_size_x", dest="box_size_x", type=float, default=3)
        self.arg_parser.add_argument("-y", "--box_size_y", dest="box_size_y", type=float, default=3)
        self.arg_parser.add_argument("-c", "--color", dest="color", type=Color, default=Color(0x00d9e5ff))
        self.arg_parser.add_argument("-d", "--delete", dest="remove_previous", type=Boolean, default=True)

    def effect(self):
        namedview = self.svg.namedview
        unit = self.svg.document_unit

        # hide old grids
        grids = self.svg.findall('.//inkscape:grid')
        for grid in grids:
            if grid.get_id().startswith("inkstitch_cross_stitch_grid_"):
                if self.options.remove_previous:
                    grid.delete()
            else:
                grid.set("enabled", "false")

        grid_id = self.svg.get_unique_id("inkstitch_cross_stitch_grid_")

        # insert new grid
        scale = self.svg.inkscape_scale
        box_size_x = self.options.box_size_x / sqrt(2) / scale
        box_size_x = convert_unit(f'{box_size_x}mm', unit)
        box_size_y = self.options.box_size_y / sqrt(2) / scale
        box_size_y = convert_unit(f'{box_size_y}mm', unit)
        grid = Grid(attrib={
            "id": grid_id,
            "units": unit,
            "originx": "0",
            "originy": "0",
            "spacingx": str(box_size_x),
            "spacingy": str(box_size_y),
            "empcolor": str(self.options.color),
            "empopacity": "0.30196078",
            "color": str(self.options.color),
            "opacity": "0.14901961",
            "empspacing": "1",
            "enabled": "true",
            "visible": "true",
        })
        namedview.append(grid)
