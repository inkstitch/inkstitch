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
import inkex
import simplepath
import simplestyle
import simpletransform
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
        return s and s.lower in ('yes', 'y', 'true', 't', '1')

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

def dupNodeAttrs(node):
    n2 = E.node()
    for k in node.attrib.keys():
        n2.attrib[k] = node.attrib[k]
    del n2.attrib["id"]
    del n2.attrib["d"]
    return n2

class Patch:
    def __init__(self, color, sortorder, stitches=None):
        self.color = color
        self.sortorder = sortorder
        if (stitches!=None):
            self.stitches = stitches
        else:
            self.stitches = []

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

        for starting_point in self.pointList:
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
                point_list.remove(last_point)

            if min_cost is None or cost < min_cost:
                min_cost = cost
                min_path = path

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

                    if c == 0:
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
                            'stroke-width':"1",
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
    def __init__(self, threadcolor, layer, preserve_layers):
        self.threadcolor = threadcolor
        if (preserve_layers):
            #dbg.write("preserve_layers is true: %s %s\n" % (layer, threadcolor));
            self.sorttuple = (layer, threadcolor)
        else:
            #dbg.write("preserve_layers is false:\n");
            self.sorttuple = (threadcolor,)

    def __cmp__(self, other):
        return cmp(self.sorttuple, other.sorttuple)

    def __repr__(self):
        return "sort %s color %s" % (self.sorttuple, self.threadcolor)

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
        self.OptionParser.add_option("-o", "--preserve_layers",
            action="store", type="choice",
            choices=["true","false"],
            dest="preserve_layers", default="false",
            help="Sort by stacking order instead of color")
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
        self.OptionParser.add_option("-F", "--filename",
            action="store", type="string",
            dest="filename", default="embroider-output.exp",
            help="Name (and possibly path) of output file")
        self.patches = []
        self.layer_cache = {}

    def get_sort_order(self, threadcolor, node):
        #print >> sys.stderr, "node", node.get("id"), self.layer_cache.get(node.get("id"))
        return SortOrder(threadcolor, self.layer_cache.get(node.get("id")), self.options.preserve_layers=="true")

    def process_one_path(self, node, shpath, threadcolor, sortorder, angle):
        #self.add_shapely_geo_to_svg(shpath.boundary, color="#c0c000")

        hatching = get_boolean_param(node, "hatching", self.hatching)
        row_spacing_px = get_float_param(node, "row_spacing", self.row_spacing_px)
        max_stitch_len_px = get_float_param(node, "max_stitch_length", self.max_stitch_len_px)

        rows_of_segments = self.intersect_region_with_grating(shpath, row_spacing_px, angle)
        segments = self.visit_segments_one_by_one(rows_of_segments, shpath)

        def small_stitches(patch, beg, end):
            vector = (end-beg)
            patch.addStitch(beg)
            old_dist = vector.length()
            if (old_dist < max_stitch_len_px):
                patch.addStitch(end)
                return
            one_stitch = vector.mul(1.0 / old_dist * max_stitch_len_px * random.random())
            beg = beg + one_stitch
            while (True):
                vector = (end-beg)
                dist = vector.length()
                assert(old_dist==None or dist<old_dist)
                old_dist = dist
                patch.addStitch(beg)
                if (dist < max_stitch_len_px):
                    patch.addStitch(end)
                    return

                one_stitch = vector.mul(1.0/dist*max_stitch_len_px)
                beg = beg + one_stitch

        swap = False
        patch = Patch(color=threadcolor,sortorder=sortorder)
        for (beg,end) in segments:
            if (swap):
                (beg,end)=(end,beg)
            if not hatching:
                swap = not swap
            small_stitches(patch, PyEmb.Point(*beg),PyEmb.Point(*end))
        return [patch]

    def intersect_region_with_grating(self, shpath, row_spacing_px, angle):
        # the max line length I'll need to intersect the whole shape is the diagonal
        (minx, miny, maxx, maxy) = shpath.bounds
        length = (PyEmb.Point(maxx, maxy) - PyEmb.Point(minx, miny)).length()
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
        start -= center.y
        end -= center.y

        # don't start right at the edge or we'll make a ridiculous single
        # stitch
        start += row_spacing_px / 2.0

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
                runs = [shapelyLineSegmentToPyTuple(res)]

            if self.hatching and len(rows) > 0:
                rows.append([(rows[-1][0][1], runs[0][0])])

            rows.append(runs)

            start += row_spacing_px
        return rows

    def visit_segments_one_by_one(self, rows, shpath):
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

        def make_quadrilateral(segment1, segment2):
            return shgeo.Polygon((segment1[0], segment1[1], segment2[1], segment2[0], segment1[0]))

        def pull_runs(rows):
            new_rows = []
            run = []
            prev = None
            done = False
            for r in rows:
                if done:
                    new_rows.append(r)
                    continue

                (first,rest) = (r[0], r[1:])

                if prev is not None:
                    quad = make_quadrilateral(prev, first)
                    quad_area = quad.area
                    intersection_area = shpath.intersection(quad).area

                    if intersection_area / quad_area < .9:
                        new_rows.append(r)
                        done = True
                        continue

                run.append(first)
                prev = first
                if (len(rest)>0):
                    new_rows.append(rest)
            return (run, new_rows)

        linearized_runs = []
        count = 0
        while (len(rows) > 0):
            (one_run,rows) = pull_runs(rows)
            linearized_runs.extend(one_run)

            rows = rows[::-1]
            count += 1
        return linearized_runs

    def handle_node(self, node):
        if (node.tag == inkex.addNS('g', 'svg')):
            #dbg.write("%s\n"%str((id, etree.tostring(node, pretty_print=True))))
            #dbg.write("not a path; recursing:\n")
            for child in node.iter(self.svgpath):
                self.handle_node(child)
            return

        #dbg.write("Node: %s\n"%str((id, etree.tostring(node, pretty_print=True))))

        israw = parse_boolean(node.get('embroider_raw'))
        if (israw):
            self.patchList.patches.extend(self.path_to_patch_list(node))
        else:
            if (self.get_style(node, "fill")!=None):
                self.patchList.patches.extend(self.filled_region_to_patchlist(node))
            if (self.get_style(node, "stroke")!=None):
                self.patchList.patches.extend(self.path_to_patch_list(node))

    def get_style(self, node, style_name):
        style = simplestyle.parseStyle(node.get("style"))
        if (style_name not in style):
            return None
        value = style[style_name]
        if (value==None or value=="none"):
            return None
        return value

    def cache_layers(self):
        self.layer_cache = {}

        layer_tag = inkex.addNS("g", "svg")
        group_attr = inkex.addNS('groupmode', 'inkscape')


        def is_layer(node):
            return node.tag == layer_tag and node.get(group_attr) == "layer"

        def process(node, layer=0):
            if is_layer(node):
                layer += 1
            else:
                self.layer_cache[node.get("id")] = layer

            for child in node:
                layer = process(child, layer)

            return layer

        process(self.document.getroot())

    def effect(self):
        if self.options.preserve_layers == "true":
            self.cache_layers()
            #print >> sys.stderr, "cached stacking order:", self.stacking_order

        self.row_spacing_px = self.options.row_spacing_mm * pixels_per_millimeter
        self.zigzag_spacing_px = self.options.zigzag_spacing_mm * pixels_per_millimeter
        self.max_stitch_len_px = self.options.max_stitch_len_mm*pixels_per_millimeter
        self.running_stitch_len_px = self.options.running_stitch_len_mm*pixels_per_millimeter
        self.collapse_len_px = self.options.collapse_len_mm*pixels_per_millimeter
        self.hatching = self.options.hatch_filled_paths == "true"

        self.svgpath = inkex.addNS('path', 'svg')
        self.patchList = PatchList([])
        for node in self.selected.itervalues():
            self.handle_node(node)

        if not self.patchList:
            inkex.errormsg("No paths selected.")
            return

        self.patchList = self.patchList.tsp_by_color()
        #dbg.write("patch count: %d\n" % len(self.patchList.patches))

        if self.options.hide_layers:
            self.hide_layers()

        eo = EmbroideryObject(self.patchList, self.row_spacing_px)
        emb = eo.emit_file(self.options.filename, self.options.output_format,
                 self.collapse_len_px, self.options.add_preamble)

        new_layer = inkex.etree.SubElement(self.document.getroot(),
                inkex.addNS('g', 'svg'), {})
        new_layer.set('id', self.uniqueId("embroidery"))
        new_layer.set(inkex.addNS('label', 'inkscape'), 'Embroidery')
        new_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        eo.emit_inkscape(new_layer, emb)

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
            if (stroke_width <= STROKE_MIN):
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

                # iteration variable: how far we are along segment
                while (rho <= seg_len):
                    left_pt = p0+along.mul(rho)+perp.mul(fact)
                    patch.addStitch(left_pt)
                    rho += zigzag_spacing_px
                    fact = -fact

                p0 = p1
                rho -= seg_len

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

    #TODO def make_stroked_patch(self, node):

if __name__ == '__main__':
    sys.setrecursionlimit(100000);
    e = Embroider()
    e.affect()
    #dbg.write("aaaand, I'm done. seeeya!\n")
    dbg.flush()

dbg.close()
