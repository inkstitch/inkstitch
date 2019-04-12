import os
import subprocess
import sys

from ..utils import get_bundled_dir


app_process = None


def open_url(url):
    global app

    if getattr(sys, 'frozen', None) is not None:
        electron_path = os.path.join(get_bundled_dir("electron"), "inkstitch-gui")

        if sys.platform == "darwin":
            electron_path += ".app/Contents/MacOS/inkstitch-gui"
            subprocess.Popen(["open", "-a", electron_path, "--args", url])
        else:
            app_process = subprocess.Popen([electron_path, url])
    else:
        # if we're not running in a pyinstaller bundle, run electron directly
        app_process = subprocess.Popen(["yarn", "dev", url], cwd=get_bundled_dir("electron"))

    return app_process
