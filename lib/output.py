import pyembroidery
import inkex
import simpletransform
import shapely.geometry as shgeo

from .utils import Point
from .svg import PIXELS_PER_MM, get_doc_size, get_viewbox_transform


def add_thread(pattern, thread):
    """Add a thread to a pattern and return the thread's index"""

    libembroidery.embPattern_addThread(pattern, thread)

    return libembroidery.embThreadList_count(pattern.threadList) - 1

def get_command(stitch):
    if stitch.jump:
        return pyembroidery.JUMP
    elif stitch.trim:
        return pyembroidery.TRIM
    elif stitch.color_change:
        return pyembroidery.COLOR_CHANGE
    elif stitch.stop:
        return pyembroidery.STOP
    else:
        return pyembroidery.NEEDLE_AT

def _string_to_floats(string):
    floats = string.split(',')
    return [float(num) for num in floats]


def get_origin(svg):
    # The user can specify the embroidery origin by defining two guides
    # named "embroidery origin" that intersect.

    namedview = svg.find(inkex.addNS('namedview', 'sodipodi'))
    all_guides = namedview.findall(inkex.addNS('guide', 'sodipodi'))
    label_attribute = inkex.addNS('label', 'inkscape')
    guides = [guide for guide in all_guides
                    if guide.get(label_attribute, "").startswith("embroidery origin")]

    # document size used below
    doc_size = list(get_doc_size(svg))

    # convert the size from viewbox-relative to real-world pixels
    viewbox_transform = get_viewbox_transform(svg)
    simpletransform.applyTransformToPoint(simpletransform.invertTransform(viewbox_transform), doc_size)

    default = [doc_size[0] / 2.0, doc_size[1] / 2.0]
    simpletransform.applyTransformToPoint(viewbox_transform, default)
    default = Point(*default)

    if len(guides) < 2:
        return default

    # Find out where the guides intersect.  Only pay attention to the first two.
    guides = guides[:2]

    lines = []
    for guide in guides:
        # inkscape's Y axis is reversed from SVG's, and the guide is in inkscape coordinates
        position = Point(*_string_to_floats(guide.get('position')))
        position.y = doc_size[1] - position.y


        # This one baffles me.  I think inkscape might have gotten the order of
        # their vector wrong?
        parts = _string_to_floats(guide.get('orientation'))
        direction = Point(parts[1], parts[0])

        # We have a theoretically infinite line defined by a point on the line
        # and a vector direction.  Shapely can only deal in concrete line
        # segments, so we'll pick points really far in either direction on the
        # line and call it good enough.
        lines.append(shgeo.LineString((position + 100000 * direction, position - 100000 * direction)))

    intersection = lines[0].intersection(lines[1])

    if isinstance(intersection, shgeo.Point):
        origin = [intersection.x, intersection.y]
        simpletransform.applyTransformToPoint(viewbox_transform, origin)
        return Point(*origin)
    else:
        # Either the two guides are the same line, or they're parallel.
        return default


def write_embroidery_file(file_path, stitch_plan, svg):
    origin = get_origin(svg)

    pattern = pyembroidery.EmbPattern()

    for color_block in stitch_plan:
        pattern.add_thread(color_block.color.pyembroidery_thread)

        for stitch in color_block:
            command = get_command(stitch)
            pattern.add_stitch_absolute(command, stitch.x, stitch.y)

    pattern.add_stitch_absolute(pyembroidery.END, stitch.x, stitch.y)

    # convert from pixels to millimeters
    # also multiply by 10 to get tenths of a millimeter as required by pyembroidery
    scale = 10 / PIXELS_PER_MM

    settings =  {
                    # correct for the origin
                    "translate": -origin,

                    # convert from pixels to millimeters
                    # also multiply by 10 to get tenths of a millimeter as required by pyembroidery
                    "scale": (scale, scale)
                }

    pyembroidery.write(pattern, file_path, settings)
