# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import inkex
from lxml.etree import Comment
from multiprocessing import Pool
from typing import List, Tuple

from ..commands import is_command, layer_commands
from ..elements import EmbroideryElement, nodes_to_elements
from ..elements.clone import is_clone
from ..i18n import _
from ..marker import has_marker
from ..metadata import InkStitchMetadata
from ..svg import generate_unique_id
from ..svg.tags import (CONNECTOR_TYPE, EMBROIDERABLE_TAGS, INKSCAPE_GROUPMODE,
                        NOT_EMBROIDERABLE_TAGS, SVG_CLIPPATH_TAG, SVG_DEFS_TAG,
                        SVG_GROUP_TAG, SVG_MASK_TAG)
from ..update import update_inkstitch_document
from ..stitch_plan import StitchGroup
from ..debug.debug import debug


class InkstitchExtension(inkex.EffectExtension):
    """Base class for Inkstitch extensions.  Not intended for direct use."""

    def load(self, *args, **kwargs):
        document = super().load(*args, **kwargs)
        update_inkstitch_document(document)
        return document

    @classmethod
    def name(cls):
        # Convert CamelCase to snake_case
        return cls.__name__[0].lower() + ''.join([x if x.islower() else f'_{x.lower()}'
                                                  for x in cls.__name__[1:]])

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
            inkex.errormsg(_("Ink/Stitch doesn't know how to work with any of the objects you've selected. "
                             "Please check if selected elements are visible.") + "\n")
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
            if node in list(self.svg.selection):
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

    def elements_to_stitch_groups(self, elements: List[EmbroideryElement]) -> List[StitchGroup]:
        if len(elements) == 0:
            return []

        # Because the embroidery processeses are implemented largely in python, the best way to get parallelism is multiprocessing
        # to sidestep the GIL. To make this happen we need to do a little setup.

        # Unfortunately you can't pass inkex/lxml elements to multiprocessing because they aren't pickleable,
        # and because EmbroideryElement has one of those as a member, it in turn is not pickleable.
        # To get around this, we give the xml document to each worker thread, and pass each element as a tuple
        # of (xpath to the element, element class) so it can be instantiated in the worker thread.
        def serialize_element(e):
            return (self.svg.getroottree().getpath(e.node), e.__class__)

        # We want to embroider each element as a seperate parallelizable task, but some elements (notably, fills with no user-defined
        # start command) are dependent on the last stitch location of the previous element. As such, we instead break the
        # list of elements into "chains" of elements which are dependent on the element before them (based on uses_previous_stitch).
        chains = []
        g = [serialize_element(elements[0])]
        for element in elements[1:]:
            if element.uses_previous_stitch():
                g.append(serialize_element(element))
            else:
                chains.append(g)
                g = [serialize_element(element)]

        chains.append(g)
        debug.log(f"Multiprocessing: Elements: {len(elements)} Chain count: {len(chains)} Max chain size: {max(len(c) for c in chains)}")

        svg_str = self.svg.tostring()

        if len(chains) > 1:
            # Embroider each chain of independent elements in a seperate task: See mp_init and mp_chain_to_stitch_groups below
            with Pool(None, initializer=mp_init, initargs=[svg_str]) as p:
                # Chunk size 1 is usually ill-advised, but the amount of work each of these groups can vary wildly
                # depending on what elements they get, so it makes sense to keep the chunk size at 1 and have the
                # pool take elements one at a time rather than have threads stay idle
                stitch_group_chunks = p.map(mp_chain_to_stitch_groups, chains, 1)

            stitch_groups = []
            for chunk in stitch_group_chunks:
                stitch_groups.extend(chunk)

            return stitch_groups
        else:
            # If there are no truly independent stitch groups, just do it single-threaded to save on pool init/teardown.
            stitch_groups = []
            for element in elements:
                if stitch_groups:
                    last_stitch_group = stitch_groups[-1]
                else:
                    last_stitch_group = None

                stitch_groups.extend(element.embroider(last_stitch_group))

            return stitch_groups

    def get_inkstitch_metadata(self):
        return InkStitchMetadata(self.svg)

    def get_base_file_name(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")

        return os.path.splitext(svg_filename)[0]

    def uniqueId(self, prefix, make_new_id=True):
        """Override inkex.Effect.uniqueId with a nicer naming scheme."""
        return generate_unique_id(self.document, prefix)

# Multiprocessing methods, which need to be declared as top-level functions for the multiprocessing library
def mp_init(svg_str: str):
    """
    An init function called by each multiprocessing worker.
    Takes the SVG document as a string, and parses it to make it available for the worker tasks.
    """
    # The only real way to have multiprocessing tasks read something like this once is to make it a global.
    # Don't worry, it's only set as a global in the worker processes, not the main process...
    global doc
    doc = inkex.load_svg(svg_str)

def mp_chain_to_stitch_groups(elements: List[Tuple[str, type]]) -> List[StitchGroup]:
    """
    Returns a list of stitch groups given a set of embroidery elements (which depend on each other).
    Requires that the pool was passed mp_init as an initializer function.
    """
    global doc

    stitch_groups = []
    for path, cls in elements:
        if stitch_groups:
            last_stitch_group = stitch_groups[-1]
        else:
            last_stitch_group = None

        element = cls(doc.xpath(path)[0])

        stitch_groups.extend(element.embroider(last_stitch_group))

    return stitch_groups
