# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS

from .base import InkstitchExtension


class ObjectCommandsToggleVisibility(InkstitchExtension):

    def effect(self):
        svg = self.document.getroot()
        # toggle object commands (in fact it's display or hide all of them)
        command_groups = svg.xpath(".//svg:g[starts-with(@id,'command_group')]", namespaces=NSS)
        display = "none"
        first_iteration = True
        for command_group in command_groups:
            if first_iteration:
                first_iteration = False
                if not command_group.is_visible():
                    display = "inline"
            command_group.style['display'] = display
