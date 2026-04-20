# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
from math import pi, sqrt
from random import random

import inkex
from inkex.paths import Path

from ..i18n import _
from ..utils import Point
from ..utils.cache import cache
from .tags import (CONNECTION_END, CONNECTION_START, CONNECTOR_TYPE,
                   INKSCAPE_GROUPMODE, INKSCAPE_LABEL, INKSTITCH_ATTRIBS, XLINK_HREF)
from .units import PIXELS_PER_MM, get_viewbox_transform

# The stitch vector path looks like this:
#  _______
# (_______)
#
# It's 0.32mm high, which is the approximate thickness of common machine
# embroidery threads.
# 1.398 pixels = 0.37mm
stitch_height = 1.398

# This vector path starts at the upper right corner of the stitch shape and
# proceeds counter-clockwise and contains a placeholder (%s) for the stitch
# length.
#
# It contains four invisible "whiskers" of zero width that go outwards
# to ensure that the SVG renderer allocates a large enough canvas area when
# computing the gaussian blur steps:
# \_____/
# (_____)  (whiskers not to scale)
# /     \
# This is necessary to avoid artifacting near the edges and corners that seems to be due to
# edge conditions for the feGaussianBlur, which is used to build the heightmap for
# the feDiffuseLighting node. So we need some extra buffer room around the shape.
# The whiskers let us specify a "fixed" amount of spacing around the stitch.
# Otherwise, we'd have to expand the width and height attributes of the <filter>
# tag to add more buffer space. The filter's width and height are specified in multiples of
# the bounding box size, It's the bounding box aligned with the global SVG canvas's axes,
# not the axes of the stitch itself.  That means that having a big enough value
# to add enough padding on the long sides of the stitch would waste a ton
# of space on the short sides and significantly slow down rendering.

# The specific extent of the whiskers (0.55 parallel to the stitch, 0.1 perpendicular)
# was found by experimentation. It seems to work with almost no artifacting.
stitch_path = (
    "M0,0"  # Start point
    "l0.55,-0.1,-0.55,0.1"  # Bottom-right whisker
    "c0.613,0,0.613,1.4,0,1.4"  # Right endcap
    "l0.55,0.1,-0.55,-0.1"  # Top-right whisker
    "h-%s"  # Stitch length
    "l-0.55,0.1,0.55,-0.1"  # Top-left whisker
    "c-0.613,0,-0.613,-1.4,0,-1.4"  # Left endcap
    "l-0.55,-0.1,0.55,0.1"  # Bottom-left whisker
    "z")  # return to start


def generate_realistic_filter() -> inkex.BaseElement:
    """
    Return a copy of the realistic stitch filter, ready to add to svg defs.
    """
    filter = inkex.Filter(attrib={
       "style": "color-interpolation-filters:sRGB",
       "id": "realistic-stitch-filter",
       "x": "0",
       "width": "1",
       "y": "0",
       "height": "1",
       inkex.addNS('auto-region', 'inkscape'): "false",
    })

    filter.add(
        inkex.Filter.GaussianBlur(attrib={
            "edgeMode": "none",
            "stdDeviation": "0.9",
            "in": "SourceAlpha",
        }),
        inkex.Filter.SpecularLighting(
            inkex.Filter.DistantLight(attrib={
                "azimuth": "154",
                "elevation": "112",
            }), attrib={
                "result": "result2",
                "surfaceScale": "4.29",
                "specularConstant": "0.65",
                "specularExponent": "1.6",
            }
        ),
        inkex.Filter.Composite(attrib={
            "in2": "SourceAlpha",
            "operator": "atop",
        }),
        inkex.Filter.Composite(attrib={
            "in2": "SourceGraphic",
            "operator": "arithmetic",
            "result": "result3",
            "k1": "0",
            "k2": "0.8",
            "k3": "1.2",
            "k4": "0",
        })
    )

    return filter


def realistic_stitch(start, end):
    """Generate a stitch vector path given a start and end point."""

    end = Point(*end)
    start = Point(*start)

    stitch_length = (end - start).length()
    stitch_center = Point((end.x+start.x)/2.0, (end[1]+start[1])/2.0)
    stitch_direction = (end - start)
    stitch_angle = math.atan2(stitch_direction.y, stitch_direction.x) * (180 / pi)

    stitch_length = max(0, stitch_length - 0.2 * PIXELS_PER_MM)

    # rotate the path to match the stitch
    rotation_center_x = -stitch_length / 2.0
    rotation_center_y = stitch_height / 2.0

    transform = (
        inkex.Transform()
             .add_translate(stitch_center.x - rotation_center_x, stitch_center.y - rotation_center_y)
             .add_rotate(stitch_angle, (rotation_center_x, rotation_center_y))
    )

    # create the path by filling in the length in the template, and transforming it as above
    path = Path(stitch_path % stitch_length).transform(transform, True)

    return str(path)


def color_block_to_point_lists(color_block, render_jumps=True):
    point_lists = [[]]
    current = point_lists[0]
    _append = current.append

    for stitch in color_block:
        if stitch._flags:
            if stitch.trim:
                if current:
                    current = []
                    point_lists.append(current)
                    _append = current.append
                    continue
            if stitch.jump:
                if not render_jumps and current:
                    current = []
                    point_lists.append(current)
                    _append = current.append
                continue
            continue
        _append((stitch.x, stitch.y))

    # filter out empty point lists
    point_lists = [p for p in point_lists if len(p) > 1]

    return point_lists


@cache
def get_correction_transform(svg):
    transform = get_viewbox_transform(svg)

    # we need to correct for the viewbox
    transform = -inkex.transforms.Transform(transform)

    return str(transform)


def color_block_to_realistic_stitches(color_block, svg, destination, render_jumps=True):
    for point_list in color_block_to_point_lists(color_block, render_jumps):
        color = color_block.color.visible_on_white.darker.to_hex_str()
        start = point_list[0]
        for point in point_list[1:]:
            destination.append(inkex.PathElement(attrib={
                'style': "fill: %s; stroke: none; filter: url(#realistic-stitch-filter);" % color,
                'd': realistic_stitch(start, point),
                'transform': get_correction_transform(svg)
            }))
            start = point


def color_block_to_paths(color_block, svg, destination, visual_commands, line_width, render_jumps=True):
    from ..commands import ensure_symbol, get_command_description
    from ..svg import generate_unique_id, get_correction_transform as get_node_correction_transform

    stitches = color_block.stitches
    n = len(stitches)

    # Fast path: if no special stitches in block, use list comprehension (C-level loop)
    if n > 1 and not any(s._flags for s in stitches):
        _round = round
        d = "M" + " ".join([f"{_round(s.x)} {_round(s.y)}" for s in stitches])
        s_prev = stitches[-2]
        s_last = stitches[-1]
        segments = [(d, ((s_prev.x, s_prev.y), (s_last.x, s_last.y)))]
    else:
        # Slow path: handle trims/jumps/etc with per-stitch flag checks
        segments = []
        coord_strs = []
        _coord_append = coord_strs.append
        last_x = last_y = prev_x = prev_y = 0.0
        count = 0

        for stitch in stitches:
            if stitch._flags:
                if stitch.trim:
                    if count > 1:
                        segments.append(("M" + " ".join(coord_strs), ((prev_x, prev_y), (last_x, last_y))))
                    coord_strs = []
                    _coord_append = coord_strs.append
                    count = 0
                    continue
                if stitch.jump:
                    if not render_jumps and count > 0:
                        if count > 1:
                            segments.append(("M" + " ".join(coord_strs), ((prev_x, prev_y), (last_x, last_y))))
                        coord_strs = []
                        _coord_append = coord_strs.append
                        count = 0
                    continue
                continue
            prev_x, prev_y = last_x, last_y
            last_x = stitch.x
            last_y = stitch.y
            _coord_append(f"{last_x} {last_y}")
            count += 1

        if count > 1:
            segments.append(("M" + " ".join(coord_strs), ((prev_x, prev_y), (last_x, last_y))))

    # Build SVG paths from segments
    first = True
    path = None
    prev_last_points = None
    color = color_block.color.visible_on_white.to_hex_str()
    correction_transform = get_correction_transform(svg)
    style = f"stroke: {color}; stroke-width: {line_width}; fill: none;stroke-linejoin: round;stroke-linecap: round;"
    _stroke_method = INKSTITCH_ATTRIBS['stroke_method']

    for d_string, last_points in segments:
        if first:
            first = False
        elif visual_commands:
            _add_command_fast(svg, path, prev_last_points, "trim",
                              ensure_symbol, get_command_description, generate_unique_id, get_node_correction_transform)
        else:
            assert path is not None
            path.set(INKSTITCH_ATTRIBS['trim_after'], 'true')

        path = inkex.PathElement(attrib={
            'id': svg.get_unique_id("object"),
            'style': style,
            'd': d_string,
            'transform': correction_transform,
            _stroke_method: 'manual_stitch'
        })
        destination.append(path)
        prev_last_points = last_points

    if path is not None and color_block.trim_after:
        if visual_commands:
            _add_command_fast(svg, path, prev_last_points, "trim",
                              ensure_symbol, get_command_description, generate_unique_id, get_node_correction_transform)
        else:
            path.set(INKSTITCH_ATTRIBS['trim_after'], 'true')

    if path is not None and color_block.stop_after:
        if visual_commands:
            _add_command_fast(svg, path, prev_last_points, "stop",
                              ensure_symbol, get_command_description, generate_unique_id, get_node_correction_transform)
        else:
            path.set(INKSTITCH_ATTRIBS['stop_after'], 'true')


def _add_command_fast(svg, path_node, last_points, command,
                      ensure_symbol, get_command_description, generate_unique_id, get_node_correction_transform):
    """Lightweight version of add_commands for paths with known point data.

    Avoids creating Stroke elements and the expensive Shapely/bezier chain.
    Produces the same SVG structure: group containing a symbol and connector.
    last_points is ((prev_x, prev_y), (last_x, last_y)) - the last two points of the segment.
    """
    ensure_symbol(svg, command)

    # Compute position near the end of the path, offset perpendicular by 10 units
    distance = 10
    prev = last_points[0]
    last = last_points[1]
    dx = last[0] - prev[0]
    dy = last[1] - prev[1]
    length = sqrt(dx * dx + dy * dy) or 1.0
    # Perpendicular offset + slight randomness to avoid stacking
    perp_x = -dy / length * distance
    perp_y = dx / length * distance
    jitter = random() * 0.05 * distance
    pos_x = last[0] + perp_x + jitter
    pos_y = last[1] + perp_y + jitter

    # Use midpoint of last two points as approximate centroid
    centroid_x = (prev[0] + last[0]) / 2
    centroid_y = (prev[1] + last[1]) / 2

    # Create group
    parent = path_node.getparent()
    description = _(get_command_description(command))
    group = inkex.Group(attrib={
        "id": generate_unique_id(svg, "command_group"),
        INKSCAPE_LABEL: _("Ink/Stitch Command") + f": {description}",
        "transform": get_node_correction_transform(path_node)
    })
    parent.insert(parent.index(path_node) + 1, group)

    # Create symbol
    symbol = inkex.Use(attrib={
        "id": svg.get_unique_id("command_use"),
        XLINK_HREF: "#inkstitch_%s" % command,
        "height": "100%",
        "width": "100%",
        "x": str(pos_x),
        "y": str(pos_y),
        INKSCAPE_LABEL: _("command marker"),
    })
    group.append(symbol)

    # Ensure path has an id for connector reference
    if path_node.get('id') is None:
        path_node.set('id', svg.get_unique_id("object"))

    # Create connector line from symbol to centroid
    connector = inkex.PathElement(attrib={
        "id": generate_unique_id(svg, "command_connector"),
        "d": f"M {pos_x},{pos_y} {centroid_x},{centroid_y}",
        "style": "fill:none;stroke:#000000;stroke-width:1;stroke-opacity:0.5;vector-effect: non-scaling-stroke;-inkscape-stroke: hairline;",
        CONNECTION_START: f"#{symbol.get('id')}",
        CONNECTION_END: f"#{path_node.get('id')}",
        INKSCAPE_LABEL: _("connector"),
        CONNECTOR_TYPE: "polyline",
    })
    group.insert(0, connector)


def render_stitch_plan(svg, stitch_plan, realistic=False, visual_commands=True, render_jumps=True, line_width=0.4) -> inkex.Group:
    layer_or_image = svg.findone(".//*[@id='__inkstitch_stitch_plan__']")
    if layer_or_image is not None:
        layer_or_image.delete()

    layer = inkex.Group(attrib={
        'id': '__inkstitch_stitch_plan__',
        INKSCAPE_LABEL: _('Stitch Plan'),
        INKSCAPE_GROUPMODE: 'layer'
    })
    svg.append(layer)

    for i, color_block in enumerate(stitch_plan):
        group = inkex.Group(attrib={
            'id': f'__color_block_{i}__',
            INKSCAPE_LABEL: f"color block {(i + 1)}"
        })
        layer.append(group)
        if realistic:
            color_block_to_realistic_stitches(color_block, svg, group, render_jumps)
        else:
            color_block_to_paths(color_block, svg, group, visual_commands, line_width, render_jumps)

    if realistic:
        # Remove filter from defs, if any
        filter: inkex.BaseElement = svg.defs.findone("//*[@id='realistic-stitch-filter']")
        if filter is not None:
            filter.delete()

        svg.defs.append(generate_realistic_filter())

    return layer
