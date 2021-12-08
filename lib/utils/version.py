# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from os.path import isfile, join, realpath

from ..i18n import _


def get_inkstitch_version():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if sys.platform == "darwin":
            version = realpath(join(sys._MEIPASS, "..", 'Resources', "VERSION"))
        else:
            version = realpath(join(sys._MEIPASS, "..", "VERSION"))
    else:
        version = realpath(join(realpath(__file__), "..", "..", "..", 'VERSION'))
    if isfile(version):
        with open(version, 'r') as v:
            inkstitch_version = _("Ink/Stitch Version: %s") % v.readline()
    else:
        inkstitch_version = _("Ink/Stitch Version: unknown")
    return inkstitch_version
