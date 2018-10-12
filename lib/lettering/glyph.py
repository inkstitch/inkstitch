import cubicsuperpath
import simpletransform
from copy import copy

from ..svg import apply_transforms, get_guides
from ..svg.tags import INKSCAPE_LABEL
from ..utils import cache


class Glyph(object):
    """Represents a single character in a single font variant.

    For example, the font inkstitch_small may have variants for left-to-right,
    right-to-left, etc.  Each variant would have a set of Glyphs, one for each
    character in that variant.

    Properties:
      width -- total width of this glyph including all component satins
      nodes -- SVG path nodes of the component satins in this character
    """

    def __init__(self, nodes):
        """Create a Glyph.

        The nodes will be copied out of their parent SVG document (with nested
        transforms applied).  The original nodes will be unmodified.

        Arguments:
          nodes -- an iterable of XML nodes
        """
        self.nodes = []

        self._process_nodes(nodes)
        self._process_bbox()
        self._move_to_origin()

    def _process_nodes(self, nodes):
        self.baseline = None

        for node in nodes:
            if self.baseline is None:
                self._process_baseline(node.getroottree().getroot())

            node_copy = copy(node)
            path = cubicsuperpath.parsePath(node.get(d))
            apply_transforms(path, node)

            node_copy.set("d", cubicsuperpath.formatPath(path))
            if 'transform' in node_copy.attrib:
                del node_copy.attrib['transform']

            self.nodes.append(node_copy)

    def _process_baseline(self, svg):
        for guide in get_guides(svg):
            if guide.label == "baseline":
                self.baseline = guide.position.y
                break
        else:
            # no baseline guide found, assume 0 for lack of anything better to use...
            self.baseline = 0

    def _process_bbox(self):
        left, right, top, bottom = simpletransform.computeBBox(self.nodes)

        self.width = right - left
        self._min_x = left

    def _move_to_origin(self):
        translate_x = -self.min_x
        translate_y = -self.baseline
        transform = "translate(%s, %s)" % (translate_x, translate_y)

        for node in self.nodes:
            node.set('transform', transform)
            simpletransform.fuseTransform(node)
