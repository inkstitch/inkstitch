import re

from shapely.validation import explain_validity

import inkex

from ..commands import get_command_description
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL,
                        SODIPODI_INSENSITIVE, SODIPODI_ROLE, SVG_GROUP_TAG,
                        SVG_PATH_TAG, SVG_TEXT_TAG, SVG_TSPAN_TAG, SVG_USE_TAG,
                        XLINK_HREF)
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

    def insert_invalid_pointer(self, shape):
        layer = self.get_or_create_validity_layer()
        correction_transform = get_correction_transform(layer, child=True)

        shapely_msg = explain_validity(shape)
        message, point_x, point_y = re.findall(r".+?(?=\[)|\d+\.\d+", shapely_msg)

        path = inkex.etree.Element(
            SVG_PATH_TAG,
            {
                "id": self.uniqueId("inkstitch__invalid_pointer__"),
                "d": "m %s,%s 4,20 h -8 l 4,-20" % (point_x, point_y),
                "style": "fill:#ff0000;stroke:#ffffff;stroke-width:0.2;",
                INKSCAPE_LABEL: _('Invalid Pointer'),
                "transform": correction_transform
             }
             )
        layer.insert(0, path)

        text = inkex.etree.Element(
            SVG_TEXT_TAG,
            {
                "x": point_x,
                "y": str(float(point_y) + 30),
                "transform": correction_transform,
                "style": "fill:#ff0000;troke:#ffffff;stroke-width:0.2;font-size:8px;text-align:center;text-anchor:middle"
            }
            )
        layer.append(text)

        tspan = inkex.etree.Element(SVG_TSPAN_TAG)
        if message == "Self-intersection":
            tspan.text = _("Self-intersection")
        elif message == "Hole lies outside shell":
            tspan.text = _("Gap")
        else:
            # different error (message not translatable)
            tspan.text = message
        text.append(tspan)

    def get_or_create_validity_layer(self):
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

            text_x = str(self.unittouu(svg.get('width')) + 5)

            text_container = inkex.etree.Element(
                SVG_TEXT_TAG,
                {
                    "x": text_x,
                    "y": str(5),
                    "style": "fill:#000000;font-size:5px;line-height:1;"
                }
                )
            layer.append(text_container)

            text = [
                        [_("Explain Validity"), "font-weight: bold; font-size: 6px;"],
                        ["", ""],
                        [_("Self-Intersection"), "font-weight: bold;"],
                        [_("* Path > Union (Ctrl++)"), "font-size: 4px;"],
                        [_("* Path > Break apart (Shift+Ctrl+K)"), "font-size: 4px;"],
                        ["", ""],
                        [_("Gap"), "font-weight: bold;"],
                        [_("* Path > Break apart (Shift+Ctrl+K)"), "font-size: 4px;"],
                        [_("* (Optional) Recombine shapes with holes (Ctrl+K)."), "font-size: 4px;"],
                        ["", ""],
                        [_("It is possible, that one object contains more than one error,"), "font-style: italic; font-size: 3px;"],
                        [_("yet there will be only one pointer per object."), "font-style: italic; font-size: 3px;"],
                        [_("Run this function again, when further errors occur."), "font-style: italic; font-size: 3px;"],
                        ["", ""],
                        [_('Remove pointers by deleting the layer named "Explain Validity"'), "font-style: italic; font-size: 3px;"],
                        [_("through the objects panel (Object -> Objects...)."), "font-style: italic; font-size: 3px;"]
                ]

            for text_line in text:
                tspan = inkex.etree.Element(
                    SVG_TSPAN_TAG,
                    {
                        SODIPODI_ROLE: "line",
                        "style": text_line[1]
                    }
                    )
                tspan.text = text_line[0]
                text_container.append(tspan)

        return layer


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
