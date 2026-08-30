from shapely import geometry as shgeo

from .satin_column import SatinColumn
from .satin_processor import SatinProcessor
from ..element import PIXELS_PER_MM
from ...debug.debug import debug
from ...utils.geometry import Point
from ...utils.threading import check_stop_flag


def get_rails_to_reverse(choice: str, rails: list[list[tuple[float, float]]]) -> tuple[bool, bool]:
    if choice == 'first':
        return True, False
    elif choice == 'second':
        return False, True
    elif choice == 'both':
        return True, True
    elif choice == 'automatic':
        rails = [shgeo.LineString(rail) for rail in rails]
        if len(rails) == 2:
            # Sample ten points along the rails.  Compare the distance
            # between corresponding points on both rails with and without
            # one rail reversed.  If the average distance between points
            # with one rail reversed is less than without one reversed, then
            # the user has probably accidentally reversed a rail.
            lengths = []
            lengths_reverse = []

            for i in range(10):
                distance = i / 10
                point0 = rails[0].interpolate(distance, normalized=True)
                point1 = rails[1].interpolate(distance, normalized=True)
                point1_reverse = rails[1].interpolate(1 - distance, normalized=True)

                lengths.append(point0.distance(point1))
                lengths_reverse.append(point0.distance(point1_reverse))

            debug.log(f"lengths: {lengths}")
            debug.log(f"lengths_reverse: {lengths_reverse}")
            if sum(lengths) > sum(lengths_reverse):
                # reverse the second rail
                return False, True

    return False, False

def _stitch_distance(pos0: Point, pos1: Point, previous_pos0: Point, previous_pos1: Point) -> float:
    """Return the distance from one stitch to the next."""

    previous_stitch = previous_pos1 - previous_pos0
    if previous_stitch.length() < 0.01:
        return shgeo.LineString((pos0, pos1)).distance(shgeo.Point(previous_pos0))
    else:
        # Measure the distance at a right angle to the previous stitch, at
        # the start and end of the stitch, and pick the biggest.  If we're
        # going around a curve, the points on the inside of the curve will
        # be much closer together, and we only care about the distance on
        # the outside of the curve.
        #
        # In this example with two horizontal stitches, we want the vertical
        # separation between them.
        #  _________
        #  \_______/
        normal = previous_stitch.unit().rotate_left()
        d0 = pos0 - previous_pos0
        d1 = pos1 - previous_pos1
        return max(abs(d0 * normal), abs(d1 * normal))

@debug.time
def plot_points_on_rails(satin: 'SatinColumn', spacing: float | int, offset_px: tuple[float, float] = (0, 0),
                         offset_proportional: tuple[float, float] = (0, 0), use_random: bool = False,
                         ) -> list[tuple[Point, Point]]:
    # Take a section from each rail in turn, and plot out an equal number
    # of points on both rails.  Return the points plotted. The points will
    # be contracted or expanded by offset using self.offset_points().

    processor = SatinProcessor(satin, offset_px, offset_proportional, use_random)

    pairs = []

    for i, (section0, section1) in enumerate(satin.flattened_sections):
        check_stop_flag()

        if i == 0:
            old_pos0 = section0[0]
            old_pos1 = section1[0]
            pairs.append(processor.process_points(old_pos0, old_pos1))

        path0 = shgeo.LineString(section0)
        path1 = shgeo.LineString(section1)

        # Base the number of stitches in each section on the _longer_ of
        # the two sections. Otherwise, things could get too sparse when one
        # side is significantly longer (e.g. when going around a corner).
        num_points = max(path0.length, path1.length, 0.01) / spacing

        # Section stitch spacing and the cursor are expressed as a fraction
        # of the total length of the path, because we use normalized=True
        # below.
        section_stitch_spacing = 1.0 / num_points

        # current_spacing, however, is in pixels.
        spacing_multiple = processor.get_stitch_spacing_multiple()
        current_spacing = spacing * spacing_multiple

        # In all sections after the first, we need to figure out how far to
        # travel before placing the first stitch.
        distance = _stitch_distance(section0[0], section1[0], old_pos0, old_pos1)
        to_travel = (1 - min(distance / spacing, 1.0)) * section_stitch_spacing * spacing_multiple
        debug.log(f"num_points: {num_points}, section_stitch_spacing: {section_stitch_spacing}, distance: {distance}, to_travel: {to_travel}")

        cursor = 0
        iterations = 0
        while cursor + to_travel <= 1:
            iterations += 1
            pos0 = Point.from_shapely_point(path0.interpolate(cursor + to_travel, normalized=True))
            pos1 = Point.from_shapely_point(path1.interpolate(cursor + to_travel, normalized=True))

            # If the rails are parallel, then our stitch spacing will be
            # perfect.  If the rails are coming together or spreading apart,
            # then we'll have to travel much further along the rails to get
            # the right stitch spacing.  Imagine a satin like the letter V:
            #
            # \______/
            #  \____/
            #   \__/
            #    \/
            #
            # In this case the stitches will be way too close together.
            # We'll compensate for that here.
            #
            # We'll measure how far this stitch is from the previous one.
            # If we went one third as far as we were expecting to, then
            # we'll need to try again, this time travelling 3x as far as we
            # originally tried.
            #
            # This works great for the V, but what if things change
            # mid-stitch?
            #
            # \      /
            #  \    /
            #   \  /
            #    ||
            #
            # In this case, we may way overshoot.  We can also undershoot
            # for similar reasons.  To deal with that, we'll revise our
            # guess a second time.  Two tries seems to be the sweet spot.
            #
            # In any case, we'll only revise if our stitch spacing is off by
            # more than 5%.
            if iterations <= 2:
                distance = _stitch_distance(pos0, pos1, old_pos0, old_pos1)
                if distance > 0.01 and abs((current_spacing - distance) / current_spacing) > 0.05:
                    # We'll revise to_travel then go back to the start of
                    # the loop and try again.
                    to_travel = (current_spacing / distance) * to_travel
                    if iterations == 1:
                        # Don't overshoot the end of this section on the
                        # first try. If we've gone too far, we want to have
                        # a chance to correct.
                        to_travel = min(to_travel, 1 - cursor)
                    continue

            cursor += to_travel
            spacing_multiple = processor.get_stitch_spacing_multiple()
            to_travel = section_stitch_spacing * spacing_multiple
            current_spacing = spacing * spacing_multiple

            old_pos0 = pos0
            old_pos1 = pos1
            pairs.append(processor.process_points(pos0, pos1))
            iterations = 0

    # Add one last stitch at the end unless our previous stitch is already
    # really close to the end.
    if pairs and section0 and section1:
        if _stitch_distance(section0[-1], section1[-1], old_pos0, old_pos1) > 0.1 * PIXELS_PER_MM:
            pairs.append(processor.process_points(section0[-1], section1[-1]))

    return pairs
