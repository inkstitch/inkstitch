import inkex

from ..i18n import _
from ..utils import cache

# modern versions of Inkscape use 96 pixels per inch as per the CSS standard
PIXELS_PER_MM = 96 / 25.4


def parse_length_with_units(str):
    value, unit = inkex.units.parse_unit(str)
    if not unit:
        raise ValueError(_("parseLengthWithUnits: unknown unit %s") % str)
    return value, unit

    """
    '''
    Parse an SVG value which may or may not have units attached
    This version is greatly simplified in that it only allows: no units,
    units of px, mm, and %.  Everything else, it returns None for.
    There is a more general routine to consider in scour.py if more
    generality is ever needed.
    '''

    # cribbed from inkscape-silhouette

    u = 'px'
    s = str.strip()
    if s[-2:] == 'px':
        s = s[:-2]
    elif s[-2:] == 'mm':
        u = 'mm'
        s = s[:-2]
    elif s[-2:] == 'pt':
        u = 'pt'
        s = s[:-2]
    elif s[-2:] == 'pc':
        u = 'pc'
        s = s[:-2]
    elif s[-2:] == 'cm':
        u = 'cm'
        s = s[:-2]
    elif s[-2:] == 'in':
        u = 'in'
        s = s[:-2]
    elif s[-1:] == '%':
        u = '%'
        s = s[:-1]
    try:
        v = float(s)
    except BaseException:
        raise ValueError(_("parseLengthWithUnits: unknown unit %s") % s)

    return v, u
    """


def convert_length(length):
    value, units = parse_length_with_units(length)

    return inkex.units.convert_unit(str(value) + units, 'px')

    """
    if not units or units == "px":
        return value

    if units == 'pt':
        value /= 72
        units = 'in'

    if units == 'pc':
        value /= 6
        units = 'in'

    if units == 'cm':
        value *= 10
        units = 'mm'

    if units == 'mm':
        value /= 25.4
        units = 'in'

    if units == 'in':
        # modern versions of Inkscape use CSS's 96 pixels per inch.  When you
        # open an old document, inkscape will add a viewbox for you.
        return value * 96

    raise ValueError(_("Unknown unit: %s") % units)
    """


@cache
def get_viewbox(svg):
    viewbox = svg.get('viewBox')
    if viewbox is None:
        viewbox = "0 0 0 0"
    return viewbox.strip().replace(',', ' ').split()


@cache
def get_doc_size(svg):
    width = svg.get('width')
    height = svg.get('height')

    if width == "100%" and height == "100%":
        # Some SVG editors set width and height to "100%".  I can't find any
        # solid documentation on how one is supposed to interpret that, so
        # just ignore it and use the viewBox.  That seems to have the intended
        # result anyway.

        width = None
        height = None

    if width is None or height is None:
        # fall back to the dimensions from the viewBox
        viewbox = get_viewbox(svg)
        width = viewbox[2]
        height = viewbox[3]

    doc_width = convert_length(width)
    doc_height = convert_length(height)

    return doc_width, doc_height


@cache
def get_viewbox_transform(node):
    # somewhat cribbed from inkscape-silhouette
    doc_width, doc_height = get_doc_size(node)

    viewbox = get_viewbox(node)

    dx = -float(viewbox[0])
    dy = -float(viewbox[1])
    transform = inkex.transforms.Transform("translate(%f, %f)" % (dx, dy))

    try:
        sx = doc_width / float(viewbox[2])
        sy = doc_height / float(viewbox[3])

        # preserve aspect ratio
        aspect_ratio = node.get('preserveAspectRatio', 'xMidYMid meet')
        if aspect_ratio != 'none':
            sx = sy = max(sx, sy) if 'slice' in aspect_ratio else min(sx, sy)

        scale_transform = inkex.transforms.Transform("scale(%f, %f)" % (sx, sy))
        transform = transform * scale_transform
    except ZeroDivisionError:
        pass

    return transform
