# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections.abc import Set

from numpy import sqrt, cbrt
from .color import ThreadColor


def f_xyzn_to_lab(xyzn):
    """Intermediate function for conversion between xyz and lab coordinates"""
    # Reference
    # https://en.wikipedia.org/wiki/CIELAB_color_space#Converting_between_CIELAB_and_CIEXYZ_coordinates
    # https://github.com/gtaylor/python-colormath/blob/master/colormath/color_conversions.py
    # https://github.com/gtaylor/python-colormath/blob/master/colormath/color_constants.py
    CIE_E = (6.0/29.0)**3
    temp = cbrt(xyzn)
    f_lab = [0.0, 0.0, 0.0]
    for i in range(len(xyzn)):
        if xyzn[i] > CIE_E:
            f_lab[i] = temp[i]
        else:
            f_lab[i] = 7.787*xyzn[i] + 16.0/116.0
    return f_lab


def convert_rgb_to_lab(color):
    """Convert sRGB255 to CIELab color"""
    # References
    # Scikit-image documentation
    # https://scikit-image.org/docs/stable/api/skimage.color.html#skimage.color.rgb2lab
    # Wikipedia
    # https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIEXYZ_to_CIELAB
    # https://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright%E2%80%93Guild_data
    # http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    # http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

    # Convert to XYZ and normalize, values from
    # https://github.com/gtaylor/python-colormath/blob/master/colormath/color_objects.py
    xyz = [0, 0, 0]
    xyz[0] = (0.412424*color[0] + 0.357579*color[1] + 0.180464*color[2])/255.0
    xyz[1] = (0.212656*color[0] + 0.715158*color[1] + 0.0721856*color[2])/255.0
    xyz[2] = (0.0193324*color[0] + 0.119193*color[1] + 0.950444*color[2])/255.0

    # scale for transformation, d65 illuminant 2 degree function
    # https://github.com/gtaylor/python-colormath/blob/master/colormath/color_constants.py
    xyzn = [0.95047, 1.0000, 1.08883]
    xyz = [xyz[0]/xyzn[0], xyz[1]/xyzn[1], xyz[2]/xyzn[2]]
    # Intermediate transformation values
    fxyz = f_xyzn_to_lab(xyz)
    return [116.0*fxyz[1] - 16.0, 500.0*(fxyz[0] - fxyz[1]), 200.0*(fxyz[1] - fxyz[2])]


def compare_thread_colors(color1, color2):
    # Textile values from scikit-image documentation
    # https://scikit-image.org/docs/stable/api/skimage.color.html#skimage.color.deltaE_ciede94
    # and Wikipedia
    # https://en.wikipedia.org/wiki/Color_difference#CIE94
    kL = 2
    kC = 1
    kH = 1
    K1 = 0.048
    K2 = 0.014
    deltaL = color1[0] - color2[0]
    C1 = color1[1]**2 + color1[2]**2
    C2 = color2[1]**2 + color2[2]**2
    deltaC = C1 - C2
    deltaa = color1[1] - color2[1]
    deltab = color1[2] - color2[2]
    SL = 1
    SC = 1 + K1*C1
    SH = 1 + K2*C1
    deltaH = sqrt(deltaa**2 + deltab**2 - deltaC**2)
    deltaE = sqrt((deltaL/(kL*SL))**2 + (deltaC/(kC*SC))**2 + (deltaH/(kH*SH))**2)
    return deltaE


class ThreadPalette(Set):
    """Holds a set of ThreadColors all from the same manufacturer."""

    def __init__(self, palette_file):
        self.threads = dict()
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
            line = palette.readline().strip()

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
                    thread_color = [int(field) for field in fields[:3]]
                    thread_name, thread_number = fields[3].strip().rsplit(" ", 1)
                    thread_name = thread_name.strip()

                    thread = ThreadColor(thread_color, thread_name, thread_number, manufacturer=self.name)
                    self.threads[thread] = convert_rgb_to_lab(thread_color)
                except (ValueError, IndexError):
                    continue

    def __contains__(self, thread):
        return thread in self.threads

    def __iter__(self):
        return iter(self.threads)

    def __len__(self):
        return len(self.threads)

    def nearest_color(self, color):
        """Find the thread in this palette that looks the most like the specified color."""

        if isinstance(color, ThreadColor):
            color = color.rgb

        color = convert_rgb_to_lab(color)

        return min(self, key=lambda thread: compare_thread_colors(self.threads[thread], color))
