# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from .clone import Clone, is_clone
from .element import EmbroideryElement
from .empty_d_object import EmptyDObject
from .fill_stitch import FillStitch
from .image import ImageObject
from .manual_stitch import ManualStitch
from .pattern import PatternObject
from .polyline import Polyline
from .running_stitch import RunningStitch
from .satin_stitch import SatinStitch
from .text import TextObject
from ..commands import is_command
from ..patterns import is_pattern
from ..svg.tags import (EMBROIDERABLE_TAGS, SVG_IMAGE_TAG, SVG_PATH_TAG,
                        SVG_POLYLINE_TAG, SVG_TEXT_TAG)


def node_to_elements(node):  # noqa: C901
    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline(node)]

    elif is_clone(node):
        return [Clone(node)]

    elif node.tag == SVG_PATH_TAG and not node.get('d', ''):
        return [EmptyDObject(node)]

    elif is_pattern(node):
        return [PatternObject(node)]

    elif node.tag in EMBROIDERABLE_TAGS:
        element = EmbroideryElement(node)
        elements = []
        if element.get_style("fill", "black") and not element.get_style('fill-opacity', 1) == "0":
            elements.append(FillStitch(node))

        if element.get_style("stroke") and not is_command(element.node):
            if element.get_boolean_param('manual_stitch'):
                elements.append(ManualStitch(node))
            elif element.get_style("stroke-dasharray") is None:
                elements.append(SatinStitch(node))
            else:
                elements.append(RunningStitch(node))

        if stroke_first(element):
            elements.reverse()

        return elements

    elif node.tag == SVG_IMAGE_TAG:
        return [ImageObject(node)]

    elif node.tag == SVG_TEXT_TAG:
        return [TextObject(node)]

    else:
        return []


def stroke_first(element):
    # Details: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/paint-order
    order = element.get_style("paint-order", "normal")

    # We want to return True iff "stroke" comes before "fill" in the list.
    # Note that if an item is not in the list, it's assumed to be at the end in
    # the default order (see link above).
    order = order.lower().split()

    # Just add the default order at the end.  This covers the normal case and
    # the case that one or two of the items is not specified.
    order.extend(["fill", "stroke", "markers"])

    return order.index("stroke") < order.index("fill")


def nodes_to_elements(nodes):
    elements = []
    for node in nodes:
        elements.extend(node_to_elements(node))

    return elements


def is_satin_column(element):
    if isinstance(element, SatinStitch) and element.satin_column:
        return True
