import skia
from inkex import BaseElement, Boolean, Group, errormsg

from .base import InkstitchExtension

from OpenGL.GL import *
from OpenGL.GLUT import *

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
import skia
from OpenGL.GL import *
from OpenGL.GL import shaders

from ..renderer.renderer import render


TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="example1" parent="GtkApplicationWindow">
    <child>
      <object class="GtkPaned" id="pane">
        <property name="shrink-start-child">false</property>
        <property name="start-child">
          <object class="GtkScrolledWindow" id="foo">
            <property name="min-content-width">200</property>
            <property name="width-request">200</property>
            <property name="hexpand">true</property>
            <property name="hscrollbar-policy">2</property>
            <child>
              <object class="GtkBox">
                <property name="hexpand">true</property>
                <property name="orientation">1</property>
                <child>
                  <object class="GtkLabel">
                    <property name="label" translatable="yes">foo</property>
                    <property name="hexpand">true</property>
                  </object>
                </child>
                <child>
                  <object class="GtkButton">
                    <property name="label" translatable="yes">bar</property>
                    <property name="hexpand">true</property>
                  </object>
                </child>
                <child>
                  <object class="GtkSpinButton" id="spinner">
                    <property name="digits">3</property>
                    <property name="value">100</property>
                    <property name="hexpand">true</property>
                  </object>
                </child>
              </object>
            </child>
          </object>
        </property>
        <property name="end-child">
          <object class="MyGLArea" id="area">
            <property name="hexpand">true</property>
            <property name="vexpand">true</property>
            <property name="width-request">400</property>
            <property name="height-request">400</property>
          </object>
        </property>
      </object>
    </child>
  </template>
</interface>
'''

class MyGLArea(Gtk.GLArea):
    __gtype_name__ = "MyGLArea"

    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)

    def on_realize(self, area):
        ctx = self.get_context()
        ctx.make_current()

        self.context = skia.GrContext.MakeGL(skia.GrGLInterface.MakeEGL())
        self.surface = None
        print("realized", ctx)

    def on_render(self, area, ctx):
        ctx.make_current()

        width = self.get_width()
        height = self.get_height()
        if self.surface is None or self.surface.width() != width or self.surface.height() != height:
          fbbinding = glGetInteger(GL_FRAMEBUFFER_BINDING)
          stencilid = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_STENCIL_ATTACHMENT, GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME)
          stencildepth = 0
          if stencilid != 0:
              glBindRenderbuffer(GL_RENDERBUFFER, stencilid)
              stencildepth = glGetRenderbufferParameteriv(GL_RENDERBUFFER, GL_RENDERBUFFER_STENCIL_SIZE)

          # colortype = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE)
          # rsz = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE)
          # gsz = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE)
          # bsz = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE)
          # asz = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE)
          # asz = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE)
          # lvl = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL)
          # name = glGetFramebufferAttachmentParameteriv(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME)
          # print(f"color {colortype == GL_TEXTURE} {name} {rsz} {gsz} {bsz} {asz} {stencildepth}")

          # Makes a hardcoded assumption about the pixel format that is true for OpenGL, maybe not GLES?
          fbinfo = skia.GrGLFramebufferInfo(fbbinding, GL_RGBA8)
          rendertarget = skia.GrBackendRenderTarget.MakeGL(width, height, 0, stencildepth, fbinfo)
          self.surface = skia.Surface.MakeFromBackendRenderTarget(
              self.context, 
              rendertarget, 
              skia.GrSurfaceOrigin.kTopLeft_GrSurfaceOrigin, 
              skia.ColorType.kRGBA_8888_ColorType,
              None, None)

          assert self.surface is not None
          self.canvas = self.surface.getCanvas()

        render(self.context, self.canvas) 

        self.context.flush()

        return True

@Gtk.Template(string=TEMPLATE)
class RootWidget(Gtk.ApplicationWindow):
    __gtype_name__ = "example1"
    
    # area = Gtk.Template.Child("area")
    # pane = Gtk.Template.Child("pane")
    spinner = Gtk.Template.Child("spinner")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spinner.set_range(0, 100)
        self.spinner.set_increments(1, 10)


class RenderGtk(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        def on_activate(app):
            win = RootWidget(application=app)
            win.present()

        # Create a new application
        app = Gtk.Application(application_id='com.example.GtkApplication')
        app.connect('activate', on_activate)

        # Run the application
        app.run(None)