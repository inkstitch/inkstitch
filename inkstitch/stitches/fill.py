from .. import Point as InkstitchPoint, cache, PIXELS_PER_MM
import shapely
import math


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
    this_row_num = row_num(stitch, angle, row_spacing)
    row_stagger = this_row_num % staggers
    stagger_offset = (float(row_stagger) / staggers) * max_stitch_length
    offset = ((stitch * east(angle)) - stagger_offset) % max_stitch_length

    return stitch - offset * east(angle)

def stitch_row(stitches, beg, end, angle, row_spacing, max_stitch_length, staggers):
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

    beg = InkstitchPoint(*beg)
    end = InkstitchPoint(*end)

    row_direction = (end - beg).unit()
    segment_length = (end - beg).length()

    # only stitch the first point if it's a reasonable distance away from the
    # last stitch
    if not stitches or (beg - stitches[-1]).length() > 0.5 * PIXELS_PER_MM:
        stitches.append(beg)

    first_stitch = adjust_stagger(beg, angle, row_spacing, max_stitch_length, staggers)

    # we might have chosen our first stitch just outside this row, so move back in
    if (first_stitch - beg) * row_direction < 0:
        first_stitch += row_direction * max_stitch_length

    offset = (first_stitch - beg).length()

    while offset < segment_length:
        stitches.append(beg + offset * row_direction)
        offset += max_stitch_length

    if (end - stitches[-1]).length() > 0.1 * PIXELS_PER_MM:
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
    direction = InkstitchPoint(1, 0).rotate(-angle)

    # and get a normal vector
    normal = direction.rotate(math.pi / 2)

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

    #print >> dbg, "grating:", start, end, height, row_spacing, end_row_spacing

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
        grating_line = shapely.geometry.LineString(endpoints)

        res = grating_line.intersection(shape)

        if (isinstance(res, shapely.geometry.MultiLineString)):
            runs = map(lambda line_string: line_string.coords, res.geoms)
        else:
            if res.is_empty or len(res.coords) == 1:
                # ignore if we intersected at a single point or no points
                runs = []
            else:
                runs = [res.coords]

        if runs:
            runs.sort(key=lambda seg: (InkstitchPoint(*seg[0]) - upper_left).length())

            if flip:
                runs.reverse()
                runs = map(lambda run: tuple(reversed(run)), runs)

            rows.append(runs)

        if end_row_spacing:
            current_row_y += row_spacing + (end_row_spacing - row_spacing) * ((current_row_y - start) / height)
        else:
            current_row_y += row_spacing

    return rows
