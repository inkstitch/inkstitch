import atexit
from datetime import datetime
import os
import socket
import sys
import time

from inkex import etree
import inkex
from simplestyle import formatStyle

from svg import line_strings_to_path
from svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL


class Debug(object):
    def __init__(self):
        self.last_log_time = None
        self.current_layer = None

    def enable(self):
        self.enable_log()
        self.enable_debugger()
        self.enable_svg()

    def enable_log(self):
        self.log = self._log
        self.raw_log = self._raw_log
        self.log_file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.log"), "w")
        self.log("Debug logging enabled.")

    def enable_debugger(self):
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
            except socket.error, error:
                self.log("Debugging: connection to pydevd failed: %s", error)
                self.log("Be sure to run 'Start debugging server' in PyDev to enable debugging.")
            else:
                self.log("Enabled PyDev debugger.")

            sys.stderr = stderr

    def enable_svg(self):
        self.svg = etree.Element("svg", nsmap=inkex.NSS)
        atexit.register(self.save_svg)

    def save_svg(self):
        tree = etree.ElementTree(self.svg)
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.svg"), "w") as debug_svg:
            tree.write(debug_svg)

    def add_layer(self, name="Debug"):
        layer = etree.Element("g", {
            INKSCAPE_GROUPMODE: "layer",
            INKSCAPE_LABEL: name
        })
        self.svg.append(layer)
        self.current_layer = layer

    def _noop(self, *args, **kwargs):
        pass

    log = _noop
    raw_log = _noop

    def _log(self, message, *args):
        if self.last_log_time:
            message = "(+%s) %s" % (datetime.now() - self.last_log_time, message)

        self.raw_log(message, *args)

    def _raw_log(self, message, *args):
        now = datetime.now()
        timestamp = now.isoformat()
        self.last_log_time = now

        print >> self.log_file, timestamp, message % args
        self.log_file.flush()

    def time(self, func):
        def decorated(*args, **kwargs):
            self.raw_log("entering %s()", func.func_name)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            self.raw_log("leaving %s(), duration = %s", func.func_name, round(end - start, 6))
            return result

        return decorated

    def log_svg_element(self, element):
        if self.current_layer is None:
            self.add_layer()

        self.current_layer.append(element)

    def log_line_string(self, line_string, color="#000000"):
        """Add a Shapely LineString to the SVG log."""
        self.log_line_strings(self, [line_string])

    def log_line_strings(self, line_strings, color="#000000"):
        path = line_strings_to_path(line_strings)
        path.set('style', formatStyle({"stroke": color, "stroke-width": "0.3"}))
        self.log_svg_element(path)


debug = Debug()
enable = debug.enable
