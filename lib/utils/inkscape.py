import sys
from os.path import expanduser, realpath


def guess_inkscape_config_path():
    if getattr(sys, 'frozen', None):
        path = realpath(sys._MEIPASS.split('extensions', 1)[0])
        if sys.platform == "win32":
            import win32api

            # This expands ugly things like EXTENS~1
            path = win32api.GetLongPathName(path)
    else:
        path = expanduser("~/.config/inkscape")

    return path
