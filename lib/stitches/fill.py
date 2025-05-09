# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math

import shapely

from ..stitch_plan import Stitch
from ..svg import PIXELS_PER_MM
from ..utils import Point as InkstitchPoint
from ..utils import cache
from ..utils.threading import check_stop_flag
from .running_stitch import split_segment_random_phase


def legacy_fill(shape, angle, row_spacing, end_row_spacing, max_stitch_length, flip, reverse, staggers, skip_last):
    rows_of_segments = intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing, flip)
    groups_of_segments = pull_runs(rows_of_segments, shape, row_spacing, end_row_spacing)

    stitches = [section_to_stitches(group, angle, row_spacing, max_stitch_length, staggers, skip_last)
                for group in groups_of_segments]
    if reverse:
        stitches = [segment[::-1] for segment in stitches[::-1]]
    return stitches


@cache
def east(angle):
    # "east" is the name of the direction that is to the right along a row
    return InkstitchPoint(1, 0).rotate(-angle)


@cache
def north(angle):
    return east(angle).rotate(math.pi / 2)


def row_num(point, angle, row_spacing):
    return round((point * north(angle)) / row_spacing)


def adjust_stagger(stitch, angle, row_spacing, max_stitch_length, staggers):
    if staggers == 0:
        staggers = 1  # sanity check to avoid division by zero.
    this_row_num = row_num(stitch, angle, row_spacing)
    stagger_phase = (this_row_num / staggers) % 1
    stagger_offset = stagger_phase * max_stitch_length
    offset = ((stitch * east(angle)) - stagger_offset) % max_stitch_length

    return stitch - offset * east(angle)


def stitch_row(stitches, beg, end, angle, row_spacing, max_stitch_length, staggers, skip_last,
               enable_random_stitch_length, random_sigma, random_seed):
    if end == beg:
        stitches.append(Stitch(*beg, tags=('fill_row_start',)))
        return

    beg = Stitch(*beg, tags=('fill_row_start',))
    end = Stitch(*end, tags=('fill_row_start',))
    stitches.append(beg)

    if enable_random_stitch_length:
        stitches += split_segment_random_phase(beg, end, max_stitch_length, random_sigma, random_seed)
    else:
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

        row_direction = (end - beg).unit()
        segment_length = (end - beg).length()

        stitches.append(beg)

        first_stitch = adjust_stagger(beg, angle, row_spacing, max_stitch_length, staggers)

        # we might have chosen our first stitch just outside this row, so move back in
        if (first_stitch - beg) * row_direction < 0:
            first_stitch += row_direction * max_stitch_length

        offset = (first_stitch - beg).length()

        while offset < segment_length:
            stitches.append(Stitch(beg + offset * row_direction, tags=('fill_row',)))
            offset += max_stitch_length

    if (end - stitches[-1]).length() > 0.1 * PIXELS_PER_MM and not skip_last:
        stitches.append(end)


def intersect_region_with_grating(shape, angle, row_spacing, end_row_spacing=None, flip=False):
    # the max line length I'll need to intersect the whole shape is the diagonal
    (minx, miny, maxx, maxy) = shape.bounds
    upper_left = InkstitchPoint(minx, miny)
    lower_right = InkstitchPoint(maxx, maxy)
    length = (upper_left - lower_right).length()
    half_length = length / 2.0

    # Now get a unit vector rotated to the requested angle.  I use -angle
    # because shapely rotates clockwise, but my geometry textbooks taught
    # me to consider angles as counter-clockwise from the X axis.
    direction = InkstitchPoint(-1, 0).rotate(-angle)

    # and get a normal vector
    normal = direction.rotate(-math.pi / 2)

    # I'll start from the center, move in the normal direction some amount,
    # and then walk left and right half_length in each direction to create
    # a line segment in the grating.
    center = InkstitchPoint((minx + maxx) / 2.0, (miny + maxy) / 2.0)

    # I need to figure out how far I need to go along the normal to get to
    # the edge of the shape.  To do that, I'll rotate the bounding box
    # angle degrees clockwise and ask for the new bounding box.  The max
    # and min y tell me how far to go.

    _, start, _, end = shapely.affinity.rotate(shape, angle, origin='center', use_radians=True).bounds

    # convert start and end to be relative to center (simplifies things later)
    start -= center.y
    end -= center.y

    height = abs(end - start)
    if height == 0:
        # return early to avoid divide-by-zero later
        return []

    # print >> dbg, "grating:", start, end, height, row_spacing, end_row_spacing

    # offset start slightly so that rows are always an even multiple of
    # row_spacing_px from the origin.  This makes it so that abutting
    # fill regions at the same angle and spacing always line up nicely.
    start -= (start + normal * center) % row_spacing

    current_row_y = start
    rows = []
    while current_row_y < end:
        check_stop_flag()

        p0 = center + normal * current_row_y + direction * half_length
        p1 = center + normal * current_row_y - direction * half_length
        endpoints = [p0.as_tuple(), p1.as_tuple()]
        grating_line = shapely.geometry.LineString(endpoints)

        res = grating_line.intersection(shape)

        if res.geom_type in ["MultiLineString", "GeometryCollection"]:
            runs = [line_string.coords for line_string in res.geoms if line_string.geom_type == "LineString"]
        elif res.geom_type in ["Point", "MultiPoint"] or res.is_empty:
            # ignore if we intersected at a single point or no points
            runs = []
        else:
            runs = [res.coords]

        if runs:
            runs.sort(key=lambda seg: (InkstitchPoint(*seg[0]) - upper_left).length())

            if flip:
                runs.reverse()
                runs = [tuple(reversed(run)) for run in runs]

            rows.append(runs)

        if end_row_spacing:
            current_row_y += row_spacing + (end_row_spacing - row_spacing) * ((current_row_y - start) / height)
        else:
            current_row_y += row_spacing

        check_stop_flag()

    return rows


def section_to_stitches(group_of_segments, angle, row_spacing, max_stitch_length, staggers, skip_last):
    stitches = []
    swap = False

    for segment in group_of_segments:
        (beg, end) = segment

        if (swap):
            (beg, end) = (end, beg)

        stitch_row(stitches, beg, end, angle, row_spacing, max_stitch_length, staggers, skip_last, False, 0.0, "")

        swap = not swap

    return stitches


def make_quadrilateral(segment1, segment2):
    return shapely.geometry.Polygon((segment1[0], segment1[1], segment2[1], segment2[0], segment1[0]))


def is_same_run(segment1, segment2, shape, row_spacing, end_row_spacing):
    line1 = shapely.geometry.LineString(segment1)
    line2 = shapely.geometry.LineString(segment2)

    spacing = row_spacing
    if end_row_spacing is not None:
        spacing = max(spacing, end_row_spacing)

    if line1.distance(line2) > spacing * 1.1:
        return False

    quad = make_quadrilateral(segment1, segment2)
    quad_area = quad.area
    intersection_area = shape.intersection(quad).area

    return (intersection_area / quad_area) >= 0.9


def pull_runs(rows, shape, row_spacing, end_row_spacing):
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

    rows = list(rows)
    runs = []
    while (len(rows) > 0):
        run = []
        prev = None

        for row_num in range(len(rows)):
            row = rows[row_num]
            first, rest = row[0], row[1:]

            # TODO: only accept actually adjacent rows here
            if prev is not None and not is_same_run(prev, first, shape, row_spacing, end_row_spacing):
                break

            run.append(first)
            prev = first

            rows[row_num] = rest

        runs.append(run)
        rows = [r for r in rows if len(r) > 0]

    return runs
