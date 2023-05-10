# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..i18n import _
from ..update import update_inkstitch_document
from .base import InkstitchExtension


class UpdateSvg(InkstitchExtension):

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        # TODO: When there are more legacy versions than only one, this can be transformed into a user input
        # inkstitch_svg_version history: 1 -> v3.0.0, May 2023
        self.update_from = 0

    def effect(self):
        if not self.svg.selection:
            errormsg(_('Please select at least one element to update. '
                       'This extension is designed to help you update copy and pasted elements from old designs.'))

        # set the file version to the update_from value, so that the updater knows where to start from
        # the updater will then reset it to the current version after the update has finished
        metadata = self.get_inkstitch_metadata()
        metadata['inkstitch_svg_version'] = self.update_from

        update_inkstitch_document(self.document, self.get_selection())

    def get_selection(self):
        selection = []
        for element in self.svg.selection:
            selection.append(element)
            for descendant in element.iterdescendants():
                selection.append(descendant)
        return selection
