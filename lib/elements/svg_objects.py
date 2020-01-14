from simpletransform import (applyTransformToPoint, composeTransform,
                             invertTransform, parseTransform)

from ..i18n import _
from ..svg import get_correction_transform
from ..svg.svg import find_elements
from ..svg.tags import SVG_IMAGE_TAG, SVG_TEXT_TAG
from .validation import ValidationTypeWarning


class TextTypeWarning(ValidationTypeWarning):
    name = _("Text")
    description = _("Ink/Stitch cannot work with objects like text.")
    steps_to_solve = [
        _('* Text: Create your own letters or try the lettering tool:'),
        _('- Extensions > Ink/Stitch > Lettering')
    ]


class ImageTypeWarning(ValidationTypeWarning):
    name = _("Image")
    description = _("Ink/Stitch can't work with objects like images.")
    steps_to_solve = [
        _('* Convert your image into a path: Path > Trace Bitmap... (Shift+Alt+B) '
          '(further steps might be required)'),
        _('* Alternatively redraw the image with the pen (P) or bezier (B) tool')
    ]


class SVGObjects(object):

    def __init__(self, svg, selection):
        self.svg = svg
        self.selection = selection

    def get_svg_objects(self):
        elements = []

        if self.selection:
            for node in self.selection:
                xpath = ".//svg:text[@id='%(id)s']|.//svg:image[@id='%(id)s']|" \
                        ".//svg:use[@id='%(id)s' and not(starts-with(@xlink:href, '#inkstitch_'))]" \
                        % dict(id=node)
                objects = find_elements(self.svg, xpath)

                if not objects:
                    xpath = ".//svg:g[@id='%(id)s']//svg:text|.//svg:g[@id='%(id)s']//svg:image|" \
                            ".//svg:g[@id='%(id)s']//svg:use[not(starts-with(@xlink:href, '#inkstitch_'))]" \
                            % dict(id=node)
                    objects = find_elements(self.svg, xpath)
                elements.extend(objects)
        else:
            xpath = ".//svg:text|.//svg:image|" \
                    ".//svg:use[not(starts-with(@xlink:href, '#inkstitch_'))]"
            elements.extend(find_elements(self.svg, xpath))

        return elements

    def validation_warnings(self):
        objects = self.get_svg_objects()
        for node in objects:
            # Skip warning on not visible shapes
            if 'style' in node.attrib.keys() and 'display:none' in node.get('style'):
                continue

            if node.tag == SVG_IMAGE_TAG:
                # image
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                applyTransformToPoint(correction_transform, point)
                yield ImageTypeWarning(point)
            elif node.tag == SVG_TEXT_TAG:
                # text
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                node_transform = parseTransform(node.get('transform'))
                transform = composeTransform(correction_transform, node_transform)
                applyTransformToPoint(transform, point)
                yield TextTypeWarning(point)

    def invert_correction_transform(self, element):
        return invertTransform(parseTransform(get_correction_transform(element)))

    def get_coordinates(self, node):
        point = [float(node.get('x')), float(node.get('y'))]

        try:
            point = [(point[0]+(float(node.get('width'))/2)), (point[1]+(float(node.get('height'))/2))]
        except TypeError:
            pass

        return point


def rect_to_path(node):
    x = float(node.get('x', '0'))
    y = float(node.get('y', '0'))
    width = float(node.get('width', '0'))
    height = float(node.get('height', '0'))
    rx = None
    ry = None

    # rounded corners
    # the following rules apply for radius calculations:
    #   if rx or ry is missing it has to take the value of the other one
    #   the radius cannot be bigger than half of the corresponding side
    #   (otherwise we receive an invalid path)
    if node.get('rx') or node.get('ry'):
        if node.get('rx'):
            rx = float(node.get('rx', '0'))
            ry = rx
        if node.get('ry'):
            ry = float(node.get('ry', '0'))
            if not ry:
                ry = rx

        rx = min(width/2, rx)
        ry = min(height/2, ry)

        path = 'M %(startx)f,%(y)f ' \
               'h %(width)f ' \
               'q %(rx)f,0 %(rx)f,%(ry)f ' \
               'v %(height)f ' \
               'q 0,%(ry)f -%(rx)f,%(ry)f ' \
               'h -%(width)f ' \
               'q -%(rx)f,0 -%(rx)f,-%(ry)f ' \
               'v -%(height)f ' \
               'q 0,-%(ry)f %(rx)f,-%(ry)f ' \
               'Z' \
               % dict(startx=x+rx, x=x, y=y, width=width-(2*rx), height=height-(2*ry), rx=rx, ry=ry)

    else:
        path = "M %f,%f H %f V %f H %f Z" % (x, y, width+x, height+y, x)

    return path


def ellipse_to_path(node):
    rx = float(node.get('rx', "0")) or float(node.get('r', "0"))
    ry = float(node.get('ry', "0")) or float(node.get('r', "0"))
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))

    path = 'M %(cxrx)f,%(cy)f ' \
           'A %(rx)f,%(ry)f 0 0 1 '\
           '%(cx)f,%(cyry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx_rx)f,%(cy)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx)f,%(cy_ry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cxrx)f,%(cy)f ' \
           'Z' \
           % dict(cxrx=cx+rx, cyry=cy+ry, cx_rx=cx-rx, cy_ry=cy-ry, rx=rx, ry=ry, cx=cx, cy=cy)

    return path


def circle_to_path(node):
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))
    r = float(node.get('r'))

    path = 'M %(xstart)f,%(cy)f ' \
           'a %(r)f,%(r)f 0 0 1 '\
           '-%(r)f,%(r)f %(r)f,%(r)f 0 0 1 ' \
           '-%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,%(r)f ' \
           'Z' \
           % dict(xstart=cx+r, cy=cy, r=r)

    return path
