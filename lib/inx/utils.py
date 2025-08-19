# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from os.path import dirname

from jinja2 import Environment, FileSystemLoader

_top_path = dirname(dirname(dirname(os.path.realpath(__file__))))
inx_path = os.path.join(_top_path, "inx")
template_path = os.path.join(_top_path, "templates")



# Used by these modules:
# - lib/inx/inputs.py
# - lib/inx/outputs.py
# - lib/inx/extensions.py


# Setup the Jinja2 environment for building INX files.
# BUILD_DIST - only set when creating distribution packages
def build_environment():
    env = Environment(loader=FileSystemLoader(template_path),
                      autoescape=True,
                      extensions=['jinja2.ext.i18n'])

    if "BUILD_DIST" in os.environ:
        # building a ZIP release, with inkstitch packaged as a binary
        # Command tag and icons path
        if sys.platform == "win32":
            env.globals[
                "command_tag"] = '<command location="inx">../bin/inkstitch.exe</command>'
            env.globals["icon_path"] = '../bin/icons/'
        elif sys.platform == "darwin":
            env.globals[
                "command_tag"] = '<command location="inx">../../MacOS/inkstitch</command>'
            env.globals["icon_path"] = '../icons/'
        else:
            env.globals[
                "command_tag"] = '<command location="inx">../bin/inkstitch</command>'
            env.globals["icon_path"] = '../bin/icons/'
    else:
        # user is running inkstitch.py directly as a developer from the source tree
        # env.globals["command_tag"] = '<command location="inx" interpreter="python">../inkstitch.py</command>'
        # use wrappers
        if sys.platform == "win32":
            # assuming user run inkscape.com (not inkscape.exe) from the command line
            env.globals[
                "command_tag"] = '<command location="inx">../inkstitch_uv.bat</command>'
        else:
            env.globals[
                "command_tag"] = '<command location="inx">../inkstitch_uv.sh</command>'

        env.globals["icon_path"] = '../icons/'
    return env


# Write the given contents to an INX file for Ink/Stitch.
# Args:
#     name (str): The name to use in the INX filename (will be prefixed with 'inkstitch_').
#     contents (str): The contents to write to the INX file.
# The file will be created in the 'inx' directory, with UTF-8 encoding.
def write_inx_file(name, contents):
    inx_file_name = "inkstitch_%s.inx" % name
    with open(os.path.join(inx_path, inx_file_name), 'w', encoding="utf-8") as inx_file:
        print(contents, file=inx_file)
