import sys

from ..stitch_plan import stitch_plan_from_file

from ..gui.generic_simulator import show_simulator, BaseSimulator, BaseSimulatorPanel, BaseControlPanel, \
    BaseDrawingPanel, BaseSimulatorPreview
# TODO possibly change import to go via init.py in gui?


class EmbroideryControlPanel(BaseControlPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseControlPanel.__init__(self, parent, *args, **kwargs)


class EmbroideryDrawingPanel(BaseDrawingPanel):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        self.np_needle_points = None
        BaseDrawingPanel.__init__(self, *args, **kwargs)


class EmbroiderySimulatorPanel(BaseSimulatorPanel):
    """"""

    def __init__(self, parent, *args, **kwargs):
        """"""
        BaseSimulatorPanel.__init__(self, parent, *args, **kwargs)
        self.cp = EmbroideryControlPanel(self,
                                         stitch_plan=self.stitch_plan,
                                         stitches_per_second=self.stitches_per_second,
                                         target_duration=self.target_duration)
        self.dp = EmbroideryDrawingPanel(self, stitch_plan=self.stitch_plan, control_panel=self.cp)
        self.FinaliseInit()


class EmbroiderySimulator(BaseSimulator):
    def __init__(self, *args, **kwargs):
        BaseSimulator.__init__(self, *args, **kwargs)
        needle_simulator_panel = EmbroiderySimulatorPanel(self,
                                                          stitch_plan=self.stitch_plan,
                                                          target_duration=self.target_duration,
                                                          stitches_per_second=self.stitches_per_second)
        self.link_simulator_panel(needle_simulator_panel)
        self.secure_minimum_size()


class SimulatorPreview(BaseSimulatorPreview):
    """Manages a preview simulation and a background thread for generating patches."""
    def __init__(self, parent, *args, **kwargs):
        BaseSimulatorPreview.__init__(self, self, parent, *args, **kwargs)
        # TODO this should be working from params (and lettering)...


def embroidery_simulator_main():
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    show_simulator(EmbroiderySimulator,  "Embroidery Simulation", stitch_plan)


if __name__ == "__main__":
    embroidery_simulator_main()
