import inkex
from .elements import AutoFill, Fill, Stroke, SatinColumn, Polyline, EmbroideryElement
from . import SVG_POLYLINE_TAG, SVG_GROUP_TAG, SVG_DEFS_TAG, INKSCAPE_GROUPMODE, EMBROIDERABLE_TAGS, PIXELS_PER_MM


class InkstitchExtension(inkex.Effect):
    """Base class for Inkstitch extensions.  Not intended for direct use."""

    def hide_all_layers(self):
        for g in self.document.getroot().findall(SVG_GROUP_TAG):
            if g.get(INKSCAPE_GROUPMODE) == "layer":
                g.set("style", "display:none")

    def no_elements_error(self):
            if self.selected:
                inkex.errormsg(_("No embroiderable paths selected."))
            else:
                inkex.errormsg(_("No embroiderable paths found in document."))
            inkex.errormsg(_("Tip: use Path -> Object to Path to convert non-paths before embroidering."))

    def descendants(self, node):
        nodes = []
        element = EmbroideryElement(node)

        if element.has_style('display') and element.get_style('display') is None:
            return []

        if node.tag == SVG_DEFS_TAG:
            return []

        for child in node:
            nodes.extend(self.descendants(child))

        if node.tag in EMBROIDERABLE_TAGS:
            nodes.append(node)

        return nodes

    def get_nodes(self):
        """Get all XML nodes, or just those selected

        effect is an instance of a subclass of inkex.Effect.
        """

        if self.selected:
            nodes = []
            for node in self.document.getroot().iter():
                if node.get("id") in self.selected:
                    nodes.extend(self.descendants(node))
        else:
            nodes = self.descendants(self.document.getroot())

        return nodes

    def detect_classes(self, node):
        if node.tag == SVG_POLYLINE_TAG:
            return [Polyline]
        else:
            element = EmbroideryElement(node)

            if element.get_boolean_param("satin_column"):
                return [SatinColumn]
            else:
                classes = []

                if element.get_style("fill"):
                    if element.get_boolean_param("auto_fill", True):
                        classes.append(AutoFill)
                    else:
                        classes.append(Fill)

                if element.get_style("stroke"):
                    classes.append(Stroke)

                if element.get_boolean_param("stroke_first", False):
                    classes.reverse()

                return classes


    def get_elements(self):
        self.elements = []
        for node in self.get_nodes():
            classes = self.detect_classes(node)
            self.elements.extend(cls(node) for cls in classes)

        if self.elements:
            return True
        else:
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
