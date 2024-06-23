# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from os.path import isfile, join, realpath

from ..i18n import _


def get_inkstitch_version():
    version = _get_source_file("VERSION")
    if isfile(version):
        with open(version, 'r') as v:
            inkstitch_version = _("Ink/Stitch Version: %s") % v.readline()
    else:
        inkstitch_version = _("Ink/Stitch Version: unknown")
    return inkstitch_version


def get_inkstitch_license():
    license = _get_source_file("LICENSE")
    if isfile(license):
        with open(license, 'r') as lcs:
            license = lcs.read()
    else:
        license = "License: GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007"
    return license


def _get_source_file(filename):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if sys.platform == "darwin":
            source_file = realpath(join(sys._MEIPASS, "..", 'Resources', filename))
        else:
            source_file = realpath(join(sys._MEIPASS, "..", filename))
    else:
        source_file = realpath(join(realpath(__file__), "..", "..", "..", filename))
    return source_file
