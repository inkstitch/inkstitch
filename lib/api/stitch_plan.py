from flask import Blueprint, g, jsonify

from ..stitch_plan import patches_to_stitch_plan


stitch_plan = Blueprint('stitch_plan', __name__)


@stitch_plan.route('')
def get_stitch_plan():
    if not g.extension.get_elements():
        return dict(colors=[], stitch_blocks=[], commands=[])

    patches = g.extension.elements_to_patches(g.extension.elements)
    stitch_plan = patches_to_stitch_plan(patches)

    return jsonify(stitch_plan)
