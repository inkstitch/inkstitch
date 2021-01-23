import os
import sys
import tempfile
from copy import deepcopy
from zipfile import ZipFile

from inkex import Boolean
from lxml import etree

import pyembroidery

from ..i18n import _
from ..output import write_embroidery_file
from ..stitch_plan import patches_to_stitch_plan
from ..svg import PIXELS_PER_MM
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class Zip(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)
        self.arg_parser.add_argument("-c", "--collapse_len_mm",
                                     action="store", type=float,
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")

        # it's kind of obnoxious that I have to do this...
        self.formats = []
        for format in pyembroidery.supported_formats():
            if 'writer' in format and format['category'] == 'embroidery':
                extension = format['extension']
                self.arg_parser.add_argument('--format-%s' % extension, type=Boolean, dest=extension)
                self.formats.append(extension)
        self.arg_parser.add_argument('--format-svg', type=Boolean, dest='svg')
        self.arg_parser.add_argument('--format-threadlist', type=Boolean, dest='threadlist')
        self.formats.append('svg')
        self.formats.append('threadlist')

    def effect(self):
        if not self.get_elements():
            return

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches, self.options.collapse_length_mm * PIXELS_PER_MM)

        base_file_name = self.get_base_file_name()
        path = tempfile.mkdtemp()

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
                    output = open(output_file, 'w')
                    output.write(self.get_threadlist(stitch_plan, base_file_name))
                    output.close()
                else:
                    write_embroidery_file(output_file, stitch_plan, self.document.getroot())
                files.append(output_file)

        if not files:
            self.errormsg(_("No embroidery file formats selected."))

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
        sys.exit(0)

    def get_threadlist(self, stitch_plan, design_name):
        ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])
        thread_used = []

        thread_output = "%s\n" % _("Design Details")
        thread_output += "==============\n\n"

        thread_output += "%s: %s\n" % (_("Title"), design_name)
        thread_output += "%s (mm): %.2f x %.2f\n" % (_("Size"),  stitch_plan.dimensions_mm[0], stitch_plan.dimensions_mm[1])
        thread_output += "%s: %s\n" % (_("Stitches"), stitch_plan.num_stitches)
        thread_output += "%s: %s\n\n" % (_("Colors"), stitch_plan.num_colors)

        thread_output += "%s\n" % _("Thread Order")
        thread_output += "============\n\n"

        for i, color_block in enumerate(stitch_plan):
            thread = color_block.color

            thread_output += str(i + 1) + " "
            string = "%s #%s - %s (#%s)" % (thread.name, thread.number, thread.manufacturer, thread.hex_digits.lower())
            thread_output += string + "\n"

            thread_used.append(string)

        thread_output += "\n"
        thread_output += _("Thread Used") + "\n"
        thread_output += "============" + "\n\n"

        for thread in set(thread_used):
            thread_output += thread + "\n"

        return "%s" % thread_output
