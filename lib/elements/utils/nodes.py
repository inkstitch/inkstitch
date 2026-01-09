# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import Iterable, List, Optional

from inkex import BaseElement
from lxml.etree import Comment

from ...commands import is_command, layer_commands
from ...debug.debug import sew_stack_enabled
from ...marker import has_marker
from ...svg import PIXELS_PER_MM
from ...svg.tags import (CONNECTOR_TYPE, EMBROIDERABLE_TAGS,
                         INKSCAPE_GROUPMODE, INKSCAPE_LABEL, NOT_EMBROIDERABLE_TAGS,
                         SVG_CLIPPATH_TAG, SVG_DEFS_TAG, SVG_GROUP_TAG,
                         SVG_IMAGE_TAG, SVG_MASK_TAG, SVG_TEXT_TAG)
from ..clone import Clone, is_clone
from ..element import EmbroideryElement
from ..empty_d_object import EmptyDObject
from ..fill_stitch import FillStitch
from ..image import ImageObject
from ..marker import MarkerObject
from ..satin_column import SatinColumn
from ..stroke import Stroke
from ..text import TextObject


def node_to_elements(node, clone_to_element=False) -> List[EmbroideryElement]:  # noqa: C901
    if node.style('display') == 'none':
        return []
    if is_clone(node) and not clone_to_element:
        # clone_to_element: get an actual embroiderable element once a clone has been defined as a clone
        return [Clone(node)]

    elif node.tag in EMBROIDERABLE_TAGS and not node.get_path():
        return [EmptyDObject(node)]

    elif has_marker(node):
        return [MarkerObject(node)]

    elif node.tag in EMBROIDERABLE_TAGS or is_clone(node):
        elements: List[EmbroideryElement] = []

        from ...sew_stack import SewStack
        sew_stack = SewStack(node)

        if not sew_stack.sew_stack_only:
            element = EmbroideryElement(node)
            if element.fill_color is not None and not element.get_style('fill-opacity', 1) == "0":
                elements.append(FillStitch(node))
            if element.stroke_color is not None:
                if element.get_boolean_param("satin_column", False) and (len(element.path) > 1 or element.stroke_width > 0.3 * PIXELS_PER_MM):
                    elements.append(SatinColumn(node))
                elif not is_command(element.node):
                    elements.append(Stroke(node))
            if element.get_boolean_param("stroke_first", False):
                elements.reverse()

        if sew_stack_enabled:
            elements.append(sew_stack)

        return elements

    elif node.tag == SVG_IMAGE_TAG:
        return [ImageObject(node)]

    elif node.tag == SVG_TEXT_TAG:
        return [TextObject(node)]

    else:
        return []


def nodes_to_elements(nodes: Iterable[BaseElement]) -> List[EmbroideryElement]:
    elements = []
    for node in nodes:
        elements.extend(node_to_elements(node))

    return elements


def iterate_nodes(node: BaseElement,  # noqa: C901
                  selection: Optional[List[BaseElement]] = None,
                  troubleshoot=False) -> List[BaseElement]:
    # Postorder traversal of selected nodes and their descendants.
    # Returns all nodes if there is no selection.
    def walk(node: BaseElement, selected: bool) -> List[BaseElement]:
        nodes = []

        # lxml-stubs types are wrong, node.tag can be Comment.
        if node.tag is Comment:  # type:ignore[comparison-overlap]
            return []

        element = EmbroideryElement(node)

        if element.has_command('ignore_object'):
            return []

        if node.tag == SVG_GROUP_TAG and node.get(INKSCAPE_GROUPMODE) == "layer":
            if len(list(layer_commands(node, "ignore_layer"))):
                return []

        if (node.tag in EMBROIDERABLE_TAGS or node.tag == SVG_GROUP_TAG) and element.get_style('display', 'inline') is None:
            return []

        # defs, masks and clippaths can contain embroiderable elements
        # but should never be rendered directly.
        if node.tag in [SVG_DEFS_TAG, SVG_MASK_TAG, SVG_CLIPPATH_TAG]:
            return []

        # command connectors with a fill color set, will glitch into the elements list
        if is_command(node) or node.get(CONNECTOR_TYPE):
            return []

        # command groups contain command symbols that should not be embroidered
        # These are groups with labels like "Ink/Stitch Command: ..."
        node_label = node.get(INKSCAPE_LABEL, "")
        if node_label.startswith("Ink/Stitch Command"):
            return []

        if not selected:
            if selection:
                if node in selection:
                    selected = True
            else:
                # if the user didn't select anything that means we process everything
                selected = True

        for child in node:
            nodes.extend(walk(child, selected))

        if selected:
            if node.tag == SVG_GROUP_TAG:
                pass
            elif (node.tag in EMBROIDERABLE_TAGS or is_clone(node)) and not has_marker(node):
                nodes.append(node)
            # add images, text and elements with a marker for the troubleshoot extension
            elif troubleshoot and (node.tag in NOT_EMBROIDERABLE_TAGS or has_marker(node)):
                nodes.append(node)

        return nodes

    return walk(node, False)
