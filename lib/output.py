# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import re
import sys
from typing import Tuple, Optional, NoReturn
import io

import inkex
from pyembroidery.exceptions import TooManyColorChangesError

import pyembroidery

from .commands import global_command
from .i18n import _
from .stitch_plan import Stitch, StitchPlan
from .svg import PIXELS_PER_MM
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
        pattern.add_stitch_absolute(pyembroidery.JUMP, stop_position.point.x, stop_position.point.y)


def _compute_pattern_settings(
        extension: str,
        stitch_plan: StitchPlan,
        svg: inkex.SvgDocumentElement,
        settings: Optional[dict]) -> Tuple[pyembroidery.EmbPattern, dict]:
    # Return an embroidery pattern and settings to pass to pyembroidery
    if settings is None:
        settings = {}

    # convert from pixels to millimeters
    # also multiply by 10 to get tenths of a millimeter as required by pyembroidery
    scale = 10 / PIXELS_PER_MM

    origin = get_origin(svg, stitch_plan.bounding_box)
    # origin = origin * scale

    pattern = pyembroidery.EmbPattern()

    # For later use when writing .dst header title field.
    pattern.extras['name'] = os.path.splitext(svg.name)[0]

    stitch = Stitch(0, 0)

    for color_block in stitch_plan:
        pattern.add_thread(color_block.color.pyembroidery_thread)

        for stitch in color_block:
            if stitch.stop:
                jump_to_stop_point(pattern, svg)
            command = get_command(stitch)
            pattern.add_stitch_absolute(command, stitch.x, stitch.y)

    pattern.add_stitch_absolute(pyembroidery.END, stitch.x, stitch.y)

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

    if extension not in ('col', 'edr', 'inf'):
        settings['encode'] = True

    if extension == 'csv':
        # Special treatment for CSV: instruct pyembroidery not to do any post-
        # processing.  This will allow the user to match up stitch numbers seen
        # in the simulator with commands in the CSV.
        settings['max_stitch'] = float('inf')
        settings['max_jump'] = float('inf')
        settings['explicit_trim'] = False

    return pattern, settings


def _too_many_color_changes(e: TooManyColorChangesError) -> NoReturn:
    match = re.search("d+", str(e))
    if match:
        num_color_changes = match.group()
    else:
        # Should never get here, the number of color changes should have been in the error's message
        num_color_changes = "???"
    msg = _("Couldn't save embroidery file.")
    msg += '\n\n'
    msg += _("There are {num_color_changes} color changes in your design. This is way too many.").format(num_color_changes=num_color_changes)
    msg += '\n'
    msg += _("Please reduce color changes. Find more information on our website:")
    msg += '\n\n'
    msg += _("https://inkstitch.org/docs/faq/#too-many-color-changes")
    inkex.errormsg(msg)
    sys.exit(1)


def write_embroidery_file(
        file_path: str,
        stitch_plan: StitchPlan,
        svg: inkex.SvgDocumentElement,
        settings: Optional[dict] = None) -> None:
    """ Write embroidery file to a given path """

    pattern, settings = _compute_pattern_settings(os.path.splitext(svg.name)[1], stitch_plan, svg, settings)

    try:
        pyembroidery.write(pattern, file_path, settings)
    except IOError as e:
        # L10N low-level file error.  %(error)s is (hopefully?) translated by
        # the user's system automatically.
        msg = _("Error writing to %(path)s: %(error)s") % dict(path=file_path, error=e.strerror)
        inkex.errormsg(msg)
        sys.exit(1)
    except TooManyColorChangesError as e:
        _too_many_color_changes(e)


def write_embroidery_file_stream(
        stream: io.IOBase,
        extension: str,
        stitch_plan: StitchPlan,
        svg: inkex.SvgDocumentElement,
        settings: Optional[dict] = None) -> None:
    """ Write embroidery file to a stream """

    pattern, settings = _compute_pattern_settings(extension, stitch_plan, svg, settings)

    try:
        for file_type in pyembroidery.EmbPattern.supported_formats():
            if file_type["extension"] != extension:
                continue
            writer = file_type.get("writer", None)
            if writer is None:
                continue

            pyembroidery.EmbPattern.write_embroidery(writer, pattern, stream, settings)
            break
    except IOError as e:
        # L10N low-level file error.  %(error)s is (hopefully?) translated by
        # the user's system automatically.
        msg = _("Error writing: %(error)s") % dict(error=e.strerror)
        inkex.errormsg(msg)
        sys.exit(1)
    except TooManyColorChangesError as e:
        _too_many_color_changes(e)
