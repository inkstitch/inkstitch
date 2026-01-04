# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
"""Utility functions to produce running stitches."""

import math
import typing
from copy import copy
from math import tau

import numpy as np
from shapely import geometry as shgeo
from shapely.geometry import LineString

from ..utils import prng
from ..utils.geometry import Point
from ..utils.threading import check_stop_flag


def lerp(a, b, t: float) -> float:
    """Linear interpolation between a and b by factor t."""
    return (1 - t) * a + t * b


def split_segment_even_n(a, b, segments: int, jitter_sigma: float = 0.0, random_seed=None) -> typing.List[shgeo.Point]:
    """Split a segment into n even parts, optionally with jitter."""
    if segments <= 1:
        return []
    line = shgeo.LineString((a, b))

    splits = np.array(range(1, segments)) / segments
    if random_seed is not None:
        jitters = (prng.n_uniform_floats(len(splits), random_seed) * 2) - 1
        splits = splits + jitters * (jitter_sigma / segments)

    # sort the splits in case a bad roll transposes any of them
    splits.sort()

    return [line.interpolate(x, normalized=True) for x in splits]


def split_segment_even_dist(a, b, max_length: float, jitter_sigma: float = 0.0, random_seed=None) -> typing.List[shgeo.Point]:
    """Split a segment into even parts with maximum length."""
    distance = shgeo.Point(a).distance(shgeo.Point(b))
    segments = math.ceil(distance / max_length)
    return split_segment_even_n(a, b, segments, jitter_sigma, random_seed)


def split_segment_random_phase(a, b, length: float, length_sigma: float, random_seed: str) -> typing.List[shgeo.Point]:
    """Split a segment with randomized phase and length variation."""
    line = shgeo.LineString([a, b])
    progress = length * prng.uniform_floats(random_seed, "phase")[0]
    splits = [progress]
    distance = line.length
    if progress >= distance:
        return []
    for x in prng.iter_uniform_floats(random_seed):
        progress += length * (1 + length_sigma * (x - 0.5) * 2)
        if progress >= distance:
            break
        splits.append(progress)
    return [line.interpolate(x, normalized=False) for x in splits]


def split_segment_stagger_phase(
    a,
    b,
    segment_length: float,
    num_staggers: int,
    this_segment_num: int,
    min_val=0,
    max_val=None,
) -> typing.List[shgeo.Point]:
    """Split a segment with staggered phase for pattern alignment."""
    line = shgeo.LineString([a, b])
    distance = line.length
    stagger_phase = (this_segment_num / num_staggers) % 1
    stagger_offset = stagger_phase * segment_length
    if max_val is None:
        max_val = distance

    splits = []
    progress = stagger_offset
    while progress < distance:
        if progress > min_val and progress < max_val:
            splits.append(progress)
        progress += segment_length
    return [line.interpolate(x, normalized=False) for x in splits]


class AngleInterval:
    """Modular interval containing either the entire circle or less than half of it.

    Partially based on https://fgiesen.wordpress.com/2015/09/24/intervals-in-modular-arithmetic/
    """

    def __init__(self, a: float, b: float, is_all: bool = False):
        self.is_all = is_all
        self.a = a
        self.b = b

    @staticmethod
    def all_angles():
        """Return an interval containing all angles."""
        return AngleInterval(0, math.tau, True)

    @staticmethod
    def from_ball(p: Point, epsilon: float):
        """Create an interval from a ball centered at origin with given radius."""
        d = p.length()
        if d <= epsilon:
            return AngleInterval.all_angles()
        center = p.angle()
        delta = math.asin(epsilon / d)
        return AngleInterval(center - delta, center + delta)

    @staticmethod
    def from_segment(a: Point, b: Point):
        """Create an interval from a line segment."""
        angle_a = a.angle()
        angle_b = b.angle()
        diff = (angle_b - angle_a) % tau
        if diff == 0 or diff == math.pi:
            return None
        elif diff < math.pi:
            # slightly larger than normal to avoid rounding error
            return AngleInterval(angle_a - 1e-6, angle_b + 1e-6)
        else:
            return AngleInterval(angle_b - 1e-6, angle_a + 1e-6)

    def contains_angle(self, angle: float):
        """Check if the interval contains the given angle."""
        if self.is_all:
            return True
        return (angle - self.a) % tau <= (self.b - self.a) % tau

    def contains_point(self, p: Point):
        """Check if the interval contains the angle to the given point."""
        return self.contains_angle(math.atan2(p.y, p.x))

    def intersect(self, other):
        """Compute the intersection of two angle intervals."""
        # assume that each interval contains less than half the circle (or all of it)
        if other is None:
            return None
        elif self.is_all:
            return other
        elif other.is_all:
            return self
        elif self.contains_angle(other.a):
            if other.contains_angle(self.b):
                return AngleInterval(other.a, self.b)
            else:
                return AngleInterval(other.a, other.b)
        elif other.contains_angle(self.a):
            if self.contains_angle(other.b):
                return AngleInterval(self.a, other.b)
            else:
                return AngleInterval(self.a, self.b)
        else:
            return None

    def cut_segment(self, origin: Point, a: Point, b: Point):
        """Cut a segment at the boundary of this interval."""
        if self.is_all:
            return None
        seg_arc = AngleInterval.from_segment(a - origin, b - origin)
        if seg_arc is None:
            return a  # b is exactly behind origin from a
        if seg_arc.contains_angle(self.a):
            return cut_segment_with_angle(origin, self.a, a, b)
        elif seg_arc.contains_angle(self.b):
            return cut_segment_with_angle(origin, self.b, a, b)
        else:
            return None


def cut_segment_with_angle(origin: Point, angle: float, a: Point, b: Point) -> Point:
    """Cut a segment at the intersection with a ray from origin at the given angle.

    Assumes the crossing is inside the segment.
    """
    p = a - origin
    d = b - a
    c = Point(math.cos(angle), math.sin(angle))
    t = (p.y * c.x - p.x * c.y) / (d.x * c.y - d.y * c.x)
    if t < -0.000001 or t > 1.000001:
        raise ValueError(f"cut_segment_with_angle returned a parameter of {t} " f"with points {p} {b - origin} and cut line {c}")
    return a + d * t


def cut_segment_with_circle(origin: Point, r: float, a: Point, b: Point) -> Point:
    """Cut a segment at the intersection with a circle centered at origin.

    Assumes that point a is inside the circle and point b is outside.
    """
    p = a - origin
    d = b - a
    # inner products
    p2 = p * p
    d2 = d * d
    r2 = r * r
    pd = p * d
    # r2 = p2 + 2*pd*t + d2*t*t, quadratic formula
    t = (math.sqrt(pd * pd + r2 * d2 - p2 * d2) - pd) / d2
    if t < -0.000001 or t > 1.000001:
        raise ValueError(f"cut_segment_with_circle returned a parameter of {t}")
    return a + d * t


def take_stitch(
    start: Point,
    points: typing.Sequence[Point],
    idx: int,
    stitch_length: float,
    tolerance: float,
) -> typing.Tuple[typing.Optional[Point], typing.Optional[int]]:
    """Take a single stitch based on the Zhao-Saalfeld curve simplification algorithm.

    Based on: https://cartogis.org/docs/proceedings/archive/auto-carto-13/pdf/
    linear-time-sleeve-fitting-polyline-simplification-algorithms.pdf
    Adds early termination condition based on stitch length.
    """
    if idx >= len(points):
        return None, None

    sleeve = AngleInterval.all_angles()
    last = start
    for i in range(idx, len(points)):
        p = points[i]
        if sleeve.contains_point(p - start):
            if start.distance(p) < stitch_length:
                sleeve = sleeve.intersect(AngleInterval.from_ball(p - start, tolerance))
                last = p
                continue
            else:
                cut = cut_segment_with_circle(start, stitch_length, last, p)
                return cut, i
        else:
            cut = sleeve.cut_segment(start, last, p)
            if start.distance(cut) > stitch_length:
                cut = cut_segment_with_circle(start, stitch_length, last, p)
            return cut, i
    return points[-1], None


def stitch_curve_evenly(
    points: typing.Sequence[Point],
    stitch_length: typing.List[float],
    tolerance: float,
    stitch_length_pos: int = 0,
) -> typing.Tuple[typing.List[Point], int]:
    """Split a curve into even-length stitches while handling curves correctly.

    Includes end point but not start point.
    """
    if len(points) < 2:
        return [], stitch_length_pos
    dist_left = [0] * len(points)
    for j in reversed(range(0, len(points) - 1)):
        dist_left[j] = dist_left[j + 1] + points[j].distance(points[j + 1])

    i: typing.Optional[int] = 1
    last = points[0]
    stitches: typing.List[Point] = []
    while i is not None and i < len(points):
        d = last.distance(points[i]) + dist_left[i]
        if d == 0:
            return stitches, stitch_length_pos
        # correction for rounding error
        stitch_len = d / math.ceil(d / stitch_length[stitch_length_pos]) + 0.000001

        stitch, newidx = take_stitch(last, points, i, stitch_len, tolerance)
        i = newidx
        if stitch is not None:
            stitches.append(stitch)
            last = stitch
            stitch_length_pos += 1
            if stitch_length_pos > len(stitch_length) - 1:
                stitch_length_pos = 0
    return stitches, stitch_length_pos


def stitch_curve_randomly(
    points: typing.Sequence[Point],
    stitch_length: typing.List[float],
    tolerance: float,
    stitch_length_sigma: float,
    random_seed: str,
    stitch_length_pos: int = 0,
) -> typing.Tuple[typing.List[Point], int]:
    """Split a curve into stitches of random length within a range.

    Attempts to randomize phase so distribution doesn't depend on direction.
    Includes end point but not start point.
    """
    if len(points) < 2:
        return [], stitch_length_pos

    # Initialize stitch length bounds
    min_stitch_length = max(0, stitch_length[stitch_length_pos] * (1 - stitch_length_sigma))
    max_stitch_length = stitch_length[stitch_length_pos] * (1 + stitch_length_sigma)

    i: typing.Optional[int] = 1
    last = points[0]
    last_shortened = 0.0
    stitches = []
    rand_iter = iter(prng.iter_uniform_floats(random_seed))
    while i is not None and i < len(points):
        if len(stitch_length) > 1:
            min_stitch_length = max(0, stitch_length[stitch_length_pos] * (1 - stitch_length_sigma))
            max_stitch_length = stitch_length[stitch_length_pos] * (1 + stitch_length_sigma)
            stitch_length_pos += 1
            if stitch_length_pos > len(stitch_length) - 1:
                stitch_length_pos = 0

        r = next(rand_iter)
        # If the last stitch was shortened due to tolerance (or this is the first stitch),
        # reduce the lower length limit to randomize the phase. This prevents moiré and asymmetry.
        stitch_len = lerp(last_shortened, 1.0, r) * lerp(min_stitch_length, max_stitch_length, r)

        stitch, newidx = take_stitch(last, points, i, stitch_len, tolerance)
        i = newidx
        if stitch is not None:
            stitches.append(stitch)
            last_shortened = min(last.distance(stitch) / stitch_len, 1.0)
            last = stitch
    return stitches, stitch_length_pos


def path_to_curves(points: typing.List[Point], min_len: float):
    """Split a path at obvious corner points so they get stitched exactly.

    min_len controls the minimum length after splitting for which it won't
    split again, used to avoid creating large numbers of corner points when
    encountering micro-messes.
    """
    if len(points) < 3:
        return [points]
    curves = []

    last = 0
    last_seg = points[1] - points[0]
    seg_len = last_seg.length()
    for i in range(1, len(points) - 1):
        # vectors of the last and next segments
        a = last_seg
        b = points[i + 1] - points[i]
        aabb = (a * a) * (b * b)
        abab = (a * b) * abs(a * b)

        # Test if the turn angle from vectors a to b is more than 45 degrees.
        # Optimized version of checking if cos(angle(a,b)) <= sqrt(0.5) and is defined
        if aabb > 0 and abab <= 0.5 * aabb:
            if seg_len >= min_len:
                curves.append(points[last:i + 1])
                last = i
            seg_len = 0

        if b * b > 0:
            last_seg = b
        seg_len += b.length()

    curves.append(points[last:])
    return curves


def even_running_stitch(points, stitch_length, tolerance):
    """Turn a continuous path into a running stitch with even length.

    Creates stitches as close to even length as possible (including first and
    last segments), keeping within the tolerance of the path.

    This should not be used for stitching tightly-spaced parallel curves as it
    tends to produce ugly moiré effects. Use random_running_stitch instead.
    """
    if not points:
        return
    stitches = [points[0]]
    last_stitch_length_pos = 0
    for curve in path_to_curves(points, 2 * tolerance):
        # Segments longer than twice tolerance are usually forced
        check_stop_flag()
        stitched_curve, last_stitch_length_pos = stitch_curve_evenly(curve, stitch_length, tolerance, last_stitch_length_pos)
        stitches.extend(stitched_curve)
    return stitches


def random_running_stitch(points, stitch_length, tolerance, stitch_length_sigma, random_seed):
    """Turn a continuous path into a running stitch with randomized length.

    Uses randomized phase and stitch length, keeping within the tolerance of
    the path. This is suitable for tightly-spaced parallel curves.
    """
    if not points:
        return
    stitches = [points[0]]
    last_stitch_length_pos = 0
    for i, curve in enumerate(path_to_curves(points, 2 * tolerance)):
        # Segments longer than twice tolerance are usually forced
        check_stop_flag()
        stitched_curve, last_stitch_length_pos = stitch_curve_randomly(
            curve,
            stitch_length,
            tolerance,
            stitch_length_sigma,
            prng.join_args(random_seed, i),
            last_stitch_length_pos,
        )
        stitches.extend(stitched_curve)
    return stitches


def running_stitch(points, stitch_length, tolerance, is_random, stitch_length_sigma, random_seed):
    """Create a running stitch with a choice of algorithm."""
    if is_random:
        return random_running_stitch(points, stitch_length, tolerance, stitch_length_sigma, random_seed)
    else:
        return even_running_stitch(points, stitch_length, tolerance)


def bean_stitch(stitches, repeats, tags_to_ignore=None):
    """Generate bean stitch from a set of stitches.

    "Bean" stitch is made by backtracking each stitch to make it heavier.  A
    simple bean stitch would be two stitches forward, one stitch back, two
    stitches forward, etc.  This would result in each stitch being tripled.

    We'll say that the above counts as 1 repeat.  Backtracking each stitch
    repeatedly will result in a heavier bean stitch.  There will always be
    an odd number of threads piled up for each stitch.

    Repeats is a list of a repeated pattern e.g. [0, 1, 3] doesn't repeat the first stitch,
    goes back and forth on the second stitch, goes goes 3 times back and forth on the third stitch,
    and starts the pattern again by not repeating the fourth stitch, etc.
    """

    if len(stitches) < 2:
        return stitches

    repeat_list_length = len(repeats)
    new_stitches = [stitches[0]]

    for i, stitch in enumerate(stitches[1:]):
        repeat_list_pos = i % repeat_list_length
        new_stitches.append(stitch)

        # ignore stitches with specified tags
        if tags_to_ignore and set(tags_to_ignore).intersection(stitch.tags):
            continue

        for i in range(repeats[repeat_list_pos]):
            new_stitches.extend(copy(new_stitches[-2:]))

    return new_stitches


def zigzag_stitch(stitches, zigzag_spacing, stroke_width, pull_compensation, peak_offset=0.0):
    """Create a zigzag stitch pattern from a set of stitches.

    Moves points left and right perpendicular to the path, alternating to
    create a zigzag pattern. Also redistributes stitches to ensure complete
    zigzag cycles (starting and ending at the same peak/valley position).

    Args:
        stitches: List of stitch points along the path.
        zigzag_spacing: Spacing between zigzag peaks.
        stroke_width: Width of the stroke for offset calculation.
        pull_compensation: Tuple of (left, right) pull compensation values.
        peak_offset: How much to shift peak stitches forward along the path (in pixels).
                    Positive values shift peaks forward, negative shifts backward.
                    This creates a slanted/leaning zigzag effect.
    """
    if len(stitches) < 2:
        return stitches

    # Build a line from the original stitches
    coords = [(s.x, s.y) for s in stitches]
    line = LineString(coords)
    total_length = line.length

    if total_length == 0:
        return stitches

    # Get the half-spacing (distance between consecutive zigzag points)
    half_spacing = zigzag_spacing[0] / 2 if isinstance(zigzag_spacing, list) else zigzag_spacing / 2

    # Calculate how many segments fit in the path
    num_segments = max(2, round(total_length / half_spacing))

    # For symmetric zigzag (start and end at same position - both peaks):
    # We need an ODD number of points = EVEN number of segments
    # Pattern: peak(0) -> valley(1) -> peak(2) -> valley(3) -> peak(4) = 5 points, 4 segments
    if num_segments % 2 == 1:
        num_segments += 1

    num_points = num_segments + 1

    # First, interpolate all positions along the path and store them
    # We need these ORIGINAL positions to calculate directions correctly
    original_positions = []
    for i in range(num_points):
        distance = (i / num_segments) * total_length
        point = line.interpolate(distance)
        original_positions.append(Point(point.x, point.y))

    # Create the new stitches list
    stitch_class = type(stitches[0])
    new_stitches = []
    for i in range(num_points):
        pos = original_positions[i]
        if i < len(stitches):
            # Reuse existing stitch object, just update position
            stitches[i].x = pos.x
            stitches[i].y = pos.y
            new_stitches.append(stitches[i])
        else:
            # Need to create a new stitch
            new_stitches.append(stitch_class(pos.x, pos.y))

    # Now apply the zigzag offsets using the ORIGINAL positions for direction
    offset1 = stroke_width / 2 + pull_compensation[0]
    offset2 = stroke_width / 2 + pull_compensation[1]

    for i, _ in enumerate(new_stitches):
        # Calculate direction using ORIGINAL positions (not the offset ones)
        if i < len(original_positions) - 1:
            start = original_positions[i]
            end = original_positions[i + 1]
        else:
            # Last stitch: use previous segment's direction from original positions
            start = original_positions[i - 1]
            end = original_positions[i]

        seg_length = (end - start).length()
        if seg_length == 0:
            continue

        segment_direction = (end - start).unit()
        zigzag_direction = segment_direction.rotate_left()

        # Alternate: even indices go one way, odd indices go the other
        if i % 2 == 1:
            # Valley stitch - offset perpendicular only
            new_stitches[i] += zigzag_direction * -offset1
        else:
            # Peak stitch - offset perpendicular + forward shift along path
            new_stitches[i] += zigzag_direction * offset2
            # Apply peak offset (shift forward along the path direction)
            if peak_offset != 0:
                new_stitches[i] += segment_direction * peak_offset

    return new_stitches
