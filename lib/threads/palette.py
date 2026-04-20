# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections.abc import Set

from colormath2.color_conversions import convert_color
from colormath2.color_diff import delta_e_cie1994
from colormath2.color_objects import LabColor, sRGBColor

from .color import ThreadColor


def compare_thread_colors(color1, color2):
    # K_L=2 indicates textiles
    return delta_e_cie1994(color1, color2, K_L=2)


class ThreadPalette(Set):
    """Holds a set of ThreadColors all from the same manufacturer."""

    def __init__(self, palette_file):
        self.threads = dict()
        self._lab_colors = None
        self.parse_palette_file(palette_file)

    def parse_palette_file(self, palette_file):
        """Read a GIMP palette file and load thread colors.

        Example file:

        GIMP Palette
        Name: Ink/Stitch: Metro
        Columns: 4
        # RGB Value                                 Color Name Number
        240     186     212                         Sugar Pink   1624
        237     171     194                           Carnatio   1636

        """

        with open(palette_file, encoding='utf8') as palette:
            try:
                line = palette.readline().strip()
            except UnicodeDecodeError:
                # File has wrong encoding. Can't read this file
                self.is_gimp_palette = False
                return

            self.is_gimp_palette = True
            if line.lower() != "gimp palette":
                self.is_gimp_palette = False
                return

            self.name = palette.readline().strip()
            if self.name.lower().startswith('name: ink/stitch: '):
                self.name = self.name[18:]

            # number of columns
            palette.readline()

            # headers
            palette.readline()

            for line in palette:
                try:
                    fields = line.split(None, 3)
                    thread_color = (int(fields[0]), int(fields[1]), int(fields[2]))
                    thread_name, thread_number = fields[3].strip().rsplit(" ", 1)
                    thread_name = thread_name.strip()

                    thread = ThreadColor.__new__(ThreadColor)
                    thread.rgb = thread_color
                    thread.name = thread_name
                    thread.number = thread_number
                    thread.manufacturer = self.name
                    thread.description = thread_name
                    thread.chart = None
                    self.threads[thread] = thread_color
                except (ValueError, IndexError):
                    continue

    def __contains__(self, thread):
        return thread in self.threads

    def __iter__(self):
        return iter(self.threads)

    def __len__(self):
        return len(self.threads)

    def _ensure_lab_colors(self):
        if self._lab_colors is None:
            self._lab_colors = {
                thread: convert_color(sRGBColor(*rgb, is_upscaled=True), LabColor)
                for thread, rgb in self.threads.items()
            }

    def nearest_color(self, color):
        """Find the thread in this palette that looks the most like the specified color."""

        if isinstance(color, ThreadColor):
            color = color.rgb

        self._ensure_lab_colors()
        assert self._lab_colors is not None
        lab_colors = self._lab_colors
        color = convert_color(sRGBColor(*color, is_upscaled=True), LabColor)

        return min(self, key=lambda thread: compare_thread_colors(lab_colors[thread], color))
