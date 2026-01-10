# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from glob import glob

from inkex import Boolean, errormsg

from ..i18n import _
from ..utils import get_bundled_dir, guess_inkscape_config_path
from ..utils.keyboard_shortcuts import install_keyboard_shortcuts as install_shortcuts
from .base import InkstitchExtension


class Install(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--install-palettes", type=Boolean, default=False, dest="install_palettes")
        self.arg_parser.add_argument("--install-symbol-libraries", type=Boolean, default=False, dest="install_symbol_libraries")
        self.arg_parser.add_argument("--install-keyboard-shortcuts", type=Boolean, default=False, dest="install_keyboard_shortcuts")

        self.inkscape_config_path = guess_inkscape_config_path()
        self.install_resources = get_bundled_dir('addons')

    def effect(self):
        installation_success = []
        if self.options.install_palettes:
            installation_success.append(self.install_palettes())
        if self.options.install_symbol_libraries:
            installation_success.append(self.install_symbol_libraries())
        if self.options.install_keyboard_shortcuts:
            installation_success.append(self.install_keyboard_shortcuts())
        if installation_success and all(installation_success):
            self.install_success_message()

    def install_palettes(self):
        path = os.path.join(self.inkscape_config_path, 'palettes')
        # palettes are also used otherwise, so they have their own location
        src_dir = get_bundled_dir('palettes')
        try:
            copy_files(glob(os.path.join(src_dir, "*")), path)
            return True
        except IOError as error:
            self.install_error_message(_("Could not install color palettes. Please file an issue on"), error)
            return False

    def install_symbol_libraries(self):
        path = os.path.join(self.inkscape_config_path, 'symbols')
        src_dir = os.path.join(self.install_resources, 'symbols')
        try:
            copy_files(glob(os.path.join(src_dir, "*")), path)
            return True
        except IOError as error:
            self.install_error_message(_("Could not install color palettes. Please file an issue on"), error)
            return False

    def install_keyboard_shortcuts(self):
        """Install keyboard shortcuts for Ink/Stitch into Inkscape's keymap."""
        try:
            added, skipped = install_shortcuts()
            if skipped:
                skipped_keys = ", ".join(skipped)
                errormsg(_("Some keyboard shortcuts were not installed because they conflict with existing shortcuts: ") + skipped_keys)
            return True
        except (IOError, OSError) as error:
            self.install_error_message(_("Could not install keyboard shortcuts. Please file an issue on"), error)
            return False

    def install_success_message(self):
        errormsg(_("Successfully installed Addons.\n\nPlease restart Inkscape."))

    def install_error_message(self, text, error):
        errormsg(text + " https://github.com/inkstitch/inkstitch/issues\n\n")
        errormsg(error)


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
