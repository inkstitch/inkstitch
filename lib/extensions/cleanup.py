# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Boolean, errormsg

from ..elements import FillStitch, Stroke
from ..i18n import _
from ..svg.tags import SVG_GROUP_TAG
from .base import InkstitchExtension


class Cleanup(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--rm_fill", dest="rm_fill", type=Boolean, default=True)
        self.arg_parser.add_argument("-s", "--rm_stroke", dest="rm_stroke", type=Boolean, default=True)
        self.arg_parser.add_argument("-a", "--fill_threshold", dest="fill_threshold", type=int, default=20)
        self.arg_parser.add_argument("-l", "--stroke_threshold", dest="stroke_threshold", type=int, default=5)
        self.arg_parser.add_argument("-g", "--rm_groups", dest="rm_groups", type=Boolean, default=True)
        self.arg_parser.add_argument("-d", "--dry_run", dest="dry_run", type=Boolean, default=False)

    def effect(self):
        self.rm_fill = self.options.rm_fill
        self.rm_stroke = self.options.rm_stroke
        self.fill_threshold = self.options.fill_threshold
        self.stroke_threshold = self.options.stroke_threshold
        self.rm_groups = self.options.rm_groups
        self.dry_run = self.options.dry_run

        self.svg.selection.clear()
        self.get_elements()

        self.elements_to_remove = []
        svg = self.document.getroot()
        empty_d_objects = svg.xpath(".//svg:path[@d='' or not(@d)]", namespaces=NSS)
        for empty in empty_d_objects:
            self.elements_to_remove.append(empty)

        for element in self.elements:
            if self.rm_fill and (isinstance(element, FillStitch) and element.shape.area < self.fill_threshold):
                self.elements_to_remove.append(element.node)
            if self.rm_stroke and (isinstance(element, Stroke) and
               element.shape.length < self.stroke_threshold and element.node.getparent() is not None):
                self.elements_to_remove.append(element.node)

        self.groups_to_remove = []
        if self.rm_groups:
            for group in self.svg.iterdescendants(SVG_GROUP_TAG):
                if len(group.getchildren()) == 0:
                    self.groups_to_remove.append(group)

        if self.dry_run:
            self._dry_run()
        else:
            self._remove()

    def _dry_run(self):
        errormsg(_("%s elements to remove:" % len(self.elements_to_remove)))
        for element in self.elements_to_remove:
            errormsg(f" - { element.label }: {element.get_id()}")

        errormsg("\n")
        errormsg(_("%s groups/layers to remove:" % len(self.groups_to_remove)))
        for group in self.groups_to_remove:
            errormsg(f" - { group.label }: {group.get_id()}")

    def _remove(self):
        errormsg(_("%s elements removed" % len(self.elements_to_remove)))
        for element in self.elements_to_remove:
            element.getparent().remove(element)

        errormsg(_("%s groups/layers removed" % len(self.groups_to_remove)))
        for group in self.groups_to_remove:
            group.getparent().remove(group)
