import os
import sys
from collections.abc import Sequence
from glob import glob
from os.path import dirname, realpath

from ..utils import guess_inkscape_config_path
from .palette import ThreadPalette


class _ThreadCatalog(Sequence):
    """Holds a set of ThreadPalettes."""

    def __init__(self):
        self.palettes = []
        self.load_palettes(self.get_palettes_paths())

    def get_palettes_paths(self):
        """Creates a list containing the path of two directories:
        1. Palette directory of Inkscape
        2. Palette directory of inkstitch
        """
        path = [os.path.join(guess_inkscape_config_path(), 'palettes')]

        if getattr(sys, 'frozen', None) is not None:
            inkstitch_path = os.path.join(sys._MEIPASS, "..")
        else:
            inkstitch_path = dirname(dirname(dirname(realpath(__file__))))

        path.append(os.path.join(inkstitch_path, 'palettes'))

        return path

    def load_palettes(self, paths):
        palettes = []
        for path in paths:
            for palette_file in glob(os.path.join(path, 'InkStitch*.gpl')):
                palette_basename = os.path.basename(palette_file)
                if palette_basename not in palettes:
                    self.palettes.append(ThreadPalette(palette_file))
                    palettes.append(palette_basename)

    def palette_names(self):
        return list(sorted(palette.name for palette in self))

    def __getitem__(self, item):
        return self.palettes[item]

    def __len__(self):
        return len(self.palettes)

    def _num_exact_color_matches(self, palette, threads):
        """Number of colors in stitch plan with an exact match in this palette."""

        return sum(1 for thread in threads if thread in palette)

    def match_and_apply_palette(self, stitch_plan, palette=None):
        if palette is None:
            palette = self.match_palette(stitch_plan)
        else:
            palette = self.get_palette_by_name(palette)

        if palette is not None:
            self.apply_palette(stitch_plan, palette)

        return palette

    def match_palette(self, stitch_plan):
        """Figure out which color palette was used

        Scans the catalog of color palettes and chooses one that seems most
        likely to be the one that the user used.  A palette will only be
        chosen if more tha 80% of the thread colors in the stitch plan are
        exact matches for threads in the palette.
        """
        if not self.palettes:
            return None

        threads = [color_block.color for color_block in stitch_plan]
        palettes_and_matches = [(palette, self._num_exact_color_matches(palette, threads))
                                for palette in self]
        palette, matches = max(palettes_and_matches, key=lambda item: item[1])

        if matches < 0.8 * len(stitch_plan):
            # if less than 80% of the colors are an exact match,
            # don't use this palette
            return None
        else:
            return palette

    def apply_palette(self, stitch_plan, palette):
        for color_block in stitch_plan:
            nearest = palette.nearest_color(color_block.color)

            color_block.color.name = nearest.name
            color_block.color.number = nearest.number
            color_block.color.manufacturer = nearest.manufacturer

    def get_palette_by_name(self, name):
        for palette in self:
            if palette.name == name:
                return palette


_catalog = None


def ThreadCatalog():
    """Singleton _ThreadCatalog factory"""

    global _catalog
    if _catalog is None:
        _catalog = _ThreadCatalog()

    return _catalog
