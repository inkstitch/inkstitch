import sys

from lib.gui.needle_simulator_common import NeedleDrawingPanel, NeedlePenInfo, NeedleDensitySearch, \
    NeedleDensityInformation
import time

from ..stitch_plan import stitch_plan_from_file

from ..gui.generic_simulator import show_simulator, BaseSimulator, BaseSimulatorPanel, BaseControlPanel, \
    BaseSimulatorPreview


class NeedleDensityControlPanel(BaseControlPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseControlPanel.__init__(self, parent, *args, **kwargs)


class NeedleDensityDrawingPanel(NeedleDrawingPanel):
    """"""

    def __init__(self, *args, **kwargs):
        NeedleDrawingPanel.__init__(self, *args, **kwargs)
        self.needle_density_info.__class__ = NeedleDensityInformation
        # above works and is pythonic, but require that there are no additonal instance variable in the higher class
        self.thread_to_thread_density_search = self.initialise_density_search_with_limits()

    def initialise_density_search_with_limits(self, density_area_radius_mm=0.5):
        pen_info = NeedlePenInfo("BLACK", 2)
        density_search = NeedleDensitySearch(pen_info, density_area_radius_mm=density_area_radius_mm)
        density_search.set_density_limits_based_on_radius_and_thread()
        density_search.add_density_limit(density_search.terrible_density_limit_count, "PURPLE", 4, 1)
        density_search.add_density_limit(density_search.bad_density_limit_count, "RED", 3, 1)
        density_search.add_density_limit(density_search.warn_density_limit_count, "ORANGE", 3, 1)
        density_search.add_density_limit(density_search.high_density_limit_count, "SKY BLUE", 2, 1)
        return density_search

    def OnPaint(self, e):
        if not self.init_on_paint():
            return

        start = time.time()
        self.needle_density_info.calculate_needle_density_up_to_current_point(
            self.current_stitch, self.thread_to_thread_density_search)
        self.output_needle_points_up_to_current_point()
        # self.output_needle_points_up_to_current_point(suppress_colours=["ORANGE", "SKY BLUE", "BLACK"])
        last_stitch = self.needle_density_info.last_calculated_stitch_as_list()
        self.last_frame_duration = time.time() - start

        self.handle_last_painted_stitch(last_stitch)


class NeedleDensitySimulatorPanel(BaseSimulatorPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseSimulatorPanel.__init__(self, parent, *args, **kwargs)
        self.cp = NeedleDensityControlPanel(self,
                                            stitch_plan=self.stitch_plan,
                                            stitches_per_second=self.stitches_per_second,
                                            target_duration=self.target_duration)
        self.dp = NeedleDensityDrawingPanel(self, stitch_plan=self.stitch_plan, control_panel=self.cp)
        self.FinaliseInit()


class NeedleDensitySimulator(BaseSimulator):
    def __init__(self, *args, **kwargs):
        BaseSimulator.__init__(self, *args, **kwargs)
        needle_simulator_panel = NeedleDensitySimulatorPanel(self,
                                                             stitch_plan=self.stitch_plan,
                                                             target_duration=self.target_duration,
                                                             stitches_per_second=self.stitches_per_second)
        self.link_simulator_panel(needle_simulator_panel)
        self.secure_minimum_size()


class NeedleDensitySimulatorPreview(BaseSimulatorPreview):
    """Manages a preview simulation and a background thread for generating patches."""
    def __init__(self, parent, *args, **kwargs):
        BaseSimulatorPreview.__init__(self, self, parent, *args, **kwargs)


def needle_density_simulator_main():
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    show_simulator(NeedleDensitySimulator, "Needle Density Simulation", stitch_plan)


if __name__ == "__main__":
    needle_density_simulator_main()
