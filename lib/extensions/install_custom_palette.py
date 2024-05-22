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
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-f", "--filepath", type=str, default="", dest="filepath")

    def effect(self):
        gpl = self.options.filepath
        if not os.path.isfile(gpl):
            inkex.errormsg(_("File does not exist."))

        palette_name = os.path.basename(gpl)
        if not palette_name.endswith('.gpl'):
            inkex.errormsg(_("Wrong file type. Ink/Stitch only accepts gpl color palettes."))

        if not palette_name.startswith('InkStitch'):
            palette_name = 'InkStitch %s' % palette_name

        palette_path = os.path.join(guess_inkscape_config_path(), 'palettes')

        if not os.path.isdir(palette_path):
            inkex.errormsg(_("Ink/Stitch cannot find your palette folder automatically. Please install your palette manually."))
        dest = os.path.join(palette_path, palette_name)
        try:
            shutil.copyfile(gpl,  dest)
        except shutil.SameFileError:
            pass

        if not os.path.isfile(dest):
            inkex.errormsg("Something wwent wrong. Ink/Stitch wasn't able to copy your palette "
                           "file into the Inkscape palettes folder. Please do it manually.")
