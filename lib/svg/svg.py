# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import math

from inkex import NSS, BaseElement, Group, Transform
from lxml import etree

from ..utils import cache
from .tags import SVG_GROUP_TAG


@cache
def get_document(node):
    return node.getroottree().getroot()


def generate_unique_id(document_or_element, prefix="path", blocklist=None):
    if isinstance(document_or_element, etree._ElementTree):
        document = document_or_element.getroot()
    else:
        document = get_document(document_or_element)

    new_id = document.get_unique_id(prefix, blacklist=blocklist)

    return new_id


def find_elements(node, xpath):
    document = get_document(node)
    elements = document.xpath(xpath, namespaces=NSS)
    return elements


def copy_no_children(node: BaseElement) -> BaseElement:
    return type(node)(attrib=node.attrib)


def point_upwards(node: BaseElement) -> None:
    """
    Given a node, adjust the transform such that it is in the same spot, but pointing upwards (e.g. for command symbols)
    """
    # Adjust the transform of the node so it's face-up and the right way around.
    node_transform = node.composed_transform()
    compensation = -Transform((node_transform.a, node_transform.b, node_transform.c, node_transform.d, 0, 0))
    scale_vector = compensation.capply_to_point(1+1j)
    scale_factor = math.sqrt(2)/math.sqrt(scale_vector.real*scale_vector.real + scale_vector.imag*scale_vector.imag)
    compensation.add_scale(scale_factor, scale_factor)

    node_correction = Transform().add_translate(float(node.get('x', 0)), float(node.get('y', 0)))
    node_correction @= compensation
    # Quick hack to compute the rotational angle - node_transform @ (1,0) = (a, b)

    node.transform = node.transform @ node_correction
    # Clear the x and y coords, they've been incorporated to the transform above
    node.set('x', None)
    node.set('y', None)


def delete_empty_groups(selection):
    for element in selection:
        selected_groups = selection.filter(Group)
        for group in selected_groups:
            groups_within_group = reversed(list(group.iterdescendants(SVG_GROUP_TAG)))
            for g in groups_within_group:
                if len(g) == 0:
                    g.delete()
            if len(group) == 0:
                group.delete()
