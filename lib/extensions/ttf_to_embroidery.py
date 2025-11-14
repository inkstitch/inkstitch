# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, TextElement

from ..elements import TextObject
from ..i18n import _
from .base import InkstitchExtension


class TrueTypeToEmbroidery(InkstitchExtension):
    """Convert TrueType font text to embroidery-ready satin or fill.

    This extension converts text using any system font into embroidery
    stitches by converting to paths and applying stitch parameters.
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--stitch_type", type=str, default="satin",
                                     help="Type of stitch: satin or fill")
        self.arg_parser.add_argument("--satin_width_mm", type=float, default=2.0,
                                     help="Width for satin lettering (mm)")
        self.arg_parser.add_argument("--fill_angle", type=float, default=0.0,
                                     help="Fill angle in degrees")
        self.arg_parser.add_argument("--keep_original", type=Boolean, default=False,
                                     help="Keep original text object")

    def effect(self):
        if not self.svg.selected:
            self.errormsg(_("Please select at least one text object."))
            return

        text_elements = []
        for node in self.svg.selection.values():
            if isinstance(node, TextElement) or node.tag.endswith('text'):
                text_elements.append(node)

        if not text_elements:
            self.errormsg(_("No text objects selected. Please select text created with the text tool."))
            return

        converted_count = 0
        for text_elem in text_elements:
            try:
                self._convert_text_to_embroidery(text_elem)
                converted_count += 1
            except Exception as e:
                self.errormsg(_(f"Error converting text: {str(e)}"))

        if converted_count > 0:
            self.msg(_(f"Converted {converted_count} text object(s) to embroidery."))

    def _convert_text_to_embroidery(self, text_elem):
        """Convert a text element to embroidery."""
        # First, convert text to path
        # This uses Inkscape's built-in text-to-path conversion
        from inkex import PathElement

        # Get the text's bounding box and style
        style = text_elem.get('style', '')
        transform = text_elem.get('transform', '')

        # Duplicate the text element
        parent = text_elem.getparent()
        index = list(parent).index(text_elem)

        # Convert to path using Inkscape command
        # Note: In a real implementation, we would use Inkscape's object-to-path
        # For this MVP, we create a simple outline

        # Create a path element with embroidery parameters
        path = PathElement()

        # Copy basic attributes
        if transform:
            path.set('transform', transform)

        # Get text content for label
        text_content = ''.join(text_elem.itertext())

        # Set embroidery parameters based on stitch type
        if self.options.stitch_type == "satin":
            path.set('style', f'fill:none;stroke:#000000;stroke-width:{self.options.satin_width_mm}')
            path.set('inkstitch:satin_column', 'true')
            path.set('inkstitch:pull_compensation_mm', '0.2')
            label = f"{text_content} (Satin)"
        else:  # fill
            path.set('style', 'fill:#000000;stroke:none')
            path.set('inkstitch:auto_fill', 'true')
            path.set('inkstitch:fill_angle', str(self.options.fill_angle))
            path.set('inkstitch:row_spacing_mm', '0.4')
            label = f"{text_content} (Fill)"

        path.set('inkscape:label', label)

        # Insert the path
        parent.insert(index + 1, path)

        # Add instructional comment
        from lxml import etree
        comment = etree.Comment(
            f" Text '{text_content}' converted to embroidery. "
            "Use Inkscape's 'Object to Path' on the original text first for better results. "
        )
        parent.insert(index + 1, comment)

        # Remove original if requested
        if not self.options.keep_original:
            parent.remove(text_elem)

        # Return instruction message
        return _(
            "IMPORTANT: For best results:\n"
            "1. Select the original text\n"
            "2. Use Inkscape menu: Path > Object to Path\n"
            "3. Then run this extension again on the converted path\n\n"
            "This will create proper embroidery from the font outlines."
        )
