# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from os.path import expanduser, realpath, split

from inkex.utils import get_user_directory


def guess_inkscape_config_path():
    user_dir = get_user_directory()
    if user_dir is not None:
        path = split(user_dir)[0]
    elif getattr(sys, 'frozen', None):
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            path = realpath(meipass.split('extensions', 1)[0])
            if sys.platform == "win32":
                try:
                    import win32api
                    # This expands ugly things like EXTENS~1
                    path = win32api.GetLongPathName(path)
                except ImportError:
                    pass  # fallback to original path if win32api not available
        else:
            path = expanduser("~/.config/inkscape")
    else:
        if sys.platform == "darwin":
            path = expanduser("~/Library/Application Support/org.inkscape.Inkscape/config/inkscape")
        else:
            path = expanduser("~/.config/inkscape")
    return path
