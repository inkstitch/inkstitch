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
            func(self, *args, **kwargs)

    return decorated


class Debug(object):
    def __init__(self):
        self.enabled = False
        self.last_log_time = None
        self.current_layer = None
        self.group_stack = []

    def enable(self):
        self.enabled = True
        self.init_log()
        self.init_debugger()
        self.init_svg()

    def init_log(self):
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.log")
        # delete old content
        with open(self.log_file, "w"):
            pass
        self.log("Debug logging enabled.")

    def init_debugger(self):
        # How to debug Ink/Stitch:
        #
        # 1. Install LiClipse (liclipse.com) -- no need to install Eclipse first
        # 2. Start debug server as described here: http://www.pydev.org/manual_adv_remote_debugger.html
        #    * follow the "Note:" to enable the debug server menu item
        # 3. Create a file named "DEBUG" next to inkstitch.py in your git clone.
        # 4. Run any extension and PyDev will start debugging.

        try:
            import pydevd
        except ImportError:
            self.log("importing pydevd failed (debugger disabled)")

        # pydevd likes to shout about errors to stderr whether I want it to or not
        with open(os.devnull, 'w') as devnull:
            stderr = sys.stderr
            sys.stderr = devnull

            try:
                pydevd.settrace()
            except socket.error as error:
                self.log("Debugging: connection to pydevd failed: %s", error)
                self.log("Be sure to run 'Start debugging server' in PyDev to enable debugging.")
            else:
                self.log("Enabled PyDev debugger.")

            sys.stderr = stderr

    def init_svg(self):
        self.svg = etree.Element("svg", nsmap=inkex.NSS)
        atexit.register(self.save_svg)

    def save_svg(self):
        tree = etree.ElementTree(self.svg)
        debug_svg = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.svg")
        tree.write(debug_svg)

    @check_enabled
    def add_layer(self, name="Debug"):
        layer = etree.Element("g", {
            INKSCAPE_GROUPMODE: "layer",
            INKSCAPE_LABEL: name,
            "style": "display: none"
        })
        self.svg.append(layer)
        self.current_layer = layer

    @check_enabled
    def open_group(self, name="Group"):
        group = etree.Element("g", {
            INKSCAPE_LABEL: name
        })

        self.log_svg_element(group)
        self.group_stack.append(group)

    @check_enabled
    def close_group(self):
        if self.group_stack:
            self.group_stack.pop()

    @check_enabled
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
    def log_svg_element(self, element):
        if self.current_layer is None:
            self.add_layer()

        if self.group_stack:
            self.group_stack[-1].append(element)
        else:
            self.current_layer.append(element)

    @check_enabled
    def log_line_string(self, line_string, name=None, color=None):
        """Add a Shapely LineString to the SVG log."""
        self.log_line_strings([line_string], name, color)

    @check_enabled
    def log_line_strings(self, line_strings, name=None, color=None):
        path = line_strings_to_path(line_strings)
        path.set('style', str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3"})))

        if name is not None:
            path.set(INKSCAPE_LABEL, name)

        self.log_svg_element(path)

    @check_enabled
    def log_line(self, start, end, name="line", color=None):
        self.log_svg_element(etree.Element("path", {
            "d": "M%s,%s %s,%s" % (start + end),
            "style": str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3"})),
            INKSCAPE_LABEL: name
        }))

    @check_enabled
    def log_graph(self, graph, name="Graph", color=None):
        d = ""

        for edge in graph.edges:
            d += "M%s,%s %s,%s" % (edge[0] + edge[1])

        self.log_svg_element(etree.Element("path", {
            "d": d,
            "style": str(inkex.Style({"stroke": color or "#000000", "stroke-width": "0.3"})),
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


def enable():
    debug.enable()
