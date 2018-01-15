#!/usr/bin/env python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import math
import sys
from copy import deepcopy

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
    def __init__(self, x, y, color=None, jump=False, stop=False):
        self.x = x
        self.y = y
        self.color = color
        self.jump = jump
        self.stop = stop
