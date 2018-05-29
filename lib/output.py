import libembroidery
import inkex
import simpletransform
import shapely.geometry as shgeo

from .utils import Point
from .svg import PIXELS_PER_MM, get_doc_size, get_viewbox_transform


def make_thread(color):
    thread = libembroidery.EmbThread()
    thread.color = libembroidery.embColor_make(*color.rgb)

    thread.description = color.name
    thread.catalogNumber = ""

    return thread

def add_thread(pattern, thread):
    """Add a thread to a pattern and return the thread's index"""

    libembroidery.embPattern_addThread(pattern, thread)

    return libembroidery.embThreadList_count(pattern.threadList) - 1

def get_flags(stitch):
    flags = 0

    if stitch.jump:
        flags |= libembroidery.JUMP

    if stitch.trim:
        flags |= libembroidery.TRIM

    if stitch.color_change:
        flags |= libembroidery.STOP

    return flags


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

    pattern = libembroidery.embPattern_create()

    for color_block in stitch_plan:
        add_thread(pattern, make_thread(color_block.color))

        for stitch in color_block:
            if stitch.stop:
                # This is the start of the extra color block added by the
                # "STOP after" handler (see stitch_plan/stop.py).  Assign it
                # the same color.
                add_thread(pattern, make_thread(color_block.color))

            flags = get_flags(stitch)
            libembroidery.embPattern_addStitchAbs(pattern, stitch.x - origin.x, stitch.y - origin.y, flags, 1)

    libembroidery.embPattern_addStitchAbs(pattern, stitch.x - origin.x, stitch.y - origin.y, libembroidery.END, 1)

    # convert from pixels to millimeters
    libembroidery.embPattern_scale(pattern, 1/PIXELS_PER_MM)

    # SVG and embroidery disagree on the direction of the Y axis
    libembroidery.embPattern_flipVertical(pattern)

    libembroidery.embPattern_write(pattern, file_path)
