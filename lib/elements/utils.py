
from ..commands import is_command
from ..svg.tags import SVG_POLYLINE_TAG, SVG_PATH_TAG

from .auto_fill import AutoFill
from .element import EmbroideryElement
from .fill import Fill
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke


def node_to_elements(node):  # noqa: C901
    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline(node)]
    elif node.tag == SVG_PATH_TAG:
        element = EmbroideryElement(node)

        if element.flattened_path_length < 2:
            return []

        if element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []

            if element.get_style("fill", "black") and not element.get_style('fill-opacity', 1) == "0":
                if element.flattened_path_length < 3:
                    return []
                if element.get_boolean_param("auto_fill", True):
                    elements.append(AutoFill(node))
                else:
                    elements.append(Fill(node))

            if element.get_style("stroke"):
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
