from cubicsuperpath import parsePath
from simpletransform import (applyTransformToPoint, composeTransform,
                             invertTransform, parseTransform, roughBBox)

from ..i18n import _
from ..svg import get_correction_transform
from ..svg.svg import find_elements
from ..svg.tags import XLINK_HREF
from .validation import ValidationTypeWarning


class ObjectTypeWarning(ValidationTypeWarning):
    name = _("Not a path")
    description = _("Ink/Stitch only knows how to work with paths.  It can't work with objects like text, rectangles, or circles.")
    steps_to_solve = [
        _('* Path > Object to Path (Shift+Ctrl+C)'),
        _('* For text also try the lettering tool: Extensions > Ink/Stitch > Lettering')
    ]


class CloneTypeWarning(ValidationTypeWarning):
    name = _("Clone")
    description = _("Ink/Stitch only knows how to work with paths.  It can't work with objects like clones.")
    steps_to_solve = [
        _('* Edit > Clone > Unlink Clone (Shift+Alt+D)'),
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
                        ".//svg:use[@id='%(id)s' and not(starts-with(@xlink:href, '#inkstitch_')]|.//svg:image[@id='%(id)s']" \
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
                # Image Object
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                applyTransformToPoint(correction_transform, point)
                yield ImageTypeWarning(point)
            elif node.get(XLINK_HREF):
                # Clone
                eid = node.get(XLINK_HREF)[1:]
                xpath = ".//*[@id='%s']" % (eid)
                orig_node = find_elements(self.svg, xpath)[0]
                point = self.get_coordinates(orig_node)
                correction_transform = self.invert_correction_transform(node)
                node_transform = parseTransform(node.get('transform'))
                transform = composeTransform(correction_transform, node_transform)
                applyTransformToPoint(transform, point)
                yield CloneTypeWarning(point)
            else:
                # Rect, Ellipse
                point = self.get_coordinates(node)
                correction_transform = self.invert_correction_transform(node)
                applyTransformToPoint(correction_transform, point)
                yield ObjectTypeWarning(point)

    def invert_correction_transform(self, element):
        return invertTransform(parseTransform(get_correction_transform(element)))

    def get_coordinates(self, node):
        point = [0, 0]
        if node.get('cx'):
            # Ellipse
            point = [float(node.get('cx')), float(node.get('cy'))]
        elif node.get('x'):
            # Rect, image
            point = [float(node.get('x')), float(node.get('y'))]
        else:
            # Origin of clone is a path object
            xmin, xMax, ymin, yMax = roughBBox(parsePath(node.get('d')))
            point = [xmin+((xMax-xmin)/2), ymin+((yMax-ymin)/2)]

        if node.get('width'):
            point = [(point[0]+(float(node.get('width'))/2)), (point[1]+(float(node.get('height'))/2))]

        return point
