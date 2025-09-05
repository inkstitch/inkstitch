# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from os.path import dirname, realpath
from pathlib import Path

import platformdirs

if sys.version_info >= (3, 11):
    import tomllib  # built-in in Python 3.11+
else:
    import tomli as tomllib


def get_bundled_dir(name=None):
    if getattr(sys, 'frozen', None) is not None:
        meipass = getattr(sys, '_MEIPASS', None)
        if sys.platform == "darwin" and meipass:
            path = os.path.join(meipass, "..", 'Resources')
        elif meipass:
            path = os.path.join(meipass, "..")
        else:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
    else:
        path = os.path.join(dirname(realpath(__file__)), '..', '..')

    if name is not None:
        path = os.path.join(path, name)

    return realpath(path)


def get_resource_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        meipass = getattr(sys, '_MEIPASS', None)
        if sys.platform == "darwin" and meipass:
            return realpath(os.path.join(meipass, "..", 'Resources', name))
        elif meipass:
            return realpath(os.path.join(meipass, name))
        else:
            return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_user_dir(name=None, create=True):
    try:
        path = platformdirs.user_config_dir('inkstitch')
    except ImportError:
        path = os.path.expanduser('~/.inkstitch')
    if create and not os.path.exists(path):
        os.makedirs(path)

    if name is not None:
        path = os.path.join(path, name)

    return path


def get_ini():
    debug_toml = Path(get_bundled_dir("DEBUG.toml"))
    if debug_toml.exists():
        with debug_toml.open("rb") as f:
            ini = tomllib.load(f)  # read DEBUG.toml file if exists, otherwise use default values in ini object
    else:
        ini = {}
    return ini
