import wx

from .base import InkstitchExtension
from ..i18n import _
from ..simulator import EmbroiderySimulator
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
        app = wx.App()
        frame = EmbroiderySimulator(None, -1, _("Embroidery Simulation"), wx.DefaultPosition, size=(1000, 1000), stitch_plan=stitch_plan)
        app.SetTopWindow(frame)
        frame.Show()
        wx.CallAfter(frame.go)
        app.MainLoop()
