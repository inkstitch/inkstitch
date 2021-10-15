# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import subprocess
import sys

from ..utils import get_bundled_dir

app_process = None


def open_url(url):
    global app

    command = []
    cwd = None

    if getattr(sys, 'frozen', None) is not None:
        electron_path = os.path.join(get_bundled_dir("electron"), "inkstitch-gui")

        if sys.platform == "darwin":
            electron_path = os.path.join(sys._MEIPASS, "electron", "inkstitch-gui.app", "Contents", "MacOS", "inkstitch-gui")
            command = ["open", "-W", "-a", electron_path, "--args", url]
        else:
            command = [electron_path, url]
    else:
        # if we're not running in a pyinstaller bundle, run electron directly
        command = ["yarn", "dev", url]
        cwd = get_bundled_dir("electron")

    # Any output on stdout will crash inkscape.
    with open(os.devnull, 'w') as null:
        return subprocess.Popen(command, cwd=cwd, stdout=null)
