# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .base import InkstitchExtension
import os
import sys
from glob import glob
from ..utils import get_bundled_dir, guess_inkscape_config_path
from inkex import errormsg
from ..i18n import _


class Install(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)

    def effect(self):
        path = os.path.join(guess_inkscape_config_path(), 'palettes')
        src_dir = get_bundled_dir('palettes')
        try:
            copy_files(glob(os.path.join(src_dir, "*")), path)
            errormsg(_("Successfully installed color palettes for Inkscape.\n\n"
                       "Please restart Inkscape."))
        except IOError:
            errormsg(_("Could not install color palettes. Please file an issue on "
                       "https://github.com/inkstitch/inkstitch/issues"))


if sys.platform == "win32":
    # If we try to just use shutil.copy it says the operation requires elevation.
    def copy_files(files, dest):
        import pythoncom
        import winutils

        pythoncom.CoInitialize()

        if not os.path.exists(dest):
            os.makedirs(dest)

        winutils.copy(files, dest)
else:
    def copy_files(files, dest):
        import shutil

        if not os.path.exists(dest):
            os.makedirs(dest)

        for palette_file in files:
            shutil.copy(palette_file, dest)
