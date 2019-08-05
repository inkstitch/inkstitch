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
    FABRIC_DEFAULT_RADIUS_TO_CHECK_MM = 0.5

    def __init__(self, *args, **kwargs):
        NeedleDrawingPanel.__init__(self, *args, **kwargs)
        self.needle_density_info.__class__ = NeedleDensityInformation
        # above works and is pythonic, but require that there are no additonal instance variable in the higher class
        self.thread_to_thread_density_search = self.initialise_density_search_with_limits(
            density_area_radius_mm=self.check_option_overriding_default_limit(
                NeedleDensityDrawingPanel.FABRIC_DEFAULT_RADIUS_TO_CHECK_MM, "fabric_radius_examined_mm"))

    def check_option_overriding_default_limit(self, default_limit, option_name_to_check):
        density_search_area_mm = default_limit
        if self.options is not None:
            options_as_dict = self.options.__dict__
            if option_name_to_check in options_as_dict:
                density_search_area_mm = options_as_dict[option_name_to_check]
        return density_search_area_mm

    def initialise_density_search_with_limits(self, density_area_radius_mm=FABRIC_DEFAULT_RADIUS_TO_CHECK_MM):
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
        dp_wanted_stitch = self.wanted_stitch
        self.set_show_colour_info()
        self.needle_density_info.calculate_needle_density_up_to_current_point(
            dp_wanted_stitch, self.thread_to_thread_density_search)
        self.output_needle_points_up_to_current_point(dp_wanted_stitch)
        # self.output_needle_points_up_to_current_point(suppress_colours=["ORANGE", "SKY BLUE", "BLACK"])
        last_stitch = self.needle_density_info.calculated_stitch_at_index_as_list(dp_wanted_stitch - 1)
        self.last_frame_duration = time.time() - start

        self.handle_last_painted_stitch(last_stitch, dp_wanted_stitch)

    def set_show_colour_info(self):
        self.set_info_text(
            "distance<=" + format(self.thread_to_thread_density_search.density_area_radius_mm, '.2') + "mm , " +
            "Counts: "
            "Purple>=" + str(self.thread_to_thread_density_search.terrible_density_limit_count) + " , " +
            "Red>=" + str(self.thread_to_thread_density_search.bad_density_limit_count) + " , " +
            "Orange>=" + str(self.thread_to_thread_density_search.warn_density_limit_count) + " , " +
            "sky blue>=" + str(self.thread_to_thread_density_search.high_density_limit_count) + " , " +
            "black=rest")


class NeedleDensitySimulatorPanel(BaseSimulatorPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseSimulatorPanel.__init__(self, parent, *args, **kwargs)
        self.cp = NeedleDensityControlPanel(self,
                                            stitch_plan=self.stitch_plan,
                                            stitches_per_second=self.stitches_per_second,
                                            target_duration=self.target_duration,
                                            options=self.options)
        self.dp = NeedleDensityDrawingPanel(self, stitch_plan=self.stitch_plan, control_panel=self.cp,
                                            options=self.options)
        self.FinaliseInit()


class NeedleDensitySimulator(BaseSimulator):
    def __init__(self, *args, **kwargs):
        BaseSimulator.__init__(self, *args, **kwargs)
        needle_simulator_panel = NeedleDensitySimulatorPanel(self,
                                                             stitch_plan=self.stitch_plan,
                                                             target_duration=self.target_duration,
                                                             stitches_per_second=self.stitches_per_second,
                                                             options=self.options)
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
