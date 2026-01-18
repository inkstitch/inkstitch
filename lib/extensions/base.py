# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import inkex

from ..elements import iterate_nodes, nodes_to_elements
from ..i18n import _
from ..metadata import InkStitchMetadata
from ..svg import generate_unique_id
from ..svg.tags import INKSCAPE_GROUPMODE, SVG_GROUP_TAG
from ..update import update_inkstitch_document


class InkstitchExtension(inkex.EffectExtension):
    """Base class for Inkstitch extensions.  Not intended for direct use."""

    # Set to True to hide this extension from release builds of Ink/Stitch.  It will
    # only be available in development installations.
    DEVELOPMENT_ONLY = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._skip_output = False

    def load(self, *args, **kwargs):
        document = super().load(*args, **kwargs)
        update_inkstitch_document(document)
        return document

    def write_file(self, filename):
        """Override write_file to skip output if _skip_output is set.
        
        This provides a safe way to prevent SVG output without calling sys.exit(),
        which can cause Inkscape to crash during document cleanup.
        """
        if not self._skip_output:
            super().write_file(filename)

    def skip_output(self):
        """Mark that the extension output should not be written to the SVG file.
        
        This is a safe alternative to sys.exit(0) that allows Inkscape to properly
        clean up the document without crashing.
        """
        self._skip_output = True

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

    def get_nodes(self, troubleshoot=False):
        # Postorder traversal of selected nodes and their descendants.
        # Returns all nodes if there is no selection.
        if self.svg.selection:
            selection = list(self.svg.selection)
        else:
            selection = None

        return iterate_nodes(self.document.getroot(), selection=selection, troubleshoot=troubleshoot)

    def get_elements(self, troubleshoot=False):
        self.elements = nodes_to_elements(self.get_nodes(troubleshoot))
        if self.elements:
            return True
        if not troubleshoot:
            self.no_elements_error()
        return False

    def elements_to_stitch_groups(self, elements):
        next_elements = [None]
        if len(elements) > 1:
            next_elements = elements[1:] + next_elements
        stitch_groups = []
        for element, next_element in zip(elements, next_elements):
            if stitch_groups:
                last_stitch_group = stitch_groups[-1]
            else:
                last_stitch_group = None

            stitch_groups.extend(element.embroider(last_stitch_group, next_element))

        return stitch_groups

    def get_inkstitch_metadata(self):
        return InkStitchMetadata(self.svg)

    def get_base_file_name(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'), "embroidery.svg")

        return os.path.splitext(svg_filename)[0]

    def uniqueId(self, prefix, make_new_id=True):
        """Override inkex.Effect.uniqueId with a nicer naming scheme."""
        return generate_unique_id(self.document, prefix)
