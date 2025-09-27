# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.


# ### General debugging notes:
# 1. to enable debugging or profiling copy DEBUG_template.toml to DEBUG.toml and edit it

# ### How create bash script for offline debugging from console
# 1. in DEBUG.toml set create_bash_script = true
# 2. call inkstitch.py extension from inkscape to create bash script named by bash_file_base in DEBUG.toml
# 3. run bash script from console

# ### Enable debugging
# 1. set debug_type to one of  - vscode, pycharm, pydev, see below for details
#      debug_type = vscode    - 'debugpy' for vscode editor
#      debug_type = pycharm   - 'pydevd-pycharm' for pycharm editor
#      debug_type = pydev     - 'pydevd' for eclipse editor
# 2. set debug_enable = true in DEBUG.toml
#    or use command line argument -d in bash script
#    or set environment variable INKSTITCH_DEBUG_ENABLE = True or 1 or yes or y

# ### Enable profiling
# 1. set profiler_type to one of - cprofile, profile, pyinstrument
#      profiler_type = cprofile    - 'cProfile' profiler
#      profiler_type = profile     - 'profile' profiler
#      profiler_type = pyinstrument- 'pyinstrument' profiler
# 2. set profile_enable = true in DEBUG.toml
#    or use command line argument -p in bash script
#    or set environment variable INKSTITCH_PROFILE_ENABLE = True or 1 or yes or y

# ### Miscelaneous notes:
# - to disable debugger when running from inkscape set disable_from_inkscape = true in DEBUG.toml
# - to change various output file names see DEBUG.toml
# - to prefer inkscape version of inkex module over pip version set prefer_pip_inkex = false in DEBUG.toml

# ###

# ### How to debug Ink/Stitch with LiClipse:
#
# 1. Install LiClipse (liclipse.com) -- no need to install Eclipse first
# 2. Start debug server as described here: http://www.pydev.org/manual_adv_remote_debugger.html
#    * follow the "Note:" to enable the debug server menu item
# 3. Copy and edit a file named "DEBUG.toml" from "DEBUG_template.toml" next to inkstitch.py in your git clone
#    and set debug_type = pydev
# 4. Run any extension and PyDev will start debugging.

# ###

# ### To debug with PyCharm:

# You must use the PyCharm Professional Edition and _not_ the Community
# Edition. Jetbrains has chosen to make remote debugging a Pro feature.
# To debug Inkscape python extensions, the extension code and Inkscape run
# independently of PyCharm, and only communicate with the debugger via a
# TCP socket. Thus, debugging is "remote," even if it's on the same machine,
# connected via the loopback interface.
#
# 1.     pip install pydev_pycharm
#
#    pydev_pycharm is versioned frequently. Jetbrains suggests installing
#    a version at least compatible with the current build. For example, if your
#    PyCharm build, as found in menu PyCharm -> About Pycharm is 223.8617.48,
#    you could do:
#        pip install pydevd-pycharm~=223.8617.48
#
# 2. From the Pycharm "Run" menu, choose "Edit Configurations..." and create a new
#    configuration. Set "IDE host name:" to  "localhost" and "Port:" to 5678.
#    You can leave the default settings for all other choices.
#
# 3. Touch a file named "DEBUG.toml" at the top of your git repo, as above
#    set debug_type = pycharm
#
# 4. Create a symbolic link in the Inkscape extensions directory to the
#    top-level directory of your git repo. On a mac, for example:
#        cd ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
#        ln -s <full path to the top level of your Ink/Stitch git repo>
#    On other architectures it may be:
#        cd ~/.config/inkscape/extensions
#        ln -s <full path to the top level of your Ink/Stitch git repo>
#    Remove any other Ink/Stitch files or references to Ink/Stitch from the
#    extensions directory, or you'll see duplicate entries in the Ink/Stitch
#    extensions menu in Inkscape.
#
# 5. In Pycharm, either click on the green "bug" icon if visible in the upper
#    right or press Ctrl-D to start debugging.The PyCharm debugger pane will
#    display the message "Waiting for process connection..."
#
# 6. Do some action in Inkscape which invokes Ink/Stitch extension code, and the
#    debugger will be triggered. If you've left "Suspend after connect" checked
#    in the Run configuration, PyCharm will pause in the "self.log("Enabled
#    PyDev debugger.)" statement, below. Uncheck the box to have it continue
#    automatically to your first set breakpoint.

# ###

# ### To debug with VS Code
# see: https://code.visualstudio.com/docs/python/debugging#_command-line-debugging
#      https://code.visualstudio.com/docs/python/debugging#_debugging-by-attaching-over-a-network-connection
#
# 1. Install the Python module to debug in VS Code
#      pip install debugpy
# 2. Install the Python and Python Debugger extensions in VS Code
# 3. Copy and edit a file named "DEBUG.toml" from "DEBUG_template.toml" next to inkstitch.py in your git clone:
#    debug_type = vscode
# 4. Start the debug server in VS Code by clicking on the debug icon in the left pane
#    select "Python: Attach" from the dropdown menu and click on the green arrow.
# 5. Run Ink/Stitch and it should connect to VS Code's debugger automatically.
#
# Notes:
#   to see flask server url routes:
#      - comment out the line self.disable_logging() in run() of lib/api/server.py

# We have some ignores so you don't see errors if you don't have one or more of the debugger libraries installed.
# But in turn those ignores will cause unused-ignore errors if those libraries aren't installed...
# mypy: disable-error-code="unused-ignore"

import os
import sys

import socket  # to check if debugger is running

from .utils import safe_get  # mimic get method of dict with default value

import logging

logger = logging.getLogger("inkstitch")

# we intentionally disable flakes C901 - function is too complex, beacuse it is used only for debugging
# currently complexity is set 10 see 'make style', this means that function can have max 10 nested blocks, here we have more
# flake8: noqa: C901
def init_debugger(debug_type:str,  ini: dict):
    if debug_type == 'none':
        return

    debugger = debug_type

    try:
        if debugger == 'vscode':
            import debugpy  # type: ignore[import-untyped, import-not-found]
        elif debugger == 'pycharm':
            import pydevd_pycharm  # type: ignore[import-untyped, import-not-found]
        elif debugger == 'pydev':
            import pydevd  # type: ignore[import-untyped, import-not-found]
        elif debugger == 'file':
            pass
        else:
            raise ValueError(f"unknown debugger: '{debugger}'")

    except ImportError:
        logger.info(f"importing debugger failed (debugger disabled) for {debugger}")

    # pydevd likes to shout about errors to stderr whether I want it to or not
    with open(os.devnull, 'w') as devnull:
        stderr = sys.stderr
        sys.stderr = devnull

        try:
            if debugger == 'vscode':
                debugpy.connect(("localhost", 5678))
                debugpy.breakpoint()
            elif debugger == 'pycharm':
                pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True,
                                        stderrToServer=True)
            elif debugger == 'pydev':
                pydevd.settrace()
            elif debugger == 'file':
                pass
            else:
                raise ValueError(f"unknown debugger: '{debugger}'")

        except socket.error as error:
            logger.info(f"Debugging: connection to {debugger} failed: %s", error)
            logger.info(f"Be sure to run 'Start debugging server' in {debugger} to enable debugging.")
        else:
            logger.info(f"Enabled '{debugger}' debugger.")

        sys.stderr = stderr
