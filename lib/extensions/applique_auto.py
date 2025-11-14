# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, PathElement
from shapely.geometry import LineString
from shapely.ops import unary_union

from ..elements import FillStitch
from ..i18n import _
from ..svg import get_correction_transform, PIXELS_PER_MM
from ..svg.tags import INKSCAPE_LABEL, SVG_PATH_TAG
from .base import InkstitchExtension


class AppliquéAuto(InkstitchExtension):
    """Automatically convert fill shapes to appliqué designs.

    Appliqué is a technique where fabric pieces are sewn onto a base fabric.
    This extension creates:
    1. Placement line (shows where to place the fabric)
    2. Tack-down stitches (secures fabric to base)
    3. Cover stitch (covers the raw edges)
    """

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--placement_offset_mm", type=float, default=0.5,
                                     help="Offset for placement line (mm)")
        self.arg_parser.add_argument("--tackdown_type", type=str, default="zigzag",
                                     help="Type of tack-down stitch: zigzag or running")
        self.arg_parser.add_argument("--tackdown_offset_mm", type=float, default=1.0,
                                     help="Offset for tack-down stitches from edge (mm)")
        self.arg_parser.add_argument("--cover_width_mm", type=float, default=3.0,
                                     help="Width of cover satin stitch (mm)")
        self.arg_parser.add_argument("--keep_original", type=Boolean, default=False,
                                     help="Keep original fill object")

    def effect(self):
        if not self.svg.selected or not self.get_elements():
            self.no_elements_error()
            return

        fill_elements = [elem for elem in self.elements if isinstance(elem, FillStitch)]

        if not fill_elements:
            self.errormsg(_("Please select at least one fill object to convert to appliqué."))
            return

        for fill_element in fill_elements:
            self.create_applique(fill_element)

        if not self.options.keep_original:
            for fill_element in fill_elements:
                fill_element.node.getparent().remove(fill_element.node)

    def create_applique(self, fill_element):
        """Create appliqué elements from a fill shape."""
        shape = fill_element.shape
        parent = fill_element.node.getparent()
        transform = get_correction_transform(fill_element.node)

        # Get original position for insertion
        index = list(parent).index(fill_element.node)

        # 1. Create placement line (thinner, offset inward)
        placement_line = self._create_placement_line(
            shape,
            fill_element,
            transform,
            -self.options.placement_offset_mm * PIXELS_PER_MM
        )
        parent.insert(index, placement_line)

        # 2. Create tack-down stitches
        tackdown = self._create_tackdown(
            shape,
            fill_element,
            transform,
            -self.options.tackdown_offset_mm * PIXELS_PER_MM
        )
        parent.insert(index + 1, tackdown)

        # 3. Create cover stitch (satin column)
        cover = self._create_cover_stitch(
            shape,
            fill_element,
            transform
        )
        parent.insert(index + 2, cover)

    def _create_placement_line(self, shape, fill_element, transform, offset):
        """Create a placement line showing where to position the fabric."""
        try:
            offset_shape = shape.buffer(offset)
            if offset_shape.is_empty:
                offset_shape = shape
        except Exception:
            offset_shape = shape

        path_d = self._shape_to_path_d(offset_shape)

        path = PathElement()
        path.set('d', path_d)
        path.set('transform', transform)
        path.set('style', 'fill:none;stroke:#0000ff;stroke-width:0.5')
        path.set(INKSCAPE_LABEL, f"{fill_element.node.label or 'Object'} - Appliqué Placement")

        # Set Ink/Stitch parameters for running stitch
        path.set('inkstitch:running_stitch_length_mm', '2.5')

        return path

    def _create_tackdown(self, shape, fill_element, transform, offset):
        """Create tack-down stitches to secure the fabric."""
        try:
            offset_shape = shape.buffer(offset)
            if offset_shape.is_empty:
                offset_shape = shape
        except Exception:
            offset_shape = shape

        path_d = self._shape_to_path_d(offset_shape)

        path = PathElement()
        path.set('d', path_d)
        path.set('transform', transform)

        if self.options.tackdown_type == "zigzag":
            # Zigzag stitch
            path.set('style', 'fill:none;stroke:#00ff00;stroke-width:1.0')
            path.set('inkstitch:zigzag_spacing_mm', '2.0')
            path.set('inkstitch:running_stitch_length_mm', '1.5')
        else:
            # Running stitch
            path.set('style', 'fill:none;stroke:#00ff00;stroke-width:0.5')
            path.set('inkstitch:running_stitch_length_mm', '1.5')

        path.set(INKSCAPE_LABEL, f"{fill_element.node.label or 'Object'} - Appliqué Tack-down")

        return path

    def _create_cover_stitch(self, shape, fill_element, transform):
        """Create satin cover stitch for the appliqué edge."""
        path_d = self._shape_to_path_d(shape)

        path = PathElement()
        path.set('d', path_d)
        path.set('transform', transform)
        path.set('style', f'fill:none;stroke:#ff0000;stroke-width:{self.options.cover_width_mm}')
        path.set(INKSCAPE_LABEL, f"{fill_element.node.label or 'Object'} - Appliqué Cover")

        # Set Ink/Stitch parameters for satin
        path.set('inkstitch:satin_column', 'true')
        path.set('inkstitch:stroke_method', 'satin')

        return path

    def _shape_to_path_d(self, shape):
        """Convert a Shapely geometry to an SVG path d attribute."""
        from shapely.geometry import MultiPolygon, Polygon

        def polygon_to_path(polygon):
            coords = list(polygon.exterior.coords)
            if not coords:
                return ""

            path_parts = [f"M {coords[0][0]},{coords[0][1]}"]
            for x, y in coords[1:]:
                path_parts.append(f"L {x},{y}")
            path_parts.append("Z")

            # Add holes
            for interior in polygon.interiors:
                hole_coords = list(interior.coords)
                if hole_coords:
                    path_parts.append(f"M {hole_coords[0][0]},{hole_coords[0][1]}")
                    for x, y in hole_coords[1:]:
                        path_parts.append(f"L {x},{y}")
                    path_parts.append("Z")

            return " ".join(path_parts)

        if isinstance(shape, MultiPolygon):
            return " ".join(polygon_to_path(poly) for poly in shape.geoms if not poly.is_empty)
        elif isinstance(shape, Polygon):
            return polygon_to_path(shape)
        else:
            return ""
