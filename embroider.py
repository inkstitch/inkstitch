#!/usr/bin/python
#
# documentation: see included index.html
# LICENSE:
# This code is copyright 2010 by Jon Howell,
# licensed under <a href="http://www.gnu.org/licenses/quick-guide-gplv3.html">GPLv3</a>.
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
# 

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
from copy import deepcopy
import time
import inkex
import simplepath
import simplestyle
import cspsubdiv
import cubicsuperpath
import PyEmb
import math
import random
import operator
import lxml.etree as etree
from lxml.builder import E
import shapely.geometry as shgeo

dbg = open("embroider-debug.txt", "w")
PyEmb.dbg = dbg
pixels_per_millimeter = 90.0 / 25.4

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
		for csp in sub_path:
			pt = (csp[1][0],csp[1][1])
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

	def sort_by_sortorder(self):
		def by_sort_order(a,b):
			return cmp(a.sortorder, b.sortorder)
		self.patches.sort(by_sort_order)

	def partition_by_color(self):
		self.sort_by_sortorder()
		dbg.write("Sorted by sortorder:\n");
		dbg.write("  %s\n" % ("\n".join(map(lambda p: str(p.sortorder), self.patches))))
		out = []
		lastPatch = None
		for patch in self.patches:
			if (lastPatch!=None and patch.color==lastPatch.color):
				out[-1].patches.append(patch)
			else:
				out.append(PatchList([patch]))
			lastPatch = patch
		dbg.write("Emitted %s partitions\n" % len(out))
		return out
		
	def tsp_by_color(self):
		list_of_patchLists = self.partition_by_color()
		for patchList in list_of_patchLists:
			patchList.traveling_salesman()
		return PatchList(reduce(operator.add,
			map(lambda pl: pl.patches, list_of_patchLists)))

#	# TODO apparently dead code; replaced by partition_by_color above
#	def clump_like_colors_together(self):
#		out = PatchList([])
#		lastPatch = None
#		for patch in self.patches:
#			if (lastPatch!=None and patch.color==lastPatch.color):
#				out.patches[-1] = Patch(
#					out.patches[-1].color,
#					out.patches[-1].sortorder,
#					out.patches[-1].stitches+patch.stitches)
#			else:
#				out.patches.append(patch)
#			lastPatch = patch
#		return out

	def get(self, i):
		if (i<0 or i>=len(self.patches)):
			return None
		return self.patches[i]

	def cost(self, a, b):
		if (a==None or b==None):
			rc = 0.0
		else:
			rc = (a.stitches[-1] - b.stitches[0]).length()
		#dbg.write("cost(%s, %s) = %5.1f\n" % (a, b, rc))
		return rc

	def try_swap(self, i, j):
		# i,j are indices;
		dbg.write("swap(%d, %d)\n" % (i,j))
		oldCost = (
			 self.cost(self.get(i-1), self.get(i))
			+self.cost(self.get(i), self.get(i+1))
			+self.cost(self.get(j-1), self.get(j))
			+self.cost(self.get(j), self.get(j+1)))
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
			return (
				 self.cost(self.get(i-1), npi)
				+self.cost(npi, self.get(i+1))
				+self.cost(self.get(j-1), npj)
				+self.cost(npj, self.get(j+1)))
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

		dbg.write("old %5.1f new %5.1f savings: %5.1f\n" % (oldCost, cost, savings))
		return success

	def try_reverse(self, i):
		dbg.write("reverse(%d)\n" % i)
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
		self.centroid = PyEmb.Point(0.0,0.0)
		self.pointList = []
		for patch in self.patches:
			def visit(idx):
				ep = deepcopy(patch.stitches[idx])
				ep.patch = patch
				self.centroid+=ep
				self.pointList.append(ep)

			visit(0)
			visit(-1)

		self.centroid = self.centroid.mul(1.0/float(len(self.pointList)))

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
			dbg.write("takePatchStartingAtPoint angling for patch %s--%s\n" % (
				patch.stitches[0],
				patch.stitches[-1]))
			self.pointList = filter(lambda pt: pt.patch!=patch, self.pointList)
			reversed = ""
			if (point!=patch.stitches[0]):
				reversed = " (reversed)"
				dbg.write('patch.stitches[0] %s point %s match %s\n' % (
					patch.stitches[0],
					point,
					point==patch.stitches[0]))
				patch = patch.reverse()
			sortedPatchList.patches.append(patch)
			dbg.write('took patch %s--%s %s\n' % (
				patch.stitches[0],
				patch.stitches[-1],
				reversed))

		# Take the patch farthest from the centroid first
		# O(n)
		dbg.write('centroid: %s\n' % self.centroid)
		def neg_distance_from_centroid(p):
			return -(p-self.centroid).length()
		farthestPoint = linear_min(self.pointList, neg_distance_from_centroid)
		takePatchStartingAtPoint(farthestPoint)
		#sortedPatchList.patches[0].color = "#000000"

		# Then greedily take closer-and-closer patches
		# O(n^2)
		while (len(self.pointList)>0):
			dbg.write('pass %s\n' % len(self.pointList));
			last_point = sortedPatchList.patches[-1].stitches[-1]
			dbg.write('last_point now %s\n' % last_point)
			def distance_from_last_point(p):
				return (p-last_point).length()
			nearestPoint = linear_min(self.pointList, distance_from_last_point)
			takePatchStartingAtPoint(nearestPoint)

		# install the initial result
		self.patches = sortedPatchList.patches

		if (1):
			# Then hill-climb.
			dbg.write("len(self.patches) = %d\n" % len(self.patches))
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

			dbg.write("success: %s\n" % successStr)

class EmbroideryObject:
	def __init__(self, patchList, row_spacing_px):
		self.patchList = patchList
		self.row_spacing_px = row_spacing_px

	def emit_file(self, filename, output_format):
		emb = PyEmb.Embroidery()
		for patch in self.patchList.patches:
			jumpStitch = True
			for stitch in patch.stitches:
				dbg.write("stitch color %s\n" % patch.color)

				newStitch = PyEmb.Point(stitch.x, -stitch.y)
				newStitch.color = patch.color
				newStitch.jumpStitch = jumpStitch
				emb.addStitch(newStitch)

				jumpStitch = False

		emb.translate_to_origin()
		emb.scale(10.0/pixels_per_millimeter)

		fp = open(filename, "wb")

		if output_format == "melco":
			fp.write(emb.export_melco(dbg))
		elif output_format == "csv":
			fp.write(emb.export_csv(dbg))
		fp.close()

	def emit_inkscape(self, parent):
		lastPatch = None
		for patch in self.patchList.patches:
			if (lastPatch!=None):
				# draw jump stitch
				inkex.etree.SubElement(parent,
					inkex.addNS('path', 'svg'),
					{	'style':simplestyle.formatStyle(
							{ 'stroke': lastPatch.color,
								'stroke-width':str(self.row_spacing_px*.25),
								'stroke-dasharray':'0.99, 1.98',
								'fill': 'none' }),
						'd':simplepath.formatPath([
							['M', (lastPatch.stitches[-1].as_tuple())],
							['L', (patch.stitches[0].as_tuple())]
						]),
					})
			lastPatch = patch
				
			new_path = []
			new_path.append(['M', patch.stitches[0].as_tuple()])
			for stitch in patch.stitches[1:]:
				new_path.append(['L', stitch.as_tuple()])
			inkex.etree.SubElement(parent,
				inkex.addNS('path', 'svg'),
				{	'style':simplestyle.formatStyle(
						{ 'stroke': patch.color,
							'stroke-width':str(self.row_spacing_px*0.25),
							'fill': 'none' }),
					'd':simplepath.formatPath(new_path),
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
	def __init__(self, threadcolor, stacking_order, preserve_order):
		self.threadcolor = threadcolor
		if (preserve_order):
			dbg.write("preserve_order is true:\n");
			self.sorttuple = (stacking_order, threadcolor)
		else:
			dbg.write("preserve_order is false:\n");
			self.sorttuple = (threadcolor, stacking_order)

	def __cmp__(self, other):
		return cmp(self.sorttuple, other.sorttuple)
	
	def __repr__(self):
		return "sort %s color %s" % (self.sorttuple, self.threadcolor)

class Embroider(inkex.Effect):
	def __init__(self, *args, **kwargs):
		dbg.write("args: %s\n" % repr(sys.argv))
		inkex.Effect.__init__(self)
		self.stacking_order_counter = 0
		self.OptionParser.add_option("-r", "--row_spacing_mm",
			action="store", type="float",
			dest="row_spacing_mm", default=0.4,
			help="row spacing (mm)")
		self.OptionParser.add_option("-l", "--max_stitch_len_mm",
			action="store", type="float",
			dest="max_stitch_len_mm", default=3.0,
			help="max stitch length (mm)")
		self.OptionParser.add_option("-f", "--flatness",
			action="store", type="float", 
			dest="flat", default=0.1,
			help="Minimum flatness of the subdivided curves")
		self.OptionParser.add_option("-o", "--preserve_order",
			action="store", type="choice", 
			choices=["true","false"],
			dest="preserve_order", default="false",
			help="Sort by stacking order instead of color")
		self.OptionParser.add_option("-O", "--output_format",
			action="store", type="choice",
			choices=["melco", "csv"],
			dest="output_format", default="melco",
			help="File output format")
		self.OptionParser.add_option("-F", "--filename",
			action="store", type="string",
			dest="filename", default="embroider-output.exp",
			help="Name (and possibly path) of output file")
		self.patches = []

	def get_sort_order(self, threadcolor):
		self.stacking_order_counter += 1
		return SortOrder(threadcolor, self.stacking_order_counter, self.options.preserve_order=="true")

	def process_one_path(self, shpath, threadcolor, sortorder):
		#self.add_shapely_geo_to_svg(shpath.boundary, color="#c0c000")

		rows_of_segments = self.intersect_region_with_grating(shpath)
		segments = self.visit_segments_one_by_one(rows_of_segments)

		def small_stitches(patch, beg, end):
			old_dist = None
			while (True):
				vector = (end-beg)
				dist = vector.length()
				assert(old_dist==None or dist<old_dist)
				old_dist = dist
				patch.addStitch(beg)
				if (dist < self.max_stitch_len_px):
					patch.addStitch(end)
					return

				one_stitch = vector.mul(1.0/dist*self.max_stitch_len_px)
				beg = beg + one_stitch
				
		swap = False
		patches = []
		for (beg,end) in segments:
			patch = Patch(color=threadcolor,sortorder=sortorder)
			if (swap):
				(beg,end)=(end,beg)
			swap = not swap
			small_stitches(patch, PyEmb.Point(*beg),PyEmb.Point(*end))
			patches.append(patch)
		return patches

	def intersect_region_with_grating(self, shpath):
		dbg.write("bounds = %s\n" % str(shpath.bounds))
		bbox = shpath.bounds
		
		delta = self.row_spacing_px/2.0
		bbox_sz = (bbox[2]-bbox[0],bbox[3]-bbox[1])
		if (bbox_sz[0] > bbox_sz[1]):
			# wide box, use vertical stripes
			p0 = PyEmb.Point(bbox[0]-delta,bbox[1])
			p1 = PyEmb.Point(bbox[0]-delta,bbox[3])
			p_inc = PyEmb.Point(self.row_spacing_px, 0)
			count = (bbox[2]-bbox[0])/self.row_spacing_px + 2
		else:
			# narrow box, use horizontal stripes
			p0 = PyEmb.Point(bbox[0], bbox[1]-delta)
			p1 = PyEmb.Point(bbox[2], bbox[1]-delta)
			p_inc = PyEmb.Point(0, self.row_spacing_px)
			count = (bbox[3]-bbox[1])/self.row_spacing_px + 2

		rows = []
		steps = 0
		while (steps < count):
			try:
				steps += 1
				p0 += p_inc
				p1 += p_inc
				endpoints = [p0.as_tuple(), p1.as_tuple()]
				shline = shgeo.LineString(endpoints)
				res = shline.intersection(shpath)
				if (isinstance(res, shgeo.MultiLineString)):
					runs = map(shapelyLineSegmentToPyTuple, res.geoms)
				else:
					runs = [shapelyLineSegmentToPyTuple(res)]
				rows.append(runs)
			except Exception, ex:
				dbg.write("--------------\n")
				dbg.write("%s\n" % ex)
				dbg.write("%s\n" % shline)
				dbg.write("%s\n" % shpath)
				dbg.write("==============\n")
				continue
		return rows
		
	def visit_segments_one_by_one(self, rows):
		def pull_runs(rows):
			new_rows = []
			run = []
			for r in rows:
				(first,rest) = (r[0], r[1:])
				run.append(first)
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
			if (count>100): raise "kablooey"
		return linearized_runs

	def handle_node(self, node):

		if (node.tag != self.svgpath):
			dbg.write("%s\n"%str((id, etree.tostring(node, pretty_print=True))))
			dbg.write("not a path; recursing:\n")
			for child in node.iter(self.svgpath):
				self.handle_node(child)
			return

		dbg.write("Node: %s\n"%str((id, etree.tostring(node, pretty_print=True))))

		israw = False
		desc = node.findtext(inkex.addNS('desc', 'svg'))
		if (desc!=None):
			israw = desc.find("embroider_raw")>=0
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
		
	def effect(self):
		self.row_spacing_px = self.options.row_spacing_mm * pixels_per_millimeter
		self.max_stitch_len_px = self.options.max_stitch_len_mm*pixels_per_millimeter 

		self.svgpath = inkex.addNS('path', 'svg')
		self.patchList = PatchList([])
		for id, node in self.selected.iteritems():
			self.handle_node(node)

		self.patchList = self.patchList.tsp_by_color()
		dbg.write("patch count: %d\n" % len(self.patchList.patches))

		eo = EmbroideryObject(self.patchList, self.row_spacing_px)
		eo.emit_file(self.options.filename, self.options.output_format)

		new_group = inkex.etree.SubElement(self.current_layer,
				inkex.addNS('g', 'svg'), {})
		eo.emit_inkscape(new_group)

		self.emit_inkscape_bbox(new_group, eo)

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
			{	'style':simplestyle.formatStyle(
					{ 'stroke': '#ff00ff',
						'stroke-width':str(1),
						'fill': 'none' }),
				'd':simplepath.formatPath(new_path),
			})

	def path_to_patch_list(self, node):
		threadcolor = simplestyle.parseStyle(node.get("style"))["stroke"]
		stroke_width_str = simplestyle.parseStyle(node.get("style"))["stroke-width"]
		if (stroke_width_str.endswith("px")):
			# don't really know how we should be doing unit conversions.
			# but let's hope px are kind of like pts?
			stroke_width_str = stroke_width_str[:-2]
		stroke_width = float(stroke_width_str)
		dbg.write("stroke_width is <%s>\n" % repr(stroke_width))
		dbg.flush()
		sortorder = self.get_sort_order(threadcolor)
		path = simplepath.parsePath(node.get("d"))

		# regularize the points lists.
		# (If we're parsing beziers, there will be a list of multi-point
		# subarrays.)

		patches = []
		emb_point_list = []

		def flush_point_list():
			STROKE_MIN = 0.5	# a 0.5pt stroke becomes a straight line.
			if (stroke_width <= STROKE_MIN):
				dbg.write("self.max_stitch_len_px = %s\n" % self.max_stitch_len_px)
				patch = self.stroke_points(emb_point_list, self.max_stitch_len_px, 0.0, threadcolor, sortorder)
			else:
				patch = self.stroke_points(emb_point_list, self.row_spacing_px*0.5, stroke_width, threadcolor, sortorder)
			patches.extend(patch)

		close_point = None
		for (type,points) in path:
			dbg.write("path_to_patch_list parses pt %s with type=%s\n" % (points, type))
			if type == 'M' and len(emb_point_list):
				flush_point_list()
				emb_point_list = []

			if type == 'Z':
				dbg.write("... closing patch to %s\n" % close_point)
				emb_point_list.append(close_point)
			else:
				pointscopy = list(points)
				while (len(pointscopy)>0):
					emb_point_list.append(PyEmb.Point(pointscopy[0], pointscopy[1]))
					pointscopy = pointscopy[2:]
			if type == 'M':
				dbg.write("latching close_point %s\n" % emb_point_list[-1])
				close_point = emb_point_list[-1]

		flush_point_list()
		return patches

	def stroke_points(self, emb_point_list, row_spacing_px, stroke_width, threadcolor, sortorder):
		patch = Patch(color=threadcolor, sortorder=sortorder)
		p0 = emb_point_list[0]
		for segi in range(1, len(emb_point_list)):
			p1 = emb_point_list[segi]

			# how far we have to go along segment
			seg_len = (p1 - p0).length()
			if (seg_len < row_spacing_px*0.5):
				# hmm. segment so short we can't do much sane with
				# it. Ignore the point p1 and move along (but keep p0
				# as the beginning).
				continue;

			# vector pointing along segment
			along = (p1 - p0).unit()
			# vector pointing to edge of stroke width
			perp = along.rotate_left().mul(stroke_width*0.5)

			# iteration variable: how far we are along segment
			rho = 0.0
			while (rho <= seg_len):
				left_pt = p0+along.mul(rho)+perp
				patch.addStitch(left_pt)
				rho += row_spacing_px
				if (rho > seg_len):
					break

				right_pt = p0+along.mul(rho)+perp.mul(-1.0)
				patch.addStitch(right_pt)
				rho += row_spacing_px

			# make sure we turn sharp corners when stroking thin paths.
			patch.addStitch(p1)

			p0 = p1

		return [patch]

	def filled_region_to_patchlist(self, node):
		p = cubicsuperpath.parsePath(node.get("d"))
		cspsubdiv.cspsubdiv(p, self.options.flat)
		shapelyPolygon = cspToShapelyPolygon(p)
		threadcolor = simplestyle.parseStyle(node.get("style"))["fill"]
		sortorder = self.get_sort_order(threadcolor)
		return self.process_one_path(
				shapelyPolygon,
				threadcolor,
				sortorder)

	#TODO def make_stroked_patch(self, node):

if __name__ == '__main__':
	sys.setrecursionlimit(100000);
	e = Embroider()
	e.affect()
	dbg.write("aaaand, I'm done. seeeya!\n")
	dbg.flush()

dbg.close()
