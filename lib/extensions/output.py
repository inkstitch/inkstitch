import sys
import traceback
import os
import inkex
import tempfile

from .base import InkstitchExtension
from ..i18n import _
from ..output import write_embroidery_file
from ..stitch_plan import patches_to_stitch_plan
from ..svg import render_stitch_plan, PIXELS_PER_MM
from ..utils.io import save_stdout

class Output(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)
        self.OptionParser.add_option("-c", "--collapse_len_mm",
                                     action="store", type="float",
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")
        self.OptionParser.add_option("-f", "--format",
                                     dest="file_extension",
                                     help="file extension to output (example: DST)")

    def effect(self):
        if not self.get_elements():
            return

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches, self.options.collapse_length_mm * PIXELS_PER_MM)

        temp_file = tempfile.NamedTemporaryFile(suffix=".%s" % self.options.file_extension, delete=False)

        # in windows, failure to close here will keep the file locked
        temp_file.close()

        write_embroidery_file(temp_file.name, stitch_plan, self.document.getroot())

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        with open(temp_file.name) as output_file:
            sys.stdout.write(output_file.read())

        # clean up the temp file
        os.remove(temp_file.name)

        # don't let inkex output the SVG!
        sys.exit(0)
