import sys

from ..elements import Fill, Stroke
from ..i18n import _
from .base import InkstitchExtension


class Cleanup(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.OptionParser.add_option("-f", "--rm_fill", dest="rm_fill", type="inkbool", default=True)
        self.OptionParser.add_option("-s", "--rm_stroke", dest="rm_stroke", type="inkbool", default=True)
        self.OptionParser.add_option("-a", "--fill_threshold", dest="fill_threshold", type="int", default=20)
        self.OptionParser.add_option("-l", "--stroke_threshold", dest="stroke_threshold", type="int", default=5)

    def effect(self):
        self.rm_fill = self.options.rm_fill
        self.rm_stroke = self.options.rm_stroke
        self.fill_threshold = self.options.fill_threshold
        self.stroke_threshold = self.options.stroke_threshold

        # Remove selection, we want every element in the document
        self.selected = {}

        if not self.get_elements():
            return

        count = 0
        for element in self.elements:
            if (isinstance(element, Fill) and self.rm_fill and
               element.shape.area < self.fill_threshold):
                element.node.getparent().remove(element.node)
                count += 1
            if (isinstance(element, Stroke) and self.rm_stroke and
               element.shape.length < self.stroke_threshold and element.node.getparent() is not None):
                element.node.getparent().remove(element.node)
                count += 1

        print(_("%s elements removed" % count), file=sys.stderr)
