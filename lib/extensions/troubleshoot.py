from itertools import chain
import textwrap

import inkex

from ..commands import add_layer_commands
from ..elements.validation import ValidationWarning, ValidationError
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

        self.create_troubleshoot_layer()

        problem_types = set()
        for element in self.elements:
            for problem in chain(element.validation_errors(), element.validation_warnings()):
                problem_types.add(type(problem))
                self.insert_pointer(problem)

        if problem_types:
            self.add_descriptions(problem_types)
        else:
            inkex.errormsg(_("All selected shapes are valid!"))

    def insert_pointer(self, problem):
        correction_transform = get_correction_transform(self.troubleshoot_layer)

        if isinstance(problem, ValidationWarning):
            fill_color = "#ffdd00"
            layer = self.warning_group
        elif isinstance(problem, ValidationError):
            fill_color = "#ff0000"
            layer = self.error_group

        pointer_style = "stroke:#ffffff;stroke-width:0.2;fill:%s;" % (fill_color)
        text_style = "fill:%s;stroke:#ffffff;stroke-width:0.2;font-size:8px;text-align:center;text-anchor:middle" % (fill_color)

        path = inkex.etree.Element(
            SVG_PATH_TAG,
            {
                "id": self.uniqueId("inkstitch__invalid_pointer__"),
                "d": "m %s,%s 4,20 h -8 l 4,-20" % (problem.position.x, problem.position.y),
                "style": pointer_style,
                INKSCAPE_LABEL: _('Invalid Pointer'),
                "transform": correction_transform
            }
        )
        layer.insert(0, path)

        text = inkex.etree.Element(
            SVG_TEXT_TAG,
            {
                INKSCAPE_LABEL: _('Description'),
                "x": str(problem.position.x),
                "y": str(float(problem.position.y) + 30),
                "transform": correction_transform,
                "style": text_style
            }
        )
        layer.append(text)

        tspan = inkex.etree.Element(SVG_TSPAN_TAG)
        tspan.text = problem.name
        text.append(tspan)

    def create_troubleshoot_layer(self):
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validation_layer__']")

        if layer is None:
            layer = inkex.etree.Element(
                SVG_GROUP_TAG,
                {
                    'id': '__validation_layer__',
                    INKSCAPE_LABEL: _('Troubleshoot'),
                    INKSCAPE_GROUPMODE: 'layer',
                })
            svg.append(layer)

        else:
            # Clear out everything from the last run
            del layer[:]

        add_layer_commands(layer, ["ignore_layer"])

        error_group = inkex.etree.SubElement(
            layer,
            SVG_GROUP_TAG,
            {
                "id": '__validation_errors__',
                INKSCAPE_LABEL: _("Errors"),
            })
        layer.append(error_group)

        warning_group = inkex.etree.SubElement(
            layer,
            SVG_GROUP_TAG,
            {
                "id": '__validation_warnings__',
                INKSCAPE_LABEL: _("Warnings"),
            })
        layer.append(warning_group)

        self.troubleshoot_layer = layer
        self.error_group = error_group
        self.warning_group = warning_group

    def add_descriptions(self, problem_types):
        svg = self.document.getroot()
        text_x = str(self.unittouu(svg.get('width')) + 5)

        text_container = inkex.etree.Element(
            SVG_TEXT_TAG,
            {
                "x": text_x,
                "y": str(5),
                "style": "fill:#000000;font-size:5px;line-height:1;"
            }
        )
        self.troubleshoot_layer.append(text_container)

        text = [
            [_("Troubleshoot"), "font-weight: bold; font-size: 6px;"],
            ["", ""]
        ]

        for problem in problem_types:
            text_color = "#ff0000"
            if issubclass(problem, ValidationWarning):
                text_color = "#ffdd00"

            text.append([problem.name, "font-weight: bold; fill:%s;" % text_color])
            description_parts = textwrap.wrap(problem.description, 60)
            for description in description_parts:
                text.append([description, "font-size: 3px;"])
            text.append(["", ""])
            for step in problem.steps_to_solve:
                text.append([step, "font-size: 4px;"])
            text.append(["", ""])

        explain_layer = _('It is possible, that one object contains more than one error, ' +
                          'yet there will be only one pointer per object.  Run this function again, ' +
                          'when further errors occur.  Remove pointers by deleting the layer named '
                          '"Troubleshoot" through the objects panel (Object -> Objects...).')
        explain_layer_parts = textwrap.wrap(explain_layer, 60)
        for description in explain_layer_parts:
            text.append([description, "font-style: italic; font-size: 3px;"])

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
