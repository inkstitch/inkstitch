# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from lxml import etree

from ..elements import SatinColumn
from ..i18n import _
from ..svg.tags import INKSTITCH_ATTRIBS, SVG_DEFS_TAG
from .base import InkstitchExtension


class ApplySatinPattern(InkstitchExtension):
    # Add inkstitch:pattern attribute to selected patterns. The patterns will be projected on a satin column, which must be in the selection too

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selected or not any(isinstance(item, SatinColumn) for item in self.elements) or len(self.svg.selected) < 2:
            inkex.errormsg(_("Please select at least one satin column and a pattern."))
            return

        if sum(isinstance(item, SatinColumn) for item in self.elements) > 1:
            inkex.errormsg(_("Please select only one satin column."))
            return

        satin_id = self.get_satin_column().node.get('id', None)
        patterns = self.get_patterns()

        for pattern in patterns:
            pattern.node.set(INKSTITCH_ATTRIBS['pattern'], satin_id)
            self.set_marker(pattern.node)

    def get_satin_column(self):
        return list(filter(lambda satin: isinstance(satin, SatinColumn), self.elements))[0]

    def get_patterns(self):
        return list(filter(lambda satin: not isinstance(satin, SatinColumn), self.elements))

    def set_marker(self, node):
        document = node.getroottree().getroot()
        xpath = ".//marker[@id='inkstitch-pattern-marker']"
        pattern_marker = document.xpath(xpath)
        if not pattern_marker:
            # get or create def element
            defs = document.find(SVG_DEFS_TAG)
            if defs is None:
                defs = etree.SubElement(document, SVG_DEFS_TAG)

            # insert marker
            marker = """<marker
                     refX="5"
                     refY="2.5"
                     orient="auto"
                     id="inkstitch-pattern-marker">
                    <g
                       id="inkstitch-pattern-group">
                      <path
                         style="fill:#fafafa;stroke:#ffbe00;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:1, 0.5;stroke-dashoffset:0;stroke-opacity:1"
                         d="m 5.05952,2.58154 c 0,1.35905 -1.10173,2.4608 -2.46079,2.4608 -1.35905,0 -2.46079,-1.10175 -2.46079,-2.4608 0,-0.65262 0.259271,-1.27856 0.720751,-1.74004 C 1.32018,0.38002 1.94609,0.120749 2.59873,0.120749 c 1.35906,0 2.46079,1.101751 2.46079,2.460791 z"
                         id="inkstitch-pattern-marker-circle" />
                      <path
                         style="fill:none;stroke:#000000;stroke-width:0.1;stroke-linecap:round;stroke-miterlimit:4;"
                         id="inkstitch-pattern-marker-spiral"
                         d="M 2.45807,2.80588 C 2.35923,2.84009 2.28168,2.72985 2.27863,2.64621 2.27369,2.48274 2.43336,2.37629 2.58086,2.3877 2.8006,2.40291 2.94012,2.6234 2.91389,2.83249 2.87853,3.11001 2.59683,3.28488 2.3292,3.24307 1.99161,3.18604 1.78366,2.84389 1.84297,2.51695 1.9152,2.11778 2.32311,1.87448 2.70974,1.95431 3.16593,2.04175 3.44307,2.51315 3.34955,2.96175 3.24121,3.47497 2.70594,3.7867 2.2007,3.67645 1.62589,3.551 1.27919,2.95034 1.4073,2.3877 1.551,1.75283 2.21439,1.37266 2.83823,1.51713 3.53165,1.67679 3.94793,2.40671 3.78522,3.0872 3.60616,3.83992 2.81504,4.29232 2.07221,4.11364 1.26018,3.91595 0.773949,3.06059 0.971634,2.25844 1.18605,1.38787 2.10528,0.867047 2.96711,1.07994 3.89775,1.31184 4.45317,2.29646 4.22089,3.21645 4.20112,3.29629 4.17565,3.37612 4.14523,3.45216" />
                    </g>
                    </marker>"""  # noqa: E501
            defs.append(etree.fromstring(marker))

        # attach marker to node
        style = node.get('style', '').split(";")
        import sys
        print(style, file=sys.stderr)
        style = [i for i in style if not i.startswith('marker-start')]
        style.append('marker-start:url(#inkstitch-pattern-marker)')
        node.set('style', ";".join(style))
