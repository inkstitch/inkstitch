# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from html import escape

import inkex
from inkex.utils import errormsg
import pystitch

from ..i18n import _
from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..svg.tags import INKSCAPE_LABEL
from .stitch import Stitch
from .stitch_plan import StitchPlan


def generate_stitch_plan(embroidery_file, import_commands="symbols"):
    validate_file_path(embroidery_file)
    pattern = pystitch.read(embroidery_file)
    if pattern is None:
        return None
    stitch_plan = StitchPlan()
    color_block = None

    scale = PIXELS_PER_MM / 10.0
    STITCH_CMD = pystitch.STITCH
    TRIM_CMD = pystitch.TRIM
    STOP_CMD = pystitch.STOP
    no_commands = import_commands == "none"
    _Stitch = Stitch
    _new = _Stitch.__new__
    _False = False
    _None = None
    _zero = 0

    for raw_stitches, thread in pattern.get_as_colorblocks():
        color_block = stitch_plan.new_color_block(thread)
        stitches = color_block.stitches
        _append = stitches.append
        for x, y, command in raw_stitches:
            if command == STITCH_CMD:
                s = _new(_Stitch)
                s.x = x * scale
                s.y = y * scale
                s.color = _None
                s.jump = _False
                s.trim = _False
                s.stop = _False
                s.color_change = _False
                s.min_stitch_length = _zero
                s._flags = _zero
                s.tags = set()
                _append(s)
            elif stitches:
                if no_commands and command in (TRIM_CMD, STOP_CMD):
                    color_block = stitch_plan.new_color_block(thread)
                    stitches = color_block.stitches
                    _append = stitches.append
                elif command == TRIM_CMD:
                    color_block.add_stitch(trim=True)
                elif command == STOP_CMD:
                    color_block.add_stitch(stop=True)
                    color_block = stitch_plan.new_color_block(thread)
                    stitches = color_block.stitches
                    _append = stitches.append

    stitch_plan.delete_empty_color_blocks()

    if not stitch_plan.color_blocks:
        errormsg(_('The file could not be loaded. No stitches were found.'))
        return None

    if stitch_plan.last_color_block:
        if stitch_plan.last_color_block.last_stitch:
            if stitch_plan.last_color_block.last_stitch.stop:
                # ending with a STOP command is redundant, so remove it
                del stitch_plan.last_color_block[-1]

    extents = stitch_plan.extents
    svg = inkex.SvgDocumentElement("svg", nsmap=inkex.NSS, attrib={
        "width": str(extents[0] * 2),
        "height": str(extents[1] * 2),
        "viewBox": "0 0 %s %s" % (extents[0] * 2, extents[1] * 2),
    })

    visual_commands = True if import_commands == "symbols" else False
    render_stitch_plan(svg, stitch_plan, visual_commands=visual_commands)

    # rename the Stitch Plan layer so that it doesn't get overwritten by Embroider
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    assert layer is not None
    layer.set(INKSCAPE_LABEL, escape(os.path.basename(embroidery_file)))
    layer.attrib.pop('id')

    # Shift the design so that its origin is at the center of the canvas
    # Note: this is NOT the same as centering the design in the canvas!
    layer.set('transform', 'translate(%s,%s)' % (extents[0], extents[1]))

    return svg


def validate_file_path(path):
    # Check if the file exists
    if not os.path.isfile(path):
        errormsg(_('File does not exist and cannot be opened. Please correct the file path and try again.\r%s') % path)
        sys.exit(1)
