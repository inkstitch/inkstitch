import logging

import inkex

from ..commands import add_layer_commands
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSCAPE_LABEL,
                        SODIPODI_ROLE, SVG_GROUP_TAG, SVG_PATH_TAG,
                        SVG_TEXT_TAG, SVG_TSPAN_TAG)
from .base import InkstitchExtension


class Troubleshoot(InkstitchExtension):

    def effect(self):
        if not self.get_elements():
            return

        logger = logging.getLogger('shapely.geos')
        level = logger.level
        logger.setLevel(logging.CRITICAL)

        errors = set()
        for element in self.elements:
            for error in element.validation_errors():
                errors.add(error)
                self.insert_invalid_pointer(error)

        logger.setLevel(level)

        if errors:
            self.add_descriptions(errors)
        else:
            inkex.errormsg(_("All selected shapes are valid!"))

    def insert_invalid_pointer(self, error):
        layer = self.get_or_create_validity_layer()
        correction_transform = get_correction_transform(layer)

        path = inkex.etree.Element(
            SVG_PATH_TAG,
            {
                "id": self.uniqueId("inkstitch__invalid_pointer__"),
                "d": "m %s,%s 4,20 h -8 l 4,-20" % (error.position.x, error.position.y),
                "style": "fill:#ff0000;stroke:#ffffff;stroke-width:0.2;",
                INKSCAPE_LABEL: _('Invalid Pointer'),
                "transform": correction_transform
            }
        )
        layer.insert(0, path)

        text = inkex.etree.Element(
            SVG_TEXT_TAG,
            {
                "x": str(error.position.x),
                "y": str(float(error.position.y) + 30),
                "transform": correction_transform,
                "style": "fill:#ff0000;troke:#ffffff;stroke-width:0.2;font-size:8px;text-align:center;text-anchor:middle"
            }
        )
        layer.append(text)

        tspan = inkex.etree.Element(SVG_TSPAN_TAG)
        tspan.text = error.name
        text.append(tspan)

    def get_or_create_validity_layer(self):
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validity_layer__']")

        if layer is None:
            layer = inkex.etree.Element(
                SVG_GROUP_TAG,
                {
                    'id': '__validity_layer__',
                    INKSCAPE_LABEL: _('Troubleshoot'),
                    INKSCAPE_GROUPMODE: 'layer',
                })
            svg.append(layer)

            add_layer_commands(layer, ["ignore_layer"])

        return layer

    def add_descriptions(self, errors):
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validity_layer__']")

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
            [_("Troubleshoot"), "font-weight: bold; font-size: 6px;"],
            ["", ""]
        ]

        for error in errors:
            text.append([error.name, "font-weight: bold;"])
            text.append(["* " + error.description, "font-size: 4px;"])
            text.append(["", ""])

        text += [
            ["", ""],
            [_("It is possible, that one object contains more than one error,"), "font-style: italic; font-size: 3px;"],
            [_("yet there will be only one pointer per object."), "font-style: italic; font-size: 3px;"],
            [_("Run this function again, when further errors occur."), "font-style: italic; font-size: 3px;"],
            ["", ""],
            [_('Remove pointers by deleting the layer named "Troubleshoot"'), "font-style: italic; font-size: 3px;"],
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
