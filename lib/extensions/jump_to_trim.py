# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, DirectedLineSegment

from ..commands import add_commands
from ..svg import PIXELS_PER_MM
from .base import InkstitchExtension


class JumpToTrim(InkstitchExtension):
    """Adds a trim command to avoid jump stitches."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--tab")

        self.arg_parser.add_argument("-c", "--command", type=str, default="trim", dest="command")
        self.arg_parser.add_argument("-i", "--minimum-jump-length", type=float, default=3.0, dest="min_jump")
        self.arg_parser.add_argument("-a", "--maximum-jump-length", type=float, default=0, dest="max_jump")
        self.arg_parser.add_argument("-t", "--use-command-symbols", type=Boolean, default=False, dest="use_command_symbols")

    def effect(self):
        self._set_selection()
        self.get_elements()

        next_elements = [None]
        if len(self.elements) > 1:
            next_elements = self.elements[1:] + next_elements
        last_element = None
        last_stitch_group = None
        for element, next_element in zip(self.elements, next_elements):
            last = last_element
            last_element = element
            stitch_groups = element.embroider(last_stitch_group, next_element)
            if not stitch_groups:
                continue

            stitch_group = stitch_groups[0]
            if last_stitch_group is None or stitch_group.color != last_stitch_group.color:
                last_stitch_group = stitch_groups[-1]
                continue

            start = last_stitch_group.stitches[-1]
            end = stitch_group.stitches[0]

            last_stitch_group = stitch_groups[-1]

            distance = DirectedLineSegment((start.x, start.y), (end.x, end.y)).length

            # do not add a trim command if the distance is smaller than min_jump setting
            if distance < self.options.min_jump * PIXELS_PER_MM:
                continue
            # do not add a trim command if the distance is longer than max_jump setting
            if self.options.max_jump > 0 and distance > self.options.max_jump * PIXELS_PER_MM:
                continue
            if last is not None:
                self._add_trim(last)

    def _add_trim(self, element):
        command = "trim"
        param = "trim_after"
        if self.options.command == "stop":
            command = "stop"
            param = "stop_after"

        # skip if the element already has a trim command in one way or the other
        if element.has_command(command) or element.trim_after:
            return

        if self.options.use_command_symbols:
            add_commands(element, [command])
        else:
            element.node.set(f'inkstitch:{param}', True)

    def _set_selection(self):
        if not self.svg.selection:
            self.svg.selection.clear()


if __name__ == '__main__':
    JumpToTrim().run()
