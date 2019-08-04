import sys

from lib.gui.needle_density_simulator import NeedleDensityDrawingPanel
from lib.gui.needle_simulator_common import ThreadDensityInformation
import time
# TODO find where Threads are defined, and use instead of constants
# TODO possibly add the limit thresholds for needle and thread density attributes?
# TODO Make 0.15 come out as 0.15 and not 0.1 or 0.2 in incscape menus
from ..stitch_plan import stitch_plan_from_file

from ..gui.generic_simulator import show_simulator, BaseSimulator, BaseSimulatorPanel, BaseControlPanel, \
    BaseSimulatorPreview


class ThreadDensityControlPanel(BaseControlPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseControlPanel.__init__(self, parent, *args, **kwargs)


class ThreadDensityDrawingPanel(NeedleDensityDrawingPanel):
    """"""
    THREAD_TO_CORE_LIMIT_MM = 0.15
    THREAD_TO_THREAD_LIMIT_MM = 0.3

    def __init__(self, *args, **kwargs):
        NeedleDensityDrawingPanel.__init__(self, *args, **kwargs)
        self.needle_density_info.__class__ = ThreadDensityInformation
        # above works and is pythonic, but require that there are no additonal instance variable in the higher class
        self.thread_to_thread_density_search = self.initialise_density_search_with_limits(
            self.check_option_overriding_default_limit(ThreadDensityDrawingPanel.THREAD_TO_THREAD_LIMIT_MM,
                                                       "thread_to_thread_distance_examined_mm"))
        self.thread_to_core_density_search = self.initialise_density_search_with_limits(
            self.check_option_overriding_default_limit(ThreadDensityDrawingPanel.THREAD_TO_CORE_LIMIT_MM,
                                                       "thread_to_needle_core_distance_examined_mm"))
        # TODO when above works, and same in needle_density, rewrite them to simpler call
        self.distance_search = self.initialise_distance_search_with_limits()

    def OnPaint(self, e):
        if not self.init_on_paint():
            return

        start = time.time()
        # TODO Time a first set of calculations, and set a minimum speed of what can be done in say half a second.
        #  that would allow me to calculate in advance before user requests higher speed
        self.needle_density_info.calculate_thread_density_up_to_current_point(
            self.current_stitch, self.thread_to_core_density_search, self.thread_to_thread_density_search)
        self.output_needle_points_up_to_current_point()
        # self.output_needle_points_up_to_current_point(suppress_colours=["ORANGE", "SKY BLUE", "BLACK"])
        last_calculated_stitch = self.needle_density_info.last_calculated_stitch_as_list()
        self.last_frame_duration = time.time() - start

        self.handle_last_painted_stitch(last_calculated_stitch)


class ThreadDensitySimulatorPanel(BaseSimulatorPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseSimulatorPanel.__init__(self, parent, *args, **kwargs)
        self.cp = ThreadDensityControlPanel(self,
                                            stitch_plan=self.stitch_plan,
                                            stitches_per_second=self.stitches_per_second,
                                            target_duration=self.target_duration,
                                            options=self.options)
        self.dp = ThreadDensityDrawingPanel(self, stitch_plan=self.stitch_plan, control_panel=self.cp,
                                            options=self.options)
        self.FinaliseInit()


class ThreadDensitySimulator(BaseSimulator):
    def __init__(self, *args, **kwargs):
        BaseSimulator.__init__(self, *args, **kwargs)
        needle_simulator_panel = ThreadDensitySimulatorPanel(self,
                                                             stitch_plan=self.stitch_plan,
                                                             target_duration=self.target_duration,
                                                             stitches_per_second=self.stitches_per_second,
                                                             options=self.options)
        self.link_simulator_panel(needle_simulator_panel)
        self.secure_minimum_size()


class ThreadDensitySimulatorPreview(BaseSimulatorPreview):
    """Manages a preview simulation and a background thread for generating patches."""
    def __init__(self, parent, *args, **kwargs):
        BaseSimulatorPreview.__init__(self, self, parent, *args, **kwargs)


def thread_density_simulator_main():
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    show_simulator(ThreadDensitySimulator, "Thread Density Simulation", stitch_plan)


if __name__ == "__main__":
    thread_density_simulator_main()
