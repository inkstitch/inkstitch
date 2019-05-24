import sys
import re
import inkex
from shapely.validation import explain_validity
from .base import InkstitchExtension
from ..svg.tags import SVG_GROUP_TAG, INKSCAPE_LABEL, INKSCAPE_GROUPMODE, SVG_PATH_TAG


class ExplainValidity(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

    def effect(self):
        if not self.get_elements():
            return

        valid_shapes = True
        for element in self.elements:
            shape = element.shape
            if not shape.is_valid:
                valid_shapes = False
                self.insert_invalid_pointer(shape)

        if valid_shapes is True:
            print >> sys.stderr, _('All selected shapes are valid!')
        else:
            pointer_info = _('Info: A pointer has been added to direct you to an invalid section of your path.')
            pointer_info += '\n\n'
            pointer_info += _('It is possible, that an object contains more than one error, yet there will be only one pointer per object. ')
            pointer_info += _('You might want to run this function again, when further errors occur.')
            pointer_info += '\n\n'
            pointer_info += _('Remove the pointer by deleting the layer named "Explain Validity".')
            print >> sys.stderr, pointer_info

    def insert_invalid_pointer(self, shape):
        invalid_point = explain_validity(shape)
        point = re.findall("\d+\.\d+", invalid_point)
        point_x, point_y = [self.unittouu(coord+'px') for coord in point]

        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validity_layer__']")

        if layer is None:
            layer = inkex.etree.Element(
                SVG_GROUP_TAG,
                {
                    'id': '__validity_layer__',
                    INKSCAPE_LABEL: _('Explain Validity'),
                    INKSCAPE_GROUPMODE: 'layer'
                })
            svg.append(layer)
            layer = svg.find(".//*[@id='__validity_layer__']")

        path = inkex.etree.Element(
            SVG_PATH_TAG,
            {
                "id": self.uniqueId("inkstitch__invalid_pointer__"),
                "d": "m %s,%s 2,10 h -4 l 2,-10" % (point_x, point_y),
                "style": "fill:#ff0000;fill-opacity:1;stroke:#ffffff;stroke-width:0.01;",
                INKSCAPE_LABEL: _('Invalid Pointer')
             }
             )
        layer.insert(0, path)
