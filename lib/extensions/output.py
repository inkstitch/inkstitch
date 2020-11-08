import os
import sys
import tempfile

from ..output import write_embroidery_file
from ..stitch_plan import patches_to_stitch_plan
from .base import InkstitchExtension


class Output(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)

    def parse_arguments(self, args=sys.argv[1:]):
        # inkex's option parsing can't handle arbitrary command line arguments
        # that may be passed for a given output format, so we'll just parse the
        # args ourselves. :P
        self.settings = {}
        extra_args = []
        for arg in args:
            if arg.startswith('--') and not arg.startswith('--id='):
                name, value = arg[2:].split('=')

                try:
                    value = float(value)
                except ValueError:
                    try:
                        value = {
                            "true": True,
                            "false": False
                        }[value]
                    except (KeyError):
                        pass

                self.settings[name] = value
            else:
                extra_args.append(arg)

        self.file_extension = self.settings.pop('format')
        del sys.argv[1:]

        InkstitchExtension.parse_arguments(self, extra_args)

    def effect(self):
        if not self.get_elements():
            return

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches, disable_ties=self.settings.get('laser_mode', False))

        temp_file = tempfile.NamedTemporaryFile(suffix=".%s" % self.file_extension, delete=False)

        # in windows, failure to close here will keep the file locked
        temp_file.close()

        write_embroidery_file(temp_file.name, stitch_plan, self.document.getroot(), self.settings)

        if sys.platform == "win32":
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        with open(temp_file.name, "rb") as output_file:
            sys.stdout.buffer.write(output_file.read())
            sys.stdout.flush()

        # clean up the temp file
        os.remove(temp_file.name)

        # don't let inkex output the SVG!
        sys.exit(0)
