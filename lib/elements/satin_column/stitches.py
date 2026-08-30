import itertools

from elements import SatinColumn
from elements.satin_column.rails import plot_points_on_rails
from stitch_plan import StitchGroup
from utils import prng
from utils.threading import check_stop_flag


def _do_e_stitch(satin: 'SatinColumn'):
    # e stitch: do a pattern that looks like the letter "E".  It looks like
    # this:
    #
    # _|_|_|_|_|_|_|_|_|_|_|_|

    stitch_group = StitchGroup(color=satin.color)

    pairs = plot_points_on_rails(
        satin,
        satin.zigzag_spacing,
        satin.pull_compensation_px,
        satin.pull_compensation_percent / 100,
        True,
    )

    short_pairs = satin.inset_short_stitches_sawtooth(pairs)
    max_stitch_length = satin.max_stitch_length_px
    length_sigma = satin.random_split_jitter
    random_phase = satin.random_split_phase
    min_split_length = satin.min_random_split_length_px
    seed = satin.random_seed
    last_point = None
    # "left" and "right" here are kind of arbitrary designations meaning
    # a point from the first and second rail respectively
    for i, (left, right), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
        check_stop_flag()
        split_points, _ = satin.get_split_points(
            left, right, a_short, b_short, max_stitch_length,
            None, length_sigma, random_phase, min_split_length,
            prng.join_args(seed, 'satin-split', 2 * i + 1), 2 * i + 1)

        # zigzag spacing is wider than stitch length, subdivide
        if last_point is not None and max_stitch_length is not None and satin.zigzag_spacing > max_stitch_length:
            points, _ = satin.get_split_points(last_point, left, last_point, left, max_stitch_length)
            stitch_group.add_stitches(points)

        stitch_group.add_stitch(a_short, ("edge", "left"))
        stitch_group.add_stitches(split_points, ("split_stitch",))
        stitch_group.add_stitch(b_short, ("edge",))
        stitch_group.add_stitches(split_points[::-1], ("split_stitch",))
        stitch_group.add_stitch(a_short, ("edge",))

        last_point = a_short

    if satin.center_walk_is_odd():
        stitch_group.stitches = list(reversed(stitch_group.stitches))

    stitch_group.add_tags(("satin_column", "e_stitch"))
    return stitch_group


def _do_s_stitch(satin: 'SatinColumn'):
    # S stitch: do a pattern that looks like the letter "S".  It looks like
    # this:
    #   _   _   _   _   _   _
    # _| |_| |_| |_| |_| |_| |

    stitch_group = StitchGroup(color=satin.color)

    pairs = plot_points_on_rails(
        satin,
        satin.zigzag_spacing,
        satin.pull_compensation_px,
        satin.pull_compensation_percent / 100,
        True,
    )

    short_pairs = satin.inset_short_stitches_sawtooth(pairs)
    max_stitch_length = satin.max_stitch_length_px
    length_sigma = satin.random_split_jitter
    random_phase = satin.random_split_phase
    min_split_length = satin.min_random_split_length_px
    seed = satin.random_seed
    last_point = None
    for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
        check_stop_flag()
        points = [a_short]
        split_points, _ = satin.get_split_points(
            a, b, a_short, b_short, max_stitch_length,
            None, length_sigma, random_phase, min_split_length,
            prng.join_args(seed, 'satin-split', i), i)
        points.extend(split_points)
        points.append(b_short)

        if i % 2 == 0:
            points = list(reversed(points))

        # zigzag spacing is wider than stitch length, subdivide
        if last_point is not None and max_stitch_length is not None and satin.zigzag_spacing > max_stitch_length:
            initial_points, _ = satin.get_split_points(last_point, points[0], last_point, points[0], max_stitch_length)

        stitch_group.add_stitches(points)
        last_point = points[-1]

    if satin.center_walk_is_odd():
        stitch_group.stitches = list(reversed(stitch_group.stitches))

    stitch_group.add_tags(("satin_column", "s_stitch"))
    return stitch_group


def _do_zigzag(satin: 'SatinColumn'):
    stitch_group = StitchGroup(color=satin.color)

    # calculate pairs at double the requested density
    pairs = plot_points_on_rails(
        satin,
        satin.zigzag_spacing / 2.0,
        satin.pull_compensation_px,
        satin.pull_compensation_percent / 100,
        True,
    )

    # alternate picking one point from each pair, first on one rail then the other
    points = [p[i % 2] for i, p in enumerate(pairs)]

    # turn the list of points back into pairs
    pairs = [points[i:i + 2] for i in range(0, len(points), 2)]

    # remove last item if it isn't paired up
    if len(pairs[-1]) == 1:
        del pairs[-1]

    short_pairs = satin.inset_short_stitches_sawtooth(pairs)
    max_stitch_length = satin.max_stitch_length_px
    length_sigma = satin.random_split_jitter
    random_phase = satin.random_split_phase
    min_split_length = satin.min_random_split_length_px
    seed = satin.random_seed

    last_point = None
    last_point_short = None
    for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
        if last_point:
            split_points, _ = satin.get_split_points(
                last_point, a, last_point_short, a_short, max_stitch_length, None,
                length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i), row_num=2 * i,
                from_end=True)
            stitch_group.add_stitches(split_points, ("satin_column", "zigzag_split_stitch"))

        stitch_group.add_stitch(a_short, ("satin_column", "peak_a", "peak_stitch"))

        split_points, _ = satin.get_split_points(
            a, b, a_short, b_short, max_stitch_length, None,
            length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i + 1),
            row_num=2 * i + 1)
        stitch_group.add_stitches(split_points, ("satin_column", "zigzag_split_stitch"))

        stitch_group.add_stitch(b_short, ("satin_column", "peak_b", "peak_stitch"))

        last_point = b
        last_point_short = b_short

    if satin.center_walk_is_odd():
        stitch_group.stitches = list(reversed(stitch_group.stitches))

    return stitch_group

def _do_satin(satin: 'SatinColumn'):
    # satin: do a zigzag pattern, alternating between the paths.  The
    # zigzag looks like this to make the satin stitches look perpendicular
    # to the column:
    #
    # |/|/|/|/|/|/|/|/|

    # print >> dbg, "satin", self.zigzag_spacing, self.pull_compensation

    stitch_group = StitchGroup(color=satin.color)

    # pull compensation is automatically converted from mm to pixels by get_float_param
    pairs = plot_points_on_rails(
        satin,
        satin.zigzag_spacing,
        satin.pull_compensation_px,
        satin.pull_compensation_percent / 100,
        True,
        )

    max_stitch_length = satin.max_stitch_length_px
    length_sigma = satin.random_split_jitter
    random_phase = satin.random_split_phase
    min_split_length = satin.min_random_split_length_px
    seed = satin.random_seed

    short_pairs = satin.inset_short_stitches_sawtooth(pairs)

    last_point = None
    last_short_point = None
    last_count = None
    for i, (a, b), (a_short, b_short) in zip(itertools.count(0), pairs, short_pairs):
        if last_point is not None:
            split_points, _ = satin.get_split_points(
                last_point, a, last_short_point, a_short, max_stitch_length, last_count,
                length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i), row_num=2 * i, from_end=True)
            stitch_group.add_stitches(split_points, ("satin_column", "satin_split_stitch"))

        stitch_group.add_stitch(a_short)
        stitch_group.stitches[-1].add_tags(("satin_column", "satin_column_edge"))

        split_points, last_count = satin.get_split_points(
            a, b, a_short, b_short, max_stitch_length, None,
            length_sigma, random_phase, min_split_length, prng.join_args(seed, 'satin-split', 2 * i + 1), row_num=2 * i + 1)
        stitch_group.add_stitches(split_points, ("satin_column", "satin_split_stitch"))

        stitch_group.add_stitch(b_short)
        stitch_group.stitches[-1].add_tags(("satin_column", "satin_column_edge"))
        last_point = b
        last_short_point = b_short

    if satin.center_walk_is_odd():
        stitch_group.stitches = list(reversed(stitch_group.stitches))

    return stitch_group

def do_top_layer_stitch_group(satin: 'SatinColumn'):
    if satin.satin_method == 'e_stitch':
        return _do_e_stitch(satin)
    elif satin.satin_method == 's_stitch':
        return _do_s_stitch(satin)
    elif satin.satin_method == 'zigzag':
        return _do_zigzag(satin)
    else:
        return _do_satin(satin)
