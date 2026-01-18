# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys

from ..i18n import _
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class ThreadList(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self)

    def effect(self):
        if not self.get_elements():
            return

        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)
        ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])

        thread_list = get_threadlist(stitch_plan, self.get_base_file_name())

        # inkscape will read the file contents from stdout and copy
        # to the destination file that the user chose
        sys.stdout.write(thread_list)

        # don't let inkex output the SVG!
        self.skip_output()


def get_threadlist(stitch_plan, design_name):
    width = round(stitch_plan.dimensions_mm[0], 2)
    height = round(stitch_plan.dimensions_mm[1], 2)

    thread_used = []

    thread_output = "%s\n" % _("Design Details")
    thread_output += "==============================\n\n"

    thread_output += _("Title")
    thread_output += f": {design_name}\n"

    thread_output += _("Size")
    thread_output += f" (mm): {width} x {height}\n"

    thread_output += _("Stitches")
    thread_output += f": {stitch_plan.num_stitches}\n"

    thread_output += _("Colors")
    thread_output += f": {stitch_plan.num_colors}\n\n"

    thread_output += _("Thread Order")
    thread_output += "\n===========================\n\n"

    for i, color_block in enumerate(stitch_plan):
        thread = color_block.color

        thread_output += str(i + 1) + " "
        string = f"{thread.name} #{thread.number} - {thread.manufacturer} (#{thread.hex_digits.lower()})"
        thread_output += string + "\n"
        thread_used.append(string)

    thread_output += "\n"
    thread_output += _("Thread Used") + "\n"
    thread_output += "===========================" + "\n\n"

    for thread in set(thread_used):
        thread_output += thread + "\n"

    return thread_output
