#!/usr/bin/python
#
# Set embroidery parameter attributes on all selected objects.  If an option
# value is blank, the parameter is created as blank on all objects that don't
# already have it.  If an option value is given, any existing node parameter
# values are overwritten on all selected objects.

import sys
sys.path.append("/usr/share/inkscape/extensions")
import os
import inkex


class EmbroiderParams(inkex.Effect):
    def __init__(self, *args, **kwargs):
        inkex.Effect.__init__(self)
        
        self.params = ["zigzag_spacing",
                       "stitch_length",
                       "row_spacing",
                       "max_stitch_length",
                       "repeats",
                       "angle",
                       "hatching",
                       "flip",
                       "satin_column",
                       "stroke_first",
                       "pull_compensation",
                      ]
       
        for param in self.params:
            self.OptionParser.add_option("--%s" % param, default="")

    def effect(self):    
        for node in self.selected.itervalues():
            for param in self.params:
                value = getattr(self.options, param).strip()
                param = "embroider_" + param
                
                if node.get(param) is not None and not value:
                    # only overwrite existing params if they gave a value
                    continue
                else:
                    node.set(param, value)

if __name__ == '__main__':
    e = EmbroiderParams()
    e.affect()
