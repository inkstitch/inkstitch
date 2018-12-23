import pyembroidery
import sys

import simpletransform

from .commands import global_command
from .i18n import _
from .svg import PIXELS_PER_MM, get_doc_size, get_viewbox_transform
from .utils import Point


def get_command(stitch):
    if stitch.jump:
        return pyembroidery.JUMP
    elif stitch.trim:
        return pyembroidery.TRIM
    elif stitch.color_change:
        return pyembroidery.COLOR_CHANGE
    elif stitch.stop:
        return pyembroidery.STOP
    else:
        return pyembroidery.NEEDLE_AT


def _string_to_floats(string):
    floats = string.split(',')
    return [float(num) for num in floats]


def get_origin(svg):
    origin_command = global_command(svg, "origin")

    if origin_command:
        return origin_command.point
    else:
        # default: center of the canvas

        doc_size = list(get_doc_size(svg))

        # convert the size from viewbox-relative to real-world pixels
        viewbox_transform = get_viewbox_transform(svg)
        simpletransform.applyTransformToPoint(simpletransform.invertTransform(viewbox_transform), doc_size)

        default = [doc_size[0] / 2.0, doc_size[1] / 2.0]
        simpletransform.applyTransformToPoint(viewbox_transform, default)
        default = Point(*default)

        return default


def jump_to_stop_point(pattern, svg):
    stop_position = global_command(svg, "stop_position")
    if stop_position:
        pattern.add_stitch_absolute(pyembroidery.JUMP, stop_position.point.x, stop_position.point.y)


def write_embroidery_file(file_path, stitch_plan, svg, settings={}):
    origin = get_origin(svg)

    pattern = pyembroidery.EmbPattern()

    for color_block in stitch_plan:
        pattern.add_thread(color_block.color.pyembroidery_thread)

        for stitch in color_block:
            if stitch.stop:
                jump_to_stop_point(pattern, svg)
            command = get_command(stitch)
            pattern.add_stitch_absolute(command, stitch.x, stitch.y)

    pattern.add_stitch_absolute(pyembroidery.END, stitch.x, stitch.y)

    # convert from pixels to millimeters
    # also multiply by 10 to get tenths of a millimeter as required by pyembroidery
    scale = 10 / PIXELS_PER_MM

    settings.update({
        # correct for the origin
        "translate": -origin,

        # convert from pixels to millimeters
        # also multiply by 10 to get tenths of a millimeter as required by pyembroidery
        "scale": (scale, scale),

        # This forces a jump at the start of the design and after each trim,
        # even if we're close enough not to need one.
        "full_jump": True,
    })

    if file_path.endswith('.csv'):
        # Special treatment for CSV: instruct pyembroidery not to do any post-
        # processing.  This will allow the user to match up stitch numbers seen
        # in the simulator with commands in the CSV.
        settings['max_stitch'] = float('inf')
        settings['max_jump'] = float('inf')
        settings['explicit_trim'] = False

    try:
        pyembroidery.write(pattern, file_path, settings)
    except IOError as e:
        # L10N low-level file error.  %(error)s is (hopefully?) translated by
        # the user's system automatically.
        print >> sys.stderr, _("Error writing to %(path)s: %(error)s") % dict(path=file_path, error=e.strerror)
        sys.exit(1)
