import os

from ..lettering import Font
from ..svg.tags import SVG_PATH_TAG, SVG_GROUP_TAG, INKSCAPE_LABEL
from ..utils import get_resource_dir
from .commands import CommandsExtension


class Lettering(CommandsExtension):
    COMMANDS = ["trim"]

    def __init__(self, *args, **kwargs):
        CommandsExtension.__init__(self, *args, **kwargs)

        self.OptionParser.add_option("-t", "--text")

    def effect(self):
        font_path = os.path.join(get_resource_dir("fonts"), "small_font")
        font = Font(font_path)
        self.ensure_current_layer()

        lines = font.render_text(self.options.text.decode('utf-8'))
        self.set_labels(lines)
        self.current_layer.append(lines)

    def set_labels(self, lines):
        path = 1
        for node in lines.iterdescendants():
            if node.tag == SVG_PATH_TAG:
                node.set("id", self.uniqueId("lettering"))

                # L10N Label for an object created by the Lettering extension
                node.set(INKSCAPE_LABEL, _("Lettering %d") % path)
                path += 1
            elif node.tag == SVG_GROUP_TAG:
                node.set("id", self.uniqueId("letteringline"))

                # lettering extension already set the label