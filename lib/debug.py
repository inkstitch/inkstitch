# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
import atexit  # to save svg file on exit
import socket  # to check if debugger is running
import time    # to measure time of code block, use time.monotonic() instead of time.time()
from datetime import datetime

from contextlib import contextmanager  # to measure time of with block
from pathlib import Path  # to work with paths as objects
from .debug_utils import safe_get  # mimic get method of dict with default value

import inkex
from lxml import etree   # to create svg file

from .svg import line_strings_to_path
from .svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL


# decorator to check if debugging is enabled
# - if debug is not enabled then decorated function is not called
def check_enabled(func):
    def decorated(self, *args, **kwargs):
        if self.enabled:
            return func(self, *args, **kwargs)

    return decorated


# unwrapping = provision for functions as arguments
# - if argument is callable then it is called and return value is used as argument
#   otherwise argument is returned as is
def _unwrap(arg):
    if callable(arg):
        return arg()
    else:
        return arg


# decorator to unwrap arguments if they are callable
#   eg: if argument is lambda function then it is called and return value is used as argument
def unwrap_arguments(func):
    def decorated(self, *args, **kwargs):
        unwrapped_args = [_unwrap(arg) for arg in args]
        unwrapped_kwargs = {name: _unwrap(value) for name, value in kwargs.items()}

        return func(self, *unwrapped_args, **unwrapped_kwargs)

    return decorated


class Debug(object):
    """Tools to help debug Ink/Stitch

    This class contains methods to log strings and SVG elements.  Strings are
    logged to debug.log, and SVG elements are stored in debug.svg to aid in
    debugging stitch algorithms.

    All functionality is gated by self.enabled.  If debugging is not enabled,
    then debug calls will consume very few resources.  Any method argument
    can be a callable, in which case it is called and the return value is
    logged instead.  This way one can log potentially expensive expressions
    by wrapping them in a lambda:

    debug.log(lambda: some_expensive_function(some_argument))

    The lambda is only called if debugging is enabled.
    """

    def __init__(self):
        self.debugger = None
        self.wait_attach = True
        self.enabled = False
        self.last_log_time = None
        self.current_layer = None
        self.group_stack = []

    def enable(self, debug_type:str, debug_dir: Path, ini: dict):
        # initilize file names and other parameters from DEBUG.toml file
        self.debug_dir = debug_dir  # directory where debug files are stored
        self.debug_log_file = safe_get(ini, "DEBUG", "debug_log_file", default="debug.log")
        self.debug_svg_file = safe_get(ini, "DEBUG", "debug_svg_file", default="debug.svg")
        self.wait_attach = safe_get(ini, "DEBUG", "wait_attach", default=True)  # currently only for vscode

        if debug_type == 'none':
            return

        self.debugger = debug_type
        self.enabled = True
        self.init_log()
        self.init_debugger()
        self.init_svg()

    def init_log(self):
        self.log_file = self.debug_dir / self.debug_log_file
        # delete old content
        with self.log_file.open("w"):
            pass
        self.log("Debug logging enabled.")

    # we intentionally disable flakes C901 - function is too complex, beacuse it is used only for debugging
    # currently complexity is set 10 see 'make style', this means that function can have max 10 nested blocks, here we have more
    # flake8: noqa: C901
    def init_debugger(self):
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
        # - to write debug output to file set debug_to_file = true in DEBUG.toml
        # - to change various output file names see DEBUG.toml
        # - to disable waiting for debugger to attach (vscode editor) set wait_attach = false in DEBUG.toml
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
        # 1. Install the Python extension for VS Code
        #      pip install debugpy
        # 2. create .vscode/launch.json containing:
        #       "configurations": [ ...
        #           {
        #               "name": "Python: Attach",
        #               "type": "python",
        #               "request": "attach",
        #               "connect": {
        #                 "host": "localhost",
        #                 "port": 5678
        #               }
        #           }
        #       ]
        # 3. Touch a file named "DEBUG.toml" at the top of your git repo, as above
        #    set debug_type = vscode
        # 4. Start the debug server in VS Code by clicking on the debug icon in the left pane
        #    select "Python: Attach" from the dropdown menu and click on the green arrow.
        #    The debug server will start and connect to already running python processes,
        #    but immediately exit if no python processes are running.
        #
        # Notes:
        #   to see flask server url routes:
        #      - comment out the line self.disable_logging() in run() of lib/api/server.py

        try:
            if self.debugger == 'vscode':
                import debugpy
            elif self.debugger == 'pycharm':
                import pydevd_pycharm
            elif self.debugger == 'pydev':
                import pydevd
            elif self.debugger == 'file':
                pass
            else:
                raise ValueError(f"unknown debugger: '{self.debugger}'")

        except ImportError:
            self.log(f"importing debugger failed (debugger disabled) for {self.debugger}")

        # pydevd likes to shout about errors to stderr whether I want it to or not
        with open(os.devnull, 'w') as devnull:
            stderr = sys.stderr
            sys.stderr = devnull

            try:
                if self.debugger == 'vscode':
                    debugpy.listen(('localhost', 5678))
                    if self.wait_attach:
                        print("Waiting for debugger attach")
                        debugpy.wait_for_client()        # wait for debugger to attach
                        debugpy.breakpoint()             # stop here to start normal debugging
                elif self.debugger == 'pycharm':
                    pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True,
                                            stderrToServer=True)
                elif self.debugger == 'pydev':
                    pydevd.settrace()
                elif self.debugger == 'file':
                    pass
                else:
                    raise ValueError(f"unknown debugger: '{self.debugger}'")

            except socket.error as error:
                self.log("Debugging: connection to pydevd failed: %s", error)
                self.log(f"Be sure to run 'Start debugging server' in {self.debugger} to enable debugging.")
            else:
                self.log(f"Enabled '{self.debugger}' debugger.")

            sys.stderr = stderr

    def init_svg(self):
        self.svg = etree.Element("svg", nsmap=inkex.NSS)
        atexit.register(self.save_svg)

    def save_svg(self):
        tree = etree.ElementTree(self.svg)
        debug_svg = self.debug_dir / self.debug_svg_file
        tree.write(str(debug_svg))    # lxml <5.0.0 does not support Path objects

    @check_enabled
    @unwrap_arguments
    def add_layer(self, name="Debug"):
        layer = etree.Element("g", {
            INKSCAPE_GROUPMODE: "layer",
            INKSCAPE_LABEL: name,
            "style": "display: none"
        })
        self.svg.append(layer)
        self.current_layer = layer

    @check_enabled
    @unwrap_arguments
    def open_group(self, name="Group"):
        group = etree.Element("g", {
            INKSCAPE_LABEL: name
        })

        self.log_svg_element(group)
        self.group_stack.append(group)

    @check_enabled
    @unwrap_arguments
    def close_group(self):
        if self.group_stack:
            self.group_stack.pop()

    @check_enabled
    @unwrap_arguments
    def log(self, message, *args):
        if self.last_log_time:
            message = "(+%s) %s" % (datetime.now() - self.last_log_time, message)

        self.raw_log(message, *args)

    def raw_log(self, message, *args):
        now = datetime.now()
        timestamp = now.isoformat()
        self.last_log_time = now

        with self.log_file.open("a") as logfile:
            print(timestamp, message % args, file=logfile)
            logfile.flush()

    # decorator to measure time of function
    def time(self, func):
        def decorated(*args, **kwargs):
            if self.enabled:
                self.raw_log("entering %s()", func.__name__)
                start = time.monotonic()

            result = func(*args, **kwargs)

            if self.enabled:
                end = time.monotonic()
                self.raw_log("leaving %s(), duration = %s", func.__name__, round(end - start, 6))

            return result

        return decorated

    @check_enabled
    @unwrap_arguments
    def log_svg_element(self, element):
        if self.current_layer is None:
            self.add_layer()

        if self.group_stack:
            self.group_stack[-1].append(element)
        else:
            self.current_layer.append(element)

    @check_enabled
    @unwrap_arguments
    def log_line_string(self, line_string, name=None, color=None):
        """Add a Shapely LineString to the SVG log."""
        self.log_line_strings([line_string], name, color)

    @check_enabled
    @unwrap_arguments
    def log_line_strings(self, line_strings, name=None, color=None):
        path = line_strings_to_path(line_strings)
        path.set('style', str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3", "fill": None})))

        if name is not None:
            path.set(INKSCAPE_LABEL, name)

        self.log_svg_element(path)

    @check_enabled
    @unwrap_arguments
    def log_line(self, start, end, name="line", color=None):
        self.log_svg_element(etree.Element("path", {
            "d": "M%s,%s %s,%s" % (start + end),
            "style": str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3", "fill": None})),
            INKSCAPE_LABEL: name
        }))

    @check_enabled
    @unwrap_arguments
    def log_point(self, point, name="point", color=None):
        self.log_svg_element(etree.Element("circle", {
            "cx": str(point.x),
            "cy": str(point.y),
            "r": "1",
            "style": str(inkex.Style({"fill": "#000000"})),
        }))

    @check_enabled
    @unwrap_arguments
    def log_graph(self, graph, name="Graph", color=None):
        d = ""

        for edge in graph.edges:
            d += "M%s,%s %s,%s" % (edge[0] + edge[1])

        self.log_svg_element(etree.Element("path", {
            "d": d,
            "style": str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3", "fill": None})),
            INKSCAPE_LABEL: name
        }))

    # decorator to measure time of with block
    @contextmanager
    def time_this(self, label="code block"):
        if self.enabled:
            start = time.monotonic()
            self.raw_log("begin %s", label)

        yield

        if self.enabled:
            self.raw_log("completed %s, duration = %s", label, time.monotonic() - start)


# global debug object
debug = Debug()
