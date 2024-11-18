# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from os.path import isfile, join

from ..i18n import _
from ..utils import get_bundled_dir


def get_inkstitch_version():
    version = join(get_bundled_dir(), "VERSION")
    if isfile(version):
        with open(version, 'r') as v:
            inkstitch_version = _("Ink/Stitch Version: %s") % v.readline()
    else:
        inkstitch_version = _("Ink/Stitch Version: unknown")
    return inkstitch_version


def get_inkstitch_license():
    license = join(get_bundled_dir(), "LICENSE")
    if isfile(license):
        with open(license, 'r') as lcs:
            license = lcs.read()
    else:
        license = "License: GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007"
    return license
