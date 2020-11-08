import json
import os
import re
from collections.abc import MutableMapping

import inkex
from lxml import etree
from stringcase import snakecase

from ..commands import is_command, layer_commands
from ..elements import EmbroideryElement, nodes_to_elements
from ..elements.clone import is_clone
from ..i18n import _
from ..svg import generate_unique_id
from ..svg.tags import (CONNECTOR_TYPE, EMBROIDERABLE_TAGS, INKSCAPE_GROUPMODE,
                        NOT_EMBROIDERABLE_TAGS, SVG_DEFS_TAG, SVG_GROUP_TAG)

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
        self.document = document
        self.metadata = self._get_or_create_metadata()

    def _get_or_create_metadata(self):
        metadata = self.document.find(SVG_METADATA_TAG)

        if metadata is None:
            metadata = inkex.etree.SubElement(self.document.getroot(), SVG_METADATA_TAG)

            # move it so that it goes right after the first element, sodipodi:namedview
            self.document.getroot().remove(metadata)
            self.document.getroot().insert(1, metadata)

        return metadata

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


class InkstitchExtension(inkex.Effect):
    """Base class for Inkstitch extensions.  Not intended for direct use."""

    @classmethod
    def name(cls):
        return snakecase(cls.__name__)

    def hide_all_layers(self):
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            if g.get(INKSCAPE_GROUPMODE) == "layer":
                g.set("style", "display:none")

    def ensure_current_layer(self):
        # if no layer is selected, inkex defaults to the root, which isn't
        # particularly useful
        if self.svg.get_current_layer() is self.document.getroot():
            try:
                self.current_layer = self.document.xpath(".//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS)[0]
            except IndexError:
                # No layers at all??  Fine, we'll stick with the default.
                pass

    def no_elements_error(self):
        if self.svg.selected:
            # l10n This was previously: "No embroiderable paths selected."
            inkex.errormsg(_("Ink/Stitch doesn't know how to work with any of the objects you've selected.") + "\n")
        else:
            inkex.errormsg(_("There are no objects in the entire document that Ink/Stitch knows how to work with.") + "\n")

        inkex.errormsg(_("Tip: Select some objects and use Path -> Object to Path to convert them to paths.") + "\n")

    def descendants(self, node, selected=False, troubleshoot=False):  # noqa: C901
        nodes = []
        element = EmbroideryElement(node)

        if element.has_command('ignore_object'):
            return []

        if node.tag == SVG_GROUP_TAG and node.get(INKSCAPE_GROUPMODE) == "layer":
            if len(list(layer_commands(node, "ignore_layer"))):
                return []

        if element.has_style('display') and element.get_style('display') is None:
            return []

        if node.tag == SVG_DEFS_TAG:
            return []

        # command connectors with a fill color set, will glitch into the elements list
        if is_command(node) or node.get(CONNECTOR_TYPE):
            return[]

        if self.svg.selected:
            if node.get("id") in self.svg.selected:
                selected = True
        else:
            # if the user didn't select anything that means we process everything
            selected = True

        for child in node:
            nodes.extend(self.descendants(child, selected, troubleshoot))

        if selected:
            if getattr(node, "get_path", None):
                nodes.append(node)
            elif troubleshoot and (node.tag in NOT_EMBROIDERABLE_TAGS or node.tag in EMBROIDERABLE_TAGS or is_clone(node)):
                nodes.append(node)

        return nodes

    def get_nodes(self, troubleshoot=False):
        return self.descendants(self.document.getroot(), troubleshoot=troubleshoot)

    def get_elements(self, troubleshoot=False):
        self.elements = nodes_to_elements(self.get_nodes(troubleshoot))
        if self.elements:
            return True
        if not troubleshoot:
            self.no_elements_error()
        return False

    def elements_to_patches(self, elements):
        patches = []
        for element in elements:
            if patches:
                last_patch = patches[-1]
            else:
                last_patch = None

            patches.extend(element.embroider(last_patch))

        return patches

    def get_inkstitch_metadata(self):
        return InkStitchMetadata(self.document)

    def get_base_file_name(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")

        return os.path.splitext(svg_filename)[0]

    def uniqueId(self, prefix, make_new_id=True):
        """Override inkex.Effect.uniqueId with a nicer naming scheme."""
        return generate_unique_id(self.document, prefix)
