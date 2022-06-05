# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from os.path import expanduser, realpath, split

from inkex.utils import get_user_directory


def guess_inkscape_config_path():
    if getattr(sys, 'frozen', None):
        if get_user_directory() is not None:
            path = split(get_user_directory())[0]
        else:
            path = realpath(sys._MEIPASS.split('extensions', 1)[0])
            if sys.platform == "win32":
                import win32api
                # This expands ugly things like EXTENS~1
                path = win32api.GetLongPathName(path)
    else:
        path = expanduser("~/.config/inkscape")
    return path
