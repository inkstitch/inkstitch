# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import deepcopy
from os import path

from shapely import geometry as shgeo

import inkex

from .svg.tags import EMBROIDERABLE_TAGS
from .utils import cache, get_bundled_dir

MARKER = ['pattern', 'guide-line']


def ensure_marker(svg, marker):
    marker_path = ".//*[@id='inkstitch-%s-marker']" % marker
    if svg.defs.find(marker_path) is None:
        svg.defs.append(deepcopy(_marker_svg().defs.find(marker_path)))


@cache
def _marker_svg():
    marker_path = path.join(get_bundled_dir("symbols"), "marker.svg")
    with open(marker_path) as marker_file:
        return inkex.load_svg(marker_file).getroot()


def set_marker(node, position, marker):
    ensure_marker(node.getroottree().getroot(), marker)

    # attach marker to node
    style = node.get('style') or ''
    style = style.split(";")
    style = [i for i in style if not i.startswith('marker-%s' % position)]
    style.append('marker-%s:url(#inkstitch-%s-marker)' % (position, marker))
    node.set('style', ";".join(style))


def get_marker_elements(node, marker, get_fills=True, get_strokes=True, get_satins=False):
    from .elements import EmbroideryElement
    from .elements.fill_stitch import FillStitch
    from .elements.satin_column import SatinColumn
    from .elements.stroke import Stroke

    fills = []
    strokes = []
    satins = []
    # do not close marker-start:url(
    # if the marker group has been copied and pasted in Inkscape it may have been duplicated with an updated id (e.g. -4)
    xpath = "./parent::svg:g/*[contains(@style, 'marker-start:url(#inkstitch-%s-marker')]" % marker
    markers = node.xpath(xpath, namespaces=inkex.NSS)
    for marker in markers:
        if marker.tag not in EMBROIDERABLE_TAGS:
            continue

        element = EmbroideryElement(marker)
        fill = element.get_style('fill')
        stroke = element.get_style('stroke')

        if get_fills and fill is not None:
            fill = FillStitch(marker).shape
            fills.append(fill)

        if get_strokes and stroke is not None:
            stroke = Stroke(marker).paths
            line_strings = [shgeo.LineString(path) for path in stroke]
            strokes.append(shgeo.MultiLineString(line_strings))

        if get_satins and stroke is not None:
            satin = SatinColumn(marker)
            if len(satin.rails) == 2:
                satins.append(satin)

    return {'fill': fills, 'stroke': strokes, 'satin': satins}


def has_marker(node, marker=list()):
    if not marker:
        marker = MARKER
    for m in marker:
        style = node.get('style') or ''
        if "marker-start:url(#inkstitch-%s-marker" % m in style:
            return True
    return False
