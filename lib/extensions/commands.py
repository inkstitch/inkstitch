import os
import sys
import inkex
import simpletransform
import cubicsuperpath
from copy import deepcopy
from random import random
from shapely import geometry as shgeo

from .base import InkstitchExtension
from ..i18n import _
from ..elements import SatinColumn
from ..utils import get_bundled_dir, cache
from ..svg.tags import SVG_DEFS_TAG, SVG_GROUP_TAG, SVG_USE_TAG, SVG_PATH_TAG, INKSCAPE_GROUPMODE, XLINK_HREF, CONNECTION_START, CONNECTION_END, CONNECTOR_TYPE
from ..svg import get_node_transform


class Commands(InkstitchExtension):
    COMMANDS = ["fill_start", "fill_end", "stop", "trim", "ignore"]

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

    def get_correction_transform(self, node):
        # if we want to place our new nodes in the same group as this node,
        # then we'll need to factor in the effects of any transforms set on
        # the parents of this node.

        # we can ignore the transform on the node itself since it won't apply
        # to the objects we add
        transform = get_node_transform(node.getparent())

        # now invert it, so that we can position our objects in absolute
        # coordinates
        transform = simpletransform.invertTransform(transform)

        return simpletransform.formatTransform(transform)

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
                "transform": self.get_correction_transform(symbol),
                CONNECTION_START: "#%s" % symbol.get('id'),
                CONNECTION_END: "#%s" % element.node.get('id'),
                CONNECTOR_TYPE: "polyline",
            }
        )

        symbol.getparent().insert(symbol.getparent().index(symbol), path)

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

    def add_command(self, element, commands):
        for i, command in enumerate(commands):
            self.remove_legacy_param(element, command)

            pos = self.get_command_pos(element, i, len(commands))

            symbol = inkex.etree.SubElement(element.node.getparent(), SVG_USE_TAG,
                {
                    "id": self.uniqueId("use"),
                    XLINK_HREF: "#inkstitch_%s" % command,
                    "height": "100%",
                    "width": "100%",
                    "x": str(pos.x),
                    "y": str(pos.y),
                    "transform": self.get_correction_transform(element.node)
                }
            )

            self.add_connector(symbol, element)

    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more objects to which to attach commands."))
            return

        self.svg = self.document.getroot()

        commands = [command for command in self.COMMANDS if getattr(self.options, command)]

        if not commands:
            inkex.errormsg(_("Please choose one or more commands to attach."))
            return

        for command in commands:
            self.ensure_symbol(command)

        # Each object (node) in the SVG may correspond to multiple Elements of different
        # types (e.g. stroke + fill).  We only want to process each one once.
        seen_nodes = set()

        for element in self.elements:
            if element.node not in seen_nodes:
                self.add_command(element, commands)
                seen_nodes.add(element.node)
