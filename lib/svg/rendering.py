import math

import inkex
from lxml import etree
from math import pi

from ..i18n import _
from ..utils import Point, cache
from .tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL, INKSTITCH_ATTRIBS,
                   SVG_DEFS_TAG, SVG_GROUP_TAG, SVG_PATH_TAG)
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
# proceeds counter-clockwise.and contains a placeholder (%s) for the stitch
# length.
#
# It contains two invisible "whiskers" of zero width that go above and below
# to ensure that the SVG renderer allocates a large enough canvas area when
# computing the gaussian blur steps.  Otherwise, we'd have to expand the
# width and height attributes of the <filter> tag to add more buffer space.
# The width and height are specified in multiples of the bounding box
# size, It's the bounding box aligned with the global SVG canvas's axes, not
# the axes of the stitch itself.  That means that having a big enough value
# to add enough padding on the long sides of the stitch would waste a ton
# of space on the short sides and significantly slow down rendering.
stitch_path = "M0,0c0.4,0,0.4,0.3,0.4,0.6c0,0.3,-0.1,0.6,-0.4,0.6v0.2,-0.2h-%sc-0.4,0,-0.4,-0.3,-0.4,-0.6c0,-0.3,0.1,-0.6,0.4,-0.6v-0.2,0.2z"

# This filter makes the above stitch path look like a real stitch with lighting.
realistic_filter = """
    <filter
       style="color-interpolation-filters:sRGB"
       id="realistic-stitch-filter"
       x="-0.1"
       width="1.2"
       y="-0.1"
       height="1.2">
      <feGaussianBlur
         stdDeviation="1.5"
         id="feGaussianBlur1542-6"
         in="SourceAlpha" />
      <feComponentTransfer
         id="feComponentTransfer1544-7"
         result="result1">
        <feFuncR
           id="feFuncR1546-5"
           type="identity" />
        <feFuncG
           id="feFuncG1548-3"
           type="identity" />
        <feFuncB
           id="feFuncB1550-5"
           type="identity"
           slope="4.5300000000000002" />
        <feFuncA
           id="feFuncA1552-6"
           type="gamma"
           slope="0.14999999999999999"
           intercept="0"
           amplitude="3.1299999999999999"
           offset="-0.33000000000000002" />
      </feComponentTransfer>
      <feComposite
         in2="SourceAlpha"
         id="feComposite1558-2"
         operator="in" />
      <feGaussianBlur
         stdDeviation="0.089999999999999997"
         id="feGaussianBlur1969" />
      <feMorphology
         id="feMorphology1971"
         operator="dilate"
         radius="0.10000000000000001" />
      <feSpecularLighting
         id="feSpecularLighting1973"
         result="result2"
         specularConstant="0.70899999"
         surfaceScale="30">
        <fePointLight
           id="fePointLight1975"
           z="10" />
      </feSpecularLighting>
      <feGaussianBlur
         stdDeviation="0.040000000000000001"
         id="feGaussianBlur1979" />
      <feComposite
         in2="SourceGraphic"
         id="feComposite1977"
         operator="arithmetic"
         k2="1"
         k3="1"
         result="result3"
         k1="0"
         k4="0" />
      <feComposite
         in2="SourceAlpha"
         id="feComposite1981"
         operator="in" />
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

    # create the path by filling in the length in the template
    path = inkex.Path(stitch_path % stitch_length).to_arrays()

    # rotate the path to match the stitch
    rotation_center_x = -stitch_length / 2.0
    rotation_center_y = stitch_height / 2.0

    path = inkex.Path(path).rotate(stitch_angle, (rotation_center_x, rotation_center_y))

    # move the path to the location of the stitch
    path = inkex.Path(path).translate(stitch_center.x - rotation_center_x, stitch_center.y - rotation_center_y)

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
            destination.append(etree.Element(SVG_PATH_TAG, {
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

        color = color_block.color.visible_on_white.to_hex_str()

        path = etree.Element(SVG_PATH_TAG, {
            'style': "stroke: %s; stroke-width: 0.4; fill: none;" % color,
            'd': "M" + " ".join(" ".join(str(coord) for coord in point) for point in point_list),
            'transform': get_correction_transform(svg),
            INKSTITCH_ATTRIBS['manual_stitch']: 'true'
        })
        destination.append(path)

    if path is not None and visual_commands:
        if color_block.trim_after:
            add_commands(Stroke(path), ["trim"])

        if color_block.stop_after:
            add_commands(Stroke(path), ["stop"])


def render_stitch_plan(svg, stitch_plan, realistic=False, visual_commands=True):
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    if layer is None:
        layer = etree.Element(SVG_GROUP_TAG,
                              {'id': '__inkstitch_stitch_plan__',
                               INKSCAPE_LABEL: _('Stitch Plan'),
                               INKSCAPE_GROUPMODE: 'layer'})
    else:
        # delete old stitch plan
        del layer[:]

        # make sure the layer is visible
        layer.set('style', 'display:inline')

    svg.append(layer)

    for i, color_block in enumerate(stitch_plan):
        group = etree.SubElement(layer,
                                 SVG_GROUP_TAG,
                                 {'id': '__color_block_%d__' % i,
                                  INKSCAPE_LABEL: "color block %d" % (i + 1)})
        if realistic:
            color_block_to_realistic_stitches(color_block, svg, group)
        else:
            color_block_to_paths(color_block, svg, group, visual_commands)

    if realistic:
        defs = svg.find(SVG_DEFS_TAG)

        if defs is None:
            defs = etree.SubElement(svg, SVG_DEFS_TAG)

        defs.append(etree.fromstring(realistic_filter))
