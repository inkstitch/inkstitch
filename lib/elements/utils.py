
from copy import deepcopy

from simpletransform import (applyTransformToNode, composeTransform,
                             formatTransform, parseTransform)

from ..commands import is_command
from ..svg.path import get_node_transform
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_GROUP_TAG, SVG_POLYLINE_TAG
from .auto_fill import AutoFill
from .element import EmbroideryElement
from .fill import Fill
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke
from .svg_objects import get_clone_source, is_clone


def node_to_elements(node):

    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline(node)]

    elif node.tag in EMBROIDERABLE_TAGS:
        element = EmbroideryElement(node)

        if element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []

            if element.get_style("fill", "black"):
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
        if not is_clone(node):
            elements.extend(node_to_elements(node))
        else:
            elements.extend(clones_to_elements(node))

    return elements


def clones_to_elements(node, trans=''):
    elements = []

    source_node = get_clone_source(node)
    clone = deepcopy(source_node)

    if trans:
        transform = parseTransform(trans)
    else:
        transform = get_node_transform(node)
    applyTransformToNode(transform, clone)

    if is_clone(source_node):
        elements.extend(clones_to_elements(source_node, clone.get('transform')))

    else:
        if clone.tag == SVG_GROUP_TAG:
            for clone_node in clone.iterdescendants():
                if is_clone(clone_node):
                    clone_node_source = get_clone_source(node, clone_node.get('id'))
                    transform = formatTransform(composeTransform(transform, parseTransform(clone_node_source.get('transform'))))
                    elements.extend(clones_to_elements(clone_node_source, transform))
                clone_id = 'clones__%s__%s' % (node.get('id', ''), clone_node.get('id', ''))
                clone_node.set('id', clone_id)
                elements.extend(node_to_elements(clone_node))
        else:
            clone_id = 'clone__%s__%s' % (node.get('id', ''), clone.get('id', ''))
            clone.set('id', clone_id)
            elements.extend(node_to_elements(clone))

    return elements
