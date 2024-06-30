# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from tempfile import TemporaryDirectory

import inkex

from ..i18n import _
from .base import InkstitchExtension
from .utils.inkex_command import inkscape


class PaletteSplitText(InkstitchExtension):
    # Splits sublines of text into it's own text elements in order to color them with the color picker
    def effect(self):
        if not self.svg.selection:
            inkex.errormsg(_("Please select one or more text elements to split lines."))
            return

        for text in self.svg.selection.get(inkex.elements.TextElement):
            parent = text.getparent()
            content = text.get_text()
            lines = content.split('\n')
            lines.reverse()
            lines = [line for line in lines if not len(line) == 0]

            style = text.style
            # If shape-inside style is used, it will lead to bad placement
            style.pop('shape-inside', None)

            transform = text.transform
            text.pop('transform')

            # the inkex command `bbox = text.get_inkscape_bbox()` is causing problems for our pyinstaller bundled
            # releases, this code block is taken from inkex/elements/_text
            with TemporaryDirectory(prefix="inkscape-command") as tmpdir:
                svg_file = inkex.command.write_svg(text.root, tmpdir, "input.svg")
                bbox = inkscape(svg_file, "-X", "-Y", "-W", "-H", query_id=text.get_id())
                bbox = list(map(text.root.viewport_to_unit, bbox.splitlines()))
                bbox = inkex.BoundingBox.new_xywh(*bbox[1:])

            x = bbox.left
            y = bbox.bottom
            height = bbox.height / (len(lines))

            for line in lines:
                element = inkex.TextElement()
                element.text = line
                element.set('style', str(style))
                element.set('x', str(x))
                element.set('y', str(y))
                element.set('transform', str(transform))

                y -= height
                parent.insert(0, element)
            parent.remove(text)
