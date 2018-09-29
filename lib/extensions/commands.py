import os
import inkex
from copy import deepcopy
from random import random


from .base import InkstitchExtension
from ..utils import get_bundled_dir, cache
from ..commands import get_command_description
from ..i18n import _
from ..svg.tags import SVG_DEFS_TAG, SVG_PATH_TAG, CONNECTION_START, CONNECTION_END, \
                       CONNECTOR_TYPE, INKSCAPE_LABEL, SVG_GROUP_TAG, SVG_USE_TAG, XLINK_HREF
from ..svg import get_correction_transform


class CommandsExtension(InkstitchExtension):
    """Base class for extensions that manipulate commands."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        for command in self.COMMANDS:
            self.OptionParser.add_option("--%s" % command, type="inkbool")

    @property
    def symbols_path(self):
        return os.path.join(get_bundled_dir("symbols"), "inkstitch.svg")

    @property
    @cache
    def symbols_svg(self):
        with open(self.symbols_path) as symbols_file:
            return inkex.etree.parse(symbols_file)

    @property
    @cache
    def symbol_defs(self):
        return self.symbols_svg.find(SVG_DEFS_TAG)

    @property
    @cache
    def defs(self):
        return self.document.find(SVG_DEFS_TAG)

    def ensure_symbol(self, command):
        path = "./*[@id='inkstitch_%s']" % command
        if self.defs.find(path) is None:
            self.defs.append(deepcopy(self.symbol_defs.find(path)))

    def add_connector(self, symbol, element):
        # I'd like it if I could position the connector endpoint nicely but inkscape just
        # moves it to the element's center immediately after the extension runs.
        start_pos = (symbol.get('x'), symbol.get('y'))
        end_pos = element.shape.centroid

        path = inkex.etree.Element(SVG_PATH_TAG,
                                   {
                                       "id": self.uniqueId("connector"),
                                       "d": "M %s,%s %s,%s" % (start_pos[0], start_pos[1], end_pos.x, end_pos.y),
                                       "style": "stroke:#000000;stroke-width:1px;stroke-opacity:0.5;fill:none;",
                                       CONNECTION_START: "#%s" % symbol.get('id'),
                                       CONNECTION_END: "#%s" % element.node.get('id'),
                                       CONNECTOR_TYPE: "polyline",

                                       # l10n: the name of the line that connects a command to the object it applies to
                                       INKSCAPE_LABEL: _("connector")
                                   }
                                   )

        symbol.getparent().insert(0, path)

    def get_command_pos(self, element, index, total):
        # Put command symbols 30 pixels out from the shape, spaced evenly around it.

        # get a line running 30 pixels out from the shape
        outline = element.shape.buffer(30).exterior

        # pick this item's spot arond the outline and perturb it a bit to avoid
        # stacking up commands if they run the extension multiple times
        position = index / float(total)
        position += random() * 0.1

        return outline.interpolate(position, normalized=True)

    def remove_legacy_param(self, element, command):
        if command == "trim" or command == "stop":
            # If they had the old "TRIM after" or "STOP after" attributes set,
            # automatically delete them.  THe new commands will do the same
            # thing.
            #
            # If we didn't delete these here, then things would get confusing.
            # If the user were to delete a "trim" symbol added by this extension
            # but the "embroider_trim_after" attribute is still set, then the
            # trim would keep happening.

            attribute = "embroider_%s_after" % command

            if attribute in element.node.attrib:
                del element.node.attrib[attribute]

    def add_commands(self, element, commands):
        for i, command in enumerate(commands):
            self.remove_legacy_param(element, command)

            pos = self.get_command_pos(element, i, len(commands))

            group = inkex.etree.SubElement(element.node.getparent(), SVG_GROUP_TAG,
                                           {
                "id": self.uniqueId("group"),
                INKSCAPE_LABEL: _("Ink/Stitch Command") + ": %s" % get_command_description(command),
                "transform": get_correction_transform(element.node)
            }
            )

            symbol = inkex.etree.SubElement(group, SVG_USE_TAG,
                                            {
                                                "id": self.uniqueId("use"),
                                                XLINK_HREF: "#inkstitch_%s" % command,
                                                "height": "100%",
                                                "width": "100%",
                                                "x": str(pos.x),
                                                "y": str(pos.y),

                                                # l10n: the name of a command symbol (example: scissors icon for trim command)
                                                INKSCAPE_LABEL: _("command marker"),
                                            }
                                            )

            self.add_connector(symbol, element)
