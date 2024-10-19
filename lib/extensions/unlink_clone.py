# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, errormsg, BaseElement

from ..elements import Clone, EmbroideryElement
from ..i18n import _
from .base import InkstitchExtension
from ..svg.tags import CONNECTION_END, CONNECTION_START

from typing import List, Tuple


class UnlinkClone(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-r", "--recursive", dest="recursive", type=Boolean, default=True)

    def effect(self) -> None:
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
                element_resolved = element.resolve_clone(recursive=recursive)
                clones_resolved.append((element.node, element_resolved[0]))

        for (clone, resolved) in clones_resolved:
            clone.delete()
            orig_id = resolved.get_id()
            new_id = clone.get_id()
            # Fix up command backlinks - note this has to happen before we rename so they can actually be found.
            for command in EmbroideryElement(resolved).commands:
                backlink_attrib = CONNECTION_START if command.connector.get(CONNECTION_START) == ("#"+orig_id) else CONNECTION_END
                command.connector.set(backlink_attrib, "#"+new_id)
            resolved.set_id(new_id)
