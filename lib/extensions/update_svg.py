# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..update import update_inkstitch_document
from .base import InkstitchExtension


class UpdateSvg(InkstitchExtension):

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--update-from", type=int, default=0, dest="update_from")
        # inkstitch_svg_version history:
        # 1 -> v3.0.0, May 2023
        # 2 -> v.3.1.0 May 2024
        # 3 -> v.3.2.0 May2025

    def effect(self):
        # set the file version to the update_from value, so that the updater knows where to start from
        # the updater will then reset it to the current version after the update has finished
        metadata = self.get_inkstitch_metadata()
        metadata['inkstitch_svg_version'] = self.options.update_from

        if not self.svg.selection:
            update_inkstitch_document(self.document, warn_unversioned=False)
        else:
            update_inkstitch_document(self.document, self.get_selection(), warn_unversioned=False)

    def get_selection(self):
        selection = []
        for element in self.svg.selection:
            selection.append(element)
            for descendant in element.iterdescendants():
                selection.append(descendant)
        return selection
