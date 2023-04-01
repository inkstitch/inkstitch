# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import textwrap

import inkex

from ..commands import add_layer_commands
from ..elements.validation import (ObjectTypeWarning, ValidationError,
                                   ValidationWarning)
from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..svg.path import get_correction_transform
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SODIPODI_ROLE
from .base import InkstitchExtension


class Troubleshoot(InkstitchExtension):

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-p", "--pointer-size", type=float, default=5, dest="pointer_size_mm")
        self.arg_parser.add_argument("-f", "--font-size", type=float, default=2, dest="font_size_mm")

    def effect(self):
        self.create_troubleshoot_layer()
        problem_types = {'error': set(), 'warning': set(), 'type_warning': set()}

        if self.get_elements(True):
            for element in self.elements:
                for problem in element.validation_errors():
                    problem_types['error'].add(type(problem))
                    self.insert_pointer(problem)
                for problem in element.validation_warnings():
                    if isinstance(problem, ObjectTypeWarning):
                        problem_types['type_warning'].add(type(problem))
                    else:
                        problem_types['warning'].add(type(problem))
                    self.insert_pointer(problem)

        if any(problem_types.values()):
            self.add_descriptions(problem_types)
        else:
            svg = self.document.getroot()
            svg.remove(self.troubleshoot_layer)

            message = _("All selected shapes are valid! ")
            message += "\n\n"
            message += _("If you are still having trouble with a shape not being embroidered, "
                         "check if it is in a layer with an ignore command.")
            inkex.errormsg(message)

    def insert_pointer(self, problem):
        correction_transform = get_correction_transform(self.troubleshoot_layer)
        pointer_size = self.options.pointer_size_mm * PIXELS_PER_MM
        font_size = self.options.font_size_mm * PIXELS_PER_MM

        if isinstance(problem, ValidationWarning):
            fill_color = "#ffdd00"
            layer = self.warning_group
        elif isinstance(problem, ValidationError):
            fill_color = "#ff0000"
            layer = self.error_group
        elif isinstance(problem, ObjectTypeWarning):
            fill_color = "#ff9900"
            layer = self.type_warning_group

        pointer_style = f'stroke:#000000;stroke-width:0.1;fill:{ fill_color }'
        text_style = f'fill:{ fill_color };stroke:#000000;stroke-width:0.1;font-size:{ font_size }px;text-align:center;text-anchor:middle'
        pointer_path = f'm {problem.position.x},{problem.position.y} {pointer_size / 5},{pointer_size} ' \
                       f'h -{pointer_size / 2.5} l {pointer_size / 5},-{pointer_size}'

        path = inkex.PathElement(attrib={
            "id": self.uniqueId("inkstitch__invalid_pointer__"),
            "d": pointer_path,
            "style": pointer_style,
            INKSCAPE_LABEL: _('Invalid Pointer'),
            "transform": correction_transform
        })
        layer.insert(0, path)

        text = inkex.TextElement(attrib={
            INKSCAPE_LABEL: _('Description'),
            "x": str(problem.position.x),
            "y": str(float(problem.position.y) + pointer_size + font_size),
            "transform": correction_transform,
            "style": text_style
        })
        layer.append(text)

        tspan = inkex.Tspan()
        tspan.text = problem.name
        if problem.label:
            tspan.text += " (%s)" % problem.label
        text.append(tspan)

    def create_troubleshoot_layer(self):
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__validation_layer__']")

        if layer is None:
            layer = inkex.Group(attrib={
                'id': '__validation_layer__',
                INKSCAPE_LABEL: _('Troubleshoot'),
                INKSCAPE_GROUPMODE: 'layer',
            })
            svg.append(layer)
        else:
            # Clear out everything from the last run
            del layer[:]

        add_layer_commands(layer, ["ignore_layer"])

        error_group = inkex.Group(attrib={
            "id": '__validation_errors__',
            INKSCAPE_LABEL: _("Errors"),
        })
        layer.append(error_group)

        warning_group = inkex.Group(attrib={
            "id": '__validation_warnings__',
            INKSCAPE_LABEL: _("Warnings"),
        })
        layer.append(warning_group)

        type_warning_group = inkex.Group(attrib={
            "id": '__validation_ignored__',
            INKSCAPE_LABEL: _("Type Warnings"),
        })
        layer.append(type_warning_group)

        self.troubleshoot_layer = layer
        self.error_group = error_group
        self.warning_group = warning_group
        self.type_warning_group = type_warning_group

    def add_descriptions(self, problem_types):  # noqa: C901
        svg = self.document.getroot()

        # We could use svg.viewport_width, but then we would need to do unit conversions,
        # so let's stay with parsing the viewbox by ourselves
        # viewbox values are either separated through white space or commas
        text_x = str(float(svg.get('viewBox', '0 0 800 0').replace(",", " ").split()[2]) + 5.0)

        text_container = inkex.TextElement(attrib={
            "x": text_x,
            "y": str(5),
            "style": "fill:#000000;font-size:5px;line-height:1;"
        })
        self.troubleshoot_layer.append(text_container)

        text = [
            [_("Troubleshoot"), "font-weight: bold; font-size: 8px;"],
            ["", ""]
        ]

        for problem_type, problems in list(problem_types.items()):
            if problem_type == "error":
                text_color = "#ff0000"
                problem_type_header = _("Errors")
                problem_type_description = _("Problems that will prevent the shape from being embroidered.")
            elif problem_type == "warning":
                text_color = "#ffdd00"
                problem_type_header = _("Warnings")
                problem_type_description = _("These are problems that won't prevent the shape from being embroidered. "
                                             "You should consider to fix the warning, but if you don't, "
                                             "Ink/Stitch will do its best to process the object.")
            elif problem_type == "type_warning":
                text_color = "#ff9900"
                problem_type_header = _("Object Type Warnings")
                problem_type_description = _("These objects may not work properly with Ink/Stitch. "
                                             "Follow the instructions to correct unwanted behaviour.")
            if problems:
                text.append([problem_type_header, "font-weight: bold; fill: %s; text-decoration: underline; font-size: 7px;" % text_color])
                text.append(["", ""])
                text.append([problem_type_description, "fill:%s;" % text_color])
                text.append(["", ""])

            for problem in problems:
                text.append([problem.name, "font-weight: bold; fill: %s;" % text_color])
                text.append([problem.description, "font-size: 3px;"])
                text.append(["", ""])
                if problem.steps_to_solve:
                    text.append([_("Possible solutions"), "font-weight: bold; text-decoration: underline; font-size: 4px;"])
                for step in problem.steps_to_solve:
                    text.append([step, "font-size: 4px;"])
                text.append(["", ""])

        explain_layer = _('It is possible, that one object contains more than one error, ' +
                          'yet there will be only one pointer per object.  Run this function again, ' +
                          'when further errors occur.  Remove pointers by deleting the layer named '
                          '"Troubleshoot" through the objects panel (Object -> Objects...).')
        explain_layer_parts = textwrap.wrap(explain_layer, 60)
        for description in explain_layer_parts:
            text.append([description, "font-style: italic; font-size: 4px;"])

        text = self.split_text(text)

        for text_line in text:
            tspan = inkex.Tspan(attrib={
                SODIPODI_ROLE: "line",
                "style": text_line[1]
            })
            tspan.text = text_line[0]
            text_container.append(tspan)

    def split_text(self, text):
        splitted_text = []
        for text_part, style in text:
            if text_part:
                description_parts = textwrap.wrap(text_part, 60)
                for description in description_parts:
                    splitted_text.append([description, style])
            else:
                splitted_text.append(["", ""])
        return splitted_text
