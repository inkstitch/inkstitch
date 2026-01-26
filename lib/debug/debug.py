# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import atexit  # to save svg file on exit
import time    # to measure time of code block, use time.monotonic() instead of time.time()
import traceback
from datetime import datetime
from typing import TypeVar, Callable, Any, cast

from contextlib import contextmanager  # to measure time of with block
from pathlib import Path  # to work with paths as objects

import inkex
from lxml import etree   # to create svg file

from ..svg import line_strings_to_path
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL

from .utils import safe_get
from ..utils.paths import get_ini

import logging
logger = logging.getLogger("inkstitch.debug")   # create module logger with name 'inkstitch.debug'

# See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar('F', bound=Callable[..., Any])

# to log messages if previous debug logger is not enabled
logger_inkstich = logging.getLogger("inkstitch")   # create module logger with name 'inkstitch'

sew_stack_enabled = safe_get(get_ini(), "DEBUG", "enable_sew_stack", default=False)


# --------------------------------------------------------------------------------------------
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
        self.enabled = False
        self.last_log_time = None
        self.current_layer = None
        self.group_stack = []
        self.svg_filename = None

    def enable(self):
        # determine svg filename from logger
        if len(logger.handlers) > 0 and isinstance(logger.handlers[0], logging.FileHandler):
            # determine filename of svg file from logger
            filename = Path(logger.handlers[0].baseFilename)
            self.svg_filename = filename.with_suffix(".svg")
            self.svg_filename.unlink(missing_ok=True)      # remove existing svg file

        # self.log is activated by active logger
        # - enabled only if logger first handler is FileHandler
        #   to disable "inkstitch.debug" simply set logging level to CRITICAL
        if logger.isEnabledFor(logging.INFO) and self.svg_filename is not None:
            self.enabled = True
            self.log(f"Logging enabled with svg file: {self.svg_filename}")
            self.init_svg()

        else:
            # use alternative logger to log message if logger has no handlers
            logger_inkstich.info("No handlers in logger, cannot enable logging and svg file creation")

    def init_svg(self):
        self.svg = etree.Element("svg", nsmap=inkex.NSS)
        atexit.register(self.save_svg)

    def save_svg(self):
        if self.enabled and self.svg_filename is not None:
            self.log(f"Writing svg file: {self.svg_filename}")
            tree = etree.ElementTree(self.svg)
            tree.write(str(self.svg_filename))    # lxml <5.0.0 does not support Path objects, requires string
        else:
            # use alternative logger to log message if logger has no handlers
            logger_inkstich.info(f"Saving to svg file is not activated {self.svg_filename=}")

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
        self.last_log_time = now

        msg = message % args
        logger.info(msg)

    # decorator to measure time of function
    def time(self, func: F) -> F:
        def decorated(*args, **kwargs):
            if self.enabled:
                self.raw_log("entering %s()", func.__name__)
                start = time.monotonic()

            result = func(*args, **kwargs)

            if self.enabled:
                end = time.monotonic()
                self.raw_log("leaving %s(), duration = %s", func.__name__, round(end - start, 6))

            return result

        return cast(F, decorated)

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

    def log_exception(self):
        if self.enabled:
            self.raw_log(traceback.format_exc())

    @contextmanager
    def log_exceptions(self):
        try:
            yield
        except Exception:
            self.log_exception()
            raise


# global debug object
debug = Debug()
