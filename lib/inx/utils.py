# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from os.path import dirname, realpath

from jinja2 import Environment, FileSystemLoader


def _resolve_mode():
    """Return the INX generation mode.

    * ``build``: PyInstaller release bundles (selected by ``BUILD`` env var).
    * ``installed``: uv/pip installed wheel; command is on PATH.
    * ``dev``: running from a source checkout.
    """
    if "BUILD" in os.environ:
        return "build"
    return os.environ.get("INKSTITCH_INX_MODE", "dev")


def _runtime_base_dir():
    """Return the project root in dev/build, or ``lib/assets/`` in a wheel."""
    # Avoid importing lib.utils.paths at module level to keep generate_inx_files
    # usable from build scripts that only add the repo root to sys.path.
    from ..utils import get_bundled_dir
    return get_bundled_dir()


def _template_path():
    return os.path.join(_runtime_base_dir(), "templates")


def _inx_path():
    if _resolve_mode() == "installed":
        # Wheel INX are generated into a separate directory so they do not
        # overwrite the development INX in inx/.
        repo_root = dirname(dirname(dirname(realpath(__file__))))
        return os.path.join(repo_root, "inx-installed")
    return os.path.join(_runtime_base_dir(), "inx")


def build_environment():
    env = Environment(
        loader=FileSystemLoader(_template_path()),
        autoescape=True,
        extensions=['jinja2.ext.i18n']
    )

    mode = _resolve_mode()

    if mode == "build":
        # building a ZIP release, with inkstitch packaged as a binary
        # Command tag and icons path
        if sys.platform == "win32":
            env.globals["command_tag"] = '<command location="inx">../bin/inkstitch.exe</command>'
            env.globals["icon_path"] = '../bin/icons/'
        elif sys.platform == "darwin":
            env.globals["command_tag"] = '<command location="inx">../../MacOS/inkstitch</command>'
            env.globals["icon_path"] = '../icons/'
        else:
            env.globals["command_tag"] = '<command location="inx">../bin/inkstitch</command>'
            env.globals["icon_path"] = '../bin/icons/'
    elif mode == "installed":
        # uv/pip installed wheel: inkstitch is on PATH, assets live in lib/assets/
        env.globals["command_tag"] = '<command location="inx">inkstitch</command>'
        env.globals["icon_path"] = 'assets/icons/'
    else:
        # user is running inkstitch.py directly as a developer
        env.globals["command_tag"] = '<command location="inx" interpreter="python">../inkstitch.py</command>'
        env.globals["icon_path"] = '../icons/'
    return env


def write_inx_file(name, contents):
    inx_file_name = "inkstitch_%s.inx" % name
    inx_path = _inx_path()
    os.makedirs(inx_path, exist_ok=True)
    with open(os.path.join(inx_path, inx_file_name), 'w', encoding="utf-8") as inx_file:
        print(contents, file=inx_file)
