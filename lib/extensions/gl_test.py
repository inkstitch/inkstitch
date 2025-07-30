from .base import InkstitchExtension
from ..stitch_plan import stitch_groups_to_stitch_plan

class GlTest(InkstitchExtension):
    def effect(self):
        if not self.get_elements():
            return
        # import os
        # os.environ["GTK_DEBUG"] = "all"

        import gi

        gi.require_version('Gtk', '4.0')
        from gi.repository import Gtk, Gdk
        from ..gui.experimental.testgtk import RenderWindow

        metadata = self.get_inkstitch_metadata()
        collapse_len = metadata['collapse_len_mm']
        min_stitch_len = metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)

        def on_activate(app):
            win = RenderWindow(application=app)
            win.set_stitch_plan(stitch_plan)
            win.present()

        # Create a new application
        app = Gtk.Application(application_id='org.inkstitch.test')
        app.connect('activate', on_activate)

        app.run()