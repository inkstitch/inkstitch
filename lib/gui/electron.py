from glob import glob
import os
import subprocess
import sys

from ..utils import get_bundled_dir


app_process = None


def open_url(url):
    global app

    if getattr(sys, 'frozen', None) is not None:
        electron_path = os.path.join(get_bundled_dir("electron"), "inkstitch-gui")
    else:
        # It's a bit trickier to find the electron app in a development environment.
        base_dir = get_bundled_dir("electron")
        package_dir = glob(os.path.join(base_dir, 'dist', '*-unpacked'))

        if not package_dir:
            raise Exception("Electron app not found.  Be sure to run 'yarn; yarn dist' in %s." % base_dir)

        electron_path = os.path.join(base_dir, package_dir, "inkstitch-gui")

    if sys.platform == "darwin":
        electron_path += ".app/Contents/MacOS/inkstitch-gui"
        app_process = subprocess.Popen(["open", "-a", electron_path, "--args", url])
    else:
        app_process = subprocess.Popen([electron_path, url])

    return app_process
