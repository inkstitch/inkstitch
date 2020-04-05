import os
import sys
import tempfile
from zipfile import ZipFile

import inkex
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
        self.OptionParser.add_option("-c", "--collapse_len_mm",
                                     action="store", type="float",
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")

        # it's kind of obnoxious that I have to do this...
        self.formats = []
        for format in pyembroidery.supported_formats():
            if 'writer' in format and format['category'] == 'embroidery':
                extension = format['extension']
                mimetype = format['mimetype']
                subtype = mimetype.split("/")[1]
                self.formats.append([extension, mimetype])
                if extension == 'txt':
                    extension = str(extension + "-" + subtype)
                self.OptionParser.add_option('--format-%s' % extension, type="inkbool", dest=subtype)
        self.OptionParser.add_option('--format-svg', type="inkbool", dest='svg')
        # we actually don't need the full mimetype here, so let's skip the +xml
        self.formats.append(['svg', 'image/svg'])

    def effect(self):
        if not self.get_elements():
            return

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches, self.options.collapse_length_mm * PIXELS_PER_MM)
        ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])

        base_file_name = self.get_base_file_name()
        path = tempfile.mkdtemp()

        files = []

        for format in self.formats:
            extension, mimetype = format
            if getattr(self.options, mimetype.split("/")[1]):
                if extension.startswith('txt') and mimetype == "text/plain":
                    colorlist_file_name = base_file_name + "_" + _("colorlist")
                    output_file = os.path.join(path, "%s.%s" % (colorlist_file_name, extension))
                else:
                    output_file = os.path.join(path, "%s.%s" % (base_file_name, extension))
                if not extension == 'svg':
                    file = [output_file, mimetype]
                    write_embroidery_file(file, stitch_plan, self.document.getroot())
                else:
                    output = open(output_file, 'w')
                    output.write(inkex.etree.tostring(self.document.getroot()))
                    output.close()
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
        with open(temp_file.name) as output_file:
            sys.stdout.write(output_file.read())

        os.remove(temp_file.name)
        for file in files:
            os.remove(file)
        os.rmdir(path)

        # don't let inkex output the SVG!
        sys.exit(0)
