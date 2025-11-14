# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, Circle, Group, PathElement
from shapely.geometry import box

from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from ..svg.tags import INKSCAPE_LABEL, SVG_GROUP_TAG
from .base import InkstitchExtension


class MultiHoop(InkstitchExtension):
    """Split large designs across multiple hoops with registration marks.

    This extension helps embroider designs larger than your hoop by
    splitting them into sections with alignment markers.
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--hoop_width_mm", type=float, default=100.0,
                                     help="Hoop width (mm)")
        self.arg_parser.add_argument("--hoop_height_mm", type=float, default=100.0,
                                     help="Hoop height (mm)")
        self.arg_parser.add_argument("--overlap_mm", type=float, default=10.0,
                                     help="Overlap between hoops (mm)")
        self.arg_parser.add_argument("--add_registration", type=Boolean, default=True,
                                     help="Add registration marks")
        self.arg_parser.add_argument("--mark_size_mm", type=float, default=5.0,
                                     help="Registration mark size (mm)")

    def effect(self):
        if not self.get_elements():
            return

        # Calculate bounding box of all elements
        bbox = self._get_design_bbox()
        if not bbox:
            self.errormsg(_("No elements found to split"))
            return

        # Calculate hoop grid
        hoops = self._calculate_hoop_grid(bbox)

        if len(hoops) == 1:
            self.msg(_("Design fits in single hoop - no splitting needed"))
            return

        # Create hoop sections
        self._create_hoop_sections(hoops)

        self.msg(_(f"Design split into {len(hoops)} hoop sections"))

    def _get_design_bbox(self):
        """Get bounding box of all selected elements."""
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for element in self.elements:
            try:
                shape = element.shape
                bounds = shape.bounds  # (minx, miny, maxx, maxy)
                min_x = min(min_x, bounds[0])
                min_y = min(min_y, bounds[1])
                max_x = max(max_x, bounds[2])
                max_y = max(max_y, bounds[3])
            except Exception:
                continue

        if min_x == float('inf'):
            return None

        return (min_x, min_y, max_x, max_y)

    def _calculate_hoop_grid(self, bbox):
        """Calculate grid of hoops needed to cover the design."""
        min_x, min_y, max_x, max_y = bbox
        design_width = max_x - min_x
        design_height = max_y - min_y

        hoop_width = self.options.hoop_width_mm * PIXELS_PER_MM
        hoop_height = self.options.hoop_height_mm * PIXELS_PER_MM
        overlap = self.options.overlap_mm * PIXELS_PER_MM

        # Calculate number of hoops needed
        effective_width = hoop_width - overlap
        effective_height = hoop_height - overlap

        cols = max(1, int((design_width + effective_width - 1) / effective_width))
        rows = max(1, int((design_height + effective_height - 1) / effective_height))

        # Generate hoop positions
        hoops = []
        for row in range(rows):
            for col in range(cols):
                hoop_x = min_x + col * effective_width
                hoop_y = min_y + row * effective_height

                hoops.append({
                    'row': row,
                    'col': col,
                    'x': hoop_x,
                    'y': hoop_y,
                    'width': hoop_width,
                    'height': hoop_height
                })

        return hoops

    def _create_hoop_sections(self, hoops):
        """Create separate layers for each hoop section."""
        svg_root = self.document.getroot()

        for i, hoop in enumerate(hoops):
            # Create layer for this hoop
            layer = Group()
            layer.set(INKSCAPE_LABEL, f"Hoop {i+1} (Row {hoop['row']+1}, Col {hoop['col']+1})")
            layer.set('inkscape:groupmode', 'layer')

            # Add hoop boundary rectangle
            self._add_hoop_boundary(layer, hoop)

            # Add registration marks
            if self.options.add_registration:
                self._add_registration_marks(layer, hoop)

            # Clone elements that fall within this hoop
            self._clone_elements_in_hoop(layer, hoop)

            svg_root.append(layer)

    def _add_hoop_boundary(self, layer, hoop):
        """Add a rectangle showing the hoop boundary."""
        rect = PathElement()
        x, y = hoop['x'], hoop['y']
        w, h = hoop['width'], hoop['height']

        path_d = f"M {x},{y} L {x+w},{y} L {x+w},{y+h} L {x},{y+h} Z"
        rect.set('d', path_d)
        rect.set('style', 'fill:none;stroke:#cccccc;stroke-width:1;stroke-dasharray:5,5')
        rect.set(INKSCAPE_LABEL, 'Hoop Boundary')
        rect.set('inkstitch:ignore_object', 'true')

        layer.append(rect)

    def _add_registration_marks(self, layer, hoop):
        """Add registration marks at corners of hoop."""
        mark_size = self.options.mark_size_mm * PIXELS_PER_MM
        x, y = hoop['x'], hoop['y']
        w, h = hoop['width'], hoop['height']

        # Cross marks at each corner
        corners = [
            (x, y),  # Top-left
            (x + w, y),  # Top-right
            (x, y + h),  # Bottom-left
            (x + w, y + h)  # Bottom-right
        ]

        for cx, cy in corners:
            # Horizontal line
            h_line = PathElement()
            h_line.set('d', f"M {cx-mark_size},{cy} L {cx+mark_size},{cy}")
            h_line.set('style', 'fill:none;stroke:#ff0000;stroke-width:0.5')
            h_line.set('inkstitch:running_stitch_length_mm', '1.0')
            layer.append(h_line)

            # Vertical line
            v_line = PathElement()
            v_line.set('d', f"M {cx},{cy-mark_size} L {cx},{cy+mark_size}")
            v_line.set('style', 'fill:none;stroke:#ff0000;stroke-width:0.5')
            v_line.set('inkstitch:running_stitch_length_mm', '1.0')
            layer.append(v_line)

    def _clone_elements_in_hoop(self, layer, hoop):
        """Clone design elements that intersect with this hoop."""
        hoop_box = box(
            hoop['x'],
            hoop['y'],
            hoop['x'] + hoop['width'],
            hoop['y'] + hoop['height']
        )

        for element in self.elements:
            try:
                shape = element.shape
                if shape.intersects(hoop_box):
                    # Clone the original node
                    cloned = element.node.duplicate()
                    layer.append(cloned)
            except Exception:
                continue
