import os
import subprocess

from ..utils import get_bundled_dir


app_process = None


def open_url(url):
    global app

    electron_path = os.path.join(get_bundled_dir("electron"), "out", "inkstitch-linux-x64", "inkstitch-gui")
    app_process = subprocess.Popen([electron_path, url])

    return app_process
