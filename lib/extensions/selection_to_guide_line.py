# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from lxml import etree

from ..i18n import _
from ..svg.tags import SVG_PATH_TAG, SVG_POLYLINE_TAG, SVG_DEFS_TAG
from .base import InkstitchExtension


class SelectionToGuideLine(InkstitchExtension):

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selected:
            inkex.errormsg(_("Please select one object to be marked as a guide line."))
            return

        if len(self.get_nodes())!=1:
            inkex.errormsg(_("Please select only one object to be marked as a guide line."))
            return

        for guide_line in self.get_nodes():
            if guide_line.tag in (SVG_PATH_TAG, SVG_POLYLINE_TAG):
                self.set_marker(guide_line)

    def set_marker(self, node):
        xpath = ".//marker[@id='inkstitch-guide-line-marker']"
        guide_line_marker = self.document.xpath(xpath)

        if not guide_line_marker:
            # get or create def element
            defs = self.document.find(SVG_DEFS_TAG)
            if defs is None:
                defs = etree.SubElement(self.document, SVG_DEFS_TAG)

            # insert marker
            marker = """<marker
                      refX="10"
                      refY="5"
                      orient="auto"
                      id="inkstitch-guide-line-marker">
                     <g
                        id="inkstitch-guide-line-group">
                       <path
                          style="fill:#fafafa;stroke:#ff00ff;stroke-width:0.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:1, 1;stroke-dashoffset:0;stroke-opacity:1;fill-opacity:0.8;"
                          d="M 10.12911,5.2916678 A 4.8374424,4.8374426 0 0 1 5.2916656,10.12911 4.8374424,4.8374426 0 0 1 0.45422399,5.2916678 4.8374424,4.8374426 0 0 1 5.2916656,0.45422399 4.8374424,4.8374426 0 0 1 10.12911,5.2916678 Z"
                          id="inkstitch-guide-line-marker-circle" />
                       <path
                          style="fill:none;stroke:#ff00ff;stroke-width:0.4;stroke-linecap:round;stroke-miterlimit:4;"
                          id="inkstitch-guide-line-marker-spiral"
                          d="M 4.9673651,5.7245662 C 4.7549848,5.7646159 4.6247356,5.522384 4.6430021,5.3419847 4.6765851,5.0103151 5.036231,4.835347 5.3381858,4.8987426 5.7863901,4.9928495 6.0126802,5.4853625 5.9002872,5.9065088 5.7495249,6.4714237 5.1195537,6.7504036 4.5799191,6.5874894 3.898118,6.3816539 3.5659013,5.6122905 3.7800789,4.9545192 4.0402258,4.1556558 4.9498996,3.7699484 5.7256318,4.035839 6.6416744,4.3498087 7.0810483,5.4003986 6.7631909,6.2939744 6.395633,7.3272552 5.2038143,7.8204128 4.1924535,7.4503931 3.0418762,7.0294421 2.4948761,5.6961604 2.9171752,4.567073 3.3914021,3.2991406 4.8663228,2.6982592 6.1130974,3.1729158 7.4983851,3.7003207 8.1531869,5.3169977 7.6260947,6.6814205 7.0456093,8.1841025 5.2870784,8.8928844 3.8050073,8.3132966 2.1849115,7.6797506 1.4221671,5.7793073 2.0542715,4.1796074 2.7408201,2.4420977 4.7832541,1.6253548 6.5005435,2.310012 8.3554869,3.0495434 9.2262638,5.2339874 8.4890181,7.0688861 8.4256397,7.2266036 8.3515789,7.379984 8.2675333,7.5277183" />
                     </g>
                     </marker>"""  # noqa: E501
            defs.append(etree.fromstring(marker))

        # attach marker to node
        style = node.get('style') or ''
        style = style.split(";")
        style = [i for i in style if not i.startswith('marker-start')]
        style.append('marker-start:url(#inkstitch-guide-line-marker)')
        node.set('style', ";".join(style))
