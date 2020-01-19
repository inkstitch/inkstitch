from ..commands import is_command
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_POLYLINE_TAG
from .auto_fill import AutoFill
from .clone import Clone, is_clone
from .element import EmbroideryElement
from .fill import Fill
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke


def node_to_elements(node):

    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline(node)]

    elif is_clone(node):
        return [Clone(node)]

    elif node.tag in EMBROIDERABLE_TAGS:
        element = EmbroideryElement(node)

        if element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []

            if element.get_style("fill"):
                if element.get_boolean_param("auto_fill", True):
                    elements.append(AutoFill(node))
                else:
                    elements.append(Fill(node))

            if element.get_style("stroke", "#000000"):
                if not is_command(element.node):
                    elements.append(Stroke(node))

            if element.get_boolean_param("stroke_first", False):
                elements.reverse()

            return elements

    else:
        return []


def nodes_to_elements(nodes):
    elements = []
    for node in nodes:
        elements.extend(node_to_elements(node))
    return elements
