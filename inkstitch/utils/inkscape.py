from os.path import realpath, expanduser, join as path_join
import sys

def guess_inkscape_config_path():
    if getattr(sys, 'frozen', None):
        path = realpath(path_join(sys._MEIPASS, ".."))
    else:
        path = expanduser("~/.config/inkscape")

    return path
