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

        try:
            package_dir = os.listdir(os.path.join(base_dir, "out"))[0]
        except (OSError, IndexError):
            raise Exception("Electron app not found.  Be sure to run 'npm install; npm run package' in %s." % base_dir)

        electron_path = os.path.join(base_dir, "out", package_dir, "inkstitch-gui")

    app_process = subprocess.Popen([electron_path, url])

    return app_process
