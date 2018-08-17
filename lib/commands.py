import inkex
import cubicsuperpath

from .svg import apply_transforms
from .svg.tags import SVG_USE_TAG, SVG_SYMBOL_TAG, CONNECTION_START, CONNECTION_END, XLINK_HREF


class CommandParseError(Exception):
    pass


class BaseCommand(object):
    def parse_symbol(self):
        if self.symbol.tag != SVG_SYMBOL_TAG:
            raise CommandParseError("use points to non-symbol")

        self.command = self.symbol.get('id')

        if self.command.startswith('inkstitch_'):
            self.command = self.command[10:]
        else:
            raise CommandParseError("symbol is not an Ink/Stitch command")

    def get_node_by_url(self,url):
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

    commands = []

    for standalone_command in standalone_commands(layer.getroottree().getroot()):
        if standalone_command.command == command:
            if layer in standalone_command.node.iterancestors():
                commands.append(command)

    return commands

def standalone_commands(svg):
    """Find all unconnected command symbols in the SVG."""

    xpath = ".//svg:use[starts-with(@xlink:href, '#inkstitch_')]"
    symbols = svg.xpath(xpath, namespaces=inkex.NSS)

    commands = []
    for symbol in symbols:
        try:
            commands.append(StandaloneCommand(symbol))
        except CommandParseError:
            pass

    return commands

def is_command(node):
    return CONNECTION_START in node.attrib or CONNECTION_END in node.attrib
