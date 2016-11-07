#!/usr/bin/python
#
# Update embroidery parameters stored in XML attributes from old to new
# format.

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
import inkex
import simplestyle

PIXELS_PER_MM = 10

class EmbroiderParams(inkex.Effect):
    def __init__(self, *args, **kwargs):
        inkex.Effect.__init__(self)

        self.mapping = { "zigzag_spacing":                "zigzag_spacing_mm",
                         "row_spacing":                   "row_spacing_mm",
                         "pull_compensation":             "pull_compensation_mm",
                         "max_stitch_length":             "max_stitch_length_mm",
                         "satin_underlay":                "contour_underlay",
                         "satin_underlay_inset":          "contour_underlay_inset_mm",
                         "satin_zigzag_underlay_spacing": "zigzag_underlay_spacing_mm",
                         "satin_center_walk":             "center_walk_underlay",
                         "stitch_length":                 "running_stitch_length_mm",
                       }

    def effect(self):    
        for node in self.document.getroot().iter():
            for old, new in self.mapping.iteritems():
                old = "embroider_%s" % old
                new = "embroider_%s" % new

                value = node.attrib.pop(old, None)
                if value:
                    if new.endswith('_mm') and value.strip():
                        value = str(float(value) / PIXELS_PER_MM)

                    node.set(new, value)

            if 'embroider_zigzag_underlay_spacing_mm' in node.attrib:
                node.set('embroider_zigzag_underlay', 'yes')

            style = simplestyle.parseStyle(node.get('style'))

            if style.get('fill', 'none') != 'none' and \
               'embroider_auto_fill' not in node.attrib:
                    node.set('embroider_auto_fill', 'no')

if __name__ == '__main__':
    e = EmbroiderParams()
    e.affect()
