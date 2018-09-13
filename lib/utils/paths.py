import sys
import os
from os.path import dirname, realpath


def get_bundled_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        return realpath(os.path.join(sys._MEIPASS, "..", name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_resource_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        return realpath(os.path.join(sys._MEIPASS, name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))
