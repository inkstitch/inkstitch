# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import subprocess
import sys

from ..utils import get_bundled_dir

app_process = None


def open_url(url, port):
    global app

    url = f'{url}?port={port}'

    os.environ['FLASKPORT'] = str(port)

    # this creates the .json for dev mode to get translations
    if getattr(sys, 'frozen', None) is None:
        dynamic_port = {
            "_comment1": "port should not be declared when commiting",
            "port": port,
        }
        port_object = json.dumps(dynamic_port, indent=1)
        with open(os.path.join("electron/src/lib/flaskserverport.json"), "w") as outfile:
            outfile.write(port_object)

    cwd = None
    searchstring = "http"

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
    # In macos manual install the python env paths are incomplete
    # Adding the yarn path to the env paths fixes this issue
    if sys.platform == "darwin" and getattr(sys, 'frozen', None) is None:
        mac_dev_env = os.environ.copy()
        # these are paths installed by brew or macports
        yarn_path = "/opt/homebrew/bin:/usr/local/bin:/opt/local/bin:"
        if yarn_path in mac_dev_env["PATH"]:
            pass
        else:
            mac_dev_env["PATH"] = yarn_path + mac_dev_env["PATH"]
            # checking URL for flask server address for printToPDF
            if searchstring in url:
                with open(os.devnull, 'w') as null:
                    subprocess.Popen(["yarn", "just-build"], cwd=cwd, stdout=null, env=mac_dev_env).wait()
            else:
                pass

        with open(os.devnull, 'w') as null:
            return subprocess.Popen(command, cwd=cwd, stdout=null, env=mac_dev_env)
    else:
        if searchstring in url and getattr(sys, 'frozen', None) is None:
            with open(os.devnull, 'w') as null:
                subprocess.Popen(["yarn", "just-build"], cwd=cwd, stdout=null).wait()
        else:
            pass
        if sys.platform == "linux":
            # Pyinstaller fix for gnome document view not opening.
            lenv = dict(os.environ)
            lp_key = 'LD_LIBRARY_PATH'
            lp_orig = lenv.get(lp_key + '_ORIG')
            if lp_orig is not None:
                lenv[lp_key] = lp_orig  # restore the original, unmodified value
            else:
                lenv.pop(lp_key, None)

            with open(os.devnull, 'w') as null:
                return subprocess.Popen(command, cwd=cwd, stdout=null, env=lenv)
        else:
            with open(os.devnull, 'w') as null:
                return subprocess.Popen(command, cwd=cwd, stdout=null)
