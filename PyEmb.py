#!/usr/bin/env python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import math
import libembroidery

PIXELS_PER_MM = 96 / 25.4

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# simplify use of lru_cache decorator
def cache(*args, **kwargs):
    return lru_cache(maxsize=None)(*args, **kwargs)

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
