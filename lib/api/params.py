from collections import Counter, defaultdict

from flask import Blueprint, Response, g, jsonify
from stringcase import snakecase

from ..elements.utils import node_to_elements
from ..svg import thumbnail
from ..svg.tags import INKSCAPE_LABEL

params = Blueprint('params', __name__)

node_to_types = None
elements_by_type = None


@params.route('/objects')
def get_objects():
    global node_to_types, elements_by_type
    elements_by_type = defaultdict(list)
    node_to_types = defaultdict(list)

    objects = {
        "nodes": [],
        "num_nodes": Counter()
    }

    for node in g.extension.nodes:
        node_id = node.get('id')

        objects['nodes'].append({"node_id": node_id,
                                 "name": node.get(INKSCAPE_LABEL) or node.get('id')})

        elements = node_to_elements(node)
        objects['num_nodes'].update(element_type(element) for element in elements)

        for element in elements:
            elements_by_type[element_type(element)].append(element)
            node_to_types[node_id].append(element_type(element))

    return jsonify(objects)


def element_type(element):
    return snakecase(element.__class__.__name__)


@params.route('/object-types/<node_id>')
def get_object_types(node_id):
    return jsonify({object_type: True for object_type in node_to_types[node_id]})


@params.route('/thumbnail/<node_id>')
def get_thumbnail(node_id):
    node = g.extension.svg.getElementById(node_id)
    png_data = thumbnail(node)

    if png_data is None:
        return Response(status=500)
    else:
        return Response(png_data, mimetype="image/png")
