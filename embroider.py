#!/usr/bin/python
#
# Important resources:
# lxml interface for walking SVG tree:
# http://codespeak.net/lxml/tutorial.html#elementpath
# Inkscape library for extracting paths from SVG:
# http://wiki.inkscape.org/wiki/index.php/Python_modules_for_extensions#simplepath.py
# Shapely computational geometry library:
# http://gispython.org/shapely/manual.html#multipolygons
# Embroidery file format documentation:
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import sys
import traceback
sys.path.append("/usr/share/inkscape/extensions")
import os

import inkex
import inkstitch
from inkstitch import _, PIXELS_PER_MM
from inkstitch.extensions import InkstitchExtension
from inkstitch.stitch_plan import patches_to_stitch_plan
from inkstitch.svg import render_stitch_plan


class Embroider(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)
        self.OptionParser.add_option("-c", "--collapse_len_mm",
                                     action="store", type="float",
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")
        self.OptionParser.add_option("--hide_layers",
                                     action="store", type="choice",
                                     choices=["true", "false"],
                                     dest="hide_layers", default="true",
                                     help="Hide all other layers when the embroidery layer is generated")
        self.OptionParser.add_option("-O", "--output_format",
                                     action="store", type="string",
                                     dest="output_format", default="csv",
                                     help="Output file extenstion (default: csv)")
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")
        self.OptionParser.add_option("-F", "--output-file",
                                     action="store", type="string",
                                     dest="output_file",
                                     help="Output filename.")
        self.OptionParser.add_option("-b", "--max-backups",
                                     action="store", type="int",
                                     dest="max_backups", default=5,
                                     help="Max number of backups of output files to keep.")
        self.OptionParser.usage += _("\n\nSeeing a 'no such option' message?  Please restart Inkscape to fix.")

    def get_output_path(self):
        if self.options.output_file:
            output_path = os.path.join(self.options.path, self.options.output_file)
        else:
            svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")
            csv_filename = svg_filename.replace('.svg', '.%s' % self.options.output_format)
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
        inkstitch.write_embroidery_file(self.get_output_path(), stitch_plan, self.document.getroot())
        render_stitch_plan(self.document.getroot(), stitch_plan)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    e = Embroider()

    try:
        e.affect()
    except KeyboardInterrupt:
        # for use at the command prompt for debugging
        print >> sys.stderr, "interrupted!"
        print >> sys.stderr, traceback.format_exc()
