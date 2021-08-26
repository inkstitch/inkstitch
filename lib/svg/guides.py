# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex.units import convert_unit

from ..utils import Point, cache, string_to_floats
from .tags import (INKSCAPE_DOCUMENT_UNITS, INKSCAPE_LABEL, SODIPODI_GUIDE,
                   SODIPODI_NAMEDVIEW)


class InkscapeGuide(object):
    def __init__(self, node):
        self.node = node
        self.svg = node.getroottree().getroot()

        self._parse()

    def _parse(self):
        self.label = self.node.get(INKSCAPE_LABEL, "")

        doc_size = self.svg.get_page_bbox()

        # inkscape's Y axis is reversed from SVG's, and the guide is in inkscape coordinates
        self.position = Point(*string_to_floats(self.node.get('position')))
        self.position.y = doc_size.y.size - self.position.y

        # convert units to px
        namedview = _get_namedview(self.svg)
        unit = namedview.get(INKSCAPE_DOCUMENT_UNITS) or namedview.get('units', 'px')
        self.position.y = convert_unit(self.position.y, 'px', unit)

        # This one baffles me.  I think inkscape might have gotten the order of
        # their vector wrong?
        parts = string_to_floats(self.node.get('orientation'))
        self.direction = Point(parts[1], parts[0])


@cache
def get_guides(svg):
    """Find all Inkscape guides and return as InkscapeGuide instances."""

    namedview = _get_namedview(svg)
    if namedview is None:
        return []

    return [InkscapeGuide(node) for node in namedview.findall(SODIPODI_GUIDE)]


@cache
def _get_namedview(svg):
    return svg.find(SODIPODI_NAMEDVIEW)
