#!/usr/bin/python
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
import traceback
sys.path.append("/usr/share/inkscape/extensions")
import os
import subprocess
from copy import deepcopy
import time
from itertools import chain, izip, groupby
from collections import deque
import inkex
import simplepath
import simplestyle
import simpletransform
from bezmisc import bezierlength, beziertatlength, bezierpointatt
from cspsubdiv import cspsubdiv
import cubicsuperpath
import math
import lxml.etree as etree
import shapely.geometry as shgeo
import shapely.affinity as affinity
import shapely.ops
import networkx
from pprint import pformat

import inkstitch
from inkstitch import _, cache, dbg, param, EmbroideryElement, get_nodes, SVG_POLYLINE_TAG, SVG_GROUP_TAG, PIXELS_PER_MM, get_viewbox_transform
from inkstitch.stitches import running_stitch
from inkstitch.utils import cut_path

class Fill(EmbroideryElement):
    element_name = _("Fill")

    def __init__(self, *args, **kwargs):
        super(Fill, self).__init__(*args, **kwargs)

    @property
    @param('auto_fill', _('Manually routed fill stitching'), type='toggle', inverse=True, default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @param('angle', _('Angle of lines of stitches'), unit='deg', type='float', default=0)
    @cache
    def angle(self):
        return math.radians(self.get_float_param('angle', 0))

    @property
    def color(self):
        return self.get_style("fill")

    @property
    @param('flip', _('Flip fill (start right-to-left)'), type='boolean', default=False)
    def flip(self):
        return self.get_boolean_param("flip", False)

    @property
    @param('row_spacing_mm', _('Spacing between rows'), unit='mm', type='float', default=0.25)
    def row_spacing(self):
        return max(self.get_float_param("row_spacing_mm", 0.25), 0.01)

    @property
    def end_row_spacing(self):
        return self.get_float_param("end_row_spacing_mm")

    @property
    @param('max_stitch_length_mm', _('Maximum fill stitch length'), unit='mm', type='float', default=3.0)
    def max_stitch_length(self):
        return max(self.get_float_param("max_stitch_length_mm", 3.0), 0.01)

    @property
    @param('staggers', _('Stagger rows this many times before repeating'), type='int', default=4)
    def staggers(self):
        return self.get_int_param("staggers", 4)

    @property
    @cache
    def paths(self):
        return self.flatten(self.parse_path())

    @property
    @cache
    def shape(self):
        poly_ary = []
        for sub_path in self.paths:
            point_ary = []
            last_pt = None
            for pt in sub_path:
                if (last_pt is not None):
                    vp = (pt[0] - last_pt[0], pt[1] - last_pt[1])
                    dp = math.sqrt(math.pow(vp[0], 2.0) + math.pow(vp[1], 2.0))
                    # dbg.write("dp %s\n" % dp)
                    if (dp > 0.01):
                        # I think too-close points confuse shapely.
                        point_ary.append(pt)
                        last_pt = pt
                else:
                    last_pt = pt
            if point_ary:
                poly_ary.append(point_ary)

        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        # TODO: actually figure out which things are holes and which are shells
        poly_ary.sort(key=lambda point_list: shgeo.Polygon(point_list).area, reverse=True)

        polygon = shgeo.MultiPolygon([(poly_ary[0], poly_ary[1:])])
        # print >> sys.stderr, "polygon valid:", polygon.is_valid
        return polygon

    @cache
    def east(self, angle):
        # "east" is the name of the direction that is to the right along a row
        return inkstitch.Point(1, 0).rotate(-angle)

    @cache
    def north(self, angle):
        return self.east(angle).rotate(math.pi / 2)

    def row_num(self, point, angle, row_spacing):
        return round((point * self.north(angle)) / row_spacing)

    def adjust_stagger(self, stitch, angle, row_spacing, max_stitch_length):
        row_num = self.row_num(stitch, angle, row_spacing)
        row_stagger = row_num % self.staggers
        stagger_offset = (float(row_stagger) / self.staggers) * max_stitch_length
        offset = ((stitch * self.east(angle)) - stagger_offset) % max_stitch_length

        return stitch - offset * self.east(angle)

    def intersect_region_with_grating(self, angle=None, row_spacing=None, end_row_spacing=None):
        if angle is None:
            angle = self.angle

        if row_spacing is None:
            row_spacing = self.row_spacing

        if end_row_spacing is None:
            end_row_spacing = self.end_row_spacing

        # the max line length I'll need to intersect the whole shape is the diagonal
        (minx, miny, maxx, maxy) = self.shape.bounds
        upper_left = inkstitch.Point(minx, miny)
        lower_right = inkstitch.Point(maxx, maxy)
        length = (upper_left - lower_right).length()
        half_length = length / 2.0

        # Now get a unit vector rotated to the requested angle.  I use -angle
        # because shapely rotates clockwise, but my geometry textbooks taught
        # me to consider angles as counter-clockwise from the X axis.
        direction = inkstitch.Point(1, 0).rotate(-angle)

        # and get a normal vector
        normal = direction.rotate(math.pi / 2)

        # I'll start from the center, move in the normal direction some amount,
        # and then walk left and right half_length in each direction to create
        # a line segment in the grating.
        center = inkstitch.Point((minx + maxx) / 2.0, (miny + maxy) / 2.0)

        # I need to figure out how far I need to go along the normal to get to
        # the edge of the shape.  To do that, I'll rotate the bounding box
        # angle degrees clockwise and ask for the new bounding box.  The max
        # and min y tell me how far to go.

        _, start, _, end = affinity.rotate(self.shape, angle, origin='center', use_radians=True).bounds

        # convert start and end to be relative to center (simplifies things later)
        start -= center.y
        end -= center.y

        height = abs(end - start)

        print >> dbg, "grating:", start, end, height, row_spacing, end_row_spacing

        # offset start slightly so that rows are always an even multiple of
        # row_spacing_px from the origin.  This makes it so that abutting
        # fill regions at the same angle and spacing always line up nicely.
        start -= (start + normal * center) % row_spacing

        rows = []

        current_row_y = start

        while current_row_y < end:
            p0 = center + normal * current_row_y + direction * half_length
            p1 = center + normal * current_row_y - direction * half_length
            endpoints = [p0.as_tuple(), p1.as_tuple()]
            grating_line = shgeo.LineString(endpoints)

            res = grating_line.intersection(self.shape)

            if (isinstance(res, shgeo.MultiLineString)):
                runs = map(lambda line_string: line_string.coords, res.geoms)
            else:
                if res.is_empty or len(res.coords) == 1:
                    # ignore if we intersected at a single point or no points
                    runs = []
                else:
                    runs = [res.coords]

            if runs:
                runs.sort(key=lambda seg: (inkstitch.Point(*seg[0]) - upper_left).length())

                if self.flip:
                    runs.reverse()
                    runs = map(lambda run: tuple(reversed(run)), runs)

                rows.append(runs)

            if end_row_spacing:
                current_row_y += row_spacing + (end_row_spacing - row_spacing) * ((current_row_y - start) / height)
            else:
                current_row_y += row_spacing

        return rows

    def make_quadrilateral(self, segment1, segment2):
        return shgeo.Polygon((segment1[0], segment1[1], segment2[1], segment2[0], segment1[0]))

    def is_same_run(self, segment1, segment2):
        if shgeo.LineString(segment1).distance(shgeo.LineString(segment2)) > self.row_spacing * 1.1:
            return False

        quad = self.make_quadrilateral(segment1, segment2)
        quad_area = quad.area
        intersection_area = self.shape.intersection(quad).area

        return (intersection_area / quad_area) >= 0.9

    def pull_runs(self, rows):
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

        # for row in rows:
        #    print >> sys.stderr, len(row)

        # print >>sys.stderr, "\n".join(str(len(row)) for row in rows)

        runs = []
        count = 0
        while (len(rows) > 0):
            run = []
            prev = None

            for row_num in xrange(len(rows)):
                row = rows[row_num]
                first, rest = row[0], row[1:]

                # TODO: only accept actually adjacent rows here
                if prev is not None and not self.is_same_run(prev, first):
                    break

                run.append(first)
                prev = first

                rows[row_num] = rest

            # print >> sys.stderr, len(run)
            runs.append(run)
            rows = [row for row in rows if len(row) > 0]

            count += 1

        return runs

    def stitch_row(self, patch, beg, end, angle, row_spacing, max_stitch_length):
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


        beg = inkstitch.Point(*beg)
        end = inkstitch.Point(*end)

        row_direction = (end - beg).unit()
        segment_length = (end - beg).length()

        # only stitch the first point if it's a reasonable distance away from the
        # last stitch
        if not patch.stitches or (beg - patch.stitches[-1]).length() > 0.5 * PIXELS_PER_MM:
            patch.add_stitch(beg)

        first_stitch = self.adjust_stagger(beg, angle, row_spacing, max_stitch_length)

        # we might have chosen our first stitch just outside this row, so move back in
        if (first_stitch - beg) * row_direction < 0:
            first_stitch += row_direction * max_stitch_length

        offset = (first_stitch - beg).length()

        while offset < segment_length:
            patch.add_stitch(beg + offset * row_direction)
            offset += max_stitch_length

        if (end - patch.stitches[-1]).length() > 0.1 * PIXELS_PER_MM:
            patch.add_stitch(end)


    def section_to_patch(self, group_of_segments, angle=None, row_spacing=None, max_stitch_length=None):
        if max_stitch_length is None:
            max_stitch_length = self.max_stitch_length

        if row_spacing is None:
            row_spacing = self.row_spacing

        if angle is None:
            angle = self.angle

        # print >> sys.stderr, len(groups_of_segments)

        patch = Patch(color=self.color)
        first_segment = True
        swap = False
        last_end = None

        for segment in group_of_segments:
            (beg, end) = segment

            if (swap):
                (beg, end) = (end, beg)

            self.stitch_row(patch, beg, end, angle, row_spacing, max_stitch_length)

            swap = not swap

        return patch

    def to_patches(self, last_patch):
        rows_of_segments = self.intersect_region_with_grating()
        groups_of_segments = self.pull_runs(rows_of_segments)

        return [self.section_to_patch(group) for group in groups_of_segments]


class MaxQueueLengthExceeded(Exception):
    pass

class AutoFill(Fill):
    element_name = _("Auto-Fill")

    @property
    @param('auto_fill', _('Automatically routed fill stitching'), type='toggle', default=True)
    def auto_fill(self):
        return self.get_boolean_param('auto_fill', True)

    @property
    @cache
    def outline(self):
        return self.shape.boundary[0]

    @property
    @cache
    def outline_length(self):
        return self.outline.length

    @property
    def flip(self):
        return False

    @property
    @param('running_stitch_length_mm', _('Running stitch length (traversal between sections)'), unit='mm', type='float', default=1.5)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('fill_underlay', _('Underlay'), type='toggle', group=_('AutoFill Underlay'), default=False)
    def fill_underlay(self):
        return self.get_boolean_param("fill_underlay", default=False)

    @property
    @param('fill_underlay_angle', _('Fill angle (default: fill angle + 90 deg)'), unit='deg', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_angle(self):
        underlay_angle = self.get_float_param("fill_underlay_angle")

        if underlay_angle:
            return math.radians(underlay_angle)
        else:
            return self.angle + math.pi / 2.0

    @property
    @param('fill_underlay_row_spacing_mm', _('Row spacing (default: 3x fill row spacing)'), unit='mm', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_row_spacing(self):
        return self.get_float_param("fill_underlay_row_spacing_mm") or self.row_spacing * 3

    @property
    @param('fill_underlay_max_stitch_length_mm', _('Max stitch length'), unit='mm', group=_('AutoFill Underlay'), type='float')
    @cache
    def fill_underlay_max_stitch_length(self):
        return self.get_float_param("fill_underlay_max_stitch_length_mm") or self.max_stitch_length

    def which_outline(self, coords):
        """return the index of the outline on which the point resides

        Index 0 is the outer boundary of the fill region.  1+ are the
        outlines of the holes.
        """

        # I'd use an intersection check, but floating point errors make it
        # fail sometimes.

        point = shgeo.Point(*coords)
        outlines = list(enumerate(self.shape.boundary))
        closest = min(outlines, key=lambda (index, outline): outline.distance(point))

        return closest[0]

    def project(self, coords, outline_index):
        """project the point onto the specified outline

        This returns the distance along the outline at which the point resides.
        """

        return self.shape.boundary.project(shgeo.Point(*coords))

    def build_graph(self, segments, angle, row_spacing):
        """build a graph representation of the grating segments

        This function builds a specialized graph (as in graph theory) that will
        help us determine a stitching path.  The idea comes from this paper:

        http://www.sciencedirect.com/science/article/pii/S0925772100000158

        The goal is to build a graph that we know must have an Eulerian Path.
        An Eulerian Path is a path from edge to edge in the graph that visits
        every edge exactly once and ends at the node it started at.  Algorithms
        exist to build such a path, and we'll use Hierholzer's algorithm.

        A graph must have an Eulerian Path if every node in the graph has an
        even number of edges touching it.  Our goal here is to build a graph
        that will have this property.

        Based on the paper linked above, we'll build the graph as follows:

          * nodes are the endpoints of the grating segments, where they meet
            with the outer outline of the region the outlines of the interior
            holes in the region.
          * edges are:
            * each section of the outer and inner outlines of the region,
              between nodes
            * double every other edge in the outer and inner hole outlines

        Doubling up on some of the edges seems as if it will just mean we have
        to stitch those spots twice.  This may be true, but it also ensures
        that every node has 4 edges touching it, ensuring that a valid stitch
        path must exist.
        """

        graph = networkx.MultiGraph()

        # First, add the grating segments as edges.  We'll use the coordinates
        # of the endpoints as nodes, which networkx will add automatically.
        for segment in segments:
            # networkx allows us to label nodes with arbitrary data.  We'll
            # mark this one as a grating segment.
            graph.add_edge(*segment, key="segment")

        for node in graph.nodes():
            outline_index = self.which_outline(node)
            outline_projection = self.project(node, outline_index)

            # Tag each node with its index and projection.
            graph.add_node(node, index=outline_index, projection=outline_projection)

        nodes = list(graph.nodes(data=True)) # returns a list of tuples: [(node, {data}), (node, {data}) ...]
        nodes.sort(key=lambda node: (node[1]['index'], node[1]['projection']))

        for outline_index, nodes in groupby(nodes, key=lambda node: node[1]['index']):
            nodes = [ node for node, data in nodes ]

            # heuristic: change the order I visit the nodes in the outline if necessary.
            # If the start and endpoints are in the same row, I can't tell which row
            # I should treat it as being in.
            for i in xrange(len(nodes)):
                row0 = self.row_num(inkstitch.Point(*nodes[0]), angle, row_spacing)
                row1 = self.row_num(inkstitch.Point(*nodes[1]), angle, row_spacing)

                if row0 == row1:
                    nodes = nodes[1:] + [nodes[0]]
                else:
                    break

            # heuristic: it's useful to try to keep the duplicated edges in the same rows.
            # this prevents the BFS from having to search a ton of edges.
            row_num = min(row0, row1)
            if row_num % 2 == 0:
                edge_set = 0
            else:
                edge_set = 1

            #print >> sys.stderr, outline_index, "es", edge_set, "rn", row_num, inkstitch.Point(*nodes[0]) * self.north(angle), inkstitch.Point(*nodes[1]) * self.north(angle)

            # add an edge between each successive node
            for i, (node1, node2) in enumerate(zip(nodes, nodes[1:] + [nodes[0]])):
                graph.add_edge(node1, node2, key="outline")

                # duplicate edges contained in every other row (exactly half
                # will be duplicated)
                row_num = min(self.row_num(inkstitch.Point(*node1), angle, row_spacing),
                              self.row_num(inkstitch.Point(*node2), angle, row_spacing))

                # duplicate every other edge around this outline
                if i % 2 == edge_set:
                    graph.add_edge(node1, node2, key="extra")


        if not networkx.is_eulerian(graph):
            raise Exception(_("Unable to autofill.  This most often happens because your shape is made up of multiple sections that aren't connected."))

        return graph

    def node_list_to_edge_list(self, node_list):
        return zip(node_list[:-1], node_list[1:])

    def bfs_for_loop(self, graph, starting_node, max_queue_length=2000):
        to_search = deque()
        to_search.appendleft(([starting_node], set(), 0))

        while to_search:
            if len(to_search) > max_queue_length:
                raise MaxQueueLengthExceeded()

            path, visited_edges, visited_segments = to_search.pop()
            ending_node = path[-1]

            # get a list of neighbors paired with the key of the edge I can follow to get there
            neighbors = [
                        (node, key)
                            for node, adj in graph.adj[ending_node].iteritems()
                            for key in adj
                    ]

            # heuristic: try grating segments first
            neighbors.sort(key=lambda (dest, key): key == "segment", reverse=True)

            for next_node, key in neighbors:
                # skip if I've already followed this edge
                edge = (tuple(sorted((ending_node, next_node))), key)
                if edge in visited_edges:
                    continue

                new_path = path + [next_node]

                if key == "segment":
                    new_visited_segments = visited_segments + 1
                else:
                    new_visited_segments = visited_segments

                if next_node == starting_node:
                    # ignore trivial loops (down and back a doubled edge)
                    if len(new_path) > 3:
                        return self.node_list_to_edge_list(new_path), new_visited_segments

                new_visited_edges = visited_edges.copy()
                new_visited_edges.add(edge)

                to_search.appendleft((new_path, new_visited_edges, new_visited_segments))

    def find_loop(self, graph, starting_nodes):
        """find a loop in the graph that is connected to the existing path

        Start at a candidate node and search through edges to find a path
        back to that node.  We'll use a breadth-first search (BFS) in order to
        find the shortest available loop.

        In most cases, the BFS should not need to search far to find a loop.
        The queue should stay relatively short.

        An added heuristic will be used: if the BFS queue's length becomes
        too long, we'll abort and try a different starting point.  Due to
        the way we've set up the graph, there's bound to be a better choice
        somewhere else.
        """

        #loop = self.simple_loop(graph, starting_nodes[-2])

        #if loop:
        #    print >> sys.stderr, "simple_loop success"
        #    starting_nodes.pop()
        #    starting_nodes.pop()
        #    return loop

        loop = None
        retry = []
        max_queue_length = 2000

        while not loop:
            while not loop and starting_nodes:
                starting_node = starting_nodes.pop()
                #print >> sys.stderr, "find loop from", starting_node

                try:
                    # Note: if bfs_for_loop() returns None, no loop can be
                    # constructed from the starting_node (because the
                    # necessary edges have already been consumed).  In that
                    # case we discard that node and try the next.
                    loop = self.bfs_for_loop(graph, starting_node, max_queue_length)

                    if not loop:
                        print >> dbg, "failed on", starting_node
                        dbg.flush()
                except MaxQueueLengthExceeded:
                    print >> dbg, "gave up on", starting_node
                    dbg.flush()
                    # We're giving up on this node for now.  We could try
                    # this node again later, so add it to the bottm of the
                    # stack.
                    retry.append(starting_node)

            # Darn, couldn't find a loop.  Try harder.
            starting_nodes.extendleft(retry)
            max_queue_length *= 2

        starting_nodes.extendleft(retry)
        return loop

    def insert_loop(self, path, loop):
        """insert a sub-loop into an existing path

        The path will be a series of edges describing a path through the graph
        that ends where it starts.  The loop will be similar, and its starting
        point will be somewhere along the path.

        Insert the loop into the path, resulting in a longer path.

        Both the path and the loop will be a list of edges specified as a
        start and end point.  The points will be specified in order, such
        that they will look like this:

        ((p1, p2), (p2, p3), (p3, p4) ... (pn, p1))

        path will be modified in place.
        """

        loop_start = loop[0][0]

        for i, (start, end) in enumerate(path):
            if start == loop_start:
                break

        path[i:i] = loop

    def find_stitch_path(self, graph, segments):
        """find a path that visits every grating segment exactly once

        Theoretically, we just need to find an Eulerian Path in the graph.
        However, we don't actually care whether every single edge is visited.
        The edges on the outline of the region are only there to help us get
        from one grating segment to the next.

        We'll build a "cycle" (a path that ends where it starts) using
        Hierholzer's algorithm.  We'll stop once we've visited every grating
        segment.

        Hierholzer's algorithm says to select an arbitrary starting node at
        each step.  In order to produce a reasonable stitch path, we'll select
        the vertex carefully such that we get back-and-forth traversal like
        mowing a lawn.

        To do this, we'll use a simple heuristic: try to start from nodes in
        the order of most-recently-visited first.
        """

        original_graph = graph
        graph = graph.copy()
        num_segments = len(segments)
        segments_visited = 0
        nodes_visited = deque()

        # start with a simple loop: down one segment and then back along the
        # outer border to the starting point.
        path = [segments[0], list(reversed(segments[0]))]

        graph.remove_edges_from(path)

        segments_visited += 1
        nodes_visited.extend(segments[0])

        while segments_visited < num_segments:
            result = self.find_loop(graph, nodes_visited)

            if not result:
                print >> sys.stderr, _("Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.")
                break

            loop, segments = result

            print >> dbg, "found loop:", loop
            dbg.flush()

            segments_visited += segments
            nodes_visited += [edge[0] for edge in loop]
            graph.remove_edges_from(loop)

            self.insert_loop(path, loop)

            #if segments_visited >= 12:
            #    break

        # Now we have a loop that covers every grating segment.  It returns to
        # where it started, which is unnecessary, so we'll snip the last bit off.
        #while original_graph.has_edge(*path[-1], key="outline"):
        #    path.pop()

        return path

    def collapse_sequential_outline_edges(self, graph, path):
        """collapse sequential edges that fall on the same outline

        When the path follows multiple edges along the outline of the region,
        replace those edges with the starting and ending points.  We'll use
        these to stitch along the outline later on.
        """

        start_of_run = None
        new_path = []

        for edge in path:
            if graph.has_edge(*edge, key="segment"):
                if start_of_run:
                    # close off the last run
                    new_path.append((start_of_run, edge[0]))
                    start_of_run = None

                new_path.append(edge)
            else:
                if not start_of_run:
                    start_of_run = edge[0]

        if start_of_run:
            # if we were still in a run, close it off
            new_path.append((start_of_run, edge[1]))

        return new_path

    def outline_distance(self, outline, p1, p2):
        # how far around the outline (and in what direction) do I need to go
        # to get from p1 to p2?

        p1_projection = outline.project(shgeo.Point(p1))
        p2_projection = outline.project(shgeo.Point(p2))

        distance = p2_projection - p1_projection

        if abs(distance) > self.outline_length / 2.0:
            # if we'd have to go more than halfway around, it's faster to go
            # the other way
            if distance < 0:
                return distance + self.outline_length
            elif distance > 0:
                return distance - self.outline_length
            else:
                # this ought not happen, but just for completeness, return 0 if
                # p1 and p0 are the same point
                return 0
        else:
            return distance

    def connect_points(self, patch, start, end):
        outline_index = self.which_outline(start)
        outline = self.shape.boundary[outline_index]

        pos = outline.project(shgeo.Point(start))
        distance = self.outline_distance(outline, start, end)
        stitches = abs(int(distance / self.running_stitch_length))

        direction = math.copysign(1.0, distance)
        one_stitch = self.running_stitch_length * direction

        print >> dbg, "connect_points:", outline_index, start, end, distance, stitches, direction
        dbg.flush()

        patch.add_stitch(inkstitch.Point(*start))

        for i in xrange(stitches):
            pos = (pos + one_stitch) % self.outline_length

            patch.add_stitch(inkstitch.Point(*outline.interpolate(pos).coords[0]))

        end = inkstitch.Point(*end)
        if (end - patch.stitches[-1]).length() > 0.1 * PIXELS_PER_MM:
            patch.add_stitch(end)

        print >> dbg, "end connect_points"
        dbg.flush()

    def path_to_patch(self, graph, path, angle, row_spacing, max_stitch_length):
        path = self.collapse_sequential_outline_edges(graph, path)

        patch = Patch(color=self.color)
        #patch.add_stitch(inkstitch.Point(*path[0][0]))

        #for edge in path:
        #    patch.add_stitch(inkstitch.Point(*edge[1]))

        for edge in path:
            if graph.has_edge(*edge, key="segment"):
                self.stitch_row(patch, edge[0], edge[1], angle, row_spacing, max_stitch_length)
            else:
                self.connect_points(patch, *edge)

        return patch

    def do_auto_fill(self, angle, row_spacing, max_stitch_length, starting_point=None):
        patches = []

        print >> dbg, "start do_auto_fill"
        dbg.flush()

        rows_of_segments = self.intersect_region_with_grating(angle, row_spacing)
        segments = [segment for row in rows_of_segments for segment in row]

        graph = self.build_graph(segments, angle, row_spacing)
        path = self.find_stitch_path(graph, segments)

        if starting_point:
            patch = Patch(self.color)
            self.connect_points(patch, starting_point, path[0][0])
            patches.append(patch)

        patches.append(self.path_to_patch(graph, path, angle, row_spacing, max_stitch_length))

        print >> dbg, "end do_auto_fill"
        dbg.flush()

        return patches


    def to_patches(self, last_patch):
        patches = []

        if last_patch is None:
            starting_point = None
        else:
            nearest_point = self.outline.interpolate(self.outline.project(shgeo.Point(last_patch.stitches[-1])))
            starting_point = inkstitch.Point(*nearest_point.coords[0])

        if self.fill_underlay:
            patches.extend(self.do_auto_fill(self.fill_underlay_angle, self.fill_underlay_row_spacing, self.fill_underlay_max_stitch_length, starting_point))
            starting_point = patches[-1].stitches[-1]

        patches.extend(self.do_auto_fill(self.angle, self.row_spacing, self.max_stitch_length, starting_point))

        print >> dbg, "end AutoFill.to_patches"
        dbg.flush()

        return patches


class Stroke(EmbroideryElement):
    element_name = "Stroke"

    @property
    @param('satin_column', _('Satin stitch along paths'), type='toggle', inverse=True)
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @cache
    def width(self):
        stroke_width = self.get_style("stroke-width")

        if stroke_width.endswith("px"):
            stroke_width = stroke_width[:-2]

        return float(stroke_width)

    @property
    def dashed(self):
        return self.get_style("stroke-dasharray") is not None

    @property
    @param('running_stitch_length_mm', _('Running stitch length'), unit='mm', type='float', default=1.5)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param('zigzag_spacing_mm', _('Zig-zag spacing (peak-to-peak)'), unit='mm', type='float', default=0.4)
    @cache
    def zigzag_spacing(self):
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param('repeats', _('Repeats'), type='int', default="1")
    def repeats(self):
        return self.get_int_param("repeats", 1)

    @property
    def paths(self):
        return self.flatten(self.parse_path())

    def is_running_stitch(self):
        # stroke width <= 0.5 pixels is deprecated in favor of dashed lines
        return self.dashed or self.width <= 0.5

    def stroke_points(self, emb_point_list, zigzag_spacing, stroke_width):
        p0 = emb_point_list[0]
        rho = 0.0
        side = 1
        last_segment_direction = None

        for repeat in xrange(self.repeats):
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
                perp = along.rotate_left() * (stroke_width * 0.5)

                if stroke_width == 0.0 and last_segment_direction is not None:
                    if abs(1.0 - along * last_segment_direction) > 0.5:
                        # if greater than 45 degree angle, stitch the corner
                        rho = zigzag_spacing
                        patch.add_stitch(p0)

                # iteration variable: how far we are along segment
                while (rho <= seg_len):
                    left_pt = p0 + along * rho + perp * side
                    patch.add_stitch(left_pt)
                    rho += zigzag_spacing
                    side = -side

                p0 = p1
                last_segment_direction = along
                rho -= seg_len

            if (p0 - patch.stitches[-1]).length() > 0.1:
                patch.add_stitch(p0)

        return patch

    def to_patches(self, last_patch):
        patches = []

        for path in self.paths:
            path = [inkstitch.Point(x, y) for x, y in path]
            if self.is_running_stitch():
                patch = self.stroke_points(path, self.running_stitch_length, stroke_width=0.0)
            else:
                patch = self.stroke_points(path, self.zigzag_spacing / 2.0, stroke_width=self.width)

            patches.append(patch)

        return patches


class SatinColumn(EmbroideryElement):
    element_name = _("Satin Column")

    def __init__(self, *args, **kwargs):
        super(SatinColumn, self).__init__(*args, **kwargs)

    @property
    @param('satin_column', _('Custom satin column'), type='toggle')
    def satin_column(self):
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @param('zigzag_spacing_mm', _('Zig-zag spacing (peak-to-peak)'), unit='mm', type='float', default=0.4)
    def zigzag_spacing(self):
        # peak-to-peak distance between zigzags
        return max(self.get_float_param("zigzag_spacing_mm", 0.4), 0.01)

    @property
    @param('pull_compensation_mm', _('Pull compensation'), unit='mm', type='float')
    def pull_compensation(self):
        # In satin stitch, the stitches have a tendency to pull together and
        # narrow the entire column.  We can compensate for this by stitching
        # wider than we desire the column to end up.
        return self.get_float_param("pull_compensation_mm", 0)

    @property
    @param('contour_underlay', _('Contour underlay'), type='toggle', group=_('Contour Underlay'))
    def contour_underlay(self):
        # "Contour underlay" is stitching just inside the rectangular shape
        # of the satin column; that is, up one side and down the other.
        return self.get_boolean_param("contour_underlay")

    @property
    @param('contour_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Contour Underlay'), type='float', default=1.5)
    def contour_underlay_stitch_length(self):
        return max(self.get_float_param("contour_underlay_stitch_length_mm", 1.5), 0.01)

    @property
    @param('contour_underlay_inset_mm', _('Contour underlay inset amount'), unit='mm', group=_('Contour Underlay'), type='float', default=0.4)
    def contour_underlay_inset(self):
        # how far inside the edge of the column to stitch the underlay
        return self.get_float_param("contour_underlay_inset_mm", 0.4)

    @property
    @param('center_walk_underlay', _('Center-walk underlay'), type='toggle', group=_('Center-Walk Underlay'))
    def center_walk_underlay(self):
        # "Center walk underlay" is stitching down and back in the centerline
        # between the two sides of the satin column.
        return self.get_boolean_param("center_walk_underlay")

    @property
    @param('center_walk_underlay_stitch_length_mm', _('Stitch length'), unit='mm', group=_('Center-Walk Underlay'), type='float', default=1.5)
    def center_walk_underlay_stitch_length(self):
        return max(self.get_float_param("center_walk_underlay_stitch_length_mm", 1.5), 0.01)

    @property
    @param('zigzag_underlay', _('Zig-zag underlay'), type='toggle', group=_('Zig-zag Underlay'))
    def zigzag_underlay(self):
        return self.get_boolean_param("zigzag_underlay")

    @property
    @param('zigzag_underlay_spacing_mm', _('Zig-Zag spacing (peak-to-peak)'), unit='mm', group=_('Zig-zag Underlay'), type='float', default=3)
    def zigzag_underlay_spacing(self):
        return max(self.get_float_param("zigzag_underlay_spacing_mm", 3), 0.01)

    @property
    @param('zigzag_underlay_inset_mm', _('Inset amount (default: half of contour underlay inset)'), unit='mm', group=_('Zig-zag Underlay'), type='float')
    def zigzag_underlay_inset(self):
        # how far in from the edge of the satin the points in the zigzags
        # should be

        # Default to half of the contour underlay inset.  That is, if we're
        # doing both contour underlay and zigzag underlay, make sure the
        # points of the zigzag fall outside the contour underlay but inside
        # the edges of the satin column.
        return self.get_float_param("zigzag_underlay_inset_mm") or self.contour_underlay_inset / 2.0

    @property
    @cache
    def csp(self):
        return self.parse_path()

    @property
    @cache
    def flattened_beziers(self):
        if len(self.csp) == 2:
            return self.simple_flatten_beziers()
        else:
            return self.flatten_beziers_with_rungs()


    def flatten_beziers_with_rungs(self):
        input_paths = [self.flatten([path]) for path in self.csp]
        input_paths = [shgeo.LineString(path[0]) for path in input_paths]

        paths = input_paths[:]
        paths.sort(key=lambda path: path.length, reverse=True)

        # Imagine a satin column as a curvy ladder.
        # The two long paths are the "rails" of the ladder.  The remainder are
        # the "rungs".
        rails = paths[:2]
        rungs = shgeo.MultiLineString(paths[2:])

        # The rails should stay in the order they were in the original CSP.
        # (this lets the user control where the satin starts and ends)
        rails.sort(key=lambda rail: input_paths.index(rail))

        result = []

        for rail in rails:
            if not rail.is_simple:
                self.fatal(_("One or more rails crosses itself, and this is not allowed.  Please split into multiple satin columns."))

            # handle null intersections here?
            linestrings = shapely.ops.split(rail, rungs)

            print >> dbg, "rails and rungs", [str(rail) for rail in rails], [str(rung) for rung in rungs]
            if len(linestrings.geoms) < len(rungs.geoms) + 1:
                self.fatal(_("satin column: One or more of the rungs doesn't intersect both rails.") + "  " + _("Each rail should intersect both rungs once."))
            elif len(linestrings.geoms) > len(rungs.geoms) + 1:
                self.fatal(_("satin column: One or more of the rungs intersects the rails more than once.") + "  " + _("Each rail should intersect both rungs once."))

            paths = [[inkstitch.Point(*coord) for coord in ls.coords] for ls in linestrings.geoms]
            result.append(paths)

        return zip(*result)


    def simple_flatten_beziers(self):
        # Given a pair of paths made up of bezier segments, flatten
        # each individual bezier segment into line segments that approximate
        # the curves.  Retain the divisions between beziers -- we'll use those
        # later.

        paths = []

        for path in self.csp:
            # See the documentation in the parent class for parse_path() for a
            # description of the format of the CSP.  Each bezier is constructed
            # using two neighboring 3-tuples in the list.

            flattened_path = []

            # iterate over pairs of 3-tuples
            for prev, current in zip(path[:-1], path[1:]):
                flattened_segment = self.flatten([[prev, current]])
                flattened_segment = [inkstitch.Point(x, y) for x, y in flattened_segment[0]]
                flattened_path.append(flattened_segment)

            paths.append(flattened_path)

        return zip(*paths)

    def validate_satin_column(self):
        # The node should have exactly two paths with no fill.  Each
        # path should have the same number of points, meaning that they
        # will both be made up of the same number of bezier curves.

        node_id = self.node.get("id")

        if self.get_style("fill") is not None:
            self.fatal(_("satin column: object %s has a fill (but should not)") % node_id)

        if len(self.csp) == 2:
            if len(self.csp[0]) != len(self.csp[1]):
                self.fatal(_("satin column: object %(id)s has two paths with an unequal number of points (%(length1)d and %(length2)d)") % \
                             dict(id=node_id, length1=len(self.csp[0]), length2=len(self.csp[1])))

    def offset_points(self, pos1, pos2, offset_px):
        # Expand or contract two points about their midpoint.  This is
        # useful for pull compensation and insetting underlay.

        distance = (pos1 - pos2).length()

        if distance < 0.0001:
            # if they're the same point, we don't know which direction
            # to offset in, so we have to just return the points
            return pos1, pos2

        # don't contract beyond the midpoint, or we'll start expanding
        if offset_px < -distance / 2.0:
            offset_px = -distance / 2.0

        pos1 = pos1 + (pos1 - pos2).unit() * offset_px
        pos2 = pos2 + (pos2 - pos1).unit() * offset_px

        return pos1, pos2

    def walk(self, path, start_pos, start_index, distance):
        # Move <distance> pixels along <path>, which is a sequence of line
        # segments defined by points.

        # <start_index> is the index of the line segment in <path> that
        # we're currently on.  <start_pos> is where along that line
        # segment we are.  Return a new position and index.

        # print >> dbg, "walk", start_pos, start_index, distance

        pos = start_pos
        index = start_index
        last_index = len(path) - 1
        distance_remaining = distance

        while True:
            if index >= last_index:
                return pos, index

            segment_end = path[index + 1]
            segment = segment_end - pos
            segment_length = segment.length()

            if segment_length > distance_remaining:
                # our walk ends partway along this segment
                return pos + segment.unit() * distance_remaining, index
            else:
                # our walk goes past the end of this segment, so advance
                # one point
                index += 1
                distance_remaining -= segment_length
                pos = segment_end

    def walk_paths(self, spacing, offset):
        # Take a bezier segment from each path in turn, and plot out an
        # equal number of points on each bezier.  Return the points plotted.
        # The points will be contracted or expanded by offset using
        # offset_points().

        points = [[], []]

        def add_pair(pos1, pos2):
            pos1, pos2 = self.offset_points(pos1, pos2, offset)
            points[0].append(pos1)
            points[1].append(pos2)

        # We may not be able to fit an even number of zigzags in each pair of
        # beziers.  We'll store the remaining bit of the beziers after handling
        # each section.
        remainder_path1 = []
        remainder_path2 = []

        for segment1, segment2 in self.flattened_beziers:
            subpath1 = remainder_path1 + segment1
            subpath2 = remainder_path2 + segment2

            len1 = shgeo.LineString(subpath1).length
            len2 = shgeo.LineString(subpath2).length

            # Base the number of stitches in each section on the _longest_ of
            # the two beziers. Otherwise, things could get too sparse when one
            # side is significantly longer (e.g. when going around a corner).
            # The risk here is that we poke a hole in the fabric if we try to
            # cram too many stitches on the short bezier.  The user will need
            # to avoid this through careful construction of paths.
            #
            # TODO: some commercial machine embroidery software compensates by
            # pulling in some of the "inner" stitches toward the center a bit.

            # note, this rounds down using integer-division
            num_points = max(len1, len2) / spacing

            spacing1 = len1 / num_points
            spacing2 = len2 / num_points

            pos1 = subpath1[0]
            index1 = 0

            pos2 = subpath2[0]
            index2 = 0

            for i in xrange(int(num_points)):
                add_pair(pos1, pos2)

                pos1, index1 = self.walk(subpath1, pos1, index1, spacing1)
                pos2, index2 = self.walk(subpath2, pos2, index2, spacing2)

            if index1 < len(subpath1) - 1:
                remainder_path1 = [pos1] + subpath1[index1 + 1:]
            else:
                remainder_path1 = []

            if index2 < len(subpath2) - 1:
                remainder_path2 = [pos2] + subpath2[index2 + 1:]
            else:
                remainder_path2 = []

        # We're off by one in the algorithm above, so we need one more
        # pair of points.  We also want to add points at the very end to
        # make sure we match the vectors on screen as best as possible.
        # Try to avoid doing both if they're going to stack up too
        # closely.

        end1 = remainder_path1[-1]
        end2 = remainder_path2[-1]

        if (end1 - pos1).length() > 0.3 * spacing:
            add_pair(pos1, pos2)

        add_pair(end1, end2)

        return points

    def do_contour_underlay(self):
        # "contour walk" underlay: do stitches up one side and down the
        # other.
        forward, back = self.walk_paths(self.contour_underlay_stitch_length,
                                        -self.contour_underlay_inset)
        return Patch(color=self.color, stitches=(forward + list(reversed(back))))

    def do_center_walk(self):
        # Center walk underlay is just a running stitch down and back on the
        # center line between the bezier curves.

        # Do it like contour underlay, but inset all the way to the center.
        forward, back = self.walk_paths(self.center_walk_underlay_stitch_length,
                                        -100000)
        return Patch(color=self.color, stitches=(forward + list(reversed(back))))

    def do_zigzag_underlay(self):
        # zigzag underlay, usually done at a much lower density than the
        # satin itself.  It looks like this:
        #
        # \/\/\/\/\/\/\/\/\/\/|
        # /\/\/\/\/\/\/\/\/\/\|
        #
        # In combination with the "contour walk" underlay, this is the
        # "German underlay" described here:
        #   http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/

        patch = Patch(color=self.color)

        sides = self.walk_paths(self.zigzag_underlay_spacing / 2.0,
                                -self.zigzag_underlay_inset)

        # This organizes the points in each side in the order that they'll be
        # visited.
        sides = [sides[0][::2] + list(reversed(sides[0][1::2])),
                 sides[1][1::2] + list(reversed(sides[1][::2]))]

        # This fancy bit of iterable magic just repeatedly takes a point
        # from each side in turn.
        for point in chain.from_iterable(izip(*sides)):
            patch.add_stitch(point)

        return patch

    def do_satin(self):
        # satin: do a zigzag pattern, alternating between the paths.  The
        # zigzag looks like this to make the satin stitches look perpendicular
        # to the column:
        #
        # /|/|/|/|/|/|/|/|

        # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

        patch = Patch(color=self.color)

        sides = self.walk_paths(self.zigzag_spacing, self.pull_compensation)

        # Like in zigzag_underlay(): take a point from each side in turn.
        for point in chain.from_iterable(izip(*sides)):
            patch.add_stitch(point)

        return patch

    def to_patches(self, last_patch):
        # Stitch a variable-width satin column, zig-zagging between two paths.

        # The algorithm will draw zigzags between each consecutive pair of
        # beziers.  The boundary points between beziers serve as "checkpoints",
        # allowing the user to control how the zigzags flow around corners.

        # First, verify that we have valid paths.
        self.validate_satin_column()

        patches = []

        if self.center_walk_underlay:
            patches.append(self.do_center_walk())

        if self.contour_underlay:
            patches.append(self.do_contour_underlay())

        if self.zigzag_underlay:
            # zigzag underlay comes after contour walk underlay, so that the
            # zigzags sit on the contour walk underlay like rail ties on rails.
            patches.append(self.do_zigzag_underlay())

        patches.append(self.do_satin())

        return patches


class Polyline(EmbroideryElement):
    # Handle a <polyline> element, which is treated as a set of points to
    # stitch exactly.
    #
    # <polyline> elements are pretty rare in SVG, from what I can tell.
    # Anything you can do with a <polyline> can also be done with a <p>, and
    # much more.
    #
    # Notably, EmbroiderModder2 uses <polyline> elements when converting from
    # common machine embroidery file formats to SVG.  Handling those here lets
    # users use File -> Import to pull in existing designs they may have
    # obtained, for example purchased fonts.

    @property
    def points(self):
       # example: "1,2 0,0 1.5,3 4,2"

       points = self.node.get('points')
       points = points.split(" ")
       points = [[float(coord) for coord in point.split(",")] for point in points]

       return points

    @property
    def path(self):
        # A polyline is a series of connected line segments described by their
        # points.  In order to make use of the existing logic for incorporating
        # svg transforms that is in our superclass, we'll convert the polyline
        # to a degenerate cubic superpath in which the bezier handles are on
        # the segment endpoints.

        path = [[[point[:], point[:], point[:]] for point in self.points]]

        return path

    @property
    @cache
    def csp(self):
        csp = self.parse_path()

        return csp

    @property
    def color(self):
        # EmbroiderModder2 likes to use the `stroke` property directly instead
        # of CSS.
        return self.get_style("stroke") or self.node.get("stroke")

    @property
    def stitches(self):
        # For a <polyline>, we'll stitch the points exactly as they exist in
        # the SVG, with no stitch spacing interpolation, flattening, etc.

        # See the comments in the parent class's parse_path method for a
        # description of the CSP data structure.

        stitches = [point for handle_before, point, handle_after in self.csp[0]]

        return stitches

    def to_patches(self, last_patch):
        patch = Patch(color=self.color)

        for stitch in self.stitches:
            patch.add_stitch(inkstitch.Point(*stitch))

        return [patch]

def detect_classes(node):
    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline]
    else:
        element = EmbroideryElement(node)

        if element.get_boolean_param("satin_column"):
            return [SatinColumn]
        else:
            classes = []

            if element.get_style("fill"):
                if element.get_boolean_param("auto_fill", True):
                    classes.append(AutoFill)
                else:
                    classes.append(Fill)

            if element.get_style("stroke"):
                classes.append(Stroke)

            if element.get_boolean_param("stroke_first", False):
                classes.reverse()

            return classes


class Patch:
    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False):
        self.color = color
        self.stitches = stitches or []
        self.trim_after = trim_after
        self.stop_after = stop_after

    def __add__(self, other):
        if isinstance(other, Patch):
            return Patch(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("Patch can only be added to another Patch")

    def add_stitch(self, stitch):
        self.stitches.append(stitch)

    def reverse(self):
        return Patch(self.color, self.stitches[::-1])


def process_stop_after(stitches):
    # The user wants the machine to pause after this patch.  This can
    # be useful for applique and similar on multi-needle machines that
    # normally would not stop between colors.
    #
    # On such machines, the user assigns needles to the colors in the
    # design before starting stitching.  C01, C02, etc are normal
    # needles, but C00 is special.  For a block of stitches assigned
    # to C00, the machine will continue sewing with the last color it
    # had and pause after it completes the C00 block.
    #
    # That means we need to introduce an artificial color change
    # shortly before the current stitch so that the user can set that
    # to C00.  We'll go back 3 stitches and do that:

    if len(stitches) >= 3:
        stitches[-3].stop = True

    # and also add a color change on this stitch, completing the C00
    # block:

    stitches[-1].stop = True

    # reference for the above: https://github.com/lexelby/inkstitch/pull/29#issuecomment-359175447


def process_trim(stitches, next_stitch):
    # DST (and maybe other formats?) has no actual TRIM instruction.
    # Instead, 3 sequential JUMPs cause the machine to trim the thread.
    #
    # To support both DST and other formats, we'll add a TRIM and two
    # JUMPs.  The TRIM will be converted to a JUMP by libembroidery
    # if saving to DST, resulting in the 3-jump sequence.

    delta = next_stitch - stitches[-1]
    delta = delta * (1/4.0)

    pos = stitches[-1]

    for i in xrange(3):
        pos += delta
        stitches.append(inkstitch.Stitch(pos.x, pos.y, stitches[-1].color, jump=True))

    # first one should be TRIM instead of JUMP
    stitches[-3].jump = False
    stitches[-3].trim = True


def add_tie(stitches, tie_path):
    color = tie_path[0].color

    tie_path = cut_path(tie_path, 0.6)
    tie_stitches = running_stitch(tie_path, 0.3)
    tie_stitches = [inkstitch.Stitch(*stitch, color=color) for stitch in tie_stitches]

    stitches.extend(tie_stitches[1:])
    stitches.extend(list(reversed(tie_stitches))[1:])


def add_tie_off(stitches):
    if not stitches:
        return

    add_tie(stitches, list(reversed(stitches)))


def add_tie_in(stitches, upcoming_stitches):
    if not upcoming_stitches:
        return

    add_tie(stitches, upcoming_stitches)


def add_ties(original_stitches):
    """Add tie-off before and after trims, jumps, and color changes."""

    # we're going to copy most stitches over, adding tie in/off as needed
    stitches = []

    need_tie_in = True

    for i, stitch in enumerate(original_stitches):
        is_special = stitch.trim or stitch.jump or stitch.stop

        if is_special and not need_tie_in:
            add_tie_off(stitches)
            stitches.append(stitch)
            need_tie_in = True
        elif need_tie_in and not is_special:
            stitches.append(stitch)
            add_tie_in(stitches, original_stitches[i:])
            need_tie_in = False
        else:
            stitches.append(stitch)

    # add tie-off at the end if we ended on a normal stitch
    if not is_special:
        add_tie_off(stitches)

    # overwrite the stitch plan with our new one that contains ties
    original_stitches[:] = stitches


def patches_to_stitches(patch_list, collapse_len_px=3.0):
    stitches = []

    last_stitch = None
    last_color = None
    need_trim = False
    for patch in patch_list:
        if not patch.stitches:
            continue

        jump_stitch = True
        for stitch in patch.stitches:
            if last_stitch and last_color == patch.color:
                l = (stitch - last_stitch).length()
                if l <= 0.1:
                    # filter out duplicate successive stitches
                    jump_stitch = False
                    continue

                if jump_stitch:
                    # consider collapsing jump stitch, if it is pretty short
                    if l < collapse_len_px:
                        # dbg.write("... collapsed\n")
                        jump_stitch = False

            if stitches and last_color and last_color != patch.color:
                # add a color change
                stitches.append(inkstitch.Stitch(last_stitch.x, last_stitch.y, last_color, stop=True))

            if need_trim:
                process_trim(stitches, stitch)
                need_trim = False

            if jump_stitch:
                stitches.append(inkstitch.Stitch(stitch.x, stitch.y, patch.color, jump=True))

            stitches.append(inkstitch.Stitch(stitch.x, stitch.y, patch.color, jump=False))

            jump_stitch = False
            last_stitch = stitch
            last_color = patch.color

        if patch.trim_after:
            need_trim = True

        if patch.stop_after:
            process_stop_after(stitches)

    add_ties(stitches)

    return stitches

def stitches_to_polylines(stitches):
    polylines = []
    last_color = None
    last_stitch = None
    trimming = False

    for stitch in stitches:
        if stitch.color != last_color or stitch.trim:
            trimming = True
            polylines.append([stitch.color, []])

        if trimming and (stitch.jump or stitch.trim):
            continue

        trimming = False

        polylines[-1][1].append(stitch.as_tuple())

        last_color = stitch.color
        last_stitch = stitch

    return polylines

def emit_inkscape(parent, stitches):
    transform = get_viewbox_transform(parent.getroottree().getroot())

    # we need to correct for the viewbox
    transform = simpletransform.invertTransform(transform)
    transform = simpletransform.formatTransform(transform)

    for color, polyline in stitches_to_polylines(stitches):
        # dbg.write('polyline: %s %s\n' % (color, repr(polyline)))
        inkex.etree.SubElement(parent,
                               inkex.addNS('polyline', 'svg'),
                               {'style': simplestyle.formatStyle(
                                   {'stroke': color if color is not None else '#000000',
                                    'stroke-width': "0.4",
                                    'fill': 'none'}),
                                   'points': " ".join(",".join(str(coord) for coord in point) for point in polyline),
                                'transform': transform
                                })

def get_elements(effect):
    elements = []
    nodes = get_nodes(effect)

    for node in nodes:
        classes = detect_classes(node)
        elements.extend(cls(node) for cls in classes)

    return elements


def elements_to_patches(elements):
    patches = []
    for element in elements:
        if patches:
            last_patch = patches[-1]
        else:
            last_patch = None

        patches.extend(element.embroider(last_patch))

    return patches

class Embroider(inkex.Effect):

    def __init__(self, *args, **kwargs):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-c", "--collapse_len_mm",
                                     action="store", type="float",
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")
        self.OptionParser.add_option("--hide_layers",
                                     action="store", type="choice",
                                     choices=["true", "false"],
                                     dest="hide_layers", default="true",
                                     help="Hide all other layers when the embroidery layer is generated")
        self.OptionParser.add_option("-O", "--output_format",
                                     action="store", type="string",
                                     dest="output_format", default="csv",
                                     help="Output file extenstion (default: csv)")
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")
        self.OptionParser.add_option("-F", "--output-file",
                                     action="store", type="string",
                                     dest="output_file",
                                     help="Output filename.")
        self.OptionParser.add_option("-b", "--max-backups",
                                     action="store", type="int",
                                     dest="max_backups", default=5,
                                     help="Max number of backups of output files to keep.")
        self.OptionParser.usage += _("\n\nSeeing a 'no such option' message?  Please restart Inkscape to fix.")

    def get_output_path(self):
        if self.options.output_file:
            output_path = os.path.join(self.options.path, self.options.output_file)
        else:
            svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")
            csv_filename = svg_filename.replace('.svg', '.%s' % self.options.output_format)
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

                if os.path.exists(dest):
                    os.remove(dest)

                os.rename(source, dest)

        move_if_exists(output_path)

        return output_path

    def hide_layers(self):
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            if g.get(inkex.addNS("groupmode", "inkscape")) == "layer":
                g.set("style", "display:none")

    def effect(self):
        # Printing anything other than a valid SVG on stdout blows inkscape up.
        old_stdout = sys.stdout
        sys.stdout = sys.stderr

        self.patch_list = []

        self.elements = get_elements(self)

        if not self.elements:
            if self.selected:
                inkex.errormsg(_("No embroiderable paths selected."))
            else:
                inkex.errormsg(_("No embroiderable paths found in document."))
            inkex.errormsg(_("Tip: use Path -> Object to Path to convert non-paths before embroidering."))
            return

        if self.options.hide_layers:
            self.hide_layers()

        patches = elements_to_patches(self.elements)
        stitches = patches_to_stitches(patches, self.options.collapse_length_mm * PIXELS_PER_MM)
        inkstitch.write_embroidery_file(self.get_output_path(), stitches, self.document.getroot())

        new_layer = inkex.etree.SubElement(self.document.getroot(), SVG_GROUP_TAG, {})
        new_layer.set('id', self.uniqueId("embroidery"))
        new_layer.set(inkex.addNS('label', 'inkscape'), _('Embroidery'))
        new_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        emit_inkscape(new_layer, stitches)

        sys.stdout = old_stdout

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    e = Embroider()

    try:
        e.affect()
    except KeyboardInterrupt:
        print >> dbg, "interrupted!"

        print >> dbg, traceback.format_exc()

    dbg.flush()
