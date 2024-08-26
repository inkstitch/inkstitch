# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..commands import is_command
from ..marker import has_marker
from ..svg.tags import EMBROIDERABLE_TAGS, SVG_IMAGE_TAG, SVG_TEXT_TAG
from .clone import Clone, is_clone
from .element import EmbroideryElement
from .empty_d_object import EmptyDObject
from .fill_stitch import FillStitch
from .image import ImageObject
from .marker import MarkerObject
from .satin_column import SatinColumn
from .stroke import Stroke
from .text import TextObject
from typing import List
from inkex import BaseElement


def node_to_elements(node, clone_to_element=False) -> List[EmbroideryElement]:  # noqa: C901
    if is_clone(node) and not clone_to_element:
        # clone_to_element: get an actual embroiderable element once a clone has been defined as a clone
        return [Clone(node)]

    elif node.tag in EMBROIDERABLE_TAGS and not node.get_path():
        return [EmptyDObject(node)]

    elif has_marker(node):
        return [MarkerObject(node)]

    elif node.tag in EMBROIDERABLE_TAGS or is_clone(node):
        element = EmbroideryElement(node)

        elements = []
        if element.get_style("fill", "black") and not element.get_style('fill-opacity', 1) == "0":
            elements.append(FillStitch(node))
        if element.get_style("stroke"):
            if element.get_boolean_param("satin_column") and len(element.path) > 1:
                elements.append(SatinColumn(node))
            elif not is_command(element.node):
                elements.append(Stroke(node))
        if element.get_boolean_param("stroke_first", False):
            elements.reverse()
        return elements

    elif node.tag == SVG_IMAGE_TAG:
        return [ImageObject(node)]

    elif node.tag == SVG_TEXT_TAG:
        return [TextObject(node)]

    else:
        return []


def node_and_children_to_elements(node: BaseElement, clone_to_element=False) -> List[EmbroideryElement]:
    """
    Iterate through a node and its children, and return all applicable EmbroideryElements.

    Notably, does not return EmbroideryElements for hidden elements or children of hidden elements,
    similar to `Base.descendants`.
    """
    elements: List[EmbroideryElement] = []

    def walk(node: BaseElement):
        if node.get_computed_style('display') == 'none':
            return

        elements.extend(node_to_elements(node, clone_to_element))
        for child in node:
            walk(child)

    walk(node)

    return elements


def nodes_to_elements(nodes):
    elements = []
    for node in nodes:
        elements.extend(node_to_elements(node))

    return elements
