import wx
import skia
from wx import glcanvas
from ..renderer.renderer import render
from inkex import BaseElement, Boolean, Group, errormsg

from .base import InkstitchExtension

class SoftwarePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.surface = None

    def OnPaint(self, event):
        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)
        gc.Clear()

        size = gc.GetSize()
        if self.surface is None or self.surface.width() != size.width or self.surface.height() != size.height:
            self.surface = skia.Surface(size.width, size.height)

        canvas = self.surface.getCanvas()

        render(None, canvas)

        # no need to flush a software canvas.

        image = self.surface.makeImageSnapshot()

        # Todo: Come up with a better option for copying the bitmap if possible. It might not be.
        gc.DrawBitmap(wx.Bitmap.FromBufferRGBA(image.width(), image.height(), image.tobytes()), 0, 0, False)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.Panel = SoftwarePanel(self)

class RenderWx(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):

        app = wx.App()
        frame = MyFrame(None, title="Sample_one", size=(380, 750))
        app.SetTopWindow(frame)
        frame.Show(True)
        app.MainLoop()
