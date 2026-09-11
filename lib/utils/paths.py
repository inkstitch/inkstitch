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


def _runtime_base_dir():
    """Return the directory containing runtime assets.

    The layout depends on how Ink/Stitch is run:

    * PyInstaller bundle: assets live next to the frozen binary (via sys._MEIPASS).
    * Installed wheel (uv/pip): ``lib/`` is installed as a package and its data
      are bundled inside ``lib/assets/``.  The module file itself is at
      ``lib/utils/paths.py``.
    * Development checkout: the repository root contains ``lib/``, ``icons/``,
      ``fonts/``, etc.  The module file is at ``lib/utils/paths.py``.
    """
    if getattr(sys, 'frozen', None) is not None:
        if sys.platform == "darwin":
            return realpath(os.path.join(sys._MEIPASS, "..", 'Resources'))
        return realpath(os.path.join(sys._MEIPASS, ".."))

    module_dir = dirname(realpath(__file__))
    # In an installed wheel data are shipped inside lib/assets/.
    wheel_assets = realpath(os.path.join(module_dir, '..', 'assets'))
    if os.path.isdir(wheel_assets):
        return wheel_assets

    # Otherwise we are in a development checkout: lib/utils/paths.py -> repo root.
    return realpath(os.path.join(module_dir, '..', '..'))


def get_bundled_dir(name=None):
    path = _runtime_base_dir()

    if name is not None:
        path = os.path.join(path, name)

    return realpath(path)


def get_resource_dir(name):
    return realpath(os.path.join(_runtime_base_dir(), name))


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
