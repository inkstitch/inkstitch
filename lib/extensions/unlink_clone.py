# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import List, Tuple, cast

from inkex import BaseElement, Boolean, Group, errormsg

from ..elements import Clone, EmbroideryElement
from ..i18n import _
from ..svg.tags import CONNECTION_END, CONNECTION_START, SVG_SYMBOL_TAG
from .base import InkstitchExtension


class UnlinkClone(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-g", "--add-group", dest="add_group", type=Boolean, default=True)
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
                resolved = element.resolve_clone(recursive=recursive)
                if resolved[0].tag in SVG_SYMBOL_TAG:
                    self._resolve_symbol(resolved)
                clones_resolved.append((element.node, resolved[0]))

        for (clone, resolved_clone) in clones_resolved:
            clone.delete()
            orig_id = resolved_clone.get_id()
            new_id = clone.get_id()
            # Fix up command backlinks - note this has to happen before we rename so they can actually be found.
            for command in EmbroideryElement(resolved_clone).commands:
                backlink_attrib = CONNECTION_START if command.connector.get(CONNECTION_START) == ("#"+orig_id) else CONNECTION_END
                command.connector.set(backlink_attrib, "#"+new_id)
            resolved_clone.set_id(new_id)

    def _resolve_symbol(self, resolved):
        parent = cast(BaseElement, resolved[0].getparent())  # Safe assumption that this has a parent.
        if self.options.add_group:
            group = Group()
        else:
            group = parent
        for child in resolved[0]:
            group.append(child)
        if self.options.add_group:
            parent.replace(resolved[0], group)
        else:
            resolved[0].delete()
