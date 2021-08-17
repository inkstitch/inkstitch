from .running_stitch import running_stitch


def simple_satin(path, zigzag_spacing, width):
    """zig-zag along the path at the specified spacing and width

    Parameters:
        path -- a list of Point instances
        zigzag_spacing -- the length for a zig and a zag together (a V shape)
        width -- how wide the satin should be

    Returns:
        a list of Point instances
    """

    # Start with a running stitch at half the zigzag spacing.
    points = running_stitch(path, zigzag_spacing / 2.0)

    # Now move the points left and right.  Consider each pair
    # of points in turn, and move perpendicular to them,
    # alternating left and right.

    offset = width / 2.0

    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        segment_direction = (end - start).unit()
        zigzag_direction = segment_direction.rotate_left()

        if i % 2 == 1:
            zigzag_direction *= -1

        points[i] += zigzag_direction * offset

    return points
