# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
import os
from os.path import dirname, realpath

import appdirs


def get_bundled_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        if sys.platform == "darwin":
            return realpath(os.path.join(sys._MEIPASS, "..", 'Resources', name))
        else:
            return realpath(os.path.join(sys._MEIPASS, "..", name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_resource_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        if sys.platform == "darwin":
            return realpath(os.path.join(sys._MEIPASS, "..", 'Resources', name))
        else:
            return realpath(os.path.join(sys._MEIPASS, name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_user_dir(name=None):
    path = appdirs.user_config_dir("inkstitch")

    if name is not None:
        path = os.path.join(path, name)

    return path
