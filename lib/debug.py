# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import atexit
import os
import socket
import sys
import time
from contextlib import contextmanager
from datetime import datetime

import inkex
from lxml import etree

from .svg import line_strings_to_path
from .svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL


def check_enabled(func):
    def decorated(self, *args, **kwargs):
        if self.enabled:
            return func(self, *args, **kwargs)

    return decorated


def _unwrap(arg):
    if callable(arg):
        return arg()
    else:
        return arg


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


    def enable(self, debug_type, debug_file, wait_attach):
        if debug_type == 'none':
            return
        self.debugger = debug_type
        self.wait_attach = wait_attach
        self.enabled = True
        self.init_log(debug_file)
        self.init_debugger()
        self.init_svg()

    def init_log(self, debug_file):
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), debug_file)
        # delete old content
        with open(self.log_file, "w"):
            pass
        self.log("Debug logging enabled.")

    def init_debugger(self):
        # How to debug Ink/Stitch with LiClipse:
        #
        # 1. Install LiClipse (liclipse.com) -- no need to install Eclipse first
        # 2. Start debug server as described here: http://www.pydev.org/manual_adv_remote_debugger.html
        #    * follow the "Note:" to enable the debug server menu item
        # 3. Create a file named "DEBUG" next to inkstitch.py in your git clone.
        # 4. Run any extension and PyDev will start debugging.

        ###

        # To debug with PyCharm:

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
        # 3. Touch a file named "DEBUG" at the top of your git repo, as above.
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
        # 5. In the execution env for Inkscape, set the environment variable
        #    PYCHARM_REMOTE_DEBUG to any value, and launch Inkscape. If you're starting
        #    Inkscape from the PyCharm Terminal pane, you can do:
        #        export PYCHARM_REMOTE_DEBUG=true;inkscape
        #
        # 6. In Pycharm, either click on the green "bug" icon if visible in the upper
        #    right or press Ctrl-D to start debugging.The PyCharm debugger pane will
        #    display the message "Waiting for process connection..."
        #
        # 7. Do some action in Inkscape which invokes Ink/Stitch extension code, and the
        #    debugger will be triggered. If you've left "Suspend after connect" checked
        #    in the Run configuration, PyCharm will pause in the "self.log("Enabled
        #    PyDev debugger.)" statement, below. Uncheck the box to have it continue
        #    automatically to your first set breakpoint.

        ###

        # To debug with VS Code
        # see: https://code.visualstudio.com/docs/python/debugging#_command-line-debugging
        #      https://code.visualstudio.com/docs/python/debugging#_debugging-by-attaching-over-a-network-connection
        # 
        # 1. Install the Python extension for VS Code
        #      pip install debugpy
        # 2. create .vscode/launch.json containing somewhere:
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
        # 3. Touch a file named "DEBUG" at the top of your git repo, as above.
        #     containing "vscode" or "vscode-script" see parse_file() in debug_mode.py for details
        # 4. Start the debug server in VS Code by clicking on the debug icon in the left pane
        #    select "Python: Attach" from the dropdown menu and click on the green arrow
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
            else:
                raise ValueError(f"unknown debugger: '{self.debugger}'")

        except ImportError:
            self.log("importing pydevd failed (debugger disabled)")

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
        debug_svg = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.svg")
        tree.write(debug_svg)

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

        with open(self.log_file, "a") as logfile:
            print(timestamp, message % args, file=logfile)
            logfile.flush()

    def time(self, func):
        def decorated(*args, **kwargs):
            if self.enabled:
                self.raw_log("entering %s()", func.__name__)
                start = time.time()

            result = func(*args, **kwargs)

            if self.enabled:
                end = time.time()
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

    @contextmanager
    def time_this(self, label="code block"):
        if self.enabled:
            start = time.time()
            self.raw_log("begin %s", label)

        yield

        if self.enabled:
            self.raw_log("completed %s, duration = %s", label, time.time() - start)


debug = Debug()


def enable(debug_type, debug_file, wait_attach):
    debug.enable(debug_type, debug_file, wait_attach)
