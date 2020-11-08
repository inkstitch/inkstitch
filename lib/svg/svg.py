from inkex import NSS
from lxml import etree

from ..utils import cache


@cache
def get_document(node):
    return node.getroottree().getroot()


def generate_unique_id(document_or_element, prefix="path"):
    if isinstance(document_or_element, etree._ElementTree):
        document = document_or_element.getroot()
    else:
        document = get_document(document_or_element)

    doc_ids = {node.get('id') for node in document.iterdescendants() if 'id' in node.attrib}

    i = 1
    while True:
        new_id = "%s%d" % (prefix, i)
        if new_id not in doc_ids:
            break
        i += 1

    return new_id


def find_elements(node, xpath):
    document = get_document(node)
    elements = document.xpath(xpath, namespaces=NSS)
    return elements
