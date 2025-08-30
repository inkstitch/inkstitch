# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from itertools import chain

import inkex
from shapely import geometry as shgeo

from ..elements import SatinColumn, Stroke
from ..elements.utils.stroke_to_satin import (convert_path_to_satin,
                                              set_first_node)
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.styles import get_join_style_args
from .base import InkstitchExtension


class StrokeToSatin(InkstitchExtension):
    """Convert a line to a satin column of the same width."""

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            inkex.errormsg(_("Please select at least one line to convert to a satin column."))
            return

        satin_converted = False
        for element in self.elements:
            if not isinstance(element, Stroke) and not (isinstance(element, SatinColumn) and len(element.paths) == 1):
                continue

            parent = element.node.getparent()
            index = parent.index(element.node)
            correction_transform = get_correction_transform(element.node)
            style_args = get_join_style_args(element)
            path_style = self.path_style(element)

            paths = element.paths
            if element.is_closed_path:
                set_first_node(paths, element.stroke_width)

            for path in paths:
                satin_paths = convert_path_to_satin(path, element.stroke_width, style_args)

                if satin_paths is not None:
                    rails, rungs = list(satin_paths)
                    rungs = self.filtered_rungs(rails, rungs)

                    path_element = self.satin_to_svg_node(rails, rungs)
                    path_element.set('id', self.uniqueId("path"))
                    path_element.set('transform', correction_transform)
                    path_element.set('style', path_style)
                    parent.insert(index, path_element)

            element.node.delete()
            satin_converted = True

        if not satin_converted:
            # L10N: Convert To Satin extension, user selected only objects that were not lines.
            inkex.errormsg(_("Only simple lines may be converted to satin columns."))

    def filtered_rungs(self, rails, rungs):
        rails = shgeo.MultiLineString(rails)
        filtered_rungs = []
        for rung in shgeo.MultiLineString(rungs).geoms:
            intersection = rung.intersection(rails)
            if intersection.geom_type == "MultiPoint" and len(intersection.geoms) == 2:
                filtered_rungs.append(list(rung.coords))
        return filtered_rungs

    def path_style(self, element):
        color = element.get_style('stroke', '#000000')
        return "stroke:%s;stroke-width:1px;fill:none" % (color)

    def satin_to_svg_node(self, rails, rungs):
        d = ""
        for path in chain(rails, rungs):
            d += "M"
            for x, y in path:
                d += "%s,%s " % (x, y)
            d += " "

        path_element = inkex.PathElement(attrib={
            "d": d,
        })
        path_element.set("inkstitch:satin_column", True)
        return path_element
