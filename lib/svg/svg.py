from ..utils import cache


@cache
def get_document(node):
    return node.getroottree().getroot()


def generate_unique_id(document, prefix="path"):
    doc_ids = {node.get('id') for node in document.iterdescendants() if 'id' in node.attrib}

    i = 1
    while True:
        new_id = "%s%d" % (prefix, i)
        if new_id not in doc_ids:
            break
        i += 1

    return new_id
