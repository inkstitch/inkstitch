# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import numpy as np
from scipy.spatial import KDTree


def get_stitch_density(stitch_plan, radius):
    stitches = []
    for color_block in stitch_plan:
        for stitch in color_block:
            stitches.append((stitch.x, stitch.y))

    # get density per stitch
    tree = KDTree(np.array(stitches))
    neighbors = tree.query_ball_tree(tree, radius)
    density = [len(i) for i in neighbors], stitches

    return density
