from copy import copy

""" Utility functions to produce running stitches. """


def running_stitch(points, stitch_length):
    """Generate running stitch along a path.

    Given a path and a stitch length, walk along the path in increments of the
    stitch length.  If sharp corners are encountered, an extra stitch will be
    added at the corner to avoid rounding the corner.  The starting and ending
    point are always stitched.

    The path is described by a set of line segments, each connected to the next.
    The line segments are described by a sequence of points.
    """

    if len(points) < 2:
        return []

    output = []
    segment_start = points[0]
    last_segment_direction = None

    # This tracks the distance we've traveled along the current segment so
    # far.  Each time we make a stitch, we add the stitch_length to this
    # value.  If we fall off the end of the current segment, we carry over
    # the remainder to the next segment.
    distance = 0.0

    for segment_end in points[1:]:
        segment = segment_end - segment_start
        segment_length = segment.length()

        if segment_length == 0:
            continue

        segment_direction = segment.unit()

        # corner detection
        if last_segment_direction:
            cos_angle_between = segment_direction * last_segment_direction

            # This checks whether the corner is sharper than 45 degrees.
            if cos_angle_between < 0.5:
                # Only add the corner point if it's more than 0.1mm away to
                # avoid a double-stitch.
                if (segment_start - output[-1]).length() > 0.1:
                    # add a stitch at the corner
                    output.append(segment_start)

                    # next stitch needs to be stitch_length along this segment
                    distance = stitch_length

        while distance < segment_length:
            output.append(segment_start + distance * segment_direction)
            distance += stitch_length

        # prepare for the next segment
        segment_start = segment_end
        last_segment_direction = segment_direction
        distance -= segment_length

    # stitch a single point if the path has a length of zero
    if not output:
        output.append(segment_start)

    # stitch the last point unless we're already almost there
    if (segment_start - output[-1]).length() > 0.1 or len(output) == 0:
        output.append(segment_start)

    return output


def bean_stitch(stitches, repeats):
    """Generate bean stitch from a set of stitches.

    "Bean" stitch is made by backtracking each stitch to make it heaver.  A
    simple bean stitch would be two stitches forward, one stitch back, two
    stitches forward, etc.  This would result in each stitch being tripled.

    We'll say that the above counts as 1 repeat.  Backtracking each stitch
    repeatedly will result in a heavier bean stitch.  There will always be
    an odd number of threads piled up for each stitch.
    """

    if len(stitches) < 2:
        return stitches

    new_stitches = [stitches[0]]

    for stitch in stitches:
        new_stitches.append(stitch)

        for i in range(repeats):
            new_stitches.extend(copy(new_stitches[-2:]))

    return new_stitches
