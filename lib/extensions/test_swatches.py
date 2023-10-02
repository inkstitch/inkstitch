# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS
from .base import InkstitchExtension


class TestSwatches(InkstitchExtension):
    '''
    This generates swatches from selection by altering one param each time.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--options")
        self.arg_parser.add_argument("--info")

        self.arg_parser.add_argument("-p", "--param", type=str, default="max_stitch_length_mm", dest="param")
        self.arg_parser.add_argument("-s", "--start-value", type=float, default="max_stitch_length_mm", dest="start_value")
        self.arg_parser.add_argument("-i", "--step", type=float, default="0.5", dest="step")
        self.arg_parser.add_argument("-r", "--num-rows", type=int, default="5", dest="num_rows")
        self.arg_parser.add_argument("-c", "--num-cols", type=int, default="5", dest="num_cols")
        self.arg_parser.add_argument("-d", "--spacing", type=float, default="1", dest="spacing")

    def effect(self):
        if not self.svg.selection:
            errormsg(_("Please select one or more elements."))
            return

        for element in self.svg.selection:
            dimensions = element.bounding_box()
            param_value = self.options.start_value
            for rows in range(0, self.options.num_rows):
                for cols in range(0, self.options.num_cols):
                    new_element = element.duplicate()
                    translate_x = cols * dimensions.width + cols * self.options.spacing
                    translate_y = rows * dimensions.height + rows * self.options.spacing
                    new_element.transform.add_translate((translate_x, translate_y))
                    if new_element.TAG == "g":
                        for embroidery_element in new_element.iterdescendants(EMBROIDERABLE_TAGS):
                            # Since this won't effect functionality, we can simply ignore the fact
                            # that this will also set the value to guide lines etc.
                            self._set_param(embroidery_element, param_value)
                    else:
                        self._set_param(new_element, param_value)
                    param_value += self.options.step
            # remove old element
            element.getparent().remove(element)

    def _set_param(self, element, value):
        element.set(f'inkstitch:{ self.options.param }', value)
