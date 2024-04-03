# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS
from lxml import etree

from ..utils import cache


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
