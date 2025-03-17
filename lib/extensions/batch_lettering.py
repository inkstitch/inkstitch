# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import sys
import tempfile
from copy import deepcopy
from zipfile import ZipFile

from inkex import Boolean, Group, errormsg
from lxml import etree

import pyembroidery

from ..extensions.lettering_along_path import TextAlongPath
from ..i18n import _
from ..lettering import get_font_by_id
from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import get_correction_transform
from ..threads import ThreadCatalog
from ..utils import DotDict
from .base import InkstitchExtension


class BatchLettering(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

        self.arg_parser.add_argument('--notebook')

        self.arg_parser.add_argument('--text', type=str, default='', dest='text')
        self.arg_parser.add_argument('--separator', type=str, default='', dest='separator')

        self.arg_parser.add_argument('--font', type=str, default='', dest='font')
        self.arg_parser.add_argument('--scale', type=int, default=100, dest='scale')
        self.arg_parser.add_argument('--color-sort', type=str, default='off', dest='color_sort')
        self.arg_parser.add_argument('--trim', type=str, default='off', dest='trim')
        self.arg_parser.add_argument('--use-command-symbols', type=Boolean, default=False, dest='command_symbols')
        self.arg_parser.add_argument('--text-align', type=str, default='left', dest='text_align')

        self.arg_parser.add_argument('--text-position', type=str, default='left', dest='text_position')

        self.arg_parser.add_argument('--file-formats', type=str, default='', dest='formats')

    def effect(self):
        separator = self.options.separator
        if not separator:
            separator = '\\n'
        text_input = self.options.text
        if not text_input:
            errormsg(_("Please specify a text"))
            return
        texts = text_input.split(separator)

        if not self.options.font:
            errormsg(_("Please specify a font"))
            return
        self.font = get_font_by_id(self.options.font)
        if self.font is None:
            errormsg(_("Please specify a valid font folder name"))
            return

        if not self.options.formats:
            errormsg(_("Please specify at least one output file format"))
            return
        available_formats = [file_format['extension'] for file_format in pyembroidery.supported_formats()] + ['svg']
        file_formats = self.options.formats.split(',')
        file_formats = [file_format.strip().lower() for file_format in file_formats if file_format.strip().lower() in available_formats]
        if not file_formats:
            errormsg(_("Please specify at least one file format supported by pyembroidery"))
            return

        self.setup_trim()
        self.setup_text_align()
        self.setup_color_sort()
        self.setup_scale()

        self.generate_output_files(texts, file_formats)

        # don't let inkex output the SVG!
        sys.exit(0)

    def setup_trim(self):
        self.trim = 0
        if self.options.trim == "line":
            self.trim = 1
        elif self.options.trim == "word":
            self.trim = 2
        elif self.options.trim == "glyph":
            self.trim = 3

    def setup_text_align(self):
        self.text_align = 0
        if self.options.text_align == "center":
            self.text_align = 1
        elif self.options.text_align == "right":
            self.text_align = 2
        elif self.options.text_align == "block":
            self.text_align = 3
        elif self.options.text_align == "letterspacing":
            self.text_align = 4

    def setup_color_sort(self):
        self.color_sort = 0
        if self.options.color_sort == "all":
            self.color_sort = 1
        elif self.options.color_sort == "line":
            self.color_sort = 2
        elif self.options.color_sort == "word":
            self.color_sort = 3

    def setup_scale(self):
        self.scale = self.options.scale / 100
        if self.font.min_scale > self.scale or self.scale > self.font.max_scale:
            self.scale = 1

    def generate_output_files(self, texts, file_formats):
        self.metadata = self.get_inkstitch_metadata()
        self.collapse_len = self.metadata['collapse_len_mm']
        self.min_stitch_len = self.metadata['min_stitch_len_mm']

        # The user can specify a frame to adapt the position of the text or influence it's scaling
        # if the path is a closed path it will try to adapt the width of the text (if the scaling input was 0) or simply use it for text positioning
        # if it is an open path, it will use the text along path method
        text_positioning_path = self.svg.findone(".//*[@inkscape:label='batch lettering']")

        path = tempfile.mkdtemp()
        files = []
        for text in texts:
            for file_format in file_formats:
                files.append(self.generate_text_file(path, text, text_positioning_path, file_format))

        temp_file = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

        # in windows, failure to close here will keep the file locked
        temp_file.close()

        with ZipFile(temp_file.name, "w") as zip_file:
            for output in files:
                zip_file.write(output, os.path.basename(output))

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        with open(temp_file.name, 'rb') as output_file:
            sys.stdout.buffer.write(output_file.read())

        os.remove(temp_file.name)
        for output in files:
            os.remove(output)
        os.rmdir(path)

    def generate_text_file(self, path, text, text_positioning_path, file_format):
        output_file = os.path.join(path, f"{text}.{file_format}")

        self.settings = DotDict({
            "text": text,
            "text_align": self.text_align,
            "back_and_forth": True,
            "font": self.font.marked_custom_font_id,
            "scale": self.scale * 100,
            "trim_option": self.trim,
            "use_trim_symbols": self.options.command_symbols,
            "color_sort": self.color_sort
        })

        lettering_group = Group()
        lettering_group.label = _("Ink/Stitch Lettering")
        lettering_group.set('inkstitch:lettering', json.dumps(self.settings))
        self.svg.append(lettering_group)
        lettering_group.set("transform", get_correction_transform(lettering_group, child=True))

        destination_group = Group()
        destination_group.label = f"{self.font.name} {_('scale')} {self.scale * 100}%"
        lettering_group.append(destination_group)

        text = self.font.render_text(
            text,
            destination_group,
            trim_option=self.trim,
            use_trim_symbols=self.options.command_symbols,
            color_sort=self.color_sort,
            text_align=self.text_align
        )

        destination_group.attrib['transform'] = f'scale({self.scale})'

        if text_positioning_path is not None:
            parent = text_positioning_path.getparent()
            index = parent.index(text_positioning_path)
            parent.insert(index, lettering_group)
            TextAlongPath(self.svg, lettering_group, text_positioning_path, self.options.text_position)
            parent.remove(text_positioning_path)

        if file_format == 'svg':
            document = deepcopy(self.document.getroot())
            with open(output_file, 'w', encoding='utf-8') as svg:
                svg.write(etree.tostring(document).decode('utf-8'))
        else:
            self.get_elements()
            stitch_groups = self.elements_to_stitch_groups(self.elements)
            stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=self.collapse_len, min_stitch_len=self.min_stitch_len)
            ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])
            write_embroidery_file(output_file, stitch_plan, self.document.getroot())

        # reset document for the next iteration
        if text_positioning_path is not None:
            parent.insert(index, text_positioning_path)
        lettering_group.getparent().remove(lettering_group)

        return output_file


if __name__ == '__main__':
    BatchLettering().run()
