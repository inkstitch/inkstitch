import inkex

from ..commands import LAYER_COMMANDS, get_command_description, ensure_symbol
from ..i18n import _
from ..svg import get_correction_transform
from ..svg.tags import SVG_USE_TAG, INKSCAPE_LABEL, XLINK_HREF
from .commands import CommandsExtension


class LayerCommands(CommandsExtension):
    COMMANDS = LAYER_COMMANDS

    def effect(self):
        commands = [command for command in self.COMMANDS if getattr(self.options, command)]

        if not commands:
            inkex.errormsg(_("Please choose one or more commands to add."))
            return

        self.ensure_current_layer()
        correction_transform = get_correction_transform(self.current_layer, child=True)

        for i, command in enumerate(commands):
            ensure_symbol(self.document, command)

            inkex.etree.SubElement(self.current_layer, SVG_USE_TAG,
                                   {
                                       "id": self.uniqueId("use"),
                                       INKSCAPE_LABEL: _("Ink/Stitch Command") + ": %s" % get_command_description(command),
                                       XLINK_HREF: "#inkstitch_%s" % command,
                                       "height": "100%",
                                       "width": "100%",
                                       "x": str(i * 20),
                                       "y": "-10",
                                       "transform": correction_transform
                                   })
