import simplepath
import math

from .units import PIXELS_PER_MM
from ..utils import Point

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
