# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import shutil

import inkex

from ..i18n import _
from ..utils import guess_inkscape_config_path
from .base import InkstitchExtension


class InstallCustomPalette(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--filepath", type=str, default="", dest="filepath")

    def effect(self):
        gpl = self.options.filepath
        if not os.path.isfile(gpl):
            inkex.errormsg(_("File does not exist."))

        palette_path = os.path.join(guess_inkscape_config_path(), 'palettes')

        if not os.path.isdir(palette_path):
            inkex.errormsg(_("Ink/Stitch cannot find your palette folder automatically. Please install your palette manually."))
        dest = os.path.join(palette_path, os.path.basename(gpl))
        shutil.copyfile(gpl,  dest)

        if not os.path.isfile(dest):
            inkex.errormsg("Something wwent wrong. Ink/Stitch wasn't able to copy your palette "
                           "file into the Inkscape palettes folder. Please do it manually.")
