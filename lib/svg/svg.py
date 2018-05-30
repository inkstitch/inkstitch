import math
import simpletransform, simplestyle, simplepath, inkex

from .units import get_viewbox_transform, PIXELS_PER_MM
from .tags import SVG_GROUP_TAG, INKSCAPE_LABEL, INKSCAPE_GROUPMODE, SVG_PATH_TAG, SVG_DEFS_TAG
from ..i18n import _
from ..utils import cache, Point


# The stitch vector path looks like this:
#  _______
# (_______)
#
# It's 0.32mm high, which is the approximate thickness of common machine embroidery threads.

# 1.216 pixels = 0.32mm
stitch_height = 1.216

# This vector path starts at the origin and contains a placeholder (%s) for the stitch length.
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
    stitch_center = (end + start) / 2.0
    stitch_direction = (end - start)
    stitch_angle = math.atan2(stitch_direction.y, stitch_direction.x)

    stitch_length = max(0, stitch_length - 0.2 * PIXELS_PER_MM)

    # create the path by filling in the length in the template
    path = simplepath.parsePath(stitch_path % stitch_length)

    # rotate the path to match the stitch
    rotation_center_x = -stitch_length / 2.0
    rotation_center_y = stitch_height / 2.0
    simplepath.rotatePath(path, stitch_angle, cx=rotation_center_x, cy=rotation_center_y)

    # move the path to the location of the stitch
    simplepath.translatePath(path, stitch_center.x - rotation_center_x, stitch_center.y - rotation_center_y)

    return simplepath.formatPath(path)


def color_block_to_point_lists(color_block):
    point_lists = [[]]

    for stitch in color_block:
         if stitch.trim:
              if point_lists[-1]:
                  point_lists.append([])
                  continue

         if not stitch.jump and not stitch.color_change:
              point_lists[-1].append(stitch.as_tuple())

    return point_lists


@cache
def get_correction_transform(svg):
    transform = get_viewbox_transform(svg)

    # we need to correct for the viewbox
    transform = simpletransform.invertTransform(transform)
    transform = simpletransform.formatTransform(transform)

    return transform


def color_block_to_paths(color_block, svg):
    paths = []
    # We could emit just a single path with one subpath per point list, but
    # emitting multiple paths makes it easier for the user to manipulate them.
    for point_list in color_block_to_point_lists(color_block):
        color = color_block.color.visible_on_white.darker.to_hex_str()
        start = point_list[0]
        for point in point_list[1:]:
            paths.append(inkex.etree.Element(
                SVG_PATH_TAG,
                {'style': simplestyle.formatStyle(
                    {
                        'fill': color,
                        'stroke': 'none',
                        'filter': 'url(#realistic-stitch-filter)'
                    }),
                'd': realistic_stitch(start, point),
                'transform': get_correction_transform(svg)
                }))
            start = point

    return paths


def render_stitch_plan(svg, stitch_plan):
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    if layer is None:
        layer = inkex.etree.Element(SVG_GROUP_TAG,
                                    {'id': '__inkstitch_stitch_plan__',
                                     INKSCAPE_LABEL: _('Stitch Plan'),
                                     INKSCAPE_GROUPMODE: 'layer'})
    else:
        # delete old stitch plan
        del layer[:]

        # make sure the layer is visible
        layer.set('style', 'display:inline')

    for i, color_block in enumerate(stitch_plan):
        group = inkex.etree.SubElement(layer,
                                       SVG_GROUP_TAG,
                                       {'id': '__color_block_%d__' % i,
                                        INKSCAPE_LABEL: "color block %d" % (i + 1)})
        group.extend(color_block_to_paths(color_block, svg))

    defs = svg.find(SVG_DEFS_TAG)
    defs.append(inkex.etree.fromstring(realistic_filter))

    svg.append(layer)
