# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
from pathlib import Path

from inkex import Group, PathElement

from ..i18n import _
from ..svg.tags import INKSCAPE_LABEL
from .base import InkstitchExtension


class DesignLibrary(InkstitchExtension):
    """Browse and insert designs from the built-in library.

    This extension provides access to a library of pre-made embroidery designs
    that can be inserted into your document.
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--category", type=str, default="all",
                                     help="Design category")
        self.arg_parser.add_argument("--design_name", type=str, default="",
                                     help="Design to insert")

    def effect(self):
        # Create library directory structure if it doesn't exist
        library_path = self._get_library_path()
        library_path.mkdir(parents=True, exist_ok=True)

        # Create sample designs if library is empty
        if not list(library_path.glob("*.svg")):
            self._create_sample_designs(library_path)

        if self.options.design_name:
            self._insert_design(self.options.design_name)
        else:
            self._show_library_info()

    def _get_library_path(self):
        """Get path to design library."""
        extension_dir = Path(__file__).parent.parent.parent
        return extension_dir / "designs" / "library"

    def _create_sample_designs(self, library_path):
        """Create sample designs for the library."""
        # Sample 1: Simple flower
        flower_path = library_path / "flower_simple.svg"
        flower_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.inkscape.org/namespace/inkscape" xmlns:svg="http://www.w3.org/2000/svg">
  <g inkscape:label="Flower">
    <circle cx="0" cy="0" r="20" style="fill:#ff0000;stroke:none" inkstitch:fill_angle="45"/>
    <circle cx="-15" cy="-15" r="10" style="fill:#ffff00;stroke:none"/>
    <circle cx="15" cy="-15" r="10" style="fill:#ffff00;stroke:none"/>
    <circle cx="15" cy="15" r="10" style="fill:#ffff00;stroke:none"/>
    <circle cx="-15" cy="15" r="10" style="fill:#ffff00;stroke:none"/>
    <circle cx="0" cy="-18" r="10" style="fill:#ffff00;stroke:none"/>
  </g>
</svg>'''
        flower_path.write_text(flower_svg)

        # Sample 2: Star
        star_path = library_path / "star.svg"
        star_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.inkscape.org/namespace/inkscape" xmlns:svg="http://www.w3.org/2000/svg">
  <g inkscape:label="Star">
    <path d="M 0,-25 L 7,-8 L 25,-8 L 10,3 L 16,20 L 0,8 L -16,20 L -10,3 L -25,-8 L -7,-8 Z"
          style="fill:#0000ff;stroke:none" inkstitch:fill_angle="0"/>
  </g>
</svg>'''
        star_path.write_text(star_svg)

        # Sample 3: Heart
        heart_path = library_path / "heart.svg"
        heart_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.inkscape.org/namespace/inkscape" xmlns:svg="http://www.w3.org/2000/svg">
  <g inkscape:label="Heart">
    <path d="M 0,10 C -20,30 -40,10 -20,-10 C -10,-20 0,-15 0,-15 C 0,-15 10,-20 20,-10 C 40,10 20,30 0,10 Z"
          style="fill:#ff00ff;stroke:none" inkstitch:fill_angle="90"/>
  </g>
</svg>'''
        heart_path.write_text(heart_svg)

    def _insert_design(self, design_name):
        """Insert a design from the library into the document."""
        library_path = self._get_library_path()
        design_file = library_path / f"{design_name}.svg"

        if not design_file.exists():
            self.errormsg(_(f"Design '{design_name}' not found in library."))
            return

        try:
            # Read the design SVG
            from lxml import etree
            design_doc = etree.parse(str(design_file))
            design_root = design_doc.getroot()

            # Get or create current layer
            current_layer = self.get_current_layer()

            # Import all elements from the design
            for element in design_root:
                # Clone the element
                imported = element
                current_layer.append(imported)

            self.msg(_(f"Inserted design: {design_name}"))

        except Exception as e:
            self.errormsg(_(f"Error loading design: {str(e)}"))

    def _show_library_info(self):
        """Show information about available designs."""
        library_path = self._get_library_path()
        designs = [f.stem for f in library_path.glob("*.svg")]

        if not designs:
            self.msg(_("Design library is empty. Creating sample designs..."))
            self._create_sample_designs(library_path)
            designs = [f.stem for f in library_path.glob("*.svg")]

        message = _("Available designs:\n\n")
        for design in sorted(designs):
            message += f"- {design}\n"

        message += _("\n\nTo insert a design, select it from the extension menu.")

        self.msg(message)
