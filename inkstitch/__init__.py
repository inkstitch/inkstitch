#!/usr/bin/env python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import os
import sys
import gettext
from copy import deepcopy
import math
import libembroidery
from inkstitch.utils import cache
from inkstitch.utils.geometry import Point

import inkex
import simplepath
import simplestyle
import simpletransform
from bezmisc import bezierlength, beziertatlength, bezierpointatt
from cspsubdiv import cspsubdiv
import cubicsuperpath
from shapely import geometry as shgeo


# modern versions of Inkscape use 96 pixels per inch as per the CSS standard
PIXELS_PER_MM = 96 / 25.4

SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_POLYLINE_TAG = inkex.addNS('polyline', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')
INKSCAPE_LABEL = inkex.addNS('label', 'inkscape')
INKSCAPE_GROUPMODE = inkex.addNS('groupmode', 'inkscape')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_POLYLINE_TAG)

dbg = open(os.devnull, "w")

translation = None
_ = lambda message: message


def localize():
    if getattr(sys, 'frozen', False):
        # we are in a pyinstaller installation
        locale_dir = sys._MEIPASS
    else:
        locale_dir = os.path.dirname(__file__)

    locale_dir = os.path.join(locale_dir, 'locales')

    global translation, _

    translation = gettext.translation("inkstitch", locale_dir, fallback=True)
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

    if units == 'pt':
       value /= 72
       units = 'in'

    if units == 'pc':
       value /= 6
       units = 'in'

    if units == 'cm':
       value *= 10
       units = 'mm'

    if units == 'mm':
        value = value / 25.4
        units = 'in'

    if units == 'in':
        # modern versions of Inkscape use CSS's 96 pixels per inch.  When you
        # open an old document, inkscape will add a viewbox for you.
        return value * 96

    raise ValueError(_("Unknown unit: %s") % units)


@cache
def get_doc_size(svg):
    doc_width = convert_length(svg.get('width'))
    doc_height = convert_length(svg.get('height'))

    return doc_width, doc_height

@cache
def get_viewbox_transform(node):
    # somewhat cribbed from inkscape-silhouette
    doc_width, doc_height = get_doc_size(node)

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

@cache
def get_stroke_scale(node):
    doc_width, doc_height = get_doc_size(node)
    viewbox = node.get('viewBox').strip().replace(',', ' ').split()
    return  doc_width / float(viewbox[2])


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


def make_thread(color):
    thread = libembroidery.EmbThread()
    thread.color = libembroidery.embColor_make(*color.rgb)

    thread.description = color.name
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


def _string_to_floats(string):
    floats = string.split(',')
    return [float(num) for num in floats]


def get_origin(svg):
    # The user can specify the embroidery origin by defining two guides
    # named "embroidery origin" that intersect.

    namedview = svg.find(inkex.addNS('namedview', 'sodipodi'))
    all_guides = namedview.findall(inkex.addNS('guide', 'sodipodi'))
    label_attribute = inkex.addNS('label', 'inkscape')
    guides = [guide for guide in all_guides
                    if guide.get(label_attribute, "").startswith("embroidery origin")]

    # document size used below
    doc_size = list(get_doc_size(svg))

    # convert the size from viewbox-relative to real-world pixels
    viewbox_transform = get_viewbox_transform(svg)
    simpletransform.applyTransformToPoint(simpletransform.invertTransform(viewbox_transform), doc_size)

    default = [doc_size[0] / 2.0, doc_size[1] / 2.0]
    simpletransform.applyTransformToPoint(viewbox_transform, default)
    default = Point(*default)

    if len(guides) < 2:
        return default

    # Find out where the guides intersect.  Only pay attention to the first two.
    guides = guides[:2]

    lines = []
    for guide in guides:
        # inkscape's Y axis is reversed from SVG's, and the guide is in inkscape coordinates
        position = Point(*_string_to_floats(guide.get('position')))
        position.y = doc_size[1] - position.y


        # This one baffles me.  I think inkscape might have gotten the order of
        # their vector wrong?
        parts = _string_to_floats(guide.get('orientation'))
        direction = Point(parts[1], parts[0])

        # We have a theoretically infinite line defined by a point on the line
        # and a vector direction.  Shapely can only deal in concrete line
        # segments, so we'll pick points really far in either direction on the
        # line and call it good enough.
        lines.append(shgeo.LineString((position + 100000 * direction, position - 100000 * direction)))

    intersection = lines[0].intersection(lines[1])

    if isinstance(intersection, shgeo.Point):
        origin = [intersection.x, intersection.y]
        simpletransform.applyTransformToPoint(viewbox_transform, origin)
        return Point(*origin)
    else:
        # Either the two guides are the same line, or they're parallel.
        return default


def write_embroidery_file(file_path, stitch_plan, svg):
    origin = get_origin(svg)

    pattern = libembroidery.embPattern_create()

    for color_block in stitch_plan:
        add_thread(pattern, make_thread(color_block.color))

        for stitch in color_block:
            if stitch.stop:
                # The user specified "STOP after".  "STOP" is the same thing as
                # a color change, and the user will assign a special color at
                # the machine that tells it to pause after.  We need to add
                # another copy of the same color here so that the stitches after
                # the STOP are still the same color.
                add_thread(pattern, make_thread(color_block.color))

            flags = get_flags(stitch)
            libembroidery.embPattern_addStitchAbs(pattern, stitch.x - origin.x, stitch.y - origin.y, flags, 1)

    libembroidery.embPattern_addStitchAbs(pattern, stitch.x - origin.x, stitch.y - origin.y, libembroidery.END, 1)

    # convert from pixels to millimeters
    libembroidery.embPattern_scale(pattern, 1/PIXELS_PER_MM)

    # SVG and embroidery disagree on the direction of the Y axis
    libembroidery.embPattern_flipVertical(pattern)

    libembroidery.embPattern_write(pattern, file_path)
