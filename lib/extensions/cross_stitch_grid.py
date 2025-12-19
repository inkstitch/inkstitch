# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import sqrt

from inkex import Boolean, Color, Grid

from .base import InkstitchExtension


class CrossStitchGrid(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-s", "--stitch_length", dest="stitch_length", type=float, default=3)
        self.arg_parser.add_argument("-c", "--color", dest="color", type=Color, default=Color(0x00d9e5ff))
        self.arg_parser.add_argument("-d", "--delete", dest="remove_previous", type=Boolean, default=True)

    def effect(self):
        namedview = self.svg.namedview

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
        grid_spacing = self.options.stitch_length / sqrt(2)
        grid = Grid(attrib={
            "id": grid_id,
            "units": "mm",
            "originx": "0",
            "originy": "0",
            "spacingx": str(grid_spacing),
            "spacingy": str(grid_spacing),
            "empcolor": str(self.options.color),
            "empopacity": "0.30196078",
            "color": str(self.options.color),
            "opacity": "0.14901961",
            "empspacing": "1",
            "enabled": "true",
            "visible": "true",
        })
        namedview.append(grid)
