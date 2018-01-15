#!/usr/bin/env python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import math
import sys
sys.path.append('Embroidermodder/experimental/python/binding')
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

        x = stitch.x / PIXELS_PER_MM
        y = stitch.y / PIXELS_PER_MM

        libembroidery.embPattern_addStitchAbs(pattern, x, y, flags, 0)

        if flags & libembroidery.JUMP:
            # I'm not sure this is right, but this is how the old version did it.
            libembroidery.embPattern_addStitchAbs(pattern, x, y, flags & ~libembroidery.JUMP, 0)

    libembroidery.embPattern_addStitchAbs(pattern, 0, 0, libembroidery.END, 0)
    libembroidery.embPattern_write(pattern, file_path)
