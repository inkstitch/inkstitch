# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from ..threads import ThreadCatalog
from .base import InkstitchExtension
from .png_simple import write_png_output


class PngRealistic(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

        self.arg_parser.add_argument('--notebook')
        self.arg_parser.add_argument('--dpi', type=int, default=300, dest='dpi')

    def effect(self):
        if not self.get_elements():
            return

        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)
        ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])

        layer = render_stitch_plan(self.svg, stitch_plan, True, visual_commands=False, render_jumps=False)

        write_png_output(self.svg, layer, self.options.dpi)

        # don't let inkex output the SVG!
        self.skip_output()
