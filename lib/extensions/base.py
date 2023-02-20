# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import os
import re
from collections.abc import MutableMapping

from lxml import etree
from lxml.etree import Comment
from stringcase import snakecase

import inkex

from ..commands import is_command, layer_commands
from ..elements import EmbroideryElement, nodes_to_elements
from ..elements.clone import is_clone
from ..i18n import _
from ..marker import has_marker
from ..svg import generate_unique_id
from ..svg.tags import (CONNECTOR_TYPE, EMBROIDERABLE_TAGS, INKSCAPE_GROUPMODE,
                        NOT_EMBROIDERABLE_TAGS, SVG_CLIPPATH_TAG, SVG_DEFS_TAG,
                        SVG_GROUP_TAG, SVG_MASK_TAG)
from ..utils.settings import DEFAULT_METADATA, global_settings

SVG_METADATA_TAG = inkex.addNS("metadata", "svg")


def strip_namespace(tag):
    """Remove xml namespace from a tag name.

    >>> {http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview
    <<< namedview
    """

    match = re.match(r'^\{[^}]+\}(.+)$', tag)

    if match:
        return match.group(1)
    else:
        return tag


class InkStitchMetadata(MutableMapping):
    """Helper class to get and set inkstitch-specific metadata attributes.

    Operates on a document and acts like a dict.  Setting an item adds or
    updates a metadata element in the document.  Getting an item retrieves
    a metadata element's text contents or None if an element by that name
    doesn't exist.
    """

    def __init__(self, document):
        super().__init__()
        self.document = document
        self.metadata = document.metadata

        for setting in DEFAULT_METADATA:
            if self[setting] is None:
                self[setting] = global_settings[f'default_{setting}']

    # Because this class inherints from MutableMapping, all we have to do is
    # implement these five methods and we get a full dict-like interface.

    def __setitem__(self, name, value):
        item = self._find_item(name)
        item.text = json.dumps(value)

    def _find_item(self, name, create=True):
        tag = inkex.addNS(name, "inkstitch")
        item = self.metadata.find(tag)
        if item is None and create:
            item = etree.SubElement(self.metadata, tag)

        return item

    def __getitem__(self, name):
        item = self._find_item(name)

        try:
            return json.loads(item.text)
        except (ValueError, TypeError):
            return None

    def __delitem__(self, name):
        item = self._find_item(name, create=False)

        if item is not None:
            self.metadata.remove(item)

    def __iter__(self):
        for child in self.metadata:
            if child.prefix == "inkstitch":
                yield strip_namespace(child.tag)

    def __len__(self):
        i = 0
        for i, item in enumerate(self):
            pass

        return i + 1

    def __json__(self):
        return dict(self)


class InkstitchExtension(inkex.Effect):
    """Base class for Inkstitch extensions.  Not intended for direct use."""

    @classmethod
    def name(cls):
        return snakecase(cls.__name__)

    def hide_all_layers(self):
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            if g.get(INKSCAPE_GROUPMODE) == "layer":
                g.set("style", "display:none")

    def get_current_layer(self):
        # if no layer is selected, inkex defaults to the root, which isn't
        # particularly useful
        current_layer = self.svg.get_current_layer()
        if current_layer is self.document.getroot():
            try:
                current_layer = self.document.xpath(".//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS)[0]
            except IndexError:
                # No layers at all??  Fine, we'll stick with the default.
                pass
        return current_layer

    def no_elements_error(self):
        if self.svg.selection:
            # l10n This was previously: "No embroiderable paths selected."
            inkex.errormsg(_("Ink/Stitch doesn't know how to work with any of the objects you've selected.") + "\n")
        else:
            inkex.errormsg(_("There are no objects in the entire document that Ink/Stitch knows how to work with.") + "\n")

        inkex.errormsg(_("Tip: Run Extensions > Ink/Stitch > Troubleshoot > Troubleshoot Objects") + "\n")

    def descendants(self, node, selected=False, troubleshoot=False):  # noqa: C901
        nodes = []

        if node.tag == Comment:
            return []

        element = EmbroideryElement(node)

        if element.has_command('ignore_object'):
            return []

        if node.tag == SVG_GROUP_TAG and node.get(INKSCAPE_GROUPMODE) == "layer":
            if len(list(layer_commands(node, "ignore_layer"))):
                return []

        if (node.tag in EMBROIDERABLE_TAGS or node.tag == SVG_GROUP_TAG) and element.get_style('display', 'inline') is None:
            return []

        # defs, masks and clippaths can contain embroiderable elements
        # but should never be rendered directly.
        if node.tag in [SVG_DEFS_TAG, SVG_MASK_TAG, SVG_CLIPPATH_TAG]:
            return []

        # command connectors with a fill color set, will glitch into the elements list
        if is_command(node) or node.get(CONNECTOR_TYPE):
            return []

        if self.svg.selection:
            if node.get("id") in self.svg.selection:
                selected = True
        else:
            # if the user didn't select anything that means we process everything
            selected = True

        for child in node:
            nodes.extend(self.descendants(child, selected, troubleshoot))

        if selected:
            if node.tag == SVG_GROUP_TAG:
                pass
            elif (node.tag in EMBROIDERABLE_TAGS or is_clone(node)) and not has_marker(node):
                nodes.append(node)
            # add images, text and elements with a marker for the troubleshoot extension
            elif troubleshoot and (node.tag in NOT_EMBROIDERABLE_TAGS or has_marker(node)):
                nodes.append(node)

        return nodes

    def get_nodes(self, troubleshoot=False):
        # Postorder traversal of selected nodes and their descendants.
        # Returns all nodes if there is no selection.
        return self.descendants(self.document.getroot(), troubleshoot=troubleshoot)

    def get_elements(self, troubleshoot=False):
        self.elements = nodes_to_elements(self.get_nodes(troubleshoot))
        if self.elements:
            return True
        if not troubleshoot:
            self.no_elements_error()
        return False

    def elements_to_stitch_groups(self, elements):
        patches = []
        for element in elements:
            if patches:
                last_patch = patches[-1]
            else:
                last_patch = None

            patches.extend(element.embroider(last_patch))

        return patches

    def get_inkstitch_metadata(self):
        return InkStitchMetadata(self.svg)

    def get_base_file_name(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")

        return os.path.splitext(svg_filename)[0]

    def uniqueId(self, prefix, make_new_id=True):
        """Override inkex.Effect.uniqueId with a nicer naming scheme."""
        return generate_unique_id(self.document, prefix)
