import os

from inkex import Boolean

from ..i18n import _
from ..output import write_embroidery_file
from ..stitch_plan import patches_to_stitch_plan
from ..svg import PIXELS_PER_MM, render_stitch_plan
from .base import InkstitchExtension


class Embroider(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-c", "--collapse_len_mm",
                                     action="store", type=float,
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")
        self.arg_parser.add_argument("--hide_layers",
                                     action="store", type=Boolean,
                                     dest="hide_layers", default="true",
                                     help="Hide all other layers when the embroidery layer is generated")
        self.arg_parser.add_argument("-O", "--output_format",
                                     action="store", type=str,
                                     dest="output_format", default="csv",
                                     help="Output file extenstion (default: csv)")
        self.arg_parser.add_argument("-P", "--path",
                                     action="store", type=str,
                                     dest="path", default=".",
                                     help="Directory in which to store output file")
        self.arg_parser.add_argument("-F", "--output-file",
                                     action="store", type=str,
                                     dest="output_file",
                                     help="Output filename.")
        self.arg_parser.add_argument("-b", "--max-backups",
                                     action="store", type=int,
                                     dest="max_backups", default=5,
                                     help="Max number of backups of output files to keep.")
        if not self.arg_parser.usage:
            self.arg_parser.usage = ""
        self.arg_parser.usage += _("\n\nSeeing a 'no such option' message?  Please restart Inkscape to fix.")

    def get_output_path(self):
        if self.options.output_file:
            # This is helpful for folks that run the embroider extension
            # manually from the command line (without Inkscape) for
            # debugging purposes.
            output_path = os.path.join(os.path.expanduser(os.path.expandvars(self.options.path)),
                                       self.options.output_file)
        else:
            csv_filename = '%s.%s' % (self.get_base_file_name(), self.options.output_format)
            output_path = os.path.join(self.options.path, csv_filename)

        def add_suffix(path, suffix):
            if suffix > 0:
                path = "%s.%s" % (path, suffix)

            return path

        def move_if_exists(path, suffix=0):
            source = add_suffix(path, suffix)

            if suffix >= self.options.max_backups:
                return

            dest = add_suffix(path, suffix + 1)

            if os.path.exists(source):
                move_if_exists(path, suffix + 1)

                if os.path.exists(dest):
                    os.remove(dest)

                os.rename(source, dest)

        move_if_exists(output_path)

        return output_path

    def effect(self):
        if not self.get_elements():
            return

        if self.options.hide_layers:
            self.hide_all_layers()

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches, self.options.collapse_length_mm * PIXELS_PER_MM)
        write_embroidery_file(self.get_output_path(), stitch_plan, self.document.getroot())
        render_stitch_plan(self.document.getroot(), stitch_plan)
