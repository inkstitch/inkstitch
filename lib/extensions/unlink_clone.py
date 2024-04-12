# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, errormsg, BaseElement

from ..elements import Clone
from ..i18n import _
from .base import InkstitchExtension

from typing import List, Tuple


class UnlinkClone(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-r", "--recursive", dest="recursive", type=Boolean, default=True)

    def effect(self):
        recursive: bool = self.options.recursive

        if not self.get_elements():
            return

        if not self.svg.selection:
            errormsg(_("Please select one or more clones to unlink."))
            return

        # Two passes here: One to resolve all clones, and then another to replace those clones with their resolved versions.
        # This way we don't accidentally remove a node that another clone refers to.
        clones_resolved: List[Tuple[BaseElement, BaseElement]] = []
        for element in self.elements:
            if isinstance(element, Clone):
                resolved = element.resolve_clone(recursive=recursive)
                clones_resolved.append((element.node, resolved))

        for (clone, resolved) in clones_resolved:
            clone.getparent().remove(clone)
            resolved.set_id(clone.get_id())
