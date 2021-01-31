import sys
from os.path import isfile, join, realpath

from ..i18n import _


def get_inkstitch_version():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        version = realpath(join(sys._MEIPASS, "..", "VERSION"))
    else:
        version = realpath(join(realpath(__file__), "..", "..", "..", 'VERSION'))
    if isfile(version):
        with open(version, 'r') as v:
            inkstitch_version = _("Ink/Stitch Version: %s") % v.readline()
    else:
        inkstitch_version = _("Ink/Stitch Version: unkown")
    return inkstitch_version
