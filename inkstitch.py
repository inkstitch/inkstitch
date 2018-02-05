#!/usr/bin/env python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import os
import sys
import gettext
from copy import deepcopy
import math
import libembroidery
import inkex
import simplepath
import simplestyle
import simpletransform
from bezmisc import bezierlength, beziertatlength, bezierpointatt
from cspsubdiv import cspsubdiv
import cubicsuperpath


try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# modern versions of Inkscape use 96 pixels per inch as per the CSS standard
PIXELS_PER_MM = 96 / 25.4

SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_POLYLINE_TAG = inkex.addNS('polyline', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_POLYLINE_TAG)

dbg = open("/tmp/embroider-debug.txt", "w")

_ = lambda message: message

# simplify use of lru_cache decorator
def cache(*args, **kwargs):
    return lru_cache(maxsize=None)(*args, **kwargs)

def localize():
    if getattr(sys, 'frozen', False):
        # we are in a pyinstaller installation
        locale_dir = sys._MEIPASS
    else:
        locale_dir = os.path.dirname(__file__)

    locale_dir = os.path.join(locale_dir, 'locales')

    translation = gettext.translation("inkstitch", locale_dir, fallback=True)

    global _
    _ = translation.gettext

localize()

# cribbed from inkscape-silhouette
def parse_length_with_units( str ):

    '''
    Parse an SVG value which may or may not have units attached
    This version is greatly simplified in that it only allows: no units,
    units of px, mm, and %.  Everything else, it returns None for.
    There is a more general routine to consider in scour.py if more
    generality is ever needed.
    '''

    u = 'px'
    s = str.strip()
    if s[-2:] == 'px':
        s = s[:-2]
    elif s[-2:] == 'mm':
        u = 'mm'
        s = s[:-2]
    elif s[-2:] == 'pt':
        u = 'pt'
        s = s[:-2]
    elif s[-2:] == 'pc':
        u = 'pc'
        s = s[:-2]
    elif s[-2:] == 'cm':
        u = 'cm'
        s = s[:-2]
    elif s[-2:] == 'in':
        u = 'in'
        s = s[:-2]
    elif s[-1:] == '%':
        u = '%'
        s = s[:-1]
    try:
        v = float( s )
    except:
        raise ValueError(_("parseLengthWithUnits: unknown unit %s") % s)

    return v, u


def convert_length(length):
    value, units = parse_length_with_units(length)

    if not units or units == "px":
        return value

    if units == 'cm':
       value *= 10
       units == 'mm'

    if units == 'mm':
        value = value / 25.4
        units = 'in'

    if units == 'in':
        # modern versions of Inkscape use CSS's 96 pixels per inch.  When you
        # open an old document, inkscape will add a viewbox for you.
        return value * 96

    raise ValueError(_("Unknown unit: %s") % units)


@cache
def get_viewbox_transform(node):
    # somewhat cribbed from inkscape-silhouette

    doc_width = convert_length(node.get('width'))
    doc_height = convert_length(node.get('height'))

    viewbox = node.get('viewBox').strip().replace(',', ' ').split()

    dx = -float(viewbox[0])
    dy = -float(viewbox[1])
    transform = simpletransform.parseTransform("translate(%f, %f)" % (dx, dy))

    try:
        sx = doc_width / float(viewbox[2])
        sy = doc_height / float(viewbox[3])
        scale_transform = simpletransform.parseTransform("scale(%f, %f)" % (sx, sy))
        transform = simpletransform.composeTransform(transform, scale_transform)
    except ZeroDivisionError:
        pass

    return transform

class Param(object):
    def __init__(self, name, description, unit=None, values=[], type=None, group=None, inverse=False, default=None, tooltip=None, sort_index=0):
        self.name = name
        self.description = description
        self.unit = unit
        self.values = values or [""]
        self.type = type
        self.group = group
        self.inverse = inverse
        self.default = default
        self.tooltip = tooltip
        self.sort_index = sort_index

    def __repr__(self):
        return "Param(%s)" % vars(self)


# Decorate a member function or property with information about
# the embroidery parameter it corresponds to
def param(*args, **kwargs):
    p = Param(*args, **kwargs)

    def decorator(func):
        func.param = p
        return func

    return decorator


class EmbroideryElement(object):
    def __init__(self, node):
        self.node = node

    @property
    def id(self):
        return self.node.get('id')

    @classmethod
    def get_params(cls):
        params = []
        for attr in dir(cls):
            prop = getattr(cls, attr)
            if isinstance(prop, property):
                # The 'param' attribute is set by the 'param' decorator defined above.
                if hasattr(prop.fget, 'param'):
                    params.append(prop.fget.param)

        return params

    @cache
    def get_param(self, param, default):
        value = self.node.get("embroider_" + param, "").strip()

        return value or default

    @cache
    def get_boolean_param(self, param, default=None):
        value = self.get_param(param, default)

        if isinstance(value, bool):
            return value
        else:
            return value and (value.lower() in ('yes', 'y', 'true', 't', '1'))

    @cache
    def get_float_param(self, param, default=None):
        try:
            value = float(self.get_param(param, default))
        except (TypeError, ValueError):
            return default

        if param.endswith('_mm'):
            value = value * PIXELS_PER_MM

        return value

    @cache
    def get_int_param(self, param, default=None):
        try:
            value = int(self.get_param(param, default))
        except (TypeError, ValueError):
            return default

        if param.endswith('_mm'):
            value = int(value * PIXELS_PER_MM)

        return value

    def set_param(self, name, value):
        self.node.set("embroider_%s" % name, str(value))

    @cache
    def get_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        if (style_name not in style):
            return None
        value = style[style_name]
        if value == 'none':
            return None
        return value

    @cache
    def has_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        return style_name in style

    @property
    def path(self):
        return cubicsuperpath.parsePath(self.node.get("d"))


    @cache
    def parse_path(self):
        # A CSP is a  "cubic superpath".
        #
        # A "path" is a sequence of strung-together bezier curves.
        #
        # A "superpath" is a collection of paths that are all in one object.
        #
        # The "cubic" bit in "cubic superpath" is because the bezier curves
        # inkscape uses involve cubic polynomials.
        #
        # Each path is a collection of tuples, each of the form:
        #
        # (control_before, point, control_after)
        #
        # A bezier curve segment is defined by an endpoint, a control point,
        # a second control point, and a final endpoint.  A path is a bunch of
        # bezier curves strung together.  One could represent a path as a set
        # of four-tuples, but there would be redundancy because the ending
        # point of one bezier is the starting point of the next.  Instead, a
        # path is a set of 3-tuples as shown above, and one must construct
        # each bezier curve by taking the appropriate endpoints and control
        # points.  Bleh. It should be noted that a straight segment is
        # represented by having the control point on each end equal to that
        # end's point.
        #
        # In a path, each element in the 3-tuple is itself a tuple of (x, y).
        # Tuples all the way down.  Hasn't anyone heard of using classes?

        path = self.path

        # start with the identity transform
        transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

        # combine this node's transform with all parent groups' transforms
        transform = simpletransform.composeParents(self.node, transform)

        # add in the transform implied by the viewBox
        viewbox_transform = get_viewbox_transform(self.node.getroottree().getroot())
        transform = simpletransform.composeTransform(viewbox_transform, transform)

        # apply the combined transform to this node's path
        simpletransform.applyTransformToPath(transform, path)


        return path

    def flatten(self, path):
        """approximate a path containing beziers with a series of points"""

        path = deepcopy(path)

        cspsubdiv(path, 0.1)

        flattened = []

        for comp in path:
            vertices = []
            for ctl in comp:
                vertices.append((ctl[1][0], ctl[1][1]))
            flattened.append(vertices)

        return flattened

    @property
    @param('trim_after',
           _('TRIM after'),
           tooltip=_('Trim thread after this object (for supported machines and file formats)'),
           type='boolean',
           default=False,
           sort_index=1000)
    def trim_after(self):
        return self.get_boolean_param('trim_after', False)

    @property
    @param('stop_after',
           _('STOP after'),
           tooltip=_('Add STOP instruction after this object (for supported machines and file formats)'),
           type='boolean',
           default=False,
           sort_index=1000)
    def stop_after(self):
        return self.get_boolean_param('stop_after', False)

    def to_patches(self, last_patch):
        raise NotImplementedError("%s must implement to_patches()" % self.__class__.__name__)

    def embroider(self, last_patch):
        patches = self.to_patches(last_patch)

        if patches:
            patches[-1].trim_after = self.trim_after
            patches[-1].stop_after = self.stop_after

        return patches

    def fatal(self, message):
        print >> sys.stderr, "error:", message
        sys.exit(1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def mul(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __mul__(self, other):
        if isinstance(other, Point):
            # dot product
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        else:
            raise ValueError("cannot multiply Point by %s" % type(other))

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        else:
            raise ValueError("cannot multiply Point by %s" % type(other))

    def __repr__(self):
        return "Point(%s,%s)" % (self.x, self.y)

    def length(self):
        return math.sqrt(math.pow(self.x, 2.0) + math.pow(self.y, 2.0))

    def unit(self):
        return self.mul(1.0 / self.length())

    def rotate_left(self):
        return Point(-self.y, self.x)

    def rotate(self, angle):
        return Point(self.x * math.cos(angle) - self.y * math.sin(angle), self.y * math.cos(angle) + self.x * math.sin(angle))

    def as_int(self):
        return Point(int(round(self.x)), int(round(self.y)))

    def as_tuple(self):
        return (self.x, self.y)

    def __cmp__(self, other):
        return cmp(self.as_tuple(), other.as_tuple())

    def __getitem__(self, item):
        return self.as_tuple()[item]

    def __len__(self):
        return 2


class Stitch(Point):
    def __init__(self, x, y, color=None, jump=False, stop=False, trim=False):
        self.x = x
        self.y = y
        self.color = color
        self.jump = jump
        self.trim = trim
        self.stop = stop

    def __repr__(self):
        return "Stitch(%s, %s, %s, %s, %s, %s)" % (self.x, self.y, self.color, "JUMP" if self.jump else "", "TRIM" if self.trim else "", "STOP" if self.stop else "")


def descendants(node):
    nodes = []
    element = EmbroideryElement(node)

    if element.has_style('display') and element.get_style('display') is None:
        return []

    if node.tag == SVG_DEFS_TAG:
        return []

    for child in node:
        nodes.extend(descendants(child))

    if node.tag in EMBROIDERABLE_TAGS:
        nodes.append(node)

    return nodes


def get_nodes(effect):
    """Get all XML nodes, or just those selected

    effect is an instance of a subclass of inkex.Effect.
    """

    if effect.selected:
        nodes = []
        for node in effect.document.getroot().iter():
            if node.get("id") in effect.selected:
                nodes.extend(descendants(node))
    else:
        nodes = descendants(effect.document.getroot())

    return nodes


def make_thread(color):
    # strip off the leading "#"
    if color.startswith("#"):
        color = color[1:]

    thread = libembroidery.EmbThread()
    thread.color = libembroidery.embColor_fromHexStr(color)

    thread.description = color
    thread.catalogNumber = ""

    return thread

def add_thread(pattern, thread):
    """Add a thread to a pattern and return the thread's index"""

    libembroidery.embPattern_addThread(pattern, thread)

    return libembroidery.embThreadList_count(pattern.threadList) - 1

def get_flags(stitch):
    flags = 0

    if stitch.jump:
        flags |= libembroidery.JUMP

    if stitch.trim:
        flags |= libembroidery.TRIM

    if stitch.stop:
        flags |= libembroidery.STOP

    return flags

def write_embroidery_file(file_path, stitches):
    # Embroidery machines don't care about our canvas size, so we relocate the
    # design to the origin.  It might make sense to center it about the origin
    # instead.
    min_x = min(stitch.x for stitch in stitches)
    min_y = min(stitch.y for stitch in stitches)

    pattern = libembroidery.embPattern_create()
    threads = {}

    last_color = None

    for stitch in stitches:
        if stitch.color != last_color:
            if stitch.color not in threads:
                thread = make_thread(stitch.color)
                thread_index = add_thread(pattern, thread)
                threads[stitch.color] = thread_index
            else:
                thread_index = threads[stitch.color]

            libembroidery.embPattern_changeColor(pattern, thread_index)
            last_color = stitch.color

        flags = get_flags(stitch)
        libembroidery.embPattern_addStitchAbs(pattern, stitch.x - min_x, stitch.y - min_y, flags, 0)

    libembroidery.embPattern_addStitchAbs(pattern, stitch.x - min_x, stitch.y - min_y, libembroidery.END, 0)

    # convert from pixels to millimeters
    libembroidery.embPattern_scale(pattern, 1/PIXELS_PER_MM)

    # SVG and embroidery disagree on the direction of the Y axis
    libembroidery.embPattern_flipVertical(pattern)

    libembroidery.embPattern_write(pattern, file_path)
