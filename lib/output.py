# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import re
import sys

import inkex
from pystitch.exceptions import TooManyColorChangesError

import pystitch

from .commands import global_command
from .i18n import _
from .stitch_plan import Stitch
from .svg import PIXELS_PER_MM
from .utils import Point


def get_command(stitch):
    if stitch.jump:
        return pystitch.JUMP
    elif stitch.trim:
        return pystitch.TRIM
    elif stitch.color_change:
        return pystitch.COLOR_CHANGE
    elif stitch.stop:
        return pystitch.STOP
    else:
        return pystitch.NEEDLE_AT


def get_origin(svg, bounding_box):
    (minx, miny, maxx, maxy) = bounding_box
    origin_command = global_command(svg, "origin")

    if origin_command:
        return origin_command.point
    else:
        bounding_box_center = [(maxx+minx)/2, (maxy+miny)/2]
        default = Point(*bounding_box_center)
        return default


def jump_to_stop_point(pattern, svg):
    stop_position = global_command(svg, "stop_position")
    if stop_position:
        pattern.add_stitch_absolute(pystitch.JUMP, stop_position.point.x, stop_position.point.y)


def write_embroidery_file(file_path, stitch_plan, svg, settings={}):
    # convert from pixels to millimeters
    # also multiply by 10 to get tenths of a millimeter as required by pystitch
    scale = 10 / PIXELS_PER_MM

    origin = get_origin(svg, stitch_plan.bounding_box)
    # origin = origin * scale

    pattern = pystitch.EmbPattern()

    # For later use when writing .dst header title field.
    pattern.extras['name'] = os.path.splitext(svg.name)[0]

    stitch = Stitch(0, 0)

    for color_block in stitch_plan:
        pattern.add_thread(color_block.color.pystitch_thread)

        for stitch in color_block:
            if stitch.stop:
                jump_to_stop_point(pattern, svg)
            command = get_command(stitch)
            pattern.add_stitch_absolute(command, stitch.x, stitch.y)

    pattern.add_stitch_absolute(pystitch.END, stitch.x, stitch.y)

    settings.update({
        # correct for the origin
        "translate": -origin,

        # convert from pixels to millimeters
        # also multiply by 10 to get tenths of a millimeter as required by pystitch
        "scale": (scale, scale),

        # This forces a jump at the start of the design and after each trim,
        # even if we're close enough not to need one.
        "full_jump": True,

        # defaults to False in pystitch (see https://github.com/EmbroidePy/pyembroidery/issues/188)
        "trims": True,
    })

    if not file_path.endswith(('.col', '.edr', '.inf')):
        settings['encode'] = True

    if file_path.endswith('.csv'):
        # Special treatment for CSV: instruct pystitch not to do any post-
        # processing.  This will allow the user to match up stitch numbers seen
        # in the simulator with commands in the CSV.
        settings['max_stitch'] = float('inf')
        settings['max_jump'] = float('inf')
        settings['explicit_trim'] = False

    try:
        pystitch.write(pattern, file_path, settings)
    except IOError as e:
        # L10N low-level file error.  %(error)s is (hopefully?) translated by
        # the user's system automatically.
        msg = _("Error writing to %(path)s: %(error)s") % dict(path=file_path, error=e.strerror)
        inkex.errormsg(msg)
        sys.exit(1)
    except TooManyColorChangesError as e:
        num_color_changes = re.search("d+", str(e)).group()
        msg = _("Couldn't save embrodiery file.")
        msg += '\n\n'
        msg += _("There are {num_color_changes} color changes in your design. This is way too many.").format(num_color_changes=num_color_changes)
        msg += '\n'
        msg += _("Please reduce color changes. Find more information on our website:")
        msg += '\n\n'
        msg += _("https://inkstitch.org/docs/faq/#too-many-color-changes")
        inkex.errormsg(msg)
        sys.exit(1)
