# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
import tempfile
from copy import deepcopy
from zipfile import ZipFile

from inkex import Boolean, errormsg
from inkex.units import convert_unit
from lxml import etree

import pystitch

from ..i18n import _
from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..threads import ThreadCatalog
from ..utils.geometry import Point
from .base import InkstitchExtension
from .png_simple import generate_png
from .thread_list import get_threadlist


class Zip(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

        self.arg_parser.add_argument('--notebook')
        self.arg_parser.add_argument('--custom-file-name', type=str, default='', dest='custom_file_name')

        # it's kind of obnoxious that I have to do this...
        self.formats = []
        for format in pystitch.supported_formats():
            if 'writer' in format and format['category'] in ['embroidery', 'color', 'image', 'stitch', 'quilting']:
                extension = format['extension']
                self.arg_parser.add_argument('--format-%s' % extension, type=Boolean, default=False, dest=extension)
                self.formats.append(extension)
        self.arg_parser.add_argument('--format-svg', type=Boolean, default=False, dest='svg')
        self.formats.append('svg')
        self.arg_parser.add_argument('--format-threadlist', type=Boolean, default=False, dest='threadlist')
        self.formats.append('threadlist')
        self.arg_parser.add_argument('--format-png-realistic', type=Boolean, default=False, dest='png_realistic')
        self.arg_parser.add_argument('--dpi-realistic', type=int, default=300, dest='dpi_realistic')
        self.formats.append('png_realistic')
        self.arg_parser.add_argument('--format-png-simple', type=Boolean, default=False, dest='png_simple')
        self.arg_parser.add_argument('--png-simple-line-width', type=float, default=0.3, dest='line_width')
        self.arg_parser.add_argument('--dpi-simple', type=int, default=300, dest='dpi_simple')
        self.formats.append('png_simple')

        self.arg_parser.add_argument('--x-repeats', type=int, default=1, dest='x_repeats', )
        self.arg_parser.add_argument('--y-repeats', type=int, default=1, dest='y_repeats',)
        self.arg_parser.add_argument('--x-spacing', type=float, default=100, dest='x_spacing')
        self.arg_parser.add_argument('--y-spacing', type=float, default=100, dest='y_spacing',)

    def effect(self):
        if not self.get_elements():
            return

        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)
        ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])

        if self.options.x_repeats != 1 or self.options.y_repeats != 1:
            stitch_plan = self._make_offsets(stitch_plan)

        base_file_name = self._get_file_name()
        path = tempfile.mkdtemp()

        files = self.generate_output_files(stitch_plan, path, base_file_name)

        if not files:
            errormsg(_("No embroidery file formats selected."))

        temp_file = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

        # in windows, failure to close here will keep the file locked
        temp_file.close()

        with ZipFile(temp_file.name, "w") as zip_file:
            for file in files:
                zip_file.write(file, os.path.basename(file))

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        with open(temp_file.name, 'rb') as output_file:
            sys.stdout.buffer.write(output_file.read())

        os.remove(temp_file.name)
        for file in files:
            os.remove(file)
        os.rmdir(path)

        # don't let inkex output the SVG!
        self.skip_output()

    def _get_file_name(self):
        if self.options.custom_file_name:
            base_file_name = self.options.custom_file_name
        else:
            base_file_name = self.get_base_file_name()
        return base_file_name

    def _make_offsets(self, stitch_plan):
        dx = self.options.x_spacing * PIXELS_PER_MM
        dy = self.options.y_spacing * PIXELS_PER_MM
        offsets = []
        for x in range(self.options.x_repeats):
            for y in range(self.options.y_repeats):
                offsets.append(Point(x * dx, y * dy))
        return stitch_plan.make_offsets(offsets)

    def generate_output_files(self, stitch_plan, path, base_file_name):
        files = []
        for format in self.formats:
            if getattr(self.options, format):
                output_file = os.path.join(path, "%s.%s" % (base_file_name, format))
                if format == 'svg':
                    document = deepcopy(self.document.getroot())
                    with open(output_file, 'w', encoding='utf-8') as svg:
                        svg.write(etree.tostring(document).decode('utf-8'))
                elif format == 'threadlist':
                    output_file = os.path.join(path, "%s_%s.txt" % (base_file_name, _("threadlist")))
                    with open(output_file, 'w', encoding='utf-8') as output:
                        output.write(get_threadlist(stitch_plan, base_file_name))
                elif format == 'png_realistic':
                    output_file = os.path.join(path, f"{base_file_name}_realistic.png")
                    layer = render_stitch_plan(self.svg, stitch_plan, True, visual_commands=False, render_jumps=False)
                    self.generate_png_output(output_file, layer, self.options.dpi_realistic)
                elif format == 'png_simple':
                    output_file = os.path.join(path, f"{base_file_name}_simple.png")
                    line_width = convert_unit(f"{self.options.line_width}mm", self.svg.document_unit)
                    layer = render_stitch_plan(self.svg, stitch_plan, False, visual_commands=False,
                                               render_jumps=False, line_width=line_width)
                    self.generate_png_output(output_file, layer, self.options.dpi_simple)
                else:
                    write_embroidery_file(output_file, stitch_plan, self.document.getroot())
                files.append(output_file)
        return files

    def generate_png_output(self, output_file, layer, dpi):
        with tempfile.TemporaryDirectory() as tempdir:
            temp_svg_path = f"{tempdir}/temp.svg"
            with open(temp_svg_path, "wb") as f:
                f.write(self.svg.tostring())
            generate_png(self.svg, layer, temp_svg_path, output_file, dpi)
