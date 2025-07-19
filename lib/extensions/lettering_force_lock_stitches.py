# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from shapely.geometry import Point

from ..elements import iterate_nodes, nodes_to_elements
from ..i18n import _
from ..marker import has_marker
from ..svg import PIXELS_PER_MM
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_GROUP_TAG
from .base import InkstitchExtension


class LetteringForceLockStitches(InkstitchExtension):
    '''
    This extension helps font creators to add the force lock stitches attribute to the last objects of each glyph
    Font creators to add forced lock stitches on glyphs with accents / spaces.
    '''

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-s", "--satin_only", type=inkex.Boolean, dest="satin_only")
        self.arg_parser.add_argument("-d", "--distance", type=inkex.Boolean, dest="distance")
        self.arg_parser.add_argument("-a", "--max_distance", type=float, default=3, dest="max_distance")
        self.arg_parser.add_argument("-i", "--min_distance", type=float, default=1, dest="min_distance")
        self.arg_parser.add_argument("-l", "--last_element", type=inkex.Boolean, dest="last_element")
        self.arg_parser.add_argument("-g", "--last_group_element", type=inkex.Boolean, dest="last_group_element")

    def effect(self):
        if self.options.max_distance < self.options.min_distance:
            inkex.errormssg(_("The maximum value is smaller than the minimum value."))

        glyph_layers = self.document.xpath('.//svg:g[starts-with(@inkscape:label, "GlyphLayer")]', namespaces=inkex.NSS)
        uses_glyph_layers = True
        if not glyph_layers:
            # they maybe want to use this method for a regular document. Let's allow it, why not.
            glyph_layers = [self.document.getroot()]
            uses_glyph_layers = False
        else:
            # Set glyph layers to be visible. We don't want them to be ignored by self.elements
            self._update_layer_visibility('inline')
        for layer in glyph_layers:
            if uses_glyph_layers and self.options.last_group_element:
                self._set_force_attribute_on_last_group_elements(layer)
            if uses_glyph_layers and self.options.last_element:
                self._set_force_attribute_on_last_elements(layer)
            if self.options.distance:
                self._set_force_attribute_by_distance(layer)

        if uses_glyph_layers:
            # unhide glyph layers
            self._update_layer_visibility('none')

    def _set_force_attribute_on_last_group_elements(self, layer):
        group_nodes = list(layer.iterdescendants(SVG_GROUP_TAG))
        for group in group_nodes:
            self._set_force_attribute_on_last_elements(group)

    def _set_force_attribute_on_last_elements(self, layer):
        # find the last path that does not carry a marker or belongs to a visual command and add a trim there
        last_element = None
        child_nodes = list(layer.iterdescendants(EMBROIDERABLE_TAGS))
        child_nodes.reverse()
        for element in child_nodes:
            if not has_marker(element) and not element.get_id().startswith('command_connector'):
                last_element = element
                break
        if last_element is not None:
            if self.options.satin_only and not last_element.get('inkstitch:satin_column', False):
                return
            last_element.set('inkstitch:force_lock_stitches', True)

    def _set_force_attribute_by_distance(self, layer):
        min_distance = self.options.min_distance * PIXELS_PER_MM
        max_distance = self.options.max_distance * PIXELS_PER_MM

        nodes = iterate_nodes(layer)
        elements = nodes_to_elements(nodes)

        last_stitch_group = None
        next_elements = [None]
        if len(elements) > 1:
            next_elements = elements[1:] + next_elements
        for element, next_element in zip(elements, next_elements):
            distance = None
            stitch_groups = element.to_stitch_groups(last_stitch_group, next_element)
            if not stitch_groups:
                continue
            if next_element is not None:
                last_stitch = stitch_groups[-1].stitches[-1]
                next_stitch = next_element.first_stitch
                if stitch_groups[-1].color != next_element.color:
                    last_stitch_group = stitch_groups[-1]
                    continue
                if next_stitch is None:
                    # get nearest point
                    shape = next_element.shape
                    if not shape.is_empty:
                        distance = shape.distance(Point(last_stitch))
                else:
                    distance = Point(last_stitch).distance(Point(next_stitch))

            if distance is not None and distance < max_distance and distance > min_distance:
                if self.options.satin_only and element.name != 'SatinColumn':
                    continue
                element.node.set('inkstitch:force_lock_stitches', True)

            last_stitch_group = stitch_groups[-1]

    def _update_layer_visibility(self, display):
        xpath = ".//svg:g[@inkscape:groupmode='layer']"
        layers = self.document.xpath(xpath, namespaces=inkex.NSS)
        for layer in layers:
            display_style = 'display:%s' % display
            style = inkex.Style(layer.get('style', '')) + inkex.Style(display_style)
            layer.set('style', style)
