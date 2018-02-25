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

    output = [points[0]]
    segment_start = points[0]
    last_segment_direction = None

    # This tracks the distance we've travelled along the current segment so
    # far.  Each time we make a stitch, we add the stitch_length to this
    # value.  If we fall off the end of the current segment, we carry over
    # the remainder to the next segment.
    distance = 0.0

    for segment_end in points[1:]:
        segment = segment_end - segment_start
        segment_length = segment.length()
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

    # stitch the last point unless we're already almos there
    if (segment_start - points[-1]).length() > 0.1:
        output.append(segment_start)

    return output
