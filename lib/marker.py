# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from copy import deepcopy
from os import path

import inkex

from .utils import cache, get_bundled_dir

MARKER = ['pattern']


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
    style.append('marker-%s:url(#inkstitch-pattern-marker)' % position)
    node.set('style', ";".join(style))
