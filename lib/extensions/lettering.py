import os

from ..i18n import _
from ..lettering import Font
from ..utils import get_resource_dir

from .base import InkstitchExtension


class Lettering(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.OptionParser.add_option("-t", "--text")

    def effect(self):
        font_path = os.path.join(get_resource_dir("fonts"), "small_font")
        font = Font(font_path)
        self.current_layer.extend(font.render_text(self.options.text))
