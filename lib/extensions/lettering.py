import os

from ..lettering import Font
from ..stitches.auto_satin import auto_satin
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

        lines = font.render_text(self.options.text)
        for line in lines:
            # they need to be SatinColumns
            elements, trim_indices = auto_satin(line, preserve_order=True)
            del line[:]
            for element in elements:
                line.append(element.node)

        self.current_layer.extend(lines)
