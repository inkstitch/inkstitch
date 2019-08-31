from simpletransform import (applyTransformToPoint, composeTransform,
                             invertTransform, parseTransform)

from ..commands import is_command
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.svg import find_elements
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_USE_TAG, XLINK_HREF
from .validation import ValidationTypeWarning


class ObjectTypeWarning(ValidationTypeWarning):
    name = _("Not a path")
    description = _("Ink/Stitch only knows how to work with paths.  It can't work with objects like text, rectangles, or circles.")
    steps_to_solve = [
        _('* Path > Object to Path (Shift+Ctrl+C)'),
        _('* For text also try the lettering tool:'),
        _('- Extensions > Ink/Stitch > Lettering')
    ]


class CloneSourceWarning(ValidationTypeWarning):
    name = _("Clone with invalid origin")
    description = _("Ink/Stitch only knows how to work with paths.  This object is a clone of an object which is not a path.")
    steps_to_solve = [
        _('* Select the source of this object and convert it to a path:'),
        _('- Path > Object to Path (Shift+Ctrl+C)'),
        _('* Alternatively unlink the clone and convert it to a path:'),
        _('- Edit > Clone > Unlink Clone (Shift+Alt+D)'),
        _('- Path > Object to Path (Shift+Ctrl+C)')
    ]


class ImageTypeWarning(ValidationTypeWarning):
    name = _("Image")
    description = _("Ink/Stitch only knows how to work with paths.  It can't work with objects like images.")
    steps_to_solve = [
        _('* Convert your image into a path: Path > Trace Bitmap... (Shift+Alt+B) '
          '(further steps might be required)'),
        _('* Alternatively redraw the image with the pen (P) or bezier (B) tool')
    ]


class InkscapeObjects(object):

    def __init__(self, svg, selection):
        self.svg = svg
        self.selection = selection

    def get_inkscape_objects(self):
        elements = []
        if self.selection:
            for node in self.selection:
                xpath = ".//svg:rect[@id='%(id)s']|.//svg:ellipse[@id='%(id)s']|.//svg:text[@id='%(id)s']|" \
                        ".//svg:use[@id='%(id)s' and not(starts-with(@xlink:href, '#inkstitch_'))]|.//svg:image[@id='%(id)s']" \
                        % dict(id=node)
                objects = find_elements(self.svg, xpath)

                if not objects:
                    xpath = ".//svg:g[@id='%(id)s']//svg:rect|.//svg:g[@id='%(id)s']//svg:ellipse|.//svg:g[@id='%(id)s']//svg:text|" \
                            ".//svg:g[@id='%(id)s']//svg:use[not(starts-with(@xlink:href, '#inkstitch_'))]|.//svg:g[@id='%(id)s']//svg:image" \
                            % dict(id=node)
                    objects = find_elements(self.svg, xpath)
                elements.extend(objects)
        else:
            xpath = ".//svg:rect|.//svg:ellipse|.//svg:text|.//svg:image|" \
                    ".//svg:use[not(starts-with(@xlink:href, '#inkstitch_'))]"
            elements.extend(find_elements(self.svg, xpath))

        return elements

    def validation_warnings(self):
        objects = self.get_inkscape_objects()
        for node in objects:
            # Skip warning on not visible shapes
            if 'style'in node.attrib.keys() and 'display:none' in node.get('style'):
                continue

            if "image" in node.tag:
                # image
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                applyTransformToPoint(correction_transform, point)
                yield ImageTypeWarning(point)
            elif node.get(XLINK_HREF):
                # clone
                if is_embroiderable_clone(node):
                    continue
                orig_node = get_clone_source(node)
                point = self.get_coordinates(orig_node)
                correction_transform = self.invert_correction_transform(node)
                node_transform = parseTransform(node.get('transform'))
                transform = composeTransform(correction_transform, node_transform)
                applyTransformToPoint(transform, point)
                yield CloneSourceWarning(point)
            else:
                # rect, ellipse
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                applyTransformToPoint(correction_transform, point)
                yield ObjectTypeWarning(point)

    def invert_correction_transform(self, element):
        return invertTransform(parseTransform(get_correction_transform(element)))

    def get_coordinates(self, node):
        if node.get('cx'):
            # ellipse
            x, y = ['cx', 'cy']
        elif node.get('x'):
            # rect, image
            x, y = ['x', 'y']

        point = [float(node.get(x)), float(node.get(y))]

        try:
            point = [(point[0]+(float(node.get('width'))/2)), (point[1]+(float(node.get('height'))/2))]
        except TypeError:
            pass

        return point


def is_clone(node):
    if node.tag == SVG_USE_TAG and not is_command(node):
        return True
    else:
        return False


def is_embroiderable_clone(node):
    if not is_clone(node):
        return False

    clone_source = get_clone_source(node)
    if clone_source.tag in EMBROIDERABLE_TAGS:
        return True


def get_clone_source(node):
    orig_id = node.get(XLINK_HREF)[1:]
    xpath = ".//*[@id='%s']" % (orig_id)
    source_node = find_elements(node, xpath)[0]
    return source_node


def add_path_to_clone(node):
    if not is_embroiderable_clone(node):
        return []

    orig_node = get_clone_source(node)

    path = "%s" % orig_node.get("d")
    node.set("d", path)

    style = "%s" % orig_node.get("style")
    node.set("style", style)

    return node
