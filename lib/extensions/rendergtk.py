from inkex import BaseElement, Boolean, Group, errormsg

from .base import InkstitchExtension


class RenderGtk(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        # Importing GI breaks wxwidgets somehow, it makes wx.App() hang. Why??
        from ..gui.gtktest import RootWidget

        import gi
        gi.require_version('Gtk', '4.0')
        from gi.repository import Gtk, Gdk

        def on_activate(app):
            win = RootWidget(application=app)
            win.present()

        # Create a new application
        app = Gtk.Application(application_id='com.example.inkstitchtest')
        app.connect('activate', on_activate)

        # Run the application
        app.run(None)