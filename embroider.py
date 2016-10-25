#!/usr/bin/python
#
# documentation: see included index.html
# LICENSE:
# Copyright 2010 by Jon Howell,
# Originally licensed under <a href="http://www.gnu.org/licenses/quick-guide-gplv3.html">GPLv3</a>.
# Copyright 2015 by Bas Wijnen <wijnen@debian.org>.
# New parts are licensed under AGPL3 or later.
# (Note that this means this work is licensed under the common part of those two: AGPL version 3.)
#
# Important resources:
# lxml interface for walking SVG tree:
# http://codespeak.net/lxml/tutorial.html#elementpath
# Inkscape library for extracting paths from SVG:
# http://wiki.inkscape.org/wiki/index.php/Python_modules_for_extensions#simplepath.py
# Shapely computational geometry library:
# http://gispython.org/shapely/manual.html#multipolygons
# Embroidery file format documentation:
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
import subprocess
from copy import deepcopy
import time
from itertools import chain, izip
import inkex
import simplepath
import simplestyle
import simpletransform
from bezmisc import bezierlength, beziertatlength, bezierpointatt
from cspsubdiv import cspsubdiv
import cubicsuperpath
import PyEmb
import math
import random
import operator
import lxml.etree as etree
from lxml.builder import E
import shapely.geometry as shgeo
import shapely.affinity as affinity
from pprint import pformat

dbg = open("/tmp/embroider-debug.txt", "w")
PyEmb.dbg = dbg
#pixels_per_millimeter = 90.0 / 25.4

#this actually makes each pixel worth one tenth of a millimeter
pixels_per_millimeter = 10

# a 0.5pt stroke becomes a straight line.
STROKE_MIN = 0.5

def parse_boolean(s):
    if isinstance(s, bool):
        return s
    else:
        return s and (s.lower() in ('yes', 'y', 'true', 't', '1'))

def get_param(node, param, default):
    value = node.get("embroider_" + param)

    if value is None or not value.strip():
        return default

    return value.strip()

def get_boolean_param(node, param, default=False):
    value = get_param(node, param, default)

    return parse_boolean(value)

def get_float_param(node, param, default=None):
    value = get_param(node, param, default)

    try:
        return float(value)
    except ValueError:
        return default

def get_int_param(node, param, default=None):
    value = get_param(node, param, default)

    try:
        return int(value)
    except ValueError:
        return default

def parse_path(node):
    path = cubicsuperpath.parsePath(node.get("d"))

#    print >> sys.stderr, pformat(path)

    # start with the identity transform
    transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

    # combine this node's transform with all parent groups' transforms
    transform = simpletransform.composeParents(node, transform)

    # apply the combined transform to this node's path
    simpletransform.applyTransformToPath(transform, path)

    return path

def flatten(path, flatness):
    """approximate a path containing beziers with a series of points"""

    path = deepcopy(path)

    cspsubdiv(path, flatness)

    flattened = []

    for comp in path:
        vertices = []
        for ctl in comp:
            vertices.append((ctl[1][0], ctl[1][1]))
        flattened.append(vertices)

    return flattened

def bboxarea(poly):
    x0=None
    x1=None
    y0=None
    y1=None
    for pt in poly:
        if (x0==None or pt[0]<x0): x0 = pt[0]
        if (x1==None or pt[0]>x1): x1 = pt[0]
        if (y0==None or pt[1]<y0): y0 = pt[1]
        if (y1==None or pt[1]>y1): y1 = pt[1]
    return (x1-x0)*(y1-y0)

def area(poly):
    return bboxarea(poly)

def byarea(a,b):
    return -cmp(area(a), area(b))

def cspToShapelyPolygon(path):
    poly_ary = []
    for sub_path in path:
        point_ary = []
        last_pt = None
        for pt in sub_path:
            if (last_pt!=None):
                vp = (pt[0]-last_pt[0],pt[1]-last_pt[1])
                dp = math.sqrt(math.pow(vp[0],2.0)+math.pow(vp[1],2.0))
                #dbg.write("dp %s\n" % dp)
                if (dp > 0.01):
                    # I think too-close points confuse shapely.
                    point_ary.append(pt)
                    last_pt = pt
            else:
                last_pt = pt
        poly_ary.append(point_ary)
    # shapely's idea of "holes" are to subtract everything in the second set
    # from the first. So let's at least make sure the "first" thing is the
    # biggest path.
    poly_ary.sort(byarea)

    polygon = shgeo.MultiPolygon([(poly_ary[0], poly_ary[1:])])
    #print >> sys.stderr, "polygon valid:", polygon.is_valid
    return polygon

def shapelyCoordsToSvgD(geo):
    coords = list(geo.coords)
    new_path = []
    new_path.append(['M', coords[0]])
    for c in coords[1:]:
        new_path.append(['L', c])
    return simplepath.formatPath(new_path)

def shapelyLineSegmentToPyTuple(shline):
    tuple = ((shline.coords[0][0],shline.coords[0][1]),
            (shline.coords[1][0],shline.coords[1][1]))
    return tuple

def reverseTuple(t):
    return tuple(reversed(t))

def dupNodeAttrs(node):
    n2 = E.node()
    for k in node.attrib.keys():
        n2.attrib[k] = node.attrib[k]
    del n2.attrib["id"]
    del n2.attrib["d"]
    return n2

class Patch:
    def __init__(self, color=None, sortorder=None, stitches=None):
        self.color = color
        self.sortorder = sortorder
        self.stitches = stitches or []

    def __add__(self, other):
        if isinstance(other, Patch):
            return Patch(self.color, self.sortorder, self.stitches + other.stitches)
        else:
            raise TypeError("Patch can only be added to another Patch")

    def addStitch(self, stitch):
        self.stitches.append(stitch)

    def reverse(self):
        return Patch(self.color, self.sortorder, self.stitches[::-1])

class DebugHole:
    pass

class PatchList:
    def __init__(self, patches):
        self.patches = patches

    def __len__(self):
        return len(self.patches)

    def sort_by_sortorder(self):
        def by_sort_order(a,b):
            return cmp(a.sortorder, b.sortorder)
        self.patches.sort(by_sort_order)

    def partition_by_color(self):
        self.sort_by_sortorder()
        #dbg.write("Sorted by sortorder:\n");
        #dbg.write("  %s\n" % ("\n".join(map(lambda p: str(p.sortorder), self.patches))))
        out = []
        lastPatch = None
        for patch in self.patches:
            if (lastPatch!=None and patch.sortorder==lastPatch.sortorder):
                out[-1].patches.append(patch)
            else:
                out.append(PatchList([patch]))
            lastPatch = patch
        #dbg.write("Emitted %s partitions\n" % len(out))
        return out

    def tsp_by_color(self):
        list_of_patchLists = self.partition_by_color()
        for patchList in list_of_patchLists:
            if len(patchList) > 1:
                patchList.traveling_salesman()
        return PatchList(reduce(operator.add,
            map(lambda pl: pl.patches, list_of_patchLists)))

#    # TODO apparently dead code; replaced by partition_by_color above
#    def clump_like_colors_together(self):
#        out = PatchList([])
#        lastPatch = None
#        for patch in self.patches:
#            if (lastPatch!=None and patch.color==lastPatch.color):
#                out.patches[-1] = Patch(
#                    out.patches[-1].color,
#                    out.patches[-1].sortorder,
#                    out.patches[-1].stitches+patch.stitches)
#            else:
#                out.patches.append(patch)
#            lastPatch = patch
#        return out

    def get(self, i):
        if (i<0 or i>=len(self.patches)):
            return None
        return self.patches[i]

    def cost(self, a, b):
        if (a is None or b is None):
            rc = 0.0
        else:
            rc = (a.stitches[-1] - b.stitches[0]).length()
        #dbg.write("cost(%s, %s) = %5.1f\n" % (a, b, rc))
        return rc

    def total_cost(self):
        total = 0

        for i in xrange(1, len(self.patches)):
            total += self.cost(self.get(i-1), self.get(i))

        return total

    def try_swap(self, i, j):
        # i,j are indices;
        #dbg.write("swap(%d, %d)\n" % (i,j))
        i, j = sorted((i, j))
        neighbors = abs(i - j) == 1
        if neighbors:
            oldCost = sum((self.cost(self.get(i-1), self.get(i)),
                           self.cost(self.get(i), self.get(j)),
                           self.cost(self.get(j), self.get(j+1))))
        else:
            oldCost = sum((self.cost(self.get(i-1), self.get(i)),
                           self.cost(self.get(i), self.get(i+1)),
                           self.cost(self.get(j-1), self.get(j)),
                           self.cost(self.get(j), self.get(j+1))))
        npi = self.get(j)
        npj = self.get(i)
        rpi = npi.reverse()
        rpj = npj.reverse()
        options = [
            (npi,npj),
            (rpi,npj),
            (npi,rpj),
            (rpi,rpj),
        ]
        def costOf(np):
            (npi,npj) = np

            if abs(i - j) == 1:
                return sum((self.cost(self.get(i-1), npi),
                            self.cost(npi, npj),
                            self.cost(npj, self.get(j+1))))
            else:
                return sum((self.cost(self.get(i-1), npi),
                            self.cost(npi, self.get(i+1)),
                            self.cost(self.get(j-1), npj),
                            self.cost(npj, self.get(j+1))))
        costs = map(lambda o: (costOf(o), o), options)
        costs.sort()
        (cost,option) = costs[0]
        savings = oldCost - cost
        if (savings > 0):
            self.patches[i] = option[0]
            self.patches[j] = option[1]
            success = "!"
        else:
            success = "."

        #dbg.write("old %5.1f new %5.1f savings: %5.1f\n" % (oldCost, cost, savings))
        return success

    def try_reverse(self, i):
        #dbg.write("reverse(%d)\n" % i)
        oldCost = (self.cost(self.get(i-1), self.get(i))
            +self.cost(self.get(i), self.get(i+1)))
        reversed = self.get(i).reverse()
        newCost = (self.cost(self.get(i-1), reversed)
            +self.cost(reversed, self.get(i+1)))
        savings = oldCost - newCost
        if (savings > 0.0):
            self.patches[i] = reversed
            success = "#"
        else:
            success = "_"
        return success

    def traveling_salesman(self):
        #print >> sys.stderr, "TSPing %s patches" % len(self)

        # shockingly, this is non-optimal and pretty much non-efficient. Sorry.
        self.pointList = []
        for patch in self.patches:
            def visit(idx):
                ep = deepcopy(patch.stitches[idx])
                ep.patch = patch
                self.pointList.append(ep)

            visit(0)
            visit(-1)

        def linear_min(list, func):
            min_item = None
            min_value = None
            for item in list:
                value = func(item)
                #dbg.write('linear_min %s: value %s => %s (%s)\n' % (func, item, value, value<min_value))
                if (min_value==None or value<min_value):
                    min_item = item
                    min_value = value
            #dbg.write('linear_min final item %s value %s\n' % (min_item, min_value))
            return min_item

        sortedPatchList = PatchList([])
        def takePatchStartingAtPoint(point):
            patch = point.patch
            #dbg.write("takePatchStartingAtPoint angling for patch %s--%s\n" % (patch.stitches[0],patch.stitches[-1]))
            self.pointList = filter(lambda pt: pt.patch!=patch, self.pointList)
            reversed = ""
            if (point!=patch.stitches[0]):
                reversed = " (reversed)"
                #dbg.write('patch.stitches[0] %s point %s match %s\n' % (patch.stitches[0], point, point==patch.stitches[0]))
                patch = patch.reverse()
            sortedPatchList.patches.append(patch)
            #dbg.write('took patch %s--%s %s\n' % (patch.stitches[0], patch.stitches[-1], reversed))

        # Try a greedy algorithm starting from each point in turn, and pick
        # the best result.  O(n^2).

        min_cost = None
        min_path = []

        def mate(point):
            for p in self.pointList:
                if p is not point and p.patch == point.patch:
                    return p

        start_time = time.time()

        for starting_point in random.sample(self.pointList, len(self.pointList)):
            point_list = self.pointList[:]
            last_point = mate(starting_point)

            point_list.remove(starting_point)
            point_list.remove(last_point)

            path = [starting_point]
            cost = 0

            while point_list:
                next_point = min(point_list, key=lambda p: (p - last_point).length())
                cost += (next_point - last_point).length()

                path.append(next_point)
                last_point = mate(next_point)

                point_list.remove(next_point)
                try:
                    point_list.remove(last_point)
                except:
                    pass

            if min_cost is None or cost < min_cost:
                min_cost = cost
                min_path = path

            # timebox this bit to avoid spinning our wheels forever
            if time.time() - start_time > 1.0:
                break

        for point in min_path:
            takePatchStartingAtPoint(point)

        # install the initial result
        self.patches = sortedPatchList.patches

        if 1:
            # Then hill-climb.
            #dbg.write("len(self.patches) = %d\n" % len(self.patches))
            count = 0
            successStr = ""
            while (count < 100):
                i = random.randint(0, len(self.patches)-1)
                j = random.randint(0, len(self.patches)-1)
                successStr += self.try_swap(i,j)

                count += 1
            # tidy up at end as best we can
            for i in range(len(self.patches)):
                successStr += self.try_reverse(i)

            #dbg.write("success: %s\n" % successStr)

class EmbroideryObject:
    def __init__(self, patchList, row_spacing_px):
        self.patchList = patchList
        self.row_spacing_px = row_spacing_px


    def make_preamble_stitch(self, lastp, nextp):
        def fromPolar(r, phi):
            x = r * math.cos(phi)
            y = r * math.sin(phi)
            return (x, y)

        def toPolar(x, y):
            r = math.sqrt(x ** 2 + y ** 2)
            if r == 0:
                phi = 0
            elif y == 0:
                phi = 0 if x > 0 else math.pi
            else:
                phi = cmp(y, 0) * math.acos(x / r)
            return (r, phi)

        v = nextp - lastp
        (r, phi) = toPolar(v.x, v.y)

        PREAMBLE_MAX_DIST = 0.5 * pixels_per_millimeter  # 1/2mm
        if r < PREAMBLE_MAX_DIST:
            # nextp is close enough to lastp, so we don't generate
            # extra points in between, but just use nextp
            return nextp
        r = PREAMBLE_MAX_DIST
        (x, y) = fromPolar(r, phi)
        return PyEmb.Point(x, y) + lastp

    def emit_file(self, filename, output_format, collapse_len_px, add_preamble):
        emb = PyEmb.Embroidery()
        lastStitch = None
        lastColor = None
        for patch in self.patchList.patches:
            jumpStitch = True
            for stitch in patch.stitches:
                if lastStitch and lastColor == patch.color:
                    c = math.sqrt((stitch.x - lastStitch.x) ** 2 + (stitch.y - lastStitch.y) ** 2)
                    #dbg.write("stitch length: %f (%d/%d -> %d/%d)\n" % (c, lastStitch.x, lastStitch.y, stitch.x, stitch.y))

                    if c <= 0.1:
                        # filter out duplicate successive stitches
                        jumpStitch = False
                        continue

                    if jumpStitch:
                        # consider collapsing jump stich, if it is pretty short
                        if c < collapse_len_px:
                            #dbg.write("... collapsed\n")
                            jumpStitch = False

                #dbg.write("stitch color %s\n" % patch.color)

                newStitch = PyEmb.Point(stitch.x, -stitch.y)
                newStitch.color = patch.color
                newStitch.jumpStitch = jumpStitch
                emb.addStitch(newStitch)

                if jumpStitch and add_preamble != "0":
                    locs = [ newStitch ]
                    i = 0
                    nextp = PyEmb.Point(patch.stitches[i].x, -patch.stitches[i].y)

                    try:
                        for j in xrange(1, 4):
                            if locs[-1] == nextp:
                                i += 1
                                nextp = PyEmb.Point(patch.stitches[i].x, -patch.stitches[i].y)
                            locs.append(self.make_preamble_stitch(locs[-1], nextp))
                    except IndexError:
                        # happens when the patch is very short and we increment i beyond the number of stitches
                        pass
                    #dbg.write("preamble locations: %s\n" % locs)

                    for j in add_preamble[1:]:
                        try:
                            stitch = deepcopy(locs[int(j)])
                            stitch.color = patch.color
                            stitch.jumpStitch = False
                            emb.addStitch(stitch)
                        except IndexError:
                            pass

                jumpStitch = False
                lastStitch = newStitch
                lastColor = patch.color

        dx, dy = emb.translate_to_origin()
        emb.scale(1.0/pixels_per_millimeter)

        fp = open(filename, "wb")

        if output_format == "melco":
            fp.write(emb.export_melco(dbg))
        elif output_format == "csv":
            fp.write(emb.export_csv(dbg))
        elif output_format == "gcode":
            fp.write(emb.export_gcode(dbg))
        fp.close()
        emb.scale(pixels_per_millimeter)
        emb.translate(dx, dy)
        return emb

    def emit_inkscape(self, parent, emb):
        emb.scale((1, -1));
        for color, path in emb.export_paths(dbg):
            dbg.write('path: %s %s\n' % (color, repr(path)))
            inkex.etree.SubElement(parent,
                inkex.addNS('path', 'svg'),
                {    'style':simplestyle.formatStyle(
                        { 'stroke': color if color is not None else '#000000',
                            'stroke-width':"0.4",
                            'fill': 'none' }),
                    'd':simplepath.formatPath(path),
                })

    def bbox(self):
        x = []
        y = []
        for patch in self.patchList.patches:
            for stitch in patch.stitches:
                x.append(stitch.x)
                y.append(stitch.y)
        return (min(x), min(y), max(x), max(y))

class SortOrder:
    def __init__(self, *terms):
        self.sorttuple = terms

    def append(self, criterion):
        self.sorttuple += (criterion,)

    def __cmp__(self, other):
        return cmp(self.sorttuple, other.sorttuple)

    def __repr__(self):
        return "Sort%s" % self.sorttuple

class Embroider(inkex.Effect):
    def __init__(self, *args, **kwargs):
        #dbg.write("args: %s\n" % repr(sys.argv))
        inkex.Effect.__init__(self)
        self.stacking_order_counter = 0
        self.OptionParser.add_option("-r", "--row_spacing_mm",
            action="store", type="float",
            dest="row_spacing_mm", default=0.4,
            help="row spacing (mm)")
        self.OptionParser.add_option("-z", "--zigzag_spacing_mm",
            action="store", type="float",
            dest="zigzag_spacing_mm", default=1.0,
            help="zigzag spacing (mm)")
        self.OptionParser.add_option("-l", "--max_stitch_len_mm",
            action="store", type="float",
            dest="max_stitch_len_mm", default=3.0,
            help="max stitch length (mm)")
        self.OptionParser.add_option("--running_stitch_len_mm",
            action="store", type="float",
            dest="running_stitch_len_mm", default=3.0,
            help="running stitch length (mm)")
        self.OptionParser.add_option("-c", "--collapse_len_mm",
            action="store", type="float",
            dest="collapse_len_mm", default=0.0,
            help="max collapse length (mm)")
        self.OptionParser.add_option("-f", "--flatness",
            action="store", type="float",
            dest="flat", default=0.1,
            help="Minimum flatness of the subdivided curves")
        self.OptionParser.add_option("-o", "--order",
            action="store", type="choice",
            choices=["automatic", "layer", "object"],
            dest="order", default="automatic",
            help="patch stitching order")
        self.OptionParser.add_option("-H", "--hatch_filled_paths",
            action="store", type="choice",
            choices=["true","false"],
            dest="hatch_filled_paths", default="false",
            help="Use hatching lines instead of equally-spaced lines to fill paths")
        self.OptionParser.add_option("--hide_layers",
            action="store", type="choice",
            choices=["true","false"],
            dest="hide_layers", default="true",
            help="Hide all other layers when the embroidery layer is generated")
        self.OptionParser.add_option("-p", "--add_preamble",
            action="store", type="choice",
            choices=["0","010","01010","01210","012101210"],
            dest="add_preamble", default="0",
            help="Add preamble")
        self.OptionParser.add_option("-O", "--output_format",
            action="store", type="choice",
            choices=["melco", "csv", "gcode"],
            dest="output_format", default="melco",
            help="File output format")
        self.OptionParser.add_option("-P", "--path",
            action="store", type="string",
            dest="path", default=".",
            help="Directory in which to store output file")
        self.OptionParser.add_option("-b", "--max-backups",
            action="store", type="int",
            dest="max_backups", default=5,
            help="Max number of backups of output files to keep.")
        self.patches = []

    def get_sort_order(self, threadcolor, node):
        #print >> sys.stderr, "node", node.get("id"), self.order.get(node.get("id"))
        return SortOrder(self.order.get(node.get("id")), threadcolor)

    def process_one_path(self, node, shpath, threadcolor, sortorder, angle):
        #self.add_shapely_geo_to_svg(shpath.boundary, color="#c0c000")

        hatching = get_boolean_param(node, "hatching", self.hatching)
        flip = get_boolean_param(node, "flip", False)
        row_spacing_px = get_float_param(node, "row_spacing", self.row_spacing_px)
        max_stitch_len_px = get_float_param(node, "max_stitch_length", self.max_stitch_len_px)
        num_staggers = get_int_param(node, "staggers", 4)

        rows_of_segments = self.intersect_region_with_grating(shpath, row_spacing_px, angle, flip)
        groups_of_segments = self.pull_runs(rows_of_segments, shpath, row_spacing_px)
 
        # "east" is the name of the direction that is to the right along a row
        east = PyEmb.Point(1, 0).rotate(-angle)

        #print >> sys.stderr, len(groups_of_segments)

        patches = []
        for group_of_segments in groups_of_segments:
            patch = Patch(color=threadcolor,sortorder=sortorder)
            first_segment = True
            swap = False
            last_end = None

            for segment in group_of_segments:
                # We want our stitches to look like this:
                # 
                # ---*-----------*-----------
                # ------*-----------*--------
                # ---------*-----------*-----
                # ------------*-----------*--
                # ---*-----------*-----------
                #
                # Each successive row of stitches will be staggered, with
                # num_staggers rows before the pattern repeats.  A value of
                # 4 gives a nice fill while hiding the needle holes.  The
                # first row is offset 0%, the second 25%, the third 50%, and
                # the fourth 75%.
                #
                # Actually, instead of just starting at an offset of 0, we
                # can calculate a row's offset relative to the origin.  This
                # way if we have two abutting fill regions, they'll perfectly
                # tile with each other.  That's important because we often get
                # abutting fill regions from pull_runs().

                (beg, end) = segment

                if (swap):
                    (beg,end)=(end,beg)

                beg = PyEmb.Point(*beg)
                end = PyEmb.Point(*end)

                row_direction = (end - beg).unit()
                segment_length = (end - beg).length()

                # only stitch the first point if it's a reasonable distance away from the
                # last stitch
                if last_end is None or (beg - last_end).length() > 0.5 * pixels_per_millimeter:
                    patch.addStitch(beg)

                # Now, imagine the coordinate axes rotated by 'angle' degrees, such that
                # the rows are parallel to the X axis.  We can find the coordinates in these
                # axes of the beginning point in this way:
                relative_beg = beg.rotate(angle)

                absolute_row_num = round(relative_beg.y / row_spacing_px)
                row_stagger = absolute_row_num % num_staggers
                row_stagger_offset = (float(row_stagger) / num_staggers) * max_stitch_len_px

                first_stitch_offset = (relative_beg.x - row_stagger_offset) % max_stitch_len_px

                first_stitch = beg - east * first_stitch_offset

                # we might have chosen our first stitch just outside this row, so move back in
                if (first_stitch - beg) * row_direction < 0:
                    first_stitch += row_direction * max_stitch_len_px

                offset = (first_stitch - beg).length()

                while offset < segment_length:
                    patch.addStitch(beg + offset * row_direction)
                    offset += max_stitch_len_px

                if (end - patch.stitches[-1]).length() > 0.1 * pixels_per_millimeter:
                    patch.addStitch(end)

                last_end = end

                if not hatching:
                    swap = not swap

            patches.append(patch)
        return patches

    def intersect_region_with_grating(self, shpath, row_spacing_px, angle, flip=False):
        # the max line length I'll need to intersect the whole shape is the diagonal
        (minx, miny, maxx, maxy) = shpath.bounds
        upper_left = PyEmb.Point(minx, miny)
        lower_right = PyEmb.Point(maxx, maxy)
        length = (upper_left - lower_right).length()
        half_length = length / 2.0

        # Now get a unit vector rotated to the requested angle.  I use -angle
        # because shapely rotates clockwise, but my geometry textbooks taught
        # me to consider angles as counter-clockwise from the X axis.
        direction = PyEmb.Point(1, 0).rotate(-angle)

        # and get a normal vector
        normal = direction.rotate(math.pi/2)

        # I'll start from the center, move in the normal direction some amount,
        # and then walk left and right half_length in each direction to create
        # a line segment in the grating.
        center = PyEmb.Point((minx + maxx) / 2.0, (miny + maxy) / 2.0)

        # I need to figure out how far I need to go along the normal to get to
        # the edge of the shape.  To do that, I'll rotate the bounding box
        # angle degrees clockwise and ask for the new bounding box.  The max
        # and min y tell me how far to go.

        _, start, _, end = affinity.rotate(shpath, angle, origin='center', use_radians = True).bounds

        # convert start and end to be relative to center (simplifies things later)
        start -= center.y
        end -= center.y

        # offset start slightly so that rows are always an even multiple of
        # row_spacing_px from the origin.  This makes it so that abutting
        # fill regions at the same angle and spacing always line up nicely.
        start -= (start + normal * center) % row_spacing_px

        rows = []

        while start < end:
            p0 = center + normal.mul(start) + direction.mul(half_length)
            p1 = center + normal.mul(start) - direction.mul(half_length)
            endpoints = [p0.as_tuple(), p1.as_tuple()]
            shline = shgeo.LineString(endpoints)

            res = shline.intersection(shpath)

            if (isinstance(res, shgeo.MultiLineString)):
                runs = map(shapelyLineSegmentToPyTuple, res.geoms)
            else:
                if res.is_empty or len(res.coords) == 1:
                    # ignore if we intersected at a single point or no points
                    start += row_spacing_px
                    continue
                runs = [shapelyLineSegmentToPyTuple(res)]

            runs.sort(key=lambda seg: (PyEmb.Point(*seg[0]) - upper_left).length())

            if flip:
                runs.reverse()
                runs = map(reverseTuple, runs)

            if self.hatching and len(rows) > 0:
                rows.append([(rows[-1][0][1], runs[0][0])])

            rows.append(runs)

            start += row_spacing_px

        return rows

    def pull_runs(self, rows, shpath, row_spacing_px):
        # Given a list of rows, each containing a set of line segments,
        # break the area up into contiguous patches of line segments.
        #
        # This is done by repeatedly pulling off the first line segment in
        # each row and calling that a shape.  We have to be careful to make
        # sure that the line segments are part of the same shape.  Consider
        # the letter "H", with an embroidery angle of 45 degrees.  When
        # we get to the bottom of the lower left leg, the next row will jump
        # over to midway up the lower right leg.  We want to stop there and
        # start a new patch.

        # Segments more than this far apart are considered not to be part of
        # the same run.  
        row_distance_cutoff = row_spacing_px * 1.1

        def make_quadrilateral(segment1, segment2):
            return shgeo.Polygon((segment1[0], segment1[1], segment2[1], segment2[0], segment1[0]))

        def is_same_run(segment1, segment2):
            if self.options.hatch_filled_paths:
                return True

            if shgeo.LineString(segment1).distance(shgeo.LineString(segment1)) > row_spacing_px * 1.1:
                return False

            quad = make_quadrilateral(segment1, segment2)
            quad_area = quad.area
            intersection_area = shpath.intersection(quad).area

            return (intersection_area / quad_area) >= 0.9

        #for row in rows:
        #    print >> sys.stderr, len(row)

        #print >>sys.stderr, "\n".join(str(len(row)) for row in rows)

        runs = []
        count = 0
        while (len(rows) > 0):
            run = []
            prev = None

            for row_num in xrange(len(rows)):
                row = rows[row_num]
                first, rest = row[0], row[1:]

                # TODO: only accept actually adjacent rows here
                if prev is not None and not is_same_run(prev, first):
                    break
    
                run.append(first)
                prev = first

                rows[row_num] = rest

            #print >> sys.stderr, len(run)
            runs.append(run)
            rows = [row for row in rows if len(row) > 0]

            count += 1

        return runs

    def handle_node(self, node):
        if simplestyle.parseStyle(node.get("style")).get('display') == "none":
            return

        if node.tag == self.svgdefs:
            return

        for child in node:
            self.handle_node(child)

        if node.tag != self.svgpath:
            return

        #dbg.write("Node: %s\n"%str((id, etree.tostring(node, pretty_print=True))))

        if get_boolean_param(node, "satin_column"):
            self.patchList.patches.extend(self.satin_column(node))
        else:
            stroke = []
            fill = []

            if (self.get_style(node, "stroke")!=None):
                stroke = self.path_to_patch_list(node)
            if (self.get_style(node, "fill")!=None):
                fill = self.filled_region_to_patchlist(node)

            if get_boolean_param(node, "stroke_first", False):
                for patch in stroke:
                    patch.sortorder.append(0)

                for patch in fill:
                    patch.sortorder.append(1)

            self.patchList.patches.extend(stroke)
            self.patchList.patches.extend(fill)

    def get_style(self, node, style_name):
        style = simplestyle.parseStyle(node.get("style"))
        if (style_name not in style):
            return None
        value = style[style_name]
        if (value==None or value=="none"):
            return None
        return value

    def cache_order(self):
        if self.options.order == "automatic":
            self.order = defaultdict(lambda: 0)
            return

        self.order = {}

        layer_tag = inkex.addNS("g", "svg")
        group_attr = inkex.addNS('groupmode', 'inkscape')

        def is_layer(node):
            return node.tag == layer_tag and node.get(group_attr) == "layer"

        def process(node, order=0):
            if self.options.order == "object" or (self.options.order == "layer" and is_layer(node)):
                order += 1

            self.order[node.get("id")] = order

            for child in node:
                order = process(child, order)

            return order

        process(self.document.getroot())

    def get_output_path(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'))
        csv_filename = svg_filename.replace('.svg', '.csv')
        output_path = os.path.join(self.options.path, csv_filename)

        def add_suffix(path, suffix):
            if suffix > 0:
                path = "%s.%s" % (path, suffix)

            return path

        def move_if_exists(path, suffix=0):
            source = add_suffix(path, suffix)

            if suffix >= self.options.max_backups:
                return

            dest = add_suffix(path, suffix + 1)

            if os.path.exists(source):
                move_if_exists(path, suffix + 1)
                os.rename(source, dest)

        move_if_exists(output_path)

        return output_path

    def effect(self):
        # Printing anything other than a valid SVG on stdout blows inkscape up.
        old_stdout = sys.stdout
        sys.stdout = sys.stderr

        self.cache_order()
        #print >> sys.stderr, "cached stacking order:", self.order

        self.row_spacing_px = self.options.row_spacing_mm * pixels_per_millimeter
        self.zigzag_spacing_px = self.options.zigzag_spacing_mm * pixels_per_millimeter
        self.max_stitch_len_px = self.options.max_stitch_len_mm*pixels_per_millimeter
        self.running_stitch_len_px = self.options.running_stitch_len_mm*pixels_per_millimeter
        self.collapse_len_px = self.options.collapse_len_mm*pixels_per_millimeter
        self.hatching = self.options.hatch_filled_paths == "true"

        self.svgpath = inkex.addNS('path', 'svg')
        self.svgdefs = inkex.addNS('defs', 'svg')
        self.patchList = PatchList([])

        dbg.write("starting nodes: %s" % time.time())
        dbg.flush()
        if self.selected:
            for node in self.selected.itervalues():
                self.handle_node(node)
        else:
            self.handle_node(self.document.getroot())
        dbg.write("finished nodes: %s" % time.time())
        dbg.flush()

        if not self.patchList:
            if self.selected:
                inkex.errormsg("No embroiderable paths selected.")
            else:
                inkex.errormsg("No embroiderable paths found in document.")
            inkex.errormsg("Tip: use Path -> Object to Path to convert non-paths before embroidering.")
            return

        dbg.write("starting tsp: %s" % time.time())
        self.patchList = self.patchList.tsp_by_color()
        dbg.write("finished tsp: %s" % time.time())
        #dbg.write("patch count: %d\n" % len(self.patchList.patches))

        if self.options.hide_layers:
            self.hide_layers()

        eo = EmbroideryObject(self.patchList, self.row_spacing_px)
        emb = eo.emit_file(self.get_output_path(), self.options.output_format,
                 self.collapse_len_px, self.options.add_preamble)

        new_layer = inkex.etree.SubElement(self.document.getroot(),
                inkex.addNS('g', 'svg'), {})
        new_layer.set('id', self.uniqueId("embroidery"))
        new_layer.set(inkex.addNS('label', 'inkscape'), 'Embroidery')
        new_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        eo.emit_inkscape(new_layer, emb)

        sys.stdout = old_stdout

    def emit_inkscape_bbox(self, parent, eo):
        (x0, y0, x1, y1) = eo.bbox()
        new_path = []
        new_path.append(['M', (x0,y0)])
        new_path.append(['L', (x1,y0)])
        new_path.append(['L', (x1,y1)])
        new_path.append(['L', (x0,y1)])
        new_path.append(['L', (x0,y0)])
        inkex.etree.SubElement(parent,
            inkex.addNS('path', 'svg'),
            {    'style':simplestyle.formatStyle(
                    { 'stroke': '#ff00ff',
                        'stroke-width':str(1),
                        'fill': 'none' }),
                'd':simplepath.formatPath(new_path),
            })

    def hide_layers(self):
        for g in self.document.getroot().findall(inkex.addNS("g","svg")):
            if g.get(inkex.addNS("groupmode", "inkscape")) == "layer":
                g.set("style", "display:none")

    def path_to_patch_list(self, node):
        threadcolor = simplestyle.parseStyle(node.get("style"))["stroke"]
        stroke_width_str = simplestyle.parseStyle(node.get("style"))["stroke-width"]
        if (stroke_width_str.endswith("px")):
            # don't really know how we should be doing unit conversions.
            # but let's hope px are kind of like pts?
            stroke_width_str = stroke_width_str[:-2]
        stroke_width = float(stroke_width_str)
        dashed = self.get_style(node, "stroke-dasharray") is not None
        #dbg.write("stroke_width is <%s>\n" % repr(stroke_width))
        #dbg.flush()

        running_stitch_len_px = get_float_param(node, "stitch_length", self.running_stitch_len_px)
        zigzag_spacing_px = get_float_param(node, "zigzag_spacing", self.zigzag_spacing_px)
        repeats = get_int_param(node, "repeats", 1)

        sortorder = self.get_sort_order(threadcolor, node)
        paths = flatten(parse_path(node), self.options.flat)

        # regularize the points lists.
        # (If we're parsing beziers, there will be a list of multi-point
        # subarrays.)

        patches = []

        for path in paths:
            path = [PyEmb.Point(x, y) for x, y in path]
            if (stroke_width <= STROKE_MIN or dashed):
                #dbg.write("self.max_stitch_len_px = %s\n" % self.max_stitch_len_px)
                patch = self.stroke_points(path, running_stitch_len_px, 0.0, repeats, threadcolor, sortorder)
            else:
                patch = self.stroke_points(path, zigzag_spacing_px*0.5, stroke_width, repeats, threadcolor, sortorder)
            patches.extend(patch)

        return patches

    def stroke_points(self, emb_point_list, zigzag_spacing_px, stroke_width, repeats, threadcolor, sortorder):
        patch = Patch(color=threadcolor, sortorder=sortorder)
        p0 = emb_point_list[0]
        rho = 0.0
        fact = 1
        last_segment_direction = None

        for repeat in xrange(repeats):
            if repeat % 2 == 0:
                order = range(1, len(emb_point_list))
            else:
                order = range(-2, -len(emb_point_list) - 1, -1)

            for segi in order:
                p1 = emb_point_list[segi]

                # how far we have to go along segment
                seg_len = (p1 - p0).length()
                if (seg_len == 0):
                    continue

                # vector pointing along segment
                along = (p1 - p0).unit()
                # vector pointing to edge of stroke width
                perp = along.rotate_left().mul(stroke_width*0.5)

                if stroke_width == 0.0 and last_segment_direction is not None:
                    if abs(1.0 - along * last_segment_direction) > 0.5:
                        # if greater than 45 degree angle, stitch the corner
                        #print >> sys.stderr, "corner", along * last_segment_direction
                        rho = zigzag_spacing_px
                        patch.addStitch(p0)

                # iteration variable: how far we are along segment
                while (rho <= seg_len):
                    left_pt = p0+along.mul(rho)+perp.mul(fact)
                    patch.addStitch(left_pt)
                    rho += zigzag_spacing_px
                    fact = -fact

                p0 = p1
                last_segment_direction = along
                rho -= seg_len

            if (p0 - patch.stitches[-1]).length() > 0.1:
                patch.addStitch(p0)

        return [patch]

    def filled_region_to_patchlist(self, node):
        angle = math.radians(float(get_float_param(node,'angle',0)))
        paths = flatten(parse_path(node), self.options.flat)
        shapelyPolygon = cspToShapelyPolygon(paths)
        threadcolor = simplestyle.parseStyle(node.get("style"))["fill"]
        sortorder = self.get_sort_order(threadcolor, node)
        return self.process_one_path(
                node,
                shapelyPolygon,
                threadcolor,
                sortorder,
                angle)

    def fatal(self, message):
        print >> sys.stderr, "error:", message
        sys.exit(1)

    def validate_satin_column(self, node, csp):
        node_id = node.get("id")

        if len(csp) != 2:
            self.fatal("satin column: object %s invalid: expected exactly two sub-paths, but there are %s" % (node_id, len(csp)))

        if self.get_style(node, "fill")!=None:
            self.fatal("satin column: object %s has a fill (but should not)" % node_id)

        if len(csp[0]) != len(csp[1]):
            self.fatal("satin column: object %s has two paths with an unequal number of points (%s and %s)" % (node_id, len(csp[0]), len(csp[1])))

    def satin_column(self, node):
        # Stitch a variable-width satin column, zig-zagging between two paths.

        # The node should have exactly two paths with no fill.  Each
        # path should have the same number of points.  The two paths will be
        # split into segments, and each segment will have a number of zigzags
        # defined by the length of the longer of the two segments, divided
        # by the zigzag spacing parameter.

        id = node.get("id")

        # First, verify that we have a valid node.
        csp = parse_path(node)
        self.validate_satin_column(node, csp)

        # fetch parameters
        zigzag_spacing_px = get_float_param(node, "zigzag_spacing", self.zigzag_spacing_px)
        pull_compensation_px = get_float_param(node, "pull_compensation", 0)
        underlay_inset = get_float_param(node, "satin_underlay_inset", 0)
        underlay_stitch_len_px = get_float_param(node, "stitch_length", self.running_stitch_len_px)
        underlay = get_boolean_param(node, "satin_underlay", False)
        center_walk = get_boolean_param(node, "satin_center_walk", False)
        zigzag_underlay_spacing = get_float_param(node, "satin_zigzag_underlay_spacing", 0)
        zigzag_underlay_inset = underlay_inset / 2.0

        # A path is a collection of tuples, each of the form:
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
        # A "superpath" is a collection of paths that are all in one object.
        # The "cubic" bit in "cubic superpath" is because the bezier curves
        # inkscape uses involve cubic polynomials.
        #
        # In a path, each element in the 3-tuple is itself a tuple of (x, y).
        # Tuples all the way down.  Hasn't anyone heard of using classes?

        path1 = csp[0]
        path2 = csp[1]

        threadcolor = simplestyle.parseStyle(node.get("style"))["stroke"]
        sortorder = self.get_sort_order(threadcolor, node)
        patch = Patch(color=threadcolor, sortorder=sortorder)

        def offset_points(pos1, pos2, offset_px):
            # Expand or contract points.  This is useful for pull
            # compensation and insetting underlay.

            distance = (pos1 - pos2).length()

            if (pos1 - pos2).length() < 0.0001:
                # if they're the same, we don't know which direction
                # to offset in, so we have to just return the points
                return pos1, pos2

            # if offset is negative, don't contract so far that pos1
            # and pos2 switch places
            if offset_px < -distance/2.0:
                offset_px = -distance/2.0 

            midpoint = (pos2 + pos1) * 0.5
            pos1 = pos1 + (pos1 - midpoint).unit() * offset_px
            pos2 = pos2 + (pos2 - midpoint).unit() * offset_px
    
            return pos1, pos2
    
        def walk_paths(spacing, offset):
            # Take a bezier segment from each path in turn, and plot out an
            # equal number of points on each side.  Later code can alternate
            # between these points to create satin stitch, underlay, etc.

            side1 = []
            side2 = []
    
            def add_pair(pos1, pos2):
                # Stitches in satin tend to pull toward each other.  We can compensate
                # by spreading the points out.
                pos1, pos2 = offset_points(pos1, pos2, offset)
                side1.append(pos1)
                side2.append(pos2)
    
            remainder_path1 = []
            remainder_path2 = []
    
            for segment in xrange(1, len(path1)):
                # construct the current bezier segments
                bezier1 = (path1[segment - 1][1], # point from previous 3-tuple
                           path1[segment - 1][2], # "after" control point from previous 3-tuple
                           path1[segment][0], # "before" control point from this 3-tuple
                           path1[segment][1], # point from this 3-tuple
                          )
    
                bezier2 = (path2[segment - 1][1],
                           path2[segment - 1][2],
                           path2[segment][0],
                           path2[segment][1],
                          )
    
                # Here's what I want to be able to do.  However, beziertatlength is so incredibly slow that it's unusable.
                #for stitch in xrange(num_zigzags):
                #    patch.addStitch(bezierpointatt(bezier1, beziertatlength(bezier1, stitch_len1 * stitch)))
                #    patch.addStitch(bezierpointatt(bezier2, beziertatlength(bezier2, stitch_len2 * (stitch + 0.5))))
    
                # Instead, flatten the beziers down to a set of line segments.
                subpath1 = remainder_path1 + flatten([[path1[segment - 1], path1[segment]]], self.options.flat)[0]
                subpath2 = remainder_path2 + flatten([[path2[segment - 1], path2[segment]]], self.options.flat)[0]
    
                len1 = shgeo.LineString(subpath1).length
                len2 = shgeo.LineString(subpath2).length
    
                subpath1 = [PyEmb.Point(*p) for p in subpath1]
                subpath2 = [PyEmb.Point(*p) for p in subpath2]
    
                # Base the number of stitches in each section on the _longest_ of
                # the two beziers. Otherwise, things could get too sparse when one
                # side is significantly longer (e.g. when going around a corner).
                # The risk here is that we poke a hole in the fabric if we try to
                # cram too many stitches on the short bezier.  The user will need
                # to avoid this through careful construction of paths.
                num_points = max(len1, len2) / spacing
    
                spacing1 = len1 / num_points
                spacing2 = len2 / num_points
    
                def walk(path, start_pos, start_index, distance):
                    # Move <distance> pixels along <path>'s line segments.
                    # <start_index> is the index of the line segment in <path> that
                    # we're currently on.  <start_pos> is where along that line
                    # segment we are.  Return a new position and index.
    
                    pos = start_pos
                    index = start_index
    
                    if index >= len(path) - 1:
                        # it's possible we'll go too far due to inaccuracy in the
                        # bezier length calculation
                        return start_pos, start_index
    
                    while True:
                        segment_end = path[index + 1]
                        segment_remaining = (segment_end - pos)
                        distance_remaining = segment_remaining.length()
    
                        if distance_remaining > distance:
                            return pos + segment_remaining.unit().mul(distance), index
                        else:
                            index += 1
    
                            if index >= len(path) - 1:
                                return segment_end, index
    
                            distance -= distance_remaining
                            pos = segment_end
    
                pos1 = subpath1[0]
                i1 = 0
    
                pos2 = subpath2[0]
                i2 = 0
    
    #            if num_zigzags >= 1.0:
    #                for stitch in xrange(int(num_zigzags) + 1):
                for i in xrange(int(num_points)):
                    add_pair(pos1, pos2)
    
                    pos2, i2 = walk(subpath2, pos2, i2, spacing2)
                    pos1, i1 = walk(subpath1, pos1, i1, spacing1)
    
                if i1 < len(subpath1) - 1:
                    remainder_path1 = [pos1] + subpath1[i1 + 1:]
                else:
                    remainder_path1 = []
    
                if i2 < len(subpath2) - 1:
                    remainder_path2 = [pos2] + subpath2[i2 + 1:]
                else:
                    remainder_path2 = []
    
                remainder_path1 = [p.as_tuple() for p in remainder_path1]
                remainder_path2 = [p.as_tuple() for p in remainder_path2]
    
            # We're off by one in the algorithm above, so we need one more
            # pair of points.  We also want to add points at the very end to
            # make sure we match the vectors on screen as best as possible.
            # Try to avoid doing both if they're going to stack up too
            # closely.
 
            end1 = PyEmb.Point(*remainder_path1[-1])
            end2 = PyEmb.Point(*remainder_path2[-1])
            if (end1 - pos1).length() > 0.3 * spacing:
                add_pair(pos1, pos2)

            add_pair(end1, end2)

            return [side1, side2]

        def calculate_underlay(inset):
            # "contour walk" underlay: do stitches up one side and down the
            # other.
            forward, back = walk_paths(underlay_stitch_len_px, -inset)
            return Patch(color=threadcolor, sortorder=sortorder, stitches=(forward + list(reversed(back))))

        def calculate_zigzag_underlay(zigzag_spacing, inset):
            # zigzag underlay, usually done at a much lower density than the
            # satin itself.  It looks like this:
            #
            # \/\/\/\/\/\/\/\/\/\/|
            # /\/\/\/\/\/\/\/\/\/\|
            #
            # In combination with the "contour walk" underlay, this is the
            # "German underlay" described here:
            #   http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/

            patch = Patch(color=threadcolor, sortorder=sortorder)

            sides = walk_paths(zigzag_spacing/2.0, -inset)
            sides = [sides[0][::2] + list(reversed(sides[0][1::2])), sides[1][1::2] + list(reversed(sides[1][::2]))] 

            # this fancy bit of iterable magic just repeatedly takes a point
            # from each list in turn
            for point in chain.from_iterable(izip(*sides)):
                patch.addStitch(point)

            return patch

        def calculate_satin(zigzag_spacing, pull_compensation):
            # satin: do a zigzag pattern, alternating between the paths.  The
            # zigzag looks like this:
            #
            # /|/|/|/|/|/|/|/|

            patch = Patch(color=threadcolor, sortorder=sortorder)

            sides = walk_paths(zigzag_spacing, pull_compensation)

            for point in chain.from_iterable(izip(*sides)):
                patch.addStitch(point)

            return patch

        if center_walk:
            # Center walk is a running stitch exactly between the paths, down
            # and back.  It comes first.

            # Bit of a hack: do it just like contour walk underlay but inset it
            # really far.  The inset will be clamped to the center between the
            # paths.
            patch += calculate_underlay(10000)

        if underlay:
            # Now do the contour walk underlay.
            patch += calculate_underlay(underlay_inset)

        if zigzag_underlay_spacing:
            # zigzag underlay comes after contour walk underlay, so that the
            # zigzags sit on the contour walk underlay like rail ties on rails.
            patch += calculate_zigzag_underlay(zigzag_underlay_spacing, zigzag_underlay_inset)

        # Finally, add the satin itself.
        patch += calculate_satin(zigzag_spacing_px, pull_compensation_px)

        return [patch]

if __name__ == '__main__':
    sys.setrecursionlimit(100000);
    e = Embroider()
    e.affect()
    #dbg.write("aaaand, I'm done. seeeya!\n")
    dbg.flush()

dbg.close()
