# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from numpy import zeros, convolve, int32, diff, setdiff1d, sign
from math import degrees, acos
from ...svg import PIXELS_PER_MM

from ...utils import Point
from shapely import geometry as shgeo
from inkex import errormsg
from ...utils.geometry import remove_duplicate_points
from shapely.ops import substring
from shapely.affinity import scale
from ...i18n import _
import sys


class SelfIntersectionError(Exception):
    pass


def convert_path_to_satin(path, stroke_width, style_args):
    path = remove_duplicate_points(fix_loop(path))

    if len(path) < 2:
        # ignore paths with just one point -- they're not visible to the user anyway
        return None

    sections = list(convert_path_to_satins(path, stroke_width, style_args))

    if sections:
        joined_satin = list(sections)[0]
        for satin in sections[1:]:
            joined_satin = _merge(joined_satin, satin)
        return joined_satin
    return None


def convert_path_to_satins(path, stroke_width, style_args, depth=0):
    try:
        rails, rungs = path_to_satin(path, stroke_width, style_args)
        yield (rails, rungs)
    except SelfIntersectionError:
        # The path intersects itself.  Split it in two and try doing the halves
        # individually.

        if depth >= 20:
            # At this point we're slicing the path way too small and still
            # getting nowhere.  Just give up on this section of the path.
            return

        halves = split_path(path)

        for path in halves:
            for section in convert_path_to_satins(path, stroke_width, style_args, depth=depth + 1):
                yield section


def split_path(path):
    linestring = shgeo.LineString(path)
    halves = [
        list(substring(linestring, 0, 0.5, normalized=True).coords),
        list(substring(linestring, 0.5, 1, normalized=True).coords),
    ]

    return halves


def fix_loop(path):
    if path[0] == path[-1] and len(path) > 1:
        first = Point.from_tuple(path[0])
        second = Point.from_tuple(path[1])
        midpoint = (first + second) / 2
        midpoint = midpoint.as_tuple()

        return [midpoint] + path[1:] + [path[0], midpoint]
    else:
        return path


def path_to_satin(path, stroke_width, style_args):
    if Point(*path[0]).distance(Point(*path[-1])) < 1:
        raise SelfIntersectionError()

    path = shgeo.LineString(path)
    distance = stroke_width / 2.0

    try:
        left_rail = path.offset_curve(-distance, **style_args)
        right_rail = path.offset_curve(distance, **style_args)
    except ValueError:
        # TODO: fix this error automatically
        # Error reference: https://github.com/inkstitch/inkstitch/issues/964
        errormsg(_("Ink/Stitch cannot convert your stroke into a satin column. "
                   "Please break up your path and try again.") + '\n')
        sys.exit(1)

    if left_rail.geom_type != 'LineString' or right_rail.geom_type != 'LineString':
        # If the offset curve come out as anything but a LineString, that means the
        # path intersects itself, when taking its stroke width into consideration.
        raise SelfIntersectionError()

    rungs = generate_rungs(path, stroke_width, left_rail, right_rail)

    left_rail = list(left_rail.coords)
    right_rail = list(right_rail.coords)

    return (left_rail, right_rail), rungs


def get_scores(path):
    """Generate an array of "scores" of the sharpness of corners in a path

    A higher score means that there are sharper corners in that section of
    the path.  We'll divide the path into boxes, with the score in each
    box indicating the sharpness of corners at around that percentage of
    the way through the path.  For example, if scores[40] is 100 and
    scores[45] is 200, then the path has sharper corners at a spot 45%
    along its length than at a spot 40% along its length.
    """

    # need 101 boxes in order to encompass percentages from 0% to 100%
    scores = zeros(101, int32)
    path_length = path.length

    prev_point = None
    prev_direction = None
    length_so_far = 0
    for point in path.coords:
        point = Point(*point)

        if prev_point is None:
            prev_point = point
            continue

        direction = (point - prev_point).unit()

        if prev_direction is not None:
            # The dot product of two vectors is |v1| * |v2| * cos(angle).
            # These are unit vectors, so their magnitudes are 1.
            cos_angle_between = prev_direction * direction

            # Clamp to the valid range for a cosine.  The above _should_
            # already be in this range, but floating point inaccuracy can
            # push it outside the range causing math.acos to throw
            # ValueError ("math domain error").
            cos_angle_between = max(-1.0, min(1.0, cos_angle_between))

            angle = abs(degrees(acos(cos_angle_between)))

            # Use the square of the angle, measured in degrees.
            #
            # Why the square?  This penalizes bigger angles more than
            # smaller ones.
            #
            # Why degrees?  This is kind of arbitrary but allows us to
            # use integer math effectively and avoid taking the square
            # of a fraction between 0 and 1.
            scores[int(round(length_so_far / path_length * 100.0))] += angle ** 2

        length_so_far += (point - prev_point).length()
        prev_direction = direction
        prev_point = point

    return scores


def local_minima(array):
    # from: https://stackoverflow.com/a/9667121/4249120
    # This finds spots where the curvature (second derivative) is > 0.
    #
    # This method has the convenient benefit of choosing points around
    # 5% before and after a sharp corner such as in a square.
    return (diff(sign(diff(array))) > 0).nonzero()[0] + 1


def generate_rungs(path, stroke_width, left_rail, right_rail):
    """Create rungs for a satin column.

    Where should we put the rungs along a path?  We want to ensure that the
    resulting satin matches the original path as closely as possible.  We
    want to avoid having a ton of rungs that will annoy the user.  We want
    to ensure that the rungs we choose actually intersect both rails.

    We'll place a few rungs perpendicular to the tangent of the path.
    Things get pretty tricky at sharp corners.  If we naively place a rung
    perpendicular to the path just on either side of a sharp corner, the
    rung may not intersect both paths:
                   |    |
    _______________|    |
                  ______|_
    ____________________|

    It'd be best to place rungs in the straight sections before and after
    the sharp corner and allow the satin column to bend the stitches around
    the corner automatically.

    How can we find those spots?

    The general algorithm below is:

      * assign a "score" to each section of the path based on how sharp its
        corners are (higher means a sharper corner)
      * pick spots with lower scores
    """

    scores = get_scores(path)

    # This is kind of like a 1-dimensional gaussian blur filter.  We want to
    # avoid the area near a sharp corner, so we spread out its effect for
    # 5 buckets in either direction.
    scores = convolve(scores, [1, 2, 4, 8, 16, 8, 4, 2, 1], mode='same')

    # Now we'll find the spots that aren't near corners, whose scores are
    # low -- the local minima.
    rung_locations = local_minima(scores)

    # Remove the start and end, because we can't stick a rung there.
    rung_locations = setdiff1d(rung_locations, [0, 100])

    if len(rung_locations) == 0:
        # Straight lines won't have local minima, so add a rung in the center.
        rung_locations = [50]

    rungs = []
    last_rung_center = None

    for location in rung_locations:
        # Convert percentage to a fraction so that we can use interpolate's
        # normalized parameter.
        location = location / 100.0

        rung_center = path.interpolate(location, normalized=True)
        rung_center = Point(rung_center.x, rung_center.y)

        # Avoid placing rungs too close together.  This somewhat
        # arbitrarily rejects the rung if there was one less than 2
        # millimeters before this one.
        if last_rung_center is not None and \
                (rung_center - last_rung_center).length() < 2 * PIXELS_PER_MM:
            continue
        else:
            last_rung_center = rung_center

        # We need to know the tangent of the path's curve at this point.
        # Pick another point just after this one and subtract them to
        # approximate a tangent vector.
        tangent_end = path.interpolate(location + 0.001, normalized=True)
        tangent_end = Point(tangent_end.x, tangent_end.y)
        tangent = (tangent_end - rung_center).unit()

        # Rotate 90 degrees left to make a normal vector.
        normal = tangent.rotate_left()

        # Extend the rungs by an offset value to make sure they will cross the rails
        offset = normal * (stroke_width / 2) * 1.2
        rung_start = rung_center + offset
        rung_end = rung_center - offset

        rung_tuple = (rung_start.as_tuple(), rung_end.as_tuple())
        rung_linestring = shgeo.LineString(rung_tuple)
        if (isinstance(rung_linestring.intersection(left_rail), shgeo.Point) and
                isinstance(rung_linestring.intersection(right_rail), shgeo.Point)):
            rungs.append(rung_tuple)

    return rungs


def _merge(section, other_section):
    """Merge two satin sections

    The two sections are expected to be contiguous; that is, the second one
    starts where the first one ends.
    """
    rails, rungs = section
    other_rails, other_rungs = other_section

    if len(other_rails[0]) < 2 or len(other_rails[1]) < 2:
        # Somehow we got a degenerate rail with only one (or no?) point.
        # Ignore this one since it has zero length anyway.
        return section

    # remove first node of each other rail before merging (avoid duplicated nodes)
    rails[0].extend(other_rails[0][1:])
    rails[1].extend(other_rails[1][1:])

    # add a rung in between the two satins and extend it just a litte to ensure it is crossing the rails
    new_rung = shgeo.LineString([other_rails[0][0], other_rails[1][0]])
    rungs.append(list(scale(new_rung, 1.2, 1.2).coords))

    # add on the other satin's rungs
    rungs.extend(other_rungs)

    return (rails, rungs)
