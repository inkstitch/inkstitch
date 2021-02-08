from flask import Blueprint, g, jsonify

from ..stitch_plan import patches_to_stitch_plan


stitch_plan = Blueprint('stitch_plan', __name__)


@stitch_plan.route('')
def get_stitch_plan():
    if not g.extension.get_elements():
        return dict(colors=[], stitch_blocks=[], commands=[])

    metadata = g.extension.get_inkstitch_metadata()
    collapse_len = metadata['collapse_len_mm']
    patches = g.extension.elements_to_patches(g.extension.elements)
    stitch_plan = patches_to_stitch_plan(patches, collapse_len=collapse_len)

    return jsonify(stitch_plan)
