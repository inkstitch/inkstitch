# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class PatternWarning(ObjectTypeWarning):
    name = _("Pattern Element")
    description = _("This element will only be stitched out as a pattern within the specified object.")
    steps_to_solve = [
        _("If you want to remove the pattern configuration for a pattern object follow these steps:"),
        _("* Select pattern element(s)"),
        _('* Run Extensions > Ink/Stitch > Troubleshoot > Remove embroidery settings...'),
        _('* Make sure "Remove params" is enables'),
        _('* Click "Apply"')
    ]


class PatternObject(EmbroideryElement):

    def validation_warnings(self):
        repr_point = next(inkex.Path(self.parse_path()).end_points)
        yield PatternWarning(repr_point)

    def to_patches(self, last_patch):
        return []


def is_pattern(node):
    if node.tag not in EMBROIDERABLE_TAGS:
        return False
    return "marker-start:url(#inkstitch-pattern-marker)" in node.get('style', '')
