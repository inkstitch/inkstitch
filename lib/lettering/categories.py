# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..i18n import _


class FontCategory:
    def __init__(self, cat_id=None, name=None):
        self.id: str = cat_id
        self.name: str = name

    def __repr__(self):
        return "FontCategory(%s, %s)" % (self.id, self.name)


FONT_CATEGORIES = [
    FontCategory('applique', _("Applique")),
    FontCategory('crossstitch', _("Crossstitch")),
    FontCategory('display', _('Display')),
    FontCategory('handwriting', _("Handwriting")),
    FontCategory('italic', _("Italic")),
    FontCategory('monogram', _("Monogram")),
    FontCategory('multicolor', _('Multicolor')),
    FontCategory('running_stitch', _('Running Stitch')),
    FontCategory('sans_serif', _("Sans Serif")),
    FontCategory('serif', _("Serif")),
    FontCategory('tiny', _("Tiny"))
]
