import sys
import time
import wx

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


def embroidery_simulator_main():
    stitch_plan = stitch_plan_from_file(sys.argv[1])
    app = wx.App()
    current_screen = wx.Display.GetFromPoint(wx.GetMousePosition())
    display = wx.Display(current_screen)
    screen_rect = display.GetClientArea()

    simulator_pos = (screen_rect[0], screen_rect[1])

    # subtract 1 because otherwise the window becomes maximized on Linux
    width = screen_rect[2] - 1
    height = screen_rect[3] - 1

    frame = EmbroiderySimulator(None, -1, "Embroidery Simulation", pos=simulator_pos, size=(width, height),
                                stitch_plan=stitch_plan)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
    app.__del__()


if __name__ == "__main__":
    embroidery_simulator_main()
    # time.sleep(5)
    # sys.exit()
    # TODO how to ensure all classes actually closes and nothing remains active? Above two lines show that
    #  stitch_plan remains active after 5 seconds.
