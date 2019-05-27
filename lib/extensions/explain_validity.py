import re

from shapely.validation import explain_validity

import inkex

from ..commands import get_command_description
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL,
                        SODIPODI_INSENSITIVE, SVG_GROUP_TAG, SVG_PATH_TAG,
                        SVG_USE_TAG, XLINK_HREF)
from .base import InkstitchExtension
from .commands import CommandsExtension


class ExplainValidity(InkstitchExtension):
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
            inkex.errormsg(_("All selected shapes are valid!"))
        else:
            inkex.errormsg(_("Info: A pointer has been added to direct you to an invalid section of your path.\n\n" +
                             "It is possible, that an object contains more than one error, yet there will be only one pointer per object.\n" +
                             "Run this function again, when further errors occur.\n\n" +
                             "Remove the pointer by deleting the layer named 'Explain Validity' through the objects panel (Object -> Objects...)."))

    def insert_invalid_pointer(self, shape):
        invalid_point = explain_validity(shape)
        point_x, point_y = re.findall("\d+\.\d+", invalid_point)

        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validity_layer__']")

        if layer is None:
            layer = inkex.etree.Element(
                SVG_GROUP_TAG,
                {
                    'id': '__validity_layer__',
                    INKSCAPE_LABEL: _('Explain Validity'),
                    INKSCAPE_GROUPMODE: 'layer',
                    SODIPODI_INSENSITIVE: "true"
                })
            svg.append(layer)
            layer = svg.find(".//*[@id='__validity_layer__']")
            ignore_layer = IgnoreValidityLayer()
            ignore_layer.insert_layer_ignore_command(layer)

        correction_transform = get_correction_transform(layer, child=True)

        path = inkex.etree.Element(
            SVG_PATH_TAG,
            {
                "id": self.uniqueId("inkstitch__invalid_pointer__"),
                "d": "m %s,%s 2,10 h -4 l 2,-10" % (point_x, point_y),
                "style": "fill:#ff0000;fill-opacity:1;stroke:#ffffff;stroke-width:0.01;",
                INKSCAPE_LABEL: _('Invalid Pointer'),
                "transform": correction_transform
             }
             )
        layer.insert(0, path)


class IgnoreValidityLayer(CommandsExtension):
        COMMANDS = ['ignore_layer']

        def insert_layer_ignore_command(self, layer):
            command = 'ignore_layer'
            correction_transform = get_correction_transform(layer, child=True)

            inkex.etree.SubElement(layer, SVG_USE_TAG,
                                   {
                                       "id": self.uniqueId("use"),
                                       INKSCAPE_LABEL: _("Ink/Stitch Command") + ": %s" % get_command_description(command),
                                       XLINK_HREF: "#inkstitch_%s" % command,
                                       "height": "100%",
                                       "width": "100%",
                                       "x": "0",
                                       "y": "-10",
                                       "transform": correction_transform
                                   })
