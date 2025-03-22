# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math
from math import pi

import inkex

from ..i18n import _
from ..utils import Point, cache
from .tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL, INKSTITCH_ATTRIBS
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
    path = inkex.Path(stitch_path % stitch_length).transform(transform, True)

    return str(path)


def color_block_to_point_lists(color_block, render_jumps=True):
    point_lists = [[]]

    for stitch in color_block:
        if stitch.trim:
            if point_lists[-1]:
                point_lists.append([])
                continue
        if stitch.jump and not render_jumps and point_lists[-1]:
            point_lists.append([])
            continue

        if not stitch.jump and not stitch.color_change and not stitch.stop:
            point_lists[-1].append(stitch.as_tuple())

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
    # If we try to import these above, we get into a mess of circular
    # imports.
    from ..commands import add_commands
    from ..elements.stroke import Stroke

    # We could emit just a single path with one subpath per point list, but
    # emitting multiple paths makes it easier for the user to manipulate them.
    first = True
    path = None
    for point_list in color_block_to_point_lists(color_block, render_jumps):
        if first:
            first = False
        elif visual_commands:
            add_commands(Stroke(destination[-1]), ["trim"])
        else:
            path.set(INKSTITCH_ATTRIBS['trim_after'], 'true')

        color = color_block.color.visible_on_white.to_hex_str()
        path = inkex.PathElement(attrib={
            'id': svg.get_unique_id("object"),
            'style': f"stroke: {color}; stroke-width: {line_width}; fill: none;stroke-linejoin: round;stroke-linecap: round;",
            'd': "M" + " ".join(" ".join(str(coord) for coord in point) for point in point_list),
            'transform': get_correction_transform(svg),
            INKSTITCH_ATTRIBS['stroke_method']: 'manual_stitch'
        })
        destination.append(path)

    if path is not None and color_block.trim_after:
        if visual_commands:
            add_commands(Stroke(path), ["trim"])
        else:
            path.set(INKSTITCH_ATTRIBS['trim_after'], 'true')

    if path is not None and color_block.stop_after:
        if visual_commands:
            add_commands(Stroke(path), ["stop"])
        else:
            path.set(INKSTITCH_ATTRIBS['stop_after'], 'true')


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
