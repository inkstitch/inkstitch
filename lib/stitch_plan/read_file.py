import pyembroidery
from .stitch_plan import StitchPlan

from ..svg import PIXELS_PER_MM


def stitch_plan_from_file(embroidery_file):
    """Read a machine embroidery file in any supported format and return a stitch plan."""
    pattern = pyembroidery.read(embroidery_file)

    stitch_plan = StitchPlan()
    previous_command = pyembroidery.NO_COMMAND
    pre_previous_command = pyembroidery.NO_COMMAND
    for raw_stitches, thread in pattern.get_as_colorblocks():
        color_block = stitch_plan.new_color_block(thread)
        for x, y, command in raw_stitches:
            if command == pyembroidery.END:
                stitch_plan.previous_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                            end=True)
            elif command == pyembroidery.TRIM and previous_command == pyembroidery.END:
                stitch_plan.previous_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                            trim=True)
            elif (command == pyembroidery.JUMP and pre_previous_command == pyembroidery.END and
                  previous_command == pyembroidery.TRIM):
                stitch_plan.last_color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                                        jump=True)
                # TODO maybe I should add them as END, end, trim, end trim jump, to be able to handle them?
            else:
                color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0,
                                       jump=(command == pyembroidery.JUMP),
                                       trim=(command == pyembroidery.TRIM),
                                       color_change=(command == pyembroidery.COLOR_CHANGE))
            pre_previous_command = previous_command
            previous_command = command
    stitch_plan.delete_empty_color_blocks()
    return stitch_plan
