# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..update import update_inkstitch_document
from .base import InkstitchExtension


class UpdateSvg(InkstitchExtension):

    def effect(self):
        metadata = self.get_inkstitch_metadata()
        del metadata['inkstitch_svg_version']
        update_inkstitch_document(self.document)
