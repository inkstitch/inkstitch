# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from os.path import expanduser, split

from inkex.utils import get_user_directory


def guess_inkscape_config_path():
    if getattr(sys, 'frozen', None):
        path = split(get_user_directory())[0]
    else:
        path = expanduser("~/.config/inkscape")
    return path
