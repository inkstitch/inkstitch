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
# 1.216 pixels = 0.32mm
stitch_height = 1.216

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

# The specific extent of the whiskers (0.45 parallel to the stitch, 0.1 perpendicular)
# was found by experimentation. It seems to work without artifacting.
stitch_path = (
    "M0,0"  # Start point
    "l0.45,-0.1,-0.45,0.1"  # Bottom-right whisker
    "c0.4,0,0.4,0.3,0.4,0.6c0,0.3,-0.1,0.6,-0.4,0.6"  # Right endcap
    "l0.45,0.1,-0.45,-0.1"  # Top-right whisker
    "h-%s"  # Stitch length
    "l-0.45,0.1,0.45,-0.1"  # Top-left whisker
    "c-0.4,0,-0.4,-0.3,-0.4,-0.6c0,-0.3,0.1,-0.6,0.4,-0.6"  # Left endcap
    "l-0.45,-0.1,0.45,0.1"  # Bottom-left whisker
    "z")  # return to start

# The filter needs the xmlns:inkscape declaration, or Inkscape will display a parse error
# "Namespace prefix inkscape for auto-region on filter is not defined"
# Even when the document itself has the namespace, go figure.
realistic_filter = """
    <filter
       style="color-interpolation-filters:sRGB"
       id="realistic-stitch-filter"
       x="0"
       width="1"
       y="0"
       height="1"
       inkscape:auto-region="false"
       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
      <feGaussianBlur
         edgeMode="none"
         stdDeviation="0.9"
         id="feGaussianBlur1542-6"
         in="SourceAlpha" />
      <feSpecularLighting
         id="feSpecularLighting1973"
         result="result2"
         surfaceScale="1.5"
         specularConstant="0.78"
         specularExponent="2.5">
        <feDistantLight
           id="feDistantLight1975"
           azimuth="-125"
           elevation="20" />
      </feSpecularLighting>
      <feComposite
         in2="SourceAlpha"
         id="feComposite1981"
         operator="atop" />
      <feComposite
         in2="SourceGraphic"
         id="feComposite1982"
         operator="arithmetic"
         k2="0.8"
         k3="1.2"
         result="result3"
         k1="0"
         k4="0" />
    </filter>
"""


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


def color_block_to_point_lists(color_block):
    point_lists = [[]]

    for stitch in color_block:
        if stitch.trim:
            if point_lists[-1]:
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


def color_block_to_realistic_stitches(color_block, svg, destination):
    for point_list in color_block_to_point_lists(color_block):
        color = color_block.color.visible_on_white.darker.to_hex_str()
        start = point_list[0]
        for point in point_list[1:]:
            destination.append(inkex.PathElement(attrib={
                'style': "fill: %s; stroke: none; filter: url(#realistic-stitch-filter);" % color,
                'd': realistic_stitch(start, point),
                'transform': get_correction_transform(svg)
            }))
            start = point


def color_block_to_paths(color_block, svg, destination, visual_commands):
    # If we try to import these above, we get into a mess of circular
    # imports.
    from ..commands import add_commands
    from ..elements.stroke import Stroke

    # We could emit just a single path with one subpath per point list, but
    # emitting multiple paths makes it easier for the user to manipulate them.
    first = True
    path = None
    for point_list in color_block_to_point_lists(color_block):
        if first:
            first = False
        elif visual_commands:
            add_commands(Stroke(destination[-1]), ["trim"])
        else:
            path.set(INKSTITCH_ATTRIBS['trim_after'], 'true')

        color = color_block.color.visible_on_white.to_hex_str()
        path = inkex.PathElement(attrib={
            'id': svg.get_unique_id("object"),
            'style': "stroke: %s; stroke-width: 0.4; fill: none;" % color,
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


def render_stitch_plan(svg, stitch_plan, realistic=False, visual_commands=True):
    layer = svg.findone(".//*[@id='__inkstitch_stitch_plan__']")
    if layer is None:
        layer = inkex.Group(attrib={
            'id': '__inkstitch_stitch_plan__',
            INKSCAPE_LABEL: _('Stitch Plan'),
            INKSCAPE_GROUPMODE: 'layer'
        })
    else:
        # delete old stitch plan
        del layer[:]

        # make sure the layer is visible
        layer.set('style', 'display:inline')

    svg.append(layer)

    for i, color_block in enumerate(stitch_plan):
        group = inkex.Group(attrib={
            'id': '__color_block_%d__' % i,
            INKSCAPE_LABEL: "color block %d" % (i + 1)
        })
        layer.append(group)
        if realistic:
            color_block_to_realistic_stitches(color_block, svg, group)
        else:
            color_block_to_paths(color_block, svg, group, visual_commands)

    if realistic:
        # Remove filter from defs, if any
        filter: inkex.BaseElement = svg.defs.findone("//*[@id='realistic-stitch-filter']")
        if filter is not None:
            svg.defs.remove(filter)

        filter_document = inkex.load_svg(realistic_filter)
        svg.defs.append(filter_document.getroot())
