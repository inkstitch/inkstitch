import os
import sys
from copy import deepcopy
from random import random

import inkex
from lxml import etree
from shapely import geometry as shgeo

from .i18n import N_, _
from .svg import (apply_transforms, generate_unique_id,
                  get_correction_transform, get_document, get_node_transform)
from .svg.tags import (CONNECTION_END, CONNECTION_START, CONNECTOR_TYPE,
                       INKSCAPE_LABEL, INKSTITCH_ATTRIBS, SVG_DEFS_TAG,
                       SVG_GROUP_TAG, SVG_PATH_TAG, SVG_SYMBOL_TAG,
                       SVG_USE_TAG, XLINK_HREF)
from .utils import Point, cache, get_bundled_dir

COMMANDS = {
    # L10N command attached to an object
    "fill_start": N_("Fill stitch starting position"),

    # L10N command attached to an object
    "fill_end": N_("Fill stitch ending position"),

    # L10N command attached to an object
    "satin_start": N_("Auto-route satin stitch starting position"),

    # L10N command attached to an object
    "satin_end": N_("Auto-route satin stitch ending position"),

    # L10N command attached to an object
    "stop": N_("Stop (pause machine) after sewing this object"),

    # L10N command attached to an object
    "trim": N_("Trim thread after sewing this object"),

    # L10N command attached to an object
    "ignore_object": N_("Ignore this object (do not stitch)"),

    # L10N command attached to an object
    "satin_cut_point": N_("Satin cut point (use with Cut Satin Column)"),


    # L10N command that affects a layer
    "ignore_layer": N_("Ignore layer (do not stitch any objects in this layer)"),

    # L10N command that affects entire document
    "origin": N_("Origin for exported embroidery files"),

    # L10N command that affects entire document
    "stop_position": N_("Jump destination for Stop commands (a.k.a. \"Frame Out position\")."),
}

OBJECT_COMMANDS = ["fill_start", "fill_end", "satin_start", "satin_end", "stop", "trim", "ignore_object", "satin_cut_point"]
LAYER_COMMANDS = ["ignore_layer"]
GLOBAL_COMMANDS = ["origin", "stop_position"]


class CommandParseError(Exception):
    pass


class BaseCommand(object):
    @property
    @cache
    def description(self):
        return get_command_description(self.command)

    def parse_symbol(self):
        if self.symbol.tag != SVG_SYMBOL_TAG:
            raise CommandParseError("use points to non-symbol")

        self.command = self.symbol.get('id')

        if self.command.startswith('inkstitch_'):
            self.command = self.command[10:]
        else:
            raise CommandParseError("symbol is not an Ink/Stitch command")

    def get_node_by_url(self, url):
        # url will be #path12345.  Find the corresponding object.
        if url is None:
            raise CommandParseError("url is None")

        if not url.startswith('#'):
            raise CommandParseError("invalid connection url: %s" % url)

        id = url[1:]

        try:
            return self.svg.xpath(".//*[@id='%s']" % id)[0]
        except (IndexError, AttributeError):
            raise CommandParseError("could not find node by url %s" % id)


class Command(BaseCommand):
    def __init__(self, connector):
        self.connector = connector
        self.svg = self.connector.getroottree().getroot()

        self.parse_command()

    def parse_connector_path(self):
        path = inkex.paths.Path(self.connector.get('d')).to_superpath()
        return apply_transforms(path, self.connector)

    def parse_command(self):
        path = self.parse_connector_path()

        neighbors = [
            (self.get_node_by_url(self.connector.get(CONNECTION_START)), path[0][0][1]),
            (self.get_node_by_url(self.connector.get(CONNECTION_END)), path[0][-1][1])
        ]

        if neighbors[0][0].tag != SVG_USE_TAG:
            neighbors.reverse()

        if neighbors[0][0].tag != SVG_USE_TAG:
            raise CommandParseError("connector does not point to a use tag")

        self.use = neighbors[0][0]

        self.symbol = self.get_node_by_url(neighbors[0][0].get(XLINK_HREF))
        self.parse_symbol()

        self.target = neighbors[1][0]
        self.target_point = neighbors[1][1]

    def __repr__(self):
        return "Command('%s', %s)" % (self.command, self.target_point)


class StandaloneCommand(BaseCommand):
    def __init__(self, use):
        self.node = use
        self.svg = self.node.getroottree().getroot()

        self.parse_command()

    def parse_command(self):
        self.symbol = self.get_node_by_url(self.node.get(XLINK_HREF))

        if self.symbol.tag != SVG_SYMBOL_TAG:
            raise CommandParseError("use points to non-symbol")

        self.parse_symbol()

    @property
    @cache
    def point(self):
        pos = [float(self.node.get("x", 0)), float(self.node.get("y", 0))]
        transform = get_node_transform(self.node)
        pos = inkex.transforms.Transform(transform).apply_to_point(pos)

        return Point(*pos)


def get_command_description(command):
    return COMMANDS[command]


def find_commands(node):
    """Find the symbols this node is connected to and return them as Commands"""

    # find all paths that have this object as a connection
    xpath = ".//*[@inkscape:connection-start='#%(id)s' or @inkscape:connection-end='#%(id)s']" % dict(id=node.get('id'))
    connectors = node.getroottree().getroot().xpath(xpath, namespaces=inkex.NSS)

    # try to turn them into commands
    commands = []
    for connector in connectors:
        try:
            commands.append(Command(connector))
        except CommandParseError:
            # Parsing the connector failed, meaning it's not actually an Ink/Stitch command.
            pass

    return commands


def layer_commands(layer, command):
    """Find standalone (unconnected) command symbols in this layer."""

    for global_command in global_commands(layer.getroottree().getroot(), command):
        if layer in global_command.node.iterancestors():
            yield global_command


def global_commands(svg, command):
    """Find standalone (unconnected) command symbols anywhere in the document."""

    for standalone_command in _standalone_commands(svg):
        if standalone_command.command == command:
            yield standalone_command


@cache
def global_command(svg, command):
    """Find a single command of the specified type.

    If more than one is found, print an error and exit.
    """

    commands = list(global_commands(svg, command))

    if len(commands) == 1:
        return commands[0]
    elif len(commands) > 1:
        print(_("Error: there is more than one %(command)s command in the document, but there can only be one.  "
                "Please remove all but one.") % dict(command=command), file=sys.stderr)

        # L10N This is a continuation of the previous error message, letting the user know
        # what command we're talking about since we don't normally expose the actual
        # command name to them.  Contents of %(description)s are in a separate translation
        # string.
        print(_("%(command)s: %(description)s") % dict(command=command, description=_(get_command_description(command))), file=sys.stderr)

        sys.exit(1)
    else:
        return None


def _standalone_commands(svg):
    """Find all unconnected command symbols in the SVG."""

    xpath = ".//svg:use[starts-with(@xlink:href, '#inkstitch_')]"
    symbols = svg.xpath(xpath, namespaces=inkex.NSS)

    for symbol in symbols:
        try:
            yield StandaloneCommand(symbol)
        except CommandParseError:
            pass


def is_command(node):
    return CONNECTION_START in node.attrib or CONNECTION_END in node.attrib


def is_command_symbol(node):
    symbol = None
    xlink = node.get(XLINK_HREF, "")
    if xlink.startswith("#inkstitch_"):
        symbol = node.get(XLINK_HREF)[11:]
    return symbol in COMMANDS


@cache
def symbols_path():
    return os.path.join(get_bundled_dir("symbols"), "inkstitch.svg")


@cache
def symbols_svg():
    with open(symbols_path()) as symbols_file:
        return etree.parse(symbols_file)


@cache
def symbol_defs():
    return get_defs(symbols_svg())


@cache
def get_defs(document):
    defs = document.find(SVG_DEFS_TAG)

    if defs is None:
        defs = etree.SubElement(document, SVG_DEFS_TAG)

    return defs


def ensure_symbol(document, command):
    """Make sure the command's symbol definition exists in the <svg:defs> tag."""

    path = "./*[@id='inkstitch_%s']" % command
    defs = get_defs(document)
    if defs.find(path) is None:
        defs.append(deepcopy(symbol_defs().find(path)))


def add_group(document, node, command):
    return etree.SubElement(
        node.getparent(),
        SVG_GROUP_TAG,
        {
            "id": generate_unique_id(document, "command_group"),
            INKSCAPE_LABEL: _("Ink/Stitch Command") + ": %s" % get_command_description(command),
            "transform": get_correction_transform(node)
        })


def add_connector(document, symbol, element):
    # I'd like it if I could position the connector endpoint nicely but inkscape just
    # moves it to the element's center immediately after the extension runs.
    start_pos = (symbol.get('x'), symbol.get('y'))
    end_pos = element.shape.centroid

    # Make sure the element's XML node has an id so that we can reference it.
    if element.node.get('id') is None:
        element.node.set('id', generate_unique_id(document, "object"))

    path = etree.Element(SVG_PATH_TAG,
                         {
                          "id": generate_unique_id(document, "command_connector"),
                          "d": "M %s,%s %s,%s" % (start_pos[0], start_pos[1], end_pos.x, end_pos.y),
                          "style": "stroke:#000000;stroke-width:1px;stroke-opacity:0.5;fill:none;",
                          CONNECTION_START: "#%s" % symbol.get('id'),
                          CONNECTION_END: "#%s" % element.node.get('id'),
                          CONNECTOR_TYPE: "polyline",

                          # l10n: the name of the line that connects a command to the object it applies to
                          INKSCAPE_LABEL: _("connector")
                         })

    symbol.getparent().insert(0, path)


def add_symbol(document, group, command, pos):
    return etree.SubElement(group, SVG_USE_TAG,
                            {
                             "id": generate_unique_id(document, "command_use"),
                             XLINK_HREF: "#inkstitch_%s" % command,
                             "height": "100%",
                             "width": "100%",
                             "x": str(pos.x),
                             "y": str(pos.y),

                             # l10n: the name of a command symbol (example: scissors icon for trim command)
                             INKSCAPE_LABEL: _("command marker"),
                            })


def get_command_pos(element, index, total):
    # Put command symbols 30 pixels out from the shape, spaced evenly around it.

    # get a line running 30 pixels out from the shape
    outline = element.shape.buffer(30).exterior

    # find the top center point on the outline and start there
    top_center = shgeo.Point(outline.centroid.x, outline.bounds[1])
    start_position = outline.project(top_center, normalized=True)

    # pick this item's spot around the outline and perturb it a bit to avoid
    # stacking up commands if they add commands multiple times
    position = index / float(total)
    position += random() * 0.05
    position += start_position

    return outline.interpolate(position, normalized=True)


def remove_legacy_param(element, command):
    if command == "trim" or command == "stop":
        # If they had the old "TRIM after" or "STOP after" attributes set,
        # automatically delete them.  The new commands will do the same
        # thing.
        #
        # If we didn't delete these here, then things would get confusing.
        # If the user were to delete a "trim" symbol added by this extension
        # but the "embroider_trim_after" attribute is still set, then the
        # trim would keep happening.

        attribute = "embroider_%s_after" % command

        if attribute in element.node.attrib:
            del element.node.attrib[attribute]

        # Attributes have changed to be namespaced.
        # Let's check for them as well, they might have automatically changed.
        attribute = INKSTITCH_ATTRIBS["%s_after" % command]

        if attribute in element.node.attrib:
            del element.node.attrib[attribute]


def add_commands(element, commands):
    document = get_document(element.node)

    for i, command in enumerate(commands):
        ensure_symbol(document, command)
        remove_legacy_param(element, command)

        group = add_group(document, element.node, command)
        pos = get_command_pos(element, i, len(commands))
        symbol = add_symbol(document, group, command, pos)
        add_connector(document, symbol, element)


def add_layer_commands(layer, commands):
    document = get_document(layer)
    correction_transform = get_correction_transform(layer)

    for command in commands:
        ensure_symbol(document, command)
        etree.SubElement(layer, SVG_USE_TAG,
                         {
                          "id": generate_unique_id(document, "use"),
                          INKSCAPE_LABEL: _("Ink/Stitch Command") + ": %s" % get_command_description(command),
                          XLINK_HREF: "#inkstitch_%s" % command,
                          "height": "100%",
                          "width": "100%",
                          "x": "0",
                          "y": "-10",
                          "transform": correction_transform
                         })
