from .base import InkstitchExtension
from ..i18n import _
from ..simulator import show_simulator
from ..stitch_plan import patches_to_stitch_plan


class Simulate(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")

    def effect(self):
        if not self.get_elements():
            return
        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        show_simulator(stitch_plan)
