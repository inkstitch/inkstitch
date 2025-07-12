import wx
import skia
from wx import glcanvas
from ..renderer.renderer import render

from .base import InkstitchExtension

try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

try:
    # The Python OpenGL package can be found at
    # http://PyOpenGL.sourceforge.net/
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

class HardwarePanel(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.context = skia.GrContext.MakeGL(skia.GrGLInterface.MakeEGL())
        self.surface = None
    
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

        fbinfo = skia.GrGLFramebufferInfo(0, GL_RGBA8)
        stencildepth = 0
        rendertarget = skia.GrBackendRenderTarget.MakeGL(size.width, size.height, 0, stencildepth, fbinfo)
        self.surface = skia.Surface.MakeFromBackendRenderTarget(
            self.context, 
            rendertarget, 
            skia.GrSurfaceOrigin.kTopLeft_GrSurfaceOrigin, 
            skia.ColorType.kRGBA_8888_ColorType,
            None, None)

        assert self.surface is not None
        self.canvas = self.surface.getCanvas()


    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)

        render(self.context, self.canvas)

        self.context.flush()

        self.SwapBuffers()


class RenderWxOgl(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        app = wx.App()
        frame = wx.Frame()
        frame.Panel = HardwarePanel(frame)
            
        app.SetTopWindow(frame)
        frame.Show()
        app.MainLoop()
