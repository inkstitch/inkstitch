from lib.gui.thread_density_simulator import ThreadDensitySimulator
from ..gui.generic_simulator import show_simulator
from ..stitch_plan import patches_to_stitch_plan
from .base import InkstitchExtension


class ThreadDensity(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")
        self.OptionParser.add_option("-c", "--thread_to_needle_core_distance_examined_mm",
                                     action="store", type="float",
                                     dest="thread_to_needle_core_distance_examined_mm", default=0.15,
                                     help="most severe distance warning (mm)")
        self.OptionParser.add_option("-t", "--thread_to_thread_distance_examined_mm",
                                     action="store", type="float",
                                     dest="thread_to_thread_distance_examined_mm", default=0.30,
                                     help="less severe distance warning (mm)")

    def effect(self):
        if not self.get_elements():
            return
        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        show_simulator(ThreadDensitySimulator, "Thread Density Simulation", stitch_plan, self.options)
