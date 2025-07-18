# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import JOIN_STYLE


def get_join_style_args(element):
    """Convert svg line join style to shapely offset_curve arguments."""

    args = {
        # mitre is the default per SVG spec
        'join_style': JOIN_STYLE.mitre
    }

    element_join_style = element.get_style('stroke-linejoin')

    if element_join_style is not None:
        if element_join_style == "miter":
            args['join_style'] = JOIN_STYLE.mitre

            # 4 is the default per SVG spec
            miter_limit = float(element.get_style('stroke-miterlimit', 4))
            args['mitre_limit'] = miter_limit
        elif element_join_style == "bevel":
            args['join_style'] = JOIN_STYLE.bevel
        elif element_join_style == "round":
            args['join_style'] = JOIN_STYLE.round

    return args
