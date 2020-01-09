from simpletransform import (applyTransformToPoint, composeTransform,
                             invertTransform, parseTransform)

from ..commands import is_command
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.svg import find_elements
from ..svg.tags import SVG_IMAGE_TAG, SVG_TEXT_TAG, SVG_USE_TAG, XLINK_HREF
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


class CloneSourceWarning(ValidationTypeWarning):
    name = _("Clone with invalid origin")
    description = _("Ink/Stitch works best with paths.  This object is a clone of an object which is not embroiderable.")
    steps_to_solve = [
        _('* Select the source of this object and convert it to a path:'),
        _('- Path > Object to Path (Shift+Ctrl+C)'),
        _('* Alternatively unlink the clone and convert it to a path:'),
        _('- Edit > Clone > Unlink Clone (Shift+Alt+D)'),
        _('- Path > Object to Path (Shift+Ctrl+C)')
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


def is_clone(node):
    if not node.tag == SVG_USE_TAG or (node.tag == SVG_USE_TAG and is_command(node)):
        return False

    elif node.tag == SVG_USE_TAG and node.get(XLINK_HREF):
        return True


def get_clone_source(node, id=None):
    if not id:
        orig_id = node.get(XLINK_HREF)[1:]
    else:
        orig_id = id
    xpath = ".//*[@id='%s']" % (orig_id)
    source_node = find_elements(node, xpath)[0]
    return source_node
