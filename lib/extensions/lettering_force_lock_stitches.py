# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from shapely.geometry import Point

from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSTITCH_ATTRIBS
from .base import InkstitchExtension


class LetteringForceLockStitches(InkstitchExtension):
    '''
    This extension helps font creators to add the force lock stitches attribute to the last objects of each glyph
    Font creators to add forced lock stitches on glyphs with accents / spaces.
    '''

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-a", "--max_distance", type=float, default=3, dest="max_distance")
        self.arg_parser.add_argument("-i", "--min_distance", type=float, default=1, dest="min_distance")
        self.arg_parser.add_argument("-l", "--last_element", type=inkex.Boolean, dest="last_element")

    def effect(self):
        if self.options.max_distance < self.options.min_distance:
            inkex.errormssg(_("The maximum value is smaller than the minimum value."))

        # Set glyph layers to be visible. We don't want them to be ignored by self.elements
        self._update_layer_visibility('inline')

        # mark last elements of a glyph
        xpath = ".//svg:g[@inkscape:groupmode='layer']//svg:path[last()]"
        last_elements = self.document.xpath(xpath, namespaces=inkex.NSS)
        for last_element in last_elements:
            last_element.set('lastglyphelement', str(True))

        # find last point of an element
        if not self.get_elements():
            return

        previous_element = None
        last_stitch = None
        for element in self.elements:
            stitch_group = element.to_stitch_groups(None)
            # if the distance of the last stitch of the previous object to the first stitch of this objects
            # lies within the user defined distance range, set the force_lock_stitches-attribute.
            if last_stitch:
                first_stitch = stitch_group[0].stitches[0]
                first_stitch = Point(first_stitch.x, first_stitch.y)
                self._set_force_attribute(first_stitch, last_stitch, previous_element)

            # if this is the last element of a glyph, we don't want to compare it to the next element
            if element.node.get('lastglyphelement', False):
                previous_element = None
                last_stitch = None
            else:
                previous_element = element
                last_stitch = stitch_group[-1].stitches[-1]
                last_stitch = Point(last_stitch.x, last_stitch.y)

        # remove last element attributes again
        # set force lock stitches attribute if needed
        for last_element in last_elements:
            last_element.attrib.pop('lastglyphelement')
            if self.options.last_element:
                last_element.set(INKSTITCH_ATTRIBS['force_lock_stitches'], True)

        # hide glyph layers again
        self._update_layer_visibility('none')

    def _set_force_attribute(self, first_stitch, last_stitch, previous_element):
        distance_mm = first_stitch.distance(last_stitch) / PIXELS_PER_MM

        if distance_mm < self.options.max_distance and distance_mm > self.options.min_distance:
            previous_element.node.set(INKSTITCH_ATTRIBS['force_lock_stitches'], True)

    def _update_layer_visibility(self, display):
        xpath = ".//svg:g[@inkscape:groupmode='layer']"
        layers = self.document.xpath(xpath, namespaces=inkex.NSS)
        for layer in layers:
            display_style = 'display:%s' % display
            style = inkex.Style(layer.get('style', '')) + inkex.Style(display_style)
            layer.set('style', style)
