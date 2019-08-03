import sys

from lib.gui.needle_simulator_common import NeedleDrawingPanel
import time

from ..stitch_plan import stitch_plan_from_file

from ..gui.generic_simulator import show_simulator, BaseSimulator, BaseSimulatorPanel, BaseControlPanel, \
    BaseSimulatorPreview


class NeedleDistanceControlPanel(BaseControlPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseControlPanel.__init__(self, parent, *args, **kwargs)


class NeedleDistanceDrawingPanel(NeedleDrawingPanel):
    """"""
    def __init__(self, *args, **kwargs):
        NeedleDrawingPanel.__init__(self, *args, **kwargs)
        self.distance_search = self.initialise_distance_search_with_limits()

    def OnPaint(self, e):
        if not self.init_on_paint():
            return

        start = time.time()
        self.needle_density_info.calculate_distance_up_to_current_point(
            self.current_stitch, self.distance_search)
        self.output_needle_points_up_to_current_point()
        last_stitch = self.needle_density_info.last_calculated_stitch()
        self.last_frame_duration = time.time() - start
        self.handle_last_painted_stitch(last_stitch)


class NeedleDistanceSimulatorPanel(BaseSimulatorPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseSimulatorPanel.__init__(self, parent, *args, **kwargs)
        self.cp = NeedleDistanceControlPanel(self,
                                             stitch_plan=self.stitch_plan,
                                             stitches_per_second=self.stitches_per_second,
                                             target_duration=self.target_duration)
        self.dp = NeedleDistanceDrawingPanel(self, stitch_plan=self.stitch_plan, control_panel=self.cp)
        self.FinaliseInit()


class NeedleDistanceSimulator(BaseSimulator):
    def __init__(self, *args, **kwargs):
        BaseSimulator.__init__(self, *args, **kwargs)
        needle_simulator_panel = NeedleDistanceSimulatorPanel(self,
                                                              stitch_plan=self.stitch_plan,
                                                              target_duration=self.target_duration,
                                                              stitches_per_second=self.stitches_per_second)
        self.link_simulator_panel(needle_simulator_panel)
        self.secure_minimum_size()


class NeedleDistanceSimulatorPreview(BaseSimulatorPreview):
    """Manages a preview simulation and a background thread for generating patches."""
    def __init__(self, parent, *args, **kwargs):
        BaseSimulatorPreview.__init__(self, self, parent, *args, **kwargs)


def needle_distance_simulator_main():
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    show_simulator(NeedleDistanceSimulator, "Needle Distance Simulation", stitch_plan)


if __name__ == "__main__":
    needle_distance_simulator_main()
