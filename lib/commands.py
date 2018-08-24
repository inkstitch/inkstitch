import sys
import inkex
import cubicsuperpath
import simpletransform

from .svg import apply_transforms, get_node_transform
from .svg.tags import SVG_USE_TAG, SVG_SYMBOL_TAG, CONNECTION_START, CONNECTION_END, XLINK_HREF
from .utils import cache, Point
from .i18n import _, N_

COMMANDS = {
    # L10N command attached to an object
    N_("fill_start"): N_("Fill stitch starting position"),

    # L10N command attached to an object
    N_("fill_end"): N_("Fill stitch ending position"),

    # L10N command attached to an object
    N_("stop"): N_("Stop (pause machine) after sewing this object"),

    # L10N command attached to an object
    N_("trim"): N_("Trim thread after sewing this object"),

    # L10N command attached to an object
    N_("ignore_object"): N_("Ignore this object (do not stitch)"),

    # L10N command that affects a layer
    N_("ignore_layer"): N_("Ignore layer (do not stitch any objects in this layer)"),

    # L10N command that affects entire document
    N_("origin"): N_("Origin for exported embroidery files"),

    # L10N command that affects entire document
    N_("stop_position"): N_("Jump destination for Stop commands (a.k.a. \"Frame Out position\")."),
}

OBJECT_COMMANDS = ["fill_start", "fill_end", "stop", "trim", "ignore_object"]
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
        path = cubicsuperpath.parsePath(self.connector.get('d'))
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
        simpletransform.applyTransformToPoint(transform, pos)

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
        print >> sys.stderr, _("Error: there is more than one %(command)s command in the document, but there can only be one.  "
                               "Please remove all but one.") % dict(command=command)

        # L10N This is a continuation of the previous error message, letting the user know
        # what command we're talking about since we don't normally expose the actual
        # command name to them.  Contents of %(description)s are in a separate translation
        # string.
        print >> sys.stderr, _("%(command)s: %(description)s") % dict(command=command, description=_(get_command_description(command)))

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
