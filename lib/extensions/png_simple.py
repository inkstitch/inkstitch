# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from tempfile import TemporaryDirectory

from inkex.units import convert_unit

from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from ..threads import ThreadCatalog
from ..utils.svg_data import get_pagecolor
from .base import InkstitchExtension
from .utils.inkex_command import inkscape


class PngSimple(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

        self.arg_parser.add_argument('--notebook')
        self.arg_parser.add_argument('--line_width', type=float, default=0.3, dest='line_width')
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

        line_width = convert_unit(f"{self.options.line_width}mm", self.svg.document_unit)
        layer = render_stitch_plan(self.svg, stitch_plan, False, visual_commands=False,
                                   render_jumps=False, line_width=line_width)

        write_png_output(self.svg, layer, self.options.dpi)

        # don't let inkex output the SVG!
        self.skip_output()


def write_png_output(svg, layer, dpi):
    with TemporaryDirectory() as tempdir:
        # Inkex's command functionality also writes files to temp directories like this.
        temp_svg_path = f"{tempdir}/temp.svg"
        temp_png_path = f"{tempdir}/temp.png"
        with open(temp_svg_path, "wb") as f:
            f.write(svg.tostring())

        generate_png(svg, layer, temp_svg_path, temp_png_path, dpi)

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        with open(temp_png_path, 'rb') as output_file:
            sys.stdout.buffer.write(output_file.read())


def generate_png(svg, layer, input_path, output_path, dpi):
    inkscape(input_path, actions="; ".join([
        f"export-id: {layer.get_id()}",
        "export-id-only",
        "export-type:png",
        f"export-dpi: {dpi}",
        f"export-filename: {output_path}",
        f"export-background: {get_pagecolor(svg.namedview)}",
        "export-do"  # Inkscape docs say this should be implicit at the end, but it doesn't seem to be.
    ]))
