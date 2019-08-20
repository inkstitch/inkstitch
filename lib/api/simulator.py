from flask import Blueprint, g, jsonify

from ..stitch_plan import patches_to_stitch_plan


simulator = Blueprint('simulator', __name__)


@simulator.route('/get_stitch_plan')
def get_stitch_plan():
    if not g.extension.get_elements():
        return dict(colors=[], stitch_blocks=[], commands=[])

    patches = g.extension.elements_to_patches(g.extension.elements)
    stitch_plan = patches_to_stitch_plan(patches)

    colors = []
    stitch_blocks = []

    # There is no 0th stitch, so add a place-holder.
    commands = [""]

    for color_block in stitch_plan:
        color = color_block.color.visible_on_white.hex_digits
        stitch_block = []

        for stitch in color_block:
            # trim any whitespace on the left and top and scale to the
            # pixel density
            stitch_block.append((stitch.x, stitch.y))

            if stitch.trim:
                commands.append("TRIM")
            elif stitch.jump:
                commands.append("JUMP")
            elif stitch.stop:
                commands.append("STOP")
            elif stitch.color_change:
                commands.append("COLOR CHANGE")
            else:
                commands.append("STITCH")

            if stitch.trim or stitch.stop or stitch.color_change:
                colors.append(color)
                stitch_blocks.append(stitch_block)
                stitch_block = []

        if stitch_block:
            colors.append(color)
            stitch_blocks.append(stitch_block)

    return jsonify(colors=colors, stitch_blocks=stitch_blocks, commands=commands)
